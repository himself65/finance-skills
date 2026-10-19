---
name: earnings-recap
description: >
  Analyze a company's most recent (or a specified past) earnings report from Yahoo
  Finance data (yfinance): actual vs estimated EPS, surprise size, revenue and margin
  trends, and the stock's price reaction. Use this skill whenever the user asks how
  earnings went — beat or miss, earnings surprise, quarterly results, the
  post-earnings move, or an earnings call recap — including casual references to a
  past report such as "AMZN reported last night" or "how did they do". For an
  upcoming report, use earnings-preview.
---

# Earnings Recap Skill

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Generates a post-earnings analysis using Yahoo Finance data via [yfinance](https://github.com/ranaroussi/yfinance). Covers the actual vs estimated numbers, surprise magnitude, stock price reaction, and financial context — a complete picture of what happened.

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

## Step 2: Identify the Ticker and Gather Data

Extract the ticker from the user's request. Fetch all relevant post-earnings data in one script.

```python
import yfinance as yf
import pandas as pd

ticker = yf.Ticker("AAPL")  # replace with actual ticker

# --- Earnings results ---
earnings_dates = ticker.get_earnings_dates(limit=12)  # report timestamps, newest first
earnings_hist = ticker.earnings_history               # last 4 quarters, indexed by fiscal quarter-end, oldest first

# --- Financial statements (about five quarters, newest first) ---
quarterly_income = ticker.quarterly_income_stmt
quarterly_cashflow = ticker.quarterly_cashflow
quarterly_balance = ticker.quarterly_balance_sheet

# --- Context ---
info = ticker.info
news = ticker.news
recommendations = ticker.recommendations
```

### What to extract

| Data Source | Key Fields | Purpose |
|---|---|---|
| `get_earnings_dates()` | Earnings Date, EPS Estimate, Reported EPS, Surprise(%) | Which report, when, and the beat/miss |
| `earnings_history` | epsEstimate, epsActual, epsDifference, surprisePercent | Last four quarters' results by fiscal quarter |
| `quarterly_income_stmt` | TotalRevenue, GrossProfit, OperatingIncome, NetIncome, BasicEPS | Actual financials |
| `history()` | Daily closes around each report | Stock price reaction |
| `info` | currentPrice, marketCap, forwardPE | Current context |
| `news` | Recent headlines | Earnings-related news |

---

## Step 3: Find the Report and Measure the Reaction

`earnings_history` is indexed by fiscal quarter-end, not by announcement date, so take report timing from `get_earnings_dates()`: the most recent report is the newest row with a `Reported EPS`. Its timestamp (US Eastern) sets the reaction window: at or after 16:00 means the company reported after the close; anything earlier means before the open or, occasionally, during the session. If the user asked about a specific quarter, use that row instead.

```python
def earnings_reaction(ticker, report_ts):
    """% move from the last close before the report to the first close after it."""
    daily = ticker.history(start=(report_ts - pd.Timedelta(days=10)).date(),
                           end=(report_ts + pd.Timedelta(days=10)).date())
    closes = daily["Close"]
    days = closes.index.date
    d = report_ts.date()
    if report_ts.hour >= 16:  # reported after the close: report-day close -> next close
        pre, post = closes[days <= d], closes[days > d]
    else:                     # before the open or intraday: prior close -> report-day close
        pre, post = closes[days < d], closes[days >= d]
    if pre.empty or post.empty:
        return None           # the reaction session hasn't closed yet
    return (post.iloc[0] / pre.iloc[-1] - 1) * 100

reported = earnings_dates[earnings_dates["Reported EPS"].notna()]
latest_ts = reported.index[0]
reaction_pct = earnings_reaction(ticker, latest_ts)

# Typical earnings-day move over the prior four reports
prior_moves = [earnings_reaction(ticker, ts) for ts in reported.index[1:5]]
avg_abs_move = pd.Series([abs(m) for m in prior_moves if m is not None]).mean()
```

If `reaction_pct` is `None`, the report came after the most recent close; say the regular-session reaction is still pending (an intraday `history(..., prepost=True)` call shows the after-hours move if the user wants it).

---

## Step 4: Build the Earnings Recap

Cover these areas, leading with the result:

1. **Headline result** — EPS actual vs estimate with the surprise %, revenue with year-over-year growth, and the stock's reaction.
2. **Estimates vs actuals** — EPS estimate, actual, and surprise ($ and %) for the quarter in question.
3. **Quarterly trends** — revenue, gross margin, operating margin, and EPS for the recent quarters, with margins computed from the statements (gross profit / revenue, operating income / revenue). yfinance usually returns about five quarters, so year-over-year growth is available for the latest quarter only (column 0 vs column 4); show sequential change for the others rather than inventing a comparison.
4. **Price reaction** — the move in the reaction session, how it compares with the stock's average absolute earnings move over the prior four reports, and whether the stock has since held, given back, or extended the move.
5. **What changed** — margin direction vs the prior quarter, any shift in the revenue growth trajectory, how this surprise compares with the company's usual pattern, and current analyst sentiment if available.

---

## Step 5: Respond to the User

Open with the headline — which quarter, when it was reported, the beat or miss, revenue growth, and the reaction — then the supporting tables. Say what matters: whether this was a meaningful beat or a low bar cleared, and whether the trend is improving or deteriorating. Keep it factual and leave out investment recommendations.

Include the caveats that apply: Yahoo Finance data doesn't capture everything from the call (guidance, segment detail), revenue is compared year over year from the statements rather than against a revenue consensus, the price reaction can reflect a broader market move that day, and this is not financial advice.

---

## Reference Files

- `references/api_reference.md` — Detailed yfinance API reference for earnings history and financial statement methods

Read the reference file when you need exact method signatures or to handle edge cases in the financial data.
