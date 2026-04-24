#!/usr/bin/env python3
"""
Component 4: Market Breadth Divergence (Weight: 15%)

Data source: CLI arguments (collected via WebSearch before script execution)
- breadth_200dma: % of S&P 500 stocks above 200DMA
- breadth_50dma: % of S&P 500 stocks above 50DMA

Scoring logic:
  When index is near highs (within -5% of 52-week high):
    200DMA_above < 40% -> 100 (Critical divergence)
    200DMA_above < 50% -> 80
    200DMA_above < 60% -> 60
    200DMA_above < 70% -> 35
    200DMA_above >= 70% -> 10

  When index is NOT near highs (> -5%):
    Score is halved (breadth divergence less meaningful when index is correcting)

  50DMA breadth is used as a supplementary signal.
"""

from typing import Optional


def calculate_breadth_divergence(
    breadth_200dma: Optional[float],
    breadth_50dma: Optional[float],
    index_distance_from_high_pct: float,
) -> dict:
    """
    Calculate market breadth divergence score.

    Args:
        breadth_200dma: % of S&P 500 stocks above 200DMA (0-100)
        breadth_50dma: % of S&P 500 stocks above 50DMA (0-100)
        index_distance_from_high_pct: S&P 500 distance from 52-week high (negative %)

    Returns:
        Dict with score (0-100), signal, details
    """
    if breadth_200dma is None:
        return {
            "score": 50,
            "signal": "NO DATA: Breadth data not provided (neutral default)",
            "data_available": False,
            "breadth_200dma": None,
            "breadth_50dma": breadth_50dma,
            "index_near_highs": False,
            "divergence_detected": False,
        }

    index_near_highs = index_distance_from_high_pct >= -5.0

    # Primary score based on 200DMA breadth
    raw_score = _score_200dma_breadth(breadth_200dma)

    # Halve score if index is NOT near highs
    if not index_near_highs:
        raw_score = raw_score * 0.5

    # 50DMA breadth supplementary adjustment
    if breadth_50dma is not None:
        if breadth_50dma < 30 and index_near_highs:
            raw_score = min(100, raw_score + 10)  # Extra warning
        elif breadth_50dma > 70:
            raw_score = max(0, raw_score - 5)  # Slight relief

    score = round(min(100, max(0, raw_score)))

    # Detect divergence
    divergence_detected = index_near_highs and breadth_200dma < 60

    if score >= 80:
        signal = "CRITICAL: Severe breadth divergence - index at highs but breadth collapsing"
    elif score >= 60:
        signal = "WARNING: Significant breadth divergence"
    elif score >= 35:
        signal = "CAUTION: Mild breadth weakness"
    elif divergence_detected:
        signal = "WATCH: Some breadth deterioration despite index strength"
    else:
        signal = "HEALTHY: Breadth supports index level"

    return {
        "score": score,
        "signal": signal,
        "data_available": True,
        "breadth_200dma": breadth_200dma,
        "breadth_50dma": breadth_50dma,
        "index_near_highs": index_near_highs,
        "index_distance_from_high_pct": round(index_distance_from_high_pct, 1),
        "divergence_detected": divergence_detected,
    }


def _score_200dma_breadth(breadth_200dma: float) -> int:
    """Score based on % of stocks above 200DMA.

    Calibrated thresholds (linearly interpolated):
      < 40%  -> 100 (Critical divergence)
      40-50% -> 100 to 55 (Severe)
      50-60% -> 55 to 30 (Moderate)
      60-70% -> 30 to 5  (Mild - still relatively healthy)
      >= 70% -> 5         (Healthy breadth)

    Calibration note: 62.26% should score ~24 (healthy/green signal)
    """
    if breadth_200dma < 40:
        return 100
    elif breadth_200dma < 50:
        return round(100 - (breadth_200dma - 40) / 10 * 45)
    elif breadth_200dma < 60:
        return round(55 - (breadth_200dma - 50) / 10 * 25)
    elif breadth_200dma < 70:
        return round(30 - (breadth_200dma - 60) / 10 * 25)
    else:
        return 5
