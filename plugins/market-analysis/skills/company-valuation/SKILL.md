---
name: company-valuation
description: >
  Estimate the intrinsic value of a public company using DCF, relative (peer multiple)
  and sum-of-parts (SOTP) methods, then triangulate to an implied share price with
  upside/downside versus the current market price. Use this skill whenever the user asks:
  "what is AAPL worth", "valuation of NVDA", "fair value of TSLA", "intrinsic value",
  "DCF for MSFT", "build a DCF", "discounted cash flow", "WACC", "terminal value",
  "implied share price", "upside to fair value", "is X overvalued/undervalued",
  "relative valuation", "peer comparison valuation", "EV/EBITDA target", "SOTP",
  "sum of the parts", "how much is [company] worth", "price target from fundamentals",
  "value this company", "公司估值", "估值建模", "合理股价", or any ticker in the context
  of computing intrinsic or relative valuation. Default to running ALL three methods
  (DCF + relative + SOTP-if-applicable) and presenting a blended implied price with a
  sensitivity table. Do not answer valuation questions from memory — always run the workflow.
---

# Company Valuation

Triangulates intrinsic value via three methods, then blends them to an implied share price:

1. **DCF** — 5-year FCFF projection, discount at WACC, terminal value.
2. **Relative** — apply peer median P/E, EV/Revenue, EV/EBITDA.
3. **SOTP** — when 2+ distinct reporting segments exist, value each at pure-play peer multiples.

Always present a WACC × terminal-growth sensitivity table and Bull/Base/Bear scenarios.

**Disclaimer**: Research/educational output. Not financial advice.

---

## Step 1: Detection Flow

Detect data source and runtime deps. The skill supports 3 method paths — pick the richest one available.

**Environment status:**

```
!`python3 -c "import yfinance, numpy, pandas; print('YFIN_OK')" 2>/dev/null || echo "YFIN_MISSING"`
```

```
!`(command -v funda && funda --version) 2>/dev/null || echo "FUNDA_CLI_MISSING"`
```

```
!`python3 -c "import yfinance as yf; t=yf.Ticker('^TNX'); p=t.fast_info.last_price; print(f'RF_10Y={p/100:.4f}')" 2>/dev/null || echo "RF_FETCH_FAIL"`
```

**Decision tree:**

| Condition | Method path |
|---|---|
| `YFIN_OK` | **Path A** (primary): yfinance for financials + peer multiples |
| `YFIN_MISSING` but `FUNDA_CLI_MISSING` is not set | **Path B**: delegate to `finance-data-providers:funda-data` skill for fundamentals |
| Both missing | **Path C**: pip-install yfinance, then Path A. `python3 -m pip install -q yfinance numpy pandas` |
| `RF_FETCH_FAIL` | Use default `rf = 0.045` and note stale risk-free rate in output |

If `RF_10Y=` printed, use that value as `rf` in Step 4d instead of the hardcoded 4.5%.

---

## Step 2: Choose Methods & Set Defaults

### Method applicability

| Company type | DCF | Relative | SOTP | Fallback |
|---|---|---|---|---|
| Mature cash-flow (CPG, telecom, utilities) | ✅ primary | ✅ | ❌ | — |
| High-growth SaaS / software | ✅ with care | ✅ primary | ❌ | Use EV/Revenue + Rule of 40 |
| Multi-segment conglomerate | ✅ | ✅ | ✅ primary | See `references/sotp.md` |
| Banks / insurance | ❌ | ✅ (P/B, P/TBV) | ❌ | DDM or excess return; note in output |
| Pre-revenue | ❌ | EV/Revenue only | ❌ | Flag low confidence |
| REITs | ❌ | ✅ (P/FFO, P/AFFO) | ❌ | NAV-based |
| Cyclicals (energy, semis, industrials) | ✅ on mid-cycle | ✅ | sometimes | Normalize through-cycle |

### Defaults table

