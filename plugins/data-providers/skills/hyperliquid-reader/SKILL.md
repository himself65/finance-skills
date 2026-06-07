---
name: hyperliquid-reader
description: >
  Read Hyperliquid (app.hyperliquid.xyz) perp + spot market data and any
  wallet's account state via opencli (read-only, public info API). Use
  whenever the user wants Hyperliquid perpetual or spot markets,
  mark/oracle/mid prices, 24h change, funding rates (hourly or annualized
  APR), open interest, volume, the L2 order book, OHLCV candles, historical
  funding, or a cross-venue funding comparison (Hyperliquid vs Binance vs
  Bybit) for funding arbitrage. Also use to read any address's Hyperliquid
  perp account (margin summary, open positions with entry/uPnL/leverage/
  liquidation price), spot balances, open orders, and recent fills by 0x
  address. Triggers: "Hyperliquid funding for BTC", "HL perp markets",
  "funding on BTC perp", "Hyperliquid order book", "HL open interest",
  "funding arb Hyperliquid vs Binance", "show Hyperliquid positions for
  0x...", "what is this wallet holding on HL", "Hyperliquid spot markets",
  "hyperliquid", "HL DEX". READ-ONLY — never places, modifies, or cancels
  orders, and never moves funds.
---

# Hyperliquid Reader (Read-Only)

