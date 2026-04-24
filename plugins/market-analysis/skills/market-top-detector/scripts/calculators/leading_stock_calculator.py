#!/usr/bin/env python3
"""
Component 2: Leading Stock Health (Weight: 20%)

Evaluates health of leading/growth ETFs as proxy for market leadership.
Uses ETF baskets instead of individual stocks for API efficiency.

Default ETF Basket: ARKK, WCLD, IGV, XBI, SOXX, SMH, KWEB, TAN
Dynamic mode: Selects top-N ETFs from a 20-ETF candidate pool by 52-week high proximity.

Evaluation per ETF:
- Distance from 52-week high
- Position vs 50DMA and 200DMA
- Lower highs pattern detection

Scoring: Weighted average of ETF deterioration signals.
If 60%+ ETFs are deteriorating, apply 1.3x amplification.
"""

from typing import Optional

# Default Leading/Growth ETF basket
DEFAULT_LEADING_ETFS = ["ARKK", "WCLD", "IGV", "XBI", "SOXX", "SMH", "KWEB", "TAN"]
LEADING_ETFS = DEFAULT_LEADING_ETFS  # backward compat

# Expanded candidate pool for dynamic basket selection
CANDIDATE_POOL = [
    "SMH",
    "SOXX",
    "PSI",
    "SOXQ",  # Semiconductors
    "IGV",
    "WCLD",
    "CLOU",
    "BUG",  # Software / Cloud / Cyber
    "XBI",
    "ARKG",  # Biotech / Genomics
    "ARKK",
    "ARKW",
    "KOMP",  # Innovation / Disruptive
    "TAN",
    "ICLN",  # Clean Energy
    "KWEB",
    "FDN",  # Internet / China Tech
    "FINX",
    "IPAY",  # Fintech / Payments
    "BOTZ",  # Robotics / AI
]


def select_dynamic_basket(quotes: dict[str, dict], top_n: int = 10) -> list[str]:
    """
    Select top-N ETFs from candidate pool by proximity to 52-week high.

    Args:
        quotes: Dict of symbol -> quote data with 'price' and 'yearHigh'
        top_n: Number of ETFs to select (default 10)

    Returns:
        List of selected symbols, sorted by proximity to high (closest first).
        Falls back to DEFAULT_LEADING_ETFS if fewer than 5 valid candidates.
    """
    scored = []
    for symbol in CANDIDATE_POOL:
        q = quotes.get(symbol)
        if not q:
            continue
        price = q.get("price", 0)
        year_high = q.get("yearHigh", 0)
        if year_high <= 0 or price <= 0:
            continue
        proximity = price / year_high  # 1.0 = at high, 0.5 = 50% below
        scored.append((symbol, proximity))

    if len(scored) < 5:
        return list(DEFAULT_LEADING_ETFS)

    # Sort by proximity descending (closest to high = strongest leader)
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in scored[:top_n]]


def calculate_leading_stock_health(
    quotes: dict[str, dict], historical: dict[str, list[dict]], etf_list: Optional[list[str]] = None
) -> dict:
    """
    Calculate leading stock health score.

    Args:
        quotes: Dict of symbol -> quote data (from FMP batch quote)
        historical: Dict of symbol -> list of daily OHLCV (most recent first, ~60 days)
        etf_list: Optional explicit list of ETF symbols to evaluate.
                  If None, uses quotes.keys() or DEFAULT_LEADING_ETFS.

    Returns:
        Dict with score (0-100), etf_details, signal, basket_mode, basket
    """
    etf_scores = []
    etf_details = {}
    if etf_list is not None:
        basket_mode = "dynamic" if etf_list != list(DEFAULT_LEADING_ETFS) else "static"
        eval_list = list(etf_list)
    elif quotes:
        basket_mode = "static"
        eval_list = list(quotes.keys())
    else:
        basket_mode = "static"
        eval_list = list(DEFAULT_LEADING_ETFS)
    total_attempted = len(eval_list)
    fetch_successes = 0
    partial_data_count = 0

    # Minimum history bars for full analysis (50DMA calculation)
    MIN_HISTORY_BARS = 50

    for symbol in eval_list:
        quote = quotes.get(symbol)
        hist = historical.get(symbol, [])

        if not quote:
            continue

        # Full success requires quote + sufficient history
        if len(hist) >= MIN_HISTORY_BARS:
            fetch_successes += 1
        else:
            partial_data_count += 1

        detail = _evaluate_etf(symbol, quote, hist)
        etf_scores.append(detail["deterioration_score"])
        etf_details[symbol] = detail

    fetch_success_rate = fetch_successes / total_attempted if total_attempted > 0 else 0.0

    if not etf_scores:
        return {
            "score": 50,
            "signal": "INSUFFICIENT DATA",
            "etf_details": {},
            "etfs_evaluated": 0,
            "etfs_deteriorating": 0,
            "data_available": False,
            "fetch_success_rate": fetch_success_rate,
            "partial_data_count": partial_data_count,
            "basket_mode": basket_mode,
            "basket": eval_list,
        }

    # Mark data as unavailable if fetch success rate is below 75%
    data_available = fetch_success_rate >= 0.75

    avg_deterioration = sum(etf_scores) / len(etf_scores)

    # Count deteriorating ETFs (score >= 50)
    deteriorating_count = sum(1 for s in etf_scores if s >= 50)
    deteriorating_pct = deteriorating_count / len(etf_scores)

    # Amplification: if 60%+ ETFs deteriorating, multiply by 1.3
    if deteriorating_pct >= 0.60:
        final_score = min(100, avg_deterioration * 1.3)
    else:
        final_score = avg_deterioration

    final_score = round(min(100, max(0, final_score)))

    # Signal
    if final_score >= 70:
        signal = "CRITICAL: Leadership broadly deteriorating"
    elif final_score >= 50:
        signal = "WARNING: Multiple leaders weakening"
    elif final_score >= 30:
        signal = "CAUTION: Some leaders showing strain"
    else:
        signal = "HEALTHY: Leadership intact"

    return {
        "score": final_score,
        "signal": signal,
        "avg_deterioration": round(avg_deterioration, 1),
        "etfs_evaluated": len(etf_scores),
        "etfs_deteriorating": deteriorating_count,
        "deteriorating_pct": round(deteriorating_pct * 100, 1),
        "amplified": deteriorating_pct >= 0.60,
        "etf_details": etf_details,
        "data_available": data_available,
        "fetch_success_rate": round(fetch_success_rate, 2),
        "partial_data_count": partial_data_count,
        "basket_mode": basket_mode,
        "basket": eval_list,
    }


