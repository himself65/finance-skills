# Exposure Coach

Synthesizes upstream market-risk signals into a one-page market posture: equity exposure ceiling, growth/value bias, participation breadth, and whether new entries are allowed.

## Triggers

- Portfolio exposure guidance
- "How much equity exposure should I have?"
- New-entry allowed versus reduce-only decisions
- Combining breadth, uptrend, top-risk, regime, theme, sector, and flow signals

## What It Does

1. Loads JSON outputs from upstream skills such as market-breadth-analyzer, uptrend-analyzer, market-top-detector, macro-regime-detector, theme-detector, sector-analyst, and institutional-flow-tracker
2. Extracts normalized component scores, including nested `composite.composite_score` outputs
3. Calculates a weighted exposure score, equity exposure ceiling, bias, participation status, recommendation, and confidence
4. Writes JSON and Markdown posture reports

## Platform

CLI-based agents. Requires Python 3.9+. It can run with partial inputs, but confidence improves as more upstream reports are provided.

## Setup

Run directly with available upstream reports:

```bash
python plugins/market-analysis/skills/exposure-coach/scripts/calculate_exposure.py \
  --breadth reports/market_breadth_latest.json \
  --uptrend reports/uptrend_analysis_latest.json \
  --top-risk reports/market_top_latest.json \
  --output-dir reports/
```

## Reference Files

| File | Contents |
|---|---|
| `references/exposure_framework.md` | Scoring rules and threshold definitions |
| `references/regime_exposure_map.md` | Regime-to-exposure mapping |

## Disclaimer

This skill is for educational and informational purposes only. It does not constitute financial advice.
