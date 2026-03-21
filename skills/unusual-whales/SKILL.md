---
name: unusual-whales
description: >
  Query the Unusual Whales API for options flow, dark pool trades, congressional trading,
  institutional holdings, insider transactions, Greek exposure, volatility data, stock screener,
  and market sentiment. Use this skill whenever the user asks about unusual options activity,
  dark pool data, whale trades, congressional stock trades, politician portfolios, gamma exposure (GEX),
  net premium, market tide, option flow alerts, IV rank, max pain, NOPE, short interest,
  failures to deliver, earnings calendar, FDA calendar, economic calendar, analyst ratings,
  ETF holdings, ETF flows, seasonality, crypto whale transactions, prediction markets,
  or any request mentioning "Unusual Whales", "UW", "flow alerts", "dark pool", "GEX",
  "gamma exposure", "congress trades", "politician trades", "insider buys", "insider sells",
  "net premium ticks", "market tide", "options screener", "stock screener", "lit flow",
  "spot exposures", "greek flow", "IV term structure", "risk reversal skew",
  "option chains", "OI change", "short volume", or "short squeeze".
---

# Unusual Whales API

Query the Unusual Whales API for options flow, dark pool, congressional trading, institutional holdings, Greek exposure, volatility, and 100+ other financial data endpoints.

## Step 1 — Authentication

The user must have an Unusual Whales API key. Check if the environment variable `UW_API_TOKEN` is set:

```bash
echo $UW_API_TOKEN
```

If not set, ask the user to provide their API token. They can purchase one at https://unusualwhales.com/pricing?product=api.

All requests use:
- **Base URL:** `https://api.unusualwhales.com`
- **Method:** `GET` (all endpoints are read-only)
- **Headers:**
  - `Authorization: Bearer <API_TOKEN>`
  - `Accept: application/json`

## Step 2 — Identify the User's Request

Match the user's request to the appropriate endpoint category and read the reference file for parameter details.

| User Intent | Category | Reference |
|---|---|---|
| Unusual options activity, flow alerts, sweeps, block trades | Options Flow | `references/endpoints.md` — Option Trade section |
| Options screener, hottest chains | Screener | `references/endpoints.md` — Screener section |
| Dark pool trades, off-exchange volume | Dark Pool | `references/endpoints.md` — Darkpool section |
| Lit flow, on-exchange trades | Lit Flow | `references/endpoints.md` — Lit Flow section |
| Congressional trades, politician portfolios | Congress / Politicians | `references/endpoints.md` — Congress & Politician sections |
| Insider buying/selling, insider transactions | Insiders | `references/endpoints.md` — Insiders section |
| Institutional holdings, 13F filings | Institutions | `references/endpoints.md` — Institution section |
| Greeks, delta, gamma, vanna, charm per strike | Greeks | `references/endpoints.md` — Stock section (greeks) |
| Gamma exposure (GEX), spot GEX | Greek Exposure | `references/endpoints.md` — Stock section (greek-exposure) |
| Net premium, call/put flow ticks | Net Premium | `references/endpoints.md` — Stock section (net-prem-ticks) |
| Market tide, market sentiment | Market | `references/endpoints.md` — Market section |
| IV rank, implied volatility, IV term structure | Volatility | `references/endpoints.md` — Stock section (volatility) |
| Max pain, NOPE | Options Analytics | `references/endpoints.md` — Stock section |
| Option chains, OI per strike/expiry | Option Chains | `references/endpoints.md` — Stock section |
| Stock screener, filter stocks | Screener | `references/endpoints.md` — Screener section |
| Earnings calendar, FDA calendar, economic events | Market Events | `references/endpoints.md` — Market section |
| Short interest, short volume, FTDs | Shorts | `references/endpoints.md` — Short section |
| ETF holdings, ETF flows, sector weights | ETFs | `references/endpoints.md` — ETFs section |
| Analyst ratings | Screener | `references/endpoints.md` — Screener section |
| Seasonality, monthly returns | Seasonality | `references/endpoints.md` — Seasonality section |
| Stock info, financials, balance sheets | Fundamentals | `references/endpoints.md` — Stock section |
| Technical indicators (RSI, MACD, etc.) | Technicals | `references/endpoints.md` — Stock section (technical-indicator) |
| Crypto whale transactions | Crypto | `references/endpoints.md` — Crypto section |
| Prediction markets | Predictions | `references/endpoints.md` — Predictions section |
| News headlines | News | `references/endpoints.md` — News section |

