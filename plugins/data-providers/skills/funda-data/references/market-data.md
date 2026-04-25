# Market Data & Prices Reference

## GET /v1/quotes

Real-time and aftermarket quotes for stocks, ETFs, mutual funds, commodities, crypto, forex, and indexes.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Data type (see below) |
| `ticker` | string | No | Ticker symbol (single or comma-separated for batch) |
| `exchange` | string | No | Exchange code (for exchange-quotes type) |

### Types

| Type | Description |
|---|---|
| `realtime` | Real-time quote for a single ticker |
| `short` | Short format real-time quote |
| `aftermarket-trade` | Aftermarket trade data |
| `aftermarket-quote` | Aftermarket quote data |
| `premarket-trade` | Pre/post-market trade for a single ticker |
| `batch-premarket` | Pre/post-market trades for all stocks |
| `price-change` | Stock price change statistics |
| `batch` | Batch quotes for multiple tickers (comma-separated) |
| `batch-short` | Batch quotes in short format |
| `batch-aftermarket-trade` | Batch aftermarket trades |
| `batch-aftermarket-quote` | Batch aftermarket quotes |
| `exchange-quotes` | All quotes for a specific exchange (requires `exchange`) |
| `mutual-fund-quotes` | All mutual fund quotes |
| `etf-quotes` | All ETF quotes |
| `commodity-quotes` | All commodity quotes |
| `crypto-quotes` | All cryptocurrency quotes |
| `forex-quotes` | All forex pair quotes |
| `index-quotes` | All market index quotes |

### Example: Real-time quote

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/quotes?type=realtime&ticker=AAPL"
```

Response fields: `ticker`, `name`, `price`, `changesPercentage`, `change`, `dayLow`, `dayHigh`, `yearHigh`, `yearLow`, `marketCap`, `priceAvg50`, `priceAvg200`, `volume`, `avgVolume`, `exchange`, `open`, `previousClose`, `eps`, `pe`, `earningsAnnouncement`, `sharesOutstanding`, `timestamp`.

### Example: Batch quotes

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/quotes?type=batch&ticker=AAPL,MSFT,GOOGL"
```

---

## GET /v1/stock-price

Historical end-of-day stock prices.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `ticker` | string | Yes | Ticker symbol |
| `date_after` | date | No | Start date (YYYY-MM-DD) |
| `date_before` | date | No | End date (YYYY-MM-DD) |

### Example

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/stock-price?ticker=AAPL&date_after=2024-01-01&date_before=2024-12-31"
```

Response: `{"data": {"ticker": "AAPL", "historical": [{"date", "open", "high", "low", "close", "volume", "vwap"}, ...]}}`.

---

## GET /v1/charts

Historical price charts (EOD and intraday) and technical indicators.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Data type (see below) |
| `ticker` | string | Yes | Ticker symbol |
| `date_after` | string | No | Start date (YYYY-MM-DD) |
| `date_before` | string | No | End date (YYYY-MM-DD) |
| `timeframe` | string | No | For technical indicators: `1day`, `1week`, `1month` (default: `1day`) |
| `period_length` | int | No | Period length for technical indicators (default: 10) |

### Price Chart Types

| Type | Description |
|---|---|
| `light` | Light EOD (date, open, high, low, close, volume) |
| `full` | Full EOD with adjusted close, change, etc. |
| `unadjusted` | Non-split-adjusted EOD |
| `dividend-adjusted` | Dividend-adjusted EOD |
| `1min` | 1-minute intraday candles |
| `5min` | 5-minute intraday candles |
| `15min` | 15-minute intraday candles |
| `30min` | 30-minute intraday candles |
| `1hour` | 1-hour intraday candles |
| `4hour` | 4-hour intraday candles |

### Technical Indicator Types

| Type | Description |
|---|---|
| `sma` | Simple Moving Average |
| `ema` | Exponential Moving Average |
| `wma` | Weighted Moving Average |
| `dema` | Double Exponential Moving Average |
| `tema` | Triple Exponential Moving Average |
| `rsi` | Relative Strength Index |
| `standarddeviation` | Standard Deviation |
| `williams` | Williams %R |
| `adx` | Average Directional Index |

### Examples

```bash
# EOD chart
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/charts?type=light&ticker=AAPL&date_after=2024-01-01&date_before=2024-01-31"

# 5-minute intraday
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/charts?type=5min&ticker=AAPL&date_after=2024-01-31"

# 50-day SMA
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/charts?type=sma&ticker=AAPL&timeframe=1day&period_length=50"

# 14-day RSI
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/charts?type=rsi&ticker=AAPL&timeframe=1day&period_length=14"
```

---

## GET /v1/commodities

Commodity quotes and historical prices. Uses `type` parameter — see full docs at `https://api.funda.ai/docs/commodities.md`.

## GET /v1/forex

Forex pair quotes and historical rates. Uses `type` parameter — see full docs at `https://api.funda.ai/docs/forex.md`.

## GET /v1/crypto

Cryptocurrency quotes and historical prices. Uses `type` parameter — see full docs at `https://api.funda.ai/docs/crypto.md`.
