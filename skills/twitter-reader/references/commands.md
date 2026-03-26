# opencli Twitter Command Reference (Read-Only)

Complete read-only reference for Twitter commands in [opencli](https://github.com/jackwener/opencli), scoped to financial research use cases.

Install: `npm install -g @jackwener/opencli`

**This skill is read-only.** Write operations (post, like, retweet, reply, quote, follow, delete) are NOT supported in this finance skill.

---

## Setup

opencli authenticates via your existing Chrome browser session — no API keys or credentials needed.

**Requirements:**
1. Chrome with the Browser Bridge extension installed
2. Logged into x.com in Chrome

**Verify setup:**
```bash
opencli doctor
```

This auto-starts the daemon, verifies extension connectivity, and checks browser session health.

---

## Read Operations

### Timeline (Home Feed)

```bash
opencli twitter timeline                          # "For You" feed (default)
opencli twitter timeline --type following          # "Following" tab
opencli twitter timeline --limit 50               # Limit count
opencli twitter timeline -f json                  # JSON output
opencli twitter timeline -f yaml                  # YAML output
```

### Search

```bash
opencli twitter search "keyword"                  # Basic search (top results)
opencli twitter search "AI agent" --filter live --limit 50    # Latest tweets
opencli twitter search "topic" -f json            # JSON output
opencli twitter search "topic" -f csv             # CSV output

# Financial research examples
opencli twitter search "$AAPL earnings" --filter live --limit 20 -f json
opencli twitter search "Fed rate decision" --limit 20 -f yaml
opencli twitter search "market crash" --filter live --limit 15 -f json
```

### Trending Topics

```bash
opencli twitter trending                          # Top 20 trending topics (default)
opencli twitter trending --limit 10               # Limit count
opencli twitter trending -f json                  # JSON output
```

### Bookmarks

```bash
opencli twitter bookmarks                         # View bookmarked tweets
opencli twitter bookmarks --limit 30              # Limit count
opencli twitter bookmarks -f json                 # JSON output
```

### Thread / Tweet Detail

```bash
opencli twitter thread TWEET_ID                   # View tweet thread
opencli twitter thread TWEET_ID -f json           # JSON output
```

### Twitter Articles

```bash
opencli twitter article TWEET_ID                  # View long-form article
opencli twitter article TWEET_ID -f json          # JSON output
```

### User Data

```bash
opencli twitter profile elonmusk                  # User profile (defaults to logged-in user)
opencli twitter profile elonmusk -f json          # JSON output
opencli twitter followers elonmusk                # List followers
opencli twitter followers elonmusk --limit 50     # Limit count
opencli twitter following elonmusk                # List following
opencli twitter following elonmusk --limit 50     # Limit count
```

### Notifications

```bash
opencli twitter notifications                     # View notifications
opencli twitter notifications -f json             # JSON output
```

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

### Output columns by command

| Command | Columns |
|---|---|
| `timeline`, `search`, `bookmarks` | `id`, `author`, `text`, `created_at`, `likes`, `views`, `url` |
| `trending` | `rank`, `topic`, `tweet_count` |
| `profile` | `username`, `name`, `bio`, `followers_count`, `following_count`, `tweet_count` |
| `followers`, `following` | `username`, `name`, `bio`, `followers_count` |
| `notifications` | varies by notification type |

---

## Financial Research Workflows

### Search for earnings sentiment

```bash
opencli twitter search "$AAPL earnings" --filter live --limit 20 -f json
opencli twitter search "$TSLA delivery numbers" --filter live --limit 15 -f json
```

### Monitor fintwit for a ticker

```bash
opencli twitter search "$NVDA" --filter live --limit 30 -f json
opencli twitter search "$SPY puts" --filter live --limit 20 -f json
```

### Track analyst commentary

```bash
# Check trending topics for market themes
opencli twitter trending --limit 20 -f json

# Search for specific analyst takes
opencli twitter search "price target AAPL" --filter live --limit 15 -f json
```

### Macro / Fed watching

```bash
opencli twitter search "Fed rate decision" --filter live --limit 20 -f json
opencli twitter search "CPI report" --filter live --limit 15 -f json
opencli twitter search "inflation data" --filter live --limit 20 -f yaml
```

### Daily market reading workflow

```bash
# Check trending topics
opencli twitter trending --limit 10 -f json

# Read your feed
opencli twitter timeline --type following --limit 30 -f json

# Check bookmarks
opencli twitter bookmarks --limit 20 -f json

# Search for market outlook
opencli twitter search "market outlook" --filter live --limit 30 -f json
```

### Export for analysis

```bash
# CSV for spreadsheet analysis
opencli twitter search "AI stocks" --limit 50 -f csv > ai_stocks.csv

# JSON for programmatic processing
opencli twitter search "earnings beat" --limit 30 -f json > earnings.json
```

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `Extension not connected` | Browser Bridge not installed | Install the Browser Bridge Chrome extension |
| `Daemon not running` | opencli daemon not started | Run `opencli doctor` to auto-start |
| `No session for twitter.com` | Not logged into x.com | Login to x.com in Chrome |
| `CSRF token missing` | Cookie expired | Refresh x.com in Chrome |
| Rate limited | Too many requests | Wait a few minutes, then retry |

---

## Limitations

- **Read-only in this skill** — write operations are not supported for finance use
- **No DMs** — direct messages are not exposed via read commands in this skill
- **Requires Chrome** — opencli uses Chrome's Browser Bridge; other browsers are not supported
- **Single browser profile** — uses the active Chrome profile's session

---

## Best Practices

- **Keep request volumes low** — use `--limit 20` instead of `--limit 500`
- **Use `opencli doctor`** before your first command in a session to verify connectivity
- **Use `-f json`** for programmatic processing and LLM context
- **Use `-f csv`** when the user wants to analyze data in a spreadsheet
- **Prefer `--filter live`** for time-sensitive financial searches (earnings, breaking news)
