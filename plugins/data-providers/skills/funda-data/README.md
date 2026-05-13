# Funda Data

Query [Funda AI](https://funda.ai) financial data via two complementary surfaces:

- **MCP server** at `https://funda.ai/api/mcp` — single `agent_chat` tool for analyst-grade research synthesis. OAuth (auto via `claude mcp add`).
- **REST API** at `https://api.funda.ai/v1` — 60+ endpoints for raw structured data. `FUNDA_API_KEY` Bearer auth.

The skill prefers the MCP for research/analysis questions and falls back to REST for raw data the MCP declines (real-time quotes, intraday candles, raw options chains, single line items, bulk downloads).

## Triggers

**MCP path** (synthesis):
- Earnings previews/recaps, beat-miss decomposition
- Analyst estimate-revision trends
- SEC filing summaries (10-K, 10-Q, 8-K, S-1)
- Earnings call transcript digestion
- Company primers, competitive positioning, supply-chain mapping
- Sector deep-dives (semis, pharma, banks, retail, energy, mining, housing)
- DCF and comps modelling against caller-supplied assumptions
- Macro framing (Fed stance, Dalio quadrant, sector rotation)

**REST path** (raw data):
- Real-time / intraday / EOD prices and quotes
- Financial statements (income, balance sheet, cash flow) as structured JSON
- Options chains, greeks, GEX, IV, max pain, flow alerts
- Supply-chain knowledge graph (raw edges)
- Twitter, Reddit, Polymarket, congressional trades, ownership (13F)
- News, calendars, FRED, ESG, COT, AI-company hiring signals

Triggers on any mention of "funda", "funda.ai", or specific endpoints/topics above.

## Out of Scope (Both Surfaces)

The Funda agent (and this skill) will not:

- Issue buy / sell / hold recommendations or price targets
- Provide personalized investment advice or portfolio allocation
- Give tax, legal, or regulatory advice
- Execute trades

## Platform

**CLI only** — requires Claude Code (or another MCP-aware client with shell access) so `claude mcp add` and the curl-based REST flow both work.

## Setup

> **Paid service** — A [Funda AI](https://funda.ai) subscription is required. The MCP returns 403 `subscription_required` and the REST API rejects unsubscribed keys.

### MCP

```bash
claude mcp add --transport http funda https://funda.ai/api/mcp
```

A browser tab opens for OAuth. The access token lasts 1 hour and auto-refreshes via a 30-day refresh token. Restart your Claude Code session after approval so the tool registers.

To remove later: `claude mcp remove funda`.

### REST

Get an API key from Funda AI, then either:

```bash
export FUNDA_API_KEY="your-api-key-here"
```

…or add `FUNDA_API_KEY=...` to `.env` at the repo root (preferred when working across worktrees — the skill resolves the key from env, local `.env`, then the repo-root `.env`).

## Reference Files

| File | Path | Description |
|---|---|---|
| `references/research-topics.md` | MCP | Example research questions per topic and framing tips for `agent_chat` |
| `references/market-data.md` | REST | Quotes, historical prices, charts, technical indicators |
| `references/fundamentals.md` | REST | Financial statements, company details, search/screener, analyst data |
| `references/options.md` | REST | Chains, greeks, GEX, flow, IV, screener, contracts |
| `references/supply-chain.md` | REST | Supply-chain KG, relationships, graph traversal |
| `references/alternative-data.md` | REST | Twitter, Reddit, Polymarket, government trading, ownership |
| `references/news-enriched.md` | REST | AI-enriched news, event timeline, aggregated sentiment |
| `references/filings-transcripts.md` | REST | SEC filings, earnings/podcast transcripts, research reports |
| `references/calendar-economics.md` | REST | Calendars, economics, treasury, FRED |
| `references/other-data.md` | REST | News, market performance, funds, ESG, COT, bulk |
| `references/recruit.md` | REST | AI-company hiring signals |
| `references/claude-proxy.md` | REST | Claude API proxy via Bedrock |
