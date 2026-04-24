#!/usr/bin/env python3
"""
Component 4: Momentum - Weight: 20%

Evaluates the rate of change (slope) and acceleration of the overall
uptrend ratio, plus sector-level slope breadth.

Data Source: Timeseries "all" + Sector Summary

Sub-scores:
  - Slope Score (50%): EMA(3)-smoothed current slope mapped to 0-100
  - Acceleration (30%): EMA(3)-smoothed slope series, 10v10 window (fallback 5v5)
  - Sector Slope Breadth (20%): Count of sectors with positive slope
"""

from typing import Optional


def calculate_momentum(all_timeseries: list[dict], sector_summary: list[dict]) -> dict:
    """
    Calculate momentum score from slope, acceleration, and sector breadth.

    Args:
        all_timeseries: Full "all" timeseries sorted by date ascending
        sector_summary: Latest sector summary rows

    Returns:
        Dict with score (0-100), signal, and detail fields
    """
    if not all_timeseries:
        return {
            "score": 50,
            "signal": "NO DATA: Timeseries unavailable (neutral default)",
            "data_available": False,
            "slope": None,
            "acceleration": None,
            "sector_slope_breadth": None,
        }

    latest = all_timeseries[-1]
    current_slope = latest.get("slope")

    # Extract slope series for smoothing
    slopes = [r.get("slope") for r in all_timeseries if r.get("slope") is not None]

    # Apply EMA(3) smoothing to slope series
    smoothed_slope = None
    if slopes:
        smoothed_slopes = _ema(slopes, span=3)
        smoothed_slope = smoothed_slopes[-1] if smoothed_slopes else current_slope
    else:
        smoothed_slopes = []

    # Sub-score 1: Slope Score (50%) - use smoothed slope
    effective_slope = smoothed_slope if smoothed_slope is not None else current_slope
    slope_score = _score_slope(effective_slope) if effective_slope is not None else 50

    # Sub-score 2: Acceleration (30%) - use smoothed slopes with 10v10 window
    accel_score, accel_value, accel_label = _score_acceleration_smoothed(smoothed_slopes)

    # Sub-score 3: Sector Slope Breadth (20%)
    breadth_score, positive_slope_count, total_sectors = _score_sector_slope_breadth(sector_summary)

    # Composite
    raw_score = slope_score * 0.50 + accel_score * 0.30 + breadth_score * 0.20
    score = round(min(100, max(0, raw_score)))

    signal = _build_signal(score, effective_slope, accel_label)

    return {
        "score": score,
        "signal": signal,
        "data_available": True,
        "slope": current_slope,
        "slope_smoothed": round(smoothed_slope, 6) if smoothed_slope is not None else None,
        "slope_smoothing": "EMA(3)",
        "slope_score": round(slope_score),
        "acceleration": accel_value,
        "acceleration_label": accel_label,
        "acceleration_score": round(accel_score),
        "acceleration_window": "10v10",
        "sector_positive_slope_count": positive_slope_count,
        "sector_total": total_sectors,
        "sector_slope_breadth_score": round(breadth_score),
        "date": latest.get("date", "N/A"),
    }


def _ema(values: list[float], span: int = 3) -> list[float]:
    """Calculate Exponential Moving Average.

    Args:
        values: List of float values
        span: EMA span (default 3)

    Returns:
        List of EMA values, same length as input. Empty list if input is empty.
    """
    if not values:
        return []
    if len(values) == 1:
        return [values[0]]

    alpha = 2.0 / (span + 1)
    result = [values[0]]
    for i in range(1, len(values)):
        ema_val = alpha * values[i] + (1 - alpha) * result[-1]
        result.append(ema_val)
    return result


def _classify_acceleration(acceleration: float) -> tuple:
    """Map acceleration value to (score, label)."""
    if acceleration > 0.005:
        return 90, "strong_accelerating"
    elif acceleration > 0.001:
        return 75, "accelerating"
    elif acceleration > -0.001:
        return 50, "steady"
    elif acceleration > -0.005:
        return 25, "decelerating"
    else:
        return 10, "strong_decelerating"


