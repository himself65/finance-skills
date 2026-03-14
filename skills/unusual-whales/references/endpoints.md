# Unusual Whales API — Endpoint Reference

Base URL: `https://api.unusualwhales.com`

All endpoints require `Authorization: Bearer <API_TOKEN>` header. All methods are `GET`.

Responses are JSON with a `data` key containing the result array/object.

---

## Alerts

### GET `/api/alerts`
Retrieve alerts.

### GET `/api/alerts/configuration`
Alert configurations.

---

## Congress

### GET `/api/congress/congress-trader`
Recent reports by a specific congress trader.

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `name` | No | Trader name |

### GET `/api/congress/late-reports`
Recent late reports filed by congress members.

### GET `/api/congress/recent-trades`
Latest transacted trades by congress members.

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `limit` | No | Default 100, max 200 |
| `date` | No | ISO date (YYYY-MM-DD). Returns reports with transaction date <= this date |
| `ticker` | No | Filter by ticker symbol |

**Response Fields:** `amounts`, `filed_at_date`, `is_active`, `issuer`, `member_type`, `name`, `notes`, `politician_id`, `reporter`, `ticker`, `transaction_date`, `txn_type`

---

## Crypto

### GET `/api/crypto/whale-transactions`
Crypto whale transactions.

### GET `/api/crypto/whales/recent`
Recent crypto whale trades.

### GET `/api/crypto/{pair}/ohlc/{candle_size}`
Crypto OHLC candles.

**Path Parameters:** `pair` (e.g., BTCUSD), `candle_size` (e.g., 1d, 1h)

### GET `/api/crypto/{pair}/state`
Crypto pair state.

**Path Parameters:** `pair`

---

## Darkpool

### GET `/api/darkpool/recent`
Recent market-wide darkpool trades.

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `newer_than` | No | Filter trades newer than timestamp |
| `older_than` | No | Filter trades older than timestamp |
| `min_premium` | No | Minimum trade premium |
| `max_premium` | No | Maximum trade premium |
| `min_size` | No | Minimum trade size |
| `max_size` | No | Maximum trade size |
| `limit` | No | Default 500, max 500 |

### GET `/api/darkpool/{ticker}`
Darkpool trades for a specific ticker on a given day.

**Path Parameters:** `ticker`

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `date` | No | Market date (YYYY-MM-DD). Defaults to current/last market day |
| `newer_than` | No | Filter trades newer than timestamp |
| `older_than` | No | Filter trades older than timestamp |
| `min_premium` | No | Minimum trade premium |
| `max_premium` | No | Maximum trade premium |
| `min_size` | No | Minimum trade size |
| `max_size` | No | Maximum trade size |
| `min_volume` | No | Minimum volume |
| `max_volume` | No | Maximum volume |
| `limit` | No | Default 500, max 500 |

**Response Fields:** `canceled`, `executed_at`, `ext_hour_sold_codes`, `market_center`, `nbbo_ask`, `nbbo_ask_quantity`, `nbbo_bid`, `nbbo_bid_quantity`, `premium`, `price`, `sale_cond_codes`, `size`, `ticker`, `tracking_id`, `trade_code`, `trade_settlement`, `volume`

---

## Earnings

### GET `/api/earnings/afterhours`
After-hours earnings reports.

### GET `/api/earnings/premarket`
Pre-market earnings reports.

### GET `/api/earnings/{ticker}`
Historical ticker earnings.

**Path Parameters:** `ticker`

---

## ETFs

### GET `/api/etfs/{ticker}/exposure`
ETF exposure breakdown.

**Path Parameters:** `ticker`

### GET `/api/etfs/{ticker}/holdings`
ETF holdings.

**Path Parameters:** `ticker`

### GET `/api/etfs/{ticker}/in-outflow`
ETF inflow and outflow data.

**Path Parameters:** `ticker`

