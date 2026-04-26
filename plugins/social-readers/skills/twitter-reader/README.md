# twitter-reader

Read-only Twitter/X skill for financial research using [opencli](https://github.com/jackwener/opencli).

## What it does

Reads Twitter/X for financial research — searching market discussions, reading analyst tweets, tracking sentiment, and monitoring financial news. Capabilities include:

- **Home feed / timeline** — read your feed ("For You" or "Following")
- **Search** — find tweets by keyword with relevance or recency filters
- **Trending** — view trending topics for market themes
- **Bookmarks** — view your saved tweets
- **User tweets** — fetch a user's recent posts (chronological)
- **User profiles** — look up users, their followers, and following
- **Tweet threads & articles** — view specific threads and long-form articles
- **Notifications** — read your Twitter notifications

**This skill is read-only.** It does NOT support posting, liking, retweeting, replying, or any write operations.

## Authentication

No API keys needed — opencli reuses your existing Chrome browser session via the Browser Bridge extension. Just be logged into x.com in Chrome.

## Triggers

- "check my feed", "search Twitter for", "show my bookmarks"
- "what are people saying about AAPL", "market sentiment on Twitter"
- "look up @user", "who follows", "fintwit", "what's trending"
- Any mention of Twitter/X in context of financial news or market research

## Platform

Works on **Claude Code** and other CLI-based agents. Does **not** work on Claude.ai — the sandbox restricts network access and binaries required by opencli.

## Setup

```bash
# As a plugin (recommended — installs all skills)
npx plugins add himself65/finance-skills --plugin finance-social-readers

# Or install just this skill
npx skills add himself65/finance-skills --skill twitter-reader
```

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- Node.js >= 21 (for `npm install -g @jackwener/opencli`)
- Chrome with the [Browser Bridge extension](https://github.com/jackwener/opencli/releases) installed (load unpacked from `chrome://extensions` in Developer mode)
- Logged into x.com in Chrome

## Reference files

- `references/commands.md` — Complete read command reference with all flags, research workflows, and usage examples
- `references/schema.md` — Output format documentation and column definitions
