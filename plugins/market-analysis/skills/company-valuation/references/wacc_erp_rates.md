# WACC, ERP, Risk-Free Rates & Sector Benchmarks

Reference values for cost-of-capital inputs. Prefer live values over snapshots and record the observation date for every rate.

## Freshness policy

- Use a risk-free rate observed within the last five trading days.
- Use Damodaran's latest monthly US implied ERP and latest quarterly country-risk update.
- Use the latest annual industry beta and cost-of-capital tables, then relever beta to the subject company's target capital structure.
- Keep risk-free rate and ERP conventions consistent. If you subtract a sovereign default spread from the Treasury yield, add that spread to the US ERP as Damodaran specifies.
- Label every fallback with its as-of date. Never present a snapshot as current live data.

**Latest checked snapshot (August 1, 2026):** Damodaran reported a 4.28% US implied ERP, a 4.74% US Treasury rate, and a 0.22% US default spread. These are offline fallbacks only; refresh them at runtime.

Primary references: [monthly implied ERP](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm), [country risk premiums](https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/ctryprem.html), [US industry betas](https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/Betas.html), and [US industry costs of capital](https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/wacc.html).

## Risk-Free Rate

Use the 10-year sovereign yield of the company's reporting currency.

| Market | Instrument | Preferred live source |
|---|---|---|
| US | 10Y Treasury | US Treasury or FRED `DGS10`; `^TNX` is a market-data fallback quoted in percent |
| UK | 10Y Gilt | Bank of England yield-curve data |
| Euro | 10Y AAA euro-area central-government spot rate | ECB yield-curve data |
| Japan | 10Y JGB | Bank of Japan or Japan Ministry of Finance |

**Live fetch:**
```python
import yfinance as yf
rf = yf.Ticker("^TNX").fast_info.last_price / 100
```

**Offline US fallback:** `rf = 0.0474` (4.74%, August 1, 2026). Flag it as stale and include the date. If using Damodaran's default-adjusted dollar risk-free convention instead, use 4.52% and increase the paired ERP by 0.22 percentage points.

## Equity Risk Premium (ERP)

Use Damodaran's monthly ERP update as the US anchor and his latest country-risk spreadsheet for other markets. Do not rely on an undated long-run average when an implied ERP is available.

| Market | Runtime method | Offline fallback |
|---|---|---|
| US | Latest monthly Damodaran implied ERP | 4.28% (August 1, 2026) |
| Mature market without added country risk | US ERP minus the contemporaneous US default spread | 4.06% using the August 2026 pair |
| Other countries | Mature-market ERP + latest country risk premium | Read the latest Damodaran country table; do not hardcode a regional bucket |

Adjust with country risk premium (CRP) for emerging markets:
```
ERP_country = ERP_mature + CRP
```

## Cost of Debt

**Preferred:** `interest_expense / total_debt` from financial statements.

**Fallback: credit rating spreads over risk-free rate.**

| Rating | Illustrative spread over RF |
|---|---|
| AAA | 0.5-0.8% |
| AA | 0.8-1.2% |
| A | 1.2-1.8% |
| BBB | 1.8-2.5% |
| BB | 3.5-5.0% |
| B | 5.5-7.5% |
| CCC+ | 9.0%+ |

Refresh synthetic-rating spreads from Damodaran's current ratings table. If no rating or coverage ratio is available, use a size-appropriate spread over the live risk-free rate and disclose it; do not use a fixed nominal cost of debt.

## Levered Beta Defaults (by sector)

Use when yfinance returns `None` or an implausible value (e.g., beta < 0 for a non-gold stock).

| Damodaran US industry | January 2026 beta |
|---|---|
| Utility (General) | 0.24 |
| Food Processing | 0.61 |
| Telecom Services | 0.63 |
| Drugs (Pharmaceutical) | 0.98 |
| R.E.I.T. | 0.64 |
| Business & Consumer Services | 0.89 |
| Banks (Regional) | 0.40 |
| Bank (Money Center) | 0.76 |
| Auto & Truck | 1.46 |
| Oil/Gas (Integrated) | 0.30 |
| Oil/Gas (Production and Exploration) | 0.72 |
| Software (System & Application) | 1.28 |
| Software (Internet) | 1.69 |
| Semiconductor | 1.52 |
| Drugs (Biotechnology) | 1.14 |

Source: Damodaran industry betas for US-listed companies, data as of January 2026. Use the exact industry row where possible; these selected rows are fallbacks, not a substitute for relevering.

## Cost-of-Capital Sanity Anchors by Sector

Compare computed WACC with the current Damodaran industry table. The selected January 2026 US anchors below are useful for detecting unit, beta, leverage, or tax mistakes, but they are not valuation inputs by themselves.

| Damodaran US industry | January 2026 cost of capital | Notes |
|---|---|---|
| Utility (General) | 4.36% | High debt capacity and low beta |
| Food Processing | 5.79% | Defensive demand, moderate leverage |
| Telecom Services | 5.39% | Heavy debt and lower beta |
| Drugs (Pharmaceutical) | 7.85% | Diversified operating companies |
| R.E.I.T. | 5.32% | Cross-check with property-level cap rates and debt costs |
| Business & Consumer Services | 7.23% | Broad services proxy |
| Auto & Truck | 9.38% | Cyclical and capital intensive |
| Oil/Gas (Integrated) | 5.07% | Large integrated producers |
| Oil/Gas (Production and Exploration) | 6.25% | Commodity-sensitive upstream producers |
| Software (System & Application) | 9.34% | Mature and growth software mix |
| Software (Internet) | 10.66% | Higher-beta internet software |
| Semiconductor | 10.55% | Cyclical, equity-heavy capital structure |
| Drugs (Biotechnology) | 8.49% | Broad biotech sample; clinical-stage firms may require scenario methods |

For banks and insurers, debt is operational funding. Prefer cost of equity and sector-appropriate valuation methods instead of a conventional industrial-company WACC.

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