### GET `/api/etfs/{ticker}/info`
ETF information.

**Path Parameters:** `ticker`

### GET `/api/etfs/{ticker}/weights`
ETF sector and country weights.

**Path Parameters:** `ticker`

---

## Group Flow

### GET `/api/group-flow/{flow_group}/greek-flow`
Greek flow for a flow group.

**Path Parameters:** `flow_group`

### GET `/api/group-flow/{flow_group}/greek-flow/{expiry}`
Greek flow by expiry for a flow group.

**Path Parameters:** `flow_group`, `expiry`

---

## Insiders

### GET `/api/insider/transactions`
Latest insider transactions. By default, transactions by the same person on the same day with the same trade code are aggregated.

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `ticker_symbol` | No | Filter by ticker |
| `min_value` | No | Minimum transaction value in dollars |
| `max_value` | No | Maximum transaction value in dollars |
| `min_price` | No | Minimum stock price at time of transaction |
| `max_price` | No | Maximum stock price at time of transaction |
| `owner_name` | No | Name of the insider |
| `sectors` | No | Filter by sector(s) |
| `industries` | No | Filter by industry or industries |
| `min_marketcap` | No | Minimum market cap |
| `max_marketcap` | No | Maximum market cap |
| `market_cap_size` | No | Size category: small, mid, large |
| `min_earnings_dte` | No | Minimum days to earnings |
| `max_earnings_dte` | No | Maximum days to earnings |
| `min_amount` | No | Minimum number of shares |
| `max_amount` | No | Maximum number of shares |
| `is_director` | No | Filter by directors (boolean) |
| `is_officer` | No | Filter by officers (boolean) |
| `is_s_p_500` | No | Only S&P 500 companies (boolean) |
| `is_ten_percent_owner` | No | Filter by 10% owners (boolean) |
| `common_stock_only` | No | Only common stock (boolean) |
| `transaction_codes[]` | No | P=Purchase, S=Sale, etc. |
| `limit` | No | Default 500, max 500 |
| `page` | No | Pagination |
| `group` | No | Group same-day transactions (default true) |
| `start_date` | No | Transaction date >= this date (YYYY-MM-DD) |
| `end_date` | No | Transaction date <= this date (YYYY-MM-DD) |

**Response Fields:** `amount`, `date_excercisable`, `director_indirect`, `expiration_date`, `filing_date`, `formtype`, `ids`, `is_10b5_1`, `is_director`, `is_officer`, `is_ten_percent_owner`, `natureofownership`, `officer_title`, `owner_name`, `price`, `price_excercisable`, `security_ad_code`, `security_title`, `shares_owned_after`, `shares_owned_before`, `ticker`, `transaction_code`, `transaction_date`, `transactions`

### GET `/api/insider/{sector}/sector-flow`
Insider sector flow.

**Path Parameters:** `sector`

### GET `/api/insider/{ticker}`
Insiders for a ticker.

**Path Parameters:** `ticker`

### GET `/api/insider/{ticker}/ticker-flow`
Insider ticker flow.

**Path Parameters:** `ticker`

---

## Institutions

### GET `/api/institutions`
List of all institutions.

### GET `/api/institutions/latest_filings`
Latest 13F filings.

### GET `/api/institution/{name}/activity` *(Deprecated)*
Institutional activity. Use v2 instead.

### GET `/api/institution/{name}/activity/v2`
Institutional activity (v2).

**Path Parameters:** `name`

### GET `/api/institution/{name}/holdings`
Institutional holdings.

**Path Parameters:** `name`

### GET `/api/institution/{name}/sectors`
Institutional sector exposure.

**Path Parameters:** `name`

### GET `/api/institution/{ticker}/ownership`
Institutional ownership for a ticker.

**Path Parameters:** `ticker`

---

## Lit Flow

### GET `/api/lit-flow/recent`
Recent on-exchange (lit) flow trades.

