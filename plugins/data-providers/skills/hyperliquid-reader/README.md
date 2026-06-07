# hyperliquid-reader

Read-only Hyperliquid market + account reader via [opencli](https://github.com/jackwener/opencli) + the [`hyperliquid`](../../../../opencli-plugins/hyperliquid/) opencli plugin shipped alongside this skill.

## What it does

Reads [Hyperliquid](https://app.hyperliquid.xyz)'s **public info API** — no API key, no wallet, no login, no scraping. Capabilities:

- **Perp markets** — mark/oracle/mid price, 24h change, hourly funding + annualized APR, open interest (coins + notional), and 24h volume for every perpetual
- **Spot markets** — pair price, 24h change, volume, circulating supply, market cap
- **Mids** — current mid price for every perp + spot market in one call
- **Order book** — L2 snapshot, top N levels per side, with spread
- **Candles** — OHLCV history for any interval (1m … 1M)
- **Funding history** — historical hourly funding (rate, APR, premium) per coin
- **Funding compare** — cross-venue predicted funding (Hyperliquid vs Binance vs Bybit), annualized, with spreads — a funding-arbitrage screen
- **Account / positions / spot balances / open orders / fills** — read **any** wallet's Hyperliquid state by its public 0x address

**This skill is read-only.** It does NOT place, modify, or cancel orders, and never moves funds.

## Authentication

None. Hyperliquid's `info` endpoint is fully public. Market data needs nothing; account data is read by public 0x address.

## Triggers

- "Hyperliquid funding for X", "what's the funding on BTC perp", "HL open interest"
- "Hyperliquid order book for ETH", "HL perp markets", "Hyperliquid spot markets"
- "funding arb Hyperliquid vs Binance", "Hyperliquid candles for SOL"
- "show Hyperliquid positions for 0x…", "what is this wallet holding on HL", "open orders on Hyperliquid for 0x…"
- Any mention of Hyperliquid / app.hyperliquid.xyz / HL DEX in context of reading market data, funding, or an account

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

- `references/commands.md` — Complete read command reference with all flags, output schemas, and analyst workflows
