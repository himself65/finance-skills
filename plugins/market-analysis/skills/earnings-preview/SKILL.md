---
name: earnings-preview
description: >
  Generate a pre-earnings briefing for any stock using Yahoo Finance data.
  Use this skill whenever the user wants to prepare for an upcoming earnings report,
  understand what analysts expect, review a company's beat/miss track record,
  or get a quick overview before an earnings call.
  Triggers include: "earnings preview for AAPL", "what to expect from TSLA earnings",
  "MSFT reports next week", "earnings preview", "pre-earnings analysis",
  "what are analysts expecting for NVDA", "earnings estimates for",
  "will GOOGL beat earnings", "earnings beat/miss history",
  "upcoming earnings", "before earnings", "earnings setup",
  "consensus estimates", "earnings whisper", "EPS expectations",
  "what's the street expecting", "earnings season preview",
  any mention of preparing for or previewing an earnings report,
  or any request to understand expectations ahead of a company's earnings date.
  Always use this skill when the user mentions a ticker in context of upcoming earnings,
  even if they don't say "preview" explicitly.
---

# Earnings Preview Skill

Generates a pre-earnings briefing using Yahoo Finance data via [yfinance](https://github.com/ranaroussi/yfinance). Pulls together upcoming earnings date, consensus estimates, historical accuracy, analyst sentiment, and key financial context — everything you need before an earnings call.

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

## Step 2: Identify the Ticker and Gather All Data

Extract the ticker symbol from the user's request. If they mention a company name without a ticker, look it up. Then fetch all relevant data in one script to minimize API calls.

```python
import yfinance as yf
import pandas as pd
from datetime import datetime

ticker = yf.Ticker("AAPL")  # replace with actual ticker

# --- Core data ---
info = ticker.info
calendar = ticker.calendar

# --- Estimates ---
earnings_est = ticker.earnings_estimate
revenue_est = ticker.revenue_estimate

# --- Historical track record ---
earnings_hist = ticker.earnings_history

# --- Analyst sentiment ---
price_targets = ticker.analyst_price_targets
recommendations = ticker.recommendations

# --- Recent financials for context ---
quarterly_income = ticker.quarterly_income_stmt
quarterly_cashflow = ticker.quarterly_cashflow
```

### What to extract from each source

| Data Source | Key Fields | Purpose |
|---|---|---|
| `calendar` | Earnings Date, Ex-Dividend Date | When earnings are and key dates |
| `earnings_estimate` | avg, low, high, numberOfAnalysts, yearAgoEps, growth (for 0q, +1q, 0y, +1y) | Consensus EPS expectations |
| `revenue_estimate` | avg, low, high, numberOfAnalysts, yearAgoRevenue, growth | Revenue expectations |
| `earnings_history` | epsEstimate, epsActual, epsDifference, surprisePercent | Beat/miss track record |
| `analyst_price_targets` | current, low, high, mean, median | Street price targets |
| `recommendations` | Buy/Hold/Sell counts | Sentiment distribution |
| `quarterly_income_stmt` | TotalRevenue, NetIncome, BasicEPS | Recent trajectory |

---

## Step 3: Build the Earnings Preview

Assemble the data into a structured briefing. The goal is to give the user everything they need in one glance.

### Section 1: Earnings Date & Key Info

Report the upcoming earnings date from `calendar`. Include:
- Company name, ticker, sector, industry
- Upcoming earnings date (and whether it's before/after market)
- Current stock price and recent performance (1-week, 1-month)
- Market cap

### Section 2: Consensus Estimates

Present the current quarter estimates from `earnings_estimate` and `revenue_estimate`:

| Metric | Consensus | Low | High | # Analysts | Year Ago | Growth |
|---|---|---|---|---|---|---|
| EPS | $1.42 | $1.35 | $1.50 | 28 | $1.26 | +12.7% |
| Revenue | $94.3B | $92.1B | $96.8B | 25 | $89.5B | +5.4% |

If the estimate range is unusually wide (high/low spread > 20% of consensus), note that as a sign of high uncertainty.

### Section 3: Historical Beat/Miss Track Record

From `earnings_history`, show the last 4 quarters:

| Quarter | EPS Est | EPS Actual | Surprise | Beat/Miss |
|---|---|---|---|---|
| Q3 2024 | $1.35 | $1.40 | +3.7% | Beat |
| Q2 2024 | $1.30 | $1.33 | +2.3% | Beat |
| Q1 2024 | $1.52 | $1.53 | +0.7% | Beat |
| Q4 2023 | $2.10 | $2.18 | +3.8% | Beat |

Summarize: "AAPL has beaten EPS estimates in 4 of the last 4 quarters by an average of 2.6%."

### Section 4: Analyst Sentiment

From `recommendations` and `analyst_price_targets`:

- Current recommendation distribution (Strong Buy / Buy / Hold / Sell / Strong Sell)
- Price target range: low, mean, median, high vs. current price
- Implied upside/downside from mean target

### Section 5: Key Metrics to Watch

Based on the quarterly financials, highlight 3-5 things the market will focus on:
- Revenue growth trend (accelerating or decelerating?)
- Margin trajectory (expanding or compressing?)
- Any notable line items that changed significantly quarter-over-quarter
- Segment breakdowns if available in the data

This section requires judgment — think about what matters for this specific company/sector.

---

## Step 4: Respond to the User

Present the preview as a clean, structured briefing:

1. **Lead with the headline**: "AAPL reports earnings on [date]. Here's what to expect."
2. **Show all 5 sections** with clear headers and tables
3. **End with a brief summary**: 2-3 sentences capturing the overall setup (bullish/bearish lean based on estimates, track record, and sentiment — frame as "the street expects" not personal recommendation)

### Caveats to include
- Estimates can change up until the report date
- Historical beats don't guarantee future beats
- Yahoo Finance data may lag real-time consensus by a few hours
- This is not financial advice

---

## Reference Files

- `references/api_reference.md` — Detailed yfinance API reference for earnings and estimate methods

Read the reference file when you need exact method signatures or edge case handling.
