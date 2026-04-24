# Uptrend Analyzer Methodology

## Data Source: Monty's Uptrend Ratio Dashboard

Monty's Uptrend Ratio Dashboard tracks approximately 2,800 US stocks across 11 GICS sectors. For each stock, it determines whether the stock is in an "uptrend" based on the criteria below. The dashboard publishes daily CSV data on GitHub.

**GitHub Repository:** `tradermonty/uptrend-dashboard`
**Live Dashboard:** https://uptrend-dashboard.streamlit.app/

### Uptrend Definition (Finviz Elite Screener)

A stock is classified as "uptrend" when it meets **all** of the following conditions:

| Condition | Description |
|-----------|-------------|
| Price > $10 | Penny stocks excluded |
| Avg Volume > 100K | Sufficient liquidity |
| Market Cap > $50M | Micro-cap and above |
| Price > SMA20 | Short-term uptrend |
| Price > SMA200 | Long-term uptrend |
| SMA50 > SMA200 | Golden cross (bullish structure) |
| 52W High/Low > 30% above Low | Recovering from bottom |
| 4-Week Performance: Up | Recent momentum positive |

The **uptrend ratio** = (stocks meeting all conditions) / (stocks meeting base filters: price, volume, market cap).

### CSV Files

| File | Description | Update Frequency |
|------|-------------|------------------|
| `uptrend_ratio_timeseries.csv` | Daily ratios for "all" + 11 sectors | Daily |
| `sector_summary.csv` | Latest snapshot of all sectors | Daily |

**Data availability:**
- "all" (full market): Since 2023-08-11
- Sector-level data: Since 2024-07-21

### Timeseries Columns

| Column | Type | Description |
|--------|------|-------------|
| worksheet | string | "all" or sector slug (e.g., "sec_technology") |
| date | string | YYYY-MM-DD format |
| count | int | Number of stocks in uptrend |
| total | int | Total stocks tracked |
| ratio | float | count/total (0-1 scale, raw decimal) |
| ma_10 | float | 10-day simple moving average of ratio |
| slope | float | 1-day difference of ma_10 (`ma_10.diff()`) |
| trend | string | "up" (slope > 0) or "down" (slope <= 0) |

### Sector Summary Columns

| Column | Type | Description |
|--------|------|-------------|
| Sector | string | Display name (e.g., "Technology") |
| Ratio | float | Current uptrend ratio (0-1) |
| 10MA | float | 10-day MA of ratio |
| Trend | string | "Up" or "Down" |
| Slope | float | 1-day difference of MA |
| Status | string | "Overbought", "Oversold", or "Normal" |

### Indicator Calculations (from source code)

All indicators are computed on-the-fly from raw count/total data:

```
ratio    = count / total
ma_10    = ratio.rolling(10).mean()       # 10-day simple MA
slope    = ma_10.diff()                   # 1-day change of MA
trend    = "up" if slope > 0 else "down"
```

**Peak/Trough Detection:** The dashboard uses `scipy.signal.find_peaks` with parameters `distance=20, prominence=0.015` to identify local tops and bottoms in the 10MA series.

---

## Official Dashboard Thresholds

These thresholds are defined in `src/constants.py` of the source repository:

| Threshold | Value | Meaning |
|-----------|-------|---------|
| **Upper (Overbought)** | **37%** | Ratio above this = overbought conditions |
| **Lower (Oversold)** | **9.7%** | Ratio below this = oversold / crisis |
| MA Period | 10 | Simple moving average window |

### Status Determination

```
ratio > 0.37  -> "Overbought"
ratio < 0.097 -> "Oversold"
otherwise     -> "Normal"
```

### Practical Interpretation

| Ratio | Interpretation | Market Environment |
|-------|---------------|-------------------|
| 50%+ | Strong breadth | Broad bull market, most stocks participating |
| 37-50% | Overbought / Healthy | Above upper threshold, strong but extended |
| 25-37% | Normal / Recovering | Between thresholds, typical trading range |
| 9.7-25% | Weak | Below normal, breadth deteriorating |
| < 9.7% | Oversold / Crisis | Below lower threshold, extreme selling |

---

## 5-Component Scoring System

### Component 1: Market Breadth (Overall) - Weight: 30%

**Rationale:** The overall uptrend ratio is the single most important measure of market health. A high ratio means broad participation; a low ratio means a narrow, fragile market.

**Scoring Bands (aligned with dashboard thresholds):**

| Ratio | Score Range | Signal |
|-------|-------------|--------|
| >= 50% | 90-100 | Strong Bull |
| 37-50% | 70-89 | Bullish (above overbought threshold) |
| 25-37% | 40-69 | Neutral/Recovering |
| 9.7-25% | 10-39 | Weak (between thresholds) |
| < 9.7% | 0-9 | Crisis (below oversold threshold) |

