#!/usr/bin/env python3
"""
Component 5: Historical Context - Weight: 10%

Evaluates the current uptrend ratio relative to its full historical
distribution (2023/08~present) using percentile rank.

Data Source: Timeseries "all" worksheet

Score = percentile rank of current ratio in historical distribution
Additional context: min, max, median, 30d avg, 90d avg
"""

from typing import Optional


def calculate_historical_context(all_timeseries: list[dict]) -> dict:
    """
    Calculate historical context score via percentile rank.

    Args:
        all_timeseries: Full "all" timeseries sorted by date ascending

    Returns:
        Dict with score (0-100), signal, and context fields
    """
    if not all_timeseries:
        return {
            "score": 50,
            "signal": "NO DATA: Historical timeseries unavailable (neutral default)",
            "data_available": False,
            "percentile": None,
            "current_ratio": None,
            "historical_min": None,
            "historical_max": None,
            "historical_median": None,
        }

    # Extract all valid ratios
    ratios = [r["ratio"] for r in all_timeseries if r.get("ratio") is not None]

    if len(ratios) < 2:
        return {
            "score": 50,
            "signal": "INSUFFICIENT DATA: Need at least 2 data points",
            "data_available": False,
            "percentile": None,
            "current_ratio": None,
            "data_points": len(ratios),
        }

    current_ratio = ratios[-1]

    # Calculate percentile rank
    below_count = sum(1 for r in ratios if r < current_ratio)
    equal_count = sum(1 for r in ratios if r == current_ratio)
    percentile = (below_count + equal_count * 0.5) / len(ratios) * 100
    percentile = round(percentile, 1)

    # Score = percentile rank (direct mapping)
    score = round(min(100, max(0, percentile)))

    # Historical statistics
    sorted_ratios = sorted(ratios)
    hist_min = sorted_ratios[0]
    hist_max = sorted_ratios[-1]
    n = len(sorted_ratios)
    if n % 2 == 0:
        hist_median = (sorted_ratios[n // 2 - 1] + sorted_ratios[n // 2]) / 2
    else:
        hist_median = sorted_ratios[n // 2]

    # Recent averages
    avg_30d = _avg_last_n(ratios, 30)
    avg_90d = _avg_last_n(ratios, 90)

    signal = _build_signal(score, percentile, current_ratio)

    # Assess confidence of historical analysis
    confidence = _assess_confidence(ratios)

    # Append confidence caveat to signal if low
    if confidence["confidence_level"] in ("Low", "Very Low"):
        signal += f" [confidence: {confidence['confidence_level']}]"

    return {
        "score": score,
        "signal": signal,
        "data_available": True,
        "percentile": percentile,
        "current_ratio": current_ratio,
        "current_ratio_pct": round(current_ratio * 100, 1),
        "historical_min": round(hist_min, 4),
        "historical_min_pct": round(hist_min * 100, 1),
        "historical_max": round(hist_max, 4),
        "historical_max_pct": round(hist_max * 100, 1),
        "historical_median": round(hist_median, 4),
        "historical_median_pct": round(hist_median * 100, 1),
        "avg_30d": round(avg_30d, 4) if avg_30d is not None else None,
        "avg_30d_pct": round(avg_30d * 100, 1) if avg_30d is not None else None,
        "avg_90d": round(avg_90d, 4) if avg_90d is not None else None,
        "avg_90d_pct": round(avg_90d * 100, 1) if avg_90d is not None else None,
        "data_points": len(ratios),
        "date_range": f"{all_timeseries[0].get('date', '?')} to {all_timeseries[-1].get('date', '?')}",
        "confidence": confidence,
    }


def _assess_confidence(ratios: list[float]) -> dict:
    """Assess confidence level of percentile analysis.

    Evaluates:
    - Sample size: >=1000 full, 500-999 moderate, 200-499 limited, <200 minimal
    - Regime coverage: Has bear data (min<10%) AND bull data (max>40%)
    - Recency bias: Whether recent 90 days span less than 30% of full range

    Returns:
        Dict with confidence_level, confidence_score, regime details
    """
    n = len(ratios)

    # Sample size assessment
    if n >= 1000:
        size_score = 3
        size_label = "full"
    elif n >= 500:
        size_score = 2
        size_label = "moderate"
    elif n >= 200:
        size_score = 1
        size_label = "limited"
    else:
        size_score = 0
        size_label = "minimal"

    # Regime coverage
    hist_min = min(ratios) if ratios else 0
    hist_max = max(ratios) if ratios else 0
    has_bear = hist_min < 0.10  # Below 10%
    has_bull = hist_max > 0.40  # Above 40%

    if has_bear and has_bull:
        regime_coverage = "Both"
        regime_score = 2
    elif has_bear or has_bull:
        regime_coverage = "Partial"
        regime_score = 1
    else:
        regime_coverage = "Narrow"
        regime_score = 0

    # Recency bias
    full_range = hist_max - hist_min if hist_max != hist_min else 1.0
    recent_90 = ratios[-90:] if len(ratios) >= 90 else ratios
    recent_range = max(recent_90) - min(recent_90) if len(recent_90) >= 2 else 0
    recency_ratio = recent_range / full_range if full_range > 0 else 0

    if recency_ratio >= 0.30:
        recency_label = "balanced"
        recency_score = 1
    else:
        recency_label = "biased"
        recency_score = 0

    # Overall confidence
    total_score = size_score + regime_score + recency_score
    if total_score >= 5:
        confidence_level = "High"
    elif total_score >= 3:
        confidence_level = "Moderate"
    elif total_score >= 1:
        confidence_level = "Low"
    else:
        confidence_level = "Very Low"

    return {
        "confidence_level": confidence_level,
        "confidence_score": total_score,
        "sample_size": n,
        "sample_label": size_label,
        "has_bear_data": has_bear,
        "has_bull_data": has_bull,
        "regime_coverage": regime_coverage,
        "recency_label": recency_label,
    }


def _avg_last_n(values: list[float], n: int) -> Optional[float]:
    """Average of the last n values, or all if fewer than n."""
    if not values:
        return None
    subset = values[-n:]
    return sum(subset) / len(subset)


def _build_signal(score: int, percentile: float, current_ratio: float) -> str:
    """Build human-readable signal."""
    ratio_pct = round(current_ratio * 100, 1)

    if score >= 80:
        return f"ABOVE AVERAGE: {ratio_pct}% at {percentile}th percentile historically"
    elif score >= 60:
        return f"SLIGHTLY ABOVE: {ratio_pct}% at {percentile}th percentile historically"
    elif score >= 40:
        return f"NEAR MEDIAN: {ratio_pct}% at {percentile}th percentile historically"
    elif score >= 20:
        return f"BELOW AVERAGE: {ratio_pct}% at {percentile}th percentile historically"
    else:
        return f"HISTORICALLY LOW: {ratio_pct}% at {percentile}th percentile historically"
