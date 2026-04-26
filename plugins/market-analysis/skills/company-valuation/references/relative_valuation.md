# Relative Valuation — Detailed Reference

Relative valuation implies a price by applying peer multiples. Fast, market-anchored, and captures sentiment — but "garbage in, garbage out" when peers are poorly chosen.

## Peer Selection Heuristics

Aim for 4–6 peers. More is noisier, fewer is brittle.

| Criterion | Priority |
|---|---|
| Same GICS industry | Must |
| Similar business model (e.g., SaaS vs perpetual license) | Must |
| Similar growth rate (within ±10 percentage points) | Strong preference |
| Similar margin profile | Preference |
| Similar capital structure | Nice to have |
| Similar geographic exposure | Nice to have |

**Avoid:** Mega-cap diversified companies as peers for pure-play small/mid-caps (e.g., MSFT is not a good peer for DDOG).

## Multiples Cheat Sheet

| Multiple | Best for | Avoid for |
|---|---|---|
| P/E (trailing) | Mature, profitable companies | Unprofitable, cyclical troughs |
| P/E (forward) | Growing, earnings-visible | Early-stage, wide estimate dispersion |
| PEG (P/E ÷ growth) | High-growth profitable | Mature low-growth |
| EV/Revenue | Unprofitable, early SaaS | Mature mixed-margin |
| EV/EBITDA | Mid-to-late stage across capital structures | Financials, REITs |
| EV/EBIT | Capital-intensive (excludes D&A smoothing) | Non-comparable D&A conventions |
| P/B | Banks, insurance | Asset-light businesses |
| P/TBV | Banks | Non-financials |
| P/FFO, P/AFFO | REITs | Anything else |
| EV/Sub, EV/MAU | Streaming, social | Not meaningful elsewhere |

## Computing Implied Price

For each multiple, take peer **median** (not mean — medians are robust to outliers).

```
# Equity multiples
Implied price (P/E) = peer median P/E × target EPS_TTM

# Enterprise multiples
Implied EV (EV/Rev)   = peer median EV/Rev × target Revenue_TTM
Implied EV (EV/EBITDA)= peer median EV/EBITDA × target EBITDA_TTM

Net debt = Total Debt − Cash
Implied equity value = Implied EV − Net debt − Minority interest − Preferred
Implied price = Implied equity value / diluted shares
```

## Adjustments — When NOT to Apply Peer Median Blindly

Adjust ±10–30% based on target vs peer median:

| If target has... | Adjust implied multiple |
|---|---|
| Higher growth rate (>500bps above peer median) | +10% to +30% |
| Lower growth rate | −10% to −30% |
| Higher margin (>300bps above peer median) | +10% to +20% |
| Lower margin | −10% to −20% |
| Better balance sheet / lower leverage | +5% to +10% |
| Higher leverage / covenant risk | −10% to −20% |
| Dominant market position / moat | +10% to +20% |
| Category laggard / market share loss | −10% to −20% |
| Regulatory overhang / activist target | −5% to −15% |

Always state the adjustment and the reason.

## Rule of 40 for SaaS

For software/SaaS peers, add Rule of 40 as a supplementary anchor:

```
Rule of 40 = Revenue Growth % + FCF Margin %
```

| Rule of 40 score | Peer EV/Revenue premium |
|---|---|
| ≥ 50 | Top quartile — use 75th percentile peer multiple |
| 40–50 | Above median — use median + 10% |
| 30–40 | Below median — use median − 10% |
| < 30 | Bottom quartile — use 25th percentile peer multiple |

## Common Peer Sets (Fallback)

Hardcoded starter sets when industry classification is ambiguous. Expand as needed.

| Theme | Peers |
|---|---|
| Enterprise software (large-cap) | MSFT, ORCL, CRM, NOW, SAP, WDAY |
| Horizontal SaaS mid-cap | DDOG, MDB, NET, SNOW, TEAM, ZS |
| Cybersecurity | CRWD, PANW, ZS, S, NET, FTNT |
| Semiconductors (compute / GPU) | NVDA, AMD, AVGO, INTC, QCOM |
| Semiconductor equipment | AMAT, LRCX, KLAC, ASML |
| Mega-cap internet | GOOGL, META, AMZN, MSFT, AAPL |
| E-commerce | AMZN, SHOP, MELI, SE, ETSY |
| Payments | V, MA, PYPL, AXP, SQ |
| US mega-bank | JPM, BAC, C, WFC, GS, MS |
| Regional banks | PNC, TFC, USB, KEY |
| Life insurance | MET, PRU, LNC, AFL |
| P&C insurance | TRV, CB, ALL, PGR |
| Consumer staples | KO, PEP, PG, CL, UL, MDLZ |
| Tobacco | MO, PM, BTI |
| Fast food | MCD, CMG, YUM, QSR, SBUX |
| Apparel / luxury | LVMUY, NKE, LULU, RL |
| Auto (legacy) | F, GM, STLA, TM, HMC |
| Auto (EV) | TSLA, LCID, RIVN, NIO, XPEV |
| Airlines (US) | DAL, UAL, AAL, LUV, ALK |
| Oil & gas majors | XOM, CVX, SHEL, BP, TTE |
| E&P pure-plays | COP, EOG, PXD, DVN, OXY |
| Pharma (large-cap) | PFE, JNJ, MRK, LLY, ABBV, BMY |
| Biotech large-cap | AMGN, GILD, REGN, VRTX |
| Medical devices | MDT, ABT, BSX, SYK, ISRG |
| Industrial conglomerates | GE, HON, MMM, ITW, EMR |
| Defense | LMT, RTX, NOC, GD, BA |
| Telecom | T, VZ, TMUS, CMCSA |
| Utilities | NEE, DUK, SO, D, AEP |
| REITs (diversified) | PLD, AMT, EQIX, CCI, SPG |
| Streaming | NFLX, DIS, WBD, PARA |

## Cross-Check: Target vs Peers Table

Always produce a table of peers with:
- Ticker / name
- Market cap
- Revenue growth (LTM, forward)
- Gross margin, EBITDA margin, operating margin
- P/E (fwd), EV/Revenue, EV/EBITDA
- Peer median (bottom row)

This lets the user see at a glance whether the target "deserves" a premium/discount.

## Common Pitfalls

- **Using a single multiple**: Triangulate with ≥2 multiples. EV/EBITDA should agree with EV/Revenue within ±15% when applied to same peer set.
- **Outlier peers**: Exclude if P/E > 100 or EV/Rev > 50 unless target is similarly extreme.
- **Peer in trough**: If peer is in distress or restructuring, their multiple compresses — excluding them or adjusting.
- **Different fiscal year ends**: Normalize to TTM.
- **Stock-based comp**: EV/EBITDA without SBC adjustment overstates multiples for SaaS. Consider EV/EBITDA (ex-SBC) for SaaS peers.
- **Currency**: International peers — normalize to USD and note FX sensitivity.
