---
name: etf-premium
description: >
  Calculate ETF premium/discount vs NAV via Yahoo Finance, and decompose single-day surges
  into NAV-driven vs structural components (gamma squeeze, dealer hedging, blocked AP arbitrage).
  Use whenever the user asks about an ETF's premium or discount, NAV comparison, why an ETF
  diverged from its holdings, or how much of a move is dealer-hedging-driven.
  Triggers: "ETF premium", "ETF discount", "NAV premium", "is SPY at a premium", "BITO premium",
  "IBIT premium", "bond ETF discount", "trading above/below NAV", "ETF premium screener",
  "biggest discount", "compare ETF NAV", "ETF arbitrage", "ETF gamma squeeze",
  "ETF premium surge", "decompose ETF move", "dealer gamma exposure", "GEX for ETF",
  "why did this ETF jump", "premium convergence", "AP arbitrage blocked", or any request
  about the gap between an ETF's price and underlying value. Especially relevant for
  leveraged, inverse, international, bond, commodity, and crypto ETFs.
---

# ETF Premium/Discount Analysis Skill

Calculates the premium or discount of an ETF's market price relative to its Net Asset Value (NAV) using data from Yahoo Finance via [yfinance](https://github.com/ranaroussi/yfinance).

**Why this matters:** An ETF's market price can diverge from the value of its underlying holdings (NAV). When you buy at a premium, you're overpaying relative to the assets; at a discount, you're getting a bargain. This divergence is typically small for liquid US equity ETFs but can be significant for bond ETFs, international ETFs, leveraged/inverse products, and crypto ETFs — especially during periods of market stress.

**Important**: For research and educational purposes only. Not financial advice. yfinance is not affiliated with Yahoo, Inc.

---

## Step 1: Ensure Dependencies Are Available

**Current environment status:**

```
!`python3 -c "import yfinance, pandas, numpy; print(f'yfinance={yfinance.__version__} pandas={pandas.__version__} numpy={numpy.__version__}')" 2>/dev/null || echo "DEPS_MISSING"`
```

If `DEPS_MISSING`, install required packages:

```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance", "pandas", "numpy"])
```

If already installed, skip and proceed.

---

## Step 2: Route to the Correct Sub-Skill

Classify the user's request and jump to the matching section. If the user asks a general question about an ETF's premium or discount without specifying a particular analysis type, default to **Sub-Skill A** (Single ETF Snapshot).

| User Request | Route To | Examples |
|---|---|---|
| Single ETF premium/discount | **Sub-Skill A: Single ETF Snapshot** | "is SPY at a premium?", "AGG premium to NAV", "BITO premium" |
| Compare multiple ETFs | **Sub-Skill B: Multi-ETF Comparison** | "compare bond ETF discounts", "which has bigger premium IBIT or BITO", "rank these ETFs by premium" |
| Screener / find extreme premiums | **Sub-Skill C: Premium Screener** | "which ETFs have biggest discount", "find ETFs trading below NAV", "premium screener" |
| Deep analysis with context | **Sub-Skill D: Premium Deep Dive** | "why is HYG at a discount", "is ARKK premium normal", "ETF premium analysis with context" |
| Sudden premium surge / gamma squeeze | **Sub-Skill E: Premium Surge Decomposition** | "why did KWEB jump 13% today", "is this ETF rally driven by gamma", "decompose today's ETF move", "dealer GEX for SOXL", "how long until the premium converges" |

### Defaults

| Parameter | Default |
|---|---|
| Data source | yfinance `navPrice` field |
| Price field | `regularMarketPrice` (falls back to `previousClose`) |
| Screener universe | Common ETF list by category (see Sub-Skill C) |

---

## Sub-Skill A: Single ETF Snapshot

**Goal**: Show the current premium/discount for one ETF with context about what's normal, plus a peer comparison to show how it stacks up against similar ETFs.

### A1: Fetch and compute

