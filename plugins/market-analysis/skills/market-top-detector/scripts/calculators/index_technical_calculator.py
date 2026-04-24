#!/usr/bin/env python3
"""
Component 5: Index Technical Condition (Weight: 15%)

Evaluates technical health of S&P 500 and NASDAQ.
Uses shared historical data from Component 1 (no additional API calls).

Checkpoints (per index, S&P 500 + NASDAQ):
1. Price < 21 EMA (short-term weakness)        -> +8pt
2. Price < 50 EMA (medium-term breakdown)       -> +12pt
3. 21 EMA < 50 EMA (MA bearish crossover)       -> +10pt
4. Price < 200 SMA (long-term trend breakdown)   -> +15pt
5. Failed rally pattern                          -> +10pt
6. Lower highs pattern                           -> +10pt
7. Gap down on volume                            -> +10pt

Max per index: ~75 points (not all conditions fire at once in early stages)
Final: average of both indices, scaled to 0-100
"""

from typing import Optional

from calculators.math_utils import calc_ema


def calculate_index_technical(
    sp500_history: list[dict],
    nasdaq_history: list[dict],
    sp500_quote: Optional[dict] = None,
    nasdaq_quote: Optional[dict] = None,
) -> dict:
    """
    Calculate index technical condition score.

    Args:
        sp500_history: S&P 500 daily OHLCV (most recent first, 250+ days preferred)
        nasdaq_history: NASDAQ daily OHLCV (most recent first, 250+ days preferred)
        sp500_quote: Current S&P 500 quote (optional, for real-time price)
        nasdaq_quote: Current NASDAQ/QQQ quote (optional)

    Returns:
        Dict with score (0-100), sp500_details, nasdaq_details, signal
    """
    sp500_result = _evaluate_index("S&P 500", sp500_history, sp500_quote)
    nasdaq_result = _evaluate_index("NASDAQ", nasdaq_history, nasdaq_quote)

    # Average only indices with available data
    scores = []
    if sp500_result.get("data_available", False):
        scores.append(sp500_result["raw_score"])
    if nasdaq_result.get("data_available", False):
        scores.append(nasdaq_result["raw_score"])

    if not scores:
        final_score = 50  # Neutral when no data
        signal = "NO DATA: Index data unavailable"
        return {
            "score": final_score,
            "signal": signal,
            "sp500": sp500_result,
            "nasdaq": nasdaq_result,
            "data_available": False,
        }

    avg_score = sum(scores) / len(scores)
    final_score = round(min(100, max(0, avg_score)))

    if final_score >= 70:
        signal = "CRITICAL: Major technical breakdown"
    elif final_score >= 50:
        signal = "WARNING: Significant technical deterioration"
    elif final_score >= 35:
        signal = "CAUTION: Short-term weakness detected"
    elif final_score >= 15:
        signal = "MIXED: Minor technical concerns"
    else:
        signal = "HEALTHY: Technical structure intact"

    return {
        "score": final_score,
        "signal": signal,
        "sp500": sp500_result,
        "nasdaq": nasdaq_result,
        "data_available": True,
    }


