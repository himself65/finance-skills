# robinhood-reader

Read-only reader for a user's [Robinhood](https://robinhood.com) brokerage
account via Robinhood's official **Agentic Trading MCP server**
(`https://agent.robinhood.com/mcp/trading`) — the integration announced at
[robinhood.com/us/en/agentic-trading](https://robinhood.com/us/en/agentic-trading/).

## What it does

After the user connects Robinhood's Trading MCP, this skill reads their account
using only the **read** tools the server exposes:

- **Accounts** — list of accounts (account numbers are masked in output)
- **Portfolio** — total value, asset-class breakdown, real-time buying power
- **Positions** — open equity positions with cost basis (for P&L)
- **Orders** — equity order history and status
- **Quotes & market data** — real-time equity quotes (batch ≤20 for prior closes), historical OHLCV series
- **Watchlists** — the user's watchlists, their contents, the options watchlist, and popular lists
- **Search** — resolve a company name to a ticker / instrument

> **Beta scope (verified June 2026).** A connected account currently exposes
> **equities + watchlists + search** only. Robinhood's docs also list option
> chains/quotes and index quotes, but those were **not** present on a live
> connection (agentic options are still rolling out) — so there is **no option
> chain, option quote, or implied-volatility data**, and an IV skew / options
> book must come from `tradingview-reader` or `funda-data`. The skill enumerates
> tools at runtime, so it picks up new reads automatically and keeps any new
> order tools on the denylist.

## ⚠️ Read-only by design — important

Robinhood's Agentic Trading MCP is a **trade-capable** server: the same
connection that exposes positions and balances also exposes tools that place
and cancel **real orders with real money**, and Robinhood enforces **no
server-side read-only mode**.

This skill's read-only guarantee is **self-imposed** — it calls only read tools
(`get_*`, `search`, …) and **never** calls any order/trade/state-changing tool
(`place_*`, `cancel_*`, `review_*`, `add_*`, `remove_*`, `create_*`, `follow_*`,
`unfollow_*`, `update_*`), even if asked. It verifies the live tool list at
runtime and treats unknown tools as forbidden. This matches the repository rule:
**no AI trade execution.**

For a hard boundary independent of the skill, keep the dedicated **Agentic
account unfunded** (or at the minimum balance) — trade writes are scoped to
that account, so with no buying power nothing can execute. Reads still work
across all accounts. Disconnect any time from the Robinhood app or with
`claude mcp remove robinhood-trading`.

## Authentication

OAuth, handled by Robinhood when you connect the MCP. Connecting prompts you to
open a dedicated **Agentic account** (desktop required) on top of an existing
primary individual investing account in good standing. Connecting grants the
agent read access across all your Robinhood accounts plus trade access scoped to
the Agentic account; this skill uses only the read half.

## Triggers

- "my Robinhood portfolio", "Robinhood positions", "what do I hold on Robinhood"
- "Robinhood account balance", "my buying power", "Robinhood order history"
- "my Robinhood watchlist", "check my Robinhood", "robinhood agent"
- "connect Robinhood MCP", "agentic trading"
- Any mention of reading data from a connected Robinhood account

**Not** for placing, modifying, or cancelling trades — those are out of scope.

## Platform

Works on **Claude Code** and other MCP-capable agents (Claude Desktop, ChatGPT,
Cursor, Codex). The account is in **beta** (US; equities live, options rolling
out). Account opening/authentication must be done on a **desktop** device.

## Setup

```bash
# As a plugin (recommended — installs all skills in this group)
npx plugins add himself65/finance-skills --plugin finance-data-providers

# Or install just this skill
npx skills add himself65/finance-skills --skill robinhood-reader
```

Then connect Robinhood's MCP server:

```bash
claude mcp add robinhood-trading --transport http https://agent.robinhood.com/mcp/trading
```

Run `/mcp` in Claude Code, select `robinhood-trading`, and authenticate. You may
need to restart the session before the tools register.

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- A Robinhood account with a primary individual investing account in good standing
- Completing Robinhood's Agentic account onboarding on a desktop device
- An MCP-capable agent (e.g. Claude Code)

## Reference files

- `references/tools.md` — Full read-tool catalog (parameters + output fields), the write-tool denylist, the runtime allowlisting rule, analyst workflows, and a note on the separate Robinhood banking/credit-card MCP.
