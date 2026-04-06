---
name: saas-valuation-compression
description: >
  Analyze SaaS company valuation compression between funding rounds. Use this skill
  whenever the user asks about: how much a SaaS company's valuation multiple changed
  between rounds, why the ARR multiple compressed or expanded, comparing a company's
  compression to macro benchmarks, or explaining what drove valuation changes for
  any VC-backed software company. Trigger on phrases like "valuation compression",
  "ARR multiple", "round-to-round valuation", "multiple change", or when
  the user asks to compare a company's funding rounds. Always use this skill for
  any multi-round SaaS valuation analysis — do not try to answer from memory alone.
---

# SaaS Valuation Compression Analyzer

## What This Skill Does

For a given SaaS company, research its funding history and compute ARR-based valuation
multiples at each round. Then explain the compression (or expansion) using a structured
framework that covers macro rates, growth trajectory, narrative shifts, and comparables.

Always render the output as an inline visualization (using the Visualizer tool) plus a
concise prose explanation. Do not just return a wall of numbers.

---

## Step-by-Step Workflow

### 1. Gather Data via Web Search

Search for each of the following. Run searches in parallel where possible.

**For the target company:**
- `[company] funding rounds valuation ARR revenue`
- `[company] Series [X] raised valuation` for each round
- `[company] annual recurring revenue ARR [year]` for each round date
- `[company] investors lead investor [round]`

**For macro context:**
- `SaaS ARR valuation multiples [year] private market`
- Use the known benchmark table below as fallback if search is thin.

**For narrative context:**
- `[company] AI customers product announcement [year]` — AI narrative premium?
- `[company] growth rate churn NRR [year]` — fundamentals shift?

### 2. Build the Data Model

For each funding round, extract or estimate:

| Field | How to get it |
|---|---|
| Round name | Direct from search |
| Date | Direct from search |
| Amount raised | Direct from search |
| Post-money valuation | Direct or compute from ownership %; if unavailable, note as estimated |
| ARR at round date | Search explicitly; if not found, estimate from customer count x ARPC or interpolate |
| ARR multiple | `valuation / ARR` |
| Lead investor | Direct |

**ARR estimation heuristics (when not public):**
- Seed/Series A: ARR often $500K–$3M
- Series B: typically $5M–$20M
- Series C: typically $20M–$60M
- Cross-check against customer count x average deal size if available

### 3. Compute Compression Metrics

For each consecutive round pair (e.g., B → C):

```
multiple_compression_pct = (later_multiple - earlier_multiple) / earlier_multiple × 100
valuation_growth_pct = (later_val - earlier_val) / earlier_val × 100
arr_growth_pct = (later_arr - earlier_arr) / earlier_arr × 100
```

Key insight: `valuation_growth = arr_growth + multiple_change`
If ARR grows faster than the multiple compresses, absolute valuation still rises.

### 4. Attribute Compression to Causes

Use this checklist. For each cause, rate it: Primary / Contributing / Not applicable.

**Macro / Rate Environment**
- Was the earlier round during 2020–2021 ZIRP bubble? (adds ~2–5x artificial premium)
- Was the later round during 2022–2023 rate hikes? (removes bubble premium)
- Reference: SaaS private market median multiples by period:

| Period | Approx Median ARR Multiple (private) |
|---|---|
| 2019 | ~8–12x |
| 2020 | ~12–18x |
| 2021 Q1–Q3 peak | ~35–45x |
| 2022 H2 | ~15–20x |
| 2023 trough | ~8–12x |
| 2024 | ~12–18x |
| 2025–2026 | ~16–22x |

*(These are rough private market estimates. Public SaaS multiples are ~30–50% lower.)*

**Growth Deceleration**
- Did YoY ARR growth rate slow materially between rounds? (most common cause)
- Did NRR/net retention drop?

**Narrative Shift**
- Did the company lose a major product story (e.g., lost PLG thesis, missed category leadership)?
- Did competitors emerge or incumbents catch up?

**AI Premium (positive or negative)**
- Does the company serve AI-native companies (OpenAI, Anthropic, etc.) as customers? → premium
- Did the company pivot to AI narrative credibly? → premium
- Did the company fail to articulate AI story? → discount vs peers

**Competitive / Market**
- Market saturation signal (e.g., Okta pressure on WorkOS, Auth0 competition)
- Customer concentration risk revealed

**Investor Supply / Demand**
- Was the later round smaller and more selective? → price discipline
- New tier of lead investor (e.g., Tier 1 growth fund vs seed fund)? → may signal higher or lower conviction

### 5. Build the Visualization

Use the Visualizer tool to render:

1. **Metric cards row** — valuation at each round, ARR at each round, multiple at each round, compression %
2. **Line chart** — ARR multiple over time for the company vs macro SaaS median
3. **Bar chart** — valuation growth vs ARR growth vs multiple change (decomposition)
4. **Comparison bar** — company compression vs 2–3 peer comparables (Vercel, Netlify, Fastly, or sector peers)
5. **Cause attribution table** inline in prose (Primary / Contributing / N/A per factor)

See design guidance: use teal for positive/growth, coral for compression/negative, gray for macro baseline, blue for valuation figures. Follow the CSS variable system throughout.

### 6. Write the Prose Summary

Structure as:
1. **One-sentence verdict** — e.g., "Multiple compressed 36% but ARR grew 5x, so absolute valuation rose 3.8x."
2. **Primary cause** — the #1 factor explaining compression
3. **Narrative premium/discount** — AI story, category leadership, or lack thereof
4. **Comparable context** — how does this company's compression compare to peers?
5. **Forward implication** — what would need to be true for the multiple to expand at next round?

---

## Output Format

Always produce:
- Inline visualization (Visualizer tool) — comes first
- Prose summary (5–8 sentences) — follows the visualization
- Optional: flag data confidence level if ARR had to be estimated

---

## Known Benchmarks & Comparables (pre-loaded)

Use these as context when search results are thin or for the comparison chart.

| Company | Round pair | Earlier multiple | Later multiple | Compression % | Primary cause |
|---|---|---|---|---|---|
| Vercel | D → E (2021→2024) | ~140x | ~32x | -77% | ZIRP unwind + growth decel |
| WorkOS | B → C (2022→2026) | ~105x | ~67x | -36% | Partial ZIRP unwind; defended by AI narrative |
| Netlify | B → stalled (2021→?) | ~90x | N/A | N/A | No new round; AI narrative absent |
| Fastly | Public (2021 peak→2024) | ~35x rev | ~3x rev | -91% | No AI pivot, growth decel |
| Stripe | — | — | — | — | Private; est. flat/compressed 2021→2023 down round |
| HashiCorp | Acquired by IBM 2024 | — | — | — | Acq at ~8x ARR vs ~40x peak |

---

## Edge Cases

- **Down round**: Multiple and absolute valuation both dropped. Note dilution implications.
- **No public ARR**: Use customer count x estimated ARPC, and label as estimate with +/- range.
- **Single round only**: Compute multiple vs sector median for that date; can't do compression analysis. Explain this.
- **Pre-revenue**: Use forward ARR or GMV multiple if applicable; note the different basis.
- **Acqui-hire / strategic acquisition**: Acquisition price often reflects strategic premium or distress, not pure ARR multiple — flag this.
