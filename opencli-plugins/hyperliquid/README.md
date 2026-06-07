# opencli-plugin-hyperliquid

Read-only [opencli](https://github.com/jackwener/opencli) adapter for **[Hyperliquid](https://app.hyperliquid.xyz)**, the on-chain perps/spot DEX. Exposes perp + spot market data — markets, mid prices, L2 order book, OHLCV candles, funding history, and a cross-venue funding-arb screen — all from Hyperliquid's **public info API**. No API key, no wallet, no login.

This plugin lives inside the [`himself65/finance-skills`](https://github.com/himself65/finance-skills) monorepo. Install it via opencli's monorepo subpath syntax:

```bash
opencli plugin install github:himself65/finance-skills/hyperliquid
```

## Install

```bash
# Prereqs: Node ≥ 22 (built-in fetch)
npm install -g @jackwener/opencli
opencli plugin install github:himself65/finance-skills/hyperliquid
```

**Zero setup.** Every command hits `https://api.hyperliquid.xyz/info` directly — no API key, no auth, no cookies, no running app.

## Commands

| Command | Description | Output columns |
|---|---|---|
| `hyperliquid markets` | Perp markets table | `coin`, `markPx`, `midPx`, `oraclePx`, `change24hPct`, `fundingHrPct`, `fundingAprPct`, `openInterest`, `oiNotional`, `dayNtlVlm`, `premiumPct`, `maxLeverage` |
| `hyperliquid spot-markets` | Spot pairs table | `pair`, `base`, `markPx`, `midPx`, `change24hPct`, `dayNtlVlm`, `circulatingSupply`, `marketCap`, `canonical` |
| `hyperliquid mids` | Mid price for every market | `coin`, `mid` |
| `hyperliquid book --coin BTC` | L2 order book snapshot | `side`, `level`, `px`, `sz`, `orders` |
| `hyperliquid candles --coin BTC` | OHLCV candles | `time`, `open`, `high`, `low`, `close`, `volume`, `trades` |
| `hyperliquid funding-history --coin BTC` | Historical hourly funding | `coin`, `fundingRatePct`, `fundingAprPct`, `premiumPct`, `time` |
| `hyperliquid funding-compare` | Cross-venue predicted funding (arb) | `coin`, `hlAprPct`, `binanceAprPct`, `bybitAprPct`, `hlVsBinancePct`, `hlVsBybitPct`, `nextHlFunding` |

`markets` flags: `--coin`, `--sort {dayNtlVlm|change24hPct|fundingAprPct|fundingHrPct|openInterest|oiNotional|markPx|coin}` (default `dayNtlVlm`), `--limit`, `--include-delisted`.

`spot-markets` flags: `--pair` (pair or base token), `--sort {dayNtlVlm|change24hPct|marketCap|markPx|pair}`, `--limit`, `--canonical-only`.

`book` flags: `--coin` (required), `--depth` (1-20, default 10), `--n-sig-figs` (2-5 price aggregation).

`candles` flags: `--coin` (required), `--interval {1m|3m|5m|15m|30m|1h|2h|4h|8h|12h|1d|3d|1w|1M}` (default `1h`), `--limit` (default 100, max 5000).

`funding-history` flags: `--coin` (required), `--hours` (default 24), `--limit`.

`funding-compare` flags: `--coin`, `--sort {hlVsBinancePct|hlVsBybitPct|hlAprPct|binanceAprPct|bybitAprPct|coin}` (default `hlVsBinancePct`, ranked by absolute spread), `--limit`.

All commands accept `-f json|yaml|md|csv|table`.

## Data path

Every command issues a single `POST https://api.hyperliquid.xyz/info` with a `{ "type": "..." }` body and normalizes the response:

| Command | info `type` |
|---|---|
| `markets` | `metaAndAssetCtxs` |
| `spot-markets` | `spotMetaAndAssetCtxs` |
| `mids` | `allMids` (+ `spotMeta` to resolve `@index` → pair name) |
| `book` | `l2Book` |
| `candles` | `candleSnapshot` |
| `funding-history` | `fundingHistory` |
| `funding-compare` | `predictedFundings` |

**Numbers** arrive as strings and are coerced to finite numbers (or `null`). **Funding** is reported per interval — Hyperliquid perps fund hourly, so APR = `rate × 24 × 365`; `funding-compare` annualizes each venue with its own interval (Binance/Bybit commonly 4h).

## Auth model

None. The info endpoint is fully public and read-only. There is **no** trading path in this plugin — placing/cancelling orders on Hyperliquid requires wallet-signed actions on the separate `/exchange` endpoint, which this adapter never calls.

## Status

**v0.1 — wire shapes verified live against `api.hyperliquid.xyz` (June 2026).** Pure-helper normalizers are unit-tested (`npm test`); the HTTP path is a single documented `POST /info` per command.

Known notes:
- `mids` resolves non-canonical spot keys (`@<index>`) to `BASE/QUOTE` via the token table; perp coin names and canonical pair names pass through unchanged, and builder-deployed perp-dex keys (`#<n>`) are surfaced as-is.
- `markets`/`spot-markets`/`funding-*` numeric sorts place `null` last.

## Layout

```
opencli-plugins/hyperliquid/
├── opencli-plugin.json        # plugin manifest
├── package.json               # Node package (type: module)
├── lib/
│   ├── api.js                 # infoFetch POST helper, num/pctChange/funding/isoTime helpers
│   ├── markets.js             # perp + spot market normalizers, allMids resolver
│   ├── funding.js             # funding history + cross-venue predicted-funding pivot
│   ├── book.js                # l2 book flattener + spread summary
│   └── candles.js             # interval table + OHLCV normalizer
├── markets.js                 # metaAndAssetCtxs → perp markets
├── spot-markets.js            # spotMetaAndAssetCtxs → spot pairs
├── mids.js                    # allMids → mid prices
├── book.js                    # l2Book → order book
├── candles.js                 # candleSnapshot → OHLCV
├── funding-history.js         # fundingHistory → historical funding
├── funding-compare.js         # predictedFundings → cross-venue arb screen
└── tests/
    ├── api.test.js            # num, pctChange, fundingToApr, isoTime
    ├── markets.test.js        # perp/spot normalizers, allMids resolver
    ├── funding.test.js        # funding history + cross-venue pivot/APR
    ├── book.test.js           # l2 flatten + spread
    └── candles.test.js        # OHLCV normalizer
```

## License

MIT
