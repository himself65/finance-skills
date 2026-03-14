---
name: twitter
description: >
  Read Twitter/X for financial research using the twitter-cli tool (read-only).
  Use this skill whenever the user wants to read their Twitter feed, search for financial tweets,
  view bookmarks, look up user profiles, or gather market sentiment from Twitter/X.
  Triggers include: "check my feed", "search Twitter for", "show my bookmarks",
  "who follows", "look up @user", "what's trending about", "market sentiment on Twitter",
  "what are people saying about AAPL", "fintwit", any mention of Twitter/X in context
  of reading financial news or market research.
  This skill is READ-ONLY — it does NOT support posting, liking, retweeting, or any write operations.
---

# Twitter Skill (Read-Only)

Reads Twitter/X for financial research using [twitter-cli](https://github.com/jackwener/twitter-cli), a command-line tool that accesses Twitter via browser cookie authentication.

**This skill is read-only.** It is designed for financial research: searching market discussions, reading analyst tweets, tracking sentiment, and monitoring financial news on Twitter/X. It does NOT support posting, liking, retweeting, replying, or any write operations.

**Important**: This tool uses your browser session cookies. No API keys needed — it authenticates via your logged-in browser session (Chrome, Arc, Edge, Firefox, Brave).

**Claude for macOS limitation**: This skill does not work out-of-the-box in Claude for macOS (Claude.app). The app's shell runs in a [sandbox](https://github.com/anthropic-experimental/sandbox-runtime) with no network access by default, so it cannot download or install the twitter-cli tool. To enable it, add the required domains to your sandbox settings at `~/.srt-settings.json`:

```json
{
  "network": {
    "allowedDomains": [
      "x.com",
      "*.x.com",
      "api.x.com",
      "pypi.org",
      "*.pypi.org",
      "files.pythonhosted.org"
    ]
  }
}
```

Alternatively, use [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (the CLI), which runs without sandbox restrictions.

---

## Step 1: Ensure twitter-cli Is Installed and Authenticated

Before running any command, install and check auth:

```bash
# Install (requires Python 3.10+)
command -v twitter || uv tool install twitter-cli

# Check authentication
twitter status --yaml >/dev/null && echo "AUTH_OK" || echo "AUTH_NEEDED"
```

If `AUTH_OK`, skip to Step 2. If `AUTH_NEEDED`, guide the user:

### Authentication methods

**Method A: Browser cookie extraction (recommended)**

Ensure user is logged into x.com in Arc/Chrome/Edge/Firefox/Brave. twitter-cli auto-extracts cookies. Verify with:

```bash
twitter whoami
```

Chrome multi-profile: all profiles are scanned automatically. To specify one:
```bash
TWITTER_CHROME_PROFILE="Profile 2" twitter feed
```

**Method B: Environment variables**

```bash
export TWITTER_AUTH_TOKEN="<auth_token from browser>"
export TWITTER_CT0="<ct0 from browser>"
twitter whoami
```

### Common auth issues

| Symptom | Fix |
|---------|-----|
| `No Twitter cookies found` | Login to x.com in browser, or set env vars |
| `Cookie expired (401/403)` | Re-login to x.com and retry |
| `Unable to get key for cookie decryption` (macOS) | Run `security unlock-keychain ~/Library/Keychains/login.keychain-db` for SSH, or allow Terminal in Keychain Access |

---

## Step 2: Identify What the User Needs

Match the user's request to one of the read commands below, then use the corresponding command from `references/commands.md`.

| User Request | Command | Key Flags |
|---|---|---|
| Auth check | `twitter status` | `--yaml` |
| Who am I | `twitter whoami` | `--json`, `--yaml` |
| Home feed / timeline | `twitter feed` | `-t following`, `--max N`, `--full-text`, `--filter` |
| Search tweets | `twitter search "QUERY"` | `-t Latest`, `--from USER`, `--since DATE`, `--lang`, `--exclude retweets`, `--has links`, `--max N` |
| Bookmarks | `twitter bookmarks` | `--max N`, `--full-text` |
| View a specific tweet | `twitter tweet TWEET_ID_OR_URL` | `--full-text` |
| Open tweet from last list | `twitter show N` | `--full-text`, `--json` |
| Twitter article | `twitter article ID_OR_URL` | `--markdown`, `--output FILE`, `--json` |
| List timeline | `twitter list LIST_ID` | `--full-text`, `--max N` |
| User profile | `twitter user USERNAME` | `--json` |
| User's tweets | `twitter user-posts USERNAME` | `--max N`, `--full-text`, `-o FILE` |
| User's likes | `twitter likes USERNAME` | own account only (private since Jun 2024) |
| Followers | `twitter followers USERNAME` | `--max N` |
| Following | `twitter following USERNAME` | `--max N` |

---

## Step 3: Execute the Command

### General pattern

```bash
# Use --yaml for structured output, -c for compact (token-efficient)
twitter feed --yaml --max 20
twitter -c feed --max 10              # Compact: ~80% fewer tokens than --json

# Searching for financial topics
twitter search "$AAPL earnings" -t Latest --max 10 --full-text --yaml
twitter search "Fed rate decision" --since 2026-03-01 --max 20 --yaml
twitter search "market crash" --exclude retweets --has links --max 15
```

### Key rules

1. **Check auth first** — run `twitter status --yaml` before any other command
2. **Use `--yaml` or `--json`** for structured output when processing data programmatically
3. **Use `-c` / `--compact`** when token efficiency matters (LLM context)
4. **Use `--full-text`** when the user wants complete tweet content (text is truncated by default in rich tables)
5. **Use `--max N`** to limit results — start with 10-20 unless the user asks for more
6. **For search, use filters** — `--from`, `--since`, `--lang`, `--exclude retweets`, `--has links`
7. **Tweet IDs vs URLs** — both work: `twitter tweet 1234567890` or `twitter tweet https://x.com/user/status/1234567890`
8. **Use `twitter show N`** to reference tweet #N from the most recent list output
9. **NEVER execute write operations** — this skill is read-only; do not post, like, retweet, reply, quote, follow, or delete

### Output flags (all read commands)

| Flag | Purpose |
|---|---|
| `--json` | JSON output |
| `--yaml` | YAML output (default in non-TTY) |
| `--full-text` | Show complete tweet text (rich table only) |
| `-c` / `--compact` | Minimal fields, great for LLM context |
| `-o FILE` / `--output FILE` | Save output to file |
| `--input FILE` | Read from previously saved JSON |

### Structured output envelope

All `--yaml` and `--json` output uses this envelope (see `references/schema.md`):

```yaml
ok: true
schema_version: "1"
data: ...          # tweet/user lists or single objects
```

Error responses:
```yaml
ok: false
schema_version: "1"
error:
  code: api_error
  message: "..."
```

---

## Step 4: Present the Results

After fetching data, present it clearly for financial research:

1. **Summarize key content** — highlight the most relevant tweets for the user's financial research
2. **Include attribution** — show @username, tweet text, and engagement metrics (likes, retweets)
3. **Provide tweet IDs/URLs** when the user might want to read the full thread
4. **For search results**, group by relevance and highlight key themes, sentiment, or market signals
5. **For user profiles**, present follower count, bio, and notable recent activity
6. **Flag sentiment** — note bullish/bearish sentiment, consensus vs contrarian views
7. **Treat cookies as secrets** — never echo cookie values to stdout

---

## Step 5: Diagnostics

If something isn't working, run:

```bash
twitter doctor
```

Reports version, OS, browser detection, keychain status, and cookie extraction results.

For verbose diagnostics on any command, add `-v`.

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `No Twitter cookies found` | Not authenticated | Login to x.com in browser, or set env vars |
| HTTP 401/403 | Cookie expired | Re-login to x.com and retry |
| HTTP 404 | QueryId rotation | Retry (auto-fallback built in) |
| HTTP 429 | Rate limited | Wait 15+ minutes, then retry |

---

## Proxy Configuration

```bash
export TWITTER_PROXY=http://127.0.0.1:7890
# or
export TWITTER_PROXY=socks5://127.0.0.1:1080
```

---

## Reference Files

- `references/commands.md` — Complete read command reference with all flags, research workflows, and usage examples
- `references/schema.md` — Structured output schema documentation

Read the reference files when you need exact command syntax, research workflow patterns, or schema details.
