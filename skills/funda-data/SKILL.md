---
name: funda-data
description: >
  Fetch financial data from the Funda AI API (https://api.funda.ai).
  Covers quotes, historical prices, financials, SEC filings, earnings transcripts,
  analyst estimates, options flow/greeks/GEX, supply chain graph, social sentiment,
  prediction markets, congressional trades, economic indicators, ESG, and news.
  Triggers: stock quotes, fundamentals, balance sheet, income statement, cash flow,
  analyst targets, DCF, options chain/flow/unusual activity, GEX, IV rank, max pain,
  earnings/dividend/IPO calendar, SEC filings (10-K/10-Q/8-K), transcripts,
  supply chain (suppliers/customers/competitors), congressional trading,
  insider trades, institutional holdings (13F), Reddit/Twitter sentiment,
  Polymarket, treasury rates, GDP, CPI, FRED data, ESG scores,
  commodity/forex/crypto prices, stock screener, sector performance,
  ETF holdings, news, COT reports. Also triggers for "funda" or "funda.ai".
  If only a ticker is provided and Funda API can answer, use this skill.
---

# Funda Data API Skill

Query the [Funda AI](https://api.funda.ai) financial data API for stocks, options, fundamentals, alternative data, and more.

**Base URL:** `https://api.funda.ai/v1`
**Auth:** `Authorization: Bearer <API_KEY>` header on all `/v1/*` endpoints.
**Pricing:** This is a paid API. A Funda AI subscription is required. See [funda.ai](https://funda.ai) for pricing details.

---

## Step 1: Check API Key Availability

```
!`echo $FUNDA_API_KEY | head -c 8 2>/dev/null && echo "...KEY_SET" || echo "KEY_NOT_SET"`
```

If `KEY_NOT_SET`, ask the user for their Funda API key. They can set it via:

```bash
export FUNDA_API_KEY="your-api-key-here"
```

Once the key is available, proceed. All `curl` commands below use `$FUNDA_API_KEY`.

---

## Step 2: Identify What the User Needs

Match the user's request to a data category below, then read the corresponding reference file for full endpoint details, parameters, and response schemas.

### Market Data & Prices

| User Request | Endpoint | Reference |
|---|---|---|
| Real-time quote, current price | `GET /v1/quotes?type=realtime&ticker=X` | `references/market-data.md` |
| Batch quotes for multiple tickers | `GET /v1/quotes?type=batch&ticker=X,Y,Z` | `references/market-data.md` |
| After-hours / aftermarket quote | `GET /v1/quotes?type=aftermarket-quote&ticker=X` | `references/market-data.md` |
| Historical EOD prices | `GET /v1/stock-price?ticker=X&date_after=...&date_before=...` | `references/market-data.md` |
| Intraday candles (1min–4hr) | `GET /v1/charts?type=5min&ticker=X` | `references/market-data.md` |
| Technical indicators (SMA, EMA, RSI, ADX) | `GET /v1/charts?type=sma&ticker=X&period_length=50` | `references/market-data.md` |
| Commodity / forex / crypto quotes | `GET /v1/quotes?type=commodity-quotes` | `references/market-data.md` |

### Company Fundamentals

| User Request | Endpoint | Reference |
|---|---|---|
| Income statement | `GET /v1/financial-statements?type=income-statement&ticker=X` | `references/fundamentals.md` |
| Balance sheet | `GET /v1/financial-statements?type=balance-sheet&ticker=X` | `references/fundamentals.md` |
| Cash flow statement | `GET /v1/financial-statements?type=cash-flow&ticker=X` | `references/fundamentals.md` |
| Key metrics (P/E, ROE, etc.) | `GET /v1/financial-statements?type=key-metrics&ticker=X` | `references/fundamentals.md` |
| Financial ratios | `GET /v1/financial-statements?type=ratios&ticker=X` | `references/fundamentals.md` |
| Revenue segmentation (product/geo) | `GET /v1/financial-statements?type=revenue-product-segmentation&ticker=X` | `references/fundamentals.md` |
| Company profile, executives, market cap | `GET /v1/company-details?type=profile&ticker=X` | `references/fundamentals.md` |
| Company search by symbol/name | `GET /v1/search?type=symbol&query=X` | `references/fundamentals.md` |
| Stock screener (market cap, sector, etc.) | `GET /v1/search?type=screener&marketCapMoreThan=...` | `references/fundamentals.md` |

### Analyst & Valuation

| User Request | Endpoint | Reference |
|---|---|---|
| Analyst estimates (EPS, revenue) | `GET /v1/analyst?type=estimates&ticker=X` | `references/fundamentals.md` |
| Price targets | `GET /v1/analyst?type=price-target-summary&ticker=X` | `references/fundamentals.md` |
| Analyst grades (buy/hold/sell) | `GET /v1/analyst?type=grades&ticker=X` | `references/fundamentals.md` |
| DCF valuation | `GET /v1/analyst?type=dcf&ticker=X` | `references/fundamentals.md` |
| Ratings snapshot | `GET /v1/analyst?type=ratings-snapshot&ticker=X` | `references/fundamentals.md` |

### Options Data

| User Request | Endpoint | Reference |
|---|---|---|
| Option chains | `GET /v1/options/stock?ticker=X&type=option-chains` | `references/options.md` |
| Option contracts (volume, OI, premium) | `GET /v1/options/stock?ticker=X&type=option-contracts` | `references/options.md` |
| Greeks per strike/expiry | `GET /v1/options/stock?ticker=X&type=greeks&expiry=...` | `references/options.md` |
| GEX / gamma exposure | `GET /v1/options/stock?ticker=X&type=greek-exposure` | `references/options.md` |
| Spot GEX (per-minute) | `GET /v1/options/stock?ticker=X&type=spot-gex` | `references/options.md` |
| IV rank, IV term structure | `GET /v1/options/stock?ticker=X&type=iv-rank` | `references/options.md` |
| Max pain | `GET /v1/options/stock?ticker=X&type=max-pain` | `references/options.md` |
| Options flow / recent trades | `GET /v1/options/stock?ticker=X&type=flow-recent` | `references/options.md` |
| Unusual options activity (flow alerts) | `GET /v1/options/flow-alerts?is_sweep=true&min_premium=100000` | `references/options.md` |
| Options screener (hottest chains) | `GET /v1/options/screener?min_volume=1000` | `references/options.md` |
| Contract-level flow/history | `GET /v1/options/contract?contract_id=X&type=flow` | `references/options.md` |
| Net premium ticks | `GET /v1/options/stock?ticker=X&type=net-prem-ticks` | `references/options.md` |
| OI change | `GET /v1/options/stock?ticker=X&type=oi-change` | `references/options.md` |
| NOPE indicator | `GET /v1/options/stock?ticker=X&type=nope` | `references/options.md` |

### Supply Chain Knowledge Graph

| User Request | Endpoint | Reference |
|---|---|---|
| Supply chain stocks | `GET /v1/supply-chain/stocks?ticker=X` | `references/supply-chain.md` |
| Bottleneck stocks | `GET /v1/supply-chain/stocks/bottlenecks` | `references/supply-chain.md` |
| Upstream suppliers | `GET /v1/supply-chain/kg-edges/graph/suppliers/X?depth=2` | `references/supply-chain.md` |
| Downstream customers | `GET /v1/supply-chain/kg-edges/graph/customers/X?depth=2` | `references/supply-chain.md` |
| Competitors | `GET /v1/supply-chain/kg-edges/graph/competitors/X` | `references/supply-chain.md` |
| Partners | `GET /v1/supply-chain/kg-edges/graph/partners/X` | `references/supply-chain.md` |
| All neighbors (1-hop) | `GET /v1/supply-chain/kg-edges/graph/neighbors/X` | `references/supply-chain.md` |
| KG edges (relationships) | `GET /v1/supply-chain/kg-edges?source_ticker=X` | `references/supply-chain.md` |

### Social Sentiment & Alternative Data

| User Request | Endpoint | Reference |
|---|---|---|
| Financial Twitter/KOL tweets | `GET /v1/twitter-posts?ticker=X` | `references/alternative-data.md` |
| Reddit posts (wallstreetbets, etc.) | `GET /v1/reddit-posts?subreddit=wallstreetbets&ticker=X` | `references/alternative-data.md` |
| Reddit comments | `GET /v1/reddit-comments?ticker=X` | `references/alternative-data.md` |
| Polymarket prediction markets | `GET /v1/polymarket/markets?keyword=bitcoin` | `references/alternative-data.md` |
| Polymarket events | `GET /v1/polymarket/events?keyword=election` | `references/alternative-data.md` |
| Congressional/government trades | `GET /v1/government-trading?type=senate-latest` | `references/alternative-data.md` |
| Insider trades (Form 4) | `GET /v1/ownership?type=insider-search&ticker=X` | `references/alternative-data.md` |
| Institutional holdings (13F) | `GET /v1/ownership?type=institutional-latest&ticker=X` | `references/alternative-data.md` |

### SEC Filings & Transcripts

| User Request | Endpoint | Reference |
|---|---|---|
| SEC filings (10-K, 10-Q, 8-K) | `GET /v1/sec-filings?ticker=X&form_type=10-K` | `references/filings-transcripts.md` |
| Search SEC filings | `GET /v1/sec-filings-search?type=8-K&ticker=X` | `references/filings-transcripts.md` |
| Earnings call transcripts | `GET /v1/transcripts?ticker=X&type=earning_call` | `references/filings-transcripts.md` |
| Podcast transcripts | `GET /v1/transcripts?type=podcast` | `references/filings-transcripts.md` |
| Investment research reports | `GET /v1/investment-research-reports?ticker=X` | `references/filings-transcripts.md` |

### Calendar & Events

| User Request | Endpoint | Reference |
|---|---|---|
| Upcoming earnings | `GET /v1/calendar?type=earnings-calendar&date_after=...` | `references/calendar-economics.md` |
| Dividend calendar | `GET /v1/calendar?type=dividends-calendar&date_after=...` | `references/calendar-economics.md` |
| IPO calendar | `GET /v1/calendar?type=ipos-calendar` | `references/calendar-economics.md` |
| Stock splits | `GET /v1/calendar?type=splits-calendar` | `references/calendar-economics.md` |
| Economic calendar | `GET /v1/calendar?type=economic-calendar` | `references/calendar-economics.md` |

### Economics & Macro

| User Request | Endpoint | Reference |
|---|---|---|
| Treasury rates | `GET /v1/economics?type=treasury-rates` | `references/calendar-economics.md` |
| GDP, CPI, unemployment, etc. | `GET /v1/economics?type=indicators&indicator=GDP` | `references/calendar-economics.md` |
| FRED series data | `GET /v1/fred?type=...` | `references/calendar-economics.md` |
| Market risk premium | `GET /v1/economics?type=market-risk-premium` | `references/calendar-economics.md` |

### Other Data

| User Request | Endpoint | Reference |
|---|---|---|
| News (stock, crypto, forex) | `GET /v1/news?type=stock&ticker=X` | `references/other-data.md` |
| Press releases | `GET /v1/news?type=press-releases&ticker=X` | `references/other-data.md` |
| Market performance (gainers/losers) | `GET /v1/market-performance?type=gainers` | `references/other-data.md` |
| ETF/fund holdings | `GET /v1/funds?type=etf-holdings&ticker=X` | `references/other-data.md` |
| ESG ratings | `GET /v1/esg?type=ratings&ticker=X` | `references/other-data.md` |
| COT reports | `GET /v1/cot-report?type=...` | `references/other-data.md` |
| Crowdfunding | `GET /v1/crowdfunding?type=...` | `references/other-data.md` |
| Market hours | `GET /v1/market-hours?type=...` | `references/other-data.md` |
| Bulk data downloads | `GET /v1/bulk?type=...` | `references/other-data.md` |
| Companies list | `GET /v1/companies` | `references/other-data.md` |

---

## Step 3: Make the API Call

Use `curl` with the bearer token to call the Funda API. Read the appropriate reference file first for exact parameter names and response formats.

**Template:**

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/<endpoint>?<params>" | python3 -m json.tool
```

**Response format:** All endpoints return `{"code": "0", "message": "", "data": ...}`. Check that `code` is `"0"` — non-zero means an error occurred (the `message` field explains why).

**Pagination:** List endpoints return `{"items": [...], "page": 0, "page_size": 20, "next_page": 1, "total_count": N}`. Pages are 0-based. `next_page` is `-1` when there are no more pages.

---

## Step 4: Handle Common Patterns

### Multiple data points for one ticker

If the user asks a broad question like "tell me about AAPL", combine several calls:
1. Real-time quote (`/v1/quotes?type=realtime&ticker=AAPL`)
2. Company profile (`/v1/company-details?type=profile&ticker=AAPL`)
3. Key metrics TTM (`/v1/financial-statements?type=key-metrics-ttm&ticker=AAPL`)
4. Analyst price target (`/v1/analyst?type=price-target-summary&ticker=AAPL`)

### Comparing multiple tickers

Use batch quotes for prices, then individual calls for fundamentals. The batch endpoint accepts comma-separated tickers: `/v1/quotes?type=batch&ticker=AAPL,MSFT,GOOGL`.

### Ticker lookup

If the user provides a company name instead of a ticker, search first:
```
GET /v1/search?type=name&query=nvidia
```

---

## Step 5: Respond to the User

Present the data clearly:
- Format numbers with appropriate precision (prices to 2 decimals, ratios to 2-4 decimals, large numbers with commas or abbreviations like $2.8T)
- Use tables for comparative data
- Highlight key insights (e.g., "Trading above/below analyst target", "Earnings beat/miss")
- For time series data, summarize the trend rather than dumping raw numbers
- Always note the data source: "Data from Funda AI API"
- Never provide trading recommendations — present the data and let the user draw conclusions

---

## Reference Files

- `references/market-data.md` — Quotes, historical prices, charts, technical indicators
- `references/fundamentals.md` — Financial statements, company details, search/screener, analyst data
- `references/options.md` — Options chains, greeks, GEX, flow, IV, screener, contract-level data
- `references/supply-chain.md` — Supply chain knowledge graph, relationships, graph traversal
- `references/alternative-data.md` — Twitter, Reddit, Polymarket, government trading, ownership
- `references/filings-transcripts.md` — SEC filings, earnings/podcast transcripts, research reports
- `references/calendar-economics.md` — Calendars (earnings, dividends, IPOs), economics, treasury, FRED
- `references/other-data.md` — News, market performance, funds, ESG, COT, crowdfunding, bulk data
