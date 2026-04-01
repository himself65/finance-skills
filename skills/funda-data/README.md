# Funda Data

Query the [Funda AI](https://api.funda.ai) financial data API for comprehensive market data, fundamentals, options flow, supply chain intelligence, social sentiment, and alternative data.

## Triggers

- Stock quotes, prices, historical data
- Financial statements (income, balance sheet, cash flow)
- Analyst estimates, price targets, DCF, ratings
- Options data (chains, greeks, GEX, flow, IV, max pain, screener)
- Supply chain relationships (suppliers, customers, competitors)
- Social sentiment (financial Twitter KOLs, Reddit/WSB)
- Prediction markets (Polymarket)
- Congressional/government trading
- Insider trades, institutional holdings (13F)
- SEC filings, earnings transcripts, podcast transcripts
- Calendars (earnings, dividends, IPOs, economic events)
- Economic indicators (GDP, CPI, treasury rates, FRED)
- News, ESG, commodities, forex, crypto
- Any mention of "funda", "funda.ai", or "funda API"

## Platform

**CLI only** — requires shell access for `curl` and the `FUNDA_API_KEY` environment variable.

## Setup

> **Paid API** — A [Funda AI](https://funda.ai) subscription is required. See their site for pricing.

1. Get an API key from [Funda AI](https://funda.ai)
2. Set the environment variable:
   ```bash
   export FUNDA_API_KEY="your-api-key-here"
   ```

## Reference Files

| File | Description |
|---|---|
| `references/market-data.md` | Quotes, historical prices, charts, technical indicators |
| `references/fundamentals.md` | Financial statements, company details, search/screener, analyst |
| `references/options.md` | Options chains, greeks, GEX, flow, IV, screener, contracts |
| `references/supply-chain.md` | Supply chain KG, relationships, graph traversal |
| `references/alternative-data.md` | Twitter, Reddit, Polymarket, government trading, ownership |
| `references/filings-transcripts.md` | SEC filings, earnings/podcast transcripts, research reports |
| `references/calendar-economics.md` | Calendars, economics, treasury, FRED |
| `references/other-data.md` | News, market performance, funds, ESG, COT, bulk data |

## API Coverage

60+ endpoints covering:
- Real-time & historical market data
- Company fundamentals & financial statements
- Options flow & analytics (powered by Unusual Whales)
- Supply chain knowledge graph
- Social media sentiment (Twitter KOLs, Reddit finance subs)
- Prediction markets (Polymarket)
- SEC filings & earnings transcripts
- Analyst research & valuation models
- Congressional/insider trading
- Economic indicators & FRED data
- ESG ratings, commodities, forex, crypto