def _evaluate_index(name: str, history: list[dict], quote: Optional[dict] = None) -> dict:
    """Evaluate a single index's technical condition"""
    if not history or len(history) < 21:
        return {"raw_score": 0, "flags": ["Insufficient data"], "mas": {}, "data_available": False}

    closes = [d.get("close", d.get("adjClose", 0)) for d in history]
    highs = [d.get("high", d.get("close", 0)) for d in history]
    [d.get("low", d.get("close", 0)) for d in history]
    volumes = [d.get("volume", 0) for d in history]

    # Current price (from quote or most recent close)
    if quote:
        price = quote.get("price", closes[0])
    else:
        price = closes[0]

    score = 0
    flags = []
    mas = {}

    # Calculate moving averages
    ema21 = calc_ema(closes, 21)
    mas["ema21"] = round(ema21, 2)

    if len(closes) >= 50:
        ema50 = calc_ema(closes, 50)
        mas["ema50"] = round(ema50, 2)
    else:
        ema50 = None

    if len(closes) >= 200:
        sma200 = sum(closes[:200]) / 200
        mas["sma200"] = round(sma200, 2)
    else:
        sma200 = None

    # Check 1: Price < 21 EMA (short-term weakness)
    if price < ema21:
        score += 8
        pct_below = (price - ema21) / ema21 * 100
        flags.append(f"Below 21 EMA ({pct_below:+.1f}%)")

    # Check 2: Price < 50 EMA (medium-term breakdown)
    if ema50 and price < ema50:
        score += 12
        pct_below = (price - ema50) / ema50 * 100
        flags.append(f"Below 50 EMA ({pct_below:+.1f}%)")

    # Check 3: 21 EMA < 50 EMA (bearish crossover)
    if ema50 and ema21 < ema50:
        score += 10
        flags.append("21 EMA < 50 EMA (bearish crossover)")

    # Check 4: Price < 200 SMA (long-term trend breakdown)
    if sma200 and price < sma200:
        score += 15
        pct_below = (price - sma200) / sma200 * 100
        flags.append(f"Below 200 SMA ({pct_below:+.1f}%)")

    # Check 5: Failed rally pattern
    if _detect_failed_rally(closes, volumes):
        score += 10
        flags.append("Failed rally pattern detected")

    # Check 6: Lower highs pattern (20 day)
    if _detect_lower_highs(highs, lookback=20):
        score += 10
        flags.append("Lower highs pattern (20 day)")

    # Check 7: Gap down on volume
    if _detect_gap_down(history):
        score += 10
        flags.append("Recent gap down on volume")

    return {
        "raw_score": min(100, score),
        "price": round(price, 2),
        "flags": flags,
        "mas": mas,
        "data_available": True,
    }


def _detect_failed_rally(closes: list[float], volumes: list[int], lookback: int = 15) -> bool:
    """
    Detect failed rally: price bounces then fails to make new high
    within recent lookback period.
    """
    if len(closes) < lookback:
        return False

    recent = closes[:lookback]
    # Find the peak in recent data
    peak_idx = recent.index(max(recent))

    # Failed rally: peak occurred 3-10 days ago, current price is below that peak
    if 3 <= peak_idx <= 10:
        # Price fell from peak
        drop = (recent[0] - recent[peak_idx]) / recent[peak_idx] * 100
        if drop < -2.0:  # Dropped >2% from recent peak
            return True
    return False


def _detect_lower_highs(highs: list[float], lookback: int = 20) -> bool:
    """Detect lower highs pattern in price action"""
    if len(highs) < lookback:
        return False

    recent_highs = highs[:lookback]

    # Find swing highs (local maxima)
    swing_highs = []
    for i in range(1, len(recent_highs) - 1):
        if recent_highs[i] > recent_highs[i - 1] and recent_highs[i] > recent_highs[i + 1]:
            swing_highs.append(recent_highs[i])

    if len(swing_highs) < 2:
        return False

    # Most recent swing high lower than previous
    return swing_highs[0] < swing_highs[1]


def _detect_gap_down(history: list[dict], lookback: int = 5) -> bool:
    """Detect gap down on increased volume in recent sessions"""
    if len(history) < lookback + 1:
        return False

    for i in range(lookback):
        today = history[i]
        yesterday = history[i + 1]

        today_open = today.get("open", 0)
        yesterday_close = yesterday.get("close", yesterday.get("adjClose", 0))
        today_volume = today.get("volume", 0)
        yesterday_volume = yesterday.get("volume", 0)

        if yesterday_close == 0 or yesterday_volume == 0:
            continue

        gap_pct = (today_open - yesterday_close) / yesterday_close * 100
        volume_increase = today_volume > yesterday_volume * 1.1

        # Gap down >= 0.5% on higher volume
        if gap_pct <= -0.5 and volume_increase:
            return True

    return False
