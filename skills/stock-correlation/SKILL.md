---
name: stock-correlation
description: >
  Analyze stock correlations to find related companies and trading pairs.
  Use this skill whenever the user asks about correlated stocks, related companies,
  sector peers, trading pairs, or how two or more stocks move together.
  Triggers include: "what correlates with NVDA", "find stocks related to AMD",
  "correlation between AAPL and MSFT", "what moves with", "sector peers",
  "pair trading", "correlated stocks", "when NVDA drops what else drops",
  "find me a pair for", "stocks that move together", "beta to", "relative performance",
  "which stocks follow AMD", "supply chain partners", "correlation matrix",
  "co-movement", "related tickers", "sympathy plays", "if GOOGL moves what else moves",
  "semiconductor peers", "compare correlation", "hedging pair",
  "sector clustering", "realized correlation", "rolling correlation",
  or any request about finding stocks that move in tandem or inversely.
  Also triggers when the user mentions well-known pairs like AMD/NVDA, GOOGL/AVGO, LITE/COHR
  and wants to understand or find similar relationships.
  Always use this skill even if the user only provides one ticker — infer that they want
  to find correlated peers.
---

# Stock Correlation Analysis Skill

Finds and analyzes correlated stocks using historical price data from Yahoo Finance via [yfinance](https://github.com/ranaroussi/yfinance). Routes to specialized sub-skills based on user intent.

**Important**: This is for research and educational purposes only. Not financial advice. yfinance is not affiliated with Yahoo, Inc.

---

## Step 1: Ensure Dependencies Are Available

Before running any code, install required packages if needed:

```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance", "pandas", "numpy"])
```

Always include this at the top of your script.

---

## Step 2: Route to the Correct Sub-Skill

Classify the user's request and jump to the matching sub-skill section below.

| User Request | Route To | Examples |
|---|---|---|
| Single ticker, wants to find related stocks | **Sub-Skill A: Co-movement Discovery** | "what correlates with NVDA", "find stocks related to AMD", "sympathy plays for TSLA" |
| Two or more specific tickers, wants relationship details | **Sub-Skill B: Return Correlation** | "correlation between AMD and NVDA", "how do LITE and COHR move together", "compare AAPL vs MSFT" |
| Group of tickers, wants structure/grouping | **Sub-Skill C: Sector Clustering** | "correlation matrix for FAANG", "cluster these semiconductor stocks", "sector peers for AMD" |
| Wants time-varying or conditional correlation | **Sub-Skill D: Realized Correlation** | "rolling correlation AMD NVDA", "when NVDA drops what else drops", "how has correlation changed" |

If ambiguous, default to **Sub-Skill A** (Co-movement Discovery) for single tickers, or **Sub-Skill B** (Return Correlation) for two tickers.

### Defaults for all sub-skills

| Parameter | Default |
|---|---|
| Lookback period | `1y` (1 year) |
| Data interval | `1d` (daily) |
| Correlation method | Pearson |
| Minimum correlation threshold | 0.60 |
| Number of results | Top 10 |
| Return type | Daily log returns |
| Rolling window | 60 trading days |

---

## Sub-Skill A: Co-movement Discovery

**Goal**: Given a single ticker, find stocks that move with it.

### A1: Build the peer universe

You need 15-30 candidates. **Do not use hardcoded ticker lists** — build the universe dynamically at runtime. See `references/sector_universes.md` for the full implementation. The approach:

1. **Screen same-industry stocks** using `yf.screen()` + `yf.EquityQuery` to find stocks in the same industry as the target
2. **Broaden to sector** if the industry screen returns fewer than 10 peers
3. **Add thematic/adjacent industries** — read the target's `longBusinessSummary` and screen 1-2 related industries (e.g., a semiconductor company → also screen semiconductor equipment)
4. **Combine, deduplicate, remove target ticker**

### A2: Compute correlations

```python
import yfinance as yf
import pandas as pd
import numpy as np

def discover_comovement(target_ticker, peer_tickers, period="1y"):
    all_tickers = [target_ticker] + [t for t in peer_tickers if t != target_ticker]
    data = yf.download(all_tickers, period=period, auto_adjust=True, progress=False)

    # Extract close prices — yf.download returns MultiIndex (Price, Ticker) columns
    closes = data["Close"].dropna(axis=1, thresh=max(60, len(data) // 2))

    # Log returns
    returns = np.log(closes / closes.shift(1)).dropna()
    corr_series = returns.corr()[target_ticker].drop(target_ticker, errors="ignore")

    # Rank by absolute correlation
    ranked = corr_series.abs().sort_values(ascending=False)

    result = pd.DataFrame({
        "Ticker": ranked.index,
        "Correlation": [round(corr_series[t], 4) for t in ranked.index],
    })
    return result, returns
```

### A3: Present results

Show a ranked table with company names and sectors (fetch via `yf.Ticker(t).info.get("shortName")`):

| Rank | Ticker | Company | Correlation | Why linked |
|---|---|---|---|---|
| 1 | AMD | Advanced Micro Devices | 0.82 | Same industry — GPU/CPU |
| 2 | AVGO | Broadcom | 0.78 | AI infrastructure peer |

Include:
- Top 10 positively correlated stocks
- Any notable negatively correlated stocks (potential hedges)
- Brief explanation of **why** each might be linked (sector, supply chain, customer overlap)

---

## Sub-Skill B: Return Correlation

**Goal**: Deep-dive into the relationship between two (or a few) specific tickers.

### B1: Download and compute

```python
import yfinance as yf
import pandas as pd
import numpy as np

def return_correlation(ticker_a, ticker_b, period="1y"):
    data = yf.download([ticker_a, ticker_b], period=period, auto_adjust=True, progress=False)
    closes = data["Close"][[ticker_a, ticker_b]].dropna()

    returns = np.log(closes / closes.shift(1)).dropna()
    corr = returns[ticker_a].corr(returns[ticker_b])

    # Beta: how much does B move per unit move of A
    cov_matrix = returns.cov()
    beta = cov_matrix.loc[ticker_b, ticker_a] / cov_matrix.loc[ticker_a, ticker_a]

    # R-squared
    r_squared = corr ** 2

    # Rolling 60-day correlation for stability
    rolling_corr = returns[ticker_a].rolling(60).corr(returns[ticker_b])

    # Spread (log price ratio) for mean-reversion
    spread = np.log(closes[ticker_a] / closes[ticker_b])
    spread_z = (spread - spread.mean()) / spread.std()

    return {
        "correlation": round(corr, 4),
        "beta": round(beta, 4),
        "r_squared": round(r_squared, 4),
        "rolling_corr_mean": round(rolling_corr.mean(), 4),
        "rolling_corr_std": round(rolling_corr.std(), 4),
        "rolling_corr_min": round(rolling_corr.min(), 4),
        "rolling_corr_max": round(rolling_corr.max(), 4),
        "spread_z_current": round(spread_z.iloc[-1], 4),
        "observations": len(returns),
    }
```

### B2: Present results

Show a summary card:

| Metric | Value |
|---|---|
| Pearson Correlation | 0.82 |
| Beta (B vs A) | 1.15 |
| R-squared | 0.67 |
| Rolling Corr (60d avg) | 0.80 |
| Rolling Corr Range | [0.55, 0.94] |
| Rolling Corr Std Dev | 0.08 |
| Spread Z-Score (current) | +1.2 |
| Observations | 250 |

Interpretation guide:
- **Correlation > 0.80**: Strong co-movement — these stocks are tightly linked
- **Correlation 0.50–0.80**: Moderate — shared sector drivers but independent factors too
- **Correlation < 0.50**: Weak — limited co-movement despite possible sector overlap
- **High rolling std**: Unstable relationship — correlation varies significantly over time
- **Spread Z > |2|**: Unusual divergence from historical relationship

---

## Sub-Skill C: Sector Clustering

**Goal**: Given a group of tickers, show the full correlation structure and identify clusters.

### C1: Build the correlation matrix

```python
import yfinance as yf
import pandas as pd
import numpy as np

def sector_clustering(tickers, period="1y"):
    data = yf.download(tickers, period=period, auto_adjust=True, progress=False)

    # yf.download returns MultiIndex (Price, Ticker) columns
    closes = data["Close"].dropna(axis=1, thresh=max(60, len(data) // 2))
    returns = np.log(closes / closes.shift(1)).dropna()
    corr_matrix = returns.corr()

    # Hierarchical clustering order
    from scipy.cluster.hierarchy import linkage, leaves_list
    from scipy.spatial.distance import squareform

    dist_matrix = 1 - corr_matrix.abs()
    np.fill_diagonal(dist_matrix.values, 0)
    condensed = squareform(dist_matrix)
    linkage_matrix = linkage(condensed, method="ward")
    order = leaves_list(linkage_matrix)
    ordered_tickers = [corr_matrix.columns[i] for i in order]

    # Reorder matrix
    clustered = corr_matrix.loc[ordered_tickers, ordered_tickers]

    return clustered, returns
```

Note: if `scipy` is not available, fall back to sorting by average correlation instead of hierarchical clustering.

### C2: Present results

1. **Full correlation matrix** — formatted as a table. For more than 8 tickers, show as a heatmap description or highlight only the strongest/weakest pairs.

2. **Identified clusters** — group tickers that have high intra-group correlation:
   - Cluster 1: [NVDA, AMD, AVGO] — avg intra-correlation 0.82
   - Cluster 2: [AAPL, MSFT] — avg intra-correlation 0.75

3. **Outliers** — tickers with low average correlation to the group (potential diversifiers).

4. **Strongest pairs** — top 5 highest-correlation pairs in the matrix.

5. **Weakest pairs** — top 5 lowest/negative-correlation pairs (hedging candidates).

---

## Sub-Skill D: Realized Correlation

**Goal**: Show how correlation changes over time and under different market conditions.

### D1: Rolling correlation

```python
import yfinance as yf
import pandas as pd
import numpy as np

def realized_correlation(ticker_a, ticker_b, period="2y", windows=[20, 60, 120]):
    data = yf.download([ticker_a, ticker_b], period=period, auto_adjust=True, progress=False)
    closes = data["Close"][[ticker_a, ticker_b]].dropna()

    returns = np.log(closes / closes.shift(1)).dropna()

    rolling = {}
    for w in windows:
        rolling[f"{w}d"] = returns[ticker_a].rolling(w).corr(returns[ticker_b])

    return rolling, returns
```

### D2: Regime-conditional correlation

```python
def regime_correlation(returns, ticker_a, ticker_b, condition_ticker=None):
    """Compare correlation across up/down/volatile regimes."""
    if condition_ticker is None:
        condition_ticker = ticker_a

    ret = returns[condition_ticker]

    regimes = {
        "All Days": pd.Series(True, index=returns.index),
        "Up Days (target > 0)": ret > 0,
        "Down Days (target < 0)": ret < 0,
        "High Vol (top 25%)": ret.abs() > ret.abs().quantile(0.75),
        "Low Vol (bottom 25%)": ret.abs() < ret.abs().quantile(0.25),
        "Large Drawdown (< -2%)": ret < -0.02,
    }

    results = {}
    for name, mask in regimes.items():
        subset = returns[mask]
        if len(subset) >= 20:
            results[name] = {
                "correlation": round(subset[ticker_a].corr(subset[ticker_b]), 4),
                "days": int(mask.sum()),
            }

    return results
```

### D3: Present results

1. **Rolling correlation summary table**:

| Window | Current | Mean | Min | Max | Std |
|---|---|---|---|---|---|
| 20-day | 0.88 | 0.76 | 0.32 | 0.95 | 0.12 |
| 60-day | 0.82 | 0.78 | 0.55 | 0.92 | 0.08 |
| 120-day | 0.80 | 0.79 | 0.68 | 0.88 | 0.05 |

2. **Regime correlation table**:

| Regime | Correlation | Days |
|---|---|---|
| All Days | 0.82 | 250 |
| Up Days | 0.75 | 132 |
| Down Days | 0.87 | 118 |
| High Vol (top 25%) | 0.90 | 63 |
| Large Drawdown (< -2%) | 0.93 | 28 |

3. **Key insight**: Highlight whether correlation **increases during sell-offs** (very common — "correlations go to 1 in a crisis"). This is critical for risk management.

4. **Trend**: Is correlation trending higher or lower recently vs. its historical average?

---

## Step 3: Respond to the User

After running the appropriate sub-skill, present results clearly:

### Always include

- The **lookback period** and **data interval** used
- The **number of observations** (trading days)
- Any tickers **dropped due to insufficient data**

### Always caveat

- **Correlation is not causation** — co-movement does not imply a causal link
- **Past correlation does not guarantee future correlation** — regimes shift
- **Short lookback windows** produce noisy estimates; longer windows smooth but may miss regime changes

### Practical applications (mention when relevant)

- **Sympathy plays**: Stocks likely to follow a peer's earnings/news move
- **Pair trading**: High-correlation pairs where the spread has diverged from its mean
- **Portfolio diversification**: Finding low-correlation assets to reduce risk
- **Hedging**: Identifying inversely correlated instruments
- **Sector rotation**: Understanding which sectors move together
- **Risk management**: Correlation spikes during stress — diversification may fail when needed most

**Important**: Never recommend specific trades. Present data and let the user draw conclusions.

---

## Reference Files

- `references/sector_universes.md` — Dynamic peer universe construction using yfinance Screener API

Read the reference file when you need to build a peer universe for a given ticker.
