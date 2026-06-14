# IBKR Agentic MCP — Read-Tool Reference

Detailed reference for the **read-only** subset of Interactive Brokers' official
Agentic MCP connector, exposed in Claude Code as
`mcp__claude_ai_Interactive_Brokers_IBKR__<tool>` after the user connects and
authenticates (the prefix may differ if IBKR's MCP is added another way).

> **Source & accuracy.** Tool names and the `get_price_snapshot` field list
> below were **confirmed against a live, authenticated connection (June 2026)**.
> IBKR adds tools over time — always classify what your own registry shows and
> treat this as a seed, not a guarantee.

---

## The read-only rule (non-negotiable)

Call a tool **only** if it merely retrieves data. A tool is forbidden if its
name/description implies it **changes anything** — creating, placing, modifying,
cancelling, deleting, or sending. **Default unknown/ambiguous tools to
forbidden.** There is no server-enforced read-only mode; this allowlisting is
the only thing keeping the skill safe. IBKR's trade path is
`create_order_instruction` / `delete_order_instruction` — never call them.

---

## Read tools (allowed)

### Account

| Tool | Purpose | Notes |
|---|---|---|
| `get_account_summary` | Account overview (net liquidation, margin, equity) | Start here for "how's my account" |
| `get_account_balances` | Cash balances + buying power | Per currency |
| `get_account_positions` | Open positions (stocks **and** options) with quantity + average cost | The dependable read-only source of option `contract_id`s for held contracts |
| `get_account_orders` | Order status/history (open + closed) | |
| `get_account_trades` | Executions / fills | |
| `get_order_instructions` | Pending **agentic** order instructions (read) | Read-only; do **not** confuse with `create_/delete_order_instruction` (writes) |

### Market data

| Tool | Purpose | Key params |
|---|---|---|
| `search_contracts` | Resolve ticker/name/keyword → `underlying_contract_id`, `exchange`, `description`, available `sections` | `query` (required); `security_type` (STK/OPT/FUT/FOP/CASH/WAR/BOND/CFD/FUND/IND/CRYPTO/CMDTY/IOPT); `language` |
| `get_price_snapshot` | Real-time snapshot — quotes, volume, **implied vol**, OI, etc. | `contract_id`, `exchange` (e.g. `SMART`), `market_data_names` (list) — all required |
| `get_price_history` | Historical OHLCV bars | `contract_id`, `exchange`, `security_type`, `step`, `outside_rth` required; provide **either** `period` **or** `step_count`, never both; optional `include_corporate_actions` |

### Research

| Tool | Purpose |
|---|---|
| `get_company_themes` | Themes a company belongs to (needs a `contract_id` from `search_contracts`) |
| `get_company_connections` | Company relationships / supply-chain-style connections |
| `get_theme_details` | Detail on a specific theme |
| `search_investment_topics` | Search IBKR investment topics / ideas |

---

## `get_price_snapshot` field catalog (`market_data_names`)

Request only what you need. IV/vol values are **fractions** (multiply by 100 for
a percentage). Fields unavailable within ~10s are omitted; `bid_ask` may be an
empty object when no quote is available.

**Quote / price**

- `last` — last trade price (+ `is_close`/halt flags; price may be null if equal to prior)
- `bid_ask` — current bid and ask
- `change` — absolute + % change vs prior close
- `prior_close` — prior session close
- `plprice` — mark / profit-loss price
- `open`, `high`, `low` — today's open / intraday high / low
- `volume` — today's total volume
- `misc_statistics` — 13/26/52-week high-low + price 52w ago
- `avg_90d_usd_volume` — avg USD volume over 90 days

**Options & volatility**

- `implied_vol` — implied vol for an **option contract** (fraction)
- `option_midpoint_iv` — midpoint IV for an **option contract**
- `implied_vol_underlying` — underlying IV; `daily_iv` + `annual_iv` (present `annual_iv`)
- `historical_vol` — 30-day historical vol (`daily_pct` + `annual_pct`)
- `implied_volatility_percentile` — IV high percentile over 13w/26w/52w (fractions)
- `option_volume` — option contract volume today (OPT)
- `option_open_interest` — call/put open interest (observed: returns aggregate call/put OI when queried on the underlying; per-contract OI on an option `contract_id`)
- `underlying_today_option_volume` — total today call/put volume for the underlying
- `underlying_avg_option_volume` — average call/put volume for the underlying

**Other**

- `dividend_yield` (STK/CFD), `future_open_interest` (FUT), `bond_yield` (BOND),
  `year_to_date_change`, `total_net_assets`,
  `cumulative_perf_1d/1w/1m/ytd/1y/3y/5y`, `perpetual_futures_funding_rate`

> **No greeks.** There is no delta/gamma/theta/vega field — implied volatility
> is the only vol surface this MCP exposes. (Greeks exist in IBKR's underlying
> Client Portal Web API — fields 7308/7309/7310/7311 — but are not surfaced by
> this connector.)

---

## Options: capability vs limitation

**Can do (read-only):**
- Underlying IV regime: `implied_vol_underlying` (annualized), `historical_vol`,
  `implied_volatility_percentile`, aggregate call/put OI + volume.
- Per-contract option IV: `get_price_snapshot` on a specific option
  `contract_id` → `implied_vol` / `option_midpoint_iv`, plus its OI/volume/quote.
- Historical option bars: `get_price_history` with `security_type: OPT` (or
  `FOP`) given an option `contract_id`.

**Cannot do:**
- **Enumerate an option chain.** `search_contracts` returns the underlying and
  flags `OPT` as available, but yields no strikes/expiries/per-contract IDs, and
  there is no `secdef/strikes`-style tool. Without contract IDs you cannot
  snapshot each strike.
- **Greeks** of any kind.

**Consequence:** a full multi-strike **IV skew** is not assemblable from IBKR
alone. Get option `contract_id`s only from `get_account_positions` (held
contracts). For an arbitrary chain / skew, use `tradingview-reader` or
`funda-data`.

---

## Write tools — NEVER call (denylist)

| Category | Tools |
|---|---|
| Order placement / cancellation (the trade path) | `create_order_instruction`, `delete_order_instruction` |
| Other side effects | `provide_customer_feedback` |
| Future | any tool whose name/description implies creating, placing, modifying, cancelling, deleting, or sending — denylist on sight |

If the user asks to trade, rebalance, or place/cancel an order, **decline** and
point them to the IBKR app.

---

## Analyst workflows (read-only)

### Portfolio snapshot
1. `get_account_summary` → net liquidation, margin.
2. `get_account_balances` → cash + buying power.
3. `get_account_positions` → holdings (symbol, qty, avg cost; includes option contracts + their IDs).
4. `get_price_snapshot` per held symbol (`last`, `bid_ask`) → market value and unrealized P&L.
5. Present headline totals first, then a positions table; mask account IDs.

### Underlying volatility read
1. `search_contracts(query)` → underlying `contract_id` + `exchange`.
2. `get_price_snapshot(contract_id, exchange, ["implied_vol_underlying","historical_vol","implied_volatility_percentile","underlying_today_option_volume","option_open_interest","last"])`.
3. Report annualized IV, where it sits (IV percentile), IV-vs-HV gap, and the
   put/call OI/volume skew — as observations, not advice.

### IV of the user's option holdings
1. `get_account_positions` → option positions and their `contract_id`s.
2. `get_price_snapshot(option_contract_id, "SMART", ["implied_vol","option_midpoint_iv","bid_ask","last","option_open_interest"])` per contract.
3. Tabulate IV per held contract. (This is holdings, **not** a chain/skew.)

### Price history / realized vol
1. `search_contracts` → `contract_id` + `exchange`.
2. `get_price_history(contract_id, exchange, security_type, step, outside_rth, period|step_count)`.
3. From closes, compute realized vol or draw a price chart. (Implied skew still
   requires an options source — see above.)

---

## Entitlement caveats

`get_price_snapshot` returns real-time **or** delayed prices automatically based
on the user's IBKR market-data subscriptions (frozen / delayed-frozen are not
supported). Without the relevant options/market-data entitlement, IV and quote
fields can come back sparse or omitted — surface this as a possible entitlement
gap rather than a failure.
