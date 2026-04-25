# AI-Enriched News Reference

AI-processed news articles with sentiment, 3-bullet summaries, importance ratings, developing-story event timelines, and aggregated per-ticker sentiment.

Only articles that have been AI-enriched (have `enriched_at` in metadata) are returned. For raw news, use `/v1/news` or `/v1/stock-news`.

---

## GET /v1/news/ticker

Enriched news articles mentioning a ticker, with AI-generated summaries, importance ratings, and per-ticker sentiment.

### Parameters

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `ticker` | string | Yes | - | Ticker (e.g., `NVDA`) |
| `page` | int | No | 0 | Page (0-based) |
| `page_size` | int | No | 20 | Items per page (1-100) |
| `date_after` | date | No | - | Filter after this date (inclusive) |
| `date_before` | date | No | - | Filter before this date (exclusive) |

### Example

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/news/ticker?ticker=NVDA&page_size=10"
```

### Response fields (per item)

- `id`, `title`, `source`, `url`, `published_at`, `tickers`
- `summary`: AI-generated 3-bullet array
- `importance_rate`: 1-10 (1=trivial, 10=black-swan)
- `sentiment`: `{direction: positive|negative|neutral, confidence: 0-1, reason, explicit}` for the requested ticker (or `null`)

---

## GET /v1/news/timeline

Event timeline for a ticker — groups related articles into developing events.

### Parameters

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `ticker` | string | Yes | - | Ticker |
| `limit` | int | No | 20 | Max events (1-100) |
| `date_after` | date | No | - | Events created after this date |

### Example

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/news/timeline?ticker=NVDA&limit=10"
```

### Response fields (per event)

- `event_id`, `title`, `summary`, `status` (e.g., `developing`)
- `sectors`, `event_types`, `key_tickers`
- `item_count`, `created_at`
- `articles`: array of `{news_id, title, source, published_at, delta}`

Events are ordered by creation date, most recent first.

---

## GET /v1/news/sentiment

Aggregated sentiment for a ticker over a lookback window, broken down by ticker/sector/market.

### Parameters

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `ticker` | string | Yes | - | Ticker |
| `days` | int | No | 7 | Lookback period (1-90) |

### Example

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/news/sentiment?ticker=NVDA&days=30"
```

### Response

- `ticker`, `period_days`
- `ticker_sentiment`: `{positive, negative, neutral, total, latest: {direction, confidence, reason, explicit}}`
- `sector_sentiment`: array of per-sector counts (empty under V1 sentiment data)
- `market_sentiment`: array of per-market counts (empty under V1 sentiment data)
