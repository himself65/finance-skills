---
name: linkedin-reader
description: >
  Read LinkedIn for financial research using opencli (read-only).
  Use this skill whenever the user wants to read their LinkedIn feed, search for jobs
  in the finance/trading industry, view professional posts about markets or earnings,
  or gather professional sentiment from LinkedIn.
  Triggers include: "check my LinkedIn feed", "search LinkedIn for", "LinkedIn posts about",
  "what's on LinkedIn about AAPL", "finance jobs on LinkedIn", "LinkedIn market sentiment",
  "who's posting about earnings on LinkedIn", "LinkedIn feed", "professional network buzz",
  "what are analysts saying on LinkedIn", any mention of LinkedIn in context
  of reading financial news, market research, job searches, or professional commentary.
  This skill is READ-ONLY — it does NOT support posting, liking, commenting, connecting, or any write operations.
---

# LinkedIn Skill (Read-Only)

Reads LinkedIn for financial research using [opencli](https://github.com/jackwener/opencli), a universal CLI tool that bridges web services to the terminal via browser session reuse.

**This skill is read-only.** It is designed for financial research: reading professional commentary on markets, monitoring analyst posts, searching finance/trading jobs, and tracking professional sentiment. It does NOT support posting, liking, commenting, connecting, messaging, or any write operations.

**Important**: opencli reuses your existing Chrome login session — no API keys or cookie extraction needed. Just be logged into linkedin.com in Chrome and have the Browser Bridge extension installed.

---

## Step 1: Ensure opencli Is Installed and Ready

**Current environment status:**

```
!`(command -v opencli && opencli doctor 2>&1 | head -5 && echo "READY" || echo "SETUP_NEEDED") 2>/dev/null || echo "NOT_INSTALLED"`
```

If the status above shows `READY`, skip to Step 2. If `NOT_INSTALLED`, install first:

```bash
# Install opencli globally
npm install -g @jackwener/opencli
```

If `SETUP_NEEDED`, guide the user through setup:

### Setup

opencli requires Node.js >= 21 and a Chrome browser with the Browser Bridge extension:

1. **Install the Browser Bridge extension:**
   - Download the latest `opencli-extension-v{version}.zip` from the [GitHub Releases page](https://github.com/jackwener/opencli/releases)
   - Unzip it, open `chrome://extensions` in Chrome, and enable **Developer mode**
   - Click **Load unpacked** and select the unzipped folder
2. **Login to linkedin.com** in Chrome — opencli reuses your existing browser session
3. **Verify connectivity:**

```bash
opencli doctor
```

This auto-starts the daemon, verifies the extension is connected, and checks session health.

### Common setup issues

| Symptom | Fix |
|---------|-----|
| `Extension not connected` | Install Browser Bridge extension in Chrome and ensure it's enabled |
| `Daemon not running` | Run `opencli doctor` — it auto-starts the daemon |
| `No session for linkedin.com` | Login to linkedin.com in Chrome, then retry |
| `AuthRequiredError` | LinkedIn session expired — refresh linkedin.com in Chrome and log in again |

---

## Step 2: Identify What the User Needs

Match the user's request to one of the read commands below, then use the corresponding command from `references/commands.md`.

| User Request | Command | Key Flags |
|---|---|---|
| Setup check | `opencli doctor` | — |
| Home feed / posts | `opencli linkedin timeline` | `--limit N` (default 20, max 100) |
| Search for jobs | `opencli linkedin search "QUERY"` | `--location`, `--limit N` (default 10, max 100), `--details` |
| Finance job search | `opencli linkedin search "QUERY"` | `--experience-level`, `--job-type`, `--remote`, `--company`, `--date-posted`, `--start` |

---

## Step 3: Execute the Command

### General pattern

```bash
# Read LinkedIn feed posts
opencli linkedin timeline --limit 20 -f json

# Search for finance/trading jobs
opencli linkedin search "quantitative analyst" --limit 10 -f json
opencli linkedin search "portfolio manager" --location "New York" --limit 15 -f json

# Detailed job listings with descriptions
opencli linkedin search "financial analyst" --details --limit 10 -f json
```

### Key rules

1. **Check setup first** — run `opencli doctor` before any other command if unsure about connectivity
2. **Use `-f json` or `-f yaml`** for structured output when processing data programmatically
3. **Use `-f csv`** when the user wants spreadsheet-compatible output
4. **Use `--limit N`** to control result count — start with 10-20 unless the user asks for more
5. **For job search, use filters** — `--location`, `--experience-level`, `--job-type`, `--remote`, `--date-posted` to narrow results
6. **NEVER execute write operations** — this skill is read-only; do not post, like, comment, connect, message, or apply to jobs

### Output format flag (`-f`)

| Format | Flag | Best for |
|---|---|---|
| Table | `-f table` (default) | Human-readable terminal output |
| JSON | `-f json` | Programmatic processing, LLM context |
| YAML | `-f yaml` | Structured output, readable |
| Markdown | `-f md` | Documentation, reports |
| CSV | `-f csv` | Spreadsheet export |

### Output columns

**Timeline** posts include: `rank`, `author`, `author_url`, `headline`, `text`, `posted_at`, `reactions`, `comments`, `url`.

**Job search** results include: `rank`, `title`, `company`, `location`, `listed`, `salary`, `url`. With `--details`: also `description`, `apply_url`.

---

## Step 4: Present the Results

After fetching data, present it clearly for financial research:

1. **Summarize key content** — highlight the most relevant posts or jobs for the user's research
2. **Include attribution** — show author name, headline, post text, and engagement (reactions, comments)
3. **Provide URLs** when the user might want to read the full post or job listing
4. **For feed posts**, highlight market commentary, analyst takes, earnings reactions, and professional sentiment
5. **For job search results**, present title, company, location, salary (when available), and posting date
6. **Flag sentiment** — note bullish/bearish professional sentiment, consensus vs contrarian views
7. **Treat sessions as private** — never expose browser session details

---

## Step 5: Diagnostics

If something isn't working, run:

```bash
opencli doctor
```

This checks daemon status, extension connectivity, and browser session health.

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `Extension not connected` | Browser Bridge not installed/enabled | Install extension and enable it in Chrome |
| `No session` | Not logged into linkedin.com | Login to linkedin.com in Chrome |
| `AuthRequiredError` | LinkedIn login wall detected | Refresh linkedin.com and log in again |
| `EmptyResultError` | No results found for query | Broaden search terms or check feed has content |
| Rate limited | Too many requests | Wait a few minutes, then retry |

---

## Reference Files

- `references/commands.md` — Complete read command reference with all flags, research workflows, and usage examples

Read the reference file when you need exact command syntax, research workflow patterns, or output details.
