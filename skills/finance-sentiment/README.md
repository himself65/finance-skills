# finance-sentiment

Structured stock sentiment research using the Adanos Finance API.

## What it does

Fetches normalized stock sentiment signals across:

- **Reddit** - buzz, bullish percentage, mentions, trend
- **X.com** - buzz, bullish percentage, mentions, trend
- **News** - buzz, bullish percentage, mentions, trend
- **Polymarket** - buzz, bullish percentage, trades, trend

This skill is useful when a user wants fast answers such as:

- "How much are Reddit users talking about TSLA right now?"
- "How hot is NVDA on X.com this week?"
- "How many Polymarket bets are active on Microsoft right now?"
- "Are Reddit and X aligned on META?"
- "Compare social sentiment on AMD vs NVDA"

**This skill is read-only.** It only fetches sentiment data for research.

## Triggers

- "social sentiment on TSLA"
- "stock buzz"
- "how hot is X stock on X.com"
- "how many Reddit mentions does AAPL have"
- "how many Polymarket bets on Microsoft"
- "compare sentiment on AMD vs NVDA"
- "is Reddit aligned with X on META"

## Prerequisites

- `ADANOS_API_KEY` must be set in the environment
- `curl` available in the shell

## Platform

Works on **all platforms** that support shell commands and outbound HTTP requests.

## Setup

```bash
npx skills add himself65/finance-skills --skill finance-sentiment
```

See the [main README](../../README.md) for more installation options.

## Reference files

- `references/api_reference.md` - endpoint guide, field meanings, and example workflows