### GET `/api/lit-flow/{ticker}`
Ticker-specific lit flow trades.

**Path Parameters:** `ticker`

---

## Market

### GET `/api/market/correlations`
Market correlations.

### GET `/api/market/economic-calendar`
Economic calendar events.

### GET `/api/market/fda-calendar`
FDA calendar.

### GET `/api/market/insider-buy-sells`
Total market insider buy and sell activity.

### GET `/api/market/market-tide`
Market Tide — proprietary market-wide options sentiment indicator based on net premium flow. Data since 2022-09-28.

Bullish when: aggregated call premium increasing faster or put premium decreasing faster.
Bearish when: aggregated call premium decreasing faster or put premium increasing faster.

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `date` | No | Market date (YYYY-MM-DD). Defaults to current/last market day |
| `otm_only` | No | Use OTM contracts only (boolean) |
| `interval_5m` | No | Return 5-minute intervals instead of 1-minute (boolean) |

**Response Fields:** `net_call_premium`, `net_put_premium`, `net_volume`, `timestamp`

### GET `/api/market/oi-change`
Market-wide open interest change.

### GET `/api/market/sector-etfs`
Sector ETF overview.

### GET `/api/market/spike`
SPIKE indicator.

### GET `/api/market/top-net-impact`
Top net impact across market.

### GET `/api/market/total-options-volume`
Total market options volume.

### GET `/api/market/{sector}/sector-tide`
Sector-specific tide.

**Path Parameters:** `sector`

### GET `/api/market/{ticker}/etf-tide`
ETF-specific tide.

**Path Parameters:** `ticker`

### GET `/api/net-flow/expiry`
Net flow by expiry.

---

## News

### GET `/api/news/headlines`
Financial news headlines.

---

## Option Contract

### GET `/api/option-contract/{id}/flow`
Flow data for a specific option contract.

**Path Parameters:** `id` (option symbol, e.g., `AAPL230908C00175000`)

### GET `/api/option-contract/{id}/historic`
Historic data for a specific option contract.

**Path Parameters:** `id`

### GET `/api/option-contract/{id}/intraday`
Intraday data for a specific option contract.

**Path Parameters:** `id`

### GET `/api/option-contract/{id}/volume-profile`
Volume profile for a specific option contract.

**Path Parameters:** `id`

### GET `/api/stock/{ticker}/expiry-breakdown`
Expiry breakdown for a ticker's options.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/option-contracts`
List all option contracts for a ticker.

**Path Parameters:** `ticker`

---

## Option Trade

