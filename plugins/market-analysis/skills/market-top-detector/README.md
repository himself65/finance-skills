# Market Top Detector

Detects tactical market-top risk over a 2-8 week horizon by combining O'Neil distribution days, leading-stock deterioration, defensive rotation, breadth divergence, index technicals, and sentiment.

## Triggers

- Market top risk
- Distribution days
- Leading stock deterioration
- Defensive sector rotation
- Whether to reduce equity exposure
- Correction probability over the next 2-8 weeks

## What It Does

1. Fetches index, VIX, ETF, and historical data using Financial Modeling Prep where available
2. Pulls 200DMA breadth automatically from TraderMonty's public CSV
3. Accepts manually collected 50DMA breadth, put/call, VIX term structure, and margin debt inputs
4. Scores six tactical top-risk components and produces JSON/Markdown reports
5. Includes follow-through-day monitoring, historical comparison, and what-if scenarios

## Platform

CLI-based agents. Requires Python 3.8+, `requests`, network access, and an FMP API key for the full analysis.

## Setup

Set an FMP API key:

```bash
export FMP_API_KEY=your_key_here
```

Run directly:

```bash
python plugins/market-analysis/skills/market-top-detector/scripts/market_top_detector.py \
  --breadth-50dma 55.0 \
  --breadth-50dma-date 2026-04-23 \
  --put-call 0.63 \
  --put-call-date 2026-04-22 \
  --output-dir reports/
```

## Reference Files

| File | Contents |
|---|---|
| `references/market_top_methodology.md` | Full top-risk scoring methodology |
| `references/distribution_day_guide.md` | O'Neil distribution and stalling day rules |
| `references/historical_tops.md` | Historical top pattern comparisons |

## Disclaimer

This skill is for educational and informational purposes only. It does not constitute financial advice.
