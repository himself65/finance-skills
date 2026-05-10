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

## Sub-Skill E: Premium Surge Decomposition (Gamma Squeeze Analysis)

**Goal**: When an ETF has just experienced a dramatic intraday move that diverges from its underlying holdings, decompose the move into (1) a fundamental NAV-driven component and (2) an "excess premium" driven by structural forces — most commonly options dealer gamma hedging, AP arbitrage breakdowns, or sentiment surges. Then assess how long the premium will likely take to converge.

This sub-skill is appropriate when the user reports or asks about:
- An ETF moving 5%+ in a single session
- A divergence between the ETF and its named underlyings (e.g., "MSTR jumped 13% but BTC only rose 3%")
- A suspected gamma squeeze in an ETF or single name
- Whether dealer hedging is amplifying a move

Read `references/gamma_squeeze_reference.md` for the full GEX formula derivation, dealer-positioning conventions, and worked examples before running E2.

### E1: Decompose today's move into NAV-driven vs excess premium

The static `navPrice` field gives only the most recent end-of-day NAV — it cannot tell you how much of *today's* move is NAV-driven. Estimate the NAV return from the holdings' returns instead:

```python
import yfinance as yf
import pandas as pd
import numpy as np

def decompose_etf_move(ticker_symbol, holdings_weights=None, window="2d"):
    """
    Decompose the ETF's most recent daily move into NAV-driven vs excess premium.

    holdings_weights: dict like {"MU": 0.20, "005930.KS": 0.22, "000660.KS": 0.27, ...}
                      If None, attempts to fetch via yfinance's funds_data;
                      falls back to user-supplied weights for ETFs where it isn't available.
    """
    etf = yf.Ticker(ticker_symbol)
    info = etf.info

    # ETF return over the most recent session
    etf_hist = etf.history(period=window, auto_adjust=False)
    if len(etf_hist) < 2:
        return {"error": "Not enough history"}
    etf_close_today = etf_hist["Close"].iloc[-1]
    etf_close_prev = etf_hist["Close"].iloc[-2]
    etf_return_pct = (etf_close_today / etf_close_prev - 1) * 100

    # Try to auto-fetch holdings if not supplied
    if holdings_weights is None:
        try:
            top_holdings = etf.funds_data.top_holdings  # DataFrame
            holdings_weights = dict(zip(top_holdings.index, top_holdings["Holding Percent"]))
        except Exception:
            holdings_weights = {}

    if not holdings_weights:
        return {
            "error": "Holdings weights unavailable — supply manually via holdings_weights={'TICKER': weight, ...}",
            "etf_return_pct": round(etf_return_pct, 4),
        }

    # Weighted return of underlying holdings (proxy for NAV move)
    weighted_return = 0.0
    coverage = 0.0
    holding_returns = {}
    for sym, w in holdings_weights.items():
        try:
            h = yf.Ticker(sym).history(period=window, auto_adjust=False)
            if len(h) >= 2:
                r = (h["Close"].iloc[-1] / h["Close"].iloc[-2] - 1) * 100
                holding_returns[sym] = round(r, 4)
                weighted_return += w * r
                coverage += w
        except Exception:
            pass

    # Normalize to coverage so partial holdings still give a sensible NAV proxy
    nav_return_proxy = weighted_return / coverage if coverage > 0 else None
    excess_premium_pct = (
        etf_return_pct - nav_return_proxy if nav_return_proxy is not None else None
    )

    return {
        "ticker": ticker_symbol,
        "etf_return_pct": round(etf_return_pct, 4),
        "nav_return_proxy_pct": round(nav_return_proxy, 4) if nav_return_proxy else None,
        "excess_premium_pct": round(excess_premium_pct, 4) if excess_premium_pct else None,
        "holdings_coverage_pct": round(coverage * 100, 2),
        "holding_returns": holding_returns,
        "interpretation": (
            "Most of the move is NAV-driven — limited structural component"
            if excess_premium_pct is not None and abs(excess_premium_pct) < 1
            else "Significant excess premium — investigate dealer hedging, AP bottlenecks, or sentiment"
            if excess_premium_pct is not None
            else "Cannot conclude without holdings data"
        ),
    }
```

