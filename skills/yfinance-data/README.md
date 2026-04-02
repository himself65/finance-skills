# yfinance-data

Fetch financial and market data using the [yfinance](https://github.com/ranaroussi/yfinance) Python library.

## What it does

Retrieves a wide range of financial data from Yahoo Finance, including:

- **Current prices & quotes** — real-time stock prices, market cap, P/E
- **Historical OHLCV** — price history with configurable period and interval
- **Financial statements** — balance sheet, income statement, cash flow (annual & quarterly)
- **Corporate actions** — dividends, stock splits
- **Options data** — full options chains with greeks
- **Analysis** — earnings history, analyst price targets, recommendations, upgrades/downgrades
- **Ownership** — institutional holders, insider transactions
- **Screener** — filter stocks using `yf.Screener` and `yf.EquityQuery`

> **Note**: yfinance is not affiliated with Yahoo, Inc. Data is for research and educational purposes.

## Triggers

- Any mention of a ticker symbol (AAPL, MSFT, TSLA, etc.)
- "what's the price of", "get me the financials", "show earnings"
- "options chain", "dividend history", "balance sheet", "income statement"
- "analyst targets", "compare stocks", "screen for stocks"

## Prerequisites

- Python 3.8+
- The skill auto-installs `yfinance` via pip if not already present

## Platform

Works on **all platforms** (Claude Code, Claude.ai with code execution, etc.).

## Setup

```bash
# As a plugin (recommended — installs all skills)
npx plugins add himself65/finance-skills

# Or install just this skill
npx skills add himself65/finance-skills --skill yfinance-data
```

See the [main README](../../README.md) for more installation options.

## Reference files

- `references/api_reference.md` — Complete yfinance API reference with code examples for every data category
