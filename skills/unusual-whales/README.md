# unusual-whales

Query the [Unusual Whales API](https://unusualwhales.com/public-api) for options flow, dark pool trades, congressional trading, institutional holdings, Greek exposure, volatility, and 100+ other financial data endpoints.

## What it does

- **Options flow** — unusual activity alerts, sweeps, block trades, flow per strike/expiry, net premium ticks
- **Dark pool & lit flow** — off-exchange and on-exchange trade data with NBBO context
- **Congressional & insider trading** — politician portfolios, congress trades, insider buy/sell transactions
- **Greeks & GEX** — delta, gamma, vanna, charm per strike/expiry, spot gamma exposure
- **Volatility** — IV rank, IV term structure, realized volatility, risk reversal skew
- **Market sentiment** — Market Tide, SPIKE, NOPE, sector tide, ETF tide
- **Screener** — stock screener, options screener, analyst ratings, short screener
- **Fundamentals** — financials, balance sheets, income statements, cash flows, earnings
- **Short data** — short interest, short volume, failures to deliver (FTDs)
- **ETFs** — holdings, exposure, inflows/outflows, sector weights
- **Seasonality** — monthly returns, year-over-year patterns, top performers
- **Crypto** — whale transactions, OHLC candles, pair state
- **Technical indicators** — RSI, MACD, Bollinger Bands, VWAP, moving averages via Alpha Vantage
- **News & events** — headlines, economic calendar, FDA calendar, earnings calendar
- **Prediction markets** — insiders, smart money, whales, unusual activity

**This skill is read-only.** All API endpoints are GET-only.

## Pricing

This API requires a **paid subscription**. There is no free tier. Purchase an API token at [unusualwhales.com/pricing](https://unusualwhales.com/pricing?product=api).

## Authentication

Set your API token as an environment variable:

```bash
export UW_API_TOKEN="your_token_here"
```

No additional API keys or OAuth flows required.

## Triggers

- "unusual options activity", "flow alerts", "sweeps"
- "dark pool trades", "off-exchange volume"
- "congress trades", "politician portfolios", "insider buys/sells"
- "gamma exposure", "GEX", "spot GEX"
- "net premium", "market tide", "market sentiment"
- "IV rank", "volatility term structure"
- "max pain", "NOPE"
- "short interest", "FTDs", "short squeeze"
- "stock screener", "options screener"
- "Unusual Whales", "UW API"

## Platform

Works on **Claude Code** (requires network access for API calls). Does **not** work on Claude.ai (sandbox restrictions).

## Setup

```bash
npx skills add himself65/finance-skills --skill unusual-whales
```

## Reference files

- `references/endpoints.md` — Complete endpoint reference with paths, parameters, and response fields for all 100+ endpoints
