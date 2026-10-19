---
name: earnings-preview
description: >
  Build a pre-earnings briefing for a stock from Yahoo Finance data (yfinance): the
  upcoming report date and timing, consensus EPS and revenue estimates with their range,
  the beat/miss track record, analyst ratings and price targets, and what to watch in
  the print. Use this skill whenever the user is preparing for an upcoming earnings
  report or asks what the street expects — consensus or whisper numbers, EPS
  expectations, whether a company will beat, an earnings setup, or an earnings-season
  preview — and whenever a ticker comes up in the context of upcoming earnings, even
  without the word "preview". For results that are already out, use earnings-recap.
---

# Earnings Preview Skill

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Generates a pre-earnings briefing using Yahoo Finance data via [yfinance](https://github.com/ranaroussi/yfinance). Pulls together upcoming earnings date, consensus estimates, historical accuracy, analyst sentiment, and key financial context — everything you need before an earnings call.

**Important**: Data is for research and educational purposes only. Not financial advice. yfinance is not affiliated with Yahoo, Inc.

---

## Step 1: Ensure yfinance Is Available

**Current environment status:**

```
!`python3 -c "exec('try:\n import yfinance\n print(\'yfinance \' + yfinance.__version__ + \' installed\')\nexcept Exception:\n print(\'YFINANCE_NOT_INSTALLED\')')"`
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

ticker = yf.Ticker("AAPL")  # replace with actual ticker

# --- Core data ---
info = ticker.info
calendar = ticker.calendar
earnings_dates = ticker.get_earnings_dates(limit=8)  # report timestamps; the upcoming one has no Reported EPS yet
hist = ticker.history(period="1mo")                  # recent price performance

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
| `get_earnings_dates()` | Earnings Date (tz-aware timestamp), EPS Estimate, Reported EPS | Report timing: the upcoming row has no Reported EPS; a time at or after 16:00 ET means after the close, earlier times mean before the open |
| `earnings_estimate` | avg, low, high, numberOfAnalysts, yearAgoEps, growth (for 0q, +1q, 0y, +1y) | Consensus EPS expectations |
| `revenue_estimate` | avg, low, high, numberOfAnalysts, yearAgoRevenue, growth | Revenue expectations |
| `earnings_history` | epsEstimate, epsActual, epsDifference, surprisePercent | Beat/miss track record (indexed by fiscal quarter-end, oldest first) |
| `analyst_price_targets` | current, low, high, mean, median | Street price targets |
| `recommendations` | Buy/Hold/Sell counts | Sentiment distribution |
| `quarterly_income_stmt` | TotalRevenue, NetIncome, BasicEPS | Recent trajectory |

---

## Step 3: Build the Earnings Preview

The briefing should let the user see the setup at a glance. Cover these five areas; if the data for one is missing, say so in a line rather than dropping it.

1. **Date and context** — company, ticker, sector and industry; the report date and whether it lands before the open or after the close; current price with 1-week and 1-month performance; market cap.
2. **Consensus estimates** — a table of this quarter's EPS and revenue consensus with low, high, analyst count, year-ago value, and expected growth. A high/low spread wider than about 20% of consensus signals unusual uncertainty; say so when you see it.
3. **Beat/miss track record** — the last four quarters of estimated vs actual EPS with surprise %, summarized as a beat count and average surprise.
4. **Analyst sentiment** — the rating distribution (strong buy through strong sell) and the price-target range (low, mean, median, high), with the implied upside or downside from the mean target.
5. **What to watch** — the few things the market will focus on in this print, chosen for this company and sector: revenue growth accelerating or decelerating, margins expanding or compressing, line items that moved sharply quarter over quarter, and segment trends where the data has them. This is the judgment part of the briefing.

---

## Step 4: Respond to the User

Open with the headline — the report date and a one-line read of the setup — then the five areas above, using tables where they help. Close with a short read of the overall setup drawn from the estimates, track record, and sentiment, framed as what the street expects rather than a recommendation.

Include the caveats that apply: estimates can change until the report date, past beats don't guarantee future ones, Yahoo Finance consensus can lag real-time providers by a few hours, and this is not financial advice.

---

## Reference Files

- `references/api_reference.md` — Detailed yfinance API reference for earnings and estimate methods

Read the reference file when you need exact method signatures or edge case handling.
