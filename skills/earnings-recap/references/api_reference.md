# Earnings Recap — yfinance API Reference

Detailed reference for the yfinance methods used by the earnings-recap skill.

---

## Earnings History

```python
ticker.earnings_history
```

Returns a DataFrame with the last 4 quarters of actual vs estimated earnings:

Columns:
- `epsEstimate` — consensus EPS estimate at the time of reporting
- `epsActual` — reported EPS
- `epsDifference` — actual minus estimate
- `surprisePercent` — surprise as a percentage (decimal form: 0.037 = 3.7%)

Index is datetime of each earnings report date.

**Usage for recap**: The most recent row (index[0]) is the latest earnings report. Use this as the primary data point for the recap.

---

## Quarterly Financial Statements

### Income Statement

```python
ticker.quarterly_income_stmt
```

Returns a DataFrame with financial line items as rows and quarter-end dates as columns (most recent first).

Key rows for earnings recap:
- `Total Revenue` — top-line revenue
- `Cost Of Revenue` — COGS
- `Gross Profit` — revenue minus COGS
- `Operating Income` — EBIT
- `Net Income` — bottom line
- `Basic EPS` — earnings per share (basic)
- `Diluted EPS` — earnings per share (diluted)
- `EBITDA` — if available

**Margin calculations:**
```python
gross_margin = df.loc['Gross Profit'] / df.loc['Total Revenue']
operating_margin = df.loc['Operating Income'] / df.loc['Total Revenue']
net_margin = df.loc['Net Income'] / df.loc['Total Revenue']
```

**YoY Growth:**
```python
# Columns are ordered most-recent-first
# Column 0 = latest quarter, Column 4 = same quarter last year (if available)
# Match by quarter (e.g., Q3 2024 vs Q3 2023)
revenue = df.loc['Total Revenue']
yoy_growth = (revenue.iloc[0] - revenue.iloc[3]) / abs(revenue.iloc[3])
```

Note: Column indexing depends on how many quarters are returned. Typically 4-5 quarters are available.

### Cash Flow Statement

```python
ticker.quarterly_cashflow
```

Key rows:
- `Operating Cash Flow` — cash from operations
- `Capital Expenditure` — capex
- `Free Cash Flow` — OCF minus capex

### Balance Sheet

```python
ticker.quarterly_balance_sheet
```

Key rows:
- `Total Assets`
- `Total Debt`
- `Cash And Cash Equivalents`
- `Total Stockholders Equity`

---

## Historical Prices

```python
# Around earnings date
from datetime import timedelta
hist = ticker.history(
    start=earnings_date - timedelta(days=10),
    end=earnings_date + timedelta(days=10)
)
```

Returns DataFrame with: Open, High, Low, Close, Volume.

**Price reaction calculation tips:**
- After-hours reporters: compare prior day's Close to next day's Open (gap) and next day's Close (full reaction)
- Before-market reporters: compare prior day's Close to same day's Close
- The biggest single-day |%change| near the earnings date is usually the reaction day
- Volume spike confirms the reaction day

---

## Company Info

```python
ticker.info
```

Key fields for context:
- `shortName` — company name
- `sector`, `industry`
- `marketCap`
- `currentPrice`, `previousClose`
- `forwardPE`, `trailingPE`
- `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`

---

## News

```python
ticker.news
```

Returns a list of dicts:
- `title` — headline
- `link` — URL
- `publisher` — source name
- `providerPublishTime` — unix timestamp

Filter for recent news around the earnings date for earnings-related headlines.

---

## Recommendations

```python
ticker.recommendations
```

Returns a DataFrame with columns: `strongBuy`, `buy`, `hold`, `sell`, `strongSell`.

Use the most recent row to show current analyst sentiment distribution. Compare to the prior period to detect any post-earnings sentiment shifts.

---

## Error Handling

```python
try:
    hist = ticker.earnings_history
    if hist is None or (hasattr(hist, 'empty') and hist.empty):
        print("No earnings history — ticker may not have reported recently")
except Exception as e:
    print(f"Error: {e}")
```

Common issues:
- **No earnings history**: Company hasn't reported yet, or it's an ETF/fund
- **Missing financial statement rows**: Not all companies report the same line items; check with `.loc` and handle KeyError
- **Quarterly alignment**: Q-end dates in financial statements don't always align perfectly with calendar quarters; use the dates as-is from yfinance