Every parameter below MUST have a value before moving to Step 3. Use these unless the user overrides.

| Parameter | Default | Rationale |
|---|---|---|
| Projection horizon | 5 years | Standard explicit forecast window |
| Terminal growth `g` | 2.5% | ~ long-run US GDP |
| Risk-free rate `rf` | Live 10Y UST from Step 1, else 4.5% | Current cost of capital anchor |
| Equity risk premium `erp` | 5.5% | Damodaran mid-range |
| Beta | `info['beta']` from yfinance | Market-observed levered beta |
| Cost of debt `kd` | `interest_expense / total_debt`, else 5.5% | Effective rate; fallback to IG spread |
| Tax rate | 3-yr median effective rate, floored 15%, capped 30% | Strips out one-offs |
| Margin assumptions | 3-yr median of each ratio | Smooths cyclical noise |
| SBC treatment | Cash for software/SaaS; non-cash for industrials/CPG | Industry convention |
| Peer count | 4-6 | Balances signal vs noise |
| Peer multiple | Median (not mean) | Robust to outliers |
| Method weights (no SOTP) | DCF 50% / Relative 50% | Equal triangulation |
| Method weights (with SOTP) | DCF 40% / Relative 30% / SOTP 30% | SOTP gets weight when applicable |
| Sensitivity grid | WACC ±1% in 0.5% steps × g from 1.5-3.5% in 0.5% | 5×5 matrix |

See `references/wacc_erp_rates.md` for current risk-free rates, ERP tables, and sector WACC benchmarks.

---

## Step 3: Pull Data

```python
import yfinance as yf
import numpy as np
import pandas as pd

TICKER = "AAPL"  # replace
t = yf.Ticker(TICKER)

info       = t.info
income_a   = t.income_stmt
cashflow_a = t.cashflow
balance_a  = t.balance_sheet
income_q   = t.quarterly_income_stmt
cashflow_q = t.quarterly_cashflow

earnings_est = t.earnings_estimate
revenue_est  = t.revenue_estimate

price       = info.get("currentPrice") or info.get("regularMarketPrice")
market_cap  = info.get("marketCap")
shares_out  = info.get("sharesOutstanding")
total_debt  = info.get("totalDebt") or 0
cash        = info.get("totalCash") or 0
beta        = info.get("beta") or 1.0
sector      = info.get("sector")
industry    = info.get("industry")
```

Key financial statement rows (yfinance labels):

| Need | Row |
|---|---|
| Revenue | `Total Revenue` |
| EBIT | `Operating Income` |
| Net income | `Net Income` |
| D&A | `Depreciation And Amortization` (in cashflow) |
| CapEx | `Capital Expenditure` (negative) |
| ΔNWC | `Change In Working Capital` (cashflow) |
| SBC | `Stock Based Compensation` (cashflow) |

---

## Step 4: DCF Build

Full methodology + industry-specific tweaks in `references/dcf.md`. Quick skeleton:

