# opencli-plugin-tradingview

Read-only [opencli](https://github.com/jackwener/opencli) adapter for the **TradingView desktop macOS app**. Exposes spot quotes, full options chains (with greeks/IV), expiries, screener (stocks/crypto/forex/futures/bonds), news, alerts, watchlists, symbol search, chart state, and chart screenshots — all by attaching to a logged-in TradingView.app over Chrome DevTools Protocol. No API key.

This plugin lives inside the [`himself65/finance-skills`](https://github.com/himself65/finance-skills) monorepo. Install it via opencli's monorepo subpath syntax:

```bash
opencli plugin install github:himself65/finance-skills/tradingview
```

## Install + launch

```bash
# Prereqs: Node ≥ 22 (built-in WebSocket), TradingView.app installed + logged in
npm install -g @jackwener/opencli
opencli plugin install github:himself65/finance-skills/tradingview

# Relaunch TradingView with --remote-debugging-port (one-time per session)
opencli tradingview launch
```

`launch` quits any running TradingView and reopens it with `--remote-debugging-port=9222`. Save chart layouts first.

**Zero extra setup.** No `apps.yaml` registration, no Browser Bridge extension. The plugin attaches to CDP directly via Node's built-in WebSocket.

## Commands

### Setup / chart inspection

| Command | Description | Output columns |
|---|---|---|
| `tradingview launch` | Relaunch TradingView with CDP port enabled | `port`, `pid`, `ready` |
| `tradingview status` | CDP connection state + active TradingView tabs | `connected`, `tabs` |
| `tradingview chart-state` | Active chart's symbol/interval/layout | `layout_id`, `symbol`, `interval`, `url` |
| `tradingview screenshot --output path.png` | PNG of an active chart tab | `path`, `bytes` |

### Quotes + options

| Command | Description | Output columns |
|---|---|---|
| `tradingview quote --ticker X` | Single-symbol spot quote | `symbol`, `close`, `change`, `change_abs`, `currency`, `time` |
| `tradingview options-chain --ticker X` | Options chain (full or ATM band) | `expiry`, `dte`, `strike`, `type`, `bid`, `ask`, `mid`, `iv`, `delta`, `gamma`, `theta`, `vega`, `rho`, `theo`, `bid_iv`, `ask_iv`, `symbol` |
| `tradingview options-expiries --ticker X` | List available expiries | `expiry`, `dte`, `contracts_count` |

`options-chain` flags: `--exchange` (default `NASDAQ`), `--expiry YYYY-MM-DD`, `--type call|put`, `--strikes-around-spot N` (default 6, `0` = full strike list).

### Screener + search

| Command | Description | Output columns |
|---|---|---|
| `tradingview screener --market <m> --columns <csv>` | Generic screener (stocks per country, crypto, forex, futures, bonds) | `symbol` + dynamic from `--columns` |
| `tradingview search --query <text>` | Symbol search / autocomplete | `symbol`, `description`, `type`, `exchange`, `country`, `currency` |

`screener` flags: `--market` (default `america`; supports ~70 country codes + `crypto`/`coin`/`forex`/`futures`/`bond`/`global`/`options`), `--columns` (CSV; append `|TF` for indicator timeframe like `RSI|60`), `--filter` (JSON array of `{left, operation, right}` clauses), `--sort field:asc|desc` (default `volume:desc`), `--tickers` (CSV of `EXCH:SYM`), `--label-product` (default `screener-stock`), `--limit` (1-500, default 50), `--offset`.

### News + watchlists + alerts

| Command | Description | Output columns |
|---|---|---|
| `tradingview news` | News headlines (filterable) or full story by `--id` | List: `id`, `published`, `provider`, `title`, `urgency`, `related_symbols`, `link`. Story: adds `body`, `tags` |
| `tradingview watchlists` | List all watchlists (or one via `--id`, or colored list via `--color`) | `id`, `name`, `symbol_count`, `symbols` |
| `tradingview alerts --type <kind>` | Read-only alerts: list / active / triggered / offline / log | `id`, `name`, `symbol`, `type`, `condition`, `value`, `active`, `status`, `fired_at` |

`news` flags: `--id`, `--symbol`, `--category {base|stock|etf|futures|forex|crypto|index|bond|economic}`, `--area {WLD|AME|EUR|ASI|OCN|AFR}`, `--section`, `--provider`, `--lang`, `--limit`.

`watchlists` flags: `--id <8-char>` (one specific list), `--color {red|orange|yellow|green|blue|purple}` (colored-flag list).

`alerts` flags: `--type {list|active|triggered|offline|log}` (default `list`).

All commands accept `-f json|yaml|md|csv|table`.

## Data path

The plugin replicates what TradingView's desktop app does internally — its main Electron process makes HTTP requests via Node's network stack, bypassing browser CORS. The plugin does the same:

1. Connect to the running app's CDP (`http://127.0.0.1:9222/json/version`)
2. Open the browser-level WebSocket
3. Call `Storage.getCookies` to harvest the user's `.tradingview.com` session cookies
4. Fire HTTP requests from Node directly with those cookies in a `Cookie` header — no browser, no CORS preflight

This was discovered the hard way: page-context `fetch()` from any TradingView page is blocked by CORS preflight, even though the website itself uses these endpoints. The `lib/cookies.js` module implements this auth flow once; commands then call `tradingViewFetch(url, init)`.

**Endpoint families used:**
- `scanner.tradingview.com/{market}/scan2` — quotes, options, screener (POST)
- `news-headlines.tradingview.com/v2/{headlines,story}` — news (GET)
- `pricealerts.tradingview.com/{list_alerts,...}` — alerts (GET)
- `www.tradingview.com/api/v1/symbols_list/...` — watchlists (GET)
- `symbol-search.tradingview.com/symbol_search/v3/` — search (GET)

Scanner responses arrive in the standard `{fields, symbols}` compressed form; field positions are read from the response — never hard-coded. The options chain endpoint specifically requires `index_filters: [{name:'underlying_symbol', values:[...]}]` + `filter2` boolean composition, captured via Network domain inspection.

## Auth model

No bearer token, no API key. The adapter relies entirely on the desktop app's logged-in session. Subscription tier matches what the user sees in the app — free / Essential / Plus / Premium tiers may return a subset of options data for some symbols.

## Status

**v0.1 — verified live against TradingView desktop app on macOS.** All 12 commands smoke-tested end-to-end (quote → MU @ $746.81, options-chain → 7,426 contracts, news → 200 headlines, screener → top mcap, etc.). Wire shapes are the actual ones the desktop app uses (captured via CDP Network domain).

Known limitations:
- macOS only (`launch` uses `open -a TradingView`).
- `chart-state` symbol/interval detection is best-effort — DOM selectors may need adjustment as TradingView updates the UI; the layout id and URL are always correct.
- No tier-degraded gracefully — empty options chains may indicate the logged-in account's tier doesn't include that symbol's options.

## Layout

```
opencli-plugins/tradingview/
├── opencli-plugin.json        # plugin manifest
├── package.json               # Node package (type: module)
├── lib/
│   ├── cookies.js             # CDP Storage.getCookies harvest + tradingViewFetch helper
│   ├── cdp.js                 # CDP tab finder, Runtime.evaluate, Page.captureScreenshot
│   ├── scanner.js             # POST helpers, {fields,symbols} decoder, screener body builder
│   ├── symbols.js             # OPRA parser, expiry helpers
│   └── news.js                # /v2/headlines + /v2/story + AST→text walker
├── launch.js                  # spawns TradingView with --remote-debugging-port
├── status.js                  # CDP /json + tab filter
├── quote.js                   # global/scan2 → spot
├── options-chain.js           # options/scan2 → chain (full or ATM band)
├── options-expiries.js        # options/scan2 → expiry list
├── screener.js                # {market}/scan2 generic screener
├── search.js                  # symbol-search/v3
├── news.js                    # /v2/headlines (list) + /v2/story (--id)
├── watchlists.js              # api/v1/symbols_list/{all,custom/<id>,colored/<c>}
├── alerts.js                  # pricealerts.tradingview.com (read-only)
├── chart-state.js             # CDP Runtime.evaluate → layout_id, symbol, interval, url
├── screenshot.js              # CDP Page.captureScreenshot → PNG
└── tests/
    ├── symbols.test.js        # OPRA parser, expiry helpers
    ├── scanner.test.js        # decoder, normalize, ATM-band slicer, body builders
    ├── screener.test.js       # buildScreenerBody (limit clamping, sort, filter, tickers)
    ├── news.test.js           # AST walker, headline normalize, epoch helpers
    ├── cookies.test.js        # endpoint resolution, header constants
    └── alerts.test.js         # normalizeAlerts (live `r:[]` shape + fallbacks)
```

## License

MIT
