---
name: tradingview-reader
description: >
  Read TradingView desktop app for market data, news, alerts, watchlists,
  and screener results using opencli (read-only).
  Use this skill whenever the user wants quotes, options chains, options
  expiries, screener results across stocks/crypto/forex/futures/bonds,
  gainers/losers/movers, news headlines or full story bodies, alerts
  (active list, fire log, offline fires), watchlists including colored
  flag lists, symbol search/autocomplete, chart state, or screenshots
  from their local TradingView.app. Triggers include: "options chain for
  X", "IV on Y", "show me SNDK puts", "TV screener for Y sector", "screen
  oversold stocks", "TV gainers", "crypto by market cap", "TradingView
  news on AAPL", "show my watchlists", "red flag list", "list my alerts",
  "what alerts fired", "search TV for nvidia", "what symbol is on my
  chart", "screenshot NVDA chart", "TradingView IV skew", "TV expiries
  for X". This skill is READ-ONLY — it does NOT place trades, modify
  watchlists, or change chart layouts.
---

# TradingView Reader (Read-Only)

Reads TradingView's desktop macOS app for quotes, options chains, and chart state via [opencli](https://github.com/jackwener/opencli) and a CDP attach to the running TradingView.app process. Powered by the `tradingview` plugin in this repo's [`opencli-plugins/tradingview`](https://github.com/himself65/finance-skills/tree/main/opencli-plugins/tradingview) tree (a separate plugin from opencli's built-in adapters, installed via opencli's monorepo subpath syntax).

**This skill is read-only.** Designed for analysis: pulling options chains, checking IV/greeks, capturing chart state. It does NOT place trades, post ideas, modify watchlists, or change chart layouts.

> **Headless alternative**: for plain quotes, TA readouts, screeners, futures, or a greeks-free options chain, prefer the sibling `tradingview-mcp` skill (bundled MCP server, no desktop app, no CDP relaunch). Use *this* skill when you need greeks / per-strike IV skew, expiries with contract counts, or account-bound data (watchlists, alerts, charts, TV news).

**Important**: Unlike browser-based opencli readers (twitter, linkedin), this one talks directly to a running TradingView desktop app over Chrome DevTools Protocol. The user must (a) have `TradingView.app` installed, and (b) be logged in inside that app. The plugin handles relaunching with the debug port.

**How it works**: data commands harvest session cookies via CDP `Storage.getCookies`, then fire HTTP requests from Node directly. Page-context fetch is blocked by browser CORS preflight even from TradingView's own pages — the desktop app uses Electron's main process (Node network stack) to bypass this, and we replicate that path. No Browser Bridge extension required, no `apps.yaml` registration needed.

---

## Step 1: Ensure opencli + Plugin Are Installed and Ready

**Current environment status:**

```
!`(command -v opencli && opencli tradingview status 2>&1 | head -5 && echo "READY" || echo "SETUP_NEEDED") 2>/dev/null || echo "NOT_INSTALLED"`
```

If the status above shows `READY`, skip to Step 2. Otherwise:

### NOT_INSTALLED — Install opencli

```bash
npm install -g @jackwener/opencli
```

Requires Node.js >= 24 — the `tradingview` plugin installed in the next step declares `engines.node >= 24`.

### SETUP_NEEDED — Install the TradingView plugin and launch with CDP

The TradingView adapter is **not** built into opencli — it's a separate plugin:

```bash
# Install the plugin
opencli plugin install github:himself65/finance-skills/tradingview

# Relaunch TradingView.app with CDP enabled (one-time per session)
opencli tradingview launch
```

The `launch` step quits the running TradingView and reopens it with `--remote-debugging-port=9222`. **Warn the user to save chart layouts first** if they have unsaved drawings.

### Common setup issues

| Symptom | Fix |
|---|---|
| `opencli: command not found` | `npm install -g @jackwener/opencli` (Node ≥ 24) |
| `Unknown command: tradingview` | `opencli plugin install github:himself65/finance-skills/tradingview` |
| `Cannot reach CDP at http://127.0.0.1:9222` | App not launched with debug port — run `opencli tradingview launch` |
| `No tradingview.com cookies found` | App is open but logged out — log in inside the desktop app |
| `No TradingView tab found` | Open any chart or symbol page in TradingView, then retry |
| Empty chain / 0 contracts | Subscription tier on the logged-in account doesn't include options for this symbol |

---

## Step 2: Identify What the User Needs

### Setup / chart inspection

| User Request | Command | Key Flags |
|---|---|---|
| Setup / connection check | `opencli tradingview status` | — |
| Relaunch app with CDP | `opencli tradingview launch` | `--port 9222` |
| What's on the chart | `opencli tradingview chart-state` | `--tab <id>` |
| Screenshot a chart | `opencli tradingview screenshot --output ~/charts/nvda.png` | `--tab <id>` |

### Quotes + options

| User Request | Command | Key Flags |
|---|---|---|
| Spot quote | `opencli tradingview quote --ticker X` | `--exchange NASDAQ` |
| Options chain (full) | `opencli tradingview options-chain --ticker X` | `--exchange` |
| Options chain (one expiry, ATM band) | `opencli tradingview options-chain --ticker X --expiry YYYY-MM-DD` | `--type call\|put`, `--strikes-around-spot N` |
| List expiries | `opencli tradingview options-expiries --ticker X` | — |

### Screener

| User Request | Command | Key Flags |
|---|---|---|
| Generic screener (stocks/crypto/forex/futures/bonds) | `opencli tradingview screener --market america --columns ...` | `--filter <json>`, `--sort field:desc`, `--limit N`, `--label-product` |
| US stocks with RSI < 30, sorted by volume | `opencli tradingview screener --market america --columns "name,close,RSI\|60,volume" --filter '[{"left":"RSI\|60","operation":"less","right":30}]' --sort volume:desc` | — |
| Top crypto by market cap | `opencli tradingview screener --market coin --columns "name,close,change,market_cap_calc" --sort market_cap_calc:desc --limit 50` | — |
| Symbol search / autocomplete | `opencli tradingview search --query "nvidia"` | `--type stock\|funds\|crypto\|...`, `--exchange`, `--country` |

### News

| User Request | Command | Key Flags |
|---|---|---|
| Global news headlines | `opencli tradingview news --limit 25` | `--category`, `--area`, `--section`, `--provider` |
| News for a specific ticker | `opencli tradingview news --symbol NASDAQ:AAPL` | `--limit`, `--section analysis\|press_release\|...` |
| Full story by id | `opencli tradingview news --id <story-id>` | `--lang en` |

### Watchlists + alerts

| User Request | Command | Key Flags |
|---|---|---|
| List all watchlists | `opencli tradingview watchlists` | — |
| Symbols in one watchlist | `opencli tradingview watchlists --id <wl-id>` | — |
| Colored-flag list (red/orange/yellow/green/blue/purple) | `opencli tradingview watchlists --color red` | — |
| List all alerts | `opencli tradingview alerts --type list` | — |
| Active alerts | `opencli tradingview alerts --type active` | — |
| Recently triggered alerts | `opencli tradingview alerts --type triggered` | — |
| Alerts that fired while offline | `opencli tradingview alerts --type offline` | — |
| Full alert log | `opencli tradingview alerts --type log` | — |

---

## Step 3: Execute the Command

### General pattern

```bash
# Use -f json or -f yaml for structured output
opencli tradingview options-chain --ticker SNDK --expiry 2026-05-22 -f json
opencli tradingview options-chain --ticker NVDA --strikes-around-spot 8 -f csv
opencli tradingview quote --ticker SPY --exchange NYSEARCA -f json
```

### Key rules

1. **Run `opencli tradingview status` first** if connectivity is uncertain — it reports CDP connection state and active TradingView tabs.
2. **Use `-f json`** for programmatic processing (LLM context, downstream skills).
3. **Filter by expiry and `--strikes-around-spot`** — full chains can be 3,000+ rows; an unfiltered dump is rarely what the user wants.
4. **Default `--exchange NASDAQ`** for US equities; require explicit `--exchange` for ETFs (e.g. SPY = NYSEARCA, QQQ = NASDAQ) or non-US listings.
5. **For `screener`, `--columns` is critical** — it controls both the request and the output table. Include `name` and any field used in `--filter` or `--sort`. Append `|TF` for an indicator's timeframe, e.g. `RSI|60` for 1-hour RSI. The default columns are sensible for stocks but should be replaced for crypto / forex / futures (different field catalogs).
6. **For `screener`, `--filter` is JSON** — array of `{left, operation, right}` clauses. Always single-quote the JSON in shell to avoid escaping issues. See `references/commands.md` for the operations cheat sheet.
7. **For `news`, narrow the feed early** — the global feed is firehose-level. Use `--symbol`, `--category`, `--section`, or `--provider` before raising `--limit`.
8. **For `search`, prefer it over guessing** — when the user gives an ambiguous ticker (e.g. "SPY" without exchange), run `search --query SPY` first to confirm the listing, then pass `--exchange` to subsequent commands.
9. **For `watchlists` and `alerts`, default to summary** — a user asking "what's in my watchlists?" wants list names + counts, not every symbol.
10. **NEVER call any write operation.** This skill is read-only — no trades, no watchlist edits, no alert creation/deletion, no chart writes. The plugin intentionally does not expose write endpoints (`/append`, `/replace`, `/create_alert`, etc.).

### Output format flag (`-f`)

| Format | Flag | Best for |
|---|---|---|
| Table | `-f table` (default) | Human-readable terminal output |
| JSON | `-f json` | Programmatic processing, LLM context |
| YAML | `-f yaml` | Structured output, readable |
| Markdown | `-f md` | Documentation, reports |
| CSV | `-f csv` | Spreadsheet export |

### Output columns

- `quote` — `symbol`, `close`, `change`, `change_abs`, `currency`, `time`
- `options-chain` — `expiry`, `dte`, `strike`, `type`, `bid`, `ask`, `mid`, `iv`, `delta`, `gamma`, `theta`, `vega`, `rho`, `theo`, `bid_iv`, `ask_iv`, `symbol`
- `options-expiries` — `expiry`, `dte`, `contracts_count`
- `screener` — dynamic; one column per `--columns` entry, plus `symbol`. (Default: `name`, `close`, `change`, `volume`, `market_cap_basic`, `sector.tr`.)
- `search` — `symbol`, `description`, `type`, `exchange`, `country`, `currency`
- `news` (list mode) — `id`, `published`, `provider`, `title`, `urgency`, `related_symbols`, `link`
- `news` (story mode, `--id` set) — `id`, `published`, `provider`, `title`, `body`, `tags`, `link`
- `watchlists` — `id`, `name`, `symbol_count`, `symbols`
- `alerts` — `id`, `name`, `symbol`, `type`, `condition`, `value`, `active`, `status`, `fired_at`
- `chart-state` — `layout_id`, `symbol`, `interval`, `url`
- `screenshot` — `path`, `bytes`

---

## Step 4: Present the Results

1. **Lead with the structure summary** — for an options chain, state spot price, expiry being shown, ATM strike, and IV regime first; then the table. For a screener, lead with the count of matches and the filters applied.
2. **Filter aggressively before showing** — never paste a 3,000-row chain or a 500-row screener. Default to ATM ± 6 strikes per expiry for chains; for screeners cap to top 20 unless the user asks for more.
3. **Highlight skew** — when showing both calls and puts, note IV skew direction if material.
4. **For chart-state**, report layout id + symbol + interval + URL succinctly; offer to screenshot.
5. **For news (list mode)**, group by provider and lead with timestamps in the user's likely timezone (or always UTC ISO if uncertain). Include the link so the user can open the story. For story mode (`--id` set), the body is plain text — present it as-is, optionally trimmed.
6. **For watchlists**, summarize counts before listing symbols (e.g. "3 watchlists: Earnings (24 syms), AI plays (12 syms), Hedges (8 syms)"). Don't dump 100-symbol watchlist contents unless asked.
7. **For alerts**, group by status (active vs triggered/fired) and order recent firings by `fired_at` desc. Don't expose alert ids unless the user explicitly asks.
8. **For screener results**, surface the top movers / extreme values in plain prose first (e.g. "highest market cap NVDA at $4.2T, 12 names below the RSI<30 threshold"), then the table.
9. **Treat sessions as private** — never expose CDP target IDs, cookies, or layout IDs unless the user asks.

---

## Step 5: Diagnostics

```bash
opencli tradingview status
```

Returns CDP connection state and active TradingView tabs. If CDP is down, run `opencli tradingview launch` to relaunch with the debug port.

---

## Error Reference

| Error | Cause | Fix |
|---|---|---|
| `Unknown command: tradingview` | Plugin not installed | `opencli plugin install github:himself65/finance-skills/tradingview` |
| `Cannot reach CDP at http://127.0.0.1:9222` | App launched without debug port | `opencli tradingview launch` |
| `No tradingview.com cookies found` | Logged out of TradingView | Log in inside the desktop app |
| `No TradingView tab found` | App open but no TradingView page loaded | Open any chart or symbol page, then retry |
| `scanner 400 / Empty chain / totalCount=0` | Subscription tier doesn't cover this symbol's options | Check account tier in the desktop app |
| `Symbol not found` | Wrong exchange | Pass `--exchange` explicitly, or run `opencli tradingview search --query <name>` first |
| Rate limited | Too many requests | Wait a few seconds, then retry |

---

## Reference Files

- `references/commands.md` — Every command with all flags, output examples, and analyst workflows