### GET `/api/option-trades/flow-alerts`
Market-wide unusual options flow alerts.

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `ticker_symbol` | No | Filter by ticker |
| `min_premium` | No | Minimum total premium |
| `max_premium` | No | Maximum total premium |
| `min_size` | No | Minimum contract size |
| `max_size` | No | Maximum contract size |
| `min_volume` | No | Minimum volume |
| `max_volume` | No | Maximum volume |
| `min_open_interest` | No | Minimum open interest |
| `max_open_interest` | No | Maximum open interest |
| `all_opening` | No | Only opening trades (boolean) |
| `is_floor` | No | Floor trades only (boolean) |
| `is_sweep` | No | Sweep trades only (boolean) |
| `is_call` | No | Calls only (boolean) |
| `is_put` | No | Puts only (boolean) |
| `is_ask_side` | No | Ask-side trades only (boolean) |
| `is_bid_side` | No | Bid-side trades only (boolean) |
| `rule_name[]` | No | Alert rule filter (e.g., RepeatedHits) |
| `min_diff` | No | Min contract diff |
| `max_diff` | No | Max contract diff |
| `min_volume_oi_ratio` | No | Min volume/OI ratio |
| `max_volume_oi_ratio` | No | Max volume/OI ratio |
| `is_otm` | No | OTM contracts only (boolean) |
| `issue_types[]` | No | Issue types filter |
| `min_dte` | No | Minimum days to expiry |
| `max_dte` | No | Maximum days to expiry |
| `min_ask_perc` | No | Min ask percentage |
| `max_ask_perc` | No | Max ask percentage |
| `min_bid_perc` | No | Min bid percentage |
| `max_bid_perc` | No | Max bid percentage |
| `min_bull_perc` | No | Min bull percentage |
| `max_bull_perc` | No | Max bull percentage |
| `min_bear_perc` | No | Min bear percentage |
| `max_bear_perc` | No | Max bear percentage |
| `min_skew` | No | Min skew |
| `max_skew` | No | Max skew |
| `min_price` | No | Min underlying price |
| `max_price` | No | Max underlying price |
| `min_iv_change` | No | Min IV change |
| `max_iv_change` | No | Max IV change |
| `min_size_vol_ratio` | No | Min size/volume ratio |
| `max_size_vol_ratio` | No | Max size/volume ratio |
| `min_spread` | No | Min spread |
| `max_spread` | No | Max spread |
| `min_marketcap` | No | Min market cap |
| `max_marketcap` | No | Max market cap |
| `is_multi_leg` | No | Multi-leg only (boolean) |
| `size_greater_oi` | No | Size > open interest (boolean) |
| `vol_greater_oi` | No | Volume > open interest (boolean) |
| `newer_than` | No | Filter trades newer than timestamp |
| `older_than` | No | Filter trades older than timestamp |
| `limit` | No | Default 100, max 200 |

**Response Fields:** `alert_rule`, `all_opening_trades`, `created_at`, `expiry`, `expiry_count`, `has_floor`, `has_multileg`, `has_singleleg`, `has_sweep`, `issue_type`, `open_interest`, `option_chain`, `price`, `strike`, `ticker`, `total_ask_side_prem`, `total_bid_side_prem`, `total_premium`, `total_size`, `trade_count`, `type`, `underlying_price`, `volume`, `volume_oi_ratio`

### GET `/api/option-trades/flow-alerts/{id}`
A single flow alert by ID.

**Path Parameters:** `id`

### GET `/api/option-trades/full-tape/{date}`
Full option trade tape for a date.

**Path Parameters:** `date` (YYYY-MM-DD)

---

## Politician Portfolios

### GET `/api/politician-portfolios/disclosures`
Annual disclosures list.

### GET `/api/politician-portfolios/holders/{ticker}`
Politicians holding a specific ticker.

**Path Parameters:** `ticker`

### GET `/api/politician-portfolios/people`
List of all tracked politicians.

### GET `/api/politician-portfolios/recent_trades`
Recent politician trades.

### GET `/api/politician-portfolios/{politician_id}`
Portfolio for a specific politician.

**Path Parameters:** `politician_id`

---

## Predictions

### GET `/api/predictions/insiders`
Prediction market insiders.

### GET `/api/predictions/market/{asset_id}`
Prediction market details.

**Path Parameters:** `asset_id`

### GET `/api/predictions/market/{asset_id}/liquidity`
Prediction market liquidity.

**Path Parameters:** `asset_id`

### GET `/api/predictions/market/{asset_id}/positions`
Prediction market positions.

**Path Parameters:** `asset_id`

### GET `/api/predictions/search-users`
Search prediction market users.

### GET `/api/predictions/smart-money`
Prediction smart money.

### GET `/api/predictions/unusual`
Unusual prediction markets.

### GET `/api/predictions/user/{user_id}`
Prediction market user profile.

**Path Parameters:** `user_id`

### GET `/api/predictions/whales`
Prediction market whales.

---

## Screener

### GET `/api/screener/analysts`
Analyst ratings screener.

### GET `/api/screener/option-contracts`
Hottest option chains screener.