**Trend Adjustment:** +5 when trend="up" and slope>0, -5 when trend="down" and slope<0.

### Component 2: Sector Participation - Weight: 25%

**Rationale:** A healthy market has most sectors participating. When only 2-3 sectors lead, the market is fragile and vulnerable to sector rotation shocks.

**Sub-scores:**
- **Uptrend Count (60%):** Number of sectors in uptrend mapped to 0-100
- **Spread (40%):** Max-min ratio spread. Narrow spread = uniform participation (good). Wide spread = selective market (risky).

**Overbought/Oversold classification uses dashboard thresholds:** >37% = Overbought, <9.7% = Oversold.

### Component 3: Sector Rotation - Weight: 15%

**Rationale:** In a healthy bull market, cyclical sectors (Technology, Consumer Cyclical) lead defensive sectors (Utilities, Consumer Defensive). When defensives lead, it signals risk-off behavior.

**Sector Classification:**

| Group | Sectors |
|-------|---------|
| Cyclical | Technology, Consumer Cyclical, Communication Services, Financial, Industrials |
| Defensive | Utilities, Consumer Defensive, Healthcare, Real Estate |
| Commodity | Energy, Basic Materials |

**Scoring:** Based on cyclical_avg - defensive_avg difference.
- Cyclical lead > +15pp = Strong risk-on (90-100)
- Balanced within +/-5pp = Neutral (45-69)
- Defensive lead > +15pp = Strong risk-off (0-19)

**Commodity Adjustment:** When commodity sectors outperform both cyclical and defensive groups, it may signal late-cycle dynamics. A penalty of -5 to -10 is applied.

**Intra-Group Divergence Detection:** The system detects significant dispersion within Cyclical and Defensive groups. A divergence flag triggers when any of:
- Group internal standard deviation > 8 percentage points
- Group internal max-min spread > 20 percentage points
- One or more sectors trend in the opposite direction from the group majority

When divergence is detected, a -5 penalty is applied to the Component 3 score. This prevents group averages from masking important internal disagreements (e.g., Financial declining while other Cyclicals rise).

> **Note (Dual-Layer Penalty):** Divergence triggers penalties at two levels:
> (1) -5 to the Component 3 score (making the rotation score more truthful), and
> (2) -3 to the composite score (triggering exposure guidance tightening, see Warning System below).
> Net composite impact ≈ 5 × 0.15 (weight) + 3 = **3.75 points**.

### Component 4: Momentum - Weight: 20%

**Rationale:** The direction and rate of change in breadth matters as much as the level. Improving breadth (positive slope, accelerating) suggests the environment is getting better; deteriorating breadth suggests caution.

**Sub-scores:**
- **Slope Score (50%):** Smoothed slope (EMA-3) mapped to 0-100 (typical range: -0.02 to +0.02). The raw 1-day slope (`ma_10.diff()`) is smoothed with a 3-period Exponential Moving Average to reduce daily noise.
- **Acceleration (30%):** Recent 10-point smoothed slope average vs prior 10-point average (10v10 window). Falls back to 5v5 when fewer than 20 data points are available.
- **Sector Slope Breadth (20%):** Count of sectors with positive slope

**Momentum Smoothing:** The raw slope signal from Monty's dashboard is inherently noisy because it is a 1-day difference of a 10-day moving average. The EMA(3) smoothing filter reduces single-day volatility while preserving directional trends. Both raw and smoothed slope values are reported for transparency.

### Component 5: Historical Context - Weight: 10%

**Rationale:** Knowing where the current ratio falls in historical distribution provides perspective. A ratio that seems "low" might be historically average, or vice versa.

**Scoring:** Percentile rank of current ratio in the full historical distribution (Aug 2023 to present).

**Note:** The "all" dataset starts from 2023-08-11 (~650+ data points), while sector data starts from 2024-07-21 (~370+ data points each).

**Confidence Assessment:** Because the historical dataset is limited (~650 data points), the system assesses and reports the confidence level of percentile analysis:

| Factor | Criteria | Score |
|--------|----------|-------|
| **Sample Size** | >=1000: full (3), 500-999: moderate (2), 200-499: limited (1), <200: minimal (0) | 0-3 |
| **Regime Coverage** | Has bear data (min<10%) AND bull data (max>40%): Both (2), one: Partial (1), neither: Narrow (0) | 0-2 |
| **Recency Bias** | Recent 90 days cover >=30% of full range: balanced (1), otherwise: biased (0) | 0-1 |

Total score 5-6 = High, 3-4 = Moderate, 1-2 = Low, 0 = Very Low confidence.

