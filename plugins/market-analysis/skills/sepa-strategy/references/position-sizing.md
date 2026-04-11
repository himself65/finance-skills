# Position Sizing, Stop Loss & Pyramiding

This is the most critical part of the entire SEPA system. Minervini: "Not losing big is the only prerequisite for winning big." You cannot control how much a stock goes up, but you can fully control how much you lose.

**Key insight**: Minervini discovered that if he had tightened his stop from 15% to 10% early in his career, a losing account would have been profitable (+72%). This discovery made the 7-8% stop loss a sacred, inviolable rule.

## Position Size Formula

The logic: first determine the maximum dollar amount you're willing to lose, then work backward to determine how many shares to buy. **Don't decide position size by looking at the stock — decide it by fixing your risk first.**

```
Shares = (Account Value × Risk Per Trade %) ÷ (Entry Price − Stop Price)
```

### Complete Calculation Example ($100,000 account, 1% risk per trade)

1. **Maximum loss amount** = $100,000 × 1% = **$1,000** (the most this trade can lose)
2. **Entry price**: $50.00. Stop at −7% = $46.50. Stop distance = $50 − $46.50 = **$3.50/share**
3. **Shares** = $1,000 ÷ $3.50 = **285 shares**
4. **Total position** = 285 × $50 = **$14,250** (14.25% of account — reasonable)
5. **Stop price**: $46.50 (exit immediately if touched)
6. **Target 1**: $50 × 1.08 = $54.00 (+8%, sell half)
7. **Target 2**: $50 × 1.15 = $57.50 (+15%, sell another 25%)
8. **Reward/Risk** (to target 2): ($57.50 − $50) / ($50 − $46.50) = 7.5 / 3.5 ≈ **2.14:1** (meets minimum)

## Stop Loss Three-Phase Evolution

### Phase 1: Initial Hard Stop (At Entry)

- Set stop loss order immediately upon entry: **entry price minus 7-8%**
- Non-negotiable. No "let's see how it goes." Entry = stop is set.
- If triggered, exit immediately. Don't ask why, don't hesitate.
- The stop being hit doesn't mean you failed — it means this trade's premise didn't hold. That's normal probability.

### Phase 2: Move to Breakeven (At +8% Profit)

- Sell half the position to lock in profit
- Move stop loss from −7% up to the **entry price (breakeven)**
- After this point, this trade cannot lose money — capital is safe
- The remaining half is now a "free trade" — playing with house money

### Phase 3: Trailing Stop (At +15% Profit)

- Sell another 25% of the original position
- Trail the remaining 25% using the **20-day moving average**
- Update stop weekly to 1-2% below the current 20MA
- When price closes below 20MA, exit all remaining shares — let profits run as long as the trend holds

### Special Case: Rapid Advance

If the stock surges 20-25% in a short period (obvious acceleration), tighten the stop to below the **10MA** instead of the 20MA. This prevents large profit give-back in overextended moves.

### Stop Level Summary

| Scenario | Stop Placement |
|---|---|
| At entry | Entry price − 7-8% |
| Stock at +8% (after selling half) | Entry price (breakeven) |
| Stock at +15% (after selling 25% more) | 1-2% below 20MA, updated weekly |
| Rapid surge (+20-25% quickly) | Tighten to below 10MA |
| Close below 50MA | Serious warning — consider exiting everything |

## Iron Rules

1. **Stop losses only move UP, never down.** Moving a stop down "to give it more room" is how small losses become catastrophic ones.
2. **Never average down on a losing position.** Adding to a loser is the fastest path to account destruction.
3. **After 3-4 consecutive losses**, reduce risk per trade from 1% to 0.5% and cut the number of positions. Determine whether the issue is your execution or the market environment before resuming normal size.
4. **Average loss should be 4-5%, hard cap at 10%.** VCP's precise entry often allows exits at 3-5% loss. The smaller the average loss, the fewer winning trades needed to recover.

## Pyramiding (Adding to Winners)

Pyramiding = adding to a winning position with decreasing size. This is the opposite of averaging down.

### How to Pyramid

| Tranche | Timing | Size | Price (Example) | Shares | Amount |
|---|---|---|---|---|---|
| 1st (Main) | VCP breakout at pivot | 50% of target | $50.00 | 100 | $5,000 |
| 2nd (Add) | +8%, pullback to 20MA | 30% of target | $54.00 | 60 | $3,240 |
| 3rd (Add) | Next base breakout | 20% of target | $58.00 | 35 | $2,030 |
| **Total** | — | 100% | Avg ≈ $53.20 | 195 | $10,270 |

### Why Pyramiding Works

- The largest position (100 shares) is at the lowest cost ($50) — minimum risk, maximum cushion
- Even if tranches 2 and 3 both hit stops (combined loss ~$263), tranche 1's locked profit from the +8% partial sell ($400) covers the loss
- You only add more money when the market proves you right — each addition has a new breakout signal confirming the trend

### Why Averaging Down Fails

- Each addition is at a lower price = the market is proving you wrong
- "$60 → $40, that's down a lot, must be near the bottom" — then it goes to $20, then $5
- "My average cost went from $60 to $52" is an illusion — your real total loss is expanding exponentially
- You're doubling down on a failed thesis
- This is the single fastest way to destroy a trading account

## Handling Losing Trades

SEPA wins only ~50-55% of the time. Nearly half of all trades lose money. This is expected and by design.

### Loss Review Framework (Three Questions)

**Q1: Was it an execution problem or a strategy problem?**
- Execution problem (chased above +5%, didn't set stop, entered with weak volume, entered before earnings) → fix the habit, the strategy isn't wrong
- Strategy problem (misidentified the pattern, entered without trend template confirmation) → study more historical examples to improve recognition

**Q2: Was it a "good loss" or a "bad loss"?**
- Good loss: Followed all rules, market just didn't cooperate, exited at stop — **this is a normal cost of doing business, change nothing**
- Bad loss: Broke rules (no stop, averaged down, chased) — **this is what must be eliminated**

**Q3: Was it the individual stock or the overall market?**
- If recent breakouts are frequently failing, check the market first: indices below MAs? Breadth deteriorating?
- If the market environment has changed, pause trading and wait for improvement rather than forcing more trades

### The Casino Analogy

A casino doesn't win every hand — it wins through mathematical edge (favorable odds) over thousands of hands. SEPA works the same way:
- Win trades average +15-30%
- Lose trades average −5-7%
- Over 10 trades at 50% win rate: 5 × 15% − 5 × 6% = **+45% net**
- A retail trader with 55% win rate but no discipline: 5.5 × 5% − 4.5 × 12% = **−26.5% net**

The win rate matters less than the win/loss size ratio.