def _score_acceleration_smoothed(smoothed_slopes: list[float]) -> tuple:
    """Calculate acceleration from smoothed slopes using 10v10 window.

    Compares recent 10-point average vs prior 10-point average of smoothed slopes.

    Falls back to original 5v5 if fewer than 20 points available.

    Returns: (score, acceleration_value, label)
    """
    if len(smoothed_slopes) < 10:
        return _score_acceleration_from_values(smoothed_slopes, window=5)

    if len(smoothed_slopes) >= 20:
        recent_avg = sum(smoothed_slopes[-10:]) / 10
        prior_avg = sum(smoothed_slopes[-20:-10]) / 10
    else:
        # Fallback to 5v5 with smoothed data
        return _score_acceleration_from_values(smoothed_slopes, window=5)

    acceleration = recent_avg - prior_avg
    score, label = _classify_acceleration(acceleration)

    return score, round(acceleration, 6), label


def _score_acceleration_from_values(slopes: list[float], window: int = 5) -> tuple:
    """Fallback acceleration using smaller window."""
    if len(slopes) < window * 2:
        return 50, None, "insufficient_data"

    recent_avg = sum(slopes[-window:]) / window
    prior_avg = sum(slopes[-window * 2 : -window]) / window
    acceleration = recent_avg - prior_avg
    score, label = _classify_acceleration(acceleration)

    return score, round(acceleration, 6), label


def _score_slope(slope: float) -> float:
    """Map current slope to 0-100 score.

    Typical slope range: -0.02 to +0.02
    Extreme range: -0.03 to +0.03

      >= +0.02 -> 95-100 (strong bullish momentum)
      +0.01~+0.02 -> 75-94
      0~+0.01 -> 55-74 (mild positive)
      -0.01~0 -> 35-54 (mild negative)
      -0.02~-0.01 -> 10-34
      < -0.02 -> 0-9 (strong bearish momentum)
    """
    if slope >= 0.02:
        return min(100, 95 + (slope - 0.02) / 0.01 * 5)
    elif slope >= 0.01:
        return 75 + (slope - 0.01) / 0.01 * 19
    elif slope >= 0:
        return 55 + slope / 0.01 * 19
    elif slope >= -0.01:
        return 35 + (slope + 0.01) / 0.01 * 19
    elif slope >= -0.02:
        return 10 + (slope + 0.02) / 0.01 * 24
    else:
        return max(0, 9 + (slope + 0.02) / 0.01 * 9)


def _score_sector_slope_breadth(sector_summary: list[dict]) -> tuple:
    """Score based on count of sectors with positive slope.

    Returns: (score, positive_count, total_count)
    """
    if not sector_summary:
        return 50, 0, 0

    total = len(sector_summary)
    positive = sum(1 for s in sector_summary if s.get("Slope") is not None and s["Slope"] > 0)

    if total == 0:
        return 50, 0, 0

    # Linear mapping: 0 sectors -> 0, all sectors -> 100
    score = (positive / total) * 100

    return score, positive, total


def _build_signal(score: int, slope: Optional[float], accel_label: str) -> str:
    """Build human-readable signal."""
    slope_str = f"slope={slope:.4f}" if slope is not None else "slope=N/A"
    accel_str = accel_label.replace("_", " ")

    if score >= 80:
        return f"STRONG MOMENTUM: {slope_str}, {accel_str}"
    elif score >= 60:
        return f"POSITIVE MOMENTUM: {slope_str}, {accel_str}"
    elif score >= 40:
        return f"NEUTRAL MOMENTUM: {slope_str}, {accel_str}"
    elif score >= 20:
        return f"WEAK MOMENTUM: {slope_str}, {accel_str}"
    else:
        return f"NEGATIVE MOMENTUM: {slope_str}, {accel_str}"
