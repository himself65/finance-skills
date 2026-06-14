---
name: ibkr-reader
description: >
  Read-only reader for an Interactive Brokers (IBKR) account via IBKR's
  official Agentic MCP connector. Use to inspect an IBKR account or pull IBKR
  market data: account summary, cash balances and buying power, stock and
  option positions with cost basis, order and trade history, real-time quotes
  (stocks, ETFs, options, futures, crypto), bid/ask, volume, historical OHLCV
  bars, and implied volatility (underlying and per option contract), IV
  percentile, historical vol, and put/call open interest. Also resolves
  contracts and reads IBKR company themes, connections, and investment topics.
  Triggers: "my IBKR account", "Interactive Brokers positions", "IBKR
  balances", "IBKR buying power", "my IB orders", "IBKR trade history", "IBKR
  quote", "implied volatility via IBKR", "ibkr", "interactive brokers".
  READ-ONLY — never creates, modifies, or cancels orders and never sends
  feedback; calls only IBKR read tools and refuses every write/order tool, even
  when asked to trade.
---

# IBKR Reader (Read-Only)

Reads an [Interactive Brokers](https://www.interactivebrokers.com) account
through IBKR's official **Agentic MCP** connector. Once connected, the account
and market data are exposed as MCP tools the agent can call
(`mcp__claude_ai_Interactive_Brokers_IBKR__*` when connected as a claude.ai
connector; the prefix may differ if you add IBKR's MCP another way).

## ⚠️ Read-only contract — read this first

IBKR's Agentic MCP is **trade-capable**: the same connection that reads your
positions and quotes also exposes tools that **place and cancel real orders**
(`create_order_instruction` / `delete_order_instruction`). There is no
server-enforced read-only mode, so this skill's read-only guarantee is
**self-imposed**:

- It calls **only** read tools (accounts, positions, balances, orders, trades,
  price snapshot/history, contract search, themes/connections/topics).
- It **never** calls any order or state-changing tool — `create_order_instruction`,
  `delete_order_instruction`, `provide_customer_feedback`, or any future tool
  whose name/description implies placing, modifying, cancelling, or sending
  anything.
- If the user asks this skill to trade, decline and point them to the IBKR app
  — this repository forbids AI trade execution.

For a hard boundary independent of this skill, authenticate with a
**paper-trading account**, or one whose data you only want to read.

## What IBKR can and cannot do for options

IBKR **does** read option details — confirmed live:

- **Per-contract implied volatility** via `get_price_snapshot` (`implied_vol`,
  `option_midpoint_iv`), plus per-contract option volume and open interest.
- **Underlying volatility metrics**: `implied_vol_underlying` (annualized IV),
  `historical_vol`, `implied_volatility_percentile`, and aggregate put/call
  open interest and volume.

IBKR **cannot** (on this connector):

- **Enumerate an option chain.** `search_contracts` resolves the *underlying*
  and lists `OPT` as available, but returns **no strikes, expiries, or
  per-contract IDs** — and `get_price_snapshot` needs a `contract_id`. So you
  can read a *specific* option contract's IV only if you can obtain its ID
  (e.g. from the user's own option positions), **not an arbitrary chain**.
- **Return greeks.** There is no delta/gamma/theta/vega field — IV only. (Greeks
  live in IBKR's underlying Client Portal Web API, not this MCP connector.)

➡️ A full multi-strike **IV skew** cannot be assembled from IBKR alone. Use
`tradingview-reader` or `funda-data` for the per-strike chain; use IBKR for the
**underlying IV regime**, IV percentile, and put/call skew, and for **per-contract
IV of positions the user holds**.

---

## Step 1: Ensure the IBKR MCP Is Connected

**Current environment status:**

```
!`claude mcp list 2>/dev/null | grep -iE "interactive|ibkr" || echo "IBKR_MCP_CHECK_INCONCLUSIVE"`
```

This check is best-effort — IBKR is typically a **claude.ai connector**, which
`claude mcp list` may not show. The reliable signal is your own tool registry:

- If `mcp__claude_ai_Interactive_Brokers_IBKR__*` tools are present → connected.
  Continue to Step 2.
- If not → ask the user to connect it:
  1. Run `/mcp`, select **"claude.ai Interactive Brokers (IBKR)"**, and
     authenticate (IBKR OAuth, opens a browser).
  2. If the tools don't appear afterward, run `/reload-plugins` or restart the
     session.

Authenticating connects to the user's IBKR account. Market data follows their
**IBKR market-data subscriptions** (real-time vs delayed); without the options
data entitlement, option IV/quote fields may be sparse or omitted.

---

## Step 2: Read-Only Allowlist (live tools)

Confirmed against a live connection (June 2026). IBKR may add tools, so
**classify what your registry actually shows** by name/description; default
unknown or ambiguous tools to forbidden.

**Read (allowed):**

| Group | Tools |
|---|---|
| Account | `get_account_summary`, `get_account_balances`, `get_account_positions`, `get_account_orders`, `get_account_trades`, `get_order_instructions` |
| Market data | `get_price_snapshot`, `get_price_history`, `search_contracts` |
| Research | `get_company_themes`, `get_company_connections`, `get_theme_details`, `search_investment_topics` |

**Write — NEVER call (denylist):**

| Type | Tools |
|---|---|
| Order placement / cancellation | `create_order_instruction`, `delete_order_instruction` |
| Other side effects | `provide_customer_feedback` |

Note: `get_order_instructions` (read — lists pending agentic order instructions)
is allowed; `create_order_instruction` / `delete_order_instruction` (the trade
path) are not. Don't confuse them.

---

## Step 3: Identify What the User Needs

| User Request | Read tool(s) |
|---|---|
| Account overview / NLV / margin | `get_account_summary` |
| Cash balances, buying power | `get_account_balances` |
| Current holdings (stocks + options) w/ cost basis | `get_account_positions` |
| Open / past orders + status | `get_account_orders` |
| Executions / fill history | `get_account_trades` |
| Pending agentic order instructions | `get_order_instructions` |
| Live quote / bid-ask / volume for a symbol | `get_price_snapshot` |
| Implied vol, IV percentile, hist vol, put/call OI | `get_price_snapshot` (vol fields) |
| Per-contract option IV (need its contract_id) | `get_price_snapshot` on the option `contract_id` |
| Historical OHLCV bars | `get_price_history` |
| Resolve ticker / company name to a contract | `search_contracts` |
| Company themes / supply-chain connections | `get_company_themes`, `get_company_connections`, `get_theme_details` |
| Investment topics / ideas | `search_investment_topics` |
| Full multi-strike IV skew / option chain | **Not possible via IBKR** — say so; use `tradingview-reader` / `funda-data` |
| "Place / cancel / modify an order" | **Decline** — read-only skill; direct to the IBKR app |

---

## Step 4: Call the Read Tool

Resolve the instrument first, then read. Key rules:

1. **Reads only.** Before calling any tool, confirm it's on the read allowlist
   (or clearly read-only by name/description). Never call an order/instruction
   or feedback tool.
2. **Resolve the contract first.** `search_contracts(query, security_type?)`
   returns `underlying_contract_id` + `exchange` + `description` + available
   `sections`. Pick the right row (watch for ADRs/leveraged ETFs and non-US
   listings) before quoting.
3. **Snapshots need `contract_id` + `exchange` + `market_data_names`.** Use
   `exchange: "SMART"` (or the listing exchange from `search_contracts`).
   Request only the fields you need:
   - Quote: `last`, `bid_ask`, `change`, `prior_close`, `volume`, `high`, `low`, `open`
   - Underlying vol: `implied_vol_underlying`, `historical_vol`, `implied_volatility_percentile`, `underlying_today_option_volume`, `option_open_interest`
   - Per-contract option (option `contract_id`): `implied_vol`, `option_midpoint_iv`, `option_volume`, `option_open_interest`, `bid_ask`, `last`
   IV values are **fractions** (e.g. `0.99` = 99% annualized) — multiply by 100
   to present a percentage.
4. **Options without a chain.** You can only snapshot an option you can name a
   `contract_id` for. The dependable read-only source of option `contract_id`s
   is `get_account_positions` (the user's own option holdings). There is **no**
   chain-enumeration tool — don't promise a strike ladder from IBKR.
5. **History:** `get_price_history(contract_id, exchange, security_type, step, outside_rth, …)`
   — provide **either** `period` **or** `step_count`, never both.
6. **Account reads** (`get_account_*`) reflect the connected account; surface
   the account/currency when relevant.
7. **Entitlements:** snapshot fields unavailable within ~10s are omitted, and
   data is real-time or delayed per the user's subscription. If a vol field is
   missing, note it may be an entitlement gap, not an error.

See `references/tools.md` for the full field catalog and analyst workflows.

---

## Step 5: Respond to the User

1. **Lead with the headline, then the table.** Portfolio: net liquidation /
   buying power in prose first, then a positions table (symbol, qty, avg cost,
   last, market value, unrealized P&L).
2. **Protect sensitive data.** Mask account identifiers unless the user asks for
   the full value; don't paste them into external tools.
3. **Format cleanly.** Prices to 2 decimals, IV/vol as percentages with a sign
   on changes, large numbers with separators. Summarize trade history rather
   than dumping every fill.
4. **For volatility:** lead with annualized IV and where it sits (IV percentile),
   and frame put/call OI/volume as a skew observation — not a recommendation.
5. **Name the source and freshness:** "Interactive Brokers (via IBKR Agentic
   MCP)"; note real-time vs delayed if you can tell.
6. **No recommendations, no trades.** Present data; if asked to act, decline and
   point to the IBKR app.
7. **Cross-reference:** for a full IV skew / option chain, valuation, or news,
   pair with `tradingview-reader`, `funda-data`, or `yfinance-data`.

---

## Diagnostics & Error Reference

| Symptom | Cause | Fix |
|---|---|---|
| No `...IBKR__*` tools in registry | Connector not enabled | `/mcp` → "claude.ai Interactive Brokers (IBKR)" → authenticate; then `/reload-plugins` |
| Tools present but calls fail with auth error | Session/token expired | Re-authenticate via `/mcp` |
| Empty `bid_ask` / missing IV fields | Market closed, or no data entitlement | Note delayed/entitlement; retry in market hours; confirm subscription |
| `search_contracts` returns several rows | Multiple listings (ADR, 2x ETF, non-US) | Pick the row whose `exchange`/`description`/`country_code` matches the intent |
| User asks for a full option chain / IV skew | IBKR can't enumerate chains | Say so; use `tradingview-reader` / `funda-data` |
| User asks to place/cancel an order | Out of scope | Decline — read-only; direct to the IBKR app |

A successful `get_account_summary` (or a `get_price_snapshot` returning a
`last` price) confirms the connector, OAuth, and read path are working.

---

## Reference Files

- `references/tools.md` — Full read-tool catalog (params + output fields,
  complete `get_price_snapshot` field list), the write-tool denylist, the
  options capability/limitation detail, and analyst workflows.