```python
# 4a. Revenue growth path — fade from Y1 (consensus or hist CAGR) to terminal g
hist_cagr = (rev[-1] / rev[0]) ** (1 / (len(rev)-1)) - 1
y1 = float(revenue_est.loc["+1y", "growth"]) if "+1y" in revenue_est.index else hist_cagr
g_terminal = 0.025
growth_path = np.linspace(y1, g_terminal + 0.01, 5)

# 4b. Margins — 3y median
ebit_margin = float((income_a.loc["Operating Income"] / income_a.loc["Total Revenue"]).iloc[:3].median())
da_pct      = float((cashflow_a.loc["Depreciation And Amortization"] / income_a.loc["Total Revenue"]).iloc[:3].median())
capex_pct   = float((cashflow_a.loc["Capital Expenditure"].abs() / income_a.loc["Total Revenue"]).iloc[:3].median())
nwc_pct     = float((cashflow_a.loc["Change In Working Capital"].abs() / income_a.loc["Total Revenue"]).iloc[:3].median())
tax_rate    = max(0.15, min(0.30, 0.21))  # use effective if available

# 4c. FCFF per year
rev_t = [float(income_a.loc["Total Revenue"].iloc[0])]
fcff  = []
for g in growth_path:
    rev_t.append(rev_t[-1] * (1 + g))
    ebit = rev_t[-1] * ebit_margin
    nopat = ebit * (1 - tax_rate)
    fcff.append(nopat + rev_t[-1]*da_pct - rev_t[-1]*capex_pct - rev_t[-1]*nwc_pct)

# 4d. WACC
rf, erp, kd = 0.045, 0.055, 0.055  # override rf with live value from Step 1
ke = rf + beta * erp
e_v = market_cap / (market_cap + total_debt)
d_v = 1 - e_v
wacc = e_v*ke + d_v*kd*(1 - tax_rate)

# 4e. Terminal value — compute both, use midpoint
tv_gordon = fcff[-1] * (1 + g_terminal) / (wacc - g_terminal)
tv_exit   = (rev_t[-1] * ebit_margin + rev_t[-1] * da_pct) * 15  # peer median EV/EBITDA
tv_base   = 0.5 * (tv_gordon + tv_exit)

# 4f. Bridge to equity
pv_fcff = sum(f / (1+wacc)**(i+1) for i, f in enumerate(fcff))
pv_tv   = tv_base / (1+wacc)**5
ev      = pv_fcff + pv_tv
equity  = ev + cash - total_debt
implied_price_dcf = equity / shares_out
```

**Gates:** (a) if `wacc <= g_terminal` → stop, g too aggressive; (b) if `pv_tv / ev > 0.85` or `< 0.45` → flag and show both TV methods; (c) if `wacc` is outside the sector sanity band in `references/wacc_erp_rates.md` → note.

---

## Step 5: Relative Valuation

Select 4-6 peers. Peer map and adjustment rules in `references/relative_valuation.md`.

```python
PEERS = ["MSFT", "ORCL", "CRM", "NOW", "SAP", "WDAY"]  # pick by industry
multiples = {}
for p in PEERS:
    pi = yf.Ticker(p).info
    multiples[p] = {
        "pe_fwd": pi.get("forwardPE"),
        "ev_rev": pi.get("enterpriseToRevenue"),
        "ev_ebitda": pi.get("enterpriseToEbitda"),
        "ps": pi.get("priceToSalesTrailing12Months"),
    }
med_pe     = np.nanmedian([v["pe_fwd"] for v in multiples.values()])
med_ev_rev = np.nanmedian([v["ev_rev"] for v in multiples.values()])
med_ev_eb  = np.nanmedian([v["ev_ebitda"] for v in multiples.values()])

eps_ttm    = float(income_q.loc["Diluted EPS"].iloc[:4].sum())
rev_ttm    = float(income_q.loc["Total Revenue"].iloc[:4].sum())
ebitda_ttm = float(income_q.loc["EBIT"].iloc[:4].sum()) + float(cashflow_q.loc["Depreciation And Amortization"].iloc[:4].sum())
net_debt   = total_debt - cash

implied_pe       = med_pe * eps_ttm
implied_ev_rev   = (med_ev_rev * rev_ttm - net_debt) / shares_out
implied_ev_ebit  = (med_ev_eb  * ebitda_ttm - net_debt) / shares_out
implied_price_rel = np.nanmedian([implied_pe, implied_ev_rev, implied_ev_ebit])
```

Adjust peer median ±10-30% if target's growth or margin profile diverges materially. Always state the adjustment and reason. Rule of 40 anchor for SaaS in `references/relative_valuation.md`.

---

## Step 6: SOTP (multi-segment only)

Skip unless the 10-K reports 2+ operating segments with distinct economics. yfinance does NOT expose segment data — user must supply or parse from filings. Full methodology in `references/sotp.md`:
- Identify segments + pure-play peer for each
- Apply peer median EV/EBITDA (or EV/Rev for growth segments)
- Subtract unallocated corporate costs (cap 2-5% of revenue if unknown)
- Subtract net debt, minority interest; divide by shares

