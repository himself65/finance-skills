# discord

Read-only Discord skill for financial research using [discord-cli](https://github.com/jackwener/discord-cli).

## What it does

Reads Discord for financial research — searching trading server discussions, monitoring crypto/market groups, tracking sentiment in financial communities, and exporting messages for analysis. Capabilities include:

- **Guilds & channels** — list your servers and their channels
- **Message history** — sync and read messages from any channel
- **Search** — find messages by keyword across servers or channels
- **Analytics** — view stats, top senders, and activity timelines
- **Export** — export messages as text or JSON for offline analysis

**This skill is read-only.** It does NOT support sending messages, reacting, editing, deleting, or any write operations.

## Authentication

Uses your Discord token extracted from the local Discord desktop app or browser session. No bot account needed — run `discord auth --save` with Discord open.

## Triggers

- "check my Discord", "search Discord for", "read Discord messages"
- "what's happening in the trading Discord", "show Discord channels"
- "Discord sentiment on BTC", "what are people saying in Discord about AAPL"
- "monitor crypto Discord", "export Discord messages", "list my servers"
- Any mention of Discord in context of financial news or market research

## Platform

Works on **Claude Code** and other CLI-based agents. Does **not** work on Claude.ai — the sandbox restricts network access and binaries required by discord-cli.

## Setup

```bash
npx skills add himself65/finance-skills --skill discord
```

See the [main README](../../README.md) for more installation options.

## Prerequisites

- Python 3.10+
- Discord desktop app running or logged in via browser (for token extraction)

## Reference files

- `references/commands.md` — Complete read command reference with all flags, research workflows, and usage examples
