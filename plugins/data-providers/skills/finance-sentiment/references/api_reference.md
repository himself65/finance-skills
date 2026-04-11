# Finance Sentiment API Reference

This skill uses the Adanos Finance API for read-only stock sentiment research.

Base docs:

```text
https://api.adanos.org/docs
```

## Authentication

Send the API key as:

```bash
-H "X-API-Key: $ADANOS_API_KEY"
```

## Compare endpoints

Use compare endpoints for quick snapshots and multi-ticker comparisons.

### Reddit

```text
GET /reddit/stocks/v1/compare?tickers=TSLA,NVDA&days=7
```

Primary fields:
- `ticker`
- `buzz_score`
- `mentions`
- `bullish_pct`
- `bearish_pct`
- `trend`
- `sentiment_score`
- `unique_posts`
- `subreddit_count`
- `total_upvotes`

### X.com

```text
GET /x/stocks/v1/compare?tickers=TSLA,NVDA&days=7
```

Primary fields:
- `ticker`
- `buzz_score`
- `mentions`
- `bullish_pct`
- `bearish_pct`
- `trend`
- `sentiment_score`
- `unique_tweets`
- `total_upvotes`

### News

```text
GET /news/stocks/v1/compare?tickers=TSLA,NVDA&days=7
```

Primary fields:
- `ticker`
- `buzz_score`
- `mentions`
- `bullish_pct`
- `bearish_pct`
- `trend`
- `sentiment_score`
- `source_count`

### Polymarket

```text
GET /polymarket/stocks/v1/compare?tickers=TSLA,NVDA&days=7
```

Primary fields:
- `ticker`
- `buzz_score`
- `trade_count`
- `bullish_pct`
- `bearish_pct`
- `trend`
- `sentiment_score`
- `market_count`
- `unique_traders`
- `total_liquidity`

## Detail endpoints

Use stock detail endpoints only when the user explicitly asks for a deeper breakdown.

```text
GET /reddit/stocks/v1/stock/{ticker}
GET /x/stocks/v1/stock/{ticker}
GET /news/stocks/v1/stock/{ticker}
GET /polymarket/stocks/v1/stock/{ticker}
```

These can include richer fields such as daily trend history and top mentions / top markets.

## Recommended answer patterns

### Single source

Always prioritize these four values:

- `Buzz`
- `Bullish %`
- `Mentions` or `Trades`
- `Trend`

Example:

```text
TSLA on X.com, last 7 days
- Buzz: 86.1/100
- Bullish: 56%
- Mentions: 2,650
- Trend: falling
```

### Multi-source for one ticker

Use one section per source, then synthesize:

- aligned bullish
- aligned bearish
- mixed / diverging

Good synthesis prompts:
- Is Reddit aligned with X?
- Which source is hottest?
- Is prediction market activity more bullish than social chatter?

### Multi-ticker comparison

Default ranking:
- `buzz_score` descending

Useful interpretations:
- high buzz + high bullish = strong attention with positive tone
- high buzz + low bullish = controversial / crowded bearish setup
- low buzz + rising trend = early attention pickup
- large source disagreement = unstable consensus
