# barchart

Read-only Barchart skill for stock quotes, options chains, greeks, and unusual options flow using [opencli](https://github.com/jackwener/opencli).

## What it does

Fetches financial data from [Barchart](https://www.barchart.com) for research and analysis:

- **Stock quotes** — price, change, open/high/low, volume, avg volume, market cap, P/E, EPS
- **Options chains** — strike, bid/ask, last, volume, open interest, IV, and greeks (delta, gamma, theta, vega)
- **Greeks overview** — near-the-money greeks for both calls and puts (delta, gamma, theta, vega, rho)
- **Options flow** — unusual options activity sorted by volume/OI ratio, filterable by call/put

**This skill is read-only.** It does NOT support placing trades or modifying any data.

## Authentication

No API keys needed — opencli authenticates via your logged-in Chrome browser session on barchart.com.

## Triggers

- "barchart quote", "options chain from barchart", "options greeks"
- "unusual options activity", "options flow", "vol/OI ratio"
- "what's the flow on AAPL", "smart money", "institutional flow"
- Any mention of barchart.com data or options flow research

## Prerequisites

- Node.js 18+
- Chrome browser logged into [barchart.com](https://www.barchart.com)
- [Playwright MCP Bridge](https://chromewebstore.google.com/detail/playwright-mcp-bridge/iiejdkmfhfnogkgikpfoddjikfciaiob) Chrome extension

## Platform

Works on **Claude Code** and other CLI-based agents. Does **not** work on Claude.ai — the sandbox restricts network access and binaries required by opencli.

## Setup

```bash
npx skills add himself65/finance-skills --skill barchart
```

See the [main README](../../README.md) for more installation options.

## Reference files

- `references/commands.md` — Complete command reference with all flags, output columns, and usage examples
