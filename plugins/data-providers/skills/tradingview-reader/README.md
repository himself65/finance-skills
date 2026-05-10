# tradingview-reader

Read-only TradingView desktop reader for market data via [opencli](https://github.com/jackwener/opencli) + the [`tradingview`](../../../../opencli-plugins/tradingview/) opencli plugin shipped alongside this skill.

## What it does

Reads TradingView's macOS desktop app for market data via Chrome DevTools Protocol — no API keys, no cookie extraction, no scraping. Capabilities include:

- **Quote** — spot quote for any symbol (close, change, currency)
- **Options chain** — full chain or filtered by expiry / type / ATM band, with full greeks (delta, gamma, theta, vega, rho), IV, bid/ask IVs, and theoretical price
- **Options expiries** — list available expirations with DTE and contracts count
- **Chart state** — current symbol, interval, and layout of an active chart tab
- **Screenshot** — PNG capture of a chart tab
- **Status / launch** — CDP connection diagnostics and one-shot relaunch helper

**This skill is read-only.** It does NOT place trades, modify watchlists, post ideas, or change chart layouts.

## Authentication

No API key, no token. The adapter attaches to the user's already-logged-in TradingView desktop app over CDP. Just have `TradingView.app` installed and logged in.

## Triggers

- "options chain for X", "what's the IV on Y", "show me SNDK puts"
- "what's the bid/ask on AAPL options", "TradingView IV skew"
- "what symbol is on my TradingView chart", "screenshot my NVDA chart"
- "TradingView quote for", "TV options for", "what expiries does X have"
- Any mention of TradingView in context of reading market data, options data, or charts

## Platform

Works on **Claude Code** and other CLI-based agents on macOS. Does **not** work on Claude.ai — the sandbox restricts network access and binaries required by opencli + CDP.

The plugin is currently macOS-only (relies on `open -a TradingView --args`).

## Setup

```bash
# As a plugin (recommended — installs all skills in this group)
npx plugins add himself65/finance-skills --plugin finance-data-providers

# Or install just this skill
npx skills add himself65/finance-skills --skill tradingview-reader
```

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- Node.js >= 21 — for `npm install -g @jackwener/opencli`
- `TradingView.app` installed on macOS, logged in
- The `tradingview` opencli plugin: `opencli plugin install github:himself65/finance-skills/tradingview` (installs from this repo's monorepo subpath)
- Relaunch with CDP enabled: `opencli tradingview launch` (one-time per session — warn the user to save chart layouts first)

## Reference files

- `references/commands.md` — Complete read command reference with all flags, output schemas, and analyst workflows
