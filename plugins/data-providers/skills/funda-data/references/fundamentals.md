# Fundamentals, Analyst & Search Reference

## GET /v1/financial-statements

Financial statements, ratios, key metrics, and growth statistics.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Data type (see below) |
| `ticker` | string | Yes | Stock ticker |
| `period` | string | No | `annual` (default) or `quarter` |
| `limit` | int | No | Max results (default: 20) |
| `page` | int | No | Page number (0-based) |
| `year` | int | No | Year filter (for financial-reports-json) |

### Types

| Type | Description |
|---|---|
| `income-statement` | Revenue, expenses, net income |
| `balance-sheet` | Assets, liabilities, equity |
| `cash-flow` | Operating, investing, financing cash flows |
| `latest-financial-statements` | Latest combined financial statements |
| `income-statement-ttm` | Trailing twelve months income statement |
| `balance-sheet-ttm` | TTM balance sheet |
| `cash-flow-ttm` | TTM cash flow |
| `key-metrics` | Key metrics (P/E, P/B, ROE, ROA, etc.) |
| `ratios` | Financial ratios (liquidity, profitability, efficiency) |
| `key-metrics-ttm` | TTM key metrics |
| `ratios-ttm` | TTM ratios |
| `financial-scores` | Piotroski score, Altman Z-score |
| `owner-earnings` | Owner earnings calculation |
| `enterprise-values` | Enterprise value calculations |
| `income-statement-growth` | YoY income statement growth rates |
| `balance-sheet-growth` | YoY balance sheet growth rates |
| `cash-flow-growth` | YoY cash flow growth rates |
| `financial-growth` | Combined financial growth metrics |
| `financial-reports-dates` | Available report dates |
| `financial-reports-json` | Complete report in JSON (specify year, period) |
| `revenue-product-segmentation` | Revenue by product/service line |
| `revenue-geographic-segmentation` | Revenue by geographic region |
| `income-statement-as-reported` | As-reported income statement (GAAP/IFRS) |
| `balance-sheet-as-reported` | As-reported balance sheet |
| `cash-flow-as-reported` | As-reported cash flow |
| `full-as-reported` | Complete as-reported financials |

### Examples

```bash
# Annual income statement (last 5 years)
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/financial-statements?type=income-statement&ticker=AAPL&period=annual&limit=5"

# Quarterly balance sheet
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/financial-statements?type=balance-sheet&ticker=AAPL&period=quarter&limit=4"

# Key metrics TTM
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/financial-statements?type=key-metrics-ttm&ticker=AAPL"

# Revenue by product segment
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/financial-statements?type=revenue-product-segmentation&ticker=AAPL"
```

Key fields in income statement response: `date`, `ticker`, `revenue`, `costOfRevenue`, `grossProfit`, `grossProfitRatio`, `operatingExpenses`, `operatingIncome`, `ebitda`, `netIncome`, `eps`, `epsdiluted`, `weightedAverageShsOutDil`.

Key fields in key-metrics-ttm: `peRatioTTM`, `priceToSalesRatioTTM`, `pbRatioTTM`, `evToSalesTTM`, `enterpriseValueOverEBITDATTM`, `roeTTM`, `roicTTM`, `debtToEquityTTM`, `currentRatioTTM`, `dividendYieldTTM`, `freeCashFlowYieldTTM`.

---

## GET /v1/company-profile

Quick company profile (price, market cap, beta, description, sector, CEO, trading flags). Single-ticker convenience endpoint.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `ticker` | string | Yes | Ticker (e.g., `AAPL`, `NVO`) |

### Example

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/company-profile?ticker=NVO"
```

Key response fields: `ticker`, `price`, `marketCap`, `beta`, `lastDividend`, `range`, `change`, `changePercentage`, `volume`, `averageVolume`, `companyName`, `currency`, `cik`, `isin`, `cusip`, `exchangeFullName`, `exchange`, `industry`, `sector`, `country`, `website`, `description`, `ceo`, `fullTimeEmployees`, `ipoDate`, `isEtf`, `isActivelyTrading`, `isAdr`, `isFund`.

---

## GET /v1/company-details

Company profile, executives, market cap, shares float, M&A history.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Data type (see below) |
| `ticker` | string | No | Stock ticker (required for most types) |
| `cik` | string | No | CIK (required for `profile-cik`) |
| `query` | string | No | Company name (for `mergers-acquisitions-search`) |
| `page` | int | No | Page (0-based, default: 0) |
| `limit` | int | No | Max results (default: 20) |

### Types

| Type | Description |
|---|---|
| `profile` | Company profile |
| `profile-cik` | Company profile by CIK |
| `notes` | Company notes / research commentary |
| `peers` | Peer companies (competitors) |
| `executives` | Key executives and board |
| `executive-compensation` | Executive compensation details |
| `executive-compensation-benchmark` | Compensation industry benchmarks |
| `employee-count` | Current employee count |
| `historical-employee-count` | Historical employee count |
| `market-cap` | Current market cap |
| `batch-market-cap` | Batch market cap (comma-separated tickers) |
| `historical-market-cap` | Historical market cap |
| `shares-float` | Shares float for a ticker |
| `all-shares-float` | Shares float for all companies |
| `delisted` | Delisted companies |
| `mergers-acquisitions-latest` | Latest M&A announcements |
| `mergers-acquisitions-search` | Search M&A by company name |

### Examples

```bash
# Profile
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/company-details?type=profile&ticker=AAPL"

