---
name: estimate-analysis
description: >
  Deep-dive into analyst estimates and revision trends for any stock using Yahoo Finance data.
  Use this skill whenever the user wants to understand the direction of analyst estimates,
  how EPS or revenue forecasts have changed over time, compare estimate distributions,
  or analyze growth projections across periods.
  Triggers include: "estimate analysis for AAPL", "analyst estimate trends for NVDA",
  "EPS revisions for TSLA", "how have estimates changed for MSFT",
  "estimate revisions", "EPS trend", "revenue estimates",
  "consensus changes", "analyst estimates", "estimate distribution",
  "growth estimates for", "how many analysts cover",
  "are estimates going up or down", "estimate momentum",
  "revision trend", "earnings estimate history",
  "forward estimates", "next quarter estimates",
  "annual estimates", "FY estimates", "estimate spread",
  "bull case vs bear case estimates", "estimate range",
  any mention of analyzing, tracking, or comparing analyst estimates/revisions,
  or any request about understanding where analyst forecasts are heading.
  Always use this skill when the user asks about estimates beyond a simple lookup —
  if they want context, trends, or analysis of the numbers, this is the right skill.
---

# Estimate Analysis Skill

Deep-dives into analyst estimates and revision trends using Yahoo Finance data via [yfinance](https://github.com/ranaroussi/yfinance). Covers EPS and revenue estimate distributions, revision momentum, growth projections, and multi-period comparisons — the full picture of where the street thinks a company is heading.

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

The user might want different levels of analysis. Route accordingly:

| User Request | Focus Area | Key Sections |
|---|---|---|
| General estimate analysis | Full analysis | All sections |
| "How have estimates changed" | Revision trends | EPS Trend + Revisions |
| "What are analysts expecting" | Current consensus | Estimate overview |
| "Growth estimates" | Growth projections | Growth Estimates |
| "Bull vs bear case" | Estimate range | High/low spread analysis |
| Compare estimates across periods | Multi-period | Period comparison table |

When in doubt, provide the full analysis — more context is better.

---

## Step 4: Build the Estimate Analysis

### Section 1: Estimate Overview

Present the current consensus for all available periods from `earnings_estimate` and `revenue_estimate`:

**EPS Estimates:**

| Period | Consensus | Low | High | Range Width | # Analysts | YoY Growth |
|---|---|---|---|---|---|---|
| Current Qtr (0q) | $1.42 | $1.35 | $1.50 | $0.15 (10.6%) | 28 | +12.7% |
| Next Qtr (+1q) | $1.58 | $1.48 | $1.68 | $0.20 (12.7%) | 25 | +8.3% |
| Current Year (0y) | $6.70 | $6.50 | $6.95 | $0.45 (6.7%) | 30 | +10.2% |
| Next Year (+1y) | $7.45 | $7.10 | $7.85 | $0.75 (10.1%) | 28 | +11.2% |

**Revenue Estimates:**

| Period | Consensus | Low | High | # Analysts | YoY Growth |
|---|---|---|---|---|---|
| Current Qtr | $94.3B | $92.1B | $96.8B | 25 | +5.4% |
| Next Qtr | $102.1B | $99.5B | $105.0B | 22 | +6.1% |

Calculate and flag:
- **Range width** as % of consensus — wide ranges (>15%) signal high uncertainty
- **Analyst coverage** — fewer than 5 analysts means thin coverage, note this
- **Growth trajectory** — is growth accelerating or decelerating across periods?

### Section 2: Revision Trends (EPS Trend)

This is often the most actionable section. From `eps_trend`, show how estimates have moved:

| Period | Current | 7 Days Ago | 30 Days Ago | 60 Days Ago | 90 Days Ago |
|---|---|---|---|---|---|
| Current Qtr | $1.42 | $1.41 | $1.40 | $1.38 | $1.35 |
| Next Qtr | $1.58 | $1.57 | $1.56 | $1.55 | $1.54 |
| Current Year | $6.70 | $6.68 | $6.65 | $6.58 | $6.50 |
| Next Year | $7.45 | $7.43 | $7.40 | $7.35 | $7.28 |

Summarize the trend: "Current quarter EPS estimates have risen 5.2% over the last 90 days, with most of the increase in the last 30 days — accelerating upward revision momentum."

**Key interpretation:**
- Rising estimates ahead of earnings = positive setup (the bar is rising)
- Falling estimates = analysts cutting numbers, often a negative signal
- Flat estimates = no new information being priced in
- Recent acceleration/deceleration matters more than the total move

### Section 3: Revision Breadth (EPS Revisions)

From `eps_revisions`, show the up vs. down count:

| Period | Up (last 7d) | Down (last 7d) | Up (last 30d) | Down (last 30d) |
|---|---|---|---|---|
| Current Qtr | 5 | 1 | 12 | 3 |
| Next Qtr | 3 | 2 | 8 | 5 |

Calculate a revision ratio: Up / (Up + Down). Ratios above 0.7 are strongly bullish; below 0.3 are bearish.

### Section 4: Growth Estimates

From `growth_estimates`, compare the company's expected growth to benchmarks:

| Entity | Current Qtr | Next Qtr | Current Year | Next Year | Past 5Y Annual |
|---|---|---|---|---|---|
| AAPL | +12.7% | +8.3% | +10.2% | +11.2% | +14.5% |
| Industry | +9.1% | +7.0% | +8.5% | +9.0% | — |
| Sector | +11.3% | +8.8% | +10.0% | +10.5% | — |
| S&P 500 | +7.5% | +6.2% | +8.0% | +8.5% | — |

Highlight whether the company is expected to grow faster or slower than its peers.

### Section 5: Historical Estimate Accuracy

From `earnings_history`, assess how reliable estimates have been:

| Quarter | Estimate | Actual | Surprise % | Direction |
|---|---|---|---|---|
| Q3 2024 | $1.35 | $1.40 | +3.7% | Beat |
| Q2 2024 | $1.30 | $1.33 | +2.3% | Beat |
| Q1 2024 | $1.52 | $1.53 | +0.7% | Beat |
| Q4 2023 | $2.10 | $2.18 | +3.8% | Beat |

Calculate:
- **Beat rate**: X of 4 quarters
- **Average surprise**: magnitude and direction
- **Trend in surprise**: Are beats getting bigger or smaller? A shrinking surprise with rising estimates could mean the bar is catching up to reality.

---

## Step 5: Synthesize and Respond

Present the analysis with clear structure:

1. **Lead with the key insight**: "AAPL estimates are trending higher across all periods, with positive revision breadth (80% of recent revisions are upward)."

2. **Show the tables** for each section the user cares about

3. **Provide interpretive context**:
   - Is the revision trend confirming or contradicting the stock's recent price action?
   - How does the growth outlook compare to what's priced into the current P/E?
   - What's the relationship between estimate accuracy history and current estimate levels?

4. **Flag risks and nuances**:
   - Estimates cluster around consensus — the "real" distribution of outcomes is wider than low/high suggests
   - Revision momentum can reverse quickly on a single data point (guidance change, macro event)
   - Yahoo Finance estimates may lag behind real-time consensus providers by hours or days
   - Growth estimates for out-years (+1y) are inherently less reliable

### Caveats to always include
- Analyst estimates reflect a consensus view, not certainty
- Estimate revisions are a signal but not a guarantee of future performance
- This is not financial advice

---

## Reference Files

- `references/api_reference.md` — Detailed yfinance API reference for all estimate-related methods

Read the reference file when you need exact return formats or edge case handling.
