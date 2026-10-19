---
name: options-payoff
description: >
  Render an interactive options payoff chart — expiry P&L plus Black-Scholes theoretical
  value — with sliders for strikes, premium, IV, DTE, and spot. Use this skill whenever
  the user describes or shares an options position or strategy and wants to see how it
  makes or loses money: vertical, calendar, diagonal, or ratio spreads, butterflies,
  condors and iron condors, straddles, strangles, covered calls, protective or naked
  puts, or any multi-leg structure. This includes pasted strikes, premiums, and
  expiries, requests like "show me the payoff" or "draw the P&L curve", and broker
  screenshots (IBKR, TastyTrade, Robinhood). Use it even when details are partial —
  defaults fill the gaps.
---

# Options Payoff Curve Skill

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Generates an interactive HTML chart using the host's available visualization tool, or a standalone HTML file in Codex, showing:
- **Expiry payoff curve** (dashed gray line) — intrinsic value at expiration
- **Theoretical value curve** (solid colored line) — Black-Scholes price at current DTE/IV
- Dynamic sliders for all key parameters
- Real-time stats: max profit, max loss, breakevens, current P&L at spot

---

## Step 1: Extract Strategy From User Input

When the user provides a screenshot or text, extract:

| Field | Where to find it | Default if missing |
|---|---|---|
| Strategy type | Title bar / leg description | "custom" |
| Underlying | Ticker symbol | SPX |
| Strike(s) | K1, K2, K3... in title or leg table | nearest round number |
| Premium paid/received | Filled price or avg price | 5.00 |
| Quantity | Position size | 1 |
| Multiplier | 100 for equity options, 100 for SPX | 100 |
| Expiry | Date in title | 30 DTE |
| Spot price | Current underlying price shown in the screenshot or text | live quote (see below); middle strike only if no quote is available |
| IV | Shown in greeks panel, or estimate from vega | 20% |
| Risk-free rate | — | 4.3% |

**Spot for screenshots**: spot is the underlying's current price, and broker screenshots often omit it or show it far from the strikes — don't read it off the strike labels. Use the price shown, else a live quote (the SPX probe below, or yfinance for other underlyings). Fall back to the middle strike only when no quote is available, and tell the user you did.

**Current SPX reference price:**
```
!`python3 -c "exec('try:\n import yfinance as yf\n p=yf.Ticker(\'^GSPC\').fast_info[\'lastPrice\']\n print(f\'SPX ≈ {p:.0f}\')\nexcept Exception:\n print(\'SPX price unavailable — check market data\')')"`
```

---

## Step 2: Identify Strategy Type

Match to one of the supported strategies below, then read the corresponding section in `references/strategies.md`.

| Strategy | Legs | Key Identifiers |
|---|---|---|
| **butterfly** | Buy K1, Sell 2×K2, Buy K3 | 3 strikes, "Butterfly" in title |
| **vertical_spread** | Buy K1, Sell K2 (same expiry) | 2 strikes, debit or credit |
| **calendar_spread** | Buy far-expiry K, Sell near-expiry K | Same strike, 2 expiries |
| **iron_condor** | Sell K2/K3, Buy K1/K4 wings | 4 strikes, 2 spreads |
| **straddle** | Buy Call K + Buy Put K | Same strike, both types |
| **strangle** | Buy OTM Call + Buy OTM Put | 2 strikes, both OTM |
| **covered_call** | Long 100 shares + Sell Call K | Stock + short call |
| **naked_put** | Sell Put K | Single leg |
| **ratio_spread** | Buy 1×K1, Sell N×K2 | Unequal quantities |

For strategies not listed, use `custom` mode: decompose into individual legs and sum their P&Ls.

---

## Step 3: Compute Payoffs

### Black-Scholes Put Price
```
d1 = (ln(S/K) + (r + σ²/2)·T) / (σ·√T)
d2 = d1 - σ·√T
put = K·e^(-rT)·N(-d2) - S·N(-d1)
```

