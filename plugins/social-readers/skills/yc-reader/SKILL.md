---
name: yc-reader
description: >
  Look up Y Combinator companies and batches from the public yc-oss API, a static JSON
  dataset refreshed daily: company profiles, batch rosters (e.g. W25, S24), companies
  by industry or tag, top companies, who is hiring, founder-diversity lists, and
  overall YC stats. Use this skill whenever the user asks about YC-backed startups, a
  YC batch, YC companies in a sector or tag or that are hiring, the Y Combinator
  portfolio, or startup and venture research that draws on YC data. Read-only.
---

# Y Combinator Reader (Read-Only)

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Fetches Y Combinator company data from the [yc-oss/api](https://github.com/yc-oss/api), an unofficial open-source API that indexes all publicly launched YC companies. The data is sourced from YC's Algolia search index and updated daily via GitHub Actions.

**This is a read-only data source.** It provides company profiles, batch listings, industry/tag breakdowns, hiring status, and diversity data. No write operations exist — the API serves static JSON files.

**No authentication required.** The API is public and free. Just use `curl` to fetch JSON endpoints.

---

## Step 1: Verify Prerequisites

This skill only needs `curl` (to fetch data) and `jq` (to parse/filter JSON). Both are pre-installed on most systems.

```
!`(command -v curl > /dev/null && echo "CURL_OK" || echo "CURL_MISSING") && (command -v jq > /dev/null && echo "JQ_OK" || echo "JQ_MISSING")`
```

If `JQ_MISSING`, install it:

```bash
# macOS
brew install jq

# Linux (Debian/Ubuntu)
sudo apt-get install jq
```

If `jq` is unavailable, you can still fetch raw JSON with `curl` and parse it inline with Python or other tools — but `jq` makes filtering much easier.

---

## Step 2: Identify What the User Needs

Match the user's request to the appropriate endpoint. See `references/api_reference.md` for full details.

| User Request | Endpoint | Notes |
|---|---|---|
| Overall YC stats | `meta.json` | Company count, batch list, industry/tag lists |
| All companies | `companies/all.json` | Full dataset (~5,700 companies) — large response |
| Top companies | `companies/top.json` | ~91 top-performing YC companies |
| Companies hiring | `companies/hiring.json` | ~1,400 currently hiring |
| Non-profit companies | `companies/nonprofit.json` | YC-backed non-profits |
| Diversity data | `companies/black-founded.json`, `hispanic-latino-founded.json`, `women-founded.json` | Founder diversity |
| Specific batch | `batches/{batch-name}.json` | e.g., `winter-2026.json`, `spring-2026.json`, `fall-2025.json` |
| Single company profile | `batches/{batch-name}/{slug}.json` | e.g., `batches/summer-2009/stripe.json`, `batches/winter-2009/airbnb.json` |
| By industry | `industries/{industry}.json` | e.g., `fintech.json`, `healthcare.json` |
| By tag | `tags/{tag}.json` | e.g., `ai.json`, `developer-tools.json` |

### Batch name format

Batches use `{season}-{year}` format: `winter-2026`, `spring-2026`, `summer-2026`, `fall-2025`. Older batches follow the same pattern back to `summer-2005`. The short form (`w09`, `s21`) also works for the per-company endpoint.

### Industry and tag name format

Use lowercase with hyphens for multi-word names: `real-estate`, `developer-tools`, `machine-learning`.

---

## Step 3: Execute the Request

### Base URL

```
https://yc-oss.github.io/api/
```

### General pattern

```bash
# Fetch and pretty-print
curl -s https://yc-oss.github.io/api/companies/top.json | jq .

# Count companies in a result
curl -s https://yc-oss.github.io/api/batches/winter-2025.json | jq length

# Filter by field (e.g., hiring companies in a batch)
curl -s https://yc-oss.github.io/api/batches/winter-2025.json | jq '[.[] | select(.isHiring == true)]'

# Extract specific fields
curl -s https://yc-oss.github.io/api/companies/top.json | jq '.[] | {name, one_liner, batch, team_size, website}'

# Search by name (case-insensitive)
curl -s https://yc-oss.github.io/api/companies/all.json | jq '[.[] | select(.name | test("stripe"; "i"))]'
```

### Key rules

1. **Use `-s` flag** with curl to suppress progress output
2. **Pipe through `jq`** for readable output and filtering
3. **Avoid fetching `companies/all.json` unless necessary** — it's a large response (~5,700 companies). Prefer more specific endpoints (batches, industries, tags) when possible
4. **Use `jq` select/filter** to narrow results client-side when the API doesn't have a specific endpoint for what the user wants
5. **Batch names are lowercase with hyphens** — `winter-2025` not `Winter 2025` or `W25`
6. **Tag and industry names are lowercase with hyphens** — `developer-tools` not `Developer Tools`

### Common jq filters

| Filter | Purpose |
|---|---|
| `jq length` | Count results |
| `jq '.[0]'` | First company |
| `jq '.[:10]'` | First 10 companies |
| `jq '[.[] \| select(.isHiring == true)]'` | Only hiring companies |
| `jq '[.[] \| select(.status == "Active")]'` | Only active companies |
| `jq '[.[] \| select(.team_size > 100)]'` | Companies with 100+ employees |
| `jq '.[] \| {name, one_liner, batch, website}'` | Select specific fields |
| `jq '[.[] \| select(.name \| test("query"; "i"))]'` | Search by name |
| `jq 'sort_by(-.team_size) \| .[:10]'` | Top 10 by team size |

---

## Step 4: Present the Results

Summarize rather than dump JSON. For each company, give the name, one-liner, batch, team size, status, hiring status (a growth signal), and website. For a batch, lead with its size and notable companies; for an industry or tag, the count and which companies are top or hiring; for research questions, aggregate stats such as counts, common industries, and team-size distribution. Mention that the dataset refreshes daily.

---

## Step 5: Diagnostics

If a request fails:

| Error | Cause | Fix |
|-------|-------|-----|
| `404 Not Found` | Invalid batch, industry, or tag name | Check `meta.json` for valid names |
| Empty array `[]` | No companies match the query | Broaden the search or check spelling |
| `curl: Could not resolve host` | No internet connection | Check network connectivity |
| Large/slow response | Fetching `companies/all.json` (5,700+ entries) | Use a more specific endpoint or add `jq` filters |

To discover valid batch, industry, and tag names:

```bash
# List all batches
curl -s https://yc-oss.github.io/api/meta.json | jq '.batches[].name'

# List all industries
curl -s https://yc-oss.github.io/api/meta.json | jq '.industries[].name'

# List all tags (there are 333+)
curl -s https://yc-oss.github.io/api/meta.json | jq '.tags[].name'
```

---

## Reference Files

- `references/api_reference.md` — Complete endpoint reference with company schema, all endpoint URLs, and research workflow examples

Read the reference file when you need the exact company field schema, valid batch/industry/tag names, or detailed research workflow patterns.
