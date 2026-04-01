---
name: earnings-recap
description: >
  Generate a post-earnings analysis for any stock using Yahoo Finance data.
  Use this skill whenever the user wants to review what happened after a company reported earnings,
  understand the beat/miss result, see how the stock reacted, or get a quick recap of recent earnings.
  Triggers include: "AAPL earnings recap", "how did TSLA earnings go", "MSFT earnings results",
  "did NVDA beat earnings", "earnings recap", "post-earnings analysis",
  "earnings surprise", "what happened with GOOGL earnings",
  "earnings reaction", "stock moved after earnings", "earnings report summary",
  "EPS beat or miss", "revenue beat or miss", "after earnings",
  "earnings results", "quarterly results for", "how were earnings",
  "AMZN reported last night", "earnings call recap",
  any mention of reviewing or summarizing earnings that already happened,
  or any request about a company's most recent earnings outcome.
  Always use this skill when the user references a past earnings event,
  even if they just say something like "AAPL reported" or "how did they do".
---

# Earnings Recap Skill

Generates a post-earnings analysis using Yahoo Finance data via [yfinance](https://github.com/ranaroussi/yfinance). Covers the actual vs estimated numbers, surprise magnitude, stock price reaction, and financial context — a complete picture of what happened.

**Important**: Data is for research and educational purposes only. Not financial advice. yfinance is not affiliated with Yahoo, Inc.

---

## Step 1: Ensure yfinance Is Available

**Current environment status:**

```
!`python3 -c "import yfinance; print('yfinance ' + yfinance.__version__ + ' installed')" 2>/dev/null || echo "YFINANCE_NOT_INSTALLED"`
```

If `YFINANCE_NOT_INSTALLED`, install it:

```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance"])
```

If already installed, skip to the next step.

---

## Step 2: Identify the Ticker and Gather Data

Extract the ticker from the user's request. Fetch all relevant post-earnings data in one script.

```python
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

ticker = yf.Ticker("AAPL")  # replace with actual ticker

# --- Earnings result ---
earnings_hist = ticker.earnings_history

# --- Financial statements ---
quarterly_income = ticker.quarterly_income_stmt
quarterly_cashflow = ticker.quarterly_cashflow
quarterly_balance = ticker.quarterly_balance_sheet

# --- Price reaction ---
# Get ~30 days of history to capture the reaction window
hist = ticker.history(period="1mo")

# --- Context ---
info = ticker.info
news = ticker.news
recommendations = ticker.recommendations
```

### What to extract

| Data Source | Key Fields | Purpose |
|---|---|---|
| `earnings_history` | epsEstimate, epsActual, epsDifference, surprisePercent | Beat/miss result |
| `quarterly_income_stmt` | TotalRevenue, GrossProfit, OperatingIncome, NetIncome, BasicEPS | Actual financials |
| `history()` | Close prices around earnings date | Stock price reaction |
| `info` | currentPrice, marketCap, forwardPE | Current context |
| `news` | Recent headlines | Earnings-related news |

---

## Step 3: Determine the Most Recent Earnings

The most recent earnings result is the first row (most recent date) in `earnings_history`. Use its date to:

1. **Identify the earnings date** for the price reaction analysis
2. **Match to the corresponding quarter** in the financial statements
3. **Calculate stock price reaction** — compare the close before earnings to the next trading day's close (or open, depending on whether earnings were before/after market)

### Price reaction calculation

```python
import numpy as np

# Find the earnings date from earnings_history index
earnings_date = earnings_hist.index[0]  # most recent

# Get daily prices around the earnings date
hist_extended = ticker.history(start=earnings_date - timedelta(days=5),
                                end=earnings_date + timedelta(days=5))

# The reaction is typically measured as:
# - Close on the last trading day before earnings -> Close on the first trading day after
# Be careful with before/after market reports
if len(hist_extended) >= 2:
    pre_price = hist_extended['Close'].iloc[0]
    post_price = hist_extended['Close'].iloc[-1]
    reaction_pct = ((post_price - pre_price) / pre_price) * 100
```

**Note**: The exact reaction window depends on when the company reported (before market open vs after close). The price data will reflect this — look for the biggest gap between consecutive closes near the earnings date.

---

## Step 4: Build the Earnings Recap

### Section 1: Headline Result

Lead with the key numbers:
- **EPS**: Actual vs. Estimate, beat/miss by how much, surprise %
- **Revenue**: Actual vs. prior year (from quarterly_income_stmt TotalRevenue)
- **Stock reaction**: % move on earnings day

Example: "AAPL beat Q3 EPS estimates by 3.7% ($1.40 actual vs $1.35 expected). Revenue grew 5.4% YoY to $94.3B. The stock rose +2.1% on the report."

### Section 2: Earnings vs. Estimates Detail

| Metric | Estimate | Actual | Surprise |
|---|---|---|---|
| EPS | $1.35 | $1.40 | +$0.05 (+3.7%) |

If the user asked about a specific quarter (not the most recent), look further back in `earnings_history`.

### Section 3: Quarterly Financial Trends

Show the last 4 quarters of key metrics from `quarterly_income_stmt`:

| Quarter | Revenue | YoY Growth | Gross Margin | Operating Margin | EPS |
|---|---|---|---|---|---|
| Q3 2024 | $94.3B | +5.4% | 46.2% | 30.1% | $1.40 |
| Q2 2024 | $85.8B | +4.9% | 46.0% | 29.8% | $1.33 |
| Q1 2024 | $119.6B | +2.1% | 45.9% | 33.5% | $2.18 |
| Q4 2023 | $89.5B | -0.3% | 45.2% | 29.2% | $1.26 |

Calculate margins from the raw financials:
- Gross Margin = GrossProfit / TotalRevenue
- Operating Margin = OperatingIncome / TotalRevenue

### Section 4: Stock Price Reaction

- The % move on the earnings day/next session
- How it compares to the stock's average earnings-day move (calculate the average absolute move from the last 4 earnings dates in `earnings_history`)
- Where the stock is now relative to the earnings-day move (has it held, given back gains, extended further?)

### Section 5: Context & What Changed

Based on the data, note:
- Whether margins expanded or compressed vs prior quarter
- Any notable changes in revenue growth trajectory
- How the beat/miss compares to the stock's historical pattern (from the full `earnings_history`)
- Current analyst sentiment from `recommendations` if available

---

## Step 5: Respond to the User

Present the recap as a clean, structured summary:

1. **Lead with the headline**: "AAPL reported Q3 2024 earnings on [date]: Beat EPS by 3.7%, revenue +5.4% YoY."
2. **Show the tables** for detail
3. **Highlight what matters**: Was this a meaningful beat or a low-bar situation? Is the trend improving or deteriorating?
4. **Keep it factual** — present the data, avoid making investment recommendations

### Caveats to include
- Yahoo Finance data may not include all details from the earnings call (guidance, segment breakdowns)
- Revenue estimates are harder to compare precisely — yfinance provides YoY comparison from financial statements
- Price reaction may be influenced by broader market moves on the same day
- This is not financial advice

---

## Reference Files

- `references/api_reference.md` — Detailed yfinance API reference for earnings history and financial statement methods

Read the reference file when you need exact method signatures or to handle edge cases in the financial data.