```python
import yfinance as yf

# Peer groups by category — used to automatically compare the target ETF against its closest peers
CATEGORY_PEERS = {
    "Digital Assets": ["IBIT", "BITO", "FBTC", "ETHA", "ARKB", "GBTC"],
    "Intermediate Core Bond": ["AGG", "BND", "SCHZ"],
    "High Yield Bond": ["HYG", "JNK", "USHY"],
    "Long Government": ["TLT", "VGLT", "SPTL"],
    "Emerging Markets Bond": ["EMB", "VWOB", "PCY"],
    "Large Growth": ["QQQ", "VUG", "IWF", "SCHG"],
    "Large Blend": ["SPY", "VOO", "IVV", "VTI"],
    "Commodities Focused": ["GLD", "IAU", "SLV", "DBC"],
    "China Region": ["KWEB", "FXI", "MCHI"],
    "Trading--Leveraged Equity": ["TQQQ", "UPRO", "SOXL", "JNUG"],
    "Trading--Inverse Equity": ["SQQQ", "SPXU", "SOXS", "JDST"],
    "Derivative Income": ["JEPI", "JEPQ", "QYLD"],
    "Large Value": ["SCHD", "VYM", "DVY", "HDV"],
}

def etf_premium_snapshot(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    # Verify this is an ETF
    quote_type = info.get("quoteType", "")
    if quote_type != "ETF":
        return {"error": f"{ticker_symbol} is not an ETF (quoteType={quote_type})"}

    price = info.get("regularMarketPrice") or info.get("previousClose")
    nav = info.get("navPrice")

    if not price or not nav or nav <= 0:
        return {"error": f"NAV data not available for {ticker_symbol}"}

    premium_pct = (price - nav) / nav * 100
    premium_dollar = price - nav

    # Additional context
    result = {
        "ticker": ticker_symbol,
        "name": info.get("longName") or info.get("shortName", ""),
        "market_price": round(price, 4),
        "nav": round(nav, 4),
        "premium_discount_pct": round(premium_pct, 4),
        "premium_discount_dollar": round(premium_dollar, 4),
        "status": "PREMIUM" if premium_pct > 0 else "DISCOUNT" if premium_pct < 0 else "AT NAV",
        "category": info.get("category", "N/A"),
        "fund_family": info.get("fundFamily", "N/A"),
        "total_assets": info.get("totalAssets"),
        "net_expense_ratio": info.get("netExpenseRatio"),
        "avg_volume": info.get("averageVolume"),
        "bid": info.get("bid"),
        "ask": info.get("ask"),
        "yield_pct": info.get("yield"),
        "ytd_return": info.get("ytdReturn"),
    }

    # Bid-ask spread as context for whether the premium is meaningful
    bid = info.get("bid")
    ask = info.get("ask")
    if bid and ask and bid > 0:
        spread_pct = (ask - bid) / ((ask + bid) / 2) * 100
        result["bid_ask_spread_pct"] = round(spread_pct, 4)

    return result
```

### A2: Fetch peer comparison

After computing the target ETF's snapshot, look up its `category` and pull premium data for peers in the same category. This gives the user immediate context on whether the premium is ETF-specific or market-wide.

Use the target's `category` to select `CATEGORY_PEERS`, remove the target, and run the same price/NAV calculation for each peer. Skip unavailable NAV rows but report how many peers were requested and returned so missing data is visible.

Present the peer comparison as a small table after the main snapshot. This helps the user see whether the premium is unique to their ETF or shared across the category — for example, if all crypto ETFs are at ~1.5% premium, the user's ETF isn't an outlier.

### A3: Interpret the result

Use this framework to explain whether the premium/discount is meaningful:

| Premium/Discount | Interpretation |
|---|---|
| Within +/- 0.05% | Essentially at NAV — normal for large, liquid ETFs |
| +/- 0.05% to 0.25% | Minor deviation — common and usually not actionable |
| +/- 0.25% to 1.0% | Notable — worth mentioning. Check bid-ask spread and category |
| +/- 1.0% to 3.0% | Significant — common for less liquid, international, or specialty ETFs |
| Beyond +/- 3.0% | Large — may indicate stress, illiquidity, or structural issues |

