---
name: opencli-reader
description: >
  Generic read-only fallback for fetching data via opencli's 90+ built-in adapters when no
  dedicated finance-skill covers the source. Use this skill whenever the user wants data
  from a site that opencli supports but this repo does not have a specialized reader for —
  e.g., Yahoo Finance, Bloomberg, Reuters, Barchart, Eastmoney, Xueqiu, Sinafinance, TDX,
  THS, Reddit, HackerNews, Substack, Medium, Weibo, Bilibili, Xiaohongshu, Zhihu, 36kr,
  Jike, Douban, Bluesky, TikTok, Instagram, Facebook, ProductHunt, arXiv, Google Scholar,
  Spotify podcasts, YouTube, Apple Podcasts, Xiaoyuzhou, Weixin Official Account,
  Gov policy/law archives, Amazon, Taobao, JD, and so on.
  Triggers include: "use opencli to read", "opencli fetch from", "check <site> via opencli",
  "grab the frontpage from hackernews", "read reddit r/wallstreetbets", "fetch Eastmoney
  hot stocks", "pull Xueqiu feed", "get Bloomberg markets headlines", "read Reuters",
  "search arXiv for", "list Substack feed", "fetch Weibo hot", "browse Bilibili hot", any
  request to read data from a site where a specialized skill doesn't exist but opencli does.
  This skill is a FALLBACK — prefer the dedicated twitter-reader, linkedin-reader,
  discord-reader, telegram-reader, or yc-reader skills when the source matches one of them.
  This skill is READ-ONLY — never invoke write operations (post, like, comment, send,
  subscribe, save, upvote, follow, block, delete, reply-dm, etc.).
---

# opencli Reader (Generic Fallback, Read-Only)

