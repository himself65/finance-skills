---
name: ibkr-mcp
description: >
  Connect to Interactive Brokers via the ibkr_trade_mcp server to retrieve account info,
  positions, P&L, balances, and place or manage orders.
  Use this skill when the user asks about their IBKR account, brokerage positions,
  portfolio holdings, account balance, buying power, margin, P&L, trade history,
  or wants to place/cancel/modify orders through Interactive Brokers.
  Triggers include: "show my positions", "what's in my portfolio", "IBKR account",
  "Interactive Brokers", "my holdings", "account balance", "buying power",
  "place an order", "cancel order", "trade history", or any request involving
  a live brokerage account.
---

# IBKR MCP Skill

Interact with Interactive Brokers accounts through the [ibkr_trade_mcp](https://github.com/goCyberTrade/ibkr_trade_mcp) MCP server.

**Prerequisites**: The ibkr_trade_mcp server must be running and configured as an MCP server in the user's environment. See [Setup](#setup) below.

---

## Setup

### 1. Install and start the MCP server

```bash
# Install
pip install ebang-securities-mcp-server

# Start in SSE mode (recommended) — auto-downloads IB Gateway on first run
# Disable SSL to avoid certificate issues in local development
export IB_AUTO_RUN=True && uv run ebang-securities-mcp-server
```

### 2. Authenticate

Open the IB Gateway login page in a browser (note: port 5000 is reserved on macOS — the gateway may use a different port; check the server startup output). Log in with your IBKR credentials (or a demo account).

**Important**: Disable SSL verification in the IB Gateway settings for local development to avoid certificate errors.

### 3. Configure MCP client

Add to your MCP settings (e.g., Claude Code `settings.json`, Cursor, etc.):

```json
{
  "mcpServers": {
    "tradeMCP": {
      "type": "sse",
      "url": "http://127.0.0.1:8000/sse",
      "timeout": 60
    }
  }
}
```

---

## Step 1: Verify Connection

Before fetching data, confirm the MCP server is reachable by listing available channels:

**Tool**: `list_channel`
- Returns the list of supported channels (e.g., `"ibkr"` for Interactive Brokers)

If this fails, the server is not running — ask the user to start it.

---

## Step 2: Get Account Info

Start by retrieving the user's accounts to get the `accountId` needed for all subsequent calls.

**Tool**: `accounts`
- **Parameters**: `channel` = `"ibkr"`
- **Returns**: List of tradable accounts, aliases, permissions, and session info

Then use the `accountId` from the response in all further requests.

---

## Step 3: Match User Request to Tools

Refer to `references/tools_reference.md` for complete tool details. Here's the quick lookup:

### Account & Portfolio

| User Request | Tool | Key Parameters |
|---|---|---|
| Account overview | `general_account_summary` | `accountId` |
| P&L | `account_profit_and_loss` | — |
| Balances | `balances` | `accountId` |
| Buying power, funds | `available_funds` | `accountId` |
| Margins | `margins` | `accountId` |
| Market value by asset class | `market_value` | `accountId` |
| Portfolio allocation | `get_portfolio_allocation` | `accountId` |
| Account ledger | `get_account_ledger` | `accountId` |
| Performance | `get_account_performance` | `accountIdList` |
| Performance over period | `get_period_account_performance` | `accountIdList`, `period` |

### Positions

| User Request | Tool | Key Parameters |
|---|---|---|
| All positions | `get_all_position` | `accountId`, `pageId` (paginated, 100/page) |
| Single instrument position | `get_instrument_position` | `accountId`, `conid` |
| Position info | `get_position_info` | `conid` |

### Trading

| User Request | Tool | Key Parameters |
|---|---|---|
| Search for a contract | `get_contract_list` | `symbol` |
| Place an order | `create_order` | `conid`, `accountId`, + order params |
| Modify an order | `edit_order` | `orderId`, `accountId`, + fields |
| Cancel an order | `cancel_order` | `accountId`, `orderId` |
| Check order impact | `order_whatif` | `conid`, `accountId`, + order params |
| Confirm order reply | `order_reply` | `id` |
| View an order | `get_order_info` | `orderId` |
| List today's orders | `get_order_list` | `accountId` (optional) |

### History

| User Request | Tool | Key Parameters |
|---|---|---|
| Transaction history | `get_history_transactions` | `accountIdList`, `conidList`, `days` |

---

## Step 4: Present the Data

1. **Positions** — Show as a table: symbol, quantity, market value, avg cost, unrealized P&L, % change
2. **Account summary** — Highlight net liquidation, buying power, margin used, total P&L
3. **Orders** — Show status, side, quantity, price, fill status
4. **Flag important items** — Positions with large unrealized losses, margin warnings, pending orders

---

## Important Notes

- **Order placement is irreversible** — Always use `order_whatif` first to preview impact, and confirm with the user before calling `create_order`
- **Pagination** — `get_all_position` returns max 100 per page. Increment `pageId` to get more.
- **Channel parameter** — Always pass `channel: "ibkr"` (the only currently supported channel)
- **Demo accounts** — For testing, register an IBKR paper trading account at [interactivebrokers.com](https://www.interactivebrokers.com)

---

## Reference Files

- `references/tools_reference.md` — Complete reference for all MCP tools with parameters and return values

Read the reference when you need exact parameter names or response field details.
