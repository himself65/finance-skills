# discord-cli Command Reference (Read-Only)

Complete read-only reference for [discord-cli](https://github.com/jackwener/discord-cli), scoped to financial research use cases.

Install: `uv tool install kabi-discord-cli` (or `pipx install kabi-discord-cli`)
Upgrade: `uv tool upgrade kabi-discord-cli`

**This skill is read-only.** Write operations (sending messages, reacting, editing, deleting) are NOT supported in this finance skill.

---

## Authentication

discord-cli authenticates via a Discord user token extracted from the local Discord client or browser.

**Auto-extract (recommended):**
```bash
discord auth --save
```

Extracts the token from the running Discord desktop app or browser session and saves it locally.

**Environment variable:**
```bash
export DISCORD_TOKEN="<token>"
discord status
```

**Auth check and identity:**
```bash
discord status                         # Validate token
discord whoami                         # Current authenticated user
discord whoami --json                  # JSON output
```

---

## Discord API Operations

### Guilds (Servers)

```bash
discord dc guilds                      # List all guilds
discord dc guilds --json               # JSON output
```

### Channels

```bash
discord dc channels GUILD_ID          # List channels in a guild
discord dc channels GUILD_ID --json   # JSON output
```

### Server Info

```bash
discord dc info GUILD_ID              # Guild details
discord dc info GUILD_ID --json       # JSON output
```

### Members

```bash
discord dc members GUILD_ID           # List members
discord dc members GUILD_ID --max 50  # Limit count
discord dc members GUILD_ID --json    # JSON output
```

### Message History

```bash
discord dc history CHANNEL_ID         # Fetch message history
discord dc history CHANNEL_ID -n 1000 # Limit to 1000 messages
```

### Sync (Download Messages Locally)

```bash
discord dc sync CHANNEL_ID            # Incremental sync
discord dc sync CHANNEL_ID -n 5000    # Sync up to 5000 messages
discord dc sync-all                   # Sync all channels
discord dc sync-all -n 5000           # Sync all with limit
```

### Tail (Latest Messages)

```bash
discord dc tail CHANNEL_ID            # Tail messages (continuous)
discord dc tail CHANNEL_ID --once     # Fetch latest batch only
```

### Search (Server-Side)

```bash
discord dc search GUILD_ID "keyword"                  # Search guild
discord dc search GUILD_ID "keyword" -c CHANNEL_ID    # Search specific channel
discord dc search GUILD_ID "keyword" --json            # JSON output
```

---

## Local Query Commands

These commands query the local SQLite database. **Run `discord dc sync` first** to populate local data.

### Search

```bash
discord search "keyword"              # Search all synced messages
discord search "keyword" -c CHANNEL   # Search specific channel
discord search "keyword" -n 50        # Limit results
discord search "keyword" --json       # JSON output
```

### Recent Messages

```bash
discord recent                        # Recent messages (all channels)
discord recent -c CHANNEL             # Recent in specific channel
discord recent --hours 24             # Last 24 hours
discord recent -n 50                  # Limit results
discord recent --json                 # JSON output
```

### Today's Messages

```bash
discord today                         # All messages from today
discord today -c CHANNEL              # Today's messages in channel
discord today --json                  # JSON output
```

### Statistics

```bash
discord stats                         # Message stats overview
discord stats --json                  # JSON output
```

### Top Senders

```bash
discord top                           # Top message senders
discord top -c CHANNEL                # Top senders in channel
discord top --hours 168               # Top senders in last week
discord top --json                    # JSON output
```

### Activity Timeline

```bash
discord timeline                      # Activity over time
discord timeline -c CHANNEL           # Timeline for channel
discord timeline --hours 168          # Last week
discord timeline --by day             # Group by day
discord timeline --by hour            # Group by hour
discord timeline --json               # JSON output
```

---

## Data Export

```bash
discord export CHANNEL_ID             # Export as text (default)
discord export CHANNEL_ID -f json     # Export as JSON
discord export CHANNEL_ID -f text     # Export as plain text
discord export CHANNEL_ID -o out.json # Save to file
discord export CHANNEL_ID --hours 24  # Export last 24 hours
```

---

## Output Modes

| Flag / Env | Purpose |
|---|---|
| `--json` | JSON structured output |
| `--yaml` | YAML structured output (default non-TTY) |
| `--rich` | Rich terminal-formatted output |
| `--auto` | Auto-detect (rich for TTY, YAML for non-TTY) |
| `OUTPUT=yaml` | Set default via environment variable |

---

## Financial Research Workflows

### Search for crypto sentiment

```bash
discord dc sync CHANNEL_ID -n 2000
discord search "BTC pump" -n 20 --json
discord search "ETH merge" -c CHANNEL -n 30 --json
```

### Monitor trading server activity

```bash
discord recent -c CHANNEL_ID --hours 12 -n 50 --json
discord today -c CHANNEL_ID --json
```

### Track active contributors

```bash
discord top -c CHANNEL_ID --hours 168 --json
discord timeline -c CHANNEL_ID --hours 168 --by day --json
```

### Search for earnings / market discussion

```bash
discord dc search GUILD_ID "earnings call" --json
discord dc search GUILD_ID "price target" -c CHANNEL_ID --json
discord search "NVDA" -n 30 --json
```

### Export channel for analysis

```bash
discord export CHANNEL_ID -f json -o trading_chat.json --hours 72
```

### Daily research workflow

```bash
# 1. Sync latest messages
discord dc sync CHANNEL_ID -n 500

# 2. Check today's activity
discord today -c CHANNEL_ID --json

# 3. Search for topics of interest
discord search "fed rate" -n 20 --json

# 4. Review who's most active
discord top -c CHANNEL_ID --hours 24 --json
```

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `Token not found` | Not authenticated | Run `discord auth --save` with Discord open |
| HTTP 401 | Token expired/invalid | Re-login to Discord and re-extract token |
| HTTP 403 | No access to resource | Verify server/channel membership |
| HTTP 429 | Rate limited | Wait a few minutes, then retry |

---

## Limitations

- **Read-only in this skill** — write operations are not supported for finance use
- **No DMs** — direct messages are not supported
- **No voice channels** — voice/audio not accessible
- **Single account** — one token at a time
- **Sync required for local queries** — must run `discord dc sync` before using `search`, `recent`, `today`, etc.

---

## Best Practices

- **Sync before querying** — local commands require synced data
- **Keep request volumes reasonable** — use `-n 1000` not `-n 100000`
- **Use `--once` with tail** — avoid continuous tailing in agent context
- **Export for analysis** — use `discord export -f json -o FILE` for offline processing
- **Treat tokens as secrets** — never log or display Discord tokens
