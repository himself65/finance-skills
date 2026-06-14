---
name: robinhood-reader
description: >
  Read-only reader for a user's Robinhood brokerage account via Robinhood's
  official Agentic Trading MCP server (agent.robinhood.com/mcp/trading). Use
  whenever the user wants to inspect their Robinhood holdings — portfolio
  value and real-time buying power, equity positions with cost basis, accounts
  and balances, equity order history, watchlists, real-time equity quotes, or
  historical price data from their connected Robinhood account. Options,
  options chains, IV, and index quotes are not exposed on this connection.
  Triggers: "my
  Robinhood portfolio", "Robinhood positions", "what do I hold on Robinhood",
  "Robinhood account balance", "my buying power", "Robinhood order history",
  "my Robinhood watchlist", "check my Robinhood", "robinhood", "robinhood
  agent", "agentic trading". READ-ONLY — never places, previews, modifies, or
  cancels orders and never changes watchlists; it calls only Robinhood MCP read
  tools and refuses every write/order tool, even when asked to trade.
---

# Robinhood Reader (Read-Only)

Reads a user's [Robinhood](https://robinhood.com) account through Robinhood's
official **Agentic Trading MCP server** (`https://agent.robinhood.com/mcp/trading`),
the same integration described at
[robinhood.com/us/en/agentic-trading](https://robinhood.com/us/en/agentic-trading/).
Once the user connects it, the account data is exposed as MCP tools the agent
can call (`mcp__robinhood-trading__*`).

## ⚠️ Read-only contract — read this first

Robinhood's Agentic Trading MCP is a **trade-capable** server. The same
connection that exposes your positions and balances also exposes tools that
**place and cancel real orders with real money**. There is **no
server-enforced read-only mode** — Robinhood does not gate writes for you, and
"ask for approval before acting" is an agent-side behavior, not a permission
the server enforces.

This skill's read-only guarantee is therefore **self-imposed**:

- It calls **only** read tools (accounts, portfolio, positions, balances,
  orders/transactions, quotes, chains, watchlist reads, historicals).
- It **never** calls any order, trade, or state-mutating tool — `place_*`,
  `cancel_*`, `review_*`/preview, `add_*`, `remove_*`, `create_*`, `follow_*`,
  `unfollow_*`, `update_*`, or any future tool whose name or description implies
  placing, cancelling, modifying, previewing, or changing anything.
- If the user asks this skill to buy, sell, cancel, or modify, **decline** and
  point them to the Robinhood app — this repository forbids AI trade execution.

For a hard safety boundary independent of this skill, advise the user to keep
the dedicated **Agentic account unfunded (or at the minimum allowed balance)**
— writes are scoped to that account, so with no buying power an order can't
execute even if something tried. Reads still work across all accounts.

---

## Step 1: Ensure the Robinhood Trading MCP Is Connected

**Current environment status:**

```
!`claude mcp list 2>/dev/null | grep -iE "^robinhood-trading" || echo "ROBINHOOD_MCP_NOT_CONNECTED"`
```

- A line starting with `robinhood-trading` → registered. Its tools are callable
  as `mcp__robinhood-trading__<tool>`. Continue to Step 2.
- `ROBINHOOD_MCP_NOT_CONNECTED` → walk the user through connecting it:

  ```bash
  claude mcp add robinhood-trading --transport http https://agent.robinhood.com/mcp/trading
  ```

  Then inside Claude Code run `/mcp`, select `robinhood-trading`, and
  authenticate. A browser opens for Robinhood's OAuth + onboarding flow. You
  may need to restart the Claude Code session before the tools register.

**What authenticating does (set expectations before they click):**

- Authentication runs Robinhood's OAuth and **prompts the user to open a
  dedicated "Agentic account"** as an additional account. This must be done on
  a **desktop device** (on mobile, copy the onboarding URL to a desktop
  browser).
- Prerequisite: an existing **primary individual investing account in good
  standing**. Robinhood allows up to 10 self-directed individual accounts total,
  including the Agentic account.
- Connecting grants the agent **read access to *all* the user's Robinhood
  accounts** — including account numbers, positions, balances, and full order
  and transaction history — plus **write access scoped to the Agentic
  account**. This skill uses only the read half.
- The product is in **beta** (US; equities live, options rolling out, with
  crypto/futures/event contracts noted as coming later). Exact availability and
  the onboarding handshake may vary — let the user follow Robinhood's prompts.

**To disconnect / revoke** when done: one tap in the Robinhood app, or
`claude mcp remove robinhood-trading` in Claude Code.

---

## Step 2: Enumerate the Live Tools and Apply the Read-Only Allowlist

**Do not assume the tool list — verify it at runtime.** After the user
connects, inspect the tools the server actually exposes (they appear in your
tool registry as `mcp__robinhood-trading__*`; `/mcp` also lists them). Robinhood
states it will keep adding tools, so classify every tool by **name and
description**, not from a fixed list:

- **Allowed (read):** anything that only retrieves/views — names beginning
  `get_*`, `search`, and similar. See the catalog in `references/tools.md`.
- **Forbidden (write / state-changing):** anything that places, submits, buys,
  sells, cancels, replaces, modifies, previews/reviews, adds, follows,
  unfollows, updates, creates, or deletes. **Default unknown or ambiguous tools
  to forbidden.**

### Observed live tools (equities beta, June 2026)

The lists below were confirmed against a real connected account. Robinhood is
still adding tools, and a different account/tier may expose a different set —
so **classify what your registry actually shows**; treat these as a seed, not a
guarantee.

**Read (allowed):**

| Group | Tools |
|---|---|
| Account / portfolio | `get_accounts`, `get_portfolio`, `get_equity_positions`, `get_equity_orders`, `get_equity_tradability` |
| Quotes / market data | `get_equity_quotes`, `get_equity_historicals`, `search` |
| Watchlists (read) | `get_watchlists`, `get_watchlist_items`, `get_popular_watchlists`, `get_option_watchlist` |

**Write — NEVER call (denylist):**

| Type | Tools |
|---|---|
| Trade execution | `place_equity_order`, `cancel_equity_order` |
| Order simulation (off-limits — write-intent, precedes an order) | `review_equity_order` |
| Watchlist mutation | `add_to_watchlist`, `add_option_to_watchlist`, `remove_from_watchlist`, `remove_option_from_watchlist`, `create_watchlist`, `update_watchlist`, `follow_watchlist`, `unfollow_watchlist` |

**Not yet exposed on this connection (but in Robinhood's docs — expect them as
the beta expands):** option market data (`get_option_chains`,
`get_option_quotes`, option positions/orders) and index quotes
(`get_indexes`, `get_indexes_quotes`). When any **option order** tool appears
(`place_option_order`, `cancel_option_order`, `review_option_order`), it goes
straight on the denylist. This is why the rule above is name/description-driven,
not a fixed list.

> **Naming note from the live wire:** Robinhood's docs render
> `get_equity-historicals` with a hyphen, but the actual tool is
> `get_equity_historicals` (underscore), and the docs' `get_popular_lists` is
> really `get_popular_watchlists`. Always trust the live registry over the docs.

---

## Step 3: Identify What the User Needs

| User Request | Read tool(s) |
|---|---|
| "My Robinhood accounts" / account list + numbers | `get_accounts` |
| Portfolio value, asset-class breakdown, buying power | `get_portfolio` (needs `account_number`) |
| Current stock holdings (qty, avg cost) | `get_equity_positions` (needs `account_number`) |
| Equity order history / status | `get_equity_orders` (needs `account_number`) |
| Live quote(s) for symbols | `get_equity_quotes` (batch ≤20 to keep prior closes) |
| Historical OHLCV series for a symbol | `get_equity_historicals` (needs `start_time`) |
| Is a symbol tradable / fractionable | `get_equity_tradability` (needs `account_number`) |
| Ticker / instrument lookup by name | `search` |
| Watchlists and their contents | `get_watchlists`, `get_watchlist_items`, `get_popular_watchlists` |
| Saved single-leg option contracts | `get_option_watchlist` (contract refs only — no quotes or IV) |
| Option chains / quotes / IV, option positions or orders, index quotes | **Not exposed in this beta** — say so plainly; for options/IV pair with `funda-data` or `tradingview-reader` |
| "Buy / sell / cancel / modify / edit a watchlist" | **Decline** — read-only skill; direct to the Robinhood app |

For multi-part requests (e.g. "how's my Robinhood doing"), call `get_accounts`
first for the `account_number`, then chain `get_portfolio` (totals + buying
power) + `get_equity_positions` for a full snapshot. **Options are not
queryable** on this connection — there is no chain, quote, or IV tool, so an IV
skew or options book must come from `tradingview-reader` / `funda-data`.

---

## Step 4: Call the Read Tool

Call the MCP tool directly, e.g. `mcp__robinhood-trading__get_portfolio`. Key
rules:

1. **Reads only.** Before calling any tool, confirm it is on the read
   allowlist (or is clearly read-only by name/description). Never call a write
   tool — not even to "preview" or "review" an order, and not to add a contract
   to a watchlist.
2. **Batch quotes, mind the 20 cap.** `get_equity_quotes` takes many symbols,
   but above 20 it omits the prior-session closes (`closes_error` is set) —
   keep batches ≤20 when you need closes.
3. **Resolve names with `search`.** Turn a company name into a ticker /
   `instrument_id` before quoting or pulling positions.
4. **Most reads are per-account.** Only `get_accounts` enumerates accounts.
   `get_portfolio`, `get_equity_positions`, `get_equity_orders`, and
   `get_equity_tradability` each require an `account_number` — call
   `get_accounts` first, and if the user has more than one account and didn't
   say which, present the list and ask before querying (don't silently dump all
   accounts). For buying power use `get_portfolio` (`get_accounts` does not
   return reliable buying power).
5. **Don't refetch needlessly.** Quotes/positions are fresh per call; reuse a
   result within the same turn instead of re-calling.

See `references/tools.md` for the full tool catalog, parameters, and analyst
workflows (portfolio review, position concentration, order-history audit,
options book review).

---

## Step 5: Respond to the User

1. **Lead with the headline, then the table.** For a portfolio request: state
   total value, day change, and buying power in prose first, then a positions
   table (symbol, qty, avg cost, last, market value, unrealized P&L).
2. **Protect sensitive data.** Account numbers come back in reads — **mask
   them** (e.g. `••••1234`) unless the user explicitly asks for the full
   number. Don't paste full account numbers into summaries or external tools.
3. **Format cleanly.** Prices to 2 decimals, percentages with sign, large
   numbers with separators (`$1,240,500`). Summarize order history rather than
   dumping every fill.
4. **Note the source and freshness:** "Robinhood (via Agentic Trading MCP)."
   Quotes are real-time; positions reflect the moment of the call.
5. **No recommendations, no trades.** Present the data and let the user draw
   conclusions. If they ask you to act on it (buy/sell/rebalance), decline and
   point them to the Robinhood app — this skill is read-only by design.
6. **Cross-reference for analysis.** For valuation, options greeks, or news
   context on what they hold, pair this with `funda-data`,
   `tradingview-reader`, or `yfinance-data`.

---

## Diagnostics & Error Reference

| Symptom | Cause | Fix |
|---|---|---|
| `ROBINHOOD_MCP_NOT_CONNECTED` | MCP not added | `claude mcp add robinhood-trading --transport http https://agent.robinhood.com/mcp/trading` |
| Tools listed but calls fail with auth error | Not authenticated / token expired | Run `/mcp`, select `robinhood-trading`, re-authenticate |
| Tools don't appear after `mcp add` | Session not reloaded | Restart Claude Code, then `/mcp` |
| Onboarding can't complete on phone | Account opening is desktop-only | Open the onboarding URL in a desktop browser |
| Empty positions/orders | Reading the Agentic (or a new) account with no activity | Confirm which account via `get_accounts`; data spans all accounts |
| User asks to place/cancel a trade | Out of scope | Decline; this skill is read-only — direct them to the Robinhood app |

A successful `get_accounts` confirms the MCP, OAuth, and read path are all
working.

---

## Reference Files

- `references/tools.md` — Full read-tool catalog (parameters + output fields),
  the write-tool denylist, the runtime allowlisting rule, analyst workflows,
  and a note on the separate Robinhood banking/credit-card MCP.
