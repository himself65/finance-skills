---
name: sepa-strategy
description: >
  Analyze stocks using Mark Minervini's SEPA (Specific Entry Point Analysis) methodology.
  Use this skill whenever the user mentions SEPA, Minervini, superperformance, trend template,
  VCP (Volatility Contraction Pattern), Stage 2 uptrend, stage analysis, pivot point breakout,
  or asks about growth stock screening criteria. Also triggers when the user wants to evaluate
  whether a stock meets swing trading entry criteria, check moving average alignment (bullish
  stacking: price > 50MA > 150MA > 200MA), assess breakout quality with volume confirmation,
  calculate position sizing based on risk percentage, or identify consolidation patterns like
  cup-with-handle, flat base, bull flag, or high tight flag. Use this skill even when the user
  simply asks "should I buy this stock" or "is this a good setup" in the context of growth/momentum
  trading, or when they share a stock chart and want pattern analysis.
---

# SEPA Strategy Analysis

Analyze stocks using Mark Minervini's SEPA (Specific Entry Point Analysis) framework — a complete system for identifying high-probability growth stock entries with strict risk management.

**Core philosophy:** Buy the right stock, in the right stage, at a precise entry point, with strict risk controls. Win rate is ~50-55% — profitability comes from asymmetric risk/reward (small losses, large gains), not from predicting direction.

> This skill is for educational/analytical purposes only. It does not constitute investment advice. Never execute trades based solely on this analysis.

---

## Step 1: Gather Stock Data

Collect the following data for the stock. Use yfinance, funda-data, or any available market data tool.

| Data needed | Purpose |
|---|---|
| Current price | Trend template check |
| 50-day, 150-day, 200-day moving averages | MA alignment verification |
| 52-week high and low | Price position check |
| 200MA value from 1 month ago and 4-5 months ago | MA200 slope direction |
| 20-day average volume + today's volume | Volume ratio analysis |
| Recent quarterly EPS (last 3-4 quarters) | EPS growth & acceleration |
| Annual EPS (last 3 years) | Long-term growth trend |
| Recent quarterly revenue (last 3-4 quarters) | Revenue growth check |
| Gross margin and net margin trend | Margin health |
| Institutional ownership changes (if available) | Smart money signal |
| RS rating or 12-month relative performance vs S&P 500 | Relative strength |
| Price history for pattern recognition | VCP / chart pattern analysis |

If certain data is unavailable, note it and proceed with what you have. Missing RS rating is a significant gap — flag it.

---

## Step 2: Stage Analysis — Identify the Current Stage

Every stock cycles through four stages. Read `references/stage-analysis.md` for full details.

Determine which stage the stock is in:

| Stage | Characteristics | Action |
|---|---|---|
| **Stage 1** — Basing | Price near 200MA, MA flat/declining, MAs tangled, low volume | Do nothing, wait |
| **Stage 2** — Advancing | Making higher highs/lows, bullish MA alignment, volume on up days | **Only stage to buy** |
| **Stage 3** — Topping | Wide swings at highs, frequent false breakouts, heavy volume without progress | Reduce, no new positions |
| **Stage 4** — Declining | Below all MAs, bearish alignment, bounces are selling opportunities | Full cash, stay away |

If the stock is NOT in Stage 2, stop here and tell the user. No further analysis needed.

Within Stage 2, count the base number (how many consolidation-then-breakout cycles have occurred):
- **Base 1-2**: Safest, most upside potential — full position
- **Base 3-4**: Still valid but reduce position size
- **Base 5-6**: Late stage — half position at most
- **Base 7+**: Avoid — likely transitioning to Stage 3

---

## Step 3: Trend Template — 8 Mandatory Conditions

All 8 conditions must be met simultaneously. If any fails, the stock does not qualify. Read `references/trend-template.md` for detailed explanations.

Present results as a checklist:

| # | Condition | Status | Value |
|---|---|---|---|
| 1 | Price > 150MA and Price > 200MA | Pass/Fail | [actual values] |
| 2 | 150MA > 200MA | Pass/Fail | [actual values] |
| 3 | 200MA trending up for ≥1 month (ideally 4-5 months) | Pass/Fail | [slope data] |
| 4 | 50MA > 150MA and 50MA > 200MA | Pass/Fail | [actual values] |
| 5 | Price > 50MA | Pass/Fail | [actual values] |
| 6 | Price ≥ 30% above 52-week low | Pass/Fail | [% above low] |
| 7 | Price within 25% of 52-week high | Pass/Fail | [% from high] |
| 8 | Relative Strength > 70th percentile (prefer 85-90+) | Pass/Fail/Unknown | [RS if available] |