## Step 3 — Execute the API Call

Read `references/endpoints.md` for the full endpoint reference with parameters and response fields.

Write and execute a Python script to call the API:

```python
import http.client
import json
import os

token = os.environ.get("UW_API_TOKEN", "YOUR_API_KEY")
conn = http.client.HTTPSConnection("api.unusualwhales.com")
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}
conn.request("GET", "/api/ENDPOINT_PATH?param=value", headers=headers)
response = conn.getresponse()
data = json.loads(response.read().decode("utf-8"))
print(json.dumps(data, indent=2))
```

### Key Rules

1. **Always use the `UW_API_TOKEN` environment variable** for authentication — never hardcode tokens.
2. **All endpoints are GET-only.** This API is read-only. Never attempt POST/PUT/DELETE.
3. **Use correct paths.** All paths start with `/api/`. Do NOT use `/api/v1/` or `/api/v2/` — these do not exist.
4. **Do NOT hallucinate endpoints.** Only use endpoints listed in `references/endpoints.md`. Common fake endpoints to avoid: `/api/options/flow`, `/api/flow/live`, `/api/v1/*`.
5. **Respect limits.** Most endpoints default to 100 results with a max of 200 or 500. Use the `limit` parameter.
6. **Date format.** Use ISO date format `YYYY-MM-DD` for date parameters.
7. **Ticker format.** Use uppercase ticker symbols (e.g., `AAPL`, `SPY`).
8. **Parse numeric strings.** Many response fields are strings that represent numbers — convert them when doing calculations.
9. **Handle pagination.** Some endpoints support a `page` parameter for pagination.
10. **Net premium ticks are incremental.** To build a cumulative chart, sum each tick with all previous ticks.

## Step 4 — Present Results to the User

Format the data clearly:

- **Flow alerts:** Show ticker, type (call/put), strike, expiry, premium, size, alert rule, and whether it's a sweep/floor/multileg. Highlight unusually large trades.
- **Dark pool:** Show ticker, price, size, premium, execution time. Note trades near NBBO vs. away from it.
- **Congress/insider trades:** Show name, ticker, transaction type (buy/sell), amount, date filed, and transaction date. Flag notable patterns.
- **Greeks/GEX:** Summarize key strikes with highest gamma exposure. Note the "gamma flip" point if visible.
- **Market tide:** Describe the net call vs. put premium trend — is sentiment bullish or bearish?
- **Screener results:** Present as a table sorted by the most relevant metric.
- **Short data:** Show short interest, short volume ratio, days to cover, and FTD trends.

Use markdown tables for tabular data. Highlight notable items (large premiums, unusual volume, politician trades in companies they regulate, etc.).

## Step 5 — Error Handling

| Error | Cause | Fix |
|---|---|---|
| 401 Unauthorized | Invalid or missing API token | Check `UW_API_TOKEN` is set correctly |
| 403 Forbidden | Endpoint not included in subscription tier | Upgrade plan at unusualwhales.com/pricing |
| 404 Not Found | Invalid endpoint path or ticker | Verify endpoint path against `references/endpoints.md` |
| 422 Unprocessable | Invalid parameter value | Check parameter types and formats |
| 429 Too Many Requests | Rate limit exceeded | Wait and retry after a delay |
| Empty `data` array | No results for the query | Try broader filters or a different date |

## Reference Files

- `references/endpoints.md` — Complete endpoint reference with paths, parameters, and response fields for all 100+ endpoints
