# ETF Premium/Discount Analysis

Calculate the premium or discount of an ETF's market price relative to its Net Asset Value (NAV).

## When it triggers

- "Is SPY trading at a premium?"
- "AGG premium to NAV"
- "Compare bond ETF discounts"
- "Which ETFs have the biggest discount right now?"
- "Why is BITO at a premium?"
- "ETF premium screener"
- "Why did this ETF jump 13% when its holdings only moved 7%?"
- "Is the rally driven by dealer gamma hedging?"
- "How long until the premium converges?"
- Any request involving ETF market price vs underlying NAV, or decomposing a sudden ETF surge

## What it does

1. Fetches the ETF's current market price and NAV from Yahoo Finance
2. Calculates `(Price - NAV) / NAV × 100` to get the premium/discount percentage
3. Provides context: is this deviation normal for this ETF category?
4. Compares against bid-ask spread to filter out market microstructure noise
5. Supports single ETF analysis, multi-ETF comparison, screener mode, and **gamma-squeeze decomposition** (split a surge into NAV-driven vs structural components, quantify dealer gamma exposure, and assess convergence timeline)

## Platform

**CLI agents only** (Claude Code, Codex, etc.) — requires Python and yfinance.

## Setup

No setup required. The skill auto-installs yfinance if needed.

## Sub-skills

| Sub-skill | Description |
|---|---|
| Single ETF Snapshot | Current premium/discount for one ETF with interpretation |
| Multi-ETF Comparison | Side-by-side comparison ranked by premium/discount |
| Premium Screener | Scan 60+ common ETFs to find extreme premiums/discounts |
| Premium Deep Dive | Full analysis with volatility, liquidity, and causal explanation |
| Premium Surge Decomposition | Decompose a single-day surge into NAV-driven vs excess premium, quantify dealer gamma exposure (GEX) from the options chain, and assess hours/days/weeks convergence timeline |

## Reference files

- `references/etf_premium_reference.md` — Detailed formulas, category benchmarks, ETF universe, creation/redemption mechanics
- `references/gamma_squeeze_reference.md` — Premium decomposition framework, Black-Scholes gamma + GEX formulas with sign conventions, convergence-timeline mechanics, and gamma-squeeze diagnostic table