# Executives
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/company-details?type=executives&ticker=AAPL"

# Peer companies
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/company-details?type=peers&ticker=AAPL"
```

---

## GET /v1/search

Search by symbol/name/CIK, stock screener, and market directories.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Data type (see below) |
| `query` | string | No | Search query (for search types) |
| `ticker` | string | No | Ticker (for exchange-variants) |
| `limit` | int | No | Max results (default: 20) |
| `page` | int | No | Page (0-based) |
| `exchange` | string | No | Exchange filter |

### Types

| Type | Description |
|---|---|
| `symbol` | Search by ticker (partial match) |
| `name` | Search by company name (partial match) |
| `cik` | Search by SEC CIK number |
| `cusip` | Search by CUSIP |
| `isin` | Search by ISIN |
| `screener` | Screen by fundamentals (marketCapMoreThan, betaMoreThan, volumeMoreThan, sector, industry, country, exchange) |
| `exchange-variants` | Ticker variants across exchanges |
| `stock-list` | All available stocks |
| `financial-statement-symbols` | Symbols with available financial statements |
| `cik-list` | All company CIK numbers |
| `symbol-changes` | Recent ticker symbol changes |
| `etf-list` | All available ETFs |
| `actively-trading` | Currently trading securities |
| `earnings-transcript-list` | Tickers with earnings call transcripts |
| `available-exchanges` | All supported exchanges |
| `available-sectors` | All sectors |
| `available-industries` | All industries |
| `available-countries` | All supported countries |

### Examples

```bash
# Search by name
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/search?type=name&query=nvidia"

# Stock screener
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/search?type=screener&marketCapMoreThan=1000000000&sector=Technology&limit=10"
```

---

## GET /v1/analyst

Analyst estimates, price targets, grades, and valuation models.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Data type (see below) |
| `ticker` | string | Yes | Stock ticker |
| `period` | string | No | `annual` or `quarter` |
| `limit` | int | No | Max results (default: 20) |
| `page` | int | No | Page (0-based) |

### Types

| Type | Description |
|---|---|
| `estimates` | Analyst EPS and revenue estimates |
| `price-target-summary` | Price target (high, low, median, average) |
| `price-target-consensus` | Price target consensus over time |
| `grades` | Latest analyst grades |
| `grades-historical` | Historical upgrades/downgrades |
| `grades-consensus` | Consensus grade distribution |
| `dcf` | Discounted cash flow valuation |
| `levered-dcf` | Levered DCF valuation |
| `custom-dcf` | Custom DCF with configurable parameters |
| `custom-levered-dcf` | Custom levered DCF with configurable parameters |
| `enterprise-values` | Enterprise value calculations |
| `ratings-snapshot` | Latest company rating (A-F) |
| `ratings-historical` | Historical ratings |

Aliases: `price-target` → `price-target-summary`, `rating`/`ratings` → `ratings-snapshot`.

> **Note:** `earnings-surprises` lives at `/v1/bulk?type=earnings-surprises`, not here.

### Examples

```bash
# Analyst estimates
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/analyst?type=estimates&ticker=AAPL&period=quarter"

# Price targets
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/analyst?type=price-target-summary&ticker=AAPL"

# DCF valuation
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/analyst?type=dcf&ticker=AAPL"

# Latest analyst grades
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/analyst?type=grades&ticker=AAPL&limit=10"
```

---

## GET /v1/companies

List companies with pagination.

### Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int | 0 | Page index (0-based) |
| `page_size` | int | 20 | Items per page (max: 500) |
| `simple` | bool | false | Simplified fields only |

When `simple=true`, returns only: `id`, `ticker`, `company_name`, `industry`.

Full response includes: `id`, `ticker`, `company_name`, `description`, `currency`, `cik`, `isin`, `cusip`, `exchange`, `industry`, `sector`, `website`, `ceo`, `country`, `full_time_employees`, `ipo_date`, `is_etf`, `is_actively_trading`.
