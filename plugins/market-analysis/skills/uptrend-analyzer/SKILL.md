---
name: uptrend-analyzer
description: Analyzes market breadth using Monty's Uptrend Ratio Dashboard data to diagnose the current market environment. Generates a 0-100 composite score from 5 components (breadth, sector participation, rotation, momentum, historical context). Use when asking about market breadth, uptrend ratios, or whether the market environment supports equity exposure. No API key required.
---

# Uptrend Analyzer Skill

## Purpose

Diagnose market breadth health using Monty's Uptrend Ratio Dashboard, which tracks ~2,800 US stocks across 11 sectors. Generates a 0-100 composite score (higher = healthier) with exposure guidance.

Unlike the Market Top Detector (API-based risk scorer), this skill uses free CSV data to assess "participation breadth" - whether the market's advance is broad or narrow.

## When to Use This Skill

**English:**
- User asks "Is the market breadth healthy?" or "How broad is the rally?"
- User wants to assess uptrend ratios across sectors
- User asks about market participation or breadth conditions
- User needs exposure guidance based on breadth analysis
- User references Monty's Uptrend Dashboard or uptrend ratios

**Japanese:**
- 「市場のブレドスは健全？」「上昇の裾野は広い？」
- セクター別のアップトレンド比率を確認したい
- 相場参加率・ブレドス状況を診断したい
- ブレドス分析に基づくエクスポージャーガイダンスが欲しい
- Montyのアップトレンドダッシュボードについて質問

## Difference from Market Top Detector

| Aspect | Uptrend Analyzer | Market Top Detector |
|--------|-----------------|-------------------|
| Score Direction | Higher = healthier | Higher = riskier |
| Data Source | Free GitHub CSV | FMP API (paid) |
| Focus | Breadth participation | Top formation risk |
| API Key | Not required | Required (FMP) |
| Methodology | Monty Uptrend Ratios | O'Neil/Minervini/Monty |

---

## Execution Workflow

### Phase 1: Execute Python Script

Run the analysis script (no API key needed):

```bash
python3 skills/uptrend-analyzer/scripts/uptrend_analyzer.py
```

The script will:
1. Download CSV data from Monty's GitHub repository
2. Calculate 5 component scores
3. Generate composite score and reports

### Phase 2: Present Results

Present the generated Markdown report to the user, highlighting:
- Composite score and zone classification
- Exposure guidance (Full/Normal/Reduced/Defensive/Preservation)
- Sector heatmap showing strongest and weakest sectors
- Key momentum and rotation signals

---

## 5-Component Scoring System

| # | Component | Weight | Key Signal |
|---|-----------|--------|------------|
| 1 | Market Breadth (Overall) | **30%** | Ratio level + trend direction |
| 2 | Sector Participation | **25%** | Uptrend sector count + ratio spread |
| 3 | Sector Rotation | **15%** | Cyclical vs Defensive balance |
| 4 | Momentum | **20%** | Slope direction + acceleration |
| 5 | Historical Context | **10%** | Percentile rank in history |

## Scoring Zones

| Score | Zone | Exposure Guidance |
|-------|------|-------------------|
| 80-100 | Strong Bull | Full Exposure (100%) |
| 60-79 | Bull | Normal Exposure (80-100%) |
| 40-59 | Neutral | Reduced Exposure (60-80%) |
| 20-39 | Cautious | Defensive (30-60%) |
| 0-19 | Bear | Capital Preservation (0-30%) |

### 7-Level Zone Detail

Each scoring zone is further divided into sub-zones for finer-grained assessment:

| Score | Zone Detail | Color |
|-------|-------------|-------|
| 80-100 | Strong Bull | Green |
| 70-79 | Bull-Upper | Light Green |
| 60-69 | Bull-Lower | Light Green |
| 40-59 | Neutral | Yellow |
| 30-39 | Cautious-Upper | Orange |
| 20-29 | Cautious-Lower | Orange |
| 0-19 | Bear | Red |

### Warning System

Active warnings trigger exposure penalties that tighten guidance even when the composite score is high:

| Warning | Condition | Penalty |
|---------|-----------|---------|
| **Late Cycle** | Commodity avg > both Cyclical and Defensive | -5 |
| **High Spread** | Max-min sector ratio spread > 40pp | -3 |
| **Divergence** | Intra-group std > 8pp, spread > 20pp, or trend dissenters | -3 |

Penalties stack (max -10) + multi-warning discount (+1 when ≥2 active). Applied after composite scoring.

### Momentum Smoothing

Slope values are smoothed using EMA(3) (Exponential Moving Average, span=3) before scoring. Acceleration is calculated by comparing the recent 10-point average vs prior 10-point average of smoothed slopes (10v10 window), with fallback to 5v5 when fewer than 20 data points are available.

### Historical Confidence Indicator

The Historical Context component includes a confidence assessment based on:
- **Sample size:** Number of historical data points available
- **Regime coverage:** Proportion of distinct market regimes (bull/bear/neutral) observed
- **Recency:** How recent the latest data point is

Confidence levels: High, Medium, Low.

---

## API Requirements

**Required:** None (uses free GitHub CSV data)

## Output Files

- JSON: `uptrend_analysis_YYYY-MM-DD_HHMMSS.json`
- Markdown: `uptrend_analysis_YYYY-MM-DD_HHMMSS.md`

## Reference Documents

### `references/uptrend_methodology.md`
- Uptrend Ratio definition and thresholds
- 5-component scoring methodology
- Sector classification (Cyclical/Defensive/Commodity)
- Historical calibration notes

### When to Load References
- **First use:** Load `uptrend_methodology.md` for full framework understanding
- **Regular execution:** References not needed - script handles scoring