### Black-Scholes Call Price (via put-call parity)
```
call = put + S - K·e^(-rT)
```

### Butterfly Put Payoff (expiry)
```
if S >= K3: 0
if S >= K2: K3 - S
if S >= K1: S - K1
else: 0
```
Net P&L per share = payoff − premium_paid

### Vertical Spread (call debit) Payoff (expiry)
```
long_call = max(S - K1, 0)
short_call = max(S - K2, 0)
payoff = long_call - short_call - net_debit
```

### Calendar Spread Theoretical Value
Calendar cannot be expressed as a simple expiry function — always use BS pricing for both legs:
```
value = BS(S, K, T_far, r, IV_far) - BS(S, K, T_near, r, IV_near)
```
For expiry curve of calendar: near leg expires worthless, far leg = BS with remaining T.

### Iron Condor Payoff (expiry)
```
put_spread = max(K2-S, 0) - max(K1-S, 0)   // short put spread
call_spread = max(S-K3, 0) - max(S-K4, 0)  // short call spread
payoff = credit_received - put_spread - call_spread
```

---

## Step 4: Render the Widget

When `visualize:read_me` is available, read modules `["chart", "interactive"]` before building and use `visualize:show_widget` to render. Otherwise use an available host visualization tool according to its documented interface. In Codex without an inline renderer, save a complete HTML document in the workspace, include the chart dependencies and CSS, verify it in a browser when available, and return a clickable file link. Preserve all controls and calculations below. Do not call tools that the host does not expose.

### Required Controls (sliders)

**Structure section:**
- All strike prices (K1, K2, K3... as needed by strategy)
- Premium paid/received
- Quantity
- Multiplier (100 default, show for clarity)

**Pricing variables section:**
- IV % (5–80%, step 0.5)
- DTE — days to expiry (0–90)
- Risk-free rate % (0–8%)

**Spot price:**
- Full-width slider, range = [min_strike - 20%, max_strike + 20%], defaulting to ACTUAL current spot

### Required Stats Cards (live-updating)
- Max profit (expiry)
- Max loss (expiry)
- Breakeven(s) — show both for two-sided strategies
- Current theoretical P&L at spot

### Chart Specs
- X-axis: SPX/underlying price
- Y-axis: Total USD P&L (not per-share)
- Blue solid line = theoretical value at current DTE/IV
- Gray dashed line = expiry payoff
- Green dashed vertical = strike prices (K2 center strike brighter)
- Amber dashed vertical = current spot price
- Fill above zero = green 10% opacity; below zero = red 10% opacity
- Tooltip: show both curves on hover

### Code template

Use this JS structure inside the widget, adapting `pnlExpiry()` and `bfTheory()` per strategy:

```js
// Black-Scholes helpers (always include)
function normCDF(x) { /* Horner approximation */ }
function bsCall(S,K,T,r,sig) { /* standard BS call */ }
function bsPut(S,K,T,r,sig) { /* standard BS put */ }

// Strategy-specific expiry payoff (returns per-share value BEFORE premium)
function expiryValue(S, ...strikes) { ... }

// Strategy-specific theoretical value using BS
function theoreticalValue(S, ...strikes, T, r, iv) { ... }

// Main update() reads all sliders, computes arrays, destroys+recreates Chart.js instance
function update() { ... }

// Attach listeners
['k1','k2',...,'iv','dte','rate','spot'].forEach(id => {
  document.getElementById(id).addEventListener('input', update);
});
update();
```

---

## Step 5: Respond to User

After rendering the widget, briefly explain:
1. What strategy was detected and how legs were mapped
2. Max profit / max loss at current settings
3. One key insight (e.g., "spot is currently 950 pts below the profit zone, expiring tomorrow")

Keep it concise — the chart speaks for itself.

---

## Reference Files

- `references/strategies.md` — Detailed payoff formulas and edge cases for each strategy type
- `references/bs_code.md` — Copy-paste ready Black-Scholes JS implementation with normCDF

Read the relevant reference file if you're unsure about payoff formula edge cases for a given strategy.
