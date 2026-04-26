# DCF Methodology — Detailed Reference

Expands on the summary in SKILL.md. Use this when building the DCF build table or when the user asks for industry-specific treatment.

## When DCF Is Appropriate

**Good fit:**
- Mature companies with predictable cash flows
- Companies whose revenue and margin trajectory can be estimated within a reasonable confidence band
- Strategic valuations requiring intrinsic value assessment
- Cross-checking a relative valuation

**Poor fit:**
- Pre-revenue / early-stage (no cash flow history)
- Banks, insurance (use DDM or excess return model)
- REITs (use NAV)
- Highly cyclical businesses without a clear cycle baseline — use mid-cycle earnings instead

## Projection Model (5-Year Explicit Forecast)

### Revenue projection

1. Compute historical 3–5 year CAGR.
2. Pull analyst consensus from `yfinance.Ticker.revenue_estimate`.
3. Consider industry growth, competitive position, and company guidance.
4. Project revenue for Y1–Y5, fading linearly toward terminal growth rate.

```
Revenue_t = Revenue_{t-1} × (1 + g_t)
```

### EBIT and Free Cash Flow Build

```
Revenue
- COGS                          → historical gross margin trend
= Gross Profit
- SG&A                          → historical SG&A % of revenue
- R&D                           → historical R&D % of revenue
- Other OpEx
= EBIT (Operating Income)

FCFF = EBIT × (1 − Tax Rate)
     + Depreciation & Amortization
     + Stock-Based Compensation    ← only if treating SBC as non-cash
     − Capital Expenditures
     − Change in Net Working Capital
```

### Assumption checklist (state explicitly)

| Assumption | How to derive | Typical range |
|---|---|---|
| Tax rate | Effective tax rate from historicals | 15–25% US; use statutory if unreliable |
| D&A | % of revenue or PP&E schedule | 3–8% revenue for most; 15–25% for telecom/utilities |
| CapEx | % of revenue; split maintenance vs growth if possible | 3–8% SaaS; 8–15% industrials; 15–25% telecom |
| NWC change | Days sales outstanding, DPO, days inventory | Usually 1–3% of Δrevenue |
| SBC treatment | Cash for software/SaaS, non-cash for industrials/CPG | Decide upfront and disclose |

## WACC Calculation

```
WACC = (E/V) × Ke + (D/V) × Kd × (1 − Tax Rate)
```

### Cost of Equity (CAPM)

```
Ke = Risk-Free Rate + Beta × Equity Risk Premium + Size Premium (if applicable)
```

| Component | Source | Typical range |
|---|---|---|
| Risk-free rate | 10-year US Treasury | 3.5–5.0% (use current) |
| Equity risk premium | Damodaran or Duff & Phelps | 4.5–6.0% |
| Beta | yfinance `info['beta']` (levered) | 0.6–2.0 |
| Size premium | Add for small/mid-cap | 0–3% |

### Cost of Debt

- Preferred: interest expense / total debt from financials.
- Fallback: credit rating spread over risk-free rate.
- Investment-grade: 4–6%. High-yield: 7–10%.

### Capital structure

Use **market** values:
- E = market cap
- D = total debt (balance sheet)
- V = E + D

## Terminal Value

### Method 1: Perpetuity Growth (Gordon Growth)

```
TV = FCFF_5 × (1 + g) / (WACC − g)
```

- Terminal growth `g`: 2–3% typical; must not exceed long-term GDP (~2.5% US, ~3–4% EM).
- TV normally represents 60–80% of total EV. Flag if outside that range.

### Method 2: Exit Multiple

```
TV = EBITDA_5 × exit EV/EBITDA multiple
```

- Use current peer trading multiples as reference.
- Apply discount for growth deceleration by Y5.
- Cross-check against Gordon TV — if they diverge by >30%, reconcile assumptions.

## Bridge to Equity Value

