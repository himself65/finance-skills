# Sum-of-the-Parts (SOTP) Valuation

For companies with 2+ reporting segments, SOTP values each segment using pure-play peer multiples, sums them, and compares to market cap to detect conglomerate discount.

## When to Use SOTP

**Triggers:**
- Company has 2+ reportable operating segments in 10-K / 20-F
- Segments operate in materially different industries (e.g., tech + retail, media + theme parks)
- One segment appears to grow faster or be more valuable than blended multiple suggests
- SOTP analysis suggests >20% upside vs current market cap (meaningful conglomerate discount)
- Plausible catalyst within 12-24 months: activist, strategic review, rumored spin-off, board pressure

**Do not force SOTP when:**
- Segments share heavy operational integration (e.g., vertically integrated manufacturers) — synergies would be destroyed by separation
- Segment disclosures are too coarse to model independently
- No realistic path to value realization (management opposed, no activists)

## Workflow

### Step 1: Extract Segment Financials

From latest 10-K / 10-Q segment disclosure, pull per segment:
- Revenue
- Operating income (EBIT)
- EBITDA (if disclosed, else EBIT + allocated D&A)
- Revenue growth YoY
- Operating margin

Track inter-segment eliminations and unallocated corporate expenses separately.

### Step 2: Identify Pure-Play Peers

For each segment, find 3-5 listed pure-play peers in the same industry. Examples:

| Segment type | Pure-play peers |
|---|---|
| Cloud infrastructure | MSFT (Azure), AMZN (AWS), GOOGL (GCP) — for growth multiples |
| Digital advertising | META, GOOGL, TTD, PINS |
| Streaming | NFLX, DIS (DTC), WBD (DTC) |
| Theme parks | SIX, FUN, CCL-adjacent leisure |
| Retail (physical) | WMT, TGT, COST, HD |
| Semiconductors (design) | NVDA, AMD, AVGO, MRVL |
| Semiconductor fab | TSM, INTC (IFS), GFS |
| Auto (legacy) | F, GM, STLA |
| Auto (EV) | TSLA, RIVN, LCID |
| Insurance (P&C) | TRV, CB, ALL, PGR |
| Insurance (life) | MET, PRU, LNC |
| Utility (regulated) | DUK, SO, AEP |
| Pharma / biotech | PFE, MRK, LLY, ABBV |

Record peer median EV/EBITDA, EV/Revenue (for growth segments), and P/E.

### Step 3: Apply Multiples

```
segment_EV_i = segment_EBITDA_i × peer_median_EV/EBITDA_i
```

Use EV/EBITDA as default. For high-growth or pre-profit segments, use EV/Revenue.

### Step 4: Adjust for Corporate-Level Items

```
Total EV from segments
− Unallocated corporate costs (cap at 2-5% of revenue, or discount at 8x the ongoing cost)
− Minority interest
− Total debt
− Preferred stock
− Pension underfunding
+ Cash & equivalents
+ Non-operating assets (excess real estate, investments, NOLs)
= Equity Value

Implied price = Equity Value / diluted shares
```

### Step 5: Compute Conglomerate Discount

```
discount_pct = (SOTP_price − market_price) / SOTP_price × 100
```

Thresholds:
- `>30%`: compelling; likely actionable
- `20-30%`: meaningful; need catalyst
- `10-20%`: narrow; requires catalyst + technicals
- `<10%`: no opportunity

### Step 6: Identify Catalyst

Conglomerate discount can persist indefinitely without a catalyst. Require at least one of:
- Activist investor filed 13D pushing for breakup
- Management publicly discussed "strategic alternatives" or "portfolio simplification"
- Rumored or announced spin-off / divestiture
- CEO change (new CEOs often simplify)
- Peer transaction highlighting valuation gap
- Board refresh with activist nominees

## Example

**DiverseTech Corp (DVTK)** — two segments:
- Cloud Platform: $3B rev, 30% growth, 25% EBITDA margin → $0.75B EBITDA
- Legacy Hardware: $5B rev, flat, 15% EBITDA margin → $0.75B EBITDA

Peer multiples:
- Cloud peers median EV/EBITDA: 20x → cloud EV = $15B
- Hardware peers median EV/EBITDA: 8x → hardware EV = $6B

```
Total segment EV = $21B
− Corporate costs  = $2B
− Net debt         = $2B
= Equity value     = $17B
Shares out         = 250M
Implied SOTP price = $68
Market price       = $42
Discount           = 38% — compelling
```

Catalyst: Activist filed 13D demanding cloud spin-off. Enter position at $42.

## Edge Cases & Traps

| Issue | Handling |
|---|---|
| Shared costs allocated inconsistently | Read 10-K segment footnote; recalculate if allocation is arbitrary |
| Synergy destruction | Deduct 5-15% of segment EV for operational coupling (shared sales, shared R&D) |
| Tax leakage on spin-off / divestiture | Factor 10-20% of realized value as tax cost |
| Minority interest in a segment | Multiply segment EV by parent's ownership % |
| Hidden liabilities (env, pension, litigation) | Review 10-K footnotes; subtract estimated NPV |
| Persistent discount with no catalyst | Don't invest — "dead money" until catalyst materializes |
| Peer group too narrow | Use broader set to avoid anchoring on inflated comps |
| Segment EBITDA before stock comp | Reconcile — SaaS peers may be post-SBC, industrial peers pre-SBC |

## Position Sizing (if SOTP feeds into a trade)

- 4-6% of portfolio per SOTP position (value trades with identified catalyst)
- Stop-loss: −15% from entry (wider stop because discount can widen before closing)
- Time stop: 12 months with no catalyst progress → reassess
- Portfolio cap: 15% of capital in SOTP / conglomerate-discount trades (correlated risk)
- Trim when discount narrows to <10%; add when it widens to >35% with no thesis break

## Performance Expectations

- Win rate with catalyst: 55-65%
- Win rate without catalyst: 40-45%
- Average winner: +20% to +40% over 12-24 months
- Average loser: −10% to −15%
- Risk/reward with catalyst: 2:1 to 3:1
