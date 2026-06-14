# Robinhood Trading MCP — Read-Tool Reference

Detailed reference for the **read-only** subset of Robinhood's Agentic Trading
MCP server (`https://agent.robinhood.com/mcp/trading`), exposed in Claude Code
as `mcp__robinhood-trading__<tool>` after the user connects and authenticates.

> **Source & accuracy.** The lists below were **confirmed against a live,
> authenticated connection (equities beta, June 2026)** — a full `tools/list`
> on a real account. This is narrower than Robinhood's public "Trading with your
> agent" support page, which also documents option chains/quotes and index
> quotes that were **not exposed** on the live connection. Robinhood is adding
> tools over time, and a different account/tier may differ — so **always
> classify what your own registry actually shows** and treat this as a seed.

---

## The read-only rule (non-negotiable)

This skill calls a tool **only** if it merely retrieves data. A tool is
forbidden if its name or description implies it **changes anything** — placing,
submitting, buying, selling, cancelling, replacing, modifying, previewing,
reviewing, adding, removing, creating, following, unfollowing, updating, or
deleting. **Default unknown or ambiguous tools to forbidden.** There is no
server-enforced read-only mode; this allowlisting is the only thing keeping the
skill safe.

---

## Read tools (allowed) — live equities-beta surface

### Account & portfolio

| Tool | Purpose | Params / notes |
|---|---|---|
| `get_accounts` | List the user's brokerage accounts | No params. Look up `account_number` here. Does **not** return reliable buying power — use `get_portfolio`. |
| `get_portfolio` | Portfolio value breakdown by asset type + **buying power** | `account_number` (required) |
| `get_equity_positions` | Open stock positions (symbol, quantity, average cost, hold breakdowns) | `account_number` (required); `cursor` paginates |
| `get_equity_orders` | Equity order history/status (open + closed, fills, cancels, rejects) | `account_number` (required); filter by `state`, `symbol`, `created_at_gte`, `placed_agent`; `order_id` for one order |
| `get_equity_tradability` | Per-session eligibility + fractional for up to 10 symbols | `account_number`, `symbols` (≤10, exact ticker) |

> **Per-account, not global.** Only `get_accounts` lists every account. The
> tools above each take an `account_number`. If the user has more than one
> account and didn't specify, present the list from `get_accounts` and ask which
> one — don't silently dump all accounts.

### Quotes & market data

| Tool | Purpose | Params / notes |
|---|---|---|
| `get_equity_quotes` | Real-time quotes + official prior-session close | `symbols` (array). Above 20 symbols the closes are omitted (`closes_error` set) — keep batches ≤20 if you need closes. |
| `get_equity_historicals` | OHLCV bars across a time range (charting, realized-vol, backtests) | `symbols` (≤10), `start_time` (RFC3339, required); optional `interval`, `bounds`, `end_time`, `adjustment_type`. Note the underscore — Robinhood's docs render this hyphenated, but the live tool is `get_equity_historicals`. |
| `search` | Resolve a name/partial/ticker to an instrument, crypto pair, or index | `query` (required); `asset_type` = `instrument` (default) / `currency_pair` / `market_index`; `limit` ≤20. Resolving a `market_index` returns a *reference* only — you cannot quote it on this connection (no `get_indexes_quotes`). |

**`get_equity_quotes` output fields:** `last_trade_price`,
`last_non_reg_trade_price` (+ their venue timestamps), `previous_close`,
`adjusted_previous_close`, `bid_price`/`ask_price`, `has_traded`, `state`, plus
a paired `close` object (official settled close). Pick whichever of
`last_trade_price` / `last_non_reg_trade_price` has the more recent timestamp;
daily change uses `adjusted_previous_close`; drop bid/ask when zero; surface
`has_traded=false` or a non-`active` state before quoting a price.

### Watchlists (read)

| Tool | Purpose | Params / notes |
|---|---|---|
| `get_watchlists` | The user's custom + followed curated lists (with `list_id`s) | No params |
| `get_watchlist_items` | Items in a list (stocks/ETFs/crypto/indexes by `object_type`) | `list_id` (required). Does not return live prices — call `get_equity_quotes`. |
| `get_popular_watchlists` | Robinhood-curated lists the user can follow | No params (docs call this `get_popular_lists`; live tool is `get_popular_watchlists`) |
| `get_option_watchlist` | Single-leg option contracts saved to the options watchlist | No params. **Contract references only — no quotes, greeks, or IV.** Returns `option_ids` meant to be passed to `get_option_quotes`, which is not exposed here (see below). |

