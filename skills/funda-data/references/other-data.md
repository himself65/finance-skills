# Other Data Reference

News, market performance, funds, ESG, COT, crowdfunding, market hours, bulk data, and companies.

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

Stock news for given tickers. See full docs at `https://api.funda.ai/docs/stock-news.md`.

---

## GET /v1/companies

List companies with pagination.

| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int | 0 | Page (0-based) |
| `page_size` | int | 20 | Items per page (max: 500) |
| `simple` | bool | false | Simplified response |

### GET /v1/companies/{company_id}

Single company by UUID.

---

## GET /v1/recruit-job-postings

AI company job postings (OpenAI, Anthropic, etc.).

| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int | 0 | Page (0-based) |
| `page_size` | int | 20 | Items per page |

See full docs at `https://api.funda.ai/docs/recruit-job-postings.md`.

---

## GET /v1/recruit-jd-classifications

JD classifications with AI-inferred metadata.

See full docs at `https://api.funda.ai/docs/recruit-jd-classifications.md`.

---

## GET /v1/recruit-product-signal-clusters

Product-level hiring signal clusters.

See full docs at `https://api.funda.ai/docs/recruit-product-signal-clusters.md`.

---

## GET /v1/recruit-gtm-products

GTM products extracted from Sales JDs.

See full docs at `https://api.funda.ai/docs/recruit-gtm-products.md`.
