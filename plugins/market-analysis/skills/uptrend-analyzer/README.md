# Uptrend Analyzer

Diagnoses market participation using Monty's Uptrend Ratio Dashboard, covering roughly 2,800 US stocks across 11 sectors. The skill generates a 0-100 composite score where higher means healthier uptrend participation.

## Triggers

- Uptrend ratio analysis
- Market participation breadth
- Sector uptrend health
- "Does the market support equity exposure?"
- Broad versus narrow rally assessment

## What It Does

1. Downloads Monty's uptrend ratio time series and sector summary CSV files
2. Scores five dimensions: market breadth, sector participation, sector rotation, momentum, and historical context
3. Applies warning penalties for late-cycle, high-spread, and sector divergence signals
4. Produces JSON and Markdown reports with exposure guidance and sector detail

## Platform

CLI-based agents. Requires Python 3.8+ and network access. No API key required.

## Setup

Install Python dependencies if needed:

```bash
pip install requests
```

Run directly:

```bash
python plugins/market-analysis/skills/uptrend-analyzer/scripts/uptrend_analyzer.py --output-dir reports/
```

## Reference Files

| File | Contents |
|---|---|
| `references/uptrend_methodology.md` | Uptrend ratio definitions, component scoring, sector groups, and calibration notes |

## Disclaimer

This skill is for educational and informational purposes only. It does not constitute financial advice.
