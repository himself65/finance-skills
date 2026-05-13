---
name: funda-data
description: >
  Query Funda AI financial data via two surfaces: the MCP server at
  https://funda.ai/api/mcp for analyst-grade research synthesis (DCF,
  comps, earnings previews/recaps, sector deep-dives, SEC filings,
  transcripts, supply-chain mapping, ownership flow, macro framing) via
  the agent_chat tool — OR the REST API at https://api.funda.ai/v1 with
  FUNDA_API_KEY for raw data (real-time quotes, intraday candles, EOD
  prices, financial statements, options chains/greeks/GEX, supply-chain
  KG, social sentiment, news, calendars, FRED, ESG, congressional
  trades, AI hiring signals). Triggers: "funda", "funda.ai", real-time
  quote, stock price, intraday, balance sheet, income statement, options
  chain, DCF, comps, earnings preview/recap, analyst estimates,
  10-K/10-Q/8-K, transcript, ownership flow, gamma exposure, supply
  chain, sector deep-dive, congressional trades, FRED. Prefer MCP for
  synthesis/analysis questions; use REST for raw structured data the MCP
  declines.
---

# Funda AI Skill

Funda AI exposes two complementary surfaces backed by the same data:

| Surface | Best for | Auth | Output |
|---|---|---|---|
| **MCP** `agent_chat` at `https://funda.ai/api/mcp` | Research, analysis, synthesis | OAuth (auto via `claude mcp add`) | Synthesized text with disclaimer |
| **REST** `/v1/*` at `https://api.funda.ai` | Raw structured data | `FUNDA_API_KEY` Bearer | JSON |

