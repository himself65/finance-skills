# tdl Command Reference (Read-Only)

Complete reference for tdl commands used in the telegram skill. Only read operations are documented — this skill does not support write operations.

## Global Flags

| Flag | Description |
|------|-------------|
| `-n NAMESPACE` | Use a specific namespace (default: `default`) |
| `--proxy PROXY` | Set proxy (e.g., `socks5://127.0.0.1:1080`, `http://127.0.0.1:7890`) |

## Login

### QR Code Login (recommended)

```bash
tdl login -T qr
```

Displays a QR code in the terminal. Scan with Telegram mobile app (Settings > Devices > Link Desktop Device).

### Phone + Code Login

```bash
tdl login -T code
```

Enter phone number and verification code interactively.

### Desktop Client Import

```bash
tdl login
```

Imports session from Telegram Desktop. Client must be from [official website](https://desktop.telegram.org/), not App Store or Microsoft Store.

Optional flags:

| Flag | Description |
|------|-------------|
| `-T TYPE` | Login type: `qr`, `code`, or desktop import (default) |
| `-n NAMESPACE` | Login to a specific namespace |
| `-p PASSCODE` | Passcode for desktop client (if set) |
| `-d PATH` | Custom path to desktop client data |

## List Chats

```bash
tdl chat ls [flags]
```

| Flag | Description |
|------|-------------|
| `-o json` | Output as JSON |
| `-f "FILTER"` | Filter expression |

### Filter examples

```bash
# All channels
tdl chat ls -f "Type contains 'channel'"

# Search by name
tdl chat ls -f "VisibleName contains 'Bloomberg'"

# Channels with specific name
tdl chat ls -f "Type contains 'channel' && VisibleName contains 'Finance'"

# Groups with topics
tdl chat ls -f "len(Topics)>0"

# List available filter fields
tdl chat ls -f -
```

## Export Messages

```bash
tdl chat export -c CHAT [flags]
```

### Chat identifier formats

| Format | Example |
|--------|---------|
| Username (with @) | `-c @channel_name` |
| Username (without @) | `-c channel_name` |
| Numeric chat ID | `-c 123456789` |
| Public link | `-c https://t.me/channel_name` |
| Phone number | `-c "+1 123456789"` |
| Saved Messages | `-c ""` |

### Range selection

| Type Flag | Input Flag | Description | Example |
|-----------|------------|-------------|---------|
| `-T last` | `-i N` | Last N messages | `-T last -i 50` |
| `-T time` | `-i START,END` | Unix timestamp range | `-T time -i 1710288000,1710374400` |
| `-T id` | `-i FROM,TO` | Message ID range | `-T id -i 100,500` |

### Content flags

| Flag | Description |
|------|-------------|
| `--all` | Include all messages, not just media messages |
| `--with-content` | Include message text content |
| `--raw` | Output raw MTProto structure |
| `-o FILE` | Output file path (default: `tdl-export.json`) |

### Topic / Reply flags

| Flag | Description |
|------|-------------|
| `--topic TOPIC_ID` | Export from a specific forum topic |
| `--reply POST_ID` | Export replies to a specific post |

### Filtering messages

```bash
# List available filter fields
tdl chat export -c CHAT -f -

# Filter by views
tdl chat export -c CHAT -T last -i 50 -f "Views>200"

# Filter by media
tdl chat export -c CHAT -T last -i 50 -f "Media.Name endsWith '.pdf'"
```

### Complete export examples

```bash
# Last 20 messages with text content from a channel
tdl chat export -c @WallStreetBets -T last -i 20 --all --with-content -o /tmp/wsb.json

# Messages from the last 24 hours (adjust timestamps)
tdl chat export -c @MarketNews -T time -i $(date -d '24 hours ago' +%s),$(date +%s) --all --with-content -o /tmp/market.json

# macOS timestamp variant
tdl chat export -c @MarketNews -T time -i $(date -v-24H +%s),$(date +%s) --all --with-content -o /tmp/market.json

# Export from a topic in a group
tdl chat export -c @CryptoGroup --topic 42 -T last -i 30 --all --with-content -o /tmp/crypto.json
```

## Useful Patterns

### Read latest news from multiple channels

```bash
# Export from each channel
for channel in "@Channel1" "@Channel2" "@Channel3"; do
  tdl chat export -c "$channel" -T last -i 10 --all --with-content -o "/tmp/tdl-${channel#@}.json"
done
```

### Find a channel then read it

```bash
# Step 1: Find the channel
tdl chat ls -f "VisibleName contains 'crypto'" -o json

# Step 2: Export messages (use the ID or username from step 1)
tdl chat export -c @found_channel -T last -i 20 --all --with-content -o /tmp/export.json
```

### Unix timestamp helpers

```bash
# macOS: 24 hours ago
date -v-24H +%s

# macOS: 7 days ago
date -v-7d +%s

# macOS: specific date
date -j -f "%Y-%m-%d" "2026-03-01" +%s

# Linux: 24 hours ago
date -d '24 hours ago' +%s

# Linux: specific date
date -d '2026-03-01' +%s

# Current time
date +%s
```
