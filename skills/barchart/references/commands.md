# Barchart Commands Reference

Complete reference for all `opencli barchart` commands.

---

## `barchart quote`

Fetch a stock quote with price, volume, and key financial metrics.

### Usage

```bash
opencli barchart quote --symbol <TICKER>
```

### Arguments

| Argument | Required | Type | Default | Description |
|----------|----------|------|---------|-------------|
| `--symbol` | Yes | string | — | Stock ticker (e.g. AAPL, MSFT, TSLA) |

### Output Columns

| Column | Description |
|--------|-------------|
| `symbol` | Ticker symbol |
| `name` | Company name |
| `price` | Last traded price |
| `change` | Price change (absolute) |
| `changePct` | Price change (percentage) |
| `open` | Opening price |
| `high` | Day high |
| `low` | Day low |
| `prevClose` | Previous close |
| `volume` | Trading volume |
| `avgVolume` | Average volume |
| `marketCap` | Market capitalization |
| `peRatio` | Price-to-earnings ratio |
| `eps` | Earnings per share |

### Examples

```bash
# Basic stock quote
opencli barchart quote --symbol AAPL

# JSON output for programmatic use
opencli barchart quote --symbol MSFT -f json

# YAML output
opencli barchart quote --symbol TSLA -f yaml
```

---

## `barchart options`

Fetch an options chain with strike prices, bid/ask, volume, open interest, IV, and greeks.

### Usage

```bash
opencli barchart options --symbol <TICKER> [--type Call|Put] [--limit N]
```

### Arguments

| Argument | Required | Type | Default | Description |
|----------|----------|------|---------|-------------|
| `--symbol` | Yes | string | — | Stock ticker (e.g. AAPL) |
| `--type` | No | string | `Call` | Option type: `Call` or `Put` |
| `--limit` | No | int | `20` | Max number of strikes to return |

### Output Columns

| Column | Description |
|--------|-------------|
| `strike` | Strike price |
| `bid` | Bid price |
| `ask` | Ask price |
| `last` | Last traded price |
| `change` | Price change |
| `volume` | Trading volume |
| `openInterest` | Open interest |
| `iv` | Implied volatility (%) |
| `delta` | Delta (rate of change of option price vs underlying) |
| `gamma` | Gamma (rate of change of delta) |
| `theta` | Theta (time decay per day) |
| `vega` | Vega (sensitivity to IV changes) |
| `expiration` | Expiration date |

### Notes

- Results are sorted by closeness to the current stock price (near-the-money first)
- Use `--type Put` for put options; default is `Call`

### Examples

```bash
# Near-the-money calls (default)
opencli barchart options --symbol AAPL --type Call --limit 10

# Near-the-money puts
opencli barchart options --symbol TSLA --type Put --limit 15

# Full chain as markdown table
opencli barchart options --symbol MSFT --limit 30 -f markdown
```

---

## `barchart greeks`

Fetch a near-the-money greeks overview for both calls and puts — IV, delta, gamma, theta, vega, rho.

### Usage

```bash
opencli barchart greeks --symbol <TICKER> [--expiration YYYY-MM-DD] [--limit N]
```

### Arguments

| Argument | Required | Type | Default | Description |
|----------|----------|------|---------|-------------|
| `--symbol` | Yes | string | — | Stock ticker (e.g. AAPL) |
| `--expiration` | No | string | Nearest expiry | Expiration date (YYYY-MM-DD) |
| `--limit` | No | int | `10` | Number of near-the-money strikes per type (calls + puts) |

### Output Columns

| Column | Description |
|--------|-------------|
| `type` | `Call` or `Put` |
| `strike` | Strike price |
| `last` | Last traded price |
| `iv` | Implied volatility (%) |
| `delta` | Delta |
| `gamma` | Gamma |
| `theta` | Theta |
| `vega` | Vega |
| `rho` | Rho (sensitivity to interest rate changes) |
| `volume` | Trading volume |
| `openInterest` | Open interest |
| `expiration` | Expiration date |

### Notes

- Returns both calls and puts, sorted by closeness to current price
- If `--expiration` is omitted, uses the nearest expiration date
- Useful for quick delta/gamma exposure analysis

### Examples

```bash
# Near-the-money greeks (nearest expiry)
opencli barchart greeks --symbol AAPL --limit 5

# Greeks for a specific expiration
opencli barchart greeks --symbol AAPL --expiration 2026-04-17 --limit 10

# JSON output
opencli barchart greeks --symbol MSFT -f json
```

---

## `barchart flow`

Fetch unusual options activity (options flow) sorted by volume/OI ratio. Shows trades that may indicate institutional or "smart money" positioning.

### Usage

```bash
opencli barchart flow [--type all|call|put] [--limit N]
```

### Arguments

| Argument | Required | Type | Default | Description |
|----------|----------|------|---------|-------------|
| `--type` | No | string | `all` | Filter: `all`, `call`, or `put` |
| `--limit` | No | int | `20` | Number of results |

### Output Columns

| Column | Description |
|--------|-------------|
| `symbol` | Underlying ticker |
| `type` | `Call` or `Put` |
| `strike` | Strike price |
| `expiration` | Expiration date |
| `last` | Last traded price |
| `volume` | Trading volume |
| `openInterest` | Open interest |
| `volOiRatio` | Volume / Open Interest ratio (higher = more unusual) |
| `iv` | Implied volatility (%) |

### Notes

- Does **not** require a `--symbol` — shows market-wide unusual activity
- Sorted by vol/OI ratio (descending) — highest ratios indicate most unusual activity
- A high vol/OI ratio means today's volume far exceeds existing open interest, suggesting new positioning
- Use `--type call` or `--type put` to filter by direction

### Examples

```bash
# Top 20 unusual options activity
opencli barchart flow --limit 20

# Unusual call activity only
opencli barchart flow --type call --limit 10

# Unusual put activity only
opencli barchart flow --type put --limit 10

# CSV output for spreadsheet analysis
opencli barchart flow --limit 50 -f csv
```

---

## Global Output Flags

All commands support these output format flags:

| Flag | Format | Description |
|------|--------|-------------|
| `-f table` | Table | Formatted ASCII table (default) |
| `-f json` | JSON | Structured JSON output |
| `-f yaml` | YAML | Structured YAML output |
| `-f csv` | CSV | Comma-separated values |
| `-f markdown` | Markdown | Markdown table |
