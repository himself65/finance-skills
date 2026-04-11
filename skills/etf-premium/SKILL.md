---
name: etf-premium
description: >
  Calculate ETF premium or discount relative to Net Asset Value (NAV) using Yahoo Finance data.
  Use this skill whenever the user asks about an ETF's premium or discount, NAV comparison,
  whether an ETF is trading above or below its fair value, or wants to compare market price vs NAV.
  Triggers: "ETF premium", "ETF discount", "NAV premium", "is SPY trading at a premium",
  "AGG premium to NAV", "market price vs NAV", "ETF mispricing", "BITO premium",
  "IBIT premium", "bond ETF discount", "trading above/below NAV", "ETF premium screener",
  "which ETFs have biggest discount", "compare ETF NAV", "ETF arbitrage",
  or any request involving the gap between an ETF's market price and its underlying value.
  Also triggers when analyzing leveraged, inverse, international, bond, commodity,
  or crypto ETFs where premium/discount is a known concern.
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

```python
def get_peer_premiums(target_ticker, target_category):
    """Fetch premium/discount for peers in the same category."""
    peers = CATEGORY_PEERS.get(target_category, [])
    # Remove the target itself from peers
    peers = [p for p in peers if p.upper() != target_ticker.upper()]
    if not peers:
        return []

    peer_data = []
    for sym in peers:
        try:
            t = yf.Ticker(sym)
            info = t.info
            p = info.get("regularMarketPrice") or info.get("previousClose")
            n = info.get("navPrice")
            if p and n and n > 0:
                prem = (p - n) / n * 100
                peer_data.append({
                    "ticker": sym,
                    "name": info.get("shortName", ""),
                    "price": round(p, 2),
                    "nav": round(n, 2),
                    "premium_pct": round(prem, 4),
                    "expense_ratio": info.get("netExpenseRatio"),
                })
        except Exception:
            pass
    return peer_data
```

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

Use this default universe organized by category. The user can supply their own list instead.

```python
DEFAULT_ETF_UNIVERSE = {
    "US Equity": ["SPY", "QQQ", "IVV", "VOO", "VTI", "DIA", "IWM", "ARKK"],
    "Bond": ["AGG", "BND", "TLT", "HYG", "LQD", "VCIT", "VCSH", "BNDX", "EMB", "JNK", "MUB", "TIP"],
    "International": ["EFA", "EEM", "VWO", "IEMG", "KWEB", "FXI", "INDA", "VEA", "EWZ", "EWJ"],
    "Commodity": ["GLD", "SLV", "USO", "UNG", "DBC", "IAU", "PDBC", "GSG"],
    "Crypto": ["IBIT", "BITO", "FBTC", "ETHA", "ARKB", "GBTC"],
    "Leveraged/Inverse": ["TQQQ", "SQQQ", "SPXU", "UPRO", "JNUG", "JDST", "SOXL", "SOXS"],
    "Sector": ["XLF", "XLE", "XLK", "XLV", "XLI", "XLP", "XLU", "XLRE", "XLC", "XLB", "XLY"],
    "Sector - Semis/Tech": ["SOXX", "SMH", "IGV", "XSD"],
    "Sector - Healthcare": ["XBI", "IBB", "IHI"],
    "Thematic": ["ARKW", "ARKG", "HACK", "CLOU", "WCLD", "BUG", "BOTZ", "LIT", "ICLN", "TAN"],
    "Income": ["JEPI", "JEPQ", "SCHD", "VYM", "DVY", "DIVO", "HDV", "QYLD"],
}

import yfinance as yf
import pandas as pd

def screen_etf_premiums(universe=None, min_abs_premium=0.0):
    if universe is None:
        universe = DEFAULT_ETF_UNIVERSE

    all_tickers = []
    for category, tickers in universe.items():
        for sym in tickers:
            all_tickers.append((sym, category))

    rows = []
    for sym, category_label in all_tickers:
        try:
            t = yf.Ticker(sym)
            info = t.info
            price = info.get("regularMarketPrice") or info.get("previousClose")
            nav = info.get("navPrice")
            if price and nav and nav > 0:
                prem = (price - nav) / nav * 100
                if abs(prem) >= min_abs_premium:
                    rows.append({
                        "ticker": sym,
                        "name": info.get("shortName", ""),
                        "category": category_label,
                        "price": round(price, 2),
                        "nav": round(nav, 2),
                        "premium_pct": round(prem, 4),
                        "total_assets_B": round(info.get("totalAssets", 0) / 1e9, 2),
                        "expense_ratio": info.get("netExpenseRatio"),
                    })
        except Exception:
            pass

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("premium_pct", ascending=True)
    return df
```

### C2: Present the results

Show a ranked table sorted by premium (most discounted first). Group by category if the list is long. Call out:
- **Top 5 deepest discounts** — potential buying opportunities (or signs of stress)
- **Top 5 highest premiums** — overpaying risk
- **Category patterns** — are all bond ETFs at a discount? Are all crypto ETFs at a premium?

Note: this screener takes time because it fetches data one ticker at a time. For large universes (60+ ETFs), warn the user it may take 1-2 minutes.

---

## Sub-Skill D: Premium Deep Dive

**Goal**: Combine premium/discount data with additional context to help the user understand *why* the premium exists and whether it's likely to persist.

### D1: Gather comprehensive data

Run the Sub-Skill A snapshot, then add:

```python
import yfinance as yf
import numpy as np

def premium_deep_dive(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    price = info.get("regularMarketPrice") or info.get("previousClose")
    nav = info.get("navPrice")
    if not price or not nav or nav <= 0:
        return {"error": "NAV data not available"}

    premium_pct = (price - nav) / nav * 100

    # Historical price data for volatility context
    hist = ticker.history(period="3mo")
    if not hist.empty:
        returns = hist["Close"].pct_change().dropna()
        daily_vol = returns.std()
        annualized_vol = daily_vol * np.sqrt(252)
        avg_volume = hist["Volume"].mean()
        dollar_volume = (hist["Close"] * hist["Volume"]).mean()

        # Price range context
        high_3m = hist["Close"].max()
        low_3m = hist["Close"].min()
        pct_from_high = (price - high_3m) / high_3m * 100
    else:
        daily_vol = annualized_vol = avg_volume = dollar_volume = None
        high_3m = low_3m = pct_from_high = None

    result = {
        "ticker": ticker_symbol,
        "name": info.get("longName", ""),
        "price": round(price, 4),
        "nav": round(nav, 4),
        "premium_pct": round(premium_pct, 4),
        "category": info.get("category", "N/A"),
        "fund_family": info.get("fundFamily", "N/A"),
        "total_assets": info.get("totalAssets"),
        "expense_ratio": info.get("netExpenseRatio"),
        "yield_pct": info.get("yield"),
        "ytd_return": info.get("ytdReturn"),
        "beta_3y": info.get("beta3Year"),
        "annualized_vol": round(annualized_vol * 100, 2) if annualized_vol else None,
        "avg_daily_dollar_volume": round(dollar_volume, 0) if dollar_volume else None,
        "pct_from_3m_high": round(pct_from_high, 2) if pct_from_high else None,
    }

    # Bid-ask spread
    bid = info.get("bid")
    ask = info.get("ask")
    if bid and ask and bid > 0:
        spread_pct = (ask - bid) / ((ask + bid) / 2) * 100
        result["bid_ask_spread_pct"] = round(spread_pct, 4)
        result["premium_exceeds_spread"] = abs(premium_pct) > spread_pct

    return result
```

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

Read the reference file for deeper technical detail on ETF premium/discount mechanics and historical context.