**Caveat**: For international ETFs whose underlyings trade in a closed session (e.g., Asian holdings during US hours), the holdings' US-listed proxies (ADRs) or futures must be used. If neither is available, flag this to the user — the NAV proxy will be stale.

### E2: Compute dealer gamma exposure (GEX) from the options chain

GEX quantifies how much hedging buying/selling dealers must do per 1% move in the underlying. Large positive GEX accumulating on the call side during a rally indicates a gamma squeeze in progress.

```python
import numpy as np
from datetime import datetime, timezone
from math import log, sqrt, exp, pi

def _norm_pdf(x):
    return exp(-0.5 * x * x) / sqrt(2 * pi)

def _bsm_gamma(S, K, T, r, sigma):
    """Black-Scholes gamma. Returns 0 for degenerate inputs."""
    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return 0.0
    d1 = (log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T))
    return _norm_pdf(d1) / (S * sigma * sqrt(T))

def compute_gex(ticker_symbol, risk_free_rate=0.045, max_expirations=8):
    """
    Compute gross and net dealer gamma exposure.

    Conventions:
      - Per contract, dollar gamma per 1% move = OI * 100 * gamma * spot * (spot * 0.01)
                                                = OI * gamma * spot^2  (with multiplier=100)
      - SqueezeMetrics convention (assumes dealers SHORT calls, LONG puts):
            net_gex = call_gamma_$ - put_gamma_$
        Positive net_gex = stabilizing (dealers sell rallies, buy dips)
        Negative net_gex = destabilizing (dealers buy rallies, sell dips → squeeze)
      - "Customer-net-long-everything" convention (dealers SHORT both):
            gross_hedge = call_gamma_$ + put_gamma_$
        This is the maximum hedging pressure assumption.
    """
    t = yf.Ticker(ticker_symbol)
    info = t.info
    spot = info.get("regularMarketPrice") or info.get("previousClose")
    if not spot:
        return {"error": "No spot price"}

    expirations = t.options[:max_expirations]
    if not expirations:
        return {"error": "No options chain available"}

    now = datetime.now(timezone.utc)
    rows = []
    for exp_str in expirations:
        try:
            chain = t.option_chain(exp_str)
        except Exception:
            continue
        exp_date = datetime.strptime(exp_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        T = max((exp_date - now).total_seconds() / (365.25 * 86400), 1e-6)

        for side, df in [("call", chain.calls), ("put", chain.puts)]:
            for _, row in df.iterrows():
                K = row.get("strike")
                iv = row.get("impliedVolatility")
                oi = row.get("openInterest", 0) or 0
                if not K or not iv or oi <= 0:
                    continue
                gamma = _bsm_gamma(spot, K, T, risk_free_rate, iv)
                # Dollar value per 1% spot move:
                gamma_dollars_per_1pct = oi * gamma * spot * spot
                rows.append({
                    "expiration": exp_str,
                    "side": side,
                    "strike": K,
                    "iv": iv,
                    "oi": oi,
                    "gamma": gamma,
                    "gamma_$_per_1pct": gamma_dollars_per_1pct,
                })

    if not rows:
        return {"error": "No usable contracts"}

    df = pd.DataFrame(rows)
    call_gex = df[df["side"] == "call"]["gamma_$_per_1pct"].sum()
    put_gex = df[df["side"] == "put"]["gamma_$_per_1pct"].sum()

    # Top concentration: which expiration & strike dominate
    top_strikes = (
        df.groupby(["expiration", "strike", "side"])["gamma_$_per_1pct"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    total_call_oi = df[df["side"] == "call"]["oi"].sum()
    total_put_oi = df[df["side"] == "put"]["oi"].sum()
    cp_ratio = total_call_oi / total_put_oi if total_put_oi > 0 else None

    # Pull near-term ATM IV as a single representative number
    df["moneyness"] = abs(df["strike"] / spot - 1)
    near_atm = df.sort_values("moneyness").head(20)
    atm_iv_pct = near_atm["iv"].median() * 100 if len(near_atm) else None

    return {
        "ticker": ticker_symbol,
        "spot": spot,
        "call_gex_per_1pct_$": call_gex,
        "put_gex_per_1pct_$": put_gex,
        "net_gex_squeezemetrics_$": call_gex - put_gex,
        "gross_hedge_pressure_$": call_gex + put_gex,
        "total_call_oi": int(total_call_oi),
        "total_put_oi": int(total_put_oi),
        "call_put_oi_ratio": round(cp_ratio, 2) if cp_ratio else None,
        "atm_iv_pct": round(atm_iv_pct, 2) if atm_iv_pct else None,
        "expirations_analyzed": len(expirations),
        "top_concentrations": top_strikes,
    }
```