When confidence is Low or Very Low, the signal text includes a `[confidence: Low]` caveat.

---

## Scoring Zones and Exposure Guidance

### 5-Level Zones (backward-compatible)

| Score | Zone | Exposure | Description |
|-------|------|----------|-------------|
| 80-100 | Strong Bull | Full (100%) | Broad participation, strong momentum. Ideal for aggressive positioning. |
| 60-79 | Bull | Normal (80-100%) | Healthy breadth. Standard position management. |
| 40-59 | Neutral | Reduced (60-80%) | Mixed signals. Participate selectively. |
| 20-39 | Cautious | Defensive (30-60%) | Weak breadth. Prioritize capital preservation. |
| 0-19 | Bear | Preservation (0-30%) | Severe deterioration. Maximum defense. |

### 7-Level Zone Detail

The `zone_detail` field provides finer granularity, splitting the Bull and Cautious zones:

| Score | Zone (5-level) | Zone Detail (7-level) | Exposure Range |
|-------|----------------|----------------------|----------------|
| 80-100 | Strong Bull | Strong Bull | 100% |
| 70-79 | Bull | Bull-Upper | 90-100% |
| 60-69 | Bull | Bull-Lower | 80-90% |
| 40-59 | Neutral | Neutral | 60-80% |
| 30-39 | Cautious | Cautious-Upper | 45-60% |
| 20-29 | Cautious | Cautious-Lower | 30-45% |
| 0-19 | Bear | Bear | 0-30% |

**Why:** The original Bull zone (60-79) was too wide. A score of 66 and 78 both showed "Bull" but warrant different exposure levels. Bull-Lower signals caution compared to Bull-Upper.

### Zone Proximity Indicator

When the composite score falls within 10 points of a zone boundary (20, 40, 60, 80), the `zone_proximity` field flags `at_boundary=True` with the distance and direction. This alerts users that a small score change could shift the zone classification.

---

## Warning System

### Component-Level Warnings

Warnings detect conditions where the composite score may overstate market health:

| Warning | Trigger | Composite Penalty | Rationale |
|---------|---------|-------------------|-----------|
| **Late Cycle** | Commodity avg > both Cyclical and Defensive group averages | -5 | Commodity leadership often precedes broader market weakness |
| **High Spread** | Max-min sector ratio spread > 40pp | -3 | Wide spread indicates narrowing leadership masked by averages |
| **Divergence** | Intra-group std > 8pp, spread > 20pp, or trend dissenters | -3 | Group averages hide internal disagreement (also -5 to Component 3 score) |

### Multi-Warning Discount

When 2 or more warnings are active simultaneously, the total penalty is reduced by 1 point to account for correlation between warning conditions.

**Example:** Late Cycle (-5) + High Spread (-3) = -8 + discount (+1) = **-7 total penalty**

### Warning Impact on Guidance

When warnings are active in Bull or Strong Bull zones:
- Exposure guidance is tightened (e.g., "Normal Exposure, Lower End (80-90%)" instead of "Normal Exposure (80-100%)")
- Guidance text notes the tension between score and warnings
- Warning-specific actions are prepended to recommended actions

The raw score (before penalty) is preserved as `composite_score_raw` for transparency.

---

## Weight Rationale

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Market Breadth | 30% | Most direct measure of market health |
| Sector Participation | 25% | Breadth of sector-level participation is critical for sustainability |
| Momentum | 20% | Direction matters as much as level |
| Sector Rotation | 15% | Rotation signals provide important risk-on/off context |
| Historical Context | 10% | Provides perspective but less actionable than real-time signals |

---

## Limitations

1. **Data History:** "all" data starts from Aug 2023; sector data from Jul 2024. Long-term percentile analysis is limited. The confidence indicator helps quantify this limitation.
2. **Single Source:** Relies entirely on Monty's dashboard (Finviz Elite data); no cross-validation with other breadth measures.
3. **No Volume Data:** Uptrend ratio is price-based only; no volume confirmation.
4. **Lagging Indicator:** 10-day moving average and slope introduce inherent lag. EMA(3) smoothing adds marginal additional lag but reduces noise.
5. **US Only:** Covers US stocks only; no international market breadth.
6. **Sector Classification:** Uses fixed GICS sectors which may not capture all rotation dynamics.
7. **Finviz Dependency:** Upstream data depends on Finviz Elite availability and screener accuracy.

---

## Complementary Analysis

This skill works best when combined with:
- **Market Top Detector:** For distribution day and leadership deterioration signals
- **Technical Analyst:** For index-level chart confirmation
- **Sector Analyst:** For detailed sector rotation analysis
- **Market News Analyst:** For fundamental catalyst context
