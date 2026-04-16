# yfinance API Reference

Complete reference for all yfinance data access methods.

## Installation

```python
pip install yfinance
```

Requires Python 3.8+. Dependencies (pandas, requests, etc.) are installed automatically.

---

## Ticker Object

The primary interface for single-stock data.

```python
import yfinance as yf
ticker = yf.Ticker("AAPL")
```

---

## Historical Price Data

### `ticker.history()`

Returns a DataFrame with columns: Open, High, Low, Close, Volume, Dividends, Stock Splits.

```python
# Default: 1 month of daily data
hist = ticker.history(period="1mo")

# Specific date range
hist = ticker.history(start="2023-01-01", end="2023-12-31")

# Weekly data for 1 year
hist = ticker.history(period="1y", interval="1wk")

# Intraday 5-minute bars for last 5 days
hist = ticker.history(period="5d", interval="5m")

# Include pre/post market data
hist = ticker.history(period="5d", prepost=True)

# Repair price anomalies
hist = ticker.history(period="1mo", repair=True)
```

**Valid periods**: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`
**Valid intervals**: `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`

**Intraday limits**:
- 1m: last ~7 days
- 2m/5m/15m/30m: last ~60 days
- 60m/90m/1h: last ~730 days

### `yf.download()` — Bulk Download

Efficient multi-threaded download for multiple tickers.

```python
data = yf.download(
    tickers="AAPL MSFT GOOGL AMZN",  # space or comma separated
    start="2023-01-01",
    end="2024-01-01",
    interval="1d",
    group_by="ticker",    # or "column" (default)
    auto_adjust=True,     # adjust for splits and dividends
    threads=True,         # multi-threading
    progress=True         # show progress bar
)

# Access a specific ticker
apple_close = data["AAPL"]["Close"]

# Download with dividends and splits
data = yf.download(["AAPL", "MSFT"], period="1y", actions=True)

# Additional options
data = yf.download(
    tickers=["TSLA", "NVDA"],
    period="6mo",
    interval="1h",
    repair=True,       # fix price anomalies
    keepna=False,      # remove NaN rows
    rounding=True,     # round to 2 decimals
    timeout=10         # request timeout seconds
)
```

---

## Company Info

### `ticker.info`

Returns a dictionary with company details, financials, and market data.

```python
info = ticker.info

# Common fields
info['shortName']          # Company name
info['sector']             # e.g., "Technology"
info['industry']           # e.g., "Consumer Electronics"
info['marketCap']          # Market capitalization
info['currentPrice']       # Current stock price
info['previousClose']      # Previous close price
info['trailingPE']         # Trailing P/E ratio
info['forwardPE']          # Forward P/E ratio
info['dividendYield']      # Dividend yield
info['beta']               # Beta
info['fiftyTwoWeekHigh']   # 52-week high
info['fiftyTwoWeekLow']    # 52-week low
info['averageVolume']      # Average volume
info['longBusinessSummary'] # Company description
```

### `ticker.fast_info`

Lightweight subset for quick price lookups (faster than `.info`).

```python
fi = ticker.fast_info
fi['lastPrice']
fi['marketCap']
fi['fiftyDayAverage']
fi['twoHundredDayAverage']
```

---

## Financial Statements

All return pandas DataFrames. Use `quarterly_` prefix for quarterly data.

```python
# Annual
ticker.income_stmt          # Income statement
ticker.balance_sheet        # Balance sheet
ticker.cashflow             # Cash flow statement

# Quarterly
ticker.quarterly_income_stmt
ticker.quarterly_balance_sheet
ticker.quarterly_cashflow
```

---

## Corporate Actions

```python
ticker.dividends            # Series of dividend payments
ticker.splits               # Series of stock splits
ticker.actions              # DataFrame with both dividends and splits
ticker.capital_gains        # Capital gains (for mutual funds/ETFs)
```

---

## Options

```python
# List available expiration dates
expirations = ticker.options   # tuple of date strings

# Get option chain for a specific expiration
opt = ticker.option_chain("2024-06-21")

# Calls and puts are separate DataFrames
calls = opt.calls
puts = opt.puts

# Key columns:
# strike, lastPrice, bid, ask, volume, openInterest, impliedVolatility,
# inTheMoney, contractSymbol, lastTradeDate, change, percentChange
```

---

## Analysis & Estimates

```python
# Analyst price targets
ticker.analyst_price_targets
# Returns dict: current, low, high, mean, median

# Recommendations (buy/hold/sell counts by period)
ticker.recommendations

# Upgrades and downgrades history
ticker.upgrades_downgrades
# Columns: firm, toGrade, fromGrade, action