**Memory aid:** Conditions 1-5 = "MA staircase" (Price > 50MA > 150MA > 200MA, 200MA rising). Conditions 6-7 = "Price position" (far from low, near high). Condition 8 = "Relative strength" (market leader).

---

## Step 4: Fundamental Check

Strong fundamentals separate real leaders from momentum-only stocks. Read `references/fundamentals.md` for thresholds and rating criteria.

Check these in order of importance:

1. **Quarterly EPS growth ≥ 20%** (prefer 25-50%+). Below 20% = disqualify.
2. **EPS acceleration**: Current quarter growth > prior quarter growth. Deceleration (even with positive growth) is a warning.
3. **Annual EPS growth ≥ 25%** for each of the past 3 years.
4. **Revenue growth ≥ 15%** annually, ≥ 20-25% quarterly preferred. If EPS grows but revenue doesn't, the growth is likely from cost-cutting (unsustainable).
5. **Margin trend**: Gross and net margins stable or expanding = healthy. Contracting margins even with EPS growth = red flag.
6. **Institutional ownership increasing**: Smart money accumulating = fuel for Stage 2 move.
7. **Catalyst**: New product, FDA approval, major contract, market expansion, etc. Stocks with catalysts can run 50-100%+; without, typically 15-25%.

Rate fundamentals: **A** (EPS >30%, positive, revenue growing) / **B** (15-30%) / **C** (0-15%) / **D** (negative — skip).

---

## Step 5: Pattern Recognition

Identify which consolidation pattern is forming (if any). Read `references/patterns.md` for detailed identification rules for each pattern.

### VCP (Volatility Contraction Pattern) — The Core Pattern

The signature SEPA pattern. Look for these 7 characteristics:

1. Stock must be in Stage 2 uptrend (prerequisite)
2. **Pullback depths decrease** in sequence (e.g., 20% → 12% → 6% → 3%). Minimum 3 contractions, 4-5 ideal.
3. **Volume shrinks** with each contraction. Final contraction shows "Volume Dry-Up" (VDU) — multi-week low volume.
4. **Higher lows** — each pullback bottom is higher than the previous one.
5. **Clear pivot point** — the consolidation range high = resistance level to break.
6. RS > 70 (preferably 85-90+)
7. Market in bull or neutral environment

### Other Valid Patterns

| Pattern | Depth | Duration | Key Feature |
|---|---|---|---|
| Cup with Handle | Cup 12-35%, handle ≤12% | 7-65 weeks | U-shaped base + small handle |
| Flat Base | ≤ 15% | 5-10 weeks | Tight range near prior highs |
| Bull Flag | ≤ 50% of flagpole | 1-5 weeks | Sharp advance + tight drift down |
| High Tight Flag | ≤ 25% after 100%+ advance | 1-4 weeks | Rarest but most powerful |

**All patterns share the same entry rule**: breakout above the pivot point with volume ≥ 1.5x the 20-day average.

---

## Step 6: Entry Point Analysis

Read `references/entry-rules.md` for detailed entry mechanics, true vs false breakout identification, and the pocket pivot alternative.

### Primary Entry: Pivot Point Breakout

- **Pivot point** = the highest price in the consolidation range. This is the supply/demand inflection point.
- **Buy zone** = pivot price to +5% above pivot. This is the only valid entry window.
- **Beyond +5%**: Do NOT chase. Wait for the next setup.
- **Breakout volume**: Must be ≥ 1.5x the 20-day average volume (≥ 2x is strong confirmation).
- **Earnings proximity**: Avoid entering within 2 weeks of an earnings report.

### Breakout Quality Check

| Signal | True Breakout | False Breakout |
|---|---|---|
| Volume | ≥ 1.5x average, big spike | Below average, weak |
| Close | Near the day's high | Falls back below pivot |
| Follow-through | Continues higher next day | Drops back into range |
| Context | VDU preceded breakout | No volume dry-up before |

### Risk/Reward Validation

