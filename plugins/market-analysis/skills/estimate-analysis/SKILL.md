---
name: estimate-analysis
description: >
  Analyze sell-side analyst estimates and how they are changing, using Yahoo Finance
  data (yfinance): EPS and revenue consensus by period, estimate ranges and dispersion,
  revision trends over 7/30/60/90 days and up/down revision breadth, growth estimates
  vs industry, sector, and the S&P 500, and historical estimate accuracy. Use this
  skill when the user wants more than a single estimate lookup: estimate revisions or
  momentum, EPS trend, consensus changes, forward or next-quarter and annual
  estimates, the bull vs bear estimate spread, or growth projections across periods.
---

# Estimate Analysis Skill

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Deep-dives into analyst estimates and revision trends using Yahoo Finance data via [yfinance](https://github.com/ranaroussi/yfinance). Covers EPS and revenue estimate distributions, revision momentum, growth projections, and multi-period comparisons — the full picture of where the street thinks a company is heading.

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

## Step 2: Identify the Ticker and Gather Estimate Data

Extract the ticker from the user's request. Fetch all estimate-related data in one script.

```python
import yfinance as yf
import pandas as pd

ticker = yf.Ticker("AAPL")  # replace with actual ticker

# --- Estimate data ---
earnings_est = ticker.earnings_estimate      # EPS estimates by period
revenue_est = ticker.revenue_estimate        # Revenue estimates by period
eps_trend = ticker.eps_trend                 # EPS estimate changes over time
eps_revisions = ticker.eps_revisions         # Up/down revision counts
growth_est = ticker.growth_estimates         # Growth rate estimates

# --- Historical context ---
earnings_hist = ticker.earnings_history      # Track record
info = ticker.info                           # Company basics
quarterly_income = ticker.quarterly_income_stmt  # Recent actuals
```

### What each data source provides

| Data Source | What It Shows | Why It Matters |
|---|---|---|
| `earnings_estimate` | Current EPS consensus by period (0q, +1q, 0y, +1y) | The estimate levels — what analysts expect |
| `revenue_estimate` | Current revenue consensus by period | Top-line expectations |
| `eps_trend` | How the EPS estimate has changed (7d, 30d, 60d, 90d ago) | Revision direction — rising or falling expectations |
| `eps_revisions` | Count of upward vs downward revisions (7d, 30d) | Revision breadth — are most analysts raising or cutting? |
| `growth_estimates` | Growth rate estimates vs peers and sector | Relative positioning |
| `earnings_history` | Actual vs estimated for last 4 quarters | Calibration — how good are these estimates historically? |

---

## Step 3: Route Based on User Intent

Match the depth of the analysis to the question:

| User Request | Focus Area | Key Sections |
|---|---|---|
| General estimate analysis | Full analysis | All sections |
| "How have estimates changed" | Revision trends | EPS Trend + Revisions |
| "What are analysts expecting" | Current consensus | Estimate overview |
| "Growth estimates" | Growth projections | Growth Estimates |
| "Bull vs bear case" | Estimate range | High/low spread analysis |
| Compare estimates across periods | Multi-period | Period comparison table |

A general request gets the full analysis; a narrow question gets the matching sections.

---

## Step 4: Build the Estimate Analysis

### Section 1: Estimate Overview

Present the current consensus for every available period (0q, +1q, 0y, +1y) from `earnings_estimate` and `revenue_estimate`: consensus, low, high, range width (as a % of consensus), analyst count, and YoY growth. Flag:

- **Range width** — ranges wider than 15% of consensus signal high uncertainty
- **Analyst coverage** — fewer than 5 analysts means thin coverage
- **Growth trajectory** — whether growth accelerates or decelerates across periods

### Section 2: Revision Trends (EPS Trend)

Often the most actionable section. From `eps_trend`, show each period's current estimate against its value 7, 30, 60, and 90 days ago, and summarize the direction and whether the recent moves are accelerating.

How to read it:
- Rising estimates ahead of earnings = positive setup (the bar is rising)
- Falling estimates = analysts cutting numbers, often a negative signal
- Flat estimates = no new information being priced in
- Recent acceleration or deceleration matters more than the total move

### Section 3: Revision Breadth (EPS Revisions)

From `eps_revisions`, show up vs down revision counts over the last 7 and 30 days for each period, and the revision ratio Up / (Up + Down). Ratios above 0.7 are strongly bullish; below 0.3 are bearish.

### Section 4: Growth Estimates

From `growth_estimates`, compare the company's expected growth for each period (and its past 5-year annual growth) with its industry, sector, and the S&P 500, and say whether it is expected to grow faster or slower than its peers.

### Section 5: Historical Estimate Accuracy

From `earnings_history`, show estimate vs actual EPS and the surprise % for the last four quarters, then assess:

- **Beat rate** — how many of the four quarters beat
- **Average surprise** — magnitude and direction
- **Trend in surprise** — are beats getting bigger or smaller? A shrinking surprise with rising estimates can mean the bar is catching up to reality.

---

## Step 5: Synthesize and Respond

Lead with the key insight — the direction and breadth of revisions across periods — then show the tables for the sections the user cares about. Interpret rather than just tabulate: does the revision trend confirm or contradict the stock's recent price action, how does the growth outlook compare with what the current P/E prices in, and what does the estimate-accuracy history say about today's consensus?

Flag the nuances that apply: estimates cluster around consensus, so the real distribution of outcomes is wider than low/high suggests; revision momentum can reverse on a single guidance change or macro event; Yahoo Finance estimates can lag real-time consensus providers by hours or days; out-year (+1y) estimates are inherently less reliable. Close with the standing caveats: analyst estimates reflect a consensus view, not certainty; revisions are a signal, not a guarantee; this is not financial advice.

---

## Reference Files

- `references/api_reference.md` — Detailed yfinance API reference for all estimate-related methods

Read the reference file when you need exact return formats or edge case handling.