### GET `/api/screener/stocks`
Stock screener with extensive filtering.

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `ticker` | No | Filter by ticker |
| `issue_types[]` | No | Issue types |
| `min_change` / `max_change` | No | % change from previous day |
| `min_underlying_price` / `max_underlying_price` | No | Stock price range |
| `is_s_p_500` | No | S&P 500 only (boolean) |
| `has_dividends` | No | Dividend payers only (boolean) |
| `sectors[]` | No | Filter by sectors |
| `min_marketcap` / `max_marketcap` | No | Market cap range |
| `min_perc_3_day_total` / `max_perc_3_day_total` | No | Options volume vs 3-day avg ratio |
| `min_perc_3_day_call` / `max_perc_3_day_call` | No | Call volume vs 3-day avg ratio |
| `min_perc_3_day_put` / `max_perc_3_day_put` | No | Put volume vs 3-day avg ratio |
| `min_perc_30_day_total` / `max_perc_30_day_total` | No | Options volume vs 30-day avg ratio |
| `min_perc_30_day_call` / `max_perc_30_day_call` | No | Call volume vs 30-day avg ratio |
| `min_perc_30_day_put` / `max_perc_30_day_put` | No | Put volume vs 30-day avg ratio |
| `min_total_oi_change_perc` / `max_total_oi_change_perc` | No | OI change % |
| `min_call_oi_change_perc` / `max_call_oi_change_perc` | No | Call OI change % |
| `min_put_oi_change_perc` / `max_put_oi_change_perc` | No | Put OI change % |
| `min_implied_move` / `max_implied_move` | No | Implied move range |
| `min_implied_move_perc` / `max_implied_move_perc` | No | Implied move % range |
| `min_volatility` / `max_volatility` | No | Volatility range |
| `min_iv_rank` / `max_iv_rank` | No | IV rank range |
| `min_volume` / `max_volume` | No | Options volume range |
| `min_call_volume` / `max_call_volume` | No | Call volume range |
| `min_put_volume` / `max_put_volume` | No | Put volume range |
| `min_premium` / `max_premium` | No | Options premium range |
| `min_call_premium` / `max_call_premium` | No | Call premium range |
| `min_put_premium` / `max_put_premium` | No | Put premium range |
| `min_net_premium` / `max_net_premium` | No | Net premium range |
| `min_net_call_premium` / `max_net_call_premium` | No | Net call premium range |
| `min_net_put_premium` / `max_net_put_premium` | No | Net put premium range |
| `min_oi` / `max_oi` | No | Open interest range |
| `min_oi_vs_vol` / `max_oi_vs_vol` | No | OI vs volume ratio |
| `min_put_call_ratio` / `max_put_call_ratio` | No | Put/call ratio range |
| `order` | No | Sort field |
| `order_direction` | No | asc or desc |
| `min_stock_volume_vs_avg30_volume` | No | Stock volume vs 30-day avg |
| `date` | No | Market date (YYYY-MM-DD) |

**Response Fields:** `avg_30_day_call_volume`, `avg_30_day_put_volume`, `avg_3_day_call_volume`, `avg_3_day_put_volume`, `avg_7_day_call_volume`, `avg_7_day_put_volume`, `bearish_premium`, `bullish_premium`, `call_open_interest`, `call_premium`, `call_volume`, `call_volume_ask_side`, `call_volume_bid_side`, `close`, `er_time`, `implied_move`, `implied_move_perc`, `is_index`, `issue_type`, `iv30d`, `iv30d_1d`, `iv30d_1m`, `iv30d_1w`, `iv_rank`, `marketcap`, `net_call_premium`, `net_put_premium`, `next_dividend_date`, `next_earnings_date`, `prev_call_oi`, `prev_close`, `prev_put_oi`, `put_call_ratio`, `put_open_interest`, `put_premium`, `put_volume`, `put_volume_ask_side`, `put_volume_bid_side`, `relative_volume`, `sector`, `ticker`, `total_open_interest`, `volatility`, `week_52_high`, `week_52_low`