def _evaluate_etf(symbol: str, quote: dict, history: list[dict]) -> dict:
    """Evaluate a single ETF's deterioration level"""
    score = 0
    flags = []

    price = quote.get("price", 0)
    year_high = quote.get("yearHigh", 0)
    quote.get("yearLow", 0)

    # 1. Distance from 52-week high (0-40 points)
    if year_high > 0:
        distance_pct = (price - year_high) / year_high * 100
        if distance_pct <= -25:
            score += 40
            flags.append(f">{abs(distance_pct):.0f}% below 52wk high (bear territory)")
        elif distance_pct <= -15:
            score += 30
            flags.append(f"{abs(distance_pct):.0f}% below 52wk high (correction)")
        elif distance_pct <= -10:
            score += 20
            flags.append(f"{abs(distance_pct):.0f}% below 52wk high")
        elif distance_pct <= -5:
            score += 10
            flags.append(f"{abs(distance_pct):.0f}% below 52wk high")
    else:
        distance_pct = 0

    # 2. Position vs moving averages (0-40 points)
    if history and len(history) >= 50:
        closes = [d.get("close", d.get("adjClose", 0)) for d in history]

        # 50DMA
        sma50 = sum(closes[:50]) / 50
        if price < sma50:
            score += 20
            flags.append(f"Below 50DMA (${sma50:.2f})")

        # 200DMA (if enough data)
        if len(closes) >= 200:
            sma200 = sum(closes[:200]) / 200
            if price < sma200:
                score += 20
                flags.append(f"Below 200DMA (${sma200:.2f})")
        elif len(closes) >= 50:
            # Estimate 200DMA position from available data
            if price < sma50 * 0.95:  # >5% below 50DMA suggests below 200DMA
                score += 10
                flags.append("Likely below 200DMA (estimated)")

    elif history and len(history) >= 20:
        closes = [d.get("close", d.get("adjClose", 0)) for d in history]
        sma20 = sum(closes[:20]) / 20
        if price < sma20:
            score += 15
            flags.append(f"Below 20DMA (${sma20:.2f})")

    # 3. Lower highs pattern (0-20 points)
    if history and len(history) >= 20:
        lower_highs = _detect_lower_highs(history)
        if lower_highs:
            score += 20
            flags.append("Lower highs pattern detected")

    score = min(100, score)

    return {
        "deterioration_score": score,
        "price": price,
        "year_high": year_high,
        "distance_from_high_pct": round(distance_pct, 1),
        "flags": flags,
    }


def _detect_lower_highs(history: list[dict], lookback: int = 20) -> bool:
    """
    Detect lower highs pattern in recent price action.

    Look for at least 2 consecutive lower swing highs in the last 20 days.
    """
    if len(history) < lookback:
        return False

    highs = [d.get("high", d.get("close", 0)) for d in history[:lookback]]

    # Find local maxima (swing highs)
    swing_highs = []
    for i in range(1, len(highs) - 1):
        if highs[i] > highs[i - 1] and highs[i] > highs[i + 1]:
            swing_highs.append(highs[i])

    # Need at least 2 swing highs to compare
    if len(swing_highs) < 2:
        return False

    # Check if most recent swing highs are declining
    # swing_highs[0] is earliest (since history is most-recent-first, reversed)
    # Actually history[0] = most recent, so highs[0] = most recent high
    # So swing_highs are in reverse chronological order
    return swing_highs[0] < swing_highs[1]