**Context matters by category:**
- **US large-cap equity** (SPY, QQQ, IVV): premiums > 0.10% are unusual
- **Bond ETFs** (AGG, HYG, LQD, TLT): discounts of 0.5-2% happen during volatility
- **International/EM** (EEM, VWO, KWEB): time-zone mismatch causes regular 0.3-1% deviations
- **Leveraged/Inverse** (TQQQ, SQQQ, JNUG): 0.3-1.5% is normal due to daily reset mechanics
- **Crypto** (IBIT, BITO): 1-3% premiums are common, especially for newer funds
- **Commodity** (GLD, USO, UNG): depends on contango/backwardation in futures

Also compare the premium/discount to the **bid-ask spread**: if the premium is smaller than the spread, it's noise, not signal.

---

## Sub-Skill B: Multi-ETF Comparison

**Goal**: Compare premium/discount across multiple ETFs side by side.

### B1: Fetch and rank

```python
import yfinance as yf
import pandas as pd

def compare_etf_premiums(tickers):
    rows = []
    for sym in tickers:
        try:
            t = yf.Ticker(sym)
            info = t.info
            if info.get("quoteType") != "ETF":
                rows.append({"ticker": sym, "error": "Not an ETF"})
                continue
            price = info.get("regularMarketPrice") or info.get("previousClose")
            nav = info.get("navPrice")
            if price and nav and nav > 0:
                prem = (price - nav) / nav * 100
                bid = info.get("bid", 0)
                ask = info.get("ask", 0)
                spread = (ask - bid) / ((ask + bid) / 2) * 100 if bid and ask and bid > 0 else None
                rows.append({
                    "ticker": sym,
                    "name": info.get("shortName", ""),
                    "price": round(price, 2),
                    "nav": round(nav, 2),
                    "premium_pct": round(prem, 4),
                    "spread_pct": round(spread, 4) if spread else None,
                    "category": info.get("category", "N/A"),
                    "total_assets": info.get("totalAssets"),
                })
            else:
                rows.append({"ticker": sym, "error": "NAV unavailable"})
        except Exception as e:
            rows.append({"ticker": sym, "error": str(e)})

    df = pd.DataFrame(rows)
    if "premium_pct" in df.columns:
        df = df.sort_values("premium_pct", ascending=True)
    return df
```

### B2: Present as a ranked table

Sort by premium/discount (most discounted first). Highlight:
- Which ETFs are at the deepest discount
- Which are at the highest premium
- Whether the premium/discount exceeds the bid-ask spread (if it doesn't, it's market microstructure noise)

---

## Sub-Skill C: Premium Screener

**Goal**: Scan a universe of common ETFs to find those with the largest premiums or discounts.

### C1: Define the universe and scan

Use the category-organized universe in `references/etf_premium_reference.md`, or the user's own list. Apply the Sub-Skill A calculation to each symbol, preserve category labels, filter by the requested absolute premium threshold, and sort from deepest discount to highest premium. Keep failed or missing-NAV counts visible instead of silently treating them as zero.

### C2: Present the results

Show a ranked table sorted by premium (most discounted first). Group by category if the list is long. Call out:
- **Top 5 deepest discounts** — potential buying opportunities (or signs of stress)
- **Top 5 highest premiums** — overpaying risk
- **Category patterns** — are all bond ETFs at a discount? Are all crypto ETFs at a premium?

Warn that large universes may take 1-2 minutes.

---

## Sub-Skill D: Premium Deep Dive

**Goal**: Combine premium/discount data with additional context to help the user understand *why* the premium exists and whether it's likely to persist.

### D1: Gather comprehensive data

Run the Sub-Skill A snapshot, then pull three months of daily history and add:

- Annualized volatility: `std(daily returns) * sqrt(252)`
- Average daily dollar volume: `mean(close * volume)`
- Percentage distance from the three-month closing high
- AUM, expense ratio, yield, YTD return, and three-year beta
- Bid-ask spread percentage and whether the absolute premium exceeds that spread

Keep unavailable fields as `null` rather than inventing values. Timestamp price and NAV inputs so users can judge whether the comparison is synchronized.

