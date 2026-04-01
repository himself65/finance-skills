# Options Data Reference

All options data powered by [Unusual Whales](https://unusualwhales.com/).

---

## GET /v1/options/stock

Stock-level options data (32 types).

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `ticker` | string | Yes | Ticker symbol |
| `type` | string | Yes | Data type (see sections below) |
| `date` | date | No | Market date (YYYY-MM-DD) |
| `expiry` | date | No | Option expiry date (for `greeks`, `greek-flow-expiry`) |
| `expirations` | date[] | No | List of expiry dates (for `atm-chains`) |
| `limit` | int | No | Result limit (1-500) |
| `side` | string | No | Trade side filter |
| `min_premium` | int | No | Minimum premium |
| `timeframe` | string | No | Timeframe (for `greek-exposure`) |

---

### Chains & Contracts

| Type | Description |
|---|---|
| `option-chains` | All available option contract symbols |
| `option-contracts` | Contracts with volume, OI, premium, bid/ask, IV |
| `atm-chains` | At-the-money chains (requires `expirations` param) |

### Volume & Open Interest

| Type | Description |
|---|---|
| `options-volume` | Daily call/put volume, premium, bid/ask breakdown |
| `vol-oi-per-expiry` | Volume and OI per expiry |
| `oi-change` | Open interest changes ranked by significance |
| `oi-per-expiry` | OI by expiry (call_oi, put_oi) |
| `oi-per-strike` | OI by strike |
| `expiry-breakdown` | Volume/OI/chains count per expiry |

### Greeks & GEX

| Type | Description | Extra Params |
|---|---|---|
| `greeks` | Greeks per strike for a given expiry | `expiry` required |
| `greek-exposure` | Net GEX/DEX for the whole chain | `timeframe` optional |
| `greek-exposure-by-expiry` | Greek exposure by expiry | |
| `greek-exposure-by-strike` | Greek exposure by strike | |
| `greek-exposure-by-strike-expiry` | Greek exposure by strike and expiry | |
| `spot-gex` | Spot GEX per 1min | |
| `spot-gex-by-strike` | Spot GEX by strike | |
| `spot-gex-by-strike-expiry` | Spot GEX by strike and expiry | |

### Flow

| Type | Description | Extra Params |
|---|---|---|
| `greek-flow` | Directional delta/vega flow per time bucket | |
| `greek-flow-expiry` | Greek flow by expiry | `expiry` required |
| `flow-per-expiry` | Option flow aggregated per expiry | |
| `flow-per-strike` | Option flow aggregated per strike | |
| `flow-per-strike-intraday` | Intraday flow per strike | |
| `flow-recent` | Latest option flows for the ticker | |
| `flow-alerts` | Flow alerts for the ticker | |
| `net-prem-ticks` | Call/put net premium and volume per time bucket | |

### IV & Volatility

| Type | Description |
|---|---|
| `interpolated-iv` | Interpolated IV at standard tenors |
| `iv-rank` | IV rank (1-year) |
| `iv-term-structure` | IV term structure across expirations |
| `historical-risk-reversal-skew` | Historical risk reversal skew |

### Other

| Type | Description |
|---|---|
| `max-pain` | Maximum pain strike per expiry |
| `nope` | Net Options Positioning Effect (NOPE) indicator |
| `option-price-levels` | Call/put volume at each price level |

### Examples

```bash
# Option chains
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/stock?ticker=AAPL&type=option-chains"

# Greeks for a specific expiry
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/stock?ticker=AAPL&type=greeks&expiry=2026-04-17"

# Gamma exposure (GEX)
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/stock?ticker=AAPL&type=greek-exposure"

# IV rank
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/stock?ticker=AAPL&type=iv-rank"

# Max pain
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/stock?ticker=AAPL&type=max-pain"

# Recent option flow
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/stock?ticker=AAPL&type=flow-recent"

# Net premium ticks
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/stock?ticker=AAPL&type=net-prem-ticks"

# OI change
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/stock?ticker=AAPL&type=oi-change"

# NOPE indicator
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/stock?ticker=AAPL&type=nope"
```

---

## GET /v1/options/flow-alerts

Market-wide unusual options activity alerts.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | No | Default: `flow-alerts` |
| `ticker` | string | No | Filter by ticker |
| `limit` | int | No | Results per page (1-200, default 100) |
| `is_call` | bool | No | Filter calls |
| `is_put` | bool | No | Filter puts |
| `is_sweep` | bool | No | Filter sweeps |
| `min_premium` | int | No | Minimum premium |
| `max_premium` | int | No | Maximum premium |
| `min_size` | int | No | Minimum trade size |
| `min_dte` | int | No | Minimum days to expiry |
| `max_dte` | int | No | Maximum days to expiry |

### Example

```bash
# Unusual options: sweeps with >$100k premium
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/flow-alerts?is_sweep=true&min_premium=100000"
```

Response fields: `type`, `ticker`, `strike`, `expiry`, `total_premium`, `volume`, `open_interest`, `underlying_price`, `iv_start`, `iv_end`, `has_sweep`, `has_multileg`, `alert_rule`, `option_chain`, `created_at`.

---

## GET /v1/options/contract

Contract-level options data.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `contract_id` | string | Yes | Option symbol (e.g., `AAPL260417C00250000`) |
| `type` | string | Yes | `flow`, `history`, `intraday`, or `volume-profile` |
| `date` | date | No | Market date |
| `limit` | int | No | Result limit |
| `side` | string | No | Trade side filter |
| `min_premium` | int | No | Minimum premium |

### Types

| Type | Description |
|---|---|
| `flow` | Trade flow for the contract (with greeks, tags) |
| `history` | Historical data (volume, OI, price per day) |
| `intraday` | Intraday OHLC data |
| `volume-profile` | Volume profile by price |

### Example

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/contract?contract_id=AAPL260417C00250000&type=flow"
```

---

## GET /v1/options/screener

Options screener for finding hottest option chains.

### Parameters

| Param | Type | Required | Description |
|---|---|---|---|
| `type` | string | No | Default: `hottest-chains` |
| `ticker` | string | No | Filter by ticker |
| `is_otm` | bool | No | Out-of-the-money filter |
| `option_type` | string | No | `call` or `put` |
| `min_volume` | int | No | Minimum volume |
| `min_premium` | int | No | Minimum premium |
| `min_dte` | int | No | Minimum days to expiry |
| `max_dte` | int | No | Maximum days to expiry |
| `order` | string | No | Sort field |
| `order_direction` | string | No | `asc` or `desc` |
| `limit` | int | No | Results per page (1-250, default 50) |
| `page` | int | No | Page (0-based) |

### Example

```bash
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/options/screener?min_volume=1000&min_premium=50000&order=volume&order_direction=desc"
```
