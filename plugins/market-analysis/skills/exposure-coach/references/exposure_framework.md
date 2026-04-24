# Exposure Framework

## Overview

This document defines the scoring rules and threshold logic used by the Exposure Coach to synthesize multiple market signals into a unified exposure recommendation.

## Component Scoring (0-100 Scale)

Each input dimension is normalized to a 0-100 score where:
- **0-30**: Bearish / Risk-off signal
- **31-50**: Cautious / Neutral-bearish
- **51-70**: Neutral-bullish / Constructive
- **71-100**: Bullish / Risk-on signal

### Breadth Score

Derived from advance/decline ratios and new highs vs new lows:

| A/D Ratio (10-day) | NH/NL Ratio | Breadth Score |
|-------------------|-------------|---------------|
| > 1.5 | > 3.0 | 80-100 |
| 1.0 - 1.5 | 1.0 - 3.0 | 50-79 |
| 0.7 - 1.0 | 0.5 - 1.0 | 30-49 |
| < 0.7 | < 0.5 | 0-29 |

### Uptrend Score

Direct mapping from uptrend participation percentage:

| Uptrend % | Score |
|-----------|-------|
| > 50% | 75-100 |
| 35-50% | 50-74 |
| 20-35% | 30-49 |
| < 20% | 0-29 |

### Regime Score

Based on macro-regime-detector output:

| Regime | Score | Rationale |
|--------|-------|-----------|
| Broadening | 80 | Healthy expansion; rising tide lifts all boats |
| Concentration | 60 | Narrow leadership; selective opportunities |
| Transitional | 50 | Uncertainty; reduce commitment |
| Inflationary | 40 | Rotation stress; defensive posture |
| Contraction | 20 | Risk-off; preserve capital |

### Top Risk Score (Inverted)

Higher distribution day counts and top probability → lower score:

| Distribution Days | Top Probability | Score |
|-------------------|-----------------|-------|
| 0-2 | < 20% | 80-100 |
| 3-4 | 20-40% | 50-79 |
| 5-6 | 40-60% | 30-49 |
| 7+ | > 60% | 0-29 |

### FTD Score (Inverted)

High failure-to-deliver anomalies indicate stress:

| FTD Anomaly Level | Score |
|-------------------|-------|
| None / Low | 80-100 |
| Moderate | 50-79 |
| Elevated | 30-49 |
| Critical | 0-29 |

### Theme Score

Based on theme strength and rotation patterns:

| Theme Status | Score |
|--------------|-------|
| Strong, expanding | 80-100 |
| Stable | 50-79 |
| Rotating / Churning | 30-49 |
| Collapsing | 0-29 |

### Sector Score

Based on sector performance dispersion and leadership quality:

| Sector Condition | Score |
|------------------|-------|
| Broad strength, low dispersion | 80-100 |
| Mixed with clear leaders | 50-79 |
| High dispersion, defensive leading | 30-49 |
| Broad weakness | 0-29 |

### Institutional Score

Net institutional buying/selling trend:

| Flow Direction | Score |
|----------------|-------|
| Strong net buying | 80-100 |
| Mild net buying | 50-79 |
| Neutral / Mixed | 30-49 |
| Net selling | 0-29 |

## Composite Calculation

### Weighted Average

The composite score uses these weights:

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Regime | 25% | Sets the macro baseline |
| Top Risk | 20% | Critical for downside protection |
| Breadth | 15% | Market health indicator |
| Uptrend | 15% | Participation confirmation |
| Institutional | 10% | Smart money signal |
| Sector | 5% | Rotation context |
| Theme | 5% | Thematic momentum |
| FTD | 5% | Stress indicator |

### Missing Input Handling

When inputs are missing:
1. Exclude missing components from weighted average
2. Reduce confidence level proportionally
3. Apply a 10% haircut per missing critical input (Regime, Top Risk, Breadth)

## Exposure Ceiling Mapping

| Composite Score | Exposure Ceiling |
|-----------------|------------------|
| 80-100 | 90-100% |
| 65-79 | 70-89% |
| 50-64 | 50-69% |
| 35-49 | 30-49% |
| 20-34 | 10-29% |
| 0-19 | 0-9% |

## Recommendation Logic

### NEW_ENTRY_ALLOWED
- Composite score >= 50
- Top risk score >= 40
- No critical inputs missing

### REDUCE_ONLY
- Composite score 30-49, OR
- Top risk score 25-39, OR
- 2+ critical inputs missing

### CASH_PRIORITY
- Composite score < 30, OR
- Top risk score < 25, OR
- Regime = Contraction with top risk score < 50

## Bias Determination

### Growth Bias
- Regime = Broadening or Concentration
- Theme score > 60
- Sector shows technology/growth leadership

### Value Bias
- Regime = Inflationary
- Sector shows financials/energy/materials leadership
- Institutional flow favoring value sectors

### Neutral Bias
- Conflicting signals or transitional regime
- Balanced sector performance

## Participation Assessment

### Broad Participation
- Uptrend score >= 50
- Breadth score >= 50
- Low sector dispersion

### Narrow Participation
- Uptrend score < 50
- Breadth score < 50 OR high sector dispersion
- Few sectors carrying the market

## Confidence Levels

| Condition | Confidence |
|-----------|------------|
| 6+ inputs provided, no conflicts | HIGH |
| 4-5 inputs provided OR minor conflicts | MEDIUM |
| < 4 inputs OR major conflicts | LOW |