### D2: Explain the *why*

After gathering data, explain the premium/discount using this diagnostic framework:

**Common causes of premiums:**
- **Demand surge** — more buyers than authorized participants can create shares (common for new/hot ETFs like crypto)
- **Time-zone mismatch** — international ETF trading when underlying markets are closed; price reflects anticipated moves
- **Creation mechanism bottleneck** — when authorized participants face constraints on creating new shares
- **Sentiment premium** — retail demand pushes price above fair value during hype cycles

**Common causes of discounts:**
- **Liquidity stress** — during sell-offs, bond and credit ETFs often trade at discounts because underlying bonds are harder to price/trade than the ETF itself
- **Redemption pressure** — heavy outflows but slow authorized participant response
- **Stale NAV** — the official NAV may not reflect after-hours news or events
- **Structural issues** — contango in futures-based ETFs (USO, UNG) creates persistent drag

**Is the premium likely to persist?**
- For liquid US equity ETFs: No — arbitrage corrects deviations within minutes
- For bond ETFs during stress: Discounts can persist for days or weeks
- For crypto ETFs: Premiums tend to narrow as the fund matures and APs become more active
- For international ETFs: Resets daily as underlying markets open

---

## Sub-Skill E: Premium Surge Decomposition (Gamma Squeeze Analysis)

**Goal**: When an ETF has just experienced a dramatic intraday move that diverges from its underlying holdings, decompose the move into (1) a fundamental NAV-driven component and (2) an "excess premium" driven by structural forces — most commonly options dealer gamma hedging, AP arbitrage breakdowns, or sentiment surges. Then assess how long the premium will likely take to converge.

This sub-skill is appropriate when the user reports or asks about:
- An ETF moving 5%+ in a single session
- A divergence between the ETF and its named underlyings (e.g., "MSTR jumped 13% but BTC only rose 3%")
- A suspected gamma squeeze in an ETF or single name
- Whether dealer hedging is amplifying a move

Read `references/gamma_squeeze_reference.md` for the full GEX formula derivation, dealer-positioning conventions, and worked examples before running E2.

### E1: Decompose today's move into NAV-driven vs excess premium

The static `navPrice` field gives only the most recent end-of-day NAV. Estimate today's NAV return from current holdings weights and same-session holding returns, normalize by the covered weight, then calculate:

```text
NAV proxy return = sum(weight_i x return_i) / covered weight
Excess premium return = ETF return - NAV proxy return
```

Report holdings coverage and the per-holding returns used. If `funds_data.top_holdings` is incomplete, prefer issuer-published holdings or user-supplied weights.

**Caveat**: For international ETFs whose underlyings trade in a closed session (e.g., Asian holdings during US hours), the holdings' US-listed proxies (ADRs) or futures must be used. If neither is available, flag this to the user — the NAV proxy will be stale.

### E2: Compute dealer gamma exposure (GEX) from the options chain

GEX approximates dealer hedging sensitivity per 1% underlying move. Read the formulas and both positioning conventions in `references/gamma_squeeze_reference.md`, calculate contract gamma from current spot, strike, time, risk-free rate, and IV, then aggregate `OI x gamma x spot^2` across the chain.

Return call GEX, put GEX, SqueezeMetrics-style net GEX, gross hedge pressure, call/put OI ratio, median near-ATM IV, expirations analyzed, and the top strike/expiry concentrations. State the sign convention explicitly; do not infer actual dealer inventory from public OI alone.

Interpret the output:

