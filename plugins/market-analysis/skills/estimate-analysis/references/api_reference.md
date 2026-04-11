# Estimate Analysis — yfinance API Reference

Detailed reference for the yfinance estimate and analysis methods.

---

## Earnings Estimate

```python
ticker.earnings_estimate
```

Returns a DataFrame indexed by period with columns:
- `numberOfAnalysts` — analyst count
- `avg` — consensus average EPS
- `low` — lowest EPS estimate
- `high` — highest EPS estimate
- `yearAgoEps` — EPS from same period last year
- `growth` — expected growth rate (decimal: 0.127 = 12.7%)

Periods:
- `0q` — current quarter
- `+1q` — next quarter
- `0y` — current fiscal year
- `+1y` — next fiscal year

---

## Revenue Estimate

```python
ticker.revenue_estimate
```

Same period structure as earnings_estimate. Columns:
- `numberOfAnalysts`
- `avg` — consensus revenue
- `low`, `high` — range
- `yearAgoRevenue` — revenue from same period last year
- `growth` — expected growth rate (decimal)

**Note**: Revenue figures are in raw numbers. Format for display:
```python
def format_revenue(val):
    if val >= 1e12: return f"${val/1e12:.1f}T"
    if val >= 1e9:  return f"${val/1e9:.1f}B"
    if val >= 1e6:  return f"${val/1e6:.1f}M"
    return f"${val:,.0f}"
```

---

## EPS Trend

```python
ticker.eps_trend
```

Shows how the EPS consensus has changed over time. Returns a DataFrame with:

Index: same periods (0q, +1q, 0y, +1y)
Columns:
- `current` — current estimate
- `7daysAgo` — estimate 7 days ago
- `30daysAgo` — estimate 30 days ago
- `60daysAgo` — estimate 60 days ago
- `90daysAgo` — estimate 90 days ago

**Usage**: Calculate the change over each window to identify revision momentum:
```python
trend = ticker.eps_trend
for period in trend.index:
    row = trend.loc[period]
    change_90d = row['current'] - row['90daysAgo']
    change_30d = row['current'] - row['30daysAgo']
    pct_change_90d = change_90d / abs(row['90daysAgo']) * 100
    print(f"{period}: {change_90d:+.2f} ({pct_change_90d:+.1f}%) over 90 days")
```

---

## EPS Revisions

```python
ticker.eps_revisions
```

Shows the count of upward and downward estimate revisions. Returns a DataFrame with:

Index: periods (0q, +1q, 0y, +1y)
Columns:
- `upLast7days` — number of upward revisions in last 7 days
- `upLast30days` — number of upward revisions in last 30 days
- `downLast7days` — number of downward revisions in last 7 days
- `downLast30days` — number of downward revisions in last 30 days

**Revision ratio** (useful metric):
```python
revisions = ticker.eps_revisions
for period in revisions.index:
    row = revisions.loc[period]
    total_30d = row['upLast30days'] + row['downLast30days']
    if total_30d > 0:
        ratio = row['upLast30days'] / total_30d
        print(f"{period}: {ratio:.0%} bullish ({row['upLast30days']} up, {row['downLast30days']} down)")
```

---

## Growth Estimates

```python
ticker.growth_estimates
```

Returns a DataFrame comparing the company's growth rates to benchmarks.

Index (rows): growth periods
- `Current Qtr` or `0q`
- `Next Qtr` or `+1q`
- `Current Year` or `0y`
- `Next Year` or `+1y`
- `Past 5 Years (per annum)` — historical annual growth
- `Next 5 Years (per annum)` — projected annual growth (PEG ratio basis)

Columns: entity names
- The ticker symbol (e.g., `AAPL`)
- `Industry` — industry average
- `Sector` — sector average
- `S&P 500` — market average (may appear as `S&P 500` or `index`)

Values are in decimal form (0.127 = 12.7%). Some cells may be NaN if data is unavailable.

---

## Earnings History

```python
ticker.earnings_history
```

Returns a DataFrame with the last 4 quarters:

Columns:
- `epsEstimate` — consensus at time of reporting
- `epsActual` — reported EPS
- `epsDifference` — actual minus estimate
- `surprisePercent` — in decimal form (0.037 = 3.7%)

Index: earnings report dates (datetime)

---

## Combining Estimate Data

For a comprehensive analysis, fetch all estimate data together:

```python
import yfinance as yf
import pandas as pd

t = yf.Ticker("AAPL")

# All estimate data
data = {
    'earnings_estimate': t.earnings_estimate,
    'revenue_estimate': t.revenue_estimate,
    'eps_trend': t.eps_trend,
    'eps_revisions': t.eps_revisions,
    'growth_estimates': t.growth_estimates,
    'earnings_history': t.earnings_history,
}

# Check what's available
for name, df in data.items():
    if df is not None and not (hasattr(df, 'empty') and df.empty):
        print(f"{name}: {df.shape}")
    else:
        print(f"{name}: NO DATA")
```

---

## Error Handling

```python
try:
    est = ticker.earnings_estimate
    if est is None or (hasattr(est, 'empty') and est.empty):
        print("No earnings estimates — may lack analyst coverage")
except Exception as e:
    print(f"Error: {e}")
```

Common issues:
- **No estimates**: Small-cap or foreign stocks may have no analyst coverage
- **Partial data**: Some periods may have data while others are NaN
- **Stale data**: Yahoo Finance may not reflect the most recent revision; note lag to user
- **Growth estimates missing benchmarks**: Industry/sector/S&P columns may be NaN for some companies
- **EPS trend columns**: Column names may vary slightly — check `df.columns` if expected names don't match
