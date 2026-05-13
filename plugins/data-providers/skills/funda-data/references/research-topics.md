# Funda Research Topics

The Funda agent has access to ~170 fundamental-research skills plus a
structured-data layer covering filings, transcripts, estimates, ownership
flow, options structure, news, sentiment, and prediction markets. Below are
the domains it covers, with example questions you can pass to `agent_chat`.

## Earnings & Estimates

- "Preview AAPL's Q4 print — segment trends to watch, where consensus is aggressive vs conservative, and the historical beat/miss pattern."
- "Walk through MSFT's Q3: beat/miss by segment, guide vs consensus, and the analyst Q&A color on Azure growth."
- "How have analyst estimates for NVDA's FY26 EPS shifted over the last 90 days, and what drove the revisions?"
- "Decompose AMZN's last earnings beat — operating leverage vs one-time items vs segment mix."

## Company & Sector Research

- "Give me a research primer on PLTR — business mix, customer base, growth drivers, key risks."
- "Who actually competes with CRWD in EDR, and how has CRWD's win rate trended over the last 4 quarters?"
- "Map ASML's top customers and their wafer-start exposure for the N3 / N2 ramp."
- "Summarize the 2026 capex cycle for hyperscalers — spending tiers by name, supplier exposure, gross-margin implications."
- "Walk me through the pharma pipeline economics for LLY — late-stage assets, peak-sales estimates, patent cliff exposure."
- "Frame the housing-cycle outlook for 2026 — affordability, inventory, builder margin compression."

## SEC Filings & Transcripts

- "Diff the new risk factors in TSLA's latest 10-K versus the prior year — flag substantive additions."
- "Pull the substantive content from META's last 8-K and explain what it means for the equity story."
- "Summarize the analyst Q&A from GOOGL's last earnings call — which themes drew the most pushback?"
- "What did NVDA's last 10-Q say about gross-margin trajectory and customer concentration?"
- "Read the S-1 for [recent IPO] and surface the bear case the prospectus glosses over."

## Valuation Methodology

Funda runs the math against assumptions you provide — it does not pick the
assumptions for you, and the output is methodology, not a price target.

- "Walk through a DCF for NVDA assuming 25% data-center growth, 10% terminal margin, 9% WACC — surface the sensitivity table."
- "Build a comp set for SNOW — who belongs in it, what multiples apply, where does SNOW screen rich/cheap on each."
- "Bull / base / bear case for AMD's data-center segment over 8 quarters, with assumptions stated."
- "Review CRWD's capital allocation over the last 3 years — buybacks, M&A, R&D as % of revenue, and what it implies."

## Macro & Cycle Context

- "Where is the Fed in the cutting cycle right now, and what does the dot plot vs market pricing imply for 2026?"
- "Which Dalio quadrant is the US economy in, and which assets historically lead/lag in that regime?"
- "What sectors typically lead in the late stage of a goods recession?"
- "Summarize the credit-cycle indicators flashing right now — corporate spreads, bank lending, default rates."

## Structured Market Data (historical, not live)

- "Has institutional ownership of CRWD shifted in the latest 13F filings — net buyers vs sellers?"
- "What does the gamma exposure profile and skew look like for SPY heading into Friday's close?"
- "How has retail sentiment on PLTR shifted over the last 14 days across Reddit and Twitter?"
- "What is Polymarket pricing for the 2026 Fed rate path?"
- "Show recent congressional trades in semiconductor names and any cluster patterns."

## Tips for Framing

- **Stand-alone questions.** Each `agent_chat` call is a fresh turn with no memory of prior calls. Re-state the ticker, horizon, and assumptions every time.
- **Be specific about horizon.** "Next quarter" vs "next 4 quarters" vs "FY26" — vague horizon gets a vague answer.
- **Surface assumptions for valuation.** Don't ask "is NVDA cheap?" — ask "model NVDA at X% growth and Y% margin and tell me what fair value falls out."
- **One topic per turn.** If you need both an earnings recap AND a DCF, that's two `agent_chat` calls — the agent's run budget is per-turn.
- **Time horizons matter for filings.** "Latest 10-K" → most recent annual; "this quarter's 10-Q" → most recent quarterly. Be explicit if you want a specific filing date.
