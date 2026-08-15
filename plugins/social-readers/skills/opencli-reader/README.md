# opencli-reader

Generic read-only **fallback** skill for fetching data from any site opencli supports but this repo doesn't have a dedicated reader for. Use when none of the specialized readers (`twitter-reader`, `linkedin-reader`, `discord-reader`, `telegram-reader`, `yc-reader`) match the request.

## What it does

Routes the user's request to the right [opencli](https://github.com/jackwener/opencli) adapter by discovering commands at runtime (`opencli list -f json`, `opencli <site> --help`) instead of relying on a stale hand-maintained list. Covers 100+ sites including:

- **Market data** — Yahoo Finance, Bloomberg, Reuters, Barchart, Eastmoney, Xueqiu, Sinafinance, TDX, THS
- **Community / sentiment** — Reddit, HackerNews, Bluesky, Weibo, Jike, Xiaohongshu, Zhihu, 36kr
- **Long-form / newsletters** — Substack, Medium, generic `web read` fallback
- **Research** — arXiv, Google Scholar, Baidu Scholar, Wanfang, CNKI, gov-law, gov-policy
- **Podcasts / video** — Apple Podcasts, Xiaoyuzhou, Spotify, YouTube, Bilibili
- **Commerce (supply-chain research)** — Amazon, Taobao, JD, 1688, Coupang
- **AI chats** — ChatGPT, Gemini, DeepSeek, Grok (read-only operations)

**This skill is read-only.** Write commands (`post`, `like`, `comment`, `send`, `subscribe`, `save`, `upvote`, `follow`, `delete`, `reply-dm`, `create-draft`, etc.) are never invoked.

## When to use vs. a specialized skill

| Request mentions… | Use this skill? |
|---|---|
| Twitter / X | **No** — use `twitter-reader` |
| LinkedIn | **No** — use `linkedin-reader` |
| Discord | **No** — use `discord-reader` |
| Telegram | **No** — use `telegram-reader` |
| Y Combinator | **No** — use `yc-reader` |
| Anything else opencli supports | **Yes** |

## Triggers

- "use opencli to read from <site>"
- "grab the frontpage from hackernews"
- "read reddit r/wallstreetbets"
- "fetch Eastmoney hot stocks"
- "pull Xueqiu feed"
- "get Bloomberg markets headlines"
- "search arXiv for <topic>"
- "list my Substack feed"
- "browse Bilibili hot"
- Any mention of a source that opencli covers but this repo doesn't have a dedicated skill for

## Platform

Works on **Claude Code** and other CLI-based agents. Does **not** work on Claude.ai — the sandbox restricts network access and binaries required by opencli.

## Setup

```bash
# Choose finance-social-readers when prompted.
npx plugins add himself65/finance-skills

# Or just this skill
npx skills add himself65/finance-skills --skill opencli-reader
```

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- Node.js >= 20 (for `npm install -g @jackwener/opencli`)
- For browser-backed adapters (`COOKIE` / `HEADER` / `INTERCEPT` / `UI` strategies):
  - Chrome with the [Browser Bridge extension](https://github.com/jackwener/opencli/releases) loaded unpacked (Developer mode in `chrome://extensions`)
  - Logged into the target site in Chrome

`PUBLIC` and `LOCAL` adapters work without Chrome.

## Reference files

- `references/discovery.md` — How to navigate `opencli list`, `<site> --help`, and the registry JSON schema; how to distinguish read vs write commands
- `references/finance-sources.md` — Curated notes on finance-relevant adapters (Yahoo Finance, Bloomberg, Eastmoney, Xueqiu, Barchart, Reuters, Reddit, HackerNews, Substack, arXiv, etc.) with the canonical read vs write split
