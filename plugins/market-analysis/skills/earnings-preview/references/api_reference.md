# Earnings Preview — yfinance API Reference

Detailed reference for the yfinance methods used by the earnings-preview skill.

---

## Calendar

```python
ticker.calendar
```

Returns a dictionary with upcoming events:
- `Earnings Date` — list of datetime objects (usually a range like [start, end])
- `Ex-Dividend Date` — next ex-dividend date
- `Dividend Date` — next dividend payment date

**Edge cases:**
- Some tickers return an empty dict if no upcoming events are scheduled
- Earnings dates may show as a 2-day range (the company hasn't specified exact date/time)

---

## Earnings Estimate

```python
ticker.earnings_estimate
```

Returns a DataFrame indexed by period:
- `0q` — current quarter
- `+1q` — next quarter
- `0y` — current year
- `+1y` — next year

Columns:
- `numberOfAnalysts` — number of analysts covering
- `avg` — consensus average EPS
- `low` — lowest estimate
- `high` — highest estimate
- `yearAgoEps` — EPS from the same period last year
- `growth` — expected growth rate (decimal, e.g., 0.127 = 12.7%)

---

## Revenue Estimate

```python
ticker.revenue_estimate
```

Same structure as `earnings_estimate` but for revenue:
- `numberOfAnalysts`, `avg`, `low`, `high`, `yearAgoRevenue`, `growth`

**Note**: Revenue figures are in raw numbers (not millions/billions). Format appropriately for display.

---

## Earnings History

```python
ticker.earnings_history
```

Returns a DataFrame with the last 4 quarters of actual vs estimated earnings:

Columns:
- `epsEstimate` — consensus EPS estimate at the time
- `epsActual` — reported EPS
- `epsDifference` — actual minus estimate
- `surprisePercent` — surprise as a percentage (decimal)

Index is datetime of each earnings report.

**Note**: `surprisePercent` is already in decimal form (0.037 = 3.7%). Multiply by 100 for display.

---

## Analyst Price Targets

```python
ticker.analyst_price_targets
```

Returns a dictionary:
- `current` — current price
- `low` — lowest analyst target
- `high` — highest analyst target
- `mean` — average target
- `median` — median target

---

## Recommendations

```python
ticker.recommendations
```

Returns a DataFrame with recommendation counts by period. Columns typically:
- `strongBuy`, `buy`, `hold`, `sell`, `strongSell`
- Index represents the period

Use the most recent row for current analyst sentiment distribution.

---

## Quarterly Financial Statements

```python
ticker.quarterly_income_stmt   # Income statement
ticker.quarterly_balance_sheet  # Balance sheet
ticker.quarterly_cashflow       # Cash flow
```

Each returns a DataFrame with financial line items as rows and quarter dates as columns (most recent first).

Key income statement rows for earnings preview:
- `Total Revenue`
- `Gross Profit`
- `Operating Income`
- `Net Income`
- `Basic EPS` / `Diluted EPS`
- `EBITDA`

**Tip**: Compare the last 2-4 quarters to identify trends in revenue growth, margin expansion/compression, and EPS trajectory.

---

## Company Info

```python
ticker.info
```

Key fields for context:
- `shortName` — company name
- `sector`, `industry` — classification
- `marketCap` — market capitalization
- `currentPrice` — current stock price
- `previousClose` — last closing price
- `trailingPE`, `forwardPE` — P/E ratios
- `fiftyTwoWeekHigh`, `fiftyTwoWeekLow` — 52-week range

---

## Historical Prices (for recent performance)

```python
# 1-month performance
hist = ticker.history(period="1mo")
# 1-week performance
hist = ticker.history(period="5d")
```

Use to calculate % change for recent performance context.

---

## Error Handling

Always wrap data fetches in try/except:

```python
try:
    data = ticker.earnings_estimate
    if data is None or (hasattr(data, 'empty') and data.empty):
        print("No earnings estimate data available")
except Exception as e:
    print(f"Error: {e}")
```

Common issues:
- **No calendar data**: Company hasn't announced next earnings date
- **Empty estimates**: Ticker may not have analyst coverage (small caps, foreign stocks)
- **Stale data**: Yahoo Finance estimates may not update in real-time; note this to the user
