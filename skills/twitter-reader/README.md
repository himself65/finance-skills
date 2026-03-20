# twitter-reader

Read-only Twitter/X skill for financial research using [twitter-cli](https://github.com/jackwener/twitter-cli).

## What it does

Reads Twitter/X for financial research — searching market discussions, reading analyst tweets, tracking sentiment, and monitoring financial news. Capabilities include:

- **Home feed / timeline** — read your feed with filtering options
- **Search** — find tweets by keyword, user, date range, and filters
- **Bookmarks** — view your saved tweets
- **User profiles** — look up users, their tweets, followers, and following
- **Tweet details** — view specific tweets and articles

**This skill is read-only.** It does NOT support posting, liking, retweeting, replying, or any write operations.

## Authentication

No API keys needed — authenticates via your logged-in browser session (Chrome, Arc, Edge, Firefox, Brave). Just be logged into x.com in your browser.

## Triggers

- "check my feed", "search Twitter for", "show my bookmarks"
- "what are people saying about AAPL", "market sentiment on Twitter"
- "look up @user", "who follows", "fintwit"
- Any mention of Twitter/X in context of financial news or market research

## Platform

Works on **Claude Code** and other CLI-based agents. Does **not** work on Claude.ai — the sandbox restricts network access and binaries required by twitter-cli.

## Setup

```bash
npx skills add himself65/finance-skills --skill twitter-reader
```

See the [main README](../../README.md) for more installation options.

## Reference files

- `references/commands.md` — Complete read command reference with all flags, research workflows, and usage examples
- `references/schema.md` — Structured output schema documentation