- **`net_gex_squeezemetrics_$` highly negative** → dealers are short gamma; rallies will be amplified by their hedging buys. Classic gamma-squeeze fuel.
- **Concentration on a single near-dated strike** (e.g., the article's "June $45 calls") → squeeze is fragile and concentrated. When that strike expires or the spot moves past it, the gamma decays sharply.
- **ATM IV well above the recent average** (article example: 78 vs typical ~30–40) → market is pricing in continued large moves; option premium decay alone will provide some convergence pressure over days.
- **Call/Put OI ratio > 2.5** → call-heavy positioning, consistent with a bullish gamma squeeze setup.

### E3: Compare structural buying pressure to actual volume

Estimate the upper-bound dealer share with:

```text
Implied dealer-driven dollars = abs(GEX per 1% move) x abs(ETF return in percentage points)
Dealer share of volume = implied dealer-driven dollars / (close x volume)
```

This is a rough estimate — it assumes every contract's full gamma was hedged in a single direction during the move. Real hedging is incremental, and not all dealers hedge identically. Treat as an upper-bound heuristic, not a precise figure. Always present it alongside the assumptions.

### E4: Assess premium convergence timeline

The article's three-tier convergence framework:

| Time scale | Mechanism | What to check |
|---|---|---|
| **Hours** | AP creation/redemption arbitrage | Is the underlying market open? Are creation units restricted? Is the spread between bid/ask widening (suggests AP stepping back)? |
| **Days** | Options expiration / gamma decay | When does the dominant strike's expiration land? Is OI rolling forward or being closed? Is IV starting to compress? |
| **Weeks** | Net flow normalization | Is the ETF receiving large daily inflows (signals demand outpacing creation capacity)? Is short interest building (potential additional squeeze fuel)? |

For the hours view, record whether the underlying market is open and whether creation/redemption is constrained. For the days view, calculate days to the largest gamma concentration's expiry and check whether IV and OI are decaying or rolling. For the weeks view, use issuer flow/creation data where available; AUM alone is only a rough proxy.

### E5: Present the decomposition

Format the answer in this order:

1. **Headline number**: today's ETF move, NAV-proxy move, and the excess premium (in pp).
2. **Decomposition table**:

   | Component | Contribution |
   |---|---|
   | NAV-driven (holdings × weights) | +X.X% |
   | Excess premium (residual) | +Y.Y% |
   | Total ETF move | +Z.Z% |

3. **Dealer hedging quantification**:
   - Net GEX (SqueezeMetrics convention)
   - Implied dealer $ buying for the day vs actual $ volume
   - Estimated dealer share of buying pressure
4. **Risk indicators**: ATM IV, call/put OI ratio, top-3 strike/expiration concentrations.
5. **Convergence outlook**: list each of the hours/days/weeks mechanisms with the current state of each.
6. **Caveats**: the GEX estimate assumes uniform dealer positioning; the NAV proxy is stale during overnight sessions; this is *not* a forecast of future price.

---

## Step 3: Respond to the User

### Always include
- The **ETF name and ticker**
- **Market price** and **NAV** with the calculation shown
- **Premium/discount percentage** clearly labeled
- **Context**: is this deviation normal for this ETF category?

### Always caveat
- NAV data from Yahoo Finance reflects the **most recent official NAV** (typically end of prior trading day) — it is not real-time
- Market price may have a **15-minute delay** depending on the exchange
- Premium/discount can change rapidly during market hours — this is a snapshot, not a live feed
- Small premiums/discounts (< bid-ask spread) are **market microstructure noise**, not real mispricing
- **Never recommend buying or selling** based on premium/discount alone — present the data and let the user decide

### Formatting
- Use markdown tables for multi-ETF comparisons
- Show the formula: `Premium/Discount = (Market Price - NAV) / NAV x 100`
- Use color indicators in text: "trading at a **0.45% discount**" or "at a **1.2% premium**"
- Round percentages to 2-4 decimal places depending on magnitude

---

## Reference Files

- `references/etf_premium_reference.md` — Detailed formulas, category-specific benchmarks, common ETF universe list, and background on the creation/redemption mechanism that drives premiums
- `references/gamma_squeeze_reference.md` — Premium decomposition framework, Black-Scholes gamma + GEX formulas with both SqueezeMetrics and customer-net-long conventions, convergence-timeline framework (hours/days/weeks), gamma-squeeze vs routine-rally diagnostic table, and a worked example. Read this **before** running Sub-Skill E.

Read the reference files for deeper technical detail on ETF premium/discount mechanics, historical context, and the gamma-squeeze decomposition methodology.
