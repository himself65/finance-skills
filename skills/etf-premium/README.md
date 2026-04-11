# ETF Premium/Discount Analysis

Calculate the premium or discount of an ETF's market price relative to its Net Asset Value (NAV).

## When it triggers

- "Is SPY trading at a premium?"
- "AGG premium to NAV"
- "Compare bond ETF discounts"
- "Which ETFs have the biggest discount right now?"
- "Why is BITO at a premium?"
- "ETF premium screener"
- Any request involving ETF market price vs underlying NAV

## What it does

1. Fetches the ETF's current market price and NAV from Yahoo Finance
2. Calculates `(Price - NAV) / NAV × 100` to get the premium/discount percentage
3. Provides context: is this deviation normal for this ETF category?
4. Compares against bid-ask spread to filter out market microstructure noise
5. Supports single ETF analysis, multi-ETF comparison, and screener mode

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

## Reference files

- `references/etf_premium_reference.md` — Detailed formulas, category benchmarks, ETF universe, creation/redemption mechanics
