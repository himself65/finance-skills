# Market Breadth Analyzer

Quantifies S&P 500 market breadth health using TraderMonty's public breadth CSV data. The skill generates a 0-100 composite score where higher means healthier participation.

## Triggers

- Market breadth or participation analysis
- "Is the rally broad-based?"
- Advance/decline health
- Breadth divergence versus the S&P 500
- Equity exposure guidance based on breadth

## What It Does

1. Downloads TraderMonty's market breadth detail and summary CSV files
2. Scores six dimensions: breadth level/trend, 8MA versus 200MA, peak/trough cycle, bearish signal status, historical percentile, and S&P 500 divergence
3. Produces JSON and Markdown reports with exposure guidance and watch levels
4. Tracks score history across runs

## Platform

CLI-based agents. Requires Python 3.8+ and network access. No API key required.

## Setup

Install Python dependencies if needed:

```bash
pip install requests
```

Run directly:

```bash
python plugins/market-analysis/skills/market-breadth-analyzer/scripts/market_breadth_analyzer.py --output-dir reports/
```

## Reference Files

| File | Contents |
|---|---|
| `references/breadth_analysis_methodology.md` | Full component scoring methodology, thresholds, and interpretation |

## Disclaimer

This skill is for educational and informational purposes only. It does not constitute financial advice.
