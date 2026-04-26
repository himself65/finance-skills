# opencli Discord Command Reference (Read-Only)

Complete read-only reference for Discord commands in [opencli](https://github.com/jackwener/opencli), scoped to financial research use cases.

Install: `npm install -g @jackwener/opencli`

**This skill is read-only.** Write operations (sending messages, reacting, editing, deleting) are NOT supported in this finance skill.

---

## Setup

opencli connects to Discord Desktop via Chrome DevTools Protocol (CDP) — no bot account, token extraction, or Browser Bridge extension needed.

**Requirements:**
1. Node.js >= 21 (or Bun >= 1.0)
2. Discord Desktop running with `--remote-debugging-port=9232`
3. `OPENCLI_CDP_ENDPOINT` environment variable set

**Start Discord with CDP:**
```bash
# macOS
/Applications/Discord.app/Contents/MacOS/Discord --remote-debugging-port=9232 &

# Linux
discord --remote-debugging-port=9232 &
```

**Set the environment variable:**
```bash
export OPENCLI_CDP_ENDPOINT="http://127.0.0.1:9232"
```

**Verify connectivity:**
```bash
opencli discord-app status
```

---

## Read Operations

### Connection Status

```bash
opencli discord-app status                        # Check CDP connection
opencli discord-app status -f json                # JSON output
```

### Servers (Guilds)

```bash
opencli discord-app servers                       # List all joined servers
opencli discord-app servers -f json               # JSON output
opencli discord-app servers -f yaml               # YAML output
```

### Channels

Lists channels in the **currently active** server in Discord.

```bash
opencli discord-app channels                      # List channels in current server
opencli discord-app channels -f json              # JSON output
```

### Members

Lists online members in the **currently active** server.

```bash
opencli discord-app members                       # List online members
opencli discord-app members -f json               # JSON output
```

### Read Messages

Reads recent messages from the **currently active** channel in Discord.

```bash
opencli discord-app read                          # Read last 20 messages (default)
opencli discord-app read 50                       # Read last 50 messages
opencli discord-app read 100 -f json              # JSON output
opencli discord-app read 30 -f yaml               # YAML output
opencli discord-app read 50 -f csv                # CSV output
```

### Search Messages

Searches messages in the current context using Discord's built-in search (Cmd+F / Ctrl+F).

```bash
opencli discord-app search "keyword"              # Search in active channel
opencli discord-app search "AAPL earnings" -f json  # JSON output
opencli discord-app search "BTC pump" -f yaml     # YAML output
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
| `status` | `Status`, `Url`, `Title` |
| `servers` | `Index`, `Server` |
| `channels` | `Index`, `Channel`, `Type` (Text/Voice/Forum/Announcement/Stage) |
| `members` | `Index`, `Name`, `Status` |
| `read` | `Author`, `Time`, `Message` |
| `search` | `Index`, `Author`, `Message` |

---

## Financial Research Workflows

### Read latest messages from a trading channel

```bash
# Navigate to the target channel in Discord first, then:
opencli discord-app read 50 -f json
```

### Search for crypto sentiment

```bash
opencli discord-app search "BTC pump" -f json
opencli discord-app search "ETH breakout" -f json
```

### Search for earnings / market discussion

```bash
opencli discord-app search "earnings call" -f json
opencli discord-app search "price target" -f json
opencli discord-app search "NVDA" -f json
```

### Survey a trading server

```bash
# 1. List servers
opencli discord-app servers -f json

# 2. List channels (navigate to target server in Discord)
opencli discord-app channels -f json

# 3. Read recent messages (navigate to target channel)
opencli discord-app read 50 -f json

# 4. Search for topics
opencli discord-app search "market outlook" -f json
```

### Export for analysis

```bash
# CSV for spreadsheet analysis
opencli discord-app read 100 -f csv > trading_chat.csv

# JSON for programmatic processing
opencli discord-app read 100 -f json > messages.json
```

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `CDP connection refused` | Discord not running with CDP flag | Start Discord with `--remote-debugging-port=9232` |
| `OPENCLI_CDP_ENDPOINT not set` | Missing environment variable | `export OPENCLI_CDP_ENDPOINT="http://127.0.0.1:9232"` |
| `No active channel` | Discord not focused on any channel | Navigate to a channel in the Discord app |
| Rate limited | Too many requests | Wait a few minutes, then retry |

---

## Limitations

- **Read-only in this skill** — opencli itself exposes `discord-app send` and `discord-app delete` commands, but this skill forbids them
- **Active channel only** — reads from the currently viewed channel in Discord; navigate in the app to switch
- **No DMs** — direct messages are not supported
- **No voice channels** — voice/audio not accessible
- **No message history sync** — no local database; reads live from the app
- **No server-side search** — search uses Discord's in-app Cmd+F / Ctrl+F
- **Requires Discord Desktop** — the web client is not supported (CDP connects to the Electron app)

---

## Best Practices

- **Navigate first, then read** — switch to the target channel in Discord before running `read` or `search`
- **Keep read counts reasonable** — use `read 50` not `read 10000`
- **Use `-f json`** for programmatic processing and LLM context
- **Use `-f csv`** when the user wants to analyze data in a spreadsheet
- **Add CDP startup to your workflow** — use a shell alias or launch script to start Discord with the CDP flag
- **Treat CDP endpoints as private** — never log or display connection URLs
