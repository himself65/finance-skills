# Stock Liquidity Analysis

Analyze stock liquidity across multiple dimensions using Yahoo Finance data — bid-ask spreads, volume profiles, order book depth estimates, market impact modeling, and turnover ratios.

## Triggers

- "how liquid is AAPL"
- "bid-ask spread for TSLA"
- "volume analysis for MSFT"
- "order book depth"
- "how much would 50k shares move the price"
- "market impact of a $1M order"
- "turnover ratio for GME"
- "slippage estimate"
- "compare liquidity between stocks"
- "is this stock liquid enough to trade"
- "Amihud illiquidity ratio"
- "average daily dollar volume"

## Platform

All platforms (CLI + Claude.ai with code execution enabled)

## Prerequisites

- Python 3.8+
- `yfinance`, `pandas`, `numpy` (auto-installed if missing)

## Sub-Skills

| Sub-Skill | Description |
|---|---|
| **Liquidity Dashboard** | Comprehensive snapshot combining all key metrics |
| **Spread Analysis** | Bid-ask spread breakdown with options context |
| **Volume Analysis** | ADV, dollar volume, RVOL, volume trends and patterns |
| **Order Book Depth** | Top-of-book data with intraday volume distribution proxy |
| **Market Impact** | Square-root model for estimating execution cost of large orders |
| **Turnover Ratio** | Trading activity relative to shares outstanding and free float |

## Reference Files

- `references/liquidity_reference.md` — Detailed formulas, code templates, metric interpretation guides, edge cases, and yfinance field reference
