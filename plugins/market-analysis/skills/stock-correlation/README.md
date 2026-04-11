# stock-correlation

Analyze stock correlations to find related companies, sector peers, and pair-trading candidates using historical price data.

## What it does

Routes to four specialized sub-skills based on user intent:

- **Co-movement Discovery** — given a single ticker, find the most correlated stocks from curated sector and thematic peer universes (e.g., "what correlates with NVDA?")
- **Return Correlation** — deep-dive pairwise analysis between two tickers: Pearson correlation, beta, R-squared, spread Z-score, and rolling stability (e.g., "correlation between AMD and NVDA")
- **Sector Clustering** — full NxN correlation matrix with hierarchical clustering to identify groups and outliers (e.g., "correlation matrix for FAANG")
- **Realized Correlation** — time-varying and regime-conditional correlation: rolling windows (20/60/120-day), up vs down days, high-vol vs low-vol, drawdown regimes (e.g., "when NVDA drops what else drops?")

## Triggers

- "what correlates with NVDA", "find stocks related to AMD"
- "correlation between AAPL and MSFT", "how do LITE and COHR move together"
- "what moves with", "stocks that move together", "sympathy plays"
- "sector peers", "pair trading", "hedging pair"
- "when NVDA drops what else drops", "rolling correlation"
- "correlation matrix for FAANG", "cluster these stocks"
- Well-known pairs: AMD/NVDA, GOOGL/AVGO, LITE/COHR

## Prerequisites

- Python 3.8+
- The skill auto-installs `yfinance`, `pandas`, and `numpy` via pip if not already present
- `scipy` is optional (used for hierarchical clustering in Sector Clustering sub-skill; falls back to sorting if unavailable)

## Platform

Works on **all platforms** (Claude Code, Claude.ai with code execution, etc.).

## Setup

```bash
# As a plugin (recommended — installs all skills)
npx plugins add himself65/finance-skills --plugin finance-market-analysis

# Or install just this skill
npx skills add himself65/finance-skills --skill stock-correlation
```

See the [main README](../../../../README.md) for more installation options.

## Reference files

- `references/sector_universes.md` — Dynamic peer universe construction using yfinance Screener API, with fallback strategies