Both require an active [Funda AI](https://funda.ai) subscription.

---

## Step 1: Decide Which Surface

| User wants | Surface |
|---|---|
| DCF / comps walkthrough, sector view, transcript synthesis, company primer | MCP |
| Earnings preview/recap with judgment, beat-miss decomposition, narrative framing | MCP |
| Real-time or intraday quote, EOD price history | REST |
| Raw options chain snapshot, greeks, GEX time series | REST |
| Specific line item from a financial statement (single number, JSON) | REST |
| 13F filings, insider trades, congressional trades as rows | REST |
| News with structured sentiment / event timeline (JSON) | REST |
| Bulk dataset downloads | REST |
| AI-company hiring signals (OpenAI, Anthropic, Google, xAI) | REST |

**Default to MCP** for ambiguous research-style questions. **Use REST** when
the user wants machine-readable structured data — or when the MCP refuses
(real-time prices, raw quotes).

The MCP also refuses buy/sell calls, price targets, personalized
portfolio advice, tax/legal advice, and trade execution. Those are out of
scope for both surfaces — decline politely and don't fall through to REST
hoping for a different answer.

---

## Step 2: MCP Flow (Research)

### 2a. Verify the MCP is connected

```
!`claude mcp list 2>/dev/null | grep -iE "^funda:" || echo "FUNDA_MCP_NOT_CONNECTED"`
```

- A line starting with `funda:` → registered. The tool is callable as `mcp__funda__agent_chat`. Continue.
- `FUNDA_MCP_NOT_CONNECTED` → ask the user to install:
  ```bash
  claude mcp add --transport http funda https://funda.ai/api/mcp
  ```
  A browser tab opens for OAuth approval (1-hour token + 30-day refresh, auto-managed). The Claude Code session may need to be restarted before the tool registers.

### 2b. Frame the question

`agent_chat` is a fresh research turn with **no cross-call memory** — bake
the ticker, time horizon, and assumptions into the question text itself.

| User wants | Question shape |
|---|---|
| Earnings preview | "Preview MSFT's Q3 print Thursday — segment trends, where consensus is aggressive/conservative, beat/miss pattern." |
| Earnings recap | "Walk through NVDA Q2: beat/miss by segment, guide vs consensus, transcript Q&A on data-center demand." |
| Sector deep-dive | "Summarize the 2026 hyperscaler capex cycle — spending tiers by name, supplier exposure, gross-margin implications." |
| Supply chain | "Map TSMC's customer concentration and N2 ramp risks — top three exposures by revenue." |
| Filing summary | "Diff the new risk factors in PLTR's latest 10-K versus the prior year." |
| DCF | "Walk through a DCF for NVDA assuming 25% data-center growth, 10% terminal margin, 9% WACC — surface the sensitivity table." |
| Macro | "Where in the Dalio long-term debt cycle is the US, and what does that imply for duration positioning?" |
| Ownership | "Has institutional ownership of CRWD shifted in the latest 13F filings — net buyers vs sellers?" |

If the user gave only a ticker, ask one clarifying question to scope the
turn (preview? recap? primer? DCF?) before calling — vague questions burn
a turn and return vague answers.

If the user is following up on a prior Funda response, quote the relevant
paragraph back inside the new question; the agent has no memory of prior
calls.

For more example questions per topic, see `references/research-topics.md`.

### 2c. Call the tool

```
mcp__funda__agent_chat(question: "<full research question>")
```

Typical run is 15–60 seconds; the server streams progress notifications
throughout, so the client doesn't time out.

Response shape:
- `content[0].text` — answer prefixed with `[Funda research output — fundamental analysis, informational only…]`. Keep the prefix.
- `_meta["funda.io/conversation_id"]` — UUID. The in-app history page is `https://funda.ai/agent-chat?c=<id>` (the `/agent-chat` route redirects to `/agent-chat-v2?c=<id>`).
- `_meta["funda.io/timed_out"]` — `true` if the agent hit its run budget. Answer is partial; offer to retry with a tighter scope.

If the call returns 403 `subscription_required`, the MCP is registered
but the account isn't subscribed — direct the user to https://funda.ai
to activate.

Each call costs a research turn. Don't speculatively re-call with a
rephrased question if the first answer was reasonable.

---

## Step 3: REST Flow (Raw Data)

### 3a. Resolve FUNDA_API_KEY

The skill resolves `FUNDA_API_KEY` in this order:
1. `FUNDA_API_KEY` environment variable
2. `FUNDA_API_KEY` in `.env` in the current directory
3. `FUNDA_API_KEY` in `.env` at the git repo root (so a worktree inherits the key from the main checkout)

```
!`if [ -n "$FUNDA_API_KEY" ]; then echo "KEY_FROM_ENV_VAR"; elif [ -f .env ] && grep -qE "^FUNDA_API_KEY=" .env; then echo "KEY_FROM_LOCAL_DOTENV:$(pwd)/.env"; else GIT_COMMON=$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null); if [ -n "$GIT_COMMON" ]; then ROOT=$(dirname "$GIT_COMMON"); if [ -f "$ROOT/.env" ] && grep -qE "^FUNDA_API_KEY=" "$ROOT/.env"; then echo "KEY_FROM_ROOT_DOTENV:$ROOT/.env"; else echo "KEY_NOT_SET"; fi; else echo "KEY_NOT_SET"; fi; fi`
```

Then act on the result:

- `KEY_FROM_ENV_VAR` — use `$FUNDA_API_KEY` directly in curl calls.
- `KEY_FROM_LOCAL_DOTENV:<path>` / `KEY_FROM_ROOT_DOTENV:<path>` — load once before calling:
  ```bash
  export FUNDA_API_KEY=$(grep -E "^FUNDA_API_KEY=" <path> | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//')
  ```
- `KEY_NOT_SET` — ask the user for their key. They can either `export FUNDA_API_KEY="..."` or add `FUNDA_API_KEY=...` to `.env` at the repo root (preferred for worktrees).

### 3b. Find the right endpoint

Match the user's request to a category and read the corresponding
reference file for full parameters and response schemas.

