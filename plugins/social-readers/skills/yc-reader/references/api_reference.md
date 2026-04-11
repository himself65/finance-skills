# yc-oss API Reference

Complete reference for the [yc-oss/api](https://github.com/yc-oss/api), an unofficial open-source API indexing all publicly launched Y Combinator companies.

**Base URL:** `https://yc-oss.github.io/api/`

**Authentication:** None required — all endpoints are public.

**Format:** Static JSON files, updated daily via GitHub Actions.

---

## Company Schema

Each company object contains:

| Field | Type | Description |
|---|---|---|
| `id` | number | Internal ID |
| `name` | string | Company name |
| `slug` | string | URL-safe identifier |
| `former_names` | string[] | Previous company names |
| `small_logo_thumb_url` | string | Logo thumbnail URL |
| `website` | string | Company website URL |
| `all_locations` | string | Comma-separated locations |
| `long_description` | string | Full company description |
| `one_liner` | string | One-line summary |
| `team_size` | number | Current team size |
| `industry` | string | Primary industry |
| `subindustry` | string | Sub-industry classification |
| `launched_at` | number | Unix timestamp of YC launch |
| `tags` | string[] | Category tags |
| `tags_highlighted` | string[] | Featured tags |
| `top_company` | boolean | Whether it's a top YC company |
| `isHiring` | boolean | Currently hiring |
| `nonprofit` | boolean | Non-profit organization |
| `batch` | string | YC batch (e.g., "W25", "S24") |
| `status` | string | Company status ("Active", "Acquired", "Inactive", "Public") |
| `industries` | string[] | All industry classifications |
| `regions` | string[] | Geographic regions |
| `stage` | string | Company stage |
| `url` | string | YC profile URL (ycombinator.com) |
| `api` | string | API endpoint URL for this company |

---

## Endpoints

### Metadata

```bash
curl -s https://yc-oss.github.io/api/meta.json | jq .
```

Returns overall statistics: total company count, list of all batches (with counts), all industries (with counts), and all tags (with counts). Use this to discover valid batch/industry/tag names.

### Company Collections

| Endpoint | Description | Approx. Count |
|---|---|---|
| `companies/all.json` | All launched companies | ~5,700 |
| `companies/top.json` | Top-performing companies | ~91 |
| `companies/hiring.json` | Currently hiring | ~1,400 |
| `companies/nonprofit.json` | Non-profit organizations | ~42 |
| `companies/black-founded.json` | Black-founded companies | varies |
| `companies/hispanic-latino-founded.json` | Hispanic/Latino-founded | varies |
| `companies/women-founded.json` | Women-founded companies | varies |

```bash
# Top YC companies
curl -s https://yc-oss.github.io/api/companies/top.json | jq '.[:5] | .[] | {name, one_liner, batch, team_size}'

# Currently hiring
curl -s https://yc-oss.github.io/api/companies/hiring.json | jq length
```

### Batches

Pattern: `batches/{season}-{year}.json`

Seasons: `winter`, `summer`, `fall`

```bash
# Winter 2025 batch
curl -s https://yc-oss.github.io/api/batches/winter-2025.json | jq length

# Summer 2024 batch
curl -s https://yc-oss.github.io/api/batches/summer-2024.json | jq '.[:5] | .[] | {name, one_liner}'

# Fall 2025 batch
curl -s https://yc-oss.github.io/api/batches/fall-2025.json | jq .
```

Historical batches go back to `summer-2005`.

### Industries

Pattern: `industries/{industry-name}.json`

Use lowercase with hyphens for multi-word names.

**Notable industries:**

| Industry | Endpoint | Approx. Count |
|---|---|---|
| B2B | `industries/b2b.json` | ~2,876 |
| Consumer | `industries/consumer.json` | ~866 |
| Healthcare | `industries/healthcare.json` | ~656 |
| Fintech | `industries/fintech.json` | ~607 |
| Engineering/Product/Design | `industries/engineering-product-and-design.json` | ~585 |
| Real Estate & Construction | `industries/real-estate-and-construction.json` | ~138 |
| Government | `industries/government.json` | ~75 |
| Education | `industries/education.json` | ~240 |
| Infrastructure | `industries/infrastructure.json` | ~261 |

```bash
# Fintech companies
curl -s https://yc-oss.github.io/api/industries/fintech.json | jq '.[:10] | .[] | {name, one_liner, batch, isHiring}'

# Healthcare companies hiring
curl -s https://yc-oss.github.io/api/industries/healthcare.json | jq '[.[] | select(.isHiring == true)] | length'
```

### Tags

Pattern: `tags/{tag-name}.json`

Use lowercase with hyphens for multi-word names.

**Notable tags:**

| Tag | Endpoint | Approx. Count |
|---|---|---|
| SaaS | `tags/saas.json` | ~1,127 |
| Artificial Intelligence | `tags/artificial-intelligence.json` | ~908 |
| AI | `tags/ai.json` | ~772 |
| Developer Tools | `tags/developer-tools.json` | ~537 |
| Marketplace | `tags/marketplace.json` | ~347 |
| Open Source | `tags/open-source.json` | ~179 |
| Climate | `tags/climate.json` | ~142 |
| Crypto/Web3 | `tags/crypto-web3.json` | ~119 |
| Robotics | `tags/robotics.json` | ~78 |
| Automation | `tags/automation.json` | ~85 |

```bash
# AI-tagged companies
curl -s https://yc-oss.github.io/api/tags/ai.json | jq '.[:10] | .[] | {name, one_liner, batch}'

# Developer tools that are hiring
curl -s https://yc-oss.github.io/api/tags/developer-tools.json | jq '[.[] | select(.isHiring == true)] | .[:10] | .[] | {name, one_liner, website}'
```

---

## Research Workflows

### Analyze the latest YC batch

```bash
# Get batch companies
curl -s https://yc-oss.github.io/api/batches/winter-2025.json | jq length

# Summarize by industry
curl -s https://yc-oss.github.io/api/batches/winter-2025.json | jq 'group_by(.industry) | map({industry: .[0].industry, count: length}) | sort_by(-.count)'

# Find hiring companies in the batch
curl -s https://yc-oss.github.io/api/batches/winter-2025.json | jq '[.[] | select(.isHiring == true)] | .[] | {name, one_liner, website}'
```

### Find fintech/finance startups

```bash
# All fintech companies
curl -s https://yc-oss.github.io/api/industries/fintech.json | jq '.[:20] | .[] | {name, one_liner, batch, team_size, status}'

# Active fintech companies that are hiring
curl -s https://yc-oss.github.io/api/industries/fintech.json | jq '[.[] | select(.isHiring == true and .status == "Active")] | .[:15] | .[] | {name, one_liner, batch, team_size, website}'
```

### Track hiring trends (growth signal)

```bash
# Largest hiring companies
curl -s https://yc-oss.github.io/api/companies/hiring.json | jq 'sort_by(-.team_size) | .[:20] | .[] | {name, team_size, industry, batch}'

# Hiring companies in AI
curl -s https://yc-oss.github.io/api/tags/ai.json | jq '[.[] | select(.isHiring == true)] | sort_by(-.team_size) | .[:15] | .[] | {name, team_size, one_liner}'
```

### Search for a specific company

```bash
# Search by name (case-insensitive)
curl -s https://yc-oss.github.io/api/companies/all.json | jq '[.[] | select(.name | test("stripe"; "i"))]'

# Search in one-liners
curl -s https://yc-oss.github.io/api/companies/all.json | jq '[.[] | select(.one_liner | test("payment"; "i"))] | .[:10] | .[] | {name, one_liner, batch}'
```

### Top companies analysis

```bash
# Top companies with details
curl -s https://yc-oss.github.io/api/companies/top.json | jq '.[] | {name, one_liner, batch, team_size, status, industry}'

# Top companies by team size
curl -s https://yc-oss.github.io/api/companies/top.json | jq 'sort_by(-.team_size) | .[:10] | .[] | {name, team_size, batch}'
```

### Diversity data

```bash
# Women-founded companies in latest batch
curl -s https://yc-oss.github.io/api/companies/women-founded.json | jq '[.[] | select(.batch == "W25")] | .[] | {name, one_liner}'

# Count by diversity category
curl -s https://yc-oss.github.io/api/companies/black-founded.json | jq length
curl -s https://yc-oss.github.io/api/companies/women-founded.json | jq length
```

### Export for analysis

```bash
# CSV export (name, batch, industry, team_size, status)
curl -s https://yc-oss.github.io/api/companies/top.json | jq -r '.[] | [.name, .batch, .industry, .team_size, .status] | @csv' > yc_top.csv

# JSON subset for processing
curl -s https://yc-oss.github.io/api/industries/fintech.json | jq '[.[] | {name, one_liner, batch, team_size, website, isHiring}]' > fintech_yc.json
```

---

## Discovering Valid Names

When the user asks for a batch, industry, or tag that you're not sure about, query `meta.json`:

```bash
# List all batch names
curl -s https://yc-oss.github.io/api/meta.json | jq '[.batches[] | .name]'

# List all industry names
curl -s https://yc-oss.github.io/api/meta.json | jq '[.industries[] | .name]'

# List all tag names (333+)
curl -s https://yc-oss.github.io/api/meta.json | jq '[.tags[] | .name]'

# Search for a tag name
curl -s https://yc-oss.github.io/api/meta.json | jq '[.tags[] | select(.name | test("fintech"; "i"))]'
```

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `404 Not Found` | Invalid endpoint name | Check `meta.json` for valid batch/industry/tag names |
| Empty array `[]` | No companies match filter | Broaden the jq filter or check spelling |
| Network error | No internet connection | Check connectivity |
| Large/slow response | `companies/all.json` is ~5,700 entries | Use specific endpoints (batch, industry, tag) or pipe through `jq '.[:N]'` to limit |

---

## Limitations

- **Read-only** — Static JSON files, no search API or query parameters
- **No individual company endpoint** — To look up one company, search `companies/all.json` by name
- **No founder details** — Company profiles don't include individual founder names or bios
- **No funding data** — Funding amounts, valuations, and investor details are not included
- **No revenue/financial data** — Only public metadata (team size, hiring status, industry)
- **Updated daily** — Data may be up to 24 hours behind YC's live directory
- **Publicly launched only** — Stealth companies not yet launched on YC are excluded
