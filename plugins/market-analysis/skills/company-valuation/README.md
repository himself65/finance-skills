# Company Valuation

Estimate the intrinsic value of a public company via DCF, relative (peer multiple), and sum-of-parts (SOTP) methods, and blend into a triangulated implied share price with sensitivity tables.

## What it does

- Pulls 5 years of financials + analyst estimates via yfinance
- Builds a 5-year DCF with explicit revenue / margin / WACC / terminal-value assumptions
- Applies peer median P/E, EV/Revenue, EV/EBITDA multiples across 4-6 peers
- Runs SOTP when the company has 2+ distinct reporting segments
- Presents a blended implied price with method weights, WACC × g sensitivity matrix, and Bull/Base/Bear scenarios
- Handles banks/REITs/pre-revenue/cyclical edge cases with appropriate fallbacks

## Triggers

`what is AAPL worth`, `valuation of NVDA`, `fair value of TSLA`, `DCF for MSFT`, `build a DCF`, `intrinsic value`, `implied share price`, `is X overvalued/undervalued`, `relative valuation`, `EV/EBITDA target`, `SOTP`, `sum of the parts`, `price target from fundamentals`, `公司估值`, `估值建模`, `合理股价`

## Prerequisites

- Python 3.8+
- `yfinance`, `numpy`, `pandas` (auto-installed if missing)

Optional: `finance-data-providers:funda-data` skill as a fallback data source.

## Platform

CLI-based agents (Claude Code). Requires shell + pip.

## Setup

No authentication required. First run will auto-install dependencies.

## Reference Files

- `references/dcf.md` — DCF methodology, industry-specific guidance (software, retail, financials, healthcare, energy, manufacturing, CPG, telecom, REITs, streaming), common pitfalls
- `references/relative_valuation.md` — Peer selection heuristics, multiple adjustment rules, Rule of 40 for SaaS, default peer sets by theme
- `references/sotp.md` — Sum-of-parts methodology, conglomerate discount detection, catalyst framework, position sizing
- `references/wacc_erp_rates.md` — Risk-free rates (live + default), equity risk premiums, sector WACC bands, sector-default betas, terminal growth ceilings

## Output

Structured briefing with: headline verdict, snapshot, three-method summary, DCF build, peer comparison, SOTP (if applicable), sensitivity matrix, scenarios, key risks, and caveats.

## Disclaimer

For research and educational purposes only. Not financial advice.
