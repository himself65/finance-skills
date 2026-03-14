---
name: discord
description: >
  Read Discord for financial research using the discord-cli tool (read-only).
  Use this skill whenever the user wants to read Discord channels, search for messages
  in trading servers, view guild/channel info, monitor crypto or market discussion groups,
  or gather financial sentiment from Discord.
  Triggers include: "check my Discord", "search Discord for", "read Discord messages",
  "what's happening in the trading Discord", "show Discord channels", "list my servers",
  "Discord sentiment on BTC", "what are people saying in Discord about AAPL",
  "monitor crypto Discord", "export Discord messages", any mention of Discord in context
  of reading financial news, market research, or trading community discussions.
  This skill is READ-ONLY — it does NOT support sending messages, reacting, or any write operations.
---

# Discord Skill (Read-Only)

Reads Discord for financial research using [discord-cli](https://github.com/jackwener/discord-cli), a command-line tool that syncs Discord messages locally and provides search, analytics, and export capabilities.

**This skill is read-only.** It is designed for financial research: searching trading server discussions, monitoring crypto/market groups, tracking sentiment in financial communities, and exporting messages for analysis. It does NOT support sending messages, reacting, editing, deleting, or any write operations.

**Important**: This tool uses your Discord token extracted from a local Discord client or browser session. No bot account needed.

---

## Step 1: Ensure discord-cli Is Installed and Authenticated

Before running any command, install and check auth:

```bash
# Install (requires Python 3.10+)
command -v discord || uv tool install kabi-discord-cli

# Check authentication
discord status && echo "AUTH_OK" || echo "AUTH_NEEDED"
```

If `AUTH_OK`, skip to Step 2. If `AUTH_NEEDED`, guide the user:

### Authentication

**Method A: Auto-extract from local Discord client (recommended)**

```bash
discord auth --save
```

This extracts the token from the locally running Discord desktop app or browser session and saves it for future use.

**Method B: Environment variable**

```bash
export DISCORD_TOKEN="<token from browser DevTools>"
discord status
```

### Common auth issues

| Symptom | Fix |
|---------|-----|
| `Token not found` | Open Discord desktop app or login in browser, then run `discord auth --save` |
| `Token expired / invalid` | Re-login to Discord and run `discord auth --save` again |
| `Unauthorized (401)` | Token is invalid — re-extract with `discord auth --save` |

---

## Step 2: Identify What the User Needs

Match the user's request to one of the read commands below, then use the corresponding command from `references/commands.md`.

| User Request | Command | Key Flags |
|---|---|---|
| Auth check | `discord status` | — |
| Who am I | `discord whoami` | `--json` |
| List servers/guilds | `discord dc guilds` | `--json` |
| List channels in a server | `discord dc channels GUILD_ID` | `--json` |
| Server info | `discord dc info GUILD_ID` | `--json` |
| Server members | `discord dc members GUILD_ID` | `--max N`, `--json` |
| Fetch message history | `discord dc history CHANNEL_ID` | `-n N` |
| Sync messages locally | `discord dc sync CHANNEL_ID` | `-n N` |
| Sync all channels | `discord dc sync-all` | `-n N` |
| Tail (live/latest) | `discord dc tail CHANNEL_ID` | `--once` |
| Search server (API) | `discord dc search GUILD_ID "QUERY"` | `-c CHANNEL_ID`, `--json` |
| Search locally | `discord search "QUERY"` | `-c CHANNEL`, `-n N`, `--json` |
| Recent messages | `discord recent` | `-c CHANNEL`, `--hours N`, `-n N`, `--json` |
| Today's messages | `discord today` | `-c CHANNEL`, `--json` |
| Message stats | `discord stats` | `--json` |
| Top senders | `discord top` | `-c CHANNEL`, `--hours N`, `--json` |
| Activity timeline | `discord timeline` | `-c CHANNEL`, `--hours N`, `--by day\|hour`, `--json` |
| Export messages | `discord export CHANNEL` | `-f text\|json`, `-o FILE`, `--hours N` |

---

## Step 3: Execute the Command

### General pattern

```bash
# Use --json or --yaml for structured output
discord dc guilds --json
discord dc channels GUILD_ID --json

# Sync messages from a channel for local queries
discord dc sync CHANNEL_ID -n 1000

# Search for financial topics
discord dc search GUILD_ID "AAPL earnings" --json
discord search "BTC pump" -n 20 --json

# Recent activity
discord recent --hours 24 -n 50 --json
discord today -c CHANNEL_ID --json
```

### Key rules

1. **Check auth first** — run `discord status` before any other command
2. **Use `--json` or `--yaml`** for structured output when processing data programmatically
3. **Sync before local queries** — run `discord dc sync CHANNEL_ID` before using `discord search`, `discord recent`, etc.
4. **Use `-n N`** to limit results — start with 50–100 unless the user asks for more
5. **Use `discord dc search`** for server-side search (no sync needed); use `discord search` for local search (requires prior sync)
6. **Use `--hours N`** with `recent`, `top`, `timeline`, and `export` to scope by time window
7. **NEVER execute write operations** — this skill is read-only; do not send messages, react, edit, delete, or manage server settings
8. **NEVER run `discord purge`** — this deletes local data and is not relevant for research

### Output flags

| Flag | Purpose |
|---|---|
| `--json` | JSON output |
| `--yaml` | YAML output (default in non-TTY) |
| `-n N` | Limit number of results |
| `-o FILE` | Save output to file |
| `-c CHANNEL` | Filter by channel |

### Typical workflow for a new server

```bash
# 1. List guilds to find the server
discord dc guilds --json

# 2. List channels in the target guild
discord dc channels GUILD_ID --json

# 3. Sync messages from channels of interest
discord dc sync CHANNEL_ID -n 2000

# 4. Search or analyze
discord search "price target" -n 20 --json
discord recent -c CHANNEL_ID --hours 24 --json
discord top -c CHANNEL_ID --hours 168 --json
```

---

## Step 4: Present the Results

After fetching data, present it clearly for financial research:

1. **Summarize key content** — highlight the most relevant messages for the user's financial research
2. **Include attribution** — show username, message content, and timestamp
3. **For search results**, group by relevance and highlight key themes, sentiment, or market signals
4. **For server/channel listings**, present as a clean table with names and IDs
5. **Flag sentiment** — note bullish/bearish sentiment, consensus vs contrarian views
6. **For analytics** (`stats`, `top`, `timeline`), present activity patterns and notable contributors
7. **Treat tokens as secrets** — never echo Discord tokens to stdout

---

## Step 5: Diagnostics

If authentication fails, re-run:

```bash
discord auth --save
discord status
```

Ensure Discord desktop app is running or you are logged into Discord in a browser.

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `Token not found` | Not authenticated | Run `discord auth --save` with Discord open |
| HTTP 401 | Token expired/invalid | Re-login to Discord and re-extract token |
| HTTP 403 | No access to resource | Verify you have access to the server/channel |
| HTTP 429 | Rate limited | Wait a few minutes, then retry |

---

## Reference Files

- `references/commands.md` — Complete read command reference with all flags and usage examples

Read the reference file when you need exact command syntax or detailed flag descriptions.