```
PV of FCFF = Σ FCFF_t / (1 + WACC)^t  for t = 1..5
PV of TV   = TV / (1 + WACC)^5

Enterprise Value = PV of FCFF + PV of TV
+ Cash & equivalents
− Total debt
− Minority interest
− Preferred stock
+ Equity investments (if material)
= Equity Value

Implied share price = Equity Value / diluted shares outstanding
```

## Sensitivity & Scenarios

### WACC × Terminal Growth matrix

5×5 grid. Vary WACC by ±1% in 0.5% steps and `g` by 0.5% from 1.5% to 3.5%. Highlight base case.

### Scenario analysis

| Scenario | Levers |
|---|---|
| Bull | Higher revenue growth, margin expansion, lower WACC |
| Base | Median historicals / consensus |
| Bear | Revenue deceleration, margin compression, higher WACC |

## Industry-Specific Guidance

### Technology / SaaS
- EV/Revenue often more meaningful than P/E if not yet profitable.
- Key metrics: ARR growth, net dollar retention (NRR), Rule of 40 (growth% + FCF margin ≥ 40).
- CapEx light (3–8% rev); R&D heavy (15–30%).
- SBC material — decide cash vs non-cash upfront and disclose.
- Terminal growth: 3–4% for category leaders, 2–3% others.

### Retail / E-commerce
- Revenue = same-store sales growth + new store openings (physical) OR GMV growth (digital).
- Working capital matters: inventory turns, payables.
- Split CapEx: maintenance (existing) vs growth (new stores/fulfillment).
- Normalize for one-time charges (store closures, write-downs).

### Financial Services (Banks / Insurance)
- Standard DCF is wrong. Use DDM or excess return model.
- If forced: project NII, provisions, non-interest income separately.
- Discount rate = cost of equity only (debt is operational).

### Healthcare / Pharma
- Separate existing portfolio from pipeline.
- Key risk: patent cliffs, FDA approval probability.
- R&D: 15–25% of revenue.
- Biotech: risk-adjust pipeline NPV by phase success probability.

### Energy (Oil & Gas)
- Revenue tied to commodity prices — use strip pricing or scenarios.
- High CapEx; distinguish development vs exploration.
- Depletion accounting differs from standard D&A.
- Terminal value very sensitive to long-term price deck.

### Manufacturing / Industrial
- Cyclical — use mid-cycle earnings for normalization.
- CapEx 8–15% of revenue.
- Working capital swings with cycle — use through-cycle averages.
- WACC 8–11% typical.

### Consumer Goods (CPG)
- Stable, predictable — good DCF candidates.
- Distinguish organic vs M&A growth.
- Watch gross margin trends, A&P spend, input costs.
- Terminal growth 2–3% (population + inflation).

### Telecommunications
- High CapEx (15–25%) for network buildout.
- Recurring revenue, low churn — good for DCF.
- Spectrum costs lumpy.
- WACC 7–9% for large incumbents.

### Real Estate / REITs
- Use NAV as primary; DCF supplementary.
- Project NOI instead of FCF.
- Cap rate replaces WACC at property level.
- Distinguish maintenance vs growth CapEx.

### Media / Streaming
- Subscriber growth × ARPU drives revenue.
- Content spend dominant cost — capitalize vs expense debate matters.
- Path to profitability > current margin for growth-stage.
- High operating leverage at scale.

## Common Pitfalls

- **Terminal value dominance**: If TV > 80% of EV, model is really a multiple-expansion bet. Disclose.
- **Growth > WACC**: Breaks Gordon formula. Cap `g` below WACC.
- **Inconsistent tax rates**: Historical effective rate may include one-offs. Cross-check with statutory.
- **Double-counting SBC**: Either subtract SBC from FCFF OR use diluted shares that price it in — not both, and not neither.
- **Stale beta**: yfinance beta may be 5-year or 3-year. For recent IPOs or post-restructuring businesses, compute fresh.
- **Ignoring minority interest / preferred**: These are claims on EV ahead of common equity. Always subtract.
- **Circular WACC**: WACC uses market cap → which is what we're trying to estimate. For IPOs or controversial names, iterate or use target capital structure.
