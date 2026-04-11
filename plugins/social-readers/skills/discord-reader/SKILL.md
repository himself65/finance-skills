---
name: discord-reader
description: >
  Read Discord for financial research using opencli (read-only).
  Use this skill whenever the user wants to read Discord channels, search for messages
  in trading servers, view guild/channel info, monitor crypto or market discussion groups,
  or gather financial sentiment from Discord.
  Triggers include: "check my Discord", "search Discord for", "read Discord messages",
  "what's happening in the trading Discord", "show Discord channels", "list my servers",
  "Discord sentiment on BTC", "what are people saying in Discord about AAPL",
  "monitor crypto Discord", any mention of Discord in context
  of reading financial news, market research, or trading community discussions.
  This skill is READ-ONLY — it does NOT support sending messages, reacting, or any write operations.
---

# Discord Skill (Read-Only)

Reads Discord for financial research using [opencli](https://github.com/jackwener/opencli), a universal CLI tool that bridges desktop apps and web services to the terminal via Chrome DevTools Protocol (CDP).

**This skill is read-only.** It is designed for financial research: searching trading server discussions, monitoring crypto/market groups, tracking sentiment in financial communities, and reading messages. It does NOT support sending messages, reacting, editing, deleting, or any write operations.

**Important**: opencli connects to the Discord desktop app via CDP — no bot account or token extraction needed. Just have Discord Desktop running.

---

## Step 1: Ensure opencli Is Installed and Discord Is Ready

**Current environment status:**

```
!`(command -v opencli && opencli discord-app status 2>&1 | head -5 && echo "READY" || echo "SETUP_NEEDED") 2>/dev/null || echo "NOT_INSTALLED"`
```

If the status above shows `READY`, skip to Step 2. If `NOT_INSTALLED`, install first:

```bash
# Install opencli globally
npm install -g @jackwener/opencli
```

If `SETUP_NEEDED`, guide the user through setup:

### Setup

opencli connects to Discord Desktop via CDP (Chrome DevTools Protocol). Two things are required:

1. **Start Discord with remote debugging enabled:**

```bash
# macOS
/Applications/Discord.app/Contents/MacOS/Discord --remote-debugging-port=9232 &

# Linux
discord --remote-debugging-port=9232 &
```

2. **Set the CDP endpoint environment variable:**

```bash
export OPENCLI_CDP_ENDPOINT="http://127.0.0.1:9232"
```

Add this to your shell profile (`.zshrc` / `.bashrc`) so it persists across sessions.

3. **Verify connectivity:**

```bash
opencli discord-app status
```

### Common setup issues

| Symptom | Fix |
|---------|-----|
| `CDP connection refused` | Ensure Discord is running with `--remote-debugging-port=9232` |
| `OPENCLI_CDP_ENDPOINT not set` | Run `export OPENCLI_CDP_ENDPOINT="http://127.0.0.1:9232"` |
| `status` shows disconnected | Restart Discord with the CDP flag and retry |
| Discord not on expected port | Check that no other app is using port 9232, or use a different port |

### Tip: create a shell alias

```bash
alias discord-cdp='/Applications/Discord.app/Contents/MacOS/Discord --remote-debugging-port=9232 &'
```

---

## Step 2: Identify What the User Needs

Match the user's request to one of the read commands below, then use the corresponding command from `references/commands.md`.

| User Request | Command | Key Flags |
|---|---|---|
| Connection check | `opencli discord-app status` | — |
| List servers | `opencli discord-app servers` | `-f json` |
| List channels | `opencli discord-app channels` | `-f json` |
| List online members | `opencli discord-app members` | `-f json` |
| Read recent messages | `opencli discord-app read` | `N` (count), `-f json` |
| Search messages | `opencli discord-app search "QUERY"` | `-f json` |

**Note:** opencli operates on the **currently active** server and channel in Discord. To read from a different channel, the user must navigate to it in the Discord app first, or use the `channels` command to identify what's available.

---

## Step 3: Execute the Command

### General pattern

```bash
# Use -f json or -f yaml for structured output
opencli discord-app servers -f json
opencli discord-app channels -f json

# Read recent messages from the active channel
opencli discord-app read 50 -f json

# Search for financial topics in the active channel
opencli discord-app search "AAPL earnings" -f json
opencli discord-app search "BTC pump" -f json
```

### Key rules

1. **Check connection first** — run `opencli discord-app status` before any other command
2. **Use `-f json` or `-f yaml`** for structured output when processing data programmatically
3. **Navigate in Discord first** — opencli reads from the currently active server/channel in the Discord app
4. **Start with small reads** — use `opencli discord-app read 20` unless the user asks for more
5. **Use search for keywords** — `opencli discord-app search` uses Discord's built-in search (Cmd+F / Ctrl+F)
6. **NEVER execute write operations** — this skill is read-only; do not send messages, react, edit, delete, or manage server settings

### Output format flag (`-f`)

| Format | Flag | Best for |
|---|---|---|
| Table | `-f table` (default) | Human-readable terminal output |
| JSON | `-f json` | Programmatic processing, LLM context |
| YAML | `-f yaml` | Structured output, readable |
| Markdown | `-f md` | Documentation, reports |
| CSV | `-f csv` | Spreadsheet export |

### Typical workflow for reading a server

```bash
# 1. Verify connection
opencli discord-app status

# 2. List servers to confirm you're in the right one
opencli discord-app servers -f json

# 3. List channels in the current server
opencli discord-app channels -f json

# 4. Read recent messages (navigate to target channel in Discord first)
opencli discord-app read 50 -f json

# 5. Search for topics of interest
opencli discord-app search "price target" -f json
```

---

## Step 4: Present the Results

After fetching data, present it clearly for financial research:

1. **Summarize key content** — highlight the most relevant messages for the user's financial research
2. **Include attribution** — show username, message content, and timestamp
3. **For search results**, group by relevance and highlight key themes, sentiment, or market signals
4. **For server/channel listings**, present as a clean table with names and types
5. **Flag sentiment** — note bullish/bearish sentiment, consensus vs contrarian views
6. **Treat sessions as private** — never expose CDP endpoints or session details

---

## Step 5: Diagnostics

If something isn't working, check:

1. **Is Discord running with CDP?**
```bash
# Check if the port is open
lsof -i :9232
```

2. **Is the environment variable set?**
```bash
echo $OPENCLI_CDP_ENDPOINT
```

3. **Can opencli connect?**
```bash
opencli discord-app status
```

If all checks fail, restart Discord with the CDP flag:
```bash
/Applications/Discord.app/Contents/MacOS/Discord --remote-debugging-port=9232 &
export OPENCLI_CDP_ENDPOINT="http://127.0.0.1:9232"
opencli discord-app status
```

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `CDP connection refused` | Discord not running with CDP or wrong port | Start Discord with `--remote-debugging-port=9232` |
| `OPENCLI_CDP_ENDPOINT not set` | Missing environment variable | `export OPENCLI_CDP_ENDPOINT="http://127.0.0.1:9232"` |
| `No active channel` | Not viewing any channel in Discord | Navigate to a channel in the Discord app |
| Rate limited | Too many requests | Wait a few minutes, then retry |

---

## Reference Files

- `references/commands.md` — Complete read command reference with all flags and usage examples

Read the reference file when you need exact command syntax or detailed flag descriptions.
