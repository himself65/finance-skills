# Regime-to-Exposure Mapping

## Overview

This document maps macro regime states to baseline exposure ceilings and bias recommendations. The macro regime provides the foundational context; other signals adjust within these bounds.

## Regime Definitions

### Broadening
**Characteristics:**
- RSP/SPY ratio rising (equal-weight outperforming cap-weight)
- Uptrend participation > 40%
- Multiple sectors contributing to gains
- Credit spreads stable or tightening

**Baseline Exposure:** 80-100%
**Bias:** Growth-tilted
**Action:** Aggressive new entries allowed

### Concentration
**Characteristics:**
- RSP/SPY ratio falling (mega-caps dominating)
- Uptrend participation 25-40%
- Leadership in few sectors (Technology, Communications)
- Narrow breadth despite index gains

**Baseline Exposure:** 60-80%
**Bias:** Quality Growth
**Action:** Selective entries in leaders only

### Transitional
**Characteristics:**
- Cross-asset signals conflicting
- Regime indicators at boundary conditions
- High volatility in breadth measures
- Sector rotation accelerating

**Baseline Exposure:** 40-60%
**Bias:** Neutral / Defensive
**Action:** Reduce new entries; hold quality positions

### Inflationary
**Characteristics:**
- Yield curve steepening
- Commodity strength (especially energy, metals)
- Value outperforming growth
- Real assets leading

**Baseline Exposure:** 50-70%
**Bias:** Value / Real Assets
**Action:** Rotate to inflation beneficiaries

### Contraction
**Characteristics:**
- Distribution days accumulating
- Uptrend participation < 20%
- Defensive sectors (Utilities, Staples, Healthcare) leading
- Credit spreads widening
- Institutional selling detected

**Baseline Exposure:** 10-30%
**Bias:** Defensive / Cash
**Action:** CASH_PRIORITY; protect capital

## Regime Transition Signals

### Broadening → Concentration
- RSP/SPY rolling over while SPY makes new highs
- Breadth divergence (fewer stocks at highs)
- Reduce exposure ceiling by 10-20%

### Concentration → Transitional
- Mega-cap leaders showing distribution
- Volatility expansion
- Reduce exposure ceiling by 15-25%

### Transitional → Contraction
- Credit spreads widening
- Safe haven flows (bonds, gold, yen)
- Reduce exposure ceiling by 25-40%

### Contraction → Transitional
- Distribution day count resetting
- Breadth thrusts
- Begin rebuilding exposure cautiously

### Transitional → Broadening
- RSP/SPY ratio turning up
- Uptrend participation expanding
- Aggressive exposure increase warranted

## Exposure Adjustment Rules

### Within-Regime Adjustments

Even within a regime, the exposure ceiling adjusts based on:

1. **Breadth Confirmation**
   - Breadth score aligning with regime: No adjustment
   - Breadth diverging negatively: -10% to ceiling
   - Breadth diverging positively: +5% to ceiling

2. **Top Risk Level**
   - Low top risk: +10% to ceiling
   - Elevated top risk: -15% to ceiling
   - Critical top risk: Force CASH_PRIORITY regardless of regime

3. **Institutional Flow**
   - Strong buying: +5% to ceiling
   - Strong selling: -10% to ceiling

4. **FTD Anomalies**
   - Critical FTD level: -15% to ceiling
   - Forces extra caution on new entries

## Bias-to-Sector Mapping

| Bias | Favored Sectors | Avoid Sectors |
|------|-----------------|---------------|
| Growth | Technology, Consumer Discretionary, Communications | Utilities, Staples |
| Value | Financials, Energy, Industrials, Materials | High-multiple Growth |
| Defensive | Utilities, Healthcare, Staples | Cyclicals |
| Quality | Stable Earnings, Strong Balance Sheets | Speculative, High Debt |

## Example Scenarios

### Scenario 1: Early Bull Market
- Regime: Broadening
- Breadth: Strong (score 85)
- Top Risk: Low (score 90)
- Uptrend: Expanding (score 80)

**Result:**
- Exposure Ceiling: 95%
- Bias: Growth
- Recommendation: NEW_ENTRY_ALLOWED

### Scenario 2: Late Cycle Concentration
- Regime: Concentration
- Breadth: Weak (score 45)
- Top Risk: Moderate (score 55)
- Uptrend: Narrow (score 35)

**Result:**
- Exposure Ceiling: 55%
- Bias: Quality Growth
- Recommendation: REDUCE_ONLY

### Scenario 3: Market Top Formation
- Regime: Transitional
- Breadth: Deteriorating (score 30)
- Top Risk: High (score 25)
- Uptrend: Collapsing (score 18)

**Result:**
- Exposure Ceiling: 15%
- Bias: Defensive
- Recommendation: CASH_PRIORITY

## Integration with Other Signals

The regime provides the framework; other signals fine-tune:

1. **Theme Detector** -- Identifies which themes to favor within bias
2. **Sector Analyst** -- Confirms sector leadership alignment
3. **Institutional Flow** -- Validates smart money direction
4. **FTD Detector** -- Flags systemic stress

When signals conflict:
- Default to more conservative posture
- Reduce confidence level
- Flag conflicts in rationale
