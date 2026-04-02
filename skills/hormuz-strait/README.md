# hormuz-strait

Real-time Strait of Hormuz monitoring for energy market and geopolitical risk research via the [Hormuz Strait Monitor](https://hormuzstraitmonitor.com) dashboard API.

## What it does

Fetches the current status of the Strait of Hormuz and presents a risk briefing covering:

- **Strait status** — open, restricted, or closed, with duration and description
- **Ship traffic** — current transits, 24h count, and percent of normal baseline
- **Oil price impact** — Brent crude price with 24h change and trend
- **Stranded vessels** — count by type (tankers, bulk, other) with daily change
- **Insurance risk** — war risk premium level, percentage, and multiplier vs. normal
- **Cargo throughput** — daily DWT vs. average with 7-day trend
- **Diplomatic status** — current situation, parties involved, and headline
- **Global trade impact** — percent of world oil/LNG at risk, daily cost, affected regions, alternative routes, and supply chain disruption
- **Crisis timeline** — chronological events (military, diplomatic, economic)
- **Latest news** — recent articles with sources and links

**This skill is read-only.** No authentication required — uses the public dashboard API.

## Triggers

- "Hormuz status", "Strait of Hormuz", "is Hormuz open"
- "shipping through the Gulf", "Persian Gulf tanker traffic"
- "oil chokepoint", "war risk premium", "Hormuz crisis"
- "energy supply chain risk", "oil transit disruption", "Middle East shipping"
- Any mention of Hormuz or Persian Gulf in context of oil, shipping, or geopolitical risk

## Platform

Works on **all platforms** (Claude Code, Claude.ai, and other agents). Only requires `curl` for the API call.

## Setup

```bash
# As a plugin (recommended — installs all skills)
npx plugins add himself65/finance-skills

# Or install just this skill
npx skills add himself65/finance-skills --skill hormuz-strait
```

See the [main README](../../README.md) for more installation options.

## Reference files

- `references/api_schema.md` — Complete API response schema with field descriptions and data types
