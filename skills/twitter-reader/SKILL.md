---
name: twitter-reader
description: >
  Read Twitter/X for financial research using opencli (read-only).
  Use this skill whenever the user wants to read their Twitter feed, search for financial tweets,
  view bookmarks, look up user profiles, or gather market sentiment from Twitter/X.
  Triggers include: "check my feed", "search Twitter for", "show my bookmarks",
  "who follows", "look up @user", "what's trending about", "market sentiment on Twitter",
  "what are people saying about AAPL", "fintwit", any mention of Twitter/X in context
  of reading financial news or market research.
  This skill is READ-ONLY — it does NOT support posting, liking, retweeting, or any write operations.
---

# Twitter Skill (Read-Only)

Reads Twitter/X for financial research using [opencli](https://github.com/jackwener/opencli), a universal CLI tool that bridges web services to the terminal via browser session reuse.

**This skill is read-only.** It is designed for financial research: searching market discussions, reading analyst tweets, tracking sentiment, and monitoring financial news on Twitter/X. It does NOT support posting, liking, retweeting, replying, or any write operations.

**Important**: opencli reuses your existing Chrome login session — no API keys or cookie extraction needed. Just be logged into x.com in Chrome and have the Browser Bridge extension installed.

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

opencli requires a Chrome browser with the Browser Bridge extension:

1. **Install the Browser Bridge extension** — follow the instructions from `opencli doctor` output
2. **Login to x.com** in Chrome — opencli reuses your existing browser session
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
| `No session for twitter.com` | Login to x.com in Chrome, then retry |
| `CSRF token missing` | Refresh x.com in Chrome to regenerate the ct0 cookie |

---

## Step 2: Identify What the User Needs

Match the user's request to one of the read commands below, then use the corresponding command from `references/commands.md`.

| User Request | Command | Key Flags |
|---|---|---|
| Setup check | `opencli doctor` | — |
| Home feed / timeline | `opencli twitter timeline` | `--type following`, `--limit N` |
| Search tweets | `opencli twitter search "QUERY"` | `--filter top\|live`, `--limit N` |
| Trending topics | `opencli twitter trending` | `--limit N` |
| Bookmarks | `opencli twitter bookmarks` | `--limit N` |
| View a specific thread | `opencli twitter thread TWEET_ID` | — |
| Twitter article | `opencli twitter article TWEET_ID` | — |
| User profile | `opencli twitter profile USERNAME` | — |
| Followers | `opencli twitter followers USERNAME` | `--limit N` |
| Following | `opencli twitter following USERNAME` | `--limit N` |
| Notifications | `opencli twitter notifications` | `--limit N` |

---

## Step 3: Execute the Command

### General pattern

```bash
# Use -f json or -f yaml for structured output
opencli twitter timeline -f json --limit 20
opencli twitter timeline --type following --limit 20

# Searching for financial topics
opencli twitter search "$AAPL earnings" --filter live --limit 10 -f json
opencli twitter search "Fed rate decision" --limit 20 -f yaml

# Trending topics
opencli twitter trending --limit 20 -f json
```

### Key rules

1. **Check setup first** — run `opencli doctor` before any other command if unsure about connectivity
2. **Use `-f json` or `-f yaml`** for structured output when processing data programmatically
3. **Use `-f csv`** when the user wants spreadsheet-compatible output
4. **Use `--limit N`** to control result count — start with 10-20 unless the user asks for more
5. **For search, use `--filter`** — `top` (default) for relevance, `live` for latest tweets
6. **NEVER execute write operations** — this skill is read-only; do not post, like, retweet, reply, quote, follow, or delete

### Output format flag (`-f`)

| Format | Flag | Best for |
|---|---|---|
| Table | `-f table` (default) | Human-readable terminal output |
| JSON | `-f json` | Programmatic processing, LLM context |
| YAML | `-f yaml` | Structured output, readable |
| Markdown | `-f md` | Documentation, reports |
| CSV | `-f csv` | Spreadsheet export |

### Output columns

Commands that return tweets typically include: `id`, `author`, `text`, `created_at`, `likes`, `views`, `url`.

Profile commands include: `username`, `name`, `bio`, `followers_count`, `following_count`.

---

## Step 4: Present the Results

After fetching data, present it clearly for financial research:

1. **Summarize key content** — highlight the most relevant tweets for the user's financial research
2. **Include attribution** — show @username, tweet text, and engagement metrics (likes, views)
3. **Provide tweet URLs** when the user might want to read the full thread
4. **For search results**, group by relevance and highlight key themes, sentiment, or market signals
5. **For user profiles**, present follower count, bio, and notable recent activity
6. **Flag sentiment** — note bullish/bearish sentiment, consensus vs contrarian views
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
| `No session` | Not logged into x.com | Login to x.com in Chrome |
| `CSRF token missing` | Cookie expired or page needs refresh | Refresh x.com in Chrome |
| Rate limited | Too many requests | Wait a few minutes, then retry |

---

## Reference Files

- `references/commands.md` — Complete read command reference with all flags, research workflows, and usage examples
- `references/schema.md` — Output format documentation and column definitions

Read the reference files when you need exact command syntax, research workflow patterns, or output details.