---

## Option & index market data — NOT exposed on this connection

This is the key real-world finding. On the live equities-beta connection, the
following tools **do not exist** even though other tools' descriptions reference
them (e.g. `add_option_to_watchlist` says "source option_ids from
`get_option_instruments`", and `get_option_watchlist` says to pass ids to
`get_option_quotes`):

- `get_option_chains`, `get_option_instruments`, `get_option_quotes`
- `get_option_positions`, `get_option_orders`
- `get_indexes`, `get_indexes_quotes`

**Consequence:** you cannot read an option chain, an option contract's quote, or
its implied volatility / greeks from this connection — so **an IV skew, an
options book, or any per-contract option flow is not obtainable here.** The only
option tools present are watchlist helpers (`get_option_watchlist` read;
`add_option_to_watchlist` / `remove_option_from_watchlist` writes). Agentic
options are "rolling out"; expect these tools to appear later — and when option
**order** tools (`place_option_order`, `cancel_option_order`,
`review_option_order`) arrive, they go straight on the denylist.

For options/IV today, pair the request with `tradingview-reader` or
`funda-data`, which do expose option chains with IV and greeks.

---

## Write tools — NEVER call (denylist, live surface)

These mutate state or place/cancel real orders with real money. Out of scope for
this skill and this repository (no AI trade execution).

| Category | Tools |
|---|---|
| Equity trade execution | `place_equity_order`, `cancel_equity_order` |
| Order simulation (off-limits — write-intent, exists only to precede an order) | `review_equity_order` |
| Watchlist mutation | `add_to_watchlist`, `add_option_to_watchlist`, `remove_from_watchlist`, `remove_option_from_watchlist`, `create_watchlist`, `update_watchlist`, `follow_watchlist`, `unfollow_watchlist` |
| Future (when options/crypto/futures land) | any `place_*` / `cancel_*` / `review_*` for new asset classes — denylist on sight |

Note: `place_equity_order` / `cancel_equity_order` / `review_equity_order`
require an `agentic_allowed=true` account and operate on a specific
`account_number`. This skill never calls them regardless. If the user asks to
trade, rebalance, set up a recurring buy, or edit a watchlist, **decline** and
point them to the Robinhood app.

---

## Analyst workflows (read-only)

### Portfolio snapshot
1. `get_accounts` → choose the `account_number` (ask if multiple).
2. `get_portfolio` → total value, asset-class split, buying power.
3. `get_equity_positions` → holdings (symbol, qty, avg cost).
4. `get_equity_quotes` for the held symbols (batch ≤20) → live market value and
   unrealized P&L = (last − avg cost) × qty.
5. Present headline totals first, then a positions table; mask account numbers.

### Position concentration
1. `get_equity_positions` + live quotes for market value per holding.
2. Weight = market value / total equity value; flag concentration (e.g. any
   single name > 20%) as an observation, not advice.

### Order / transaction audit
1. `get_equity_orders` (filter by `state`, `symbol`, `created_at_gte`,
   `placed_agent`) for an account.
2. Summarize by symbol/side/date; separate open/pending from filled/cancelled.

### Equity volatility / charting (no options)
1. `get_equity_historicals` (`start_time` + interval) → OHLCV series.
2. From closes you can compute **realized/historical** volatility or draw a
   price/vol chart. This is *not* implied vol — an **IV skew needs the options
   chain**, which this connection does not expose (use `tradingview-reader` /
   `funda-data`).

---

## Related: Robinhood Banking / Agentic Credit Card MCP (out of scope)

Robinhood ships a **separate** MCP for its Agentic Credit Card at
`https://banking-agent.robinhood.com/mcp/banking`. It is scoped only to
authorized agentic virtual cards (card transaction history, card policies, card
number details) and exists to let an agent complete purchases — it is **not**
covered by this skill. This skill is the **trading** reader only. If a user
wants card data, that is a different connector with its own onboarding, and any
purchase capability is again out of scope for read-only use.