Before entering, verify:
- **Stop loss distance**: Entry price to stop ≤ 7-8%
- **Reward/risk ratio**: Target profit / stop distance ≥ 2:1 (prefer 3:1)
- If ratio < 2:1, the entry is too risky — skip it.

---

## Step 7: Position Sizing & Stop Loss Plan

Read `references/position-sizing.md` for the full formula, examples, stop loss evolution, and pyramiding rules.

### Position Size Formula

```
Shares = (Account Value × Risk Per Trade %) ÷ (Entry Price − Stop Price)
```

**Example**: $100,000 account, 1% risk, buy at $50, stop at $46.50:
- Max loss = $100,000 × 1% = $1,000
- Stop distance = $50 − $46.50 = $3.50
- Shares = $1,000 ÷ $3.50 = **285 shares** ($14,250 = 14.25% of account)

### Stop Loss Evolution (3 phases)

| Phase | Trigger | Action |
|---|---|---|
| Phase 1: Initial | At entry | Hard stop at entry price −7-8%. Non-negotiable. |
| Phase 2: Breakeven | Stock reaches +8% | Sell half, move stop to entry price (breakeven). Trade can no longer lose money. |
| Phase 3: Trailing | Stock reaches +15% | Sell another 25%, trail remaining stop along 20MA. Close below 20MA = exit all. |

**Iron rules**: Stop losses only move UP, never down. Never average down on a losing position. After 3-4 consecutive losses, reduce risk per trade to 0.5%.

### Pyramiding (Adding to Winners)

Only add to winning positions, with decreasing size: 50% initial → 30% at +8% → 20% at next base breakout. Never add to losers.

---

## Step 8: Market Environment Check

Read `references/market-environment.md` for detailed criteria.

The market environment is the master switch for position sizing:

| Environment | Criteria | Risk Per Trade | Max Positions |
|---|---|---|---|
| **Bull** | S&P 500/Nasdaq above 200MA, breadth expanding, new highs > new lows | 1-2% | 6-8 |
| **Choppy** | Sideways indices, frequent failed breakouts | 0.5-1% | 2-3 |
| **Bear** | Indices below 200MA, >50% of stocks below 200MA | 0% (no new positions) | 0 (all cash) |

Even the best setups fail in bear markets. Holding cash during bear markets IS a winning strategy — preserving capital for the next bull run.

---

## Step 9: Respond to the User

Present a structured analysis report with these sections:

### Report Structure

1. **Stock & Stage**: Ticker, current price, identified stage, base count if Stage 2
2. **Trend Template Scorecard**: 8-condition checklist with pass/fail and actual values
3. **Fundamental Grade**: A/B/C/D with EPS growth, acceleration status, revenue, margins
4. **Pattern Identified**: Which pattern (VCP, cup-handle, flat base, flag, HTF, or none), with key measurements (contraction depths, volume behavior)
5. **Entry Assessment**:
   - If a valid pattern exists: pivot price, buy zone, breakout volume requirement
   - If not yet formed: what to watch for
   - If already extended: "This has moved beyond the buy zone — wait for the next consolidation"
6. **Position Sizing**: Using the formula, show exact shares, stop price, first target, second target, and reward/risk ratio. Ask the user for their account size and risk tolerance if not provided.
7. **Market Environment**: Current assessment and how it affects sizing
8. **Overall Verdict**: One of:
   - **Strong Buy Setup** — all criteria met, actionable now
   - **Watch List** — promising but pattern not yet complete or one condition marginal
   - **Pass** — fails trend template, wrong stage, or poor fundamentals

Always end with the disclaimer that this is educational analysis, not investment advice.

---

## Reference Files

- `references/stage-analysis.md` — Four-stage theory, transition signals, base counting
- `references/trend-template.md` — Detailed 8-condition explanations and memory aids
- `references/fundamentals.md` — EPS, revenue, margins, institutional holdings, catalysts
- `references/patterns.md` — VCP 7 rules, cup-with-handle, flat base, flag, high tight flag, quality vs fake signals
- `references/entry-rules.md` — Pivot point mechanics, buy zone, pocket pivot, true vs false breakout identification
- `references/position-sizing.md` — Formula, stop loss 3-phase evolution, pyramiding, loss handling
- `references/market-environment.md` — Bull/choppy/bear criteria and position adjustment rules
