# Reliable data fallbacks for US market close daily email

Use this reference when the generated report would otherwise contain `暂无可靠数据`. Prefer a sourced replacement over a generic missing-data note.

## Tested reachable sources

### Treasury yields and curves
- Primary: U.S. Treasury CSV
  - `https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{YEAR}/all?type=daily_treasury_yield_curve&field_tdr_date_value={YEAR}&page&_format=csv`
  - Tested reachable. Columns include `2 Yr`, `10 Yr`, `30 Yr`.
  - Use latest row with data. Compute `2Y-10Y` and `10Y-30Y`; show the source date.
- Fallback: FRED CSV
  - `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2`
  - `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10`
  - `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS30`

### Credit spreads
- FRED CSV works and is usually delayed one trading day.
- HY OAS: `BAMLH0A0HYM2`
- IG OAS: `BAMLC0A0CM`
- URL pattern: `https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}`
- Always display source date to avoid implying same-day availability.

### Volatility, MOVE, term structure
- yfinance tested symbols:
  - `^MOVE` for bond volatility
  - `^VVIX` for volatility-of-volatility
  - `^VIX` and `^VIX3M` for VIX term-structure proxy
- CBOE CSV fallbacks:
  - `https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv`
  - `https://cdn.cboe.com/api/global/us_indices/daily_prices/VVIX_History.csv`
- VIX term structure can be reported as `^VIX3M - ^VIX` or `^VIX3M / ^VIX`; label it as a proxy.

### Put/Call Ratio
- CBOE CSV works:
  - `https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/totalpc.csv`
- Parse the latest available row. The file begins with disclaimer text before the table, so parsing may need to skip non-CSV header lines.

### NYSE/Nasdaq advancers and decliners
- Nasdaq screener API works with a browser User-Agent:
  - `https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=10000&exchange=nasdaq`
  - `https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=10000&exchange=nyse`
- Compute from `pctchange`:
  - `>0` = advancer
  - `<0` = decliner
  - `0` or blank = flat/unknown
- Disclose the limitation: Nasdaq screener may include common stocks plus ETFs/ADRs depending on exchange filters.

### 52-week highs/lows
- First try Barchart pages:
  - `https://www.barchart.com/stocks/highs-lows/highs?timeFrame=1y`
  - `https://www.barchart.com/stocks/highs-lows/lows?timeFrame=1y`
- Barchart proxy API may return 401 without browser/session cookies. If page/API extraction fails, write `暂无可靠数据` and state that Barchart extraction failed; do not estimate from a small sample.

### Earnings calendar
- Nasdaq earnings API works:
  - `https://api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD`
- Available fields include EPS, EPS forecast, surprise, market cap, fiscal quarter, and number of estimates. Revenue often is not included; use company IR/SEC/Yahoo/Reuters if needed, otherwise mark revenue unavailable.

### Economic calendar
- Try Nasdaq economic events API:
  - `https://api.nasdaq.com/api/calendar/economicevents?date=YYYY-MM-DD`
- It may return `No record found` for dates without events or when endpoint coverage is sparse.
- For major releases, use official/FRED sources rather than generic placeholders: BLS (CPI, payrolls), BEA (PCE/GDP), DOL (jobless claims), Census (retail/housing), ISM, JOLTS/BLS, Treasury auctions.
- Distinguish `no major event found` from `source unavailable`.

### Market breadth above moving averages
- S&P 500 constituents: Wikipedia `List_of_S%26P_500_companies` with `User-Agent: Mozilla/5.0` works.
- Nasdaq-100 constituents: Wikipedia `Nasdaq-100` table with `Ticker` column works.
- Use yfinance daily history per constituent and compute percentage above 20/50/100/200 DMA.
- For Russell 2000/full NYSE/full Nasdaq, use proxies if full constituent computation is too costly; label the proxy.

### SIVE
- Yahoo `SIVE` returns no data.
- Tested alternatives:
  - `SIVE.ST` works for Sivers Semiconductors Stockholm.
  - `SIVEF` works for OTC.
- Prefer `SIVE.ST`, then `SIVEF`; explicitly label the substituted ticker/exchange.

### Index volume
- SOX and VIX are indexes; volume is not applicable, not missing.
- Report `不适用（指数无成交量）` and use proxies when useful:
  - SOX: SMH/SOXX volume
  - VIX: VXX/UVXY volume or VIX/VIX3M term-structure proxy

## Email formatting pitfall
Gmail does not reliably preserve CSS grid/flex in email bodies. Build the top `市场快照` with a presentation table, not a grid/flex snapshot container.

Required order:
1. SPY / QQQ / IWM
2. SMH / VIX / 10Y
3. DXY / WTI / BTC

Use inline color styles for change values, e.g. `style="color:#047857"` for gains and `style="color:#dc2626"` for losses.
