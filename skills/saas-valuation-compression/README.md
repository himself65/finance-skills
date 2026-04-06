# saas-valuation-compression

Analyze SaaS company valuation compression between funding rounds.

## What it does

This skill researches a SaaS company's funding history and computes ARR-based valuation multiples at each round, then explains the compression (or expansion) using a structured framework:

- **Data gathering** — funding rounds, valuations, ARR, lead investors via web search
- **Compression metrics** — ARR multiple change, valuation growth decomposition
- **Cause attribution** — macro/ZIRP, growth deceleration, narrative shifts, AI premium, competitive dynamics
- **Visualization** — metric cards, line charts, bar charts, and peer comparisons
- **Prose summary** — one-sentence verdict, primary cause, comparable context, forward implications

## Triggers

- "valuation compression" or "ARR multiple" analysis
- "round-to-round valuation" comparisons
- "why did the multiple compress/expand"
- Comparing a company's funding rounds
- Any multi-round SaaS valuation analysis

## Known benchmarks

Includes pre-loaded comparables for Vercel, WorkOS, Netlify, Fastly, Stripe, and HashiCorp with compression percentages and primary causes.

## Platform

Works on **All** platforms (Claude.ai, Claude Code, and other supported agents). Uses web search for data gathering and the Visualizer tool for inline charts.

## Setup

```bash
# As a plugin (recommended — installs all skills)
npx plugins add himself65/finance-skills

# Or install just this skill
npx skills add himself65/finance-skills --skill saas-valuation-compression
```

See the [main README](../../README.md) for more installation options.
