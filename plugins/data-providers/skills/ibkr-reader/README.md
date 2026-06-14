# ibkr-reader

Read-only reader for an [Interactive Brokers](https://www.interactivebrokers.com)
(IBKR) account via IBKR's official **Agentic MCP** connector.

## What it does

After the user connects IBKR's MCP, this skill reads their account and IBKR
market data using only the **read** tools the server exposes:

- **Account** — summary (net liquidation, margin), cash balances and buying power
- **Positions** — stock and option holdings with quantity + average cost
- **Orders & trades** — order status/history and execution fills
- **Quotes** — real-time snapshot: last, bid/ask, change, volume, day high/low/open
- **Volatility** — implied vol (underlying *and* per option contract), IV percentile, historical vol, put/call open interest and volume
- **History** — OHLCV price bars over a range or bar count
- **Contracts & research** — ticker/contract resolution, company themes, supply-chain connections, investment topics

## ⚠️ Read-only by design — important

IBKR's Agentic MCP is **trade-capable**: the same connection exposes tools that
place and cancel **real orders** (`create_order_instruction` /
`delete_order_instruction`), and there is no server-side read-only mode.

This skill's read-only guarantee is **self-imposed** — it calls only read tools
and **never** calls any order or state-changing tool (`create_*`/`delete_order_instruction`,
`provide_customer_feedback`), even if asked. It classifies the live tool list at
runtime and treats unknown tools as forbidden. This matches the repository rule:
**no AI trade execution.** For a hard boundary, authenticate with a
**paper-trading account**.

## Options: what works, what doesn't

IBKR **does** read option details — confirmed live: per-contract **implied
volatility** (`implied_vol` / `option_midpoint_iv`), underlying IV
(`implied_vol_underlying`), IV percentile, historical vol, and put/call OI/volume.

It **cannot** enumerate an option chain — `search_contracts` resolves the
underlying and flags `OPT` as available but returns no strikes/expiries/IDs, and
there are no greeks (IV only). So a **full multi-strike IV skew** can't be built
from IBKR alone; pair with `tradingview-reader` or `funda-data` for the per-strike
chain. IBKR is excellent for the **underlying IV regime**, IV percentile, put/call
skew, and **per-contract IV of positions you hold**.

## Authentication

OAuth, handled by IBKR when you connect the MCP. Connect via `/mcp` → select
**"claude.ai Interactive Brokers (IBKR)"** → authenticate. Market data follows
your IBKR market-data subscriptions (real-time vs delayed).

## Triggers

- "my IBKR account", "Interactive Brokers positions", "my IB portfolio"
- "IBKR balances", "IBKR buying power", "my IB orders", "IBKR trade history"
- "IBKR quote for X", "implied volatility on X via IBKR", "IBKR price history"
- Any mention of reading data from a connected Interactive Brokers account

**Not** for placing, modifying, or cancelling orders — those are out of scope.

## Platform

Works on **Claude Code** and other MCP-capable agents (including Claude.ai,
since IBKR is a claude.ai connector). Account authentication is via IBKR OAuth.

## Setup

```bash
# As a plugin (recommended — installs all skills in this group)
npx plugins add himself65/finance-skills --plugin finance-data-providers

# Or install just this skill
npx skills add himself65/finance-skills --skill ibkr-reader
```

Then connect IBKR: run `/mcp`, select **"claude.ai Interactive Brokers (IBKR)"**,
and authenticate. If the tools don't appear, run `/reload-plugins` or restart the
session.

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- An Interactive Brokers account (a paper-trading account works and keeps it read-only by construction)
- IBKR market-data subscriptions for live quotes/IV (otherwise data may be delayed or sparse)
- An MCP-capable agent (e.g. Claude Code)

## Reference files

- `references/tools.md` — Full read-tool catalog (params + output fields, complete `get_price_snapshot` field list), the write-tool denylist, the options capability/limitation detail, and analyst workflows.