---

## Seasonality

### GET `/api/seasonality/market`
Market-wide seasonality.

### GET `/api/seasonality/{month}/performers`
Top performers for a given month.

**Path Parameters:** `month`

### GET `/api/seasonality/{ticker}/monthly`
Average return per month for a ticker.

**Path Parameters:** `ticker`

### GET `/api/seasonality/{ticker}/year-month`
Price change per month per year for a ticker.

**Path Parameters:** `ticker`

---

## Shorts

### GET `/api/short_screener`
Short screener.

### GET `/api/shorts/{ticker}/data`
Short data for a ticker.

**Path Parameters:** `ticker`

### GET `/api/shorts/{ticker}/ftds`
Failures to deliver for a ticker.

**Path Parameters:** `ticker`

### GET `/api/shorts/{ticker}/interest-float` *(Deprecated)*
V1 short interest and float. Use v2 instead.

### GET `/api/shorts/{ticker}/interest-float/v2`
V2 short interest and float.

**Path Parameters:** `ticker`

### GET `/api/shorts/{ticker}/volume-and-ratio`
Short volume and ratio.

**Path Parameters:** `ticker`

### GET `/api/shorts/{ticker}/volumes-by-exchange`
Short volume by exchange.

**Path Parameters:** `ticker`

---

## Stock

### GET `/api/stock/{sector}/tickers`
Companies in a sector.

**Path Parameters:** `sector`

### GET `/api/stock/{ticker}/atm-chains`
At-the-money option chains.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/balance-sheets`
Balance sheet data.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/cash-flows`
Cash flow statements.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/earnings`
Earnings history.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/financials`
Full financial data.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/flow-alerts`
Ticker-specific flow alerts.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/flow-per-expiry`
Flow grouped by expiry.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/flow-per-strike`
Flow grouped by strike.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/flow-per-strike-intraday`
Intraday flow grouped by strike.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/flow-recent`
Recent flows for a ticker.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/fundamental-breakdown`
Fundamental breakdown.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/greek-exposure`
Total Greek exposure across all strikes and expiries.

**Path Parameters:** `ticker`

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `date` | No | Market date (YYYY-MM-DD) |

### GET `/api/stock/{ticker}/greek-exposure/expiry`
Greek exposure grouped by expiry.

**Path Parameters:** `ticker`

**Query Parameters:** `date` (optional)

### GET `/api/stock/{ticker}/greek-exposure/strike`
Greek exposure grouped by strike.

**Path Parameters:** `ticker`

**Query Parameters:** `date` (optional)

**Response Fields:** `call_charm`, `call_delta`, `call_gamma`, `call_vanna`, `put_charm`, `put_delta`, `put_gamma`, `put_vanna`, `strike`

### GET `/api/stock/{ticker}/greek-exposure/strike-expiry`
Greek exposure by strike and expiry.

**Path Parameters:** `ticker`

**Query Parameters:** `date` (optional)

### GET `/api/stock/{ticker}/greek-flow`
Greek flow for a ticker.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/greek-flow/{expiry}`
Greek flow by expiry.

**Path Parameters:** `ticker`, `expiry`

### GET `/api/stock/{ticker}/greeks`
Greeks for each strike for a single expiry.

**Path Parameters:** `ticker`

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `expiry` | Yes | Expiry date (YYYY-MM-DD) |
| `date` | No | Market date (YYYY-MM-DD) |

**Response Fields:** `call_charm`, `call_delta`, `call_gamma`, `call_rho`, `call_theta`, `call_vanna`, `call_vega`, `call_volatility`, `date`, `expiry`, `put_charm`, `put_delta`, `put_gamma`, `put_rho`, `put_theta`, `put_vanna`, `put_vega`, `put_volatility`, `strike`

### GET `/api/stock/{ticker}/historical-risk-reversal-skew`
Historical risk reversal skew.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/income-statements`
Income statements.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/info`
Stock information.

