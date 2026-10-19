---
name: yfinance-data
description: >
  Fetch financial and market data with the yfinance Python library (Yahoo Finance).
  Use this skill whenever the user wants stock data: current quotes and price history,
  financial statements (income statement, balance sheet, cash flow), options chains,
  dividends and splits, earnings and analyst estimates, price targets and ratings,
  institutional and insider holdings, news, multi-ticker comparisons, stock screens,
  or sector and industry data. Use it even when the user gives only a ticker symbol
  (AAPL, MSFT, TSLA) and the intent has to be inferred. For earnings previews or
  recaps, estimate revisions, valuation, correlation, liquidity, or ETF premium
  analysis, prefer the dedicated skill.
---

# yfinance Data Skill

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Fetches financial and market data from Yahoo Finance using the [yfinance](https://github.com/ranaroussi/yfinance) Python library.

**Important**: yfinance is not affiliated with Yahoo, Inc. Data is for research and educational purposes.

---

## Step 1: Ensure yfinance Is Available

**Current environment status:**

```
!`python3 -c "exec('try:\n import yfinance\n print(\'yfinance \' + yfinance.__version__ + \' installed\')\nexcept Exception:\n print(\'YFINANCE_NOT_INSTALLED\')')"`
```

If `YFINANCE_NOT_INSTALLED`, install it before running any code:

```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance"])
```

If yfinance is already installed, skip the install step and proceed directly.

---

## Step 2: Identify What the User Needs

Match the user's request to one or more data categories below, then use the corresponding code from `references/api_reference.md`.

| User Request | Data Category | Primary Method |
|---|---|---|
| Stock price, quote | Current price | `ticker.info` or `ticker.fast_info` |
| Price history, chart data | Historical OHLCV | `ticker.history()` or `yf.download()` |
| Balance sheet | Financial statements | `ticker.balance_sheet` |
| Income statement, revenue | Financial statements | `ticker.income_stmt` |
| Cash flow | Financial statements | `ticker.cashflow` |
| Dividends | Corporate actions | `ticker.dividends` |
| Stock splits | Corporate actions | `ticker.splits` |
| Options chain, calls, puts | Options data | `ticker.option_chain()` |
| Earnings, EPS | Analysis | `ticker.earnings_history` |
| Analyst price targets | Analysis | `ticker.analyst_price_targets` |
| Recommendations, ratings | Analysis | `ticker.recommendations` |
| Upgrades/downgrades | Analysis | `ticker.upgrades_downgrades` |
| Institutional holders | Ownership | `ticker.institutional_holders` |
| Insider transactions | Ownership | `ticker.insider_transactions` |
| Company overview, sector | General info | `ticker.info` |
| Compare multiple stocks | Bulk download | `yf.download()` |
| Screen/filter stocks | Screener | `yf.screen()` + `yf.EquityQuery` |
| Sector/industry data | Market data | `yf.Sector` / `yf.Industry` |
| News | News | `ticker.news` |

---

## Step 3: Write and Execute the Code

### General pattern

```python
import yfinance as yf

ticker = yf.Ticker("AAPL")
# ... use the appropriate method from the reference
```

### Key rules

1. **Always wrap in try/except** — Yahoo Finance may rate-limit or return empty data
2. **Use `yf.download()` for multi-ticker comparisons** — it's faster with multi-threading
3. **For options, list expiration dates first** with `ticker.options` before calling `ticker.option_chain(date)`
4. **For quarterly data**, use `quarterly_` prefix: `ticker.quarterly_income_stmt`, `ticker.quarterly_balance_sheet`, `ticker.quarterly_cashflow`
5. **For large date ranges**, be mindful of intraday limits — 1m data only goes back ~7 days, 1h data ~730 days
6. **Print DataFrames clearly** — use `.to_string()` or `.to_markdown()` for readability, or select key columns
7. **Timezone handling** — yfinance returns tz-aware datetime indices (e.g., `America/New_York`). When comparing dates, always use `pd.Timestamp(..., tz=...)` or strip timezones with `.tz_localize(None)`. See the reference file for details.

### Valid periods and intervals

| Periods | `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max` |
|---|---|
| **Intervals** | `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo` |

---

## Step 4: Present the Data

Answer with the numbers the user asked for first, then the supporting table (markdown, or a trimmed DataFrame with the key columns). Call out anything notable in the data — an earnings beat or miss, unusual volume, a dividend change — and add context such as sector averages, historical ranges, or analyst consensus where it changes how the numbers read. If the user wants a chart, pair the data with a visualization.

---

## Reference Files

- `references/api_reference.md` — Complete yfinance API reference with code examples for every data category

Read the reference file when you need exact method signatures or edge case handling.