SOTP discount = (SOTP price − market price) / SOTP price. Flag if >20% (conglomerate discount).

---

## Step 7: Triangulate, Sensitivity, Scenarios

```python
# Blended implied price
if sotp_price is None:
    blended = 0.5*implied_price_dcf + 0.5*implied_price_rel
else:
    blended = 0.4*implied_price_dcf + 0.3*implied_price_rel + 0.3*sotp_price

# 5x5 sensitivity grid
wacc_grid = [wacc + dx for dx in (-0.01, -0.005, 0, 0.005, 0.01)]
g_grid    = [0.015, 0.020, 0.025, 0.030, 0.035]
sens = {}
for w in wacc_grid:
    for g in g_grid:
        tv = fcff[-1]*(1+g)/(w-g)
        pv = sum(f/(1+w)**(i+1) for i,f in enumerate(fcff)) + tv/(1+w)**5
        sens[(w,g)] = (pv + cash - total_debt) / shares_out
```

Also produce Bull / Base / Bear: shift revenue growth ±300bps, EBIT margin ±200bps, WACC ∓100bps, terminal g 3.0% / 2.5% / 1.5%.

---

## Step 8: Respond to the User

Output in this order:

1. **Headline verdict** — one sentence: blended fair value, vs. current, % upside/downside, most bullish/bearish method. Example: "AAPL fair value ≈ $215 (blended), vs. current $198 → ~9% upside; DCF is most bullish at $228."
2. **Snapshot** — sector, industry, market cap, current price, 3M / 12M price change, LTM revenue growth.
3. **Three-method summary** — 3-column table: method | implied price | weight | brief rationale.
4. **DCF build** — assumptions table (growth path, margins, WACC components, terminal method) + 5-yr FCFF projection table + EV-to-equity bridge.
5. **Peer comparison** — table of peers with P/E fwd, EV/Rev, EV/EBITDA, gross margin, rev growth; bottom row = median; flag target's premium/discount.
6. **SOTP** (if applicable) — segment table + adjustments + equity value.
7. **Sensitivity matrix** — WACC × g grid (5×5), base case highlighted.
8. **Scenarios** — Bull / Base / Bear table with levers + implied price.
9. **Key risks** — 3-5 bullets: which assumption moves the answer most; what could break the thesis.

### Error handling

| Missing / edge case | Action |
|---|---|
| yfinance returns `None` for beta | Use sector-default beta from `references/wacc_erp_rates.md` |
| Negative LTM EBITDA | Skip EV/EBITDA multiple; rely on EV/Revenue + DCF |
| Negative LTM EPS | Skip P/E multiple; use forward P/E if positive, else skip |
| Growth > WACC in Gordon | Cap `g = wacc − 0.5%` and flag |
| Fewer than 3 years history | Use what's available; flag data confidence as "low" |
| Peer data fetch fails | Drop that peer from median; note in output |
| No segment data for SOTP | Skip Section 6; proceed with DCF + Relative only |

### Caveats to include
- TTM data lags real-time; peer multiples reflect market sentiment (can overshoot)
- DCF is garbage-in/garbage-out; sensitivity matters more than a point estimate
- yfinance data is unofficial; cross-check any decision with primary filings
- Not financial advice

---

## Reference Files

- `references/dcf.md` — DCF methodology + industry-specific guidance (software, retail, financials, healthcare, energy, manufacturing, CPG, telecom, REITs, streaming)
- `references/relative_valuation.md` — Peer selection, multiple adjustment rules, Rule of 40, peer sets by theme
- `references/sotp.md` — Sum-of-parts methodology, conglomerate discount detection, catalysts
- `references/wacc_erp_rates.md` — Risk-free rates, equity risk premiums, sector WACC benchmarks, sector-default betas
