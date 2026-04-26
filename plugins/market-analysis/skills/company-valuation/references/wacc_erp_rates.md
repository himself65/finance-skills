# WACC, ERP, Risk-Free Rates & Sector Benchmarks

Reference values for cost-of-capital inputs. Prefer live values over these defaults when available.

## Risk-Free Rate

Use the 10-year sovereign yield of the company's reporting currency.

| Market | Instrument | yfinance ticker | Typical range |
|---|---|---|---|
| US | 10Y Treasury | `^TNX` (note: quoted in %, divide by 100) | 3.5-5.0% |
| UK | 10Y Gilt | `^TNX` does not cover; use FRED or manual | 3.0-4.5% |
| Germany | 10Y Bund | Manual (ECB) | 2.0-3.5% |
| Japan | 10Y JGB | Manual (BoJ) | 0.5-1.5% |

**Live fetch:**
```python
import yfinance as yf
rf = yf.Ticker("^TNX").fast_info.last_price / 100
```

**Default (when fetch fails):** `rf = 0.045` (4.5%). Flag as stale.

## Equity Risk Premium (ERP)

Use Damodaran's monthly ERP update (damodaran.nyu.edu) as anchor. Intra-year, 5.5% is a reasonable mid-range.

| Market | ERP (default) | Source |
|---|---|---|
| US | 5.5% | Damodaran implied ERP (S&P 500) |
| Developed Europe | 6.0-6.5% | Country risk + base ERP |
| Japan | 6.0% | Country risk + base ERP |
| China | 7.5-8.5% | Base + country risk premium |
| India | 7.5% | Base + country risk premium |
| Emerging (broad) | 8.0-10.0% | Base + country risk |

Adjust with country risk premium (CRP) for emerging markets:
```
ERP_country = ERP_mature + CRP
```

## Cost of Debt

**Preferred:** `interest_expense / total_debt` from financial statements.

**Fallback: credit rating spreads over risk-free rate.**

| Rating | Spread over RF | Kd range (at RF=4.5%) |
|---|---|---|
| AAA | 0.5-0.8% | 5.0-5.3% |
| AA | 0.8-1.2% | 5.3-5.7% |
| A | 1.2-1.8% | 5.7-6.3% |
| BBB | 1.8-2.5% | 6.3-7.0% |
| BB | 3.5-5.0% | 8.0-9.5% |
| B | 5.5-7.5% | 10.0-12.0% |
| CCC+ | 9.0%+ | 13.5%+ |

**Default (when unknown):** `kd = 0.055` for large-caps, `0.07` for mid-caps.

## Levered Beta Defaults (by sector)

Use when yfinance returns `None` or an implausible value (e.g., beta < 0 for a non-gold stock).

| Sector | Default beta |
|---|---|
| Utilities | 0.55 |
| Consumer staples | 0.70 |
| Telecom | 0.85 |
| Healthcare / pharma | 0.90 |
| REITs | 0.90 |
| Industrials | 1.05 |
| Financials (banks) | 1.15 |
| Consumer discretionary | 1.20 |
| Energy (integrated) | 1.10 |
| Energy (E&P) | 1.40 |
| Technology (large-cap) | 1.15 |
| Technology (SaaS high-growth) | 1.35 |
| Semiconductors | 1.45 |
| Biotech (clinical stage) | 1.60 |
| Auto (EV pure-play) | 1.80 |

Source: Damodaran industry betas (levered, US-listed, recent year-end update).

## WACC Sanity Ranges by Sector

If computed WACC falls outside these bands, double-check inputs (beta, capital structure, kd).

| Sector | WACC range | Notes |
|---|---|---|
| Utilities | 5-7% | High debt capacity, low beta |
| Consumer staples | 7-9% | Low beta, moderate leverage |
| Telecom (large) | 7-9% | Heavy debt, moderate beta |
| Healthcare / pharma | 8-10% | Moderate beta, moderate leverage |
| REITs | 6-8% | High debt (but use WACD + cost of equity separately) |
| Industrials | 8-11% | Cyclical, moderate leverage |
| Financials | 9-12% | High beta, but debt is operational (use cost of equity only) |
| Consumer discretionary | 9-11% | Cyclical, higher beta |
| Energy (majors) | 8-10% | Moderate beta, strong BS |
| Energy (E&P) | 10-12% | High beta, commodity exposure |
| Technology (large-cap) | 8-11% | Low debt, moderate beta |
| SaaS high-growth | 10-13% | High beta, minimal debt → cost of equity dominates |
| Semiconductors | 10-12% | High beta, cyclical |
| Biotech | 11-14% | Very high beta, often pre-revenue |

## Size Premium (CRSP / Ibbotson style)

Small / micro caps justify additional return above CAPM. Add to `ke` if applicable.

| Market cap | Size premium |
|---|---|
| > $20B (mega) | 0% |
| $10-20B (large) | 0% |
| $2-10B (mid) | 0.5-1.0% |
| $500M-$2B (small) | 1.5-2.5% |
| $100-500M (micro) | 2.5-4.0% |
| < $100M (nano) | 4.0%+ |

## Terminal Growth Rate Ceilings

Terminal `g` must be plausible relative to long-run nominal GDP growth. Hard ceilings:

| Economy | Long-run nominal GDP | Max defensible `g` |
|---|---|---|
| US | 4.0-4.5% | 3.0% |
| Developed Europe | 3.0-4.0% | 2.5% |
| Japan | 1.5-2.5% | 1.5% |
| China | 5.0-6.0% | 4.0% |
| India | 7.0-9.0% | 5.0% |

Global-franchise exporters can argue slightly above local GDP, but rarely above +0.5%.

## Cross-Check: Implied Cost of Equity

Back-solve from current multiples to sanity-check WACC:
```
Forward earnings yield ≈ 1 / forward P/E
Implied ke ≈ earnings yield + sustainable growth
```
If computed WACC diverges from this implied number by >300bps, one of the inputs (beta, ERP, growth) is off.
