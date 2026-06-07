# hyperliquid-reader

Read-only Hyperliquid market-data reader via [opencli](https://github.com/jackwener/opencli) + the [`hyperliquid`](../../../../opencli-plugins/hyperliquid/) opencli plugin shipped alongside this skill.

## What it does

Reads [Hyperliquid](https://app.hyperliquid.xyz)'s **public info API** — no API key, no wallet, no login, no scraping. Capabilities:

- **Perp markets** — mark/oracle/mid price, 24h change, hourly funding + annualized APR, open interest (coins + notional), and 24h volume for every perpetual
- **Spot markets** — pair price, 24h change, volume, circulating supply, market cap
- **Mids** — current mid price for every perp + spot market in one call
- **Order book** — L2 snapshot, top N levels per side, with spread
- **Candles** — OHLCV history for any interval (1m … 1M)
- **Funding history** — historical hourly funding (rate, APR, premium) per coin
- **Funding compare** — cross-venue predicted funding (Hyperliquid vs Binance vs Bybit), annualized, with spreads — a funding-arbitrage screen

**This skill is read-only and market-data only.** It does NOT read individual accounts, place/modify/cancel orders, or move funds.

## Authentication

None. Hyperliquid's `info` market-data endpoints are fully public — nothing to authenticate.

## Triggers

- "Hyperliquid funding for X", "what's the funding on BTC perp", "HL open interest"
- "Hyperliquid order book for ETH", "HL perp markets", "Hyperliquid spot markets"
- "funding arb Hyperliquid vs Binance", "Hyperliquid candles for SOL"
- "PURR price on Hyperliquid", "Hyperliquid mid prices"
- Any mention of Hyperliquid / app.hyperliquid.xyz / HL DEX in context of reading market data or funding

## Platform

Works on **Claude Code** and other CLI-based agents (any OS with Node ≥ 22). Does **not** work on Claude.ai — the sandbox restricts the network access opencli needs. Unlike the TradingView reader, there is no desktop-app or macOS dependency — it's a plain HTTP API.

## Setup

```bash
# As a plugin (recommended — installs all skills in this group)
npx plugins add himself65/finance-skills --plugin finance-data-providers

# Or install just this skill
npx skills add himself65/finance-skills --skill hyperliquid-reader
```

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- Node.js >= 22 — for `npm install -g @jackwener/opencli` and the plugin's built-in `fetch`
- The `hyperliquid` opencli plugin: `opencli plugin install github:himself65/finance-skills/hyperliquid` (installs from this repo's monorepo subpath)

No API key, no wallet, no launch step.

## Reference files

- `references/commands.md` — Complete market-data command reference with all flags, output schemas, and analyst workflows
