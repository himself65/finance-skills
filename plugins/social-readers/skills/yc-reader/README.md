# yc-reader

Read-only Y Combinator company data skill using the [yc-oss/api](https://github.com/yc-oss/api).

## What it does

Fetches Y Combinator company data for startup and venture research — company profiles, batch listings, industry/tag breakdowns, hiring status, and diversity data. Capabilities include:

- **Company collections** — top companies, all companies, currently hiring, non-profits, diversity data
- **Batch lookup** — companies by YC batch (e.g., Winter 2025, Summer 2024)
- **Industry filter** — companies by industry (fintech, healthcare, B2B, etc.)
- **Tag filter** — companies by tag (AI, developer tools, SaaS, climate, etc.)
- **Metadata** — overall YC stats, valid batch/industry/tag names
- **Client-side search** — find companies by name or description via jq filters

**This is a read-only data source.** The API serves static JSON files — no write operations exist.

## Authentication

None required. The API is public and free — just `curl` the endpoints.

## Triggers

- "YC companies in fintech", "top Y Combinator companies", "latest YC batch"
- "YC startups hiring", "find YC companies tagged AI", "W25 batch"
- "Y Combinator portfolio", "startup research", "which YC companies do X"
- Any mention of Y Combinator or YC in context of startup/venture research

## Platform

Works on **Claude Code** and other CLI-based agents. Does **not** work on Claude.ai — the sandbox restricts network access required for API calls.

## Setup

```bash
# As a plugin (recommended — installs all skills)
npx plugins add himself65/finance-skills --plugin finance-social-readers

# Or install just this skill
npx skills add himself65/finance-skills --skill yc-reader
```

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- `curl` (pre-installed on macOS and most Linux)
- `jq` (for JSON filtering — `brew install jq` or `apt-get install jq`)

## Reference files

- `references/api_reference.md` — Complete endpoint reference with company schema, all URLs, and research workflow examples
