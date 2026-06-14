# Robinhood Trading MCP — Read-Tool Reference

Detailed reference for the **read-only** subset of Robinhood's Agentic Trading
MCP server (`https://agent.robinhood.com/mcp/trading`), exposed in Claude Code
as `mcp__robinhood-trading__<tool>` after the user connects and authenticates.

> **Source & accuracy.** Tool names below come from Robinhood's public
> "Trading with your agent" support article. Robinhood states it will keep
> adding tools, and exact runtime spellings may differ from the documented
> page (notably `get_equity-historicals`, which is documented with a hyphen).
> **Always trust the live tool registry over this list** — enumerate the tools
> the connected server actually exposes and classify each one read vs. write by
> its name and description before calling it.

---

## The read-only rule (non-negotiable)

This skill calls a tool **only** if it merely retrieves data. A tool is
forbidden if its name or description implies it **changes anything** — placing,
submitting, buying, selling, cancelling, replacing, modifying, previewing,
reviewing, adding, following, unfollowing, updating, creating, or deleting.
**Default unknown or ambiguous tools to forbidden.** There is no
server-enforced read-only mode; this allowlisting is the only thing keeping the
skill safe.

---

## Read tools (allowed)

### Account & portfolio

| Tool | Purpose | Notable output |
|---|---|---|
| `get_accounts` | List all the user's Robinhood accounts | Account types, account numbers (mask these in output), status |
| `get_portfolio` | Portfolio snapshot | Total value, breakdown by asset class, **real-time buying power** |
| `get_equity_positions` | Open stock positions | Symbol, quantity, average/cost basis (use with quotes for P&L) |
| `get_equity_orders` | Equity order history | Order status, side, type, quantity, price, timestamps |
| `get_equity_tradability` | Whether a symbol is tradable / fractionable | Tradable flag, fractional eligibility |

> Reads span **all** of the user's Robinhood accounts, not only the Agentic
> account. When summarizing, note which account(s) the data is from.

### Quotes & market data

| Tool | Purpose | Notes |
|---|---|---|
| `get_equity_quotes` | Real-time quotes + prior close | Accepts **up to 20 symbols** per call — batch them |
| `get_equity-historicals` | Historical price series for a symbol | Verify exact name at runtime (documented with a hyphen) |
| `get_indexes` | Index data | e.g. broad market indexes |
| `get_indexes_quotes` | Index quotes | Current index levels |
| `search` | Resolve a company name / partial string to a ticker | Use before quote/position calls when the user gives a name |

### Watchlists (read)

| Tool | Purpose |
|---|---|
| `get_watchlists` | The user's watchlists |
| `get_watchlist_items` | Contents of a watchlist |
| `get_popular_lists` | Robinhood's popular/curated lists |

### Options (read)

| Tool | Purpose |
|---|---|
| `get_option_chains` | Option chain for an underlying |
| `get_option_instruments` | Specific option contracts/instruments |
| `get_option_quotes` | Real-time option quotes |
| `get_option_positions` | Open option positions |
| `get_option_orders` | Option order history |

---

## Write tools — NEVER call (denylist)

These mutate state or place/cancel real orders with real money. They are out of
scope for this skill and for this repository (no AI trade execution).

| Category | Tools |
|---|---|
| Equity trade execution | `place_equity_order`, `cancel_equity_order` |
| Option trade execution | `place_option_order`, `cancel_option_order` |
| Order simulation (off-limits — write-intent, exists only to precede an order) | `review_equity_order`, `review_option_order` |
| Watchlist mutation | `add_to_watchlist`, `follow_list`, `unfollow_list`, `update_watchlist` |
| Any future tool | Anything whose name/description implies placing, cancelling, modifying, previewing, or changing — default to forbidden |

If the user asks to trade, rebalance, set up a recurring buy, or modify a
watchlist, **decline** and point them to the Robinhood app. Do not call a write
tool under any circumstance.

---

## Analyst workflows (read-only)

### Portfolio snapshot
1. `get_portfolio` → total value, asset-class split, buying power.
2. `get_equity_positions` (+ `get_option_positions` if relevant).
3. `get_equity_quotes` for the held symbols (batch ≤20) to compute live market
   value and unrealized P&L = (last − avg cost) × qty.
4. Present: headline totals first, then a positions table; mask account numbers.

### Position concentration
1. `get_equity_positions` + live quotes for market value per holding.
2. Compute each position's weight = market value / total equity value.
3. Flag concentration (e.g. any single name > 20%) — as an observation, not
   advice.

### Order / transaction audit
1. `get_equity_orders` (and `get_option_orders`) for status and fills.
2. Summarize by symbol/side/date; surface open/pending vs. filled/cancelled.
3. For a specific period, filter the returned orders by timestamp.

### Options book review
1. `get_option_positions` → open contracts (strike, expiry, side, qty).
2. `get_option_quotes` / `get_option_chains` for current marks and the
   surrounding chain.
3. Summarize exposure (e.g. net debit/credit, expirations approaching); pair
   with `tradingview-reader` or `funda-data` for greeks/IV context.

---

## Related: Robinhood Banking / Agentic Credit Card MCP (out of scope)

Robinhood ships a **separate** MCP for its Agentic Credit Card at
`https://banking-agent.robinhood.com/mcp/banking`. It is scoped only to
authorized agentic virtual cards (card transaction history, card policies, card
number details) and exists to let an agent complete purchases — it is **not**
covered by this skill. This skill is the **trading** reader only. If a user
wants card data, that is a different connector with its own onboarding, and any
purchase capability is again out of scope for read-only use.
