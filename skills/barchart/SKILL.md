---
name: barchart
description: >
  Fetch stock quotes, options chains, options greeks, and unusual options flow from Barchart
  using opencli (read-only).
  Use this skill whenever the user asks for Barchart data, stock quotes with market metrics,
  options chains with greeks and IV, near-the-money greeks overview, or unusual options activity / options flow.
  Triggers include: "barchart quote", "get me the barchart data", "options chain from barchart",
  "options greeks", "near the money greeks", "unusual options activity", "options flow",
  "what's the flow on AAPL", "show me unusual activity", "vol/OI ratio", "institutional flow",
  "smart money", "whale activity", "dark pool flow", "options sweep",
  any mention of barchart.com data, or requests for options flow sorted by volume/open interest ratio.
  This skill is READ-ONLY — it does NOT support placing trades or modifying any data.
---

# Barchart Skill (Read-Only)

Fetches stock quotes, options chains, options greeks, and unusual options flow from [Barchart](https://www.barchart.com) using [opencli](https://github.com/jackwener/opencli), a CLI tool that accesses websites via your Chrome browser session.

**This skill is read-only.** It retrieves market data for research purposes only. It does NOT support placing trades or modifying any data.

**Important**: This tool uses your Chrome browser session cookies. No API keys needed — it authenticates via your logged-in browser session.

---

## Step 1: Ensure opencli Is Installed and Connected

Before running any command, verify opencli is available:

```bash
command -v opencli || npm install -g @jackwener/opencli

# Check browser connection
opencli doctor
```

If opencli is not connected to Chrome, guide the user:

1. Install the [Playwright MCP Bridge](https://chromewebstore.google.com/detail/playwright-mcp-bridge/iiejdkmfhfnogkgikpfoddjikfciaiob) Chrome extension
2. Run `opencli setup` to auto-discover the auth token and validate connectivity
3. Be logged into [barchart.com](https://www.barchart.com) in Chrome

---

## Step 2: Identify What the User Needs

Match the user's request to one of the commands below, then use the corresponding syntax from `references/commands.md`.

| User Request | Command | Key Flags |
|---|---|---|
| Stock price, quote, market cap, P/E | `opencli barchart quote` | `--symbol AAPL` |
| Options chain, strikes, bid/ask, greeks | `opencli barchart options` | `--symbol AAPL`, `--type Call/Put`, `--limit N` |
| Near-the-money greeks overview | `opencli barchart greeks` | `--symbol AAPL`, `--expiration YYYY-MM-DD`, `--limit N` |
| Unusual options activity, options flow | `opencli barchart flow` | `--type all/call/put`, `--limit N` |

---

## Step 3: Execute the Command

### General pattern

```bash
# Stock quote with key metrics
opencli barchart quote --symbol AAPL

# Options chain — calls near the money
opencli barchart options --symbol AAPL --type Call --limit 10

# Options chain — puts
opencli barchart options --symbol TSLA --type Put --limit 15

# Near-the-money greeks for both calls and puts
opencli barchart greeks --symbol AAPL --limit 5

# Greeks for a specific expiration
opencli barchart greeks --symbol AAPL --expiration 2026-04-17 --limit 10

# Unusual options activity (all types)
opencli barchart flow --limit 20

# Filter flow to calls or puts only
opencli barchart flow --type call --limit 10
opencli barchart flow --type put --limit 10
```

### Output formats

All opencli commands support output format flags:

```bash
opencli barchart quote --symbol AAPL -f json    # JSON output
opencli barchart quote --symbol AAPL -f yaml    # YAML output
opencli barchart quote --symbol AAPL -f csv     # CSV output
opencli barchart flow --limit 10 -f markdown    # Markdown table
```

Default output is a formatted table.

### Key rules

1. **Check connection first** — run `opencli doctor` if commands fail
2. **Use `-f json` or `-f yaml`** for structured output when processing data programmatically
3. **Use `--limit N`** to control result size — start with 10-20 unless the user asks for more
4. **Symbol is required** for `quote`, `options`, and `greeks` commands
5. **Flow does not require a symbol** — it shows market-wide unusual activity
6. **Flow type filter** — use `--type call` or `--type put` to filter; default is `all`
7. **Options type** — use `--type Call` or `--type Put` for options chain; default is `Call`
8. **NEVER execute trades** — this skill is read-only; do not place orders or modify any data

---

## Step 4: Present the Results

After fetching data, present it clearly for financial research:

### Quote data
- **Highlight key metrics** — price, change, change%, volume vs avg volume, market cap, P/E, EPS
- **Flag notable moves** — large % changes, unusual volume (volume >> avg volume)

### Options chain data
- **Show the chain as a table** — strike, bid, ask, last, volume, OI, IV, delta
- **Highlight liquid strikes** — high volume and open interest indicate liquid contracts
- **Note IV levels** — compare to historical or cross-strike to identify skew

### Greeks data
- **Present calls and puts separately** — or side-by-side for comparison
- **Highlight delta exposure** — useful for hedging analysis
- **Note theta decay** — relevant for time-sensitive positions

### Flow / unusual activity data
- **Sort by vol/OI ratio** — higher ratios suggest new positioning
- **Flag large volume** — especially when volume >> open interest
- **Note sentiment** — heavy call flow = bullish signal, heavy put flow = bearish signal
- **Include expiration dates** — helps assess whether activity is short-term or longer-dated

---

## Step 5: Diagnostics

If something isn't working:

```bash
# Check opencli health and browser connection
opencli doctor

# List all available commands
opencli list
```

| Error | Cause | Fix |
|-------|-------|-----|
| `opencli: command not found` | Not installed | `npm install -g @jackwener/opencli` |
| Browser connection failed | Extension not installed or Chrome not running | Install Playwright MCP Bridge extension, restart Chrome |
| Empty results | Not logged into barchart.com | Log into barchart.com in Chrome |
| Rate limited / blocked | Too many requests | Wait a few minutes and retry |

---

## Reference Files

- `references/commands.md` — Complete command reference with all flags, output columns, and usage examples

Read the reference file when you need exact command syntax or column definitions.
