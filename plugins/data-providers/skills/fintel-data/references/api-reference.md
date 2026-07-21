# Fintel Public Data API — Endpoint Reference

Base URL: `https://api.fintel.io`
Auth: `X-API-KEY: $FINTEL_API_KEY` header on every request (the legacy
`auth` header is accepted for compatibility; prefer `X-API-KEY`).
Docs: https://api.fintel.io/docs · OpenAPI: https://api.fintel.io/openapi.json
MCP: `https://mcp.fintel.io/mcp` (canonical) or `https://api.fintel.io/mcp`
(secondary) — JSON-RPC 2.0 over HTTP POST, same auth header, same
entitlements, tool names in the tables below.

All endpoints in this file are **GET** and read-only. Required
parameters are marked `*`. Path params `{country}` (ISO code, e.g. `us`)
and `{symbol}` (ticker, e.g. `AAPL`) apply to every `/v1/securities/...`
endpoint and are not repeated in the tables.

Error envelope: `{"error": {"code": "...", "message": "..."}}`.
Common codes: `unauthorized` (401, missing/invalid/revoked key —
response carries `WWW-Authenticate: ApiKey realm="fintel-api"`), 403
(dataset not enabled for the account), `not_available` (503, downstream
service down — retry later). Success responses may carry a `meta` object
with `warnings`, `status`, and freshness/provenance metadata.

---

## Security Master & Reference

| Endpoint | MCP tool | Params | Description |
|---|---|---|---|
| `/v1/securities` | `fintel.search_securities` | `query`* (ticker exact, name prefix, or exact CUSIP/ISIN/FIGI), `country`, `limit` (1-100, default 25) | Search the security master; returns active securities |
| `/v1/securities/{country}/{symbol}` | `fintel.get_security` | — | Full profile incl. `security_identifiers` history and `security_listings` on other exchanges |
| `/v1/identifiers/{type}/{value}` | `fintel.lookup_identifier` | `type`*: `cusip`, `isin`, `ticker`, `id`; `value`* | Resolve an external identifier to a security profile |
| `/v1/countries` | `fintel.list_countries` | — | Countries with active securities + counts |
| `/v1/countries/{countryCode}/securities` | `fintel.list_country_securities` | `limit`, `page` | Active securities in a country (alias: `/v1/countries/{countryCode}`) |
| `/v1/exchanges` | `fintel.list_exchanges` | — | Exchanges with active securities + counts |
| `/v1/exchanges/{exchangeCode}/securities` | `fintel.list_exchange_securities` | `limit`, `page` | Active securities on an exchange (alias: `/v1/exchanges/{exchangeCode}`) |

```bash
curl -s -H "X-API-KEY: $FINTEL_API_KEY" "https://api.fintel.io/v1/securities?query=apple&country=us&limit=5"
curl -s -H "X-API-KEY: $FINTEL_API_KEY" "https://api.fintel.io/v1/identifiers/cusip/037833100"
```

## Market Data / Prices

| Endpoint | MCP tool | Params | Description |
|---|---|---|---|
| `/v1/securities/{country}/{symbol}/eod` | `fintel.get_price_bars` | `period`: `1m`, `3m`, `6m`, `1y` (default), `2y`, `3y`, `5y`, `all` | EOD adjusted daily price bars |
| `/v1/securities/{country}/{symbol}/last-price` | `fintel.get_last_price` | `session`: `regular` (default), `pre`, `post`, `extended` | Latest trade price + previous close, daily change abs/pct, intraday high/low, WTD/MTD/YTD change, 52-week high/low with distance, volume, avg volume. US listings use intraday tick tape when available; otherwise degrades to latest EOD close with `meta.warnings=["quote_stale"]` |

## Short Interest & Borrow

Fintel's signature datasets. All trailing-year unless noted.

| Endpoint | MCP tool | Params | Description |
|---|---|---|---|
| `/v1/securities/{country}/{symbol}/short-interest` | `fintel.get_short_interest` | — | Exchange-reported short interest (NYSE/NASDAQ-derived). **Limited availability: disabled for general use, must be enabled per account** — expect 403 otherwise |
| `/v1/securities/{country}/{symbol}/borrow-rate` | `fintel.get_borrow_rate` | — | Latest securities-lending borrow rate: fee rate, rebate rate, shares available to borrow |
| `/v1/securities/{country}/{symbol}/short-volume` | `fintel.get_short_volume` | — | Daily short-sale volume: short volume, short-exempt volume, total volume |
| `/v1/securities/{country}/{symbol}/fails-to-deliver` | `fintel.get_fails_to_deliver` | — | SEC fails-to-deliver records (US securities): fail quantity and price |

```bash
curl -s -H "X-API-KEY: $FINTEL_API_KEY" "https://api.fintel.io/v1/securities/us/GME/borrow-rate"
curl -s -H "X-API-KEY: $FINTEL_API_KEY" "https://api.fintel.io/v1/securities/us/GME/short-volume"
```

## Ownership & Insiders

| Endpoint | MCP tool | Params | Description |
|---|---|---|---|
| `/v1/securities/{country}/{symbol}/owners` | `fintel.get_security_owners` | — | Current institutional owners (SEC 13F-derived) |
| `/v1/securities/{country}/{symbol}/insiders` | `fintel.get_security_insiders` | `count` | Reported insider transactions (SEC Form 3/4/5-derived) |

