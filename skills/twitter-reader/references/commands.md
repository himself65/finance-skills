# twitter-cli Command Reference (Read-Only)

Complete read-only reference for [twitter-cli](https://github.com/jackwener/twitter-cli), scoped to financial research use cases.

Install: `uv tool install twitter-cli` (or `pipx install twitter-cli`)
Upgrade: `uv tool upgrade twitter-cli`

**This skill is read-only.** Write operations (post, like, retweet, reply, quote, follow, delete) are NOT supported in this finance skill.

---

## Authentication

twitter-cli authenticates via browser cookies (no API keys needed).

**Priority order:**
1. Environment variables: `TWITTER_AUTH_TOKEN` + `TWITTER_CT0`
2. Automatic browser cookie extraction (Arc, Chrome, Edge, Firefox, Brave)

Browser extraction is recommended — it forwards ALL Twitter cookies and aligns request headers with the local runtime.

**Chrome profile selection:**
```bash
TWITTER_CHROME_PROFILE="Profile 2" twitter feed
```

**Auth check and identity:**
```bash
twitter status                         # Quick auth check
twitter status --yaml                  # Structured auth status
twitter whoami                         # Current authenticated user
twitter whoami --yaml                  # YAML output
twitter whoami --json                  # JSON output
```

---

## Read Operations

### Feed (Home Timeline)

```bash
twitter feed                           # "For You" feed
twitter feed -t following              # "Following" tab
twitter feed --max 50                  # Limit count
twitter feed --full-text               # Show full post body in table
twitter feed --filter                  # Enable ranking filter
twitter feed --yaml > tweets.yaml      # Export as YAML
twitter feed --input tweets.json       # Read from local JSON file
```

### Search

```bash
twitter search "keyword"               # Basic search
twitter search "AI agent" -t Latest --max 50    # Latest tab
twitter search "AI agent" --full-text  # Full text in results
twitter search "topic" -o results.json # Save to file
twitter search "trending" --filter     # Apply ranking filter

# Advanced filters
twitter search "python" --from elonmusk --lang en --since 2026-01-01
twitter search --from bbc --exclude retweets --has links
```

### Bookmarks

```bash
twitter bookmarks
twitter bookmarks --full-text
twitter bookmarks --max 30 --yaml
```

### Tweet Detail

```bash
twitter tweet 1234567890               # By ID (shows tweet + replies)
twitter tweet 1234567890 --full-text   # Full text in reply table
twitter tweet https://x.com/user/status/12345  # By URL

# Open tweet by index from last list output
twitter show 2                         # Tweet #2 from last feed/search
twitter show 2 --full-text
twitter show 2 --json
```

### Twitter Articles

```bash
twitter article 1234567890
twitter article https://x.com/user/article/1234567890 --json
twitter article 1234567890 --markdown
twitter article 1234567890 --output article.md
```

### Lists

```bash
twitter list 1539453138322673664
twitter list 1539453138322673664 --full-text
```

### User Data

```bash
twitter user elonmusk                  # Profile
twitter user elonmusk --json           # JSON output
twitter user-posts elonmusk --max 20   # User's tweets
twitter user-posts elonmusk --full-text
twitter user-posts elonmusk -o tweets.json
twitter likes elonmusk --max 30        # Own likes only (private since Jun 2024)
twitter likes elonmusk --full-text
twitter likes elonmusk -o likes.json
twitter followers elonmusk --max 50
twitter following elonmusk --max 50
```

---

## Output Modes

| Flag | Purpose |
|---|---|
| (default) | Rich table, human-readable |
| `--full-text` | Disable text truncation in rich table |
| `--json` | JSON structured output |
| `--yaml` | YAML structured output (default non-TTY) |
| `-c` / `--compact` | Minimal fields, ~80% fewer tokens for LLM context |
| `-o FILE` / `--output FILE` | Save output to file |
| `--input FILE` | Read from previously saved JSON |

**Compact mode fields (per tweet):** `id`, `author` (@handle), `text` (truncated 140 chars), `likes`, `rts`, `time` (short format)

---

## Financial Research Workflows

### Search for earnings sentiment

```bash
twitter search "$AAPL earnings" -t Latest --max 20 --yaml
twitter search "$TSLA delivery numbers" --since 2026-03-01 --max 15 --full-text
```

### Monitor fintwit for a ticker

```bash
twitter search "$NVDA" -t Latest --max 30 --yaml
twitter search "$SPY puts" --exclude retweets --max 20
```

### Track analyst commentary

```bash
twitter user-posts jimcramer --max 10 --full-text
twitter search "price target" --from hedgeye --max 10 --yaml
```

### Macro / Fed watching

```bash
twitter search "Fed rate decision" -t Latest --max 20 --full-text
twitter search "CPI report" --since 2026-03-01 --has links --max 15
twitter search "inflation data" --exclude retweets --max 20 --yaml
```

### Find most-engaged financial tweets

```bash
twitter search "$SPX" --max 30 --json | jq '[.data[] | select(.metrics.likes > 100)] | sort_by(.metrics.likes) | reverse'
```

### Daily market reading workflow

```bash
# Compact mode for token-efficient LLM context
twitter -c feed -t following --max 30
twitter -c bookmarks --max 20

# Full text for deep reading
twitter feed -t following --max 20 --full-text

# Export for analysis
twitter search "market outlook" -t Latest --max 30 -o market_tweets.json
```

### Search with jq filtering

```bash
# Tweets with > 100 likes about a topic
twitter search "AI stocks" --max 20 --json | jq '[.data[] | select(.metrics.likes > 100)]'

# Extract just text and author
twitter search "earnings beat" --max 10 --json | jq '.data[] | {author: .author.screenName, text: .text[:100]}'
```

### Read a specific thread or article

```bash
twitter tweet https://x.com/user/status/1234567890 --full-text
twitter article 1234567890 --markdown --output analysis.md
```

---

## Ranking Filter

Filtering is opt-in. Enable with `--filter`:

```bash
twitter feed --filter
twitter bookmarks --filter
```

Scoring formula:
```
score = likes_w * likes + retweets_w * retweets + replies_w * replies
      + bookmarks_w * bookmarks + views_log_w * log10(max(views, 1))
```

Configure in `config.yaml`:
```yaml
filter:
  mode: "topN"          # "topN" | "score" | "all"
  topN: 20
  minScore: 50
  weights:
    likes: 1.0
    retweets: 3.0
    replies: 2.0
    bookmarks: 5.0
    views_log: 0.5
```

---

## Configuration (config.yaml)

Place in working directory:

```yaml
fetch:
  count: 50              # Default item limit when --max is omitted

filter:
  mode: "topN"
  topN: 20
  minScore: 50

rateLimit:
  requestDelay: 2.5      # Base delay between requests (randomized ×0.7–1.5)
  maxRetries: 3
  retryBaseDelay: 5.0
  maxCount: 200           # Hard cap on fetched items
```

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `No Twitter cookies found` | Not authenticated | Login to x.com in browser, or set env vars |
| HTTP 401/403 | Cookie expired | Re-login to x.com and retry |
| HTTP 404 | QueryId rotation | Retry (auto-fallback built in) |
| HTTP 429 | Rate limited | Wait 15+ minutes, then retry |

---

## Proxy Support

```bash
export TWITTER_PROXY=http://127.0.0.1:7890
export TWITTER_PROXY=socks5://127.0.0.1:1080
```

---

## Limitations

- **Read-only in this skill** — write operations are not supported for finance use
- **No DMs** — no direct messaging
- **No notifications** — can't read notifications
- **Single account** — one set of credentials at a time
- **Likes are private** — `twitter likes` only works for your own account (since Jun 2024)

---

## Best Practices

- **Keep request volumes low** — use `--max 20` instead of `--max 500`
- **Don't run too frequently** — each startup fetches x.com for anti-detection headers
- **Use browser cookie extraction** — provides full cookie fingerprint
- **Use a proxy** if concerned about IP exposure

---

## Diagnostics

```bash
twitter doctor
```

Reports version, OS, browser detection, keychain status, and cookie extraction results.

For verbose output on any command, add `-v`.
