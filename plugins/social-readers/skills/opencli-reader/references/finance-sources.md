# Finance-Relevant opencli Adapters

Curated notes on the opencli adapters most useful for financial research, with **read** commands highlighted and **write** commands listed as "do not invoke". Treat these as starting points — always run `opencli <site> <command> --help` to confirm current flags and defaults.

---

## Market data (US)

### `yahoo-finance`

| Command | Read/Write | Purpose |
|---|---|---|
| `quote SYMBOL` | Read | Stock quote — price, change, volume, market cap |

Strategy: `PUBLIC`. No login needed.

```bash
opencli yahoo-finance quote AAPL -f json
opencli yahoo-finance quote MSFT -f json
```

Columns: `symbol`, `name`, `price`, `change`, `changePercent`, `open`, `high`, `low`, `volume`, `marketCap`.

### `barchart`

| Command | Read/Write | Purpose |
|---|---|---|
| `quote SYMBOL` | Read | Equity quote |
| `options SYMBOL` | Read | Options chain |
| `flow SYMBOL` | Read | Unusual options flow |
| `greeks SYMBOL` | Read | Option greeks |

Check `opencli barchart <command> --help` for expiry/strike filters.

### `bloomberg`

| Command | Read/Write | Purpose |
|---|---|---|
| `main` | Read | Bloomberg homepage feed |
| `markets` | Read | Markets section |
| `economics` | Read | Economics section |
| `industries` | Read | Industries section |
| `tech` | Read | Tech section |
| `politics` | Read | Politics section |
| `opinions` | Read | Opinion pieces |
| `news` | Read | General news feed |
| `businessweek` | Read | Businessweek articles |
| `feeds` | Read | RSS-style feeds |

Likely `COOKIE` or `INTERCEPT` — Bloomberg paywalls content for non-subscribers. Run `opencli list | grep bloomberg` to confirm.

### `reuters`

| Command | Read/Write | Purpose |
|---|---|---|
| `search QUERY` | Read | Reuters search |

---

## Market data (China)

### `eastmoney` (东方财富)

13 finance adapters (opencli 1.7.5, Phase A oracle):

| Command | Read/Write | Purpose |
|---|---|---|
| `quote SYMBOL` | Read | A-shares quote |
| `rank` | Read | Gainers / losers rank |
| `hot-rank` | Read | Hot stocks by retail flow |
| `kline SYMBOL` | Read | K-line / OHLCV |
| `sectors` | Read | Sector performance |
| `etf` | Read | ETF list / data |
| `holders SYMBOL` | Read | Top holders |
| `money-flow SYMBOL` | Read | Capital flow |
| `northbound` | Read | Northbound (Stock Connect) flow |
| `longhu` | Read | 龙虎榜 (big-block trading) |
| `kuaixun` | Read | 快讯 (market news flashes) |
| `convertible` | Read | Convertible bonds |
| `index-board` | Read | Index board |
| `announcement SYMBOL` | Read | Company announcements |

Mostly `PUBLIC`.

### `xueqiu` (雪球)

| Command | Read/Write | Purpose |
|---|---|---|
| `stock SYMBOL` | Read | Stock detail (e.g., `SH600519`, `SZ002594`) |
| `hot-stock` | Read | Hot-stock list |
| `hot` | Read | Hot discussion feed |
| `feed` | Read | Homepage feed |
| `comments SYMBOL` | Read | Comments on a stock |
| `watchlist` | Read | User's watchlist (requires login) |
| `search QUERY` | Read | Search across Xueqiu |
| `groups` | Read | Discussion groups |
| `fund-snapshot FUND_CODE` | Read | Fund snapshot |
| `fund-holdings FUND_CODE` | Read | Fund holdings breakdown |
| `earnings-date SYMBOL` | Read | Upcoming earnings date |
| `kline SYMBOL` | Read | K-line data |

Symbol format: exchange prefix + code (e.g., `SH600519` = 贵州茅台 on Shanghai, `SZ002594` = BYD on Shenzhen, `HK00700` = Tencent on HKEX).

### `sinafinance`, `tdx`, `ths`

Chinese brokerage / data provider adapters. Run `opencli <site> --help` to see commands — they change more often than western adapters.

---

## Community forums / sentiment

### `reddit`

| Command | Read/Write | Purpose |
|---|---|---|
| `frontpage` | Read | Reddit front page |
| `hot` | Read | Hot across Reddit |
| `popular` | Read | Popular |
| `subreddit NAME` | Read | Posts from a subreddit (e.g., `wallstreetbets`, `investing`, `SecurityAnalysis`) |
| `read POST_URL_OR_ID` | Read | Full post + comments |
| `search QUERY` | Read | Reddit search |
| `user NAME` | Read | User profile |
| `user-posts NAME` | Read | User's posts |
| `user-comments NAME` | Read | User's comments |
| `saved` | Read | Your saved items (requires login) |
| `subscribe` | **Write** — do not invoke |
| `save` / `upvote` / `comment` | **Write** — do not invoke |

### `hackernews`

| Command | Read/Write | Purpose |
|---|---|---|
| `top` | Read | Top stories |
| `best` | Read | Best stories |
| `new` | Read | Newest stories |
| `ask` | Read | Ask HN |
| `show` | Read | Show HN |
| `jobs` | Read | Who's hiring / job posts |
| `user NAME` | Read | User profile |
| `search QUERY` | Read | HN search (via Algolia) |

All `PUBLIC`. No login needed.

### `bluesky`

Check `opencli bluesky --help` — adapter coverage has been expanding.

### `jike`, `weibo`, `xiaohongshu`, `zhihu`, `douban`, `36kr`

Chinese social + research platforms. Usually `COOKIE`. Run `opencli <site> --help`.

---

## Long-form / newsletters

### `substack`

| Command | Read/Write | Purpose |
|---|---|---|
| `feed` | Read | Your Substack feed (requires login) |
| `publication SLUG` | Read | Posts from a specific publication |
| `search QUERY` | Read | Search Substack |

### `medium`

Run `opencli medium --help`.

### `web read URL`

Renders an arbitrary web page to markdown via opencli's generic reader. Great last-resort fallback when no adapter exists but the page is publicly readable.

```bash
opencli web read "https://example.com/long-article" -f json
```

---

## Research databases

### `arxiv`

Research-paper search on arXiv. Run `opencli arxiv --help` for search flags.

### `google-scholar`, `baidu-scholar`, `wanfang`, `cnki`

Academic search adapters. `COOKIE` for some; `PUBLIC` for others.

### `gov-law`, `gov-policy`

Chinese government legal / policy archives.

---

## Podcasts & video

### `apple-podcasts`, `xiaoyuzhou`, `spotify`, `youtube`

Podcast and video discovery / metadata. Some support full transcript fetching; check `--help`.

### `bilibili`

`hot`, `video`, and more. See `opencli bilibili --help`.

---

## Commerce (for supply-chain / competitive research)

### `amazon`, `taobao`, `jd`, `xianyu`, `1688`, `ke`, `coupang`

Product data, pricing, reviews. Strategies vary. Useful for surfacing competitive or supply-chain signals in equity research.

---

## AI chat tools (for research automation)

### `chatgpt`, `gemini`, `deepseek`, `grok`, `doubao`, `yuanbao`

Browser-based chat adapters. Read operations like `history`, `read`, `status` are safe. Write operations like `ask` send a prompt — allowed for research automation but count them as writes to an external account; prefer local LLM calls when possible.

---

## Full list

Run `opencli list -f json | jq '.[] | .site' | sort -u` for the authoritative list — it's the only source that stays current as adapters are added weekly.
