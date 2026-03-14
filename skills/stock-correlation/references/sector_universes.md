# Dynamic Peer Universe Construction

How to build a peer universe at runtime for correlation analysis. **Do not hardcode ticker lists** — fetch them dynamically so results stay current.

---

## Method 1: Same-Industry Screen (Primary)

Use yfinance's `Screener` + `EquityQuery` to find stocks in the same sector and industry as the target:

```python
import yfinance as yf
from yfinance import Screener, EquityQuery

def get_industry_peers(ticker_symbol, min_market_cap=1_000_000_000, max_results=30):
    """Find peers in the same industry with similar market cap."""
    target = yf.Ticker(ticker_symbol)
    info = target.info
    sector = info.get("sector", "")
    industry = info.get("industry", "")
    market_cap = info.get("marketCap", 0)

    if not industry:
        return []

    # Screen for same-industry stocks above minimum market cap
    query = EquityQuery("and", [
        EquityQuery("eq", ["industry", industry]),
        EquityQuery("gt", ["marketcap", min_market_cap]),
    ])

    screener = Screener()
    screener.set_body(query, size=max_results)
    result = screener.response

    peers = []
    for quote in result.get("quotes", []):
        symbol = quote.get("symbol", "")
        if symbol and symbol != ticker_symbol:
            peers.append(symbol)

    return peers
```

## Method 2: Same-Sector Screen (Broader)

When the industry is too narrow (< 5 peers), widen to the full sector:

```python
def get_sector_peers(ticker_symbol, min_market_cap=5_000_000_000, max_results=30):
    """Find large-cap peers in the same sector."""
    target = yf.Ticker(ticker_symbol)
    info = target.info
    sector = info.get("sector", "")

    if not sector:
        return []

    query = EquityQuery("and", [
        EquityQuery("eq", ["sector", sector]),
        EquityQuery("gt", ["marketcap", min_market_cap]),
    ])

    screener = Screener()
    screener.set_body(query, size=max_results)
    result = screener.response

    peers = []
    for quote in result.get("quotes", []):
        symbol = quote.get("symbol", "")
        if symbol and symbol != ticker_symbol:
            peers.append(symbol)

    return peers
```

## Method 3: Thematic Expansion

For cross-sector correlations (e.g., AI supply chain spans semis + cloud + software), use the target's known business relationships:

```python
def get_thematic_peers(ticker_symbol):
    """Use company description and sector to infer thematic peers."""
    target = yf.Ticker(ticker_symbol)
    info = target.info
    description = info.get("longBusinessSummary", "")
    sector = info.get("sector", "")
    industry = info.get("industry", "")

    # Return the description and sector info so the model can reason about
    # which adjacent industries to also screen
    return {
        "sector": sector,
        "industry": industry,
        "description": description,
    }
```

After reading the company description, screen 1-2 adjacent industries. For example:
- A semiconductor company → also screen "Semiconductor Equipment" and "Electronic Components"
- A cloud platform → also screen "Software - Infrastructure" and "Information Technology Services"
- An EV maker → also screen "Auto Parts", "Electrical Equipment", and "Specialty Chemicals" (battery materials)

## Combining Methods

Build the full universe by combining all methods:

```python
def build_peer_universe(ticker_symbol):
    """Build a comprehensive peer universe for correlation analysis."""
    peers = set()

    # 1. Same industry (narrow)
    industry_peers = get_industry_peers(ticker_symbol, min_market_cap=1_000_000_000)
    peers.update(industry_peers)

    # 2. If too few, broaden to sector
    if len(peers) < 10:
        sector_peers = get_sector_peers(ticker_symbol, min_market_cap=5_000_000_000)
        peers.update(sector_peers)

    # 3. Add thematic/adjacent industries based on business description
    # (model should reason about which adjacent industries to screen)

    peers.discard(ticker_symbol)
    return list(peers)
```

**Target**: 15-30 peers for a meaningful correlation scan. Too few gives sparse results; too many slows the yfinance download.

---

## Fallback: Well-Known Groupings

If the screener is unavailable or rate-limited, ask the model to use its knowledge of well-known groupings:

- **Mag 7**: AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA
- **Major indices**: SPY (S&P 500), QQQ (Nasdaq 100), DIA (Dow 30), IWM (Russell 2000)
- **Sector ETFs**: XLK, XLF, XLE, XLV, XLI, XLP, XLU, XLY, XLC, XLRE, XLB

These ETFs are useful as correlation benchmarks — comparing a stock's correlation to sector ETFs quickly reveals its primary driver.