Generic fallback for any source opencli supports via its [adapter registry](https://github.com/jackwener/opencli) (90+ sites, growing). Use this skill only when **no dedicated finance-skill covers the source** — the specialized skills (`twitter-reader`, `linkedin-reader`, `discord-reader`, `telegram-reader`, `yc-reader`) are always preferred when the request matches one of them.

**This skill is read-only.** Write commands that opencli exposes (post, like, comment, send, save, upvote, subscribe, follow, delete, reply-dm, etc.) must not be invoked.

---

## Step 1: Decide Whether to Use This Skill

Only use this skill if the request **cannot** be handled by a more specific skill.

| If the user asks about… | Use this skill instead |
|---|---|
| Twitter/X | `twitter-reader` |
| LinkedIn | `linkedin-reader` |
| Discord | `discord-reader` |
| Telegram | `telegram-reader` |
| Y Combinator | `yc-reader` |
| Anything else opencli supports (Yahoo Finance, Bloomberg, Reuters, Reddit, HackerNews, Eastmoney, Xueqiu, Substack, arXiv, etc.) | **this skill** |

If the source is not in opencli's registry either, stop and tell the user the request isn't covered — don't fall back to ad-hoc scraping.

---

## Step 2: Ensure opencli Is Ready

**Current environment status:**

```
!`(command -v opencli && opencli doctor 2>&1 | head -5 && echo "READY" || echo "SETUP_NEEDED") 2>/dev/null || echo "NOT_INSTALLED"`
```

If `NOT_INSTALLED`:

```bash
npm install -g @jackwener/opencli
```

If `SETUP_NEEDED`, guide the user through Browser Bridge setup (only required for adapters whose strategy is `COOKIE`, `HEADER`, `INTERCEPT`, or `UI` — `PUBLIC` and `LOCAL` adapters work without a browser):

1. Download the latest `opencli-extension-v{version}.zip` from the [GitHub Releases page](https://github.com/jackwener/opencli/releases)
2. Unzip it, open `chrome://extensions` in Chrome, enable **Developer mode**
3. Click **Load unpacked** and select the unzipped folder
4. Make sure Chrome is logged into the target site, then re-run `opencli doctor`

Requires Node.js >= 21 (or Bun >= 1.0).

---

## Step 3: Discover the Right Command

**Do not guess command names or flags** — the registry has 500+ commands and changes weekly. Instead:

```bash
# Full registry (grouped by site), machine-readable JSON
opencli list -f json

# Filter to a site
opencli list | grep -i <site>

# Site-level help (all commands + flags)
opencli <site> --help

# Command-level help (positional args + flags + defaults)
opencli <site> <command> --help
```

The `opencli list -f json` entry for each command includes:
- `site` — adapter namespace (e.g., `yahoo-finance`)
- `name` — subcommand (e.g., `quote`)
- `strategy` — `PUBLIC` / `COOKIE` / `HEADER` / `INTERCEPT` / `UI` / `LOCAL` — tells you if a browser login is needed
- `description`, `args`, `columns` — canonical metadata

Use `opencli list -f json` as the source of truth. Never paste a site list into the plan from memory; adapters are added every week.

### Quick map of the most common finance / research sources

The table below is a **shortlist**, not exhaustive — always confirm with `opencli <site> --help`.

| Source | Site slug | Common commands |
|---|---|---|
| Yahoo Finance | `yahoo-finance` | `quote` |
| Bloomberg | `bloomberg` | `markets`, `economics`, `industries`, `tech`, `politics`, `opinions`, `news`, `businessweek`, `feeds`, `main` |
| Reuters | `reuters` | `search` |
| Eastmoney (东方财富) | `eastmoney` | `quote`, `rank`, `kline`, `sectors`, `etf`, `holders`, `money-flow`, `northbound`, `longhu`, `kuaixun`, `convertible`, `index-board`, `announcement`, `hot-rank` |
| Xueqiu (雪球) | `xueqiu` | `stock`, `hot-stock`, `hot`, `feed`, `comments`, `watchlist`, `search`, `groups`, `fund-snapshot`, `fund-holdings`, `earnings-date`, `kline` |
| Sinafinance | `sinafinance` | (see `--help`) |
| TDX / THS | `tdx`, `ths` | (see `--help`) |
| Barchart (options) | `barchart` | `quote`, `options`, `flow`, `greeks` |
| Reddit | `reddit` | `hot`, `popular`, `frontpage`, `search`, `subreddit`, `read`, `user`, `user-posts`, `user-comments`, `saved` |
| HackerNews | `hackernews` | `top`, `best`, `new`, `ask`, `show`, `jobs`, `user`, `search` |
| Substack | `substack` | `feed`, `publication`, `search` |
| Medium | `medium` | (see `--help`) |
| arXiv | `arxiv` | (see `--help`) |
| Google Scholar | `google-scholar` | (see `--help`) |
| Weibo | `weibo` | (see `--help`) |
| Bilibili | `bilibili` | `hot`, `video` + more |
| Xiaohongshu (小红书) | `xiaohongshu` | (see `--help`) |
| Zhihu | `zhihu` | (see `--help`) |
| 36kr | `36kr` | (see `--help`) |
| Jike | `jike` | (see `--help`) |
| Bluesky | `bluesky` | (see `--help`) |
| Apple Podcasts | `apple-podcasts` | (see `--help`) |
| Xiaoyuzhou (podcasts) | `xiaoyuzhou` | (see `--help`) |
| Spotify | `spotify` | (see `--help`) |
| YouTube | `youtube` | (see `--help`) |
| Weixin Official Account | `weixin` | (see `--help` — `drafts` is read; `create-draft` is write) |
| Toutiao | `toutiao` | `articles` |
| Government policy / law | `gov-policy`, `gov-law` | (see `--help`) |
| Web download / reader | `web` | `read`, `download` |

For anything not listed, run `opencli list -f json` and filter.

---

## Step 4: Check the Adapter's Strategy Before Running

Run `opencli list -f json` (or `opencli <site> <command> --help`) and read the `strategy` field:

| Strategy | What it means | Preconditions |
|---|---|---|
| `PUBLIC` | Pure HTTP; no browser needed | None |
| `LOCAL` | Talks to a local endpoint | Local service running |
| `COOKIE` / `HEADER` | Reuses your Chrome login for the site | Chrome logged into the site + Browser Bridge extension loaded |
| `INTERCEPT` | Opens an automation window to capture a signed request | Same as COOKIE; be patient — may take several seconds |
| `UI` | Full DOM interaction | Same as COOKIE; slowest; results depend on the site's current layout |

If the user doesn't have a login and the adapter's strategy is not `PUBLIC` / `LOCAL`, tell them they need to log into the site in Chrome before retrying.

---

## Step 5: Execute the Command

### General pattern

```bash
opencli <site> <command> [positional-args] [flags] -f json
```

### Universal flags

| Flag | Effect |
|---|---|
| `-f json` | Structured JSON — always prefer this for agent processing |
| `-f yaml` / `-f csv` / `-f md` / `-f table` / `-f plain` | Other formats |
| `-v` | Verbose logging (also sets `OPENCLI_VERBOSE=1`) |
| `--live` | Keep the automation window open after the command (browser-backed adapters only) |
| `--focus` | Open the automation window in the foreground (browser-backed adapters only) |

Command-specific flags (`--limit`, `--filter`, `--type`, etc.) are **not** universal — always check `opencli <site> <command> --help`.

### Examples

```bash
# Yahoo Finance quote (PUBLIC)
opencli yahoo-finance quote AAPL -f json

# Reddit hot posts in a subreddit (COOKIE or PUBLIC depending on subreddit)
opencli reddit subreddit wallstreetbets --limit 20 -f json
opencli reddit search "SPY options" --limit 15 -f json

# HackerNews top (PUBLIC)
opencli hackernews top --limit 20 -f json

# Eastmoney hot rank (PUBLIC)
opencli eastmoney hot-rank -f json

# Xueqiu hot stocks (PUBLIC or COOKIE)
opencli xueqiu hot-stock -f json
opencli xueqiu stock SH600519 -f json

# Bloomberg markets headlines (COOKIE)
opencli bloomberg markets -f json

# arXiv paper search (PUBLIC)
opencli arxiv search "volatility surface" --limit 10 -f json

# Substack feed
opencli substack feed --limit 20 -f json

# Web page → readable markdown (PUBLIC)
opencli web read "https://example.com/article" -f json
```

### Key rules

1. **Always use `opencli <site> <command> --help`** before constructing a command you haven't run this session — don't assume flag names.
2. **Use `-f json`** for programmatic processing.
3. **Start with a small `--limit`** (10–20) to validate the shape before pulling more.
4. **Check `strategy` before running a browser-backed adapter** — if the user isn't logged in, a `COOKIE` / `UI` adapter will fail.
5. **NEVER execute write operations.** Common write command names to avoid across adapters: `post`, `reply`, `comment`, `like`, `unlike`, `upvote`, `save`, `subscribe`, `unsubscribe`, `follow`, `unfollow`, `block`, `unblock`, `delete`, `bookmark`, `unbookmark`, `send`, `create-draft`, `reply-dm`, `accept`. If you're unsure whether a command is read or write, check the `description` in `opencli list -f json`; if it suggests a mutation, skip it.

---

## Step 6: Handle Failures

If a command returns empty or errors out, the site may have changed its selectors / API. opencli has a built-in self-repair loop:

```bash
# Re-run with diagnostic context
OPENCLI_DIAGNOSTIC=1 opencli <site> <command> <args>
```

This emits a structured `RepairContext` that identifies the failing adapter's source path. Possible responses:

1. If the user has the `opencli-autofix` skill installed, tell them to run that skill.
2. If not, suggest they file an issue at https://github.com/jackwener/opencli/issues with the `RepairContext` output.
3. Don't silently fall back to hand-rolled scraping — that hides the bug from the upstream registry.

Rate limits on the target site can also cause empty results; wait and retry.

---

## Step 7: Present the Results

1. **Summarize the data** for the user's actual question, don't just dump the raw JSON.
2. **Include source attribution** — site name + URL for each item where available.
3. **For market data**, surface price / % change / volume / market cap and flag anomalies.
4. **For news/posts**, highlight headlines, timestamps, and key quotes.
5. **For research (arXiv, Scholar)**, include title, authors, abstract, and link.
6. **Treat browser sessions as private** — never echo CDP endpoints, cookies, or auth tokens.

---

## Reference Files

- `references/discovery.md` — How to navigate `opencli list`, `opencli <site> --help`, and the JSON schema of registry entries
- `references/finance-sources.md` — Detailed notes on the finance-heavy adapters (Yahoo Finance, Bloomberg, Eastmoney, Xueqiu, Barchart, Reuters, Reddit, HackerNews) and which commands are read vs write

Read these reference files when you need concrete examples for a specific site, or when the user asks for a capability not covered by one of the dedicated readers.
