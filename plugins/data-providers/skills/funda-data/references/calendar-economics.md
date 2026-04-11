# Calendar & Economics Reference

---

## GET /v1/calendar

Corporate event calendars and earnings transcripts.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Data type (see below) |
| `ticker` | string | No | Stock ticker |
| `date_after` | string | No | Start date (YYYY-MM-DD) |
| `date_before` | string | No | End date (YYYY-MM-DD) |
| `year` | int | No | Year (for transcripts) |
| `quarter` | int | No | Quarter 1-4 (for transcripts) |
| `page` | int | No | Page (0-based) |
| `limit` | int | No | Max results (default: 20) |

### Calendar Types

| Type | Description |
|---|---|
| `earnings` | Historical earnings (EPS actual vs estimate, revenue) |
| `earnings-calendar` | Upcoming earnings announcements |
| `dividends` | Historical dividend payments |
| `dividends-calendar` | Upcoming dividend dates |
| `ipos-calendar` | Upcoming IPOs |
| `ipos-disclosure` | IPO disclosure documents |
| `ipos-prospectus` | IPO prospectus filings |
| `splits` | Historical stock splits |
| `splits-calendar` | Upcoming stock splits |
| `economic-calendar` | Economic events (Fed, GDP, CPI, etc.) |

### Transcript Types

| Type | Description |
|---|---|
| `transcript-latest` | Latest earnings transcript for a ticker |
| `transcript` | Transcript for specific quarter/year |
| `transcript-dates` | Available transcript dates |
| `transcript-symbols` | Tickers with available transcripts |

### Examples

```bash
# Upcoming earnings this week
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/calendar?type=earnings-calendar&date_after=2026-03-31&date_before=2026-04-04"

# Historical earnings for AAPL
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/calendar?type=earnings&ticker=AAPL&limit=8"

# Dividend calendar
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/calendar?type=dividends-calendar&date_after=2026-04-01&date_before=2026-04-30"

# Economic calendar
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/calendar?type=economic-calendar&date_after=2026-03-31&date_before=2026-04-07"

# Latest earnings transcript
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/calendar?type=transcript-latest&ticker=AAPL"
```

Earnings calendar response fields: `date`, `ticker`, `eps`, `epsEstimated`, `time` (amc/bmo), `revenue`, `revenueEstimated`, `fiscalDateEnding`.

---

## GET /v1/economics

Economic indicators, treasury rates, and market risk premium.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Data type (see below) |
| `indicator` | string | No | Indicator name (for `indicators` type) |
| `date_after` | string | No | Start date (YYYY-MM-DD) |
| `date_before` | string | No | End date (YYYY-MM-DD) |

### Types

| Type | Description |
|---|---|
| `treasury-rates` | U.S. Treasury rates (1M–30Y) |
| `indicators` | Economic indicators (requires `indicator` param) |
| `market-risk-premium` | Market risk premium by country |

### Available Indicators

| Indicator | Description |
|---|---|
| `GDP` | Gross Domestic Product |
| `realGDP` | Real GDP |
| `realGDPPerCapita` | Real GDP per Capita |
| `federalFunds` | Federal Funds Rate |
| `CPI` | Consumer Price Index |
| `inflationRate` | Inflation Rate |
| `retailSales` | Retail Sales |
| `consumerSentiment` | Consumer Sentiment |
| `durableGoods` | Durable Goods Orders |
| `unemploymentRate` | Unemployment Rate |
| `totalNonfarmPayroll` | Nonfarm Payroll |
| `initialClaims` | Initial Jobless Claims |
| `industrialProductionTotalIndex` | Industrial Production Index |
| `newPrivatelyOwnedHousingUnitsStartedTotalUnits` | Housing Starts |
| `totalVehicleSales` | Total Vehicle Sales |
| `smoothedUSRecessionProbabilities` | Recession Probability |
| `30YearFixedRateMortgageAverage` | 30-Year Mortgage Rate |
| `15YearFixedRateMortgageAverage` | 15-Year Mortgage Rate |

### Examples

```bash
# Treasury rates
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/economics?type=treasury-rates&date_after=2026-01-01"

# GDP data
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/economics?type=indicators&indicator=GDP&date_after=2023-01-01"

# Unemployment rate
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/economics?type=indicators&indicator=unemploymentRate"

# CPI
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/economics?type=indicators&indicator=CPI"

# Market risk premium
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/economics?type=market-risk-premium"
```

Treasury rates response fields: `date`, `month1`, `month2`, `month3`, `month6`, `year1`, `year2`, `year3`, `year5`, `year7`, `year10`, `year20`, `year30`.

---

## GET /v1/fred

FRED series data: sector indices, money supply, PCE, trade balance.

Uses `type` parameter. See full docs at `https://api.funda.ai/docs/fred.md`.