Interpret the output:

- **`net_gex_squeezemetrics_$` highly negative** → dealers are short gamma; rallies will be amplified by their hedging buys. Classic gamma-squeeze fuel.
- **Concentration on a single near-dated strike** (e.g., the article's "June $45 calls") → squeeze is fragile and concentrated. When that strike expires or the spot moves past it, the gamma decays sharply.
- **ATM IV well above the recent average** (article example: 78 vs typical ~30–40) → market is pricing in continued large moves; option premium decay alone will provide some convergence pressure over days.
- **Call/Put OI ratio > 2.5** → call-heavy positioning, consistent with a bullish gamma squeeze setup.

### E3: Compare structural buying pressure to actual volume

The article's most concrete claim was that ~35% of the day's buying was dealer-driven. Reproduce this comparison:

```python
def estimate_dealer_share_of_volume(ticker_symbol, gex_per_1pct_dollars, etf_return_pct):
    """
    Implied dealer-driven $ buying = |gex_per_1pct| * |etf_return_pct|
    Compare to actual dollar volume.
    """
    t = yf.Ticker(ticker_symbol)
    hist = t.history(period="2d", auto_adjust=False)
    if hist.empty:
        return None
    today = hist.iloc[-1]
    actual_dollar_volume = today["Close"] * today["Volume"]

    implied_dealer_buying = abs(gex_per_1pct_dollars) * abs(etf_return_pct)
    share = implied_dealer_buying / actual_dollar_volume if actual_dollar_volume > 0 else None

    return {
        "actual_dollar_volume_$": round(actual_dollar_volume, 0),
        "implied_dealer_buying_$": round(implied_dealer_buying, 0),
        "dealer_share_of_volume_pct": round(share * 100, 2) if share else None,
    }
```

This is a rough estimate — it assumes every contract's full gamma was hedged in a single direction during the move. Real hedging is incremental, and not all dealers hedge identically. Treat as an upper-bound heuristic, not a precise figure. Always present it alongside the assumptions.

### E4: Assess premium convergence timeline

The article's three-tier convergence framework:

| Time scale | Mechanism | What to check |
|---|---|---|
| **Hours** | AP creation/redemption arbitrage | Is the underlying market open? Are creation units restricted? Is the spread between bid/ask widening (suggests AP stepping back)? |
| **Days** | Options expiration / gamma decay | When does the dominant strike's expiration land? Is OI rolling forward or being closed? Is IV starting to compress? |
| **Weeks** | Net flow normalization | Is the ETF receiving large daily inflows (signals demand outpacing creation capacity)? Is short interest building (potential additional squeeze fuel)? |

```python
def assess_convergence(ticker_symbol, top_concentrations_df):
    """Returns a dict of qualitative convergence signals."""
    t = yf.Ticker(ticker_symbol)
    info = t.info

    # 1. AP arbitrage: market hours of underlying
    region = info.get("region") or info.get("market") or "unknown"
    underlying_session_note = (
        "International — check whether underlying market overlaps US trading hours; "
        "AP arbitrage may be blocked when underlying market is closed"
        if "us_market" not in (info.get("market") or "").lower()
        else "US-listed underlying — AP arbitrage active during US hours"
    )

    # 2. Options expiration: nearest concentrated strike
    if not top_concentrations_df.empty:
        next_major_exp = top_concentrations_df.iloc[0]["expiration"]
        days_to_exp = (datetime.strptime(next_major_exp, "%Y-%m-%d") - datetime.now()).days
        exp_note = f"Largest gamma concentration expires in {days_to_exp} days ({next_major_exp})"
    else:
        exp_note = "No clear strike concentration"

    # 3. Flow proxy: AUM trajectory (very rough)
    aum = info.get("totalAssets")
    aum_note = f"Total AUM: ${aum/1e9:.2f}B" if aum else "AUM unavailable"

    return {
        "ap_arbitrage": underlying_session_note,
        "options_window": exp_note,
        "flows": aum_note,
    }
```

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
