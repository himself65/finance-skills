# Fintel Data

Query [Fintel](https://fintel.io) institutional market intelligence:

- **REST API** at `https://api.fintel.io/v1` — `X-API-KEY` header auth. Default surface; works from any CLI agent via curl.
- **MCP server** at `https://mcp.fintel.io/mcp` — same tools, same data contract, same key; for MCP-native clients.

Fintel's signature datasets are the ones most other providers lack: short interest, borrow rates and shares available to borrow, daily short volume, fails-to-deliver (FTD), 13F institutional ownership, and insider transactions.

## Triggers

- Short interest, days to cover, short interest ratio, short squeeze data
- Borrow rate / cost to borrow / rebate rate / shares available to borrow
- Daily short volume, short-exempt volume
- Fails-to-deliver (FTD) records
- Institutional owners, 13F holders, "who owns X"
- Insider buying/selling, Form 3/4/5 transactions
- Analyst price targets, buy/hold/sell ratings, revenue/EPS forecasts
- Dividend and earnings history, earnings/dividend calendars
- EOD price bars, last trade price with 52-week stats
- Security lookup by ticker, CUSIP, ISIN, or FIGI
- Leaderboards, user watchlists (stock lists), alerts
- Any mention of "fintel" or "fintel.io"

## Read-Only

This skill only calls GET endpoints. The Fintel API also exposes write operations (stock lists, alert subscriptions, teams) — the skill never invokes them, per this repo's read-only policy.

## Platform

**CLI only** — requires shell access for curl (Claude Code or similar). Does not work on Claude.ai's sandbox.

## Setup

> **Paid service** — a Fintel API plan is required. Some datasets (notably short interest) must additionally be enabled per account; the API returns 403 for unentitled datasets.

Get an API key from [Fintel](https://fintel.io) (docs: [api.fintel.io/docs](https://api.fintel.io/docs)), then either:

```bash
export FINTEL_API_KEY="your-api-key-here"
```

…or add `FINTEL_API_KEY=...` to `.env` at the repo root (preferred when working across worktrees — the skill resolves the key from env, local `.env`, then the repo-root `.env`).

Optional MCP registration instead of REST:

```bash
claude mcp add --transport http fintel https://mcp.fintel.io/mcp --header "X-API-KEY: your_key_here"
```

## Reference Files

| File | Description |
|---|---|
| `references/api-reference.md` | Full REST endpoint reference — all GET endpoints with parameters, defaults, limits, error semantics, MCP tool-name mapping, and curl examples |
