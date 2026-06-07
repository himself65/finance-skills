# Hyperliquid Reader — Command Reference

Every command issues a single `POST https://api.hyperliquid.xyz/info` and prints normalized rows. All are **read-only market data**, need no auth, and accept `-f json|yaml|md|csv|table`.

> Symbols: perps are bare names (`BTC`, `ETH`, `HYPE`); spot pairs are `BASE/USDC` (`PURR/USDC`). `book` and `candles` accept either.

---

## Market data

### `markets` — perpetual markets table

`metaAndAssetCtxs` → one row per perp.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (all) | Filter to one coin (exact, case-insensitive) |
| `--sort` | `dayNtlVlm` | One of `dayNtlVlm`, `change24hPct`, `fundingAprPct`, `fundingHrPct`, `openInterest`, `oiNotional`, `markPx`, `coin` (desc; `coin` asc). `null` sorts last |
| `--limit` | (all) | Max rows after sort |
| `--include-delisted` | `false` | Include delisted markets |

Columns: `coin`, `markPx`, `midPx`, `oraclePx`, `change24hPct`, `fundingHrPct`, `fundingAprPct`, `openInterest`, `oiNotional`, `dayNtlVlm`, `premiumPct`, `maxLeverage`.

- `fundingHrPct` — raw hourly funding rate as a percent.
- `fundingAprPct` — `hourly × 24 × 365` (annualized).
- `openInterest` — in coins; `oiNotional` — `openInterest × markPx` (USD).
- `premiumPct` — perp premium/discount vs oracle (mark-implied).

```bash
opencli hyperliquid markets --sort dayNtlVlm --limit 15
opencli hyperliquid markets --coin HYPE -f json
opencli hyperliquid markets --sort fundingAprPct --limit 20   # highest carry
```

### `spot-markets` — spot pairs table

`spotMetaAndAssetCtxs` → one row per spot pair.

| Flag | Default | Notes |
|---|---|---|
| `--pair` | (all) | Filter by pair or base token (e.g. `PURR` or `PURR/USDC`) |
| `--sort` | `dayNtlVlm` | One of `dayNtlVlm`, `change24hPct`, `marketCap`, `markPx`, `pair` |
| `--limit` | (all) | Max rows after sort |
| `--canonical-only` | `false` | Only named pairs (hide `@index` pairs) |

Columns: `pair`, `base`, `markPx`, `midPx`, `change24hPct`, `dayNtlVlm`, `circulatingSupply`, `marketCap`, `canonical`.

```bash
opencli hyperliquid spot-markets --canonical-only --sort dayNtlVlm --limit 20
opencli hyperliquid spot-markets --pair PURR -f json
```

### `mids` — all mid prices

`allMids` (+ `spotMeta` to resolve names) → `coin`, `mid` for every market.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (all) | Case-insensitive **substring** filter |

Non-canonical spot keys (`@<index>`) resolve to `BASE/QUOTE`; perp names and canonical pairs pass through; builder perp-dex keys (`#<n>`) are shown as-is.

```bash
opencli hyperliquid mids --coin BTC      # BTC, plus any pair containing "BTC"
opencli hyperliquid mids -f json | jq '.[] | select(.coin=="ETH")'
```

### `book` — L2 order book snapshot

`l2Book` → up to `--depth` levels per side, bids first then asks.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (required) | Coin or spot pair |
| `--depth` | `10` | Levels per side (1-20) |
| `--n-sig-figs` | (full) | Price aggregation, 2-5 |

Columns: `side` (`bid`/`ask`), `level`, `px`, `sz`, `orders`.

Spread = best ask − best bid; mid = their average. Top-of-book is `level: 1` on each side.

```bash
opencli hyperliquid book --coin ETH --depth 5
opencli hyperliquid book --coin BTC --n-sig-figs 3 -f json
```

### `candles` — OHLCV history

`candleSnapshot` → most recent `--limit` candles of `--interval`.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (required) | Coin or spot pair |
| `--interval` | `1h` | `1m 3m 5m 15m 30m 1h 2h 4h 8h 12h 1d 3d 1w 1M` |
| `--limit` | `100` | Number of candles (max 5000) |

Columns: `time` (ISO, candle open), `open`, `high`, `low`, `close`, `volume`, `trades`.

```bash
opencli hyperliquid candles --coin BTC --interval 4h --limit 60
opencli hyperliquid candles --coin SOL --interval 1d --limit 30 -f csv
```

### `funding-history` — historical funding for a coin

`fundingHistory` → hourly prints within the lookback window, newest first.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (required) | Coin (e.g. `BTC`) |
| `--hours` | `24` | Lookback window in hours |
| `--limit` | (all) | Cap to most recent N |

Columns: `coin`, `fundingRatePct`, `fundingAprPct`, `premiumPct`, `time`.

```bash
opencli hyperliquid funding-history --coin BTC --hours 72
opencli hyperliquid funding-history --coin ETH --hours 168 --limit 24 -f json
```

### `funding-compare` — cross-venue funding (arb screen)

`predictedFundings` → per coin, each venue's predicted funding annualized to APR, plus HL-vs-venue spreads.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (all) | Filter to one coin (exact) |
| `--sort` | `hlVsBinancePct` | `hlVsBinancePct`, `hlVsBybitPct` (by absolute spread), or `hlAprPct`, `binanceAprPct`, `bybitAprPct`, `coin` (signed) |
| `--limit` | (all) | Max rows after sort |

Columns: `coin`, `hlAprPct`, `binanceAprPct`, `bybitAprPct`, `hlVsBinancePct`, `hlVsBybitPct`, `nextHlFunding`.

Each venue is annualized with its own interval (HL hourly, Binance/Bybit usually 4h). `hlVsBinancePct = hlAprPct − binanceAprPct`; positive ⇒ HL longs pay more. Default sort surfaces the widest dislocations first. Treat as a screen — a real arb also pays exchange and transfer frictions.

```bash
opencli hyperliquid funding-compare --limit 20            # widest HL/Binance gaps
opencli hyperliquid funding-compare --coin BTC -f json
opencli hyperliquid funding-compare --sort hlAprPct --limit 15   # highest HL carry
```

---

## Analyst workflows

### Funding carry scan
1. `markets --sort fundingAprPct --limit 20` — highest (and, reversed mentally, lowest) annualized funding.
2. `funding-history --coin <X> --hours 168` — confirm the rate is persistent, not a one-hour spike.
3. `markets --coin <X>` — check open interest and premium to size whether the carry is tradeable.

### Cross-venue funding arbitrage
1. `funding-compare --limit 25` — widest HL-vs-Binance/Bybit dislocations.
2. For a candidate `<X>`: `funding-compare --coin <X>` for all three venues' APRs and the next HL funding time.
3. `book --coin <X>` and `markets --coin <X>` — verify depth and OI can support the size before treating the spread as real (it's annualized and ignores frictions).

### Basis / premium check
1. `markets --coin <X>` — `premiumPct` shows perp rich/cheap vs oracle; `markPx` vs `oraclePx` is the absolute basis.
2. `candles --coin <X> --interval 1h` — recent price action around the basis.

### Spot token snapshot
1. `spot-markets --canonical-only --sort dayNtlVlm` — most active named pairs.
2. `spot-markets --pair <BASE>` — price, 24h change, market cap for one token.
3. `book --coin <BASE>/USDC` — liquidity at top of book.
