# Dynamic Peer Universe Construction

How to build a peer universe at runtime for correlation analysis. **Do not hardcode ticker lists** — fetch them dynamically so results stay current.

---

## Method 1: Same-Sector Screen (Primary)

Use yfinance's `yf.screen()` + `EquityQuery` to find stocks in the same sector as the target. Note: the screener supports filtering by `sector` but not directly by `industry` — use sector-level screening and let the correlation math surface the closest peers.

```python
import yfinance as yf
from yfinance import EquityQuery

def get_sector_peers(ticker_symbol, min_market_cap=1_000_000_000, max_results=30):
    """Find peers in the same sector above a market cap threshold."""
    target = yf.Ticker(ticker_symbol)
    info = target.info
    sector = info.get("sector", "")

    if not sector:
        return []

    # Screen for same-sector stocks on major US exchanges
    query = EquityQuery("and", [
        EquityQuery("eq", ["sector", sector]),
        EquityQuery("gt", ["intradaymarketcap", min_market_cap]),
        EquityQuery("is-in", ["exchange", "NMS", "NYQ"]),
    ])

    result = yf.screen(query, size=max_results, sortField="intradaymarketcap", sortAsc=False)

    peers = []
    for quote in result.get("quotes", []):
        symbol = quote.get("symbol", "")
        if symbol and symbol != ticker_symbol:
            peers.append(symbol)

    return peers
```

## Method 2: Thematic Expansion

For cross-sector correlations (e.g., AI supply chain spans semis + cloud + software), read the target's business description and screen adjacent sectors:

```python
def get_thematic_context(ticker_symbol):
    """Get company context to inform adjacent-sector screening."""
    target = yf.Ticker(ticker_symbol)
    info = target.info
    return {
        "sector": info.get("sector", ""),
        "industry": info.get("industry", ""),
        "description": info.get("longBusinessSummary", ""),
    }
```

After reading the company description, screen 1-2 adjacent sectors. For example:
- A semiconductor company (Technology sector) → also consider screening for related names in "Industrials" (equipment suppliers)
- A cloud platform → also screen for networking/data-center REITs
- An EV maker (Consumer Cyclical) → also screen "Basic Materials" (battery materials), "Industrials" (auto parts)

## Combining Methods

Build the full universe by combining sector screen + thematic expansion:

```python
def build_peer_universe(ticker_symbol):
    """Build a comprehensive peer universe for correlation analysis."""
    peers = set()

    # 1. Same sector
    sector_peers = get_sector_peers(ticker_symbol, min_market_cap=1_000_000_000, max_results=25)
    peers.update(sector_peers)

    # 2. If too few, lower the market cap threshold
    if len(peers) < 10:
        more_peers = get_sector_peers(ticker_symbol, min_market_cap=500_000_000, max_results=30)
        peers.update(more_peers)

    # 3. Add thematic/adjacent sectors based on business description
    # (model should reason about which adjacent sectors to screen)

    peers.discard(ticker_symbol)
    return list(peers)
```

**Target**: 15-30 peers for a meaningful correlation scan. Too few gives sparse results; too many slows the yfinance download.

---

## Fallback: Well-Known Groupings

If the screener is unavailable or rate-limited, use well-known benchmarks:

- **Mag 7**: AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA
- **Major indices**: SPY (S&P 500), QQQ (Nasdaq 100), DIA (Dow 30), IWM (Russell 2000)
- **Sector ETFs**: XLK, XLF, XLE, XLV, XLI, XLP, XLU, XLY, XLC, XLRE, XLB

These ETFs are useful as correlation benchmarks — comparing a stock's correlation to sector ETFs quickly reveals its primary driver.
