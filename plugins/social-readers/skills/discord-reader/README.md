# discord-reader

Read-only Discord skill for financial research using [opencli](https://github.com/jackwener/opencli).

## What it does

Reads Discord for financial research — reading trading server messages, searching for market discussions, monitoring crypto/market groups, and tracking sentiment in financial communities. Capabilities include:

- **Servers** — list all joined servers
- **Channels** — list channels in the active server
- **Messages** — read recent messages from the active channel
- **Search** — find messages by keyword in the active channel
- **Members** — list online members in the active server

**This skill is read-only.** It does NOT support sending messages, reacting, editing, deleting, or any write operations.

## Authentication

No bot account or token extraction needed — opencli connects to Discord Desktop via Chrome DevTools Protocol (CDP). Just have Discord running with `--remote-debugging-port=9232`.

## Triggers

- "check my Discord", "search Discord for", "read Discord messages"
- "what's happening in the trading Discord", "show Discord channels"
- "Discord sentiment on BTC", "what are people saying in Discord about AAPL"
- "monitor crypto Discord", "list my servers"
- Any mention of Discord in context of financial news or market research

## Platform

Works on **Claude Code** and other CLI-based agents. Does **not** work on Claude.ai — the sandbox restricts network access and binaries required by opencli.

## Setup

```bash
# As a plugin (recommended — installs all skills)
npx plugins add himself65/finance-skills --plugin finance-social-readers

# Or install just this skill
npx skills add himself65/finance-skills --skill discord-reader
```

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- Node.js 20+ (for `npm install -g @jackwener/opencli`)
- Discord Desktop running with `--remote-debugging-port=9232`
- Environment variable: `export OPENCLI_CDP_ENDPOINT="http://127.0.0.1:9232"`

## Reference files

- `references/commands.md` — Complete read command reference with all flags, research workflows, and usage examples
