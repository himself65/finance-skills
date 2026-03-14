---
name: telegram-news
description: >
  Read Telegram channels and groups for financial news and market research using tdl (read-only).
  Use this skill whenever the user wants to read Telegram channels, export messages from financial
  Telegram groups, list their Telegram chats, search for news in Telegram channels, or gather
  market intelligence from Telegram.
  Triggers include: "check my Telegram", "read Telegram channel", "Telegram news",
  "what's new in my Telegram channels", "export messages from", "list my Telegram chats",
  "financial news on Telegram", "crypto Telegram", "market news Telegram",
  any mention of Telegram in context of reading financial news, crypto signals, or market research.
  This skill is READ-ONLY — it does NOT support sending messages, joining channels, or any write operations.
---

# Telegram News Skill (Read-Only)

Reads Telegram channels and groups for financial news and market research using [tdl](https://github.com/iyear/tdl), a Telegram CLI tool.

**This skill is read-only.** It is designed for financial research: reading channel messages, monitoring financial news channels, and exporting message history. It does NOT support sending messages, joining/leaving channels, or any write operations.

---

## Step 1: Ensure tdl Is Installed

Before running any command, check if tdl is installed:

```bash
command -v tdl && tdl version || echo "TDL_NOT_INSTALLED"
```

If `TDL_NOT_INSTALLED`, install tdl based on the user's platform:

| Platform | Install Command |
|----------|----------------|
| macOS / Linux | `curl -sSL https://docs.iyear.me/tdl/install.sh \| sudo bash` |
| macOS (Homebrew) | `brew install telegram-downloader` |
| Linux (Termux) | `pkg install tdl` |
| Linux (AUR) | `yay -S tdl` |
| Linux (Nix) | `nix-env -iA nixos.tdl` |
| Go (any platform) | `go install github.com/iyear/tdl@latest` |

Ask the user which installation method they prefer. Default to Homebrew on macOS, curl script on Linux.

---

## Step 2: Ensure tdl Is Authenticated

Check if the user is logged in:

```bash
tdl chat ls --limit 1 2>&1 && echo "AUTH_OK" || echo "AUTH_NEEDED"
```

If `AUTH_OK`, skip to Step 3.

If `AUTH_NEEDED`, guide the user through login. **Login requires interactive input** — the user must enter their phone number and verification code manually.

### Login methods

**Method A: QR Code (recommended — fastest)**

```bash
tdl login -T qr
```

A QR code will be displayed in the terminal. The user scans it with their Telegram mobile app (Settings > Devices > Link Desktop Device).

**Method B: Phone + Code**

```bash
tdl login -T code
```

The user enters their phone number, then the verification code sent to their Telegram app.

**Method C: Import from Telegram Desktop**

If the user has Telegram Desktop installed and logged in:

```bash
tdl login
```

This imports the session from the existing desktop client. The desktop client must be from the [official website](https://desktop.telegram.org/), NOT from the App Store or Microsoft Store.

### Namespaces

By default, tdl uses a `default` namespace. To manage multiple accounts:

```bash
tdl login -n work -T qr      # Login to "work" namespace
tdl chat ls -n work           # Use "work" namespace for commands
```

### Important login notes

- Login is a **one-time** operation. The session persists on disk after successful login.
- If login fails, ask the user to check their internet connection and try again.
- **Never ask for or handle Telegram passwords/2FA codes programmatically** — always let the user enter them interactively.

---

## Step 3: Identify What the User Needs

Match the user's request to one of the read operations below.

| User Request | Command | Key Flags |
|---|---|---|
| List all chats/channels | `tdl chat ls` | `-o json`, `-f "FILTER"` |
| List only channels | `tdl chat ls -f "Type contains 'channel'"` | `-o json` |
| Export recent messages | `tdl chat export -c CHAT -T last -i N` | `--all`, `--with-content` |
| Export messages by time range | `tdl chat export -c CHAT -T time -i START,END` | `--all`, `--with-content` |
| Export messages by ID range | `tdl chat export -c CHAT -T id -i FROM,TO` | `--all`, `--with-content` |
| Export from a topic/thread | `tdl chat export -c CHAT --topic TOPIC_ID` | `--all`, `--with-content` |
| Search for a channel by name | `tdl chat ls -f "VisibleName contains 'NAME'"` | `-o json` |

### Chat identifiers

The `-c` flag accepts multiple formats:

| Format | Example |
|--------|---------|
| Username (with @) | `-c @channel_name` |
| Username (without @) | `-c channel_name` |
| Numeric chat ID | `-c 123456789` |
| Public link | `-c https://t.me/channel_name` |
| Phone number | `-c "+1 123456789"` |
| Saved Messages | `-c ""` (empty) |

---

## Step 4: Execute the Command

### Listing chats

```bash
# List all chats
tdl chat ls

# JSON output for processing
tdl chat ls -o json

# Filter for channels only
tdl chat ls -f "Type contains 'channel'"

# Search by name
tdl chat ls -f "VisibleName contains 'Bloomberg'"
```

### Exporting messages

Always use `--all --with-content` to get text messages (not just media):

```bash
# Last 20 messages from a channel
tdl chat export -c @channel_name -T last -i 20 --all --with-content -o /tmp/tdl-export.json

# Messages from a time range (Unix timestamps)
tdl chat export -c @channel_name -T time -i 1710288000,1710374400 --all --with-content -o /tmp/tdl-export.json

# Messages by ID range
tdl chat export -c @channel_name -T id -i 100,200 --all --with-content -o /tmp/tdl-export.json
```

### Key rules

1. **Check auth first** — run `tdl chat ls --limit 1` before other commands to verify the session is valid
2. **Always use `--all --with-content`** when exporting messages for reading — without these flags, tdl only exports media messages
3. **Use `-o FILE`** to save exports to a file, then read the JSON — this is more reliable than parsing stdout
4. **Start with small exports** — use `-T last -i 20` unless the user asks for more
5. **Use filters on `chat ls`** to help users find the right channel before exporting
6. **NEVER execute write operations** — this skill is read-only; do not send messages, join channels, or modify anything
7. **Convert timestamps** — when the user gives dates, convert to Unix timestamps for the `-T time` filter

### Working with exported JSON

After exporting, read the JSON file and extract the relevant information:

```bash
# Export messages
tdl chat export -c @channel_name -T last -i 20 --all --with-content -o /tmp/tdl-export.json

# Read and process the export
cat /tmp/tdl-export.json
```

The export JSON contains message objects with fields like `id`, `date`, `message` (text content), `from_id`, `views`, and media metadata.

---

## Step 5: Present the Results

After fetching data, present it clearly for financial research:

1. **Summarize key messages** — highlight the most relevant news or market updates
2. **Include timestamps** — show when each message was posted
3. **Group by topic** — if multiple channels, organize by theme (macro, earnings, crypto, etc.)
4. **Flag actionable information** — note breaking news, price targets, earnings surprises
5. **Provide channel context** — mention which channel/group each message came from
6. **For channel lists**, show channel name, member count, and type

---

## Step 6: Diagnostics

If something isn't working:

| Error | Cause | Fix |
|-------|-------|-----|
| `not authorized` or session errors | Not logged in or session expired | Run `tdl login -T qr` to re-authenticate |
| `FLOOD_WAIT_X` | Rate limited by Telegram | Wait X seconds, then retry |
| `CHANNEL_PRIVATE` | No access to channel | User must join the channel in their Telegram app first |
| `tdl: command not found` | tdl not installed | Install using Step 1 |

---

## Reference Files

- `references/commands.md` — Complete tdl command reference for reading channels and exporting messages

Read the reference file when you need exact command syntax or detailed flag documentation.
