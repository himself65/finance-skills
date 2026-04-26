# linkedin-reader

Read-only LinkedIn skill for financial research using [opencli](https://github.com/jackwener/opencli).

## What it does

Reads LinkedIn for financial research — reading professional market commentary, monitoring analyst posts, searching finance/trading jobs, and tracking professional sentiment. Capabilities include:

- **Home feed / timeline** — read posts from your LinkedIn feed (author, headline, text, reactions, comments)
- **Job search** — search LinkedIn job listings with filters for location, experience level, job type, remote/hybrid, date posted, and company

**This skill is read-only.** It does NOT support posting, liking, commenting, connecting, messaging, or any write operations.

## Authentication

No API keys needed — opencli reuses your existing Chrome browser session via the Browser Bridge extension. Just be logged into linkedin.com in Chrome.

## Triggers

- "check my LinkedIn feed", "LinkedIn posts about", "what's on LinkedIn"
- "search LinkedIn for jobs", "finance jobs on LinkedIn", "quant jobs"
- "LinkedIn market sentiment", "what are analysts saying on LinkedIn"
- "who's hiring in finance", "professional network buzz"
- Any mention of LinkedIn in context of financial news, market research, or job searches

## Platform

Works on **Claude Code** and other CLI-based agents. Does **not** work on Claude.ai — the sandbox restricts network access and binaries required by opencli.

## Setup

```bash
# As a plugin (recommended — installs all skills)
npx plugins add himself65/finance-skills --plugin finance-social-readers

# Or install just this skill
npx skills add himself65/finance-skills --skill linkedin-reader
```

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- Node.js >= 21 (for `npm install -g @jackwener/opencli`)
- Chrome with the [Browser Bridge extension](https://github.com/jackwener/opencli/releases) installed (load unpacked from `chrome://extensions` in Developer mode)
- Logged into linkedin.com in Chrome

## Reference files

- `references/commands.md` — Complete read command reference with all flags, research workflows, and usage examples
