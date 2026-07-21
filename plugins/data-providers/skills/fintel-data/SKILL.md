---
name: fintel-data
description: >
  Query Fintel (fintel.io) institutional market intelligence
  via the REST API at https://api.fintel.io/v1 with FINTEL_API_KEY
  (X-API-KEY header), or the official MCP server at
  https://mcp.fintel.io/mcp. Read-only data: short interest, borrow
  rate/fee and shares available to borrow, daily short volume,
  fails-to-deliver (FTD), institutional ownership from SEC 13F filings,
  insider transactions from SEC Form 3/4/5, analyst price targets,
  ratings and forecasts, dividends and earnings history, earnings and
  dividend calendars, EOD price bars, last trade price, security master
  lookup by ticker/CUSIP/ISIN/FIGI, leaderboards, watchlists and alerts.
  Triggers: "fintel", "fintel.io", short interest, short squeeze data,
  borrow rate, cost to borrow, shares available to borrow, FTD, fails to
  deliver, short volume, 13F holders, institutional owners, who owns X,
  insider buying, insider selling, Form 4 transactions, analyst price
  target, days to cover, short interest ratio.
---

# Fintel Data Skill

Fintel ([fintel.io](https://fintel.io)) is an institutional-grade market
intelligence platform.
Its strongest datasets are the ones most other providers lack: **short
interest, borrow rates, short volume, fails-to-deliver, 13F institutional
ownership, and insider transactions**.

Fintel exposes two surfaces backed by the same data contract:

| Surface | Endpoint | Auth | Best for |
|---|---|---|---|
| **REST** | `https://api.fintel.io/v1/*` | `X-API-KEY` header | Default — curl from any CLI agent |
| **MCP** | `https://mcp.fintel.io/mcp` | `X-API-KEY` header | MCP-native clients, tool auto-discovery |

Both require a Fintel API key. **This skill is READ-ONLY** — only call
GET endpoints. The API also exposes write endpoints (create/delete stock
lists, alert subscriptions, teams); do not call them.

---

## Step 1: Resolve FINTEL_API_KEY

The skill resolves `FINTEL_API_KEY` in this order:
1. `FINTEL_API_KEY` environment variable
2. `FINTEL_API_KEY` in `.env` in the current directory
3. `FINTEL_API_KEY` in `.env` at the git repo root (so a worktree inherits the key from the main checkout)

```
!`if [ -n "$FINTEL_API_KEY" ]; then echo "KEY_FROM_ENV_VAR"; elif [ -f .env ] && grep -qE "^FINTEL_API_KEY=" .env; then echo "KEY_FROM_LOCAL_DOTENV:$(pwd)/.env"; else GIT_COMMON=$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null); if [ -n "$GIT_COMMON" ]; then ROOT=$(dirname "$GIT_COMMON"); if [ -f "$ROOT/.env" ] && grep -qE "^FINTEL_API_KEY=" "$ROOT/.env"; then echo "KEY_FROM_ROOT_DOTENV:$ROOT/.env"; else echo "KEY_NOT_SET"; fi; else echo "KEY_NOT_SET"; fi; fi`
```

Then act on the result:

- `KEY_FROM_ENV_VAR` — use `$FINTEL_API_KEY` directly in curl calls.
- `KEY_FROM_LOCAL_DOTENV:<path>` / `KEY_FROM_ROOT_DOTENV:<path>` — load once before calling:
  ```bash
  export FINTEL_API_KEY=$(grep -E "^FINTEL_API_KEY=" <path> | head -1 | cut -d= -f2- | sed 's/^["'\'']//;s/["'\'']$//')
  ```
- `KEY_NOT_SET` — ask the user for their key. Keys come with a Fintel API
  plan ([fintel.io](https://fintel.io), docs at
  [api.fintel.io/docs](https://api.fintel.io/docs)). They can either
  `export FINTEL_API_KEY="..."` or add `FINTEL_API_KEY=...` to `.env` at
  the repo root (preferred for worktrees).

---

## Step 2: Resolve the Security

Most endpoints are addressed by `{country}/{symbol}` — an ISO country
code plus ticker, e.g. `us/AAPL`. Default to `us` when the user gives
only a ticker.

If the ticker is ambiguous or the user gives a company name, CUSIP,
ISIN, or FIGI, resolve it first:

```bash
# name / ticker / CUSIP / ISIN / FIGI search
curl -s -H "X-API-KEY: $FINTEL_API_KEY" "https://api.fintel.io/v1/securities?query=apple&country=us"
# exact identifier lookup (type: cusip, isin, ticker, id)
curl -s -H "X-API-KEY: $FINTEL_API_KEY" "https://api.fintel.io/v1/identifiers/isin/US0378331005"
```

---

## Step 3: Match the Request to an Endpoint

| User wants | Endpoint | Notes |
|---|---|---|
| Short interest, days to cover | `/v1/securities/{country}/{symbol}/short-interest` | Trailing year, NYSE/NASDAQ-reported. Limited availability — must be enabled per account; 403 means not entitled |
| Borrow rate, cost to borrow, shares available | `/v1/securities/{country}/{symbol}/borrow-rate` | Latest securities-lending fee rate, rebate rate, shares available |
| Daily short volume | `/v1/securities/{country}/{symbol}/short-volume` | Trailing year: short, short-exempt, total volume |
| Fails-to-deliver / FTD | `/v1/securities/{country}/{symbol}/fails-to-deliver` | Trailing-year SEC FTD records (US only) |
| Institutional owners / 13F holders | `/v1/securities/{country}/{symbol}/owners` | Current SEC 13F-derived holders |
| Insider transactions / Form 4 | `/v1/securities/{country}/{symbol}/insiders` | SEC Form 3/4/5-derived; `count` param |
| Analyst price targets | `/v1/securities/{country}/{symbol}/price-targets` | High, low, mean, median |
| Analyst buy/hold/sell ratings | `/v1/securities/{country}/{symbol}/analyst-ratings` | Aggregated recommendations |
| Revenue / EPS forecasts | `/v1/securities/{country}/{symbol}/forecast` | Aggregated analyst estimates |
| EOD price history | `/v1/securities/{country}/{symbol}/eod` | `period`: 1m, 3m, 6m, 1y (default), 2y, 3y, 5y, all |
| Latest price + derived stats | `/v1/securities/{country}/{symbol}/last-price` | 52w high/low, WTD/MTD/YTD change; falls back to EOD close with `meta.warnings=["quote_stale"]` |
| Dividend history | `/v1/securities/{country}/{symbol}/dividends` | |
| Earnings history and surprises | `/v1/securities/{country}/{symbol}/earnings` | |
| Upcoming earnings (one stock / market-wide) | `/v1/securities/{country}/{symbol}/calendar/earnings` or `/v1/calendar/earnings` | `from`/`to` ISO dates, default today +7d, max 90d window |
| Upcoming dividends (one stock / market-wide) | `/v1/securities/{country}/{symbol}/calendar/dividends` or `/v1/calendar/dividends` | Same window rules |
| A specific fundamental metric | `/v1/securities/{country}/{symbol}/data-points/{key}` | Discover keys via `/v1/data-definitions?query=...` |
| Top/bottom ranked stocks | `/v1/leaderboards` then `/v1/leaderboards/{key}/entries` | 503 not_available means retry later; `meta.status="beta"` means stub data |
| Security profile, listings, identifier history | `/v1/securities/{country}/{symbol}` | |
| User's watchlists | `/v1/stock-lists`, `/v1/stock-lists/{id}/items` | Also `/insiders`, `/owners`, `/filings` per list |
| User's alerts | `/v1/alerts`, `/v1/alert-messages` | |
| Account / entitlements | `/v1/account` | |

Full parameter details, country/exchange discovery endpoints, and more
curl examples: read `references/api-reference.md`.

---

## Step 4: Call the API

```bash
curl -s -H "X-API-KEY: $FINTEL_API_KEY" \
  "https://api.fintel.io/v1/securities/us/AAPL/short-volume" | python3 -m json.tool
```

- Success responses are JSON; some carry a `meta` object (warnings,
  freshness, status). Surface `meta.warnings` to the user when present.
- Errors return `{"error": {"code": "...", "message": "..."}}` — e.g.
  `unauthorized` (bad/missing key), `403` (dataset not enabled for the
  account, common for short-interest), `503 not_available` (ranking
  service down — retry later, don't treat as empty data).
- Usage is metered per account — batch thoughtfully; don't poll.

---

## Step 5: MCP Alternative (Optional)

For MCP-native setups, the same tools are discoverable from the official
server (tool names like `fintel.get_short_interest`,
`fintel.get_security_owners` — REST parity, same entitlements):

```bash
claude mcp add --transport http fintel https://mcp.fintel.io/mcp --header "X-API-KEY: your_key_here"
```

Prefer REST via curl when shell access is available — it needs no setup
beyond the key. Use MCP when the user explicitly asks for it or shell
access is restricted (note: neither works on Claude.ai's sandbox).

---

## Step 6: Respond to the User

- Format numbers cleanly: prices to 2 decimals, percentages to 1-2
  decimals, share counts with commas or abbreviations (2.3M, 1.1B).
- For short data: contextualize — short interest as % of float, days to
  cover, borrow fee trend direction. High borrow fee + falling shares
  available is the classic squeeze setup; present the data, not a
  prediction.
- For ownership/insiders: use tables (holder, shares, change, date).
  Distinguish buys from sells and option exercises in Form 4 data.
- Note the data source: "Fintel" with dataset provenance (SEC 13F, Form
  3/4/5, NYSE/NASDAQ short reports) when relevant.
- Never turn the data into a trading recommendation, price target, or
  squeeze call — present facts and let the user draw conclusions.

---

## Reference Files

- `references/api-reference.md` — full REST endpoint reference: all GET
  endpoints with parameters, defaults, limits, error semantics, MCP tool
  name mapping, and curl examples.
