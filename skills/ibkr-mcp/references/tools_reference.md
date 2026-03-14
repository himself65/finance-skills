# IBKR Trade MCP — Tools Reference

All tools accept `channel` (default `"ibkr"`) as their first parameter.

---

## Channel Tools

### `list_channel`
List supported trading channels.
- **Parameters**: none
- **Returns**: List of channel identifiers (e.g., `["ibkr"]`)

---

## Account Tools

### `accounts`
Retrieve all tradable accounts and session info.
- **Parameters**: `channel`
- **Returns**: Account list, aliases, permissions, chart periods, session data

### `switch_account`
Switch the active account (for financial advisors / multi-account structures).
- **Parameters**: `channel`, `accountId`
- **Returns**: Confirmation with new active account ID

### `signatures_and_owners`
List all applicant names and entity info on the account.
- **Parameters**: `channel`, `accountId`
- **Returns**: User roles, entity types, names, applicant signatures

### `general_account_summary`
Overview of account details and balance values.
- **Parameters**: `channel`, `accountId`
- **Returns**: Account type, status, buying power, margins, multi-currency cash balances

### `account_profit_and_loss`
Detailed P&L information.
- **Parameters**: `channel`
- **Returns**: Unrealized/realized P&L, net liquidation, market values by account

### `available_funds`
Summary of available funds with detail.
- **Parameters**: `channel`, `accountId`
- **Returns**: Current/overnight availability, excess liquidity, buying power by segment

### `balances`
Account balance overview.
- **Parameters**: `channel`, `accountId`
- **Returns**: Net liquidation, equity, security valuations, cash positions by category

### `margins`
Account margins overview.
- **Parameters**: `channel`, `accountId`
- **Returns**: Regulatory, initial, and maintenance margin values by asset class

### `market_value`
Market value breakdown by asset class and currency.
- **Parameters**: `channel`, `accountId`
- **Returns**: Multi-currency valuations (stocks, options, futures, bonds, crypto), realized/unrealized P&L, exchange rates

---

## Position Tools

### `get_all_position`
Get all positions (paginated).
- **Parameters**: `channel`, `accountId`, `pageId` (int, default 0, max 100 per page)
- **Returns**: Position list with contract details, pricing, P&L metrics, market data

### `get_instrument_position`
Get position for a single instrument.
- **Parameters**: `channel`, `accountId`, `conid` (int, contract ID)
- **Returns**: Position data with security definition and valuation metrics

### `get_position_info`
Get position details by contract ID.
- **Parameters**: `channel`, `conid` (int)
- **Returns**: Symbol, quantity, market value, average cost

### `get_portfolio_allocation`
Portfolio breakdown by asset class and sector.
- **Parameters**: `channel`, `accountId`
- **Returns**: Long/short positions by asset class, sector, and sector group

### `get_account_ledger`
Multi-currency balance details.
- **Parameters**: `channel`, `accountId`
- **Returns**: Cash, market values by instrument type, realized/unrealized P&L, exchange rates

### `get_account_attributes`
Account metadata.
- **Parameters**: `channel`, `accountId`
- **Returns**: Alias, status, entity type, regulatory classification, trading permissions

### `get_account_summary`
Condensed account overview.
- **Parameters**: `channel`, `accountId`
- **Returns**: Readiness status, account type, accrued cash

### `get_account_performance`
Consolidated MTM performance.
- **Parameters**: `channel`, `accountIdList` (List[str])
- **Returns**: NAV, cumulative performance, frequency-based datasets, historical period ranges

### `get_period_account_performance`
Performance over a specific time period.
- **Parameters**: `channel`, `accountIdList` (List[str]), `period` (str, default `"12M"`)
- **Valid periods**: `1D`, `7D`, `MTD`, `1M`, `3M`, `6M`, `12M`, `YTD`
- **Returns**: NAV, cumulative/time-period returns with standardized frequency and date arrays

### `get_history_transactions`
Historical transaction ledger.
- **Parameters**: `channel`, `accountIdList` (List[str]), `conidList` (List[str]), `currency` (str, default `"USD"`), `days` (int, default 90)
- **Returns**: Timestamps, quantities, prices, FX rates, trade amounts

---

## Lookup Tools (read-only)

### `get_contract_list`
Search for contracts by symbol.
- **Parameters**: `channel`, `symbol` (str)
- **Returns**: Contract info: conId, symbol, description, secType for all matching contracts

### `get_order_info`
Get details for a specific order.
- **Parameters**: `channel`, `orderId` (str)
- **Returns**: Order status, type, price, fills, execution time

### `get_order_list`
List all orders for the current trading day.
- **Parameters**: `channel`, `accountId` (str, optional)
- **Returns**: All orders with comprehensive attributes

### `get_portfolio_accounts`
List all accounts with details.
- **Parameters**: `channel`
- **Returns**: Account IDs, currency, type, business classification

### `get_sub_accounts`
List subaccounts.
- **Parameters**: `channel`
- **Returns**: Subaccount info with attributes and parent relationship

---

## PROHIBITED Tools — Do NOT Use

The following tools execute real trades with real money. They must **NEVER** be called by this skill.

- `create_order` — Places a live order
- `edit_order` — Modifies a live order
- `cancel_order` — Cancels a live order
- `order_reply` — Confirms order execution
- `order_whatif` — Simulates an order