## Fundamentals

| Endpoint | MCP tool | Params | Description |
|---|---|---|---|
| `/v1/securities/{country}/{symbol}/dividends` | `fintel.get_security_dividends` | — | Historical dividend payments |
| `/v1/securities/{country}/{symbol}/earnings` | `fintel.get_security_earnings` | — | Historical earnings reports and surprises |
| `/v1/securities/{country}/{symbol}/data-points/{key}` | `fintel.get_security_data_point` | `key`* — a data-dictionary key | One financial metric by key; discover keys via data definitions below |

## Analyst Estimates

| Endpoint | MCP tool | Params | Description |
|---|---|---|---|
| `/v1/securities/{country}/{symbol}/price-targets` | `fintel.get_security_price_targets` | — | Analyst price targets: high, low, mean, median |
| `/v1/securities/{country}/{symbol}/analyst-ratings` | `fintel.get_security_analyst_ratings` | — | Aggregated buy/hold/sell recommendations |
| `/v1/securities/{country}/{symbol}/forecast` | `fintel.get_security_forecast` | — | Aggregated revenue and earnings forecasts |

## Calendars

Date rules for all four: `from` (ISO-8601, default today), `to` (default
`from` + 7 days, **max window 90 days**), `limit` (1-1000, default 100).

| Endpoint | MCP tool | Description |
|---|---|---|
| `/v1/calendar/earnings` | `fintel.get_earnings_calendar` | Market-wide earnings events |
| `/v1/calendar/dividends` | `fintel.get_dividend_calendar` | Market-wide dividend events |
| `/v1/securities/{country}/{symbol}/calendar/earnings` | `fintel.get_security_earnings_calendar` | One security's earnings events |
| `/v1/securities/{country}/{symbol}/calendar/dividends` | `fintel.get_security_dividend_calendar` | One security's dividend events |

```bash
curl -s -H "X-API-KEY: $FINTEL_API_KEY" "https://api.fintel.io/v1/calendar/earnings?from=2026-07-21&to=2026-07-28&limit=200"
```

## Leaderboards

| Endpoint | MCP tool | Params | Description |
|---|---|---|---|
| `/v1/leaderboards` | `fintel.list_leaderboards` | — | All available leaderboards (top/bottom performers by category) |
| `/v1/leaderboards/{key}` | `fintel.get_leaderboard` | — | Leaderboard metadata |
| `/v1/leaderboards/{key}/entries` | `fintel.get_leaderboard` | `limit` (1-500, default 50) | Ordered current entries. 503 `not_available` = ranking service down, retry later (not an empty result). `meta.status="beta"` = served from stub dataset |

## Data Definitions (data dictionary)

| Endpoint | MCP tool | Params | Description |
|---|---|---|---|
| `/v1/data-definitions` | `fintel.list_data_definitions` | `query`, `tag`, `limit`, `page` | Search available metrics/attributes |
| `/v1/data-definitions/{key}` | `fintel.get_data_definition` | — | Detail for one metric/attribute key |

## Account & Application State (read-only subset)

| Endpoint | MCP tool | Description |
|---|---|---|
| `/v1/account` | `fintel.get_account` | Account profile and entitlements |
| `/v1/stock-lists` | `fintel.list_stock_lists` | User's stock lists (watchlists) |
| `/v1/stock-lists/{stockListId}` | `fintel.get_stock_list` | One stock list |
| `/v1/stock-lists/{stockListId}/items` | `fintel.list_stock_list_items` | Symbols in a list |
| `/v1/stock-lists/{stockListId}/insiders` | — | Insider transactions across a list |
| `/v1/stock-lists/{stockListId}/owners` | — | Institutional owners across a list |
| `/v1/stock-lists/{stockListId}/filings` | — | Filings across a list |
| `/v1/alerts` | `fintel.list_alerts` | User's alerts |
| `/v1/alerts/{alertId}` | `fintel.get_alert` | One alert |
| `/v1/alert-messages` | `fintel.list_alert_messages` | Fired alert messages |
| `/v1/alert-definitions` | — | Available alert definitions |
| `/v1/screens` | — | User's saved screens |
| `/v1/follows` | — | User's follows |
| `/v1/teams`, `/v1/teams/{teamId}`, `/v1/teams/{teamId}/members` | `fintel.list_teams`, `fintel.get_team`, `fintel.get_team_members` | Team collaboration (read) |

The API also exposes write endpoints on these resources (POST/PUT/PATCH/
DELETE for stock lists, alert subscriptions, teams, documents, topics).
**This skill never calls them** — read-only by policy.

## MCP Notes

- Protocol: JSON-RPC 2.0 over HTTP POST to `https://mcp.fintel.io/mcp`.
- Same auth (`X-API-KEY` header), same entitlements, same backend as REST
  ("one data contract, two front doors").
- `tools/list` returns the account-aware live catalog — tools the key is
  actually entitled to. The public (unauthenticated) capability catalog
  is at https://mcp.fintel.io/#capabilities.
- Example raw call:
  ```bash
  curl -s -X POST https://mcp.fintel.io/mcp \
    -H "Content-Type: application/json" -H "X-API-KEY: $FINTEL_API_KEY" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
  ```
