---
name: tradingview-mcp
description: >
  Query TradingView market data through the bundled tradingview MCP server
  without a desktop app or login. Use whenever the user wants a technical
  analysis readout (RSI, MACD, Bollinger rating, BUY/SELL summary),
  multi-timeframe alignment (weekly→daily→4h→1h→15m),
  exchange-wide scans (Bollinger squeeze, volume breakout, consecutive
  candles, smart volume), top gainers/losers by exchange, futures market
  data (NQ/ES/CL/GC overview, overnight movers, category snapshots), pre-market /
  after-hours quotes, a quick options chain or unusual options activity
  (volume/OI by strike), bulk stock prices, a global market snapshot,
  strategy backtests (Sharpe, drawdown, win rate), or crypto exchange
  scans. Triggers include "TA on X", "multi-timeframe read", "BB squeeze
  scan", "futures movers", "NQ overnight", "pre-market price", "unusual
  options activity", "backtest RSI on AAPL", and "top gainers on NASDAQ".
  For options greeks, watchlists, alerts, or chart screenshots use
  tradingview-reader instead.
---

# TradingView MCP (Headless Market Data)

Market data via the bundled [`tradingview` MCP server](https://github.com/atilaahmettaner/tradingview-mcp) — TradingView's public scanner API plus Yahoo Finance, spoken over MCP. **No TradingView desktop app or account.** Most tools need no API key. The server ships with this plugin (`.mcp.json`) and starts automatically; its 37 tools appear under the plugin's `tradingview` MCP namespace (load them through the client's deferred-tool mechanism when necessary).

**Read-only.** Nothing here places trades or mutates any account.

## When to use this vs the other data skills

| Need | Skill |
|---|---|
| Quotes, TA readout, indicator ratings, multi-timeframe alignment | **this skill** |
| Exchange-wide scans: squeeze / volume breakout / gainers / losers | **this skill** |
| Futures (NQ, ES, CL, GC…) overview, movers, category quotes | **this skill** |
| Pre-market / after-hours price | **this skill** |
| Options chain quick look (bid/ask/IV/OI, **no greeks**), unusual activity | **this skill** (fallback / positioning scan) |
| Options chain **with greeks** (delta/gamma/theta/vega), IV skew, expiries with contract counts | `tradingview-reader` (desktop app) |
| Watchlists, alerts, TV news, chart state / screenshots, custom-column screener | `tradingview-reader` (desktop app) |


## Step 1: Check requirements

- `uv` installed (`brew install uv`) — the server runs via `uvx` and self-installs on first launch (give the first call ~30s).
- Python 3.10–3.13. The pinned upstream currently excludes Python 3.14.

If the MCP tools are missing, ask the user to restart the agent after enabling the plugin. Do not silently replace market data with invented values.

## Step 2: Select the smallest useful tool set

Prefer one focused call for a simple question. For a research brief, combine only the independent views that matter: price/snapshot, TA, volume, and optionally news. Avoid calling multiple overlapping TA tools merely to produce more output.

### Quotes & snapshots

| Tool | Use for |
|---|---|
| `stock_prices(tickers)` | Bulk quotes. `tickers` is comma-separated `EXCHANGE:SYMBOL` (e.g. `"NASDAQ:NVDA,NYSE:DELL"`), up to 1,000 rows in one call. OHLC + change%. |
| `yahoo_price(symbol)` | Single quote, Yahoo symbology: `AAPL`, `BTC-USD`, `SPY`, `^GSPC`, `^VIX`, `EURUSD=X`, `THYAO.IS`. |
| `stock_extended_hours(symbol)` | Pre-market / after-hours price for a US symbol — earnings reactions, overnight moves. |
| `market_snapshot()` | Global one-shot: major indices, top crypto, FX, key ETFs. |
| `bitcoin_market_pulse()` | BTC price + dominance + total mcap risk frame — call before analyzing any crypto. |

### Technical analysis (single symbol)

| Tool | Use for |
|---|---|
| `coin_analysis(symbol, exchange, timeframe)` | **The canonical TA readout** for one stock or coin — RSI, MACD, Bollinger rating, indicator summary. Despite the name it handles stocks: `coin_analysis("NVDA", "NASDAQ", "1D")`. |
| `multi_timeframe_analysis(symbol, exchange)` | Weekly → Daily → 4H → 1H → 15m trend alignment. |
| `combined_analysis(symbol, exchange, timeframe)` | TA + news + sentiment in one call (news legs need `MARKETAUX_API_TOKEN`). |
| `multi_agent_analysis(symbol, exchange, timeframe)` | Technical vs Sentiment vs Risk "debate" summary. |
| `volume_confirmation_analysis(symbol, exchange, timeframe)` | Is the move volume-confirmed? |

### Exchange-wide scans

| Tool | Use for |
|---|---|
| `top_gainers` / `top_losers(exchange, timeframe, limit)` | Movers on one exchange. |
| `bollinger_scan(exchange, timeframe, bbw_threshold, limit)` | Low-BBW squeeze candidates. |
| `rating_filter(exchange, timeframe, rating, limit)` | Filter by BB rating −3 (strong sell) … +3 (strong buy). |
| `volume_breakout_scanner` / `smart_volume_scanner` | Volume + price breakout detection. |
| `consecutive_candles_scan` / `advanced_candle_pattern` | Candle-pattern scans. |
| `stock_screener(country, stock_type, limit, …)` | Common/preferred share screen by country (`america`, `japan`, …), mcap-ranked. |

### Futures (夜盘 / overnight)

| Tool | Use for |
|---|---|
| `futures_market_overview(category, exchanges, limit)` | Top contracts by volume. `category`: all / equity_index / energy / metals / agriculture / rates / forex / crypto_futures; `exchanges`: us / global. |
| `futures_top_movers(direction, exchanges, limit)` | Biggest % movers today. |
| `futures_category_snapshot(category)` | OHLCV for all front-month contracts in one category — e.g. `equity_index` → NQ, ES, YM, RTY. |
| `futures_watchlist()` | Canonical front-month symbol list per category. |

### Options (US equities — no greeks)

| Tool | Use for |
|---|---|
| `stock_options_chain(symbol, expiry)` | Calls + puts for one expiry (`YYYY-MM-DD`; omit → nearest). Returns strike, last, bid/ask, volume, OI, IV, ITM flag, plus the full `available_expiries` list. Source: Yahoo. **No delta/gamma/theta/vega** — use `tradingview-reader` for greeks. |
| `stock_options_unusual_activity(symbol, top_n, min_volume, expiries)` | Top strikes by volume/OI ratio across the soonest expiries — positioning scan before earnings. |

### Backtesting

| Tool | Use for |
|---|---|
| `backtest_strategy(symbol, strategy, period, interval, …)` | One strategy (`rsi`, `bollinger`, `macd`, `ema_cross`, `supertrend`, `donchian`, `rsi_pullback`, `keltner_breakout`, `triple_ema`) with Sharpe, max DD, win rate, vs buy-and-hold. Yahoo symbology. |
| `compare_strategies(symbol, period, …)` | All 9 strategies ranked. |
| `walk_forward_backtest_strategy(…)` | Train/test split with an overfitting verdict. |

### News & sentiment (needs `MARKETAUX_API_TOKEN`)


### Regional extras

`egx_*` (Egyptian Exchange suite) — rarely relevant; also BIST, HKEX, SSE, SZSE, TWSE supported via the `exchange` param on scan tools.

## Step 3: Normalize inputs

1. **`exchange` defaults to `KUCOIN` (crypto!) on most scan/TA tools** — always pass `NASDAQ` / `NYSE` explicitly for US equities.
2. **Three symbologies coexist**: scanner tools take bare symbol + `exchange` param; `stock_prices` takes `EXCHANGE:SYMBOL`; Yahoo-backed tools (`yahoo_price`, backtests, options) take Yahoo tickers (`BTC-USD`, `^VIX`, `THYAO.IS`).
3. **Timeframes**: `5m, 15m, 1h, 4h, 1D, 1W, 1M`. Intraday scans on stock exchanges can be sparse — prefer `1D` for equities.
4. **Tool names** are canonical as listed. Use `coin_analysis` and `multi_timeframe_analysis`, not README-style aliases such as `get_technical_analysis`.

## Step 4: Validate and interpret results

1. Check timestamps, exchange, symbol, session, and currency before drawing conclusions.
2. Treat a returned error envelope as an error, not as an empty result. Use its retryability and symbol suggestions; retry at most once when marked retryable.
3. Filter wide scanner results to roughly 10 rows and the columns relevant to the question.
5. Backtests are historical simulations. Report the period, interval, costs, sample size, benchmark, and walk-forward result when available; do not present them as forecasts.

## Step 5: Respond to the user

Lead with the answer, then show a compact evidence table. Include an as-of timestamp and data source, name any missing or stale fields, and separate observed facts from interpretation. For trading-shaped requests, keep the response analytical and read-only: discuss risks and scenarios without placing or offering to place a trade.

## Maintainer note

The server is pinned to an immutable upstream commit in `.mcp.json`. To upgrade it, select a reviewed SHA, update the pin, perform a real MCP initialize + `tools/list` handshake, confirm all tools remain read-only, and reconcile this catalog with the registered tool names and schemas.