# Earnings estimates
ticker.earnings_estimate
# Columns: numberOfAnalysts, avg, low, high, yearAgoEps, growth
# Index: 0q (current quarter), +1q, 0y, +1y

# Revenue estimates
ticker.revenue_estimate

# EPS trend
ticker.eps_trend

# EPS revisions
ticker.eps_revisions

# Growth estimates
ticker.growth_estimates

# Earnings history (actual vs estimate)
ticker.earnings_history
# Columns: epsEstimate, epsActual, epsDifference, surprisePercent

# Sustainability / ESG scores
ticker.sustainability
```

---

## Ownership

```python
# Major holders summary
ticker.major_holders

# Top institutional holders
ticker.institutional_holders
# Columns: Holder, Shares, Date Reported, % Out, Value

# Mutual fund holders
ticker.mutualfund_holders

# Insider transactions
ticker.insider_transactions

# Insider roster
ticker.insider_roster_holders

# Shares outstanding over time
ticker.get_shares_full(start="2023-01-01", end="2023-12-31")
```

---

## Calendar & Events

```python
ticker.calendar
# Returns dict with upcoming earnings dates, dividends, etc.
```

---

## News

```python
ticker.news
# Returns list of dicts with: title, link, publisher, providerPublishTime, type
```

---

## Multiple Tickers

```python
tickers = yf.Tickers("AAPL MSFT GOOGL")

# Access individual tickers
tickers.tickers["AAPL"].info
tickers.tickers["MSFT"].history(period="1mo")
```

---

## Screener & Equity Query

Build custom stock screens.

```python
from yfinance import Screener, EquityQuery

# Create a query
query = EquityQuery('and', [
    EquityQuery('gt', ['marketcap', 1_000_000_000]),      # market cap > $1B
    EquityQuery('lt', ['peratio', 20]),                     # P/E < 20
    EquityQuery('eq', ['sector', 'Technology'])             # tech sector
])

# Run the screen
screener = Screener()
screener.set_body(query)
result = screener.response

# Available operators: eq, gt, lt, gte, lte, btwn, is_in
# Available fields: marketcap, peratio, sector, industry, dividendyield, etc.
```

---

## Sector & Industry

```python
# Sector data
tech = yf.Sector("technology")
tech.overview
tech.industries    # DataFrame of industries in this sector

# Industry data
semiconductors = yf.Industry("semiconductors")
semiconductors.overview
semiconductors.top_companies

# Valid sector keys:
# basic-materials, communication-services, consumer-cyclical,
# consumer-defensive, energy, financial-services, healthcare,
# industrials, real-estate, technology, utilities
```

---

## Search

```python
search = yf.Search("Tesla")
search.quotes    # matching ticker quotes
search.news      # related news articles
```

---

## Timezone Handling

yfinance returns tz-aware datetime indices (typically `America/New_York`). When filtering or comparing dates, you **must** match timezone awareness to avoid `TypeError: Cannot compare tz-naive and tz-aware datetime-like objects`.

```python
import yfinance as yf
import pandas as pd

hist = yf.Ticker("AAPL").history(period="1y")

# WRONG — tz-naive timestamp vs tz-aware index:
# filtered = hist[hist.index >= pd.Timestamp("2025-01-01")]  # TypeError!

# Option A (recommended): make the comparison timestamp tz-aware
start = pd.Timestamp("2025-01-01", tz="America/New_York")
filtered = hist[hist.index >= start]

# Option B: strip timezone from index first
hist.index = hist.index.tz_localize(None)
filtered = hist[hist.index >= pd.Timestamp("2025-01-01")]
```

Always use **Option A** when you need to preserve timezone info for accurate date boundaries. Use **Option B** when timezone doesn't matter (e.g., daily data aggregation).

---

## Error Handling

```python
import yfinance as yf

try:
    ticker = yf.Ticker("AAPL")
    hist = ticker.history(period="1mo")
    if hist.empty:
        print("No data returned — check ticker symbol or date range")
    else:
        print(hist)
except Exception as e:
    print(f"Error fetching data: {e}")
```

Common issues:
- **Empty DataFrame**: Invalid ticker, delisted stock, or date range outside available data
- **Rate limiting**: Too many requests in short time — add delays between calls
- **Missing fields in `.info`**: Not all fields are available for all tickers (ETFs, mutual funds, foreign stocks may differ)
- **Intraday data limits**: 1m data only available for last ~7 days
- **Timezone mismatch**: See "Timezone Handling" section above — always match tz-awareness when comparing dates
