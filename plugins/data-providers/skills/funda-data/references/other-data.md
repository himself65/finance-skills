# Other Data Reference

News, market performance, funds, ESG, COT, crowdfunding, market hours, bulk data, stock news.

---

## GET /v1/news

Financial news and press releases.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Data type (see below) |
| `ticker` | string | No | Ticker (for ticker-specific types) |
| `page` | int | No | Page (0-based) |
| `limit` | int | No | Max results (default: 20) |

### Types

| Type | Description |
|---|---|
| `fmp-articles` | All news articles |
| `general-latest` | Latest general market news |
| `press-releases-latest` | Latest press releases |
| `stock-latest` | Latest stock news |
| `crypto-latest` | Latest crypto news |
| `forex-latest` | Latest forex news |
| `press-releases` | Press releases for ticker(s) |
| `stock` | Stock news for ticker(s) |
| `crypto` | Crypto news for coin(s) |
| `forex` | Forex news for pair(s) |

```bash
# AAPL stock news
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/news?type=stock&ticker=AAPL&limit=10"

# Latest market news
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/news?type=general-latest&limit=10"

# TSLA press releases
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/news?type=press-releases&ticker=TSLA&limit=5"
```

---

## GET /v1/market-performance

Sector/industry performance, gainers, losers.

Uses `type` parameter. See full docs at `https://api.funda.ai/docs/market-performance.md`.

---

## GET /v1/funds

ETF/mutual fund holdings, index constituents.

Uses `type` parameter. See full docs at `https://api.funda.ai/docs/funds.md`.

---

## GET /v1/esg

ESG ratings, disclosures, benchmarks.

Uses `type` parameter. See full docs at `https://api.funda.ai/docs/esg.md`.

---

## GET /v1/cot-report

Commitment of Traders reports.

Uses `type` parameter. See full docs at `https://api.funda.ai/docs/cot-report.md`.

---

## GET /v1/crowdfunding

Crowdfunding offerings (Form C/D).

Uses `type` parameter. See full docs at `https://api.funda.ai/docs/crowdfunding.md`.

---

## GET /v1/market-hours

Exchange trading hours and holiday schedules.

Uses `type` parameter. See full docs at `https://api.funda.ai/docs/market-hours.md`.

---

## GET /v1/bulk

Bulk data downloads.

Uses `type` parameter. See full docs at `https://api.funda.ai/docs/bulk.md`.

Note: `earnings-surprises` is available at `/v1/bulk?type=earnings-surprises`.

---

## GET /v1/stock-news

Stock news merged from internal database (moomoo, etc.) and FMP, deduplicated by URL, sorted by published date desc.

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `ticker` | string | Yes | - | Comma-separated tickers (e.g., `AAPL` or `AAPL,MSFT`) |
| `date_after` | date | No | - | Start date (YYYY-MM-DD) |
| `date_before` | date | No | - | End date (YYYY-MM-DD) |
| `page` | int | No | 0 | Page (0-based) |
| `limit` | int | No | 20 | Items per page (1-100) |

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/stock-news?ticker=AAPL,MSFT&limit=10"
```

Response fields per item: `tickers`, `published_at`, `source`, `title`, `image`, `text`, `url`.

> For AI-enriched news (summary, sentiment, importance rating, event timelines), see `references/news-enriched.md` (`/v1/news/ticker`, `/v1/news/timeline`, `/v1/news/sentiment`).

---

> For companies listing (`/v1/companies`), see `references/fundamentals.md`.
> For AI-company recruit signals (`/v1/recruit-*`), see `references/recruit.md`.