| Category | Endpoint family | Reference |
|---|---|---|
| Real-time / batch / aftermarket quotes | `/v1/quotes?type=...` | `references/market-data.md` |
| Historical EOD, intraday candles, technical indicators | `/v1/stock-price`, `/v1/charts` | `references/market-data.md` |
| Commodity / forex / crypto quotes | `/v1/quotes?type=commodity-quotes` | `references/market-data.md` |
| Income / balance / cash flow / metrics / ratios | `/v1/financial-statements` | `references/fundamentals.md` |
| Company profile, peers, shares float, search, screener, list | `/v1/company-profile`, `/v1/company-details`, `/v1/search`, `/v1/companies` | `references/fundamentals.md` |
| Analyst estimates, price targets, grades, DCF, ratings | `/v1/analyst?type=...` | `references/fundamentals.md` |
| Options chain, greeks, GEX, IV, max pain, flow, screener | `/v1/options/...` | `references/options.md` |
| Supply-chain KG: suppliers, customers, competitors, partners | `/v1/supply-chain/...` | `references/supply-chain.md` |
| Twitter, Reddit, Polymarket, government trading, ownership | `/v1/twitter-posts`, `/v1/reddit-posts`, `/v1/polymarket/...`, `/v1/government-trading`, `/v1/ownership` | `references/alternative-data.md` |
| AI-enriched news + aggregated sentiment + event timeline | `/v1/news/ticker`, `/v1/news/timeline`, `/v1/news/sentiment` | `references/news-enriched.md` |
| SEC filings, earnings/podcast transcripts, research reports | `/v1/sec-filings`, `/v1/transcripts`, `/v1/investment-research-reports` | `references/filings-transcripts.md` |
| Earnings / dividend / IPO / splits / economic calendar | `/v1/calendar?type=...` | `references/calendar-economics.md` |
| Treasury rates, GDP/CPI indicators, FRED, risk premium | `/v1/economics`, `/v1/fred` | `references/calendar-economics.md` |
| Stock news, gainers/losers, ETF holdings, ESG, COT, bulk, market hours | `/v1/news`, `/v1/market-performance`, `/v1/funds`, `/v1/esg`, `/v1/cot-report`, `/v1/bulk`, `/v1/market-hours` | `references/other-data.md` |
| AI-company hiring signals (OpenAI, Anthropic, Google, xAI, Mercor, SurgeAI) | `/v1/recruit-...` | `references/recruit.md` |
| Claude API proxy via Bedrock | `/v1/claude/v1/messages` | `references/claude-proxy.md` |

### 3c. Call the endpoint

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/<endpoint>?<params>" | python3 -m json.tool
```

All responses are `{"code": "0", "message": "", "data": ...}`. A non-zero
`code` is an error — read `message`.

List endpoints paginate: `{"items": [...], "page": 0, "page_size": 20, "next_page": 1, "total_count": N}`. Pages are 0-based; `next_page` is `-1` when exhausted.

For broad ticker overviews ("tell me about AAPL"), combine a few REST
calls: `/v1/company-profile` for sector/CEO/mcap/price + `/v1/financial-statements?type=key-metrics-ttm` + `/v1/analyst?type=price-target-summary`.

---

## Step 4: Respond to the User

- For MCP synthesis: surface with structure (tables, bullets, headings) — don't dump the raw blob. Preserve the Funda disclaimer; never repackage analysis as a recommendation, price target, or trade signal.
- For MCP responses, cite `https://funda.ai/agent-chat?c={conversation_id}` so the user can inspect the agent's full timeline.
- For REST responses, format numbers cleanly (prices to 2 decimals, ratios to 2-4, large numbers with commas or abbreviations like `$2.8T`). Use tables for comparative data; summarize trends rather than dumping time series.
- For DCF / valuation work, surface the assumptions Funda used so the user can adjust them.
- Note the source: "Funda AI" (whether MCP or REST).
- Never provide trading recommendations — present the data and let the user draw conclusions.

---

## Reference Files

**MCP path:**
- `references/research-topics.md` — categorized example questions and tips for framing `agent_chat` queries.

**REST path:**
- `references/market-data.md` — quotes, historical prices, charts, technical indicators
- `references/fundamentals.md` — financial statements, company profile/details, search/screener, analyst, companies list
- `references/options.md` — chains, greeks, GEX, flow, IV, screener, contract-level data
- `references/supply-chain.md` — supply-chain KG, relationships, graph traversal
- `references/alternative-data.md` — Twitter, Reddit, Polymarket, government trading, ownership
- `references/news-enriched.md` — AI-enriched news, event timeline, aggregated sentiment
- `references/filings-transcripts.md` — SEC filings, earnings/podcast transcripts, research reports
- `references/calendar-economics.md` — calendars, economics, treasury, FRED
- `references/other-data.md` — news, market performance, funds, ESG, COT, bulk, market hours
- `references/recruit.md` — AI-company hiring signals, JD classifications, product clusters, launch probabilities
- `references/claude-proxy.md` — Claude API proxy via Bedrock