**Path Parameters:** `ticker`

**Response Fields:** `announce_time`, `avg30_volume`, `beta`, `full_name`, `has_dividend`, `has_earnings_history`, `has_investment_arm`, `has_options`, `issue_type`, `logo`, `marketcap`, `next_earnings_date`, `sector`, `short_description`

### GET `/api/stock/{ticker}/insider-buy-sells`
Insider buy and sell totals for a ticker.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/interpolated-iv`
Interpolated implied volatility percentiles.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/iv-rank`
IV rank for a ticker.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/max-pain`
Max pain for a ticker.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/net-prem-ticks`
Call/put net premium and volume ticks (1-minute incremental data). Sum each tick with previous ticks to build cumulative chart.

**Path Parameters:** `ticker`

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `date` | No | Market date (YYYY-MM-DD) |

**Response Fields:** `call_volume`, `call_volume_ask_side`, `call_volume_bid_side`, `date`, `net_call_premium`, `net_call_volume`, `net_delta`, `net_put_premium`, `net_put_volume`, `put_volume`, `put_volume_ask_side`, `put_volume_bid_side`, `tape_time`

### GET `/api/stock/{ticker}/nope`
NOPE (Net Options Pricing Effect) indicator.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/ohlc/{candle_size}`
OHLC price data.

**Path Parameters:** `ticker`, `candle_size`

### GET `/api/stock/{ticker}/oi-change`
Open interest change.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/oi-per-expiry`
Open interest by expiry.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/oi-per-strike`
Open interest by strike.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/option-chains`
All option symbols for a ticker on a given day.

**Path Parameters:** `ticker`

**Query Parameters:**

| Name | Required | Description |
|---|---|---|
| `date` | No | Market date (YYYY-MM-DD) |

Option symbol regex: `^(?<symbol>[\w]*)(?<expiry>(\d{2})(\d{2})(\d{2}))(?<type>[PC])(?<strike>\d{8})$`

Strike must be divided by 1,000.

### GET `/api/stock/{ticker}/option/stock-price-levels`
Option price levels.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/option/volume-oi-expiry`
Volume and OI per expiry.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/options-volume`
Options volume and put/call ratios.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/ownership`
Institutional ownership for a ticker.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/spot-exposures`
Spot GEX exposures per 1-minute.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/spot-exposures/expiry-strike`
Spot GEX exposures by strike and expiry (v2).

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/spot-exposures/strike`
Spot GEX exposures by strike.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/spot-exposures/{expiry}/strike` *(Deprecated)*
Spot GEX exposures by strike and expiry. Use `/spot-exposures/expiry-strike` instead.

### GET `/api/stock/{ticker}/stock-state`
Current stock state.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/stock-volume-price-levels`
Off-exchange and lit exchange price levels.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/technical-indicator/{function}`
Technical indicators via Alpha Vantage. Supported functions: RSI, MACD, BBANDS, STOCH, VWAP, SMA, EMA, and others.

**Path Parameters:** `ticker`, `function`

### GET `/api/stock/{ticker}/volatility/realized`
Realized volatility.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/volatility/stats`
Volatility statistics.

**Path Parameters:** `ticker`

### GET `/api/stock/{ticker}/volatility/term-structure`
Implied volatility term structure.

**Path Parameters:** `ticker`

---

## Stock Directory

### GET `/api/stock-directory/ticker-exchanges`
Ticker to exchange mapping.

---

## WebSocket

### GET `/api/socket`
List available WebSocket channels.

### GET `/api/socket/flow_alerts`
WebSocket flow alerts channel info.

### GET `/api/socket/gex`
WebSocket GEX channel info.

### GET `/api/socket/news`
WebSocket news channel info.

### GET `/api/socket/option_trades`
WebSocket option trades channel info.

### GET `/api/socket/price`
WebSocket price channel info.