Reads [Hyperliquid](https://app.hyperliquid.xyz) — the on-chain perps/spot DEX — for market data and account state via [opencli](https://github.com/jackwener/opencli) and the `hyperliquid` plugin in this repo's [`opencli-plugins/hyperliquid`](https://github.com/himself65/finance-skills/tree/main/opencli-plugins/hyperliquid) tree (a separate plugin from opencli's built-in adapters, installed via opencli's monorepo subpath syntax).

**This skill is read-only.** It reads Hyperliquid's fully public info API for analysis: market tables, funding, order book, candles, and any address's positions/orders/fills. It does NOT place, modify, or cancel orders, and never moves funds. There is no trading path in the plugin — order placement requires wallet-signed actions on a separate endpoint this adapter never calls.

**How it works**: every command issues a single `POST https://api.hyperliquid.xyz/info` with a `{ "type": "..." }` body and normalizes the response. **No API key, no wallet, no login, no running app** — the info API is public. Account data is read by public **0x address** (anyone's address; the user supplies whichever they want to inspect).

---

## Step 1: Ensure opencli + Plugin Are Installed and Ready

**Current environment status:**

```
!`(command -v opencli && opencli hyperliquid markets --coin BTC -f json 2>&1 | head -3 && echo "READY" || echo "SETUP_NEEDED") 2>/dev/null || echo "NOT_INSTALLED"`
```

If the status above shows `READY`, skip to Step 2. Otherwise:

### NOT_INSTALLED — Install opencli

```bash
npm install -g @jackwener/opencli
```

Requires Node.js >= 22 (built-in `fetch`).

### SETUP_NEEDED — Install the Hyperliquid plugin

The Hyperliquid adapter is **not** built into opencli — it's a separate plugin:

```bash
opencli plugin install github:himself65/finance-skills/hyperliquid
```

That's the entire setup — no auth, no launch step. Verify with `opencli hyperliquid markets --coin BTC`.

### Common setup issues

| Symptom | Fix |
|---|---|
| `opencli: command not found` | `npm install -g @jackwener/opencli` (Node ≥ 22) |
| `Unknown command: hyperliquid` | `opencli plugin install github:himself65/finance-skills/hyperliquid` |
| `hyperliquid info 429` | Rate limited — wait a few seconds and retry |
| `--user must be a 0x-prefixed 40-hex-char address` | Pass a full 42-char `0x…` address to account commands |

---

## Step 2: Identify What the User Needs

### Market data (no address required)

| User Request | Command | Key Flags |
|---|---|---|
| Perp markets overview / top by volume | `opencli hyperliquid markets` | `--sort`, `--limit`, `--coin` |
| One perp's price + funding + OI | `opencli hyperliquid markets --coin BTC` | — |
| Spot pairs overview | `opencli hyperliquid spot-markets` | `--sort`, `--limit`, `--pair`, `--canonical-only` |
| All current mid prices | `opencli hyperliquid mids` | `--coin <substring>` |
| Order book for a coin | `opencli hyperliquid book --coin ETH` | `--depth`, `--n-sig-figs` |
| OHLCV candles | `opencli hyperliquid candles --coin BTC --interval 1h` | `--limit` |
| Historical funding for a coin | `opencli hyperliquid funding-history --coin BTC` | `--hours`, `--limit` |
| Funding arb: HL vs Binance vs Bybit | `opencli hyperliquid funding-compare` | `--coin`, `--sort`, `--limit` |

### Account data (by 0x address — read any wallet)

| User Request | Command | Key Flags |
|---|---|---|
| Account value / margin summary | `opencli hyperliquid account --user 0x…` | — |
| Open perp positions | `opencli hyperliquid positions --user 0x…` | `--coin` |
| Spot token balances | `opencli hyperliquid spot-balances --user 0x…` | — |
| Resting open orders | `opencli hyperliquid open-orders --user 0x…` | `--coin` |
| Recent fills / trade history | `opencli hyperliquid fills --user 0x…` | `--coin`, `--limit` |

---

## Step 3: Execute the Command

### General pattern

```bash
# Use -f json or -f yaml for structured output
opencli hyperliquid markets --sort fundingAprPct --limit 15 -f json
opencli hyperliquid funding-compare --sort hlVsBinancePct --limit 20 -f md
opencli hyperliquid candles --coin BTC --interval 4h --limit 50 -f csv
opencli hyperliquid positions --user 0xABC...123 -f json
```

### Key rules

1. **Coin symbols are bare perp names** — `BTC`, `ETH`, `SOL`, `HYPE` (no exchange prefix). Spot pairs are `BASE/USDC` (e.g. `PURR/USDC`); for `book`/`candles` you can pass either a perp coin or a spot pair.
2. **`markets` is the default lens for "how is X / the market doing"** — it carries mark/oracle/mid price, 24h change, hourly funding + APR, open interest (coins and notional), and 24h volume in one row per perp. Filter with `--coin` for a single asset.
3. **Funding is reported two ways** — `fundingHrPct` is the raw hourly rate as a percent; `fundingAprPct` annualizes it (`hourly × 24 × 365`). Lead with APR when comparing carry across assets; use the hourly figure for "what will I pay next hour".
4. **`funding-compare` is the funding-arb screen** — it annualizes each venue with its own interval (HL hourly, Binance/Bybit usually 4h) and reports `hlVsBinancePct` / `hlVsBybitPct` spreads. Default sort ranks by **absolute** HL-vs-Binance spread (widest dislocations first). A positive `hlVsBinancePct` means HL longs pay more than Binance longs.
5. **`book` defaults to 10 levels per side** — raise `--depth` (max 20) for more, or `--n-sig-figs 2..5` to aggregate price levels. Compute the spread/mid from the top bid and ask.
6. **`candles` pulls the most recent `--limit` candles** of `--interval` (default `1h`, 100 candles). Valid intervals: `1m 3m 5m 15m 30m 1h 2h 4h 8h 12h 1d 3d 1w 1M`. Max 5000.
7. **Account commands need a full `0x` address** (42 chars). The skill reads *any* address — confirm whose wallet the user means if ambiguous. `positions`/`open-orders`/`fills` accept `--coin` to narrow to one asset.
8. **`fills` defaults to the 50 most recent** (API holds up to 2000). Raise `--limit` for deeper history; each row carries `closedPnl` and `fee`.
9. **`-f json`** for programmatic processing / feeding other skills; `-f md` or `-f table` for human-readable output.
10. **NEVER call any write operation.** This skill is read-only — no order placement, modification, or cancellation, and no transfers. The plugin intentionally exposes no write endpoints.

### Output format flag (`-f`)

| Format | Flag | Best for |
|---|---|---|
| Table | `-f table` (default) | Human-readable terminal output |
| JSON | `-f json` | Programmatic processing, LLM context |
| YAML | `-f yaml` | Structured, readable |
| Markdown | `-f md` | Reports |
| CSV | `-f csv` | Spreadsheet export |

### Output columns

- `markets` — `coin`, `markPx`, `midPx`, `oraclePx`, `change24hPct`, `fundingHrPct`, `fundingAprPct`, `openInterest`, `oiNotional`, `dayNtlVlm`, `premiumPct`, `maxLeverage`
- `spot-markets` — `pair`, `base`, `markPx`, `midPx`, `change24hPct`, `dayNtlVlm`, `circulatingSupply`, `marketCap`, `canonical`
- `mids` — `coin`, `mid`
- `book` — `side`, `level`, `px`, `sz`, `orders`
- `candles` — `time`, `open`, `high`, `low`, `close`, `volume`, `trades`
- `funding-history` — `coin`, `fundingRatePct`, `fundingAprPct`, `premiumPct`, `time`
- `funding-compare` — `coin`, `hlAprPct`, `binanceAprPct`, `bybitAprPct`, `hlVsBinancePct`, `hlVsBybitPct`, `nextHlFunding`
- `account` — `accountValue`, `totalNtlPos`, `totalRawUsd`, `totalMarginUsed`, `crossAccountValue`, `crossMaintenanceMarginUsed`, `withdrawable`, `numPositions`, `time`
- `positions` — `coin`, `side`, `size`, `entryPx`, `positionValue`, `unrealizedPnl`, `roePct`, `leverage`, `leverageType`, `liquidationPx`, `marginUsed`, `fundingSinceOpen`
- `spot-balances` — `coin`, `total`, `hold`, `available`, `entryNtl`
- `open-orders` — `coin`, `side`, `orderType`, `limitPx`, `sz`, `origSz`, `oid`, `tif`, `reduceOnly`, `triggerCondition`, `triggerPx`, `time`
- `fills` — `coin`, `dir`, `side`, `px`, `sz`, `notional`, `closedPnl`, `fee`, `feeToken`, `crossed`, `time`, `hash`

---

## Step 4: Present the Results

1. **Lead with the headline number, then the table.** For `markets --coin BTC`: state mark price, 24h change, funding APR, and open interest in prose first. For a full `markets` dump: lead with the count and the top movers / highest-funding names.
2. **Frame funding in carry terms** — e.g. "BTC perp funding is +10.9% APR (longs pay shorts)". Positive funding ⇒ longs pay shorts; negative ⇒ shorts pay longs.
3. **For `funding-compare`, surface the widest dislocations first** — name the coin, both venues' APRs, and the spread, and remember the spread is annualized; a real arb also pays exchange/withdrawal frictions, so present it as a screen, not a guaranteed edge.
4. **For `book`, report the spread** — best bid, best ask, mid, and spread in bps before (or instead of) dumping every level. Don't paste 20 levels unless asked.
5. **For `positions`, summarize the book** — total account value and uPnL first, then the largest positions by `positionValue`; flag any position whose `liquidationPx` is close to the current mark.
6. **For `candles`, describe the move** — first/last close, high/low, and direction; only show the full OHLCV table when the user wants the series.
7. **Filter aggressively before showing** — `markets` has ~180 perps and `mids` ~700 markets; cap to top 15-20 by the relevant sort unless the user asks for the full list.
8. **Treat addresses as the user provides them** — don't expose or guess wallet addresses; echo only what was supplied.
9. **Cross-reference for trade decisions** — Hyperliquid is the on-chain venue; for equities/options context pair it with the `funda-data` or `tradingview-reader` skills. For funding/basis trades, `funding-compare` plus `markets` (premium, OI) is the core view.

---

## Step 5: Diagnostics

```bash
opencli hyperliquid markets --coin BTC
```

A successful BTC row confirms opencli, the plugin, and the public API are all reachable. If it errors with `Unknown command: hyperliquid`, reinstall the plugin (Step 1). A `hyperliquid info 4xx/5xx` is an upstream API issue — retry after a short wait.

---

## Error Reference

| Error | Cause | Fix |
|---|---|---|
| `Unknown command: hyperliquid` | Plugin not installed | `opencli plugin install github:himself65/finance-skills/hyperliquid` |
| `hyperliquid info 429` | Rate limited | Wait a few seconds, then retry |
| `hyperliquid info 422/500` | Malformed body or upstream issue | Re-check the coin/interval; retry after a wait |
| `No perp market for coin "X"` | Wrong/unlisted symbol | Run `opencli hyperliquid markets` (or `mids`) to find the exact symbol |
| `--user must be a 0x-prefixed 40-hex-char address` | Bad/short address | Pass the full 42-char `0x…` address |
| Empty result for an address | Address has no Hyperliquid activity | Confirm the address actually trades on Hyperliquid |

---

## Reference Files

- `references/commands.md` — Every command with all flags, output schemas, and analyst workflows (funding carry, basis/arb, position monitoring)
