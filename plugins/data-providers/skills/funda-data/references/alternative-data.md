# Alternative Data Reference

Social sentiment (Twitter, Reddit), prediction markets (Polymarket), government trading, and ownership data.

---

## GET /v1/twitter-posts

Tweets from financial KOLs (key opinion leaders).

### Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `author_username` | string | - | Filter by username (exact match) |
| `ticker` | string | - | Filter by ticker |
| `lang` | string | - | Language code (e.g., `en`, `zh`) |
| `is_reply` | bool | - | Filter replies |
| `is_retweet` | bool | - | Filter retweets |
| `is_quote` | bool | - | Filter quote tweets |
| `search` | string | - | Search tweet text (case-insensitive) |
| `tweeted_after` | datetime | - | ISO 8601 datetime |
| `tweeted_before` | datetime | - | ISO 8601 datetime |
| `order` | string | `-tweeted_at` | Sort field |
| `page` | int | 0 | Page (0-based) |
| `page_size` | int | 20 | Items per page (max: 1000) |

Response fields: `tweet_id`, `url`, `author_username`, `author_name`, `text`, `lang`, `retweet_count`, `reply_count`, `like_count`, `view_count`, `tickers`, `tweeted_at`.

### GET /v1/twitter-posts/{id}

Full details including `entities`, `quoted_tweet`, author profile.

```bash
# Tweets mentioning AAPL
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/twitter-posts?ticker=AAPL&page_size=10"

# Search tweets
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/twitter-posts?search=nvidia+earnings&page_size=10"
```

---

## GET /v1/reddit-posts

Reddit posts from finance subreddits (wallstreetbets, stocks, etc.).

### Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `subreddit` | string | - | Filter by subreddit |
| `author` | string | - | Filter by author |
| `ticker` | string | - | Filter by ticker |
| `is_self` | bool | - | Text post (true) or link post (false) |
| `link_flair_text` | string | - | Filter by flair (e.g., `DD`, `Discussion`, `YOLO`) |
| `search` | string | - | Search post title (case-insensitive) |
| `posted_after` | datetime | - | ISO 8601 datetime |
| `posted_before` | datetime | - | ISO 8601 datetime |
| `order` | string | `-posted_at` | Sort field |
| `page` | int | 0 | Page (0-based) |
| `page_size` | int | 20 | Max: 1000 |

Response fields: `post_id`, `subreddit`, `author`, `title`, `selftext`, `link_flair_text`, `score`, `upvote_ratio`, `num_comments`, `tickers`, `posted_at`.

## GET /v1/reddit-comments

Reddit comments from finance subreddits.

### Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `subreddit` | string | - | Filter by subreddit |
| `post_id` | string | - | Filter by post ID |
| `author` | string | - | Filter by author |
| `ticker` | string | - | Filter by ticker |
| `search` | string | - | Search comment body |
| `commented_after` | datetime | - | ISO 8601 |
| `commented_before` | datetime | - | ISO 8601 |
| `order` | string | `-commented_at` | Sort |
| `page` | int | 0 | Page |
| `page_size` | int | 20 | Max: 1000 |

```bash
# WSB posts about TSLA
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/reddit-posts?subreddit=wallstreetbets&ticker=TSLA&page_size=10"

# DD posts on r/stocks
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/reddit-posts?subreddit=stocks&link_flair_text=DD&page_size=10"
```

---

## GET /v1/polymarket/markets

Search prediction markets from Polymarket.

### Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | - | Search in question/description |
| `active` | bool | - | Filter active markets |
| `closed` | bool | - | Filter closed markets |
| `tag` | string | - | Filter by tag (crypto, sports, politics) |
| `order` | string | - | Sort (volume24hr, liquidity, createdAt) |
| `ascending` | bool | false | Sort direction |
| `limit` | int | 20 | Max: 100 |
| `offset` | int | 0 | Pagination offset |

Response fields: `id`, `question`, `outcomes`, `outcome_prices`, `volume`, `volume_24hr`, `liquidity`, `active`, `closed`, `end_date`.

## GET /v1/polymarket/events

Search prediction market events (groups of related markets).

Same parameters as `/markets`. Response additionally includes a `markets` array with nested market details.

```bash
# Bitcoin prediction markets
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/polymarket/markets?keyword=bitcoin&active=true&order=volume24hr"

# Political events
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/polymarket/events?tag=politics&active=true"
```

---

## GET /v1/government-trading

Congressional stock trades (Senate & House).

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Data type (see below) |
| `ticker` | string | No | Stock ticker |
| `name` | string | No | Member name (for by-name types) |
| `page` | int | No | Page (0-based) |
| `limit` | int | No | Max results (default: 20) |

### Types

| Type | Description |
|---|---|
| `senate-latest` | Latest Senate trades |
| `house-latest` | Latest House trades |
| `senate-trades` | Senate trades for a ticker |
| `senate-trades-by-name` | Senate trades by member name |
| `house-trades` | House trades for a ticker |
| `house-trades-by-name` | House trades by member name |

Response fields: `disclosureDate`, `transactionDate`, `ticker`, `name`, `assetDescription`, `type` (Purchase/Sale), `amount`, `representative`, `district`.

```bash
# Latest Senate trades
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/government-trading?type=senate-latest&limit=20"

# Congressional trades in NVDA
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/government-trading?type=senate-trades&ticker=NVDA"
```

---

## GET /v1/ownership

Institutional ownership (13F) and insider trades (Form 4).

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Data type (see below) |
| `ticker` | string | No | Stock ticker |
| `cik` | string | No | CIK (for institutional types) |
| `name` | string | No | Insider name (for insider-by-name) |
| `year` | int | No | Year filter |
| `quarter` | int | No | Quarter (1-4) |
| `page` | int | No | Page (0-based) |
| `limit` | int | No | Max results (default: 20) |

### Institutional Types (13F)

| Type | Description |
|---|---|
| `institutional-latest` | Latest institutional holders for a ticker |
| `institutional-extract` | Holdings by CIK or ticker |
| `institutional-filing-dates` | 13F filing dates for a holder |
| `institutional-analytics` | Portfolio analytics for an institution |
| `institutional-holder-performance` | Holder performance summary |
| `institutional-holder-industry` | Industry breakdown |
| `institutional-positions` | Position summary for a ticker |
| `institutional-industry-summary` | Industry-level ownership summary |

### Insider Types (Form 4)

| Type | Description |
|---|---|
| `insider-latest` | Latest insider trades (all tickers) |
| `insider-search` | Insider trades for a ticker |
| `insider-by-name` | Trades by person name |
| `insider-transaction-types` | Transaction type codes |
| `insider-statistics` | Insider trading statistics |
| `insider-acquisition-ownership` | Acquisition of ownership filings |

```bash
# Top institutional holders of AAPL
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/ownership?type=institutional-latest&ticker=AAPL&limit=10"

# Recent insider trades in TSLA
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/ownership?type=insider-search&ticker=TSLA&limit=10"

# Latest insider trades across all stocks
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/ownership?type=insider-latest&limit=20"
```
