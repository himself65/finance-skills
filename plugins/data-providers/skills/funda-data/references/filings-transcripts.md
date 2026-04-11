# SEC Filings, Transcripts & Research Reports Reference

---

## GET /v1/sec-filings

SEC filings with filtering and pagination.

### Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | - | Filter by ticker |
| `cik` | string | - | Filter by CIK |
| `form_type` | string | - | Filter by type (10-K, 10-Q, 8-K, etc.) |
| `filing_date_after` | date | - | Filed on or after (YYYY-MM-DD) |
| `filing_date_before` | date | - | Filed on or before (YYYY-MM-DD) |
| `accepted_date_after` | datetime | - | Accepted on or after (ISO 8601) |
| `accepted_date_before` | datetime | - | Accepted on or before (ISO 8601) |
| `order` | string | `-filing_date` | Sort field |
| `page` | int | 0 | Page (0-based) |
| `page_size` | int | 20 | Items per page (max: 500) |

Response fields: `id`, `accession_number`, `ticker`, `cik`, `filing_date`, `accepted_date`, `form_type`, `fiscal_year`, `fiscal_quarter`, `filing_index_url`, `primary_doc_url`.

### GET /v1/sec-filings/{filing_id}

Single filing by UUID.

```bash
# AAPL 10-K filings
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/sec-filings?ticker=AAPL&form_type=10-K&page_size=5"

# Recent 8-K filings for any company
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/sec-filings?form_type=8-K&page_size=10"
```

---

## GET /v1/sec-filings-search

Search SEC filings. Uses `type` parameter for filing type. See full docs at `https://api.funda.ai/docs/sec-filings-search.md`.

---

## GET /v1/transcripts

Earnings call and podcast transcripts.

### Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | - | Filter by ticker (earnings only) |
| `year` | int | - | Filter by year (earnings only) |
| `quarter` | int | - | Filter by quarter 1-4 (earnings only) |
| `type` | string | - | `earning_call` or `podcast` |
| `date_after` | date | - | On or after (YYYY-MM-DD) |
| `date_before` | date | - | On or before (YYYY-MM-DD) |
| `order` | string | `-date` | Sort field |
| `page` | int | 0 | Page (0-based) |
| `page_size` | int | 20 | Items per page (max: 1000) |

### Earnings call response fields

`id`, `ticker`, `date`, `year`, `quarter`, `type`, `content` (full text), `content_json` (array of `{speaker, title, text}` objects).

### Podcast response fields

`id`, `type`, `title`, `source_url`, `content`, `content_json` with nested: `podcast`, `episode_title`, `youtube_id`, `url`, `published_at`, `channel_handle`, `segments` (array of `{text, start, duration}`).

### GET /v1/transcripts/{transcript_id}

Single transcript by UUID.

```bash
# AAPL earnings call Q1 2025
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/transcripts?ticker=AAPL&year=2025&quarter=1&type=earning_call"

# Latest podcast transcripts
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/transcripts?type=podcast&page_size=5"

# All transcripts from last month
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/transcripts?date_after=2026-03-01&date_before=2026-03-31"
```

---

## GET /v1/investment-research-reports

Investment research reports with filtering.

### Parameters

| Param | Type | Description |
|---|---|---|
| `ticker` | string | Filter by ticker |

### GET /v1/investment-research-reports/{report_id}

Single report by UUID.

See full docs at `https://api.funda.ai/docs/investment-research-reports.md`.

---

## GET /v1/emails

Research emails with filtering.

### Parameters

| Param | Type | Description |
|---|---|---|
| (various filters) | - | See `https://api.funda.ai/docs/emails.md` |

### GET /v1/emails/{email_id}

Single email with full content.
