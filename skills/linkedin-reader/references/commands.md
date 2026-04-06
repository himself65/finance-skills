# opencli LinkedIn Command Reference (Read-Only)

Complete read-only reference for LinkedIn commands in [opencli](https://github.com/jackwener/opencli), scoped to financial research use cases.

Install: `npm install -g @jackwener/opencli`

**This skill is read-only.** Write operations (posting, liking, commenting, connecting, messaging) are NOT supported in this finance skill.

---

## Setup

opencli authenticates via your existing Chrome browser session — no API keys or credentials needed.

**Requirements:**
1. Chrome with the Browser Bridge extension installed
2. Logged into linkedin.com in Chrome

**Verify setup:**
```bash
opencli doctor
```

This auto-starts the daemon, verifies extension connectivity, and checks browser session health.

---

## Read Operations

### Timeline (Home Feed)

Reads posts from your LinkedIn home feed by scrolling and extracting visible posts.

```bash
opencli linkedin timeline                         # Last 20 posts (default)
opencli linkedin timeline --limit 50              # Up to 50 posts (max 100)
opencli linkedin timeline -f json                 # JSON output
opencli linkedin timeline -f yaml                 # YAML output
opencli linkedin timeline -f csv                  # CSV output
```

**Output columns:** `rank`, `author`, `author_url`, `headline`, `text`, `posted_at`, `reactions`, `comments`, `url`

### Job Search

Searches LinkedIn job listings by keyword with optional filters.

```bash
opencli linkedin search "keyword"                 # Basic job search (10 results)
opencli linkedin search "quantitative analyst" --limit 20        # More results
opencli linkedin search "trader" --location "Chicago" -f json    # Filter by location
opencli linkedin search "financial analyst" --details -f json    # Full descriptions

# Filter by experience level
opencli linkedin search "portfolio manager" --experience-level mid-senior -f json

# Filter by job type
opencli linkedin search "risk analyst" --job-type full-time -f json

# Filter by work mode
opencli linkedin search "data scientist finance" --remote remote -f json

# Filter by date posted
opencli linkedin search "hedge fund" --date-posted week -f json

# Combine filters
opencli linkedin search "investment banking" \
  --location "New York" \
  --experience-level associate \
  --job-type full-time \
  --date-posted month \
  --details \
  --limit 20 \
  -f json
```

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--location` | string | — | Geographic area (e.g., "San Francisco Bay Area") |
| `--limit` | integer | 10 | Number of results (max 100) |
| `--start` | integer | 0 | Pagination offset |
| `--details` | boolean | false | Include full job descriptions and apply URLs |
| `--company` | string | — | Comma-separated company names or LinkedIn IDs |
| `--experience-level` | string | — | `internship`, `entry`, `associate`, `mid-senior`, `director`, `executive` |
| `--job-type` | string | — | `full-time`, `part-time`, `contract`, `temporary`, `volunteer`, `internship`, `other` |
| `--date-posted` | string | — | `any`, `month`, `week`, `24h` |
| `--remote` | string | — | `on-site`, `hybrid`, `remote` |

**Output columns:** `rank`, `title`, `company`, `location`, `listed`, `salary`, `url`

With `--details`: also `description`, `apply_url`

---

## Output Formats

All commands support the `-f` / `--format` flag:

| Format | Flag | Description |
|---|---|---|
| Table | `-f table` (default) | Rich CLI table with bold headers, word wrapping, footer with count/elapsed time |
| JSON | `-f json` | Pretty-printed JSON (2-space indent) |
| YAML | `-f yaml` | Structured YAML |
| Markdown | `-f md` | Pipe-delimited markdown tables |
| CSV | `-f csv` | Comma-separated values with proper quoting/escaping |

---

## Financial Research Workflows

### Read professional market commentary

```bash
# Read your LinkedIn feed for analyst posts and market takes
opencli linkedin timeline --limit 30 -f json
```

### Search for finance industry jobs

```bash
# Quantitative roles
opencli linkedin search "quantitative analyst" --location "New York" --details --limit 15 -f json
opencli linkedin search "quant trader" --experience-level mid-senior --limit 10 -f json

# Portfolio management
opencli linkedin search "portfolio manager" --job-type full-time --limit 15 -f json

# Risk and compliance
opencli linkedin search "risk analyst" --date-posted week --limit 10 -f json
opencli linkedin search "compliance officer fintech" --limit 10 -f json
```

### Track hiring trends at specific companies

```bash
opencli linkedin search "analyst" --company "Goldman Sachs" --limit 20 -f json
opencli linkedin search "engineer" --company "Citadel,Two Sigma,Jane Street" --limit 20 -f json
```

### Remote finance opportunities

```bash
opencli linkedin search "financial analyst" --remote remote --limit 20 -f json
opencli linkedin search "data scientist trading" --remote hybrid --location "Chicago" --limit 10 -f json
```

### Entry-level finance positions

```bash
opencli linkedin search "investment banking analyst" --experience-level entry --date-posted month --limit 15 -f json
opencli linkedin search "junior trader" --experience-level entry --limit 10 -f json
```

### Export for analysis

```bash
# CSV for spreadsheet analysis
opencli linkedin search "hedge fund" --limit 50 -f csv > hedge_fund_jobs.csv

# JSON for programmatic processing
opencli linkedin timeline --limit 30 -f json > linkedin_feed.json
```

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `Extension not connected` | Browser Bridge not installed | Install the Browser Bridge Chrome extension |
| `Daemon not running` | opencli daemon not started | Run `opencli doctor` to auto-start |
| `No session for linkedin.com` | Not logged into linkedin.com | Login to linkedin.com in Chrome |
| `AuthRequiredError` | Login wall detected, session expired | Refresh linkedin.com and log in again |
| `EmptyResultError` | No results found | Broaden search terms or check feed content |
| Rate limited | Too many requests | Wait a few minutes, then retry |

---

## Limitations

- **Read-only in this skill** — write operations are not supported for finance use
- **No profile lookups** — individual user/company profile viewing is not yet supported
- **No messaging** — LinkedIn messages/InMail are not accessible
- **No connection management** — cannot view, send, or manage connection requests
- **No notifications** — LinkedIn notifications are not exposed
- **Job search only** — search is scoped to job listings, not posts or people
- **Requires Chrome** — opencli uses Chrome's Browser Bridge; other browsers are not supported
- **Single browser profile** — uses the active Chrome profile's session

---

## Best Practices

- **Keep request volumes low** — use `--limit 20` instead of `--limit 100`
- **Use `opencli doctor`** before your first command in a session to verify connectivity
- **Use `-f json`** for programmatic processing and LLM context
- **Use `-f csv`** when the user wants to analyze data in a spreadsheet
- **Use `--details`** only when you need full job descriptions — it's slower since it fetches each listing individually
- **Use `--date-posted week` or `--date-posted 24h`** for time-sensitive job market research
