# telegram

Read-only Telegram skill for financial news and market research using [tdl](https://github.com/iyear/tdl).

## What it does

Reads Telegram channels and groups for financial news — exporting messages, listing channels, and monitoring financial news feeds. Capabilities include:

- **List chats** — view all your Telegram channels, groups, and contacts with filtering
- **Export messages** — read recent messages from any channel or group you've joined
- **Time-range queries** — fetch messages from specific time periods
- **Channel search** — find channels by name or type

**This skill is read-only.** It does NOT support sending messages, joining/leaving channels, or any write operations.

## Authentication

Requires a one-time interactive login via QR code or phone number. After login, the session persists on disk — no further authentication needed.

## Triggers

- "check my Telegram", "read Telegram channel", "Telegram news"
- "what's new in my Telegram channels", "export messages from"
- "financial news on Telegram", "crypto Telegram", "market news Telegram"
- Any mention of Telegram in context of financial news or market research

## Platform

Works on **Claude Code** and other CLI-based agents. Does **not** work on Claude.ai — the sandbox restricts network access and binaries required by tdl.

## Setup

```bash
npx skills add himself65/finance-skills --skill telegram
```

See the [main README](../../README.md) for more installation options.

## Prerequisites

- [tdl](https://github.com/iyear/tdl) installed (`brew install telegram-downloader` on macOS)
- One-time login: `tdl login -T qr` (scan QR code with Telegram mobile app)

## Reference files

- `references/commands.md` — Complete tdl command reference for reading channels and exporting messages
