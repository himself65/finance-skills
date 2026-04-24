#!/usr/bin/env python3
"""
Component 1: Market Breadth (Overall) - Weight: 30%

Evaluates the overall market uptrend ratio level and trend direction.
Primary signal: ratio level mapped to scoring bands with trend adjustment.

Data Source: Timeseries "all" worksheet

Thresholds aligned with Monty's dashboard:
  - Overbought: 37% (upper threshold)
  - Oversold: 9.7% (lower threshold)

Scoring Bands (linear interpolation within each band):
  >= 50%    -> 90-100 (Strong Bull)
  37-50%    -> 70-89  (Bullish / above overbought threshold)
  25-37%    -> 40-69  (Neutral/Recovering)
  9.7-25%   -> 10-39  (Weak / between thresholds)
  < 9.7%    -> 0-9    (Crisis / below oversold threshold)

Trend adjustment: trend="up" & slope>0 -> +5, trend="down" & slope<0 -> -5
"""

from typing import Optional

# Monty's official dashboard thresholds
UPPER_THRESHOLD = 0.37  # Overbought
LOWER_THRESHOLD = 0.097  # Oversold


def calculate_market_breadth(latest_all: Optional[dict], all_timeseries: list[dict]) -> dict:
    """
    Calculate market breadth score from overall uptrend ratio.

    Args:
        latest_all: Most recent "all" timeseries row
        all_timeseries: Full "all" timeseries sorted by date ascending

    Returns:
        Dict with score (0-100), signal, and detail fields
    """
    if not latest_all or latest_all.get("ratio") is None:
        return {
            "score": 50,
            "signal": "NO DATA: Overall uptrend ratio unavailable (neutral default)",
            "data_available": False,
            "ratio": None,
            "ma_10": None,
            "trend": None,
            "slope": None,
            "distance_from_upper": None,
            "distance_from_lower": None,
        }

    ratio = latest_all["ratio"]
    ma_10 = latest_all.get("ma_10")
    trend = latest_all.get("trend", "")
    slope = latest_all.get("slope")

    # Map ratio to base score via linear interpolation
    base_score = _ratio_to_score(ratio)

    # Trend adjustment
    trend_adj = 0
    if trend.lower() == "up" and slope is not None and slope > 0:
        trend_adj = 5
    elif trend.lower() == "down" and slope is not None and slope < 0:
        trend_adj = -5

    score = round(min(100, max(0, base_score + trend_adj)))

    # Signal label
    signal = _score_to_signal(score, ratio, trend)

    # Key distances from Monty's official thresholds
    distance_from_upper = round(ratio - UPPER_THRESHOLD, 4) if ratio is not None else None
    distance_from_lower = round(ratio - LOWER_THRESHOLD, 4) if ratio is not None else None

    return {
        "score": score,
        "signal": signal,
        "data_available": True,
        "ratio": ratio,
        "ratio_pct": round(ratio * 100, 1) if ratio is not None else None,
        "ma_10": ma_10,
        "ma_10_pct": round(ma_10 * 100, 1) if ma_10 is not None else None,
        "trend": trend,
        "slope": slope,
        "trend_adjustment": trend_adj,
        "distance_from_upper": distance_from_upper,
        "distance_from_lower": distance_from_lower,
        "upper_threshold": UPPER_THRESHOLD,
        "lower_threshold": LOWER_THRESHOLD,
        "date": latest_all.get("date", "N/A"),
    }


def _ratio_to_score(ratio: float) -> float:
    """Map uptrend ratio (0-1 scale) to base score (0-100).

    Aligned with Monty's dashboard thresholds:
      Upper (Overbought) = 0.37, Lower (Oversold) = 0.097

    Scoring bands with linear interpolation:
      >= 0.50  -> 90-100 (Strong Bull)
      0.37-0.50 -> 70-89 (Bullish, above overbought)
      0.25-0.37 -> 40-69 (Neutral/Recovering)
      0.097-0.25 -> 10-39 (Weak, between thresholds)
      < 0.097  -> 0-9   (Crisis, below oversold)
    """
    if ratio >= 0.50:
        # 0.50 -> 90, 0.60+ -> 100
        return min(100, 90 + (ratio - 0.50) / 0.10 * 10)
    elif ratio >= UPPER_THRESHOLD:
        # 0.37 -> 70, 0.50 -> 89
        return 70 + (ratio - UPPER_THRESHOLD) / (0.50 - UPPER_THRESHOLD) * 19
    elif ratio >= 0.25:
        # 0.25 -> 40, 0.37 -> 69
        return 40 + (ratio - 0.25) / (UPPER_THRESHOLD - 0.25) * 29
    elif ratio >= LOWER_THRESHOLD:
        # 0.097 -> 10, 0.25 -> 39
        return 10 + (ratio - LOWER_THRESHOLD) / (0.25 - LOWER_THRESHOLD) * 29
    else:
        # 0 -> 0, 0.097 -> 9
        return max(0, ratio / LOWER_THRESHOLD * 9)


def _score_to_signal(score: int, ratio: float, trend: str) -> str:
    """Map score to human-readable signal."""
    ratio_pct = round(ratio * 100, 1)
    trend_label = f", trend {trend}" if trend else ""

    if score >= 90:
        return f"STRONG BULL: {ratio_pct}% uptrend ratio{trend_label}"
    elif score >= 70:
        return f"BULLISH: {ratio_pct}% uptrend ratio{trend_label}"
    elif score >= 45:
        return f"NEUTRAL: {ratio_pct}% uptrend ratio{trend_label}"
    elif score >= 30:
        return f"WEAK: {ratio_pct}% uptrend ratio{trend_label}"
    elif score >= 10:
        return f"VERY WEAK: {ratio_pct}% uptrend ratio{trend_label}"
    else:
        return f"CRISIS: {ratio_pct}% uptrend ratio{trend_label}"
