#!/usr/bin/env python3
"""
Component 2: Sector Participation - Weight: 25%

Evaluates how many sectors are participating in the uptrend and the
uniformity of participation (spread between strongest and weakest).

Data Source: Sector Summary CSV

Sub-scores:
  - Uptrend Count (60%): How many of 11 sectors are in uptrend
  - Spread (40%): Max-min ratio spread (uniform = healthy, selective = weak)
"""

import sys
from typing import Optional

from data_fetcher import build_summary_from_timeseries

# Monty's official dashboard thresholds
OVERBOUGHT_THRESHOLD = 0.37  # Upper threshold
OVERSOLD_THRESHOLD = 0.097  # Lower threshold


def calculate_sector_participation(
    sector_summary: list[dict], sector_timeseries: dict[str, list[dict]]
) -> dict:
    """
    Calculate sector participation score.

    Args:
        sector_summary: List of sector summary rows
        sector_timeseries: Dict mapping sector -> timeseries rows; used as
                          fallback if sector_summary is unavailable

    Returns:
        Dict with score (0-100), signal, and detail fields
    """
    if not sector_summary:
        if sector_timeseries:
            sector_summary = build_summary_from_timeseries(sector_timeseries)
            print("  (fallback: built sector summary from timeseries data)", file=sys.stderr)
        else:
            return {
                "score": 50,
                "signal": "NO DATA: Sector summary unavailable (neutral default)",
                "data_available": False,
                "uptrend_count": None,
                "total_sectors": None,
                "spread": None,
                "sector_details": [],
            }

    total_sectors = len(sector_summary)
    if total_sectors == 0:
        return {
            "score": 50,
            "signal": "NO DATA: No sectors in summary",
            "data_available": False,
            "uptrend_count": 0,
            "total_sectors": 0,
            "spread": None,
            "sector_details": [],
        }

    # Count sectors in uptrend
    uptrend_count = sum(1 for s in sector_summary if s.get("Trend", "").lower() == "up")

    # Get ratios for spread calculation
    ratios = [s["Ratio"] for s in sector_summary if s.get("Ratio") is not None]

    if ratios:
        max_ratio = max(ratios)
        min_ratio = min(ratios)
        spread = max_ratio - min_ratio
    else:
        max_ratio = None
        min_ratio = None
        spread = None

    # Sub-score 1: Uptrend Count (60%)
    count_score = _score_uptrend_count(uptrend_count, total_sectors)

    # Sub-score 2: Spread (40%)
    spread_score = _score_spread(spread) if spread is not None else 50

    # Composite
    raw_score = count_score * 0.60 + spread_score * 0.40
    score = round(min(100, max(0, raw_score)))

    # Identify overbought/oversold sectors
    overbought = [
        s
        for s in sector_summary
        if s.get("Ratio") is not None and s["Ratio"] >= OVERBOUGHT_THRESHOLD
    ]
    oversold = [
        s for s in sector_summary if s.get("Ratio") is not None and s["Ratio"] < OVERSOLD_THRESHOLD
    ]

    signal = _build_signal(score, uptrend_count, total_sectors, spread)

    # Build sector details sorted by ratio descending
    sector_details = []
    for s in sorted(sector_summary, key=lambda x: x.get("Ratio") or 0, reverse=True):
        sector_details.append(
            {
                "sector": s.get("Sector", "Unknown"),
                "ratio": s.get("Ratio"),
                "ratio_pct": round(s["Ratio"] * 100, 1) if s.get("Ratio") is not None else None,
                "ma_10": s.get("10MA"),
                "trend": s.get("Trend", ""),
                "slope": s.get("Slope"),
                "status": s.get("Status", ""),
                "count": s.get("Count"),
                "total": s.get("Total"),
            }
        )

    return {
        "score": score,
        "signal": signal,
        "data_available": True,
        "uptrend_count": uptrend_count,
        "total_sectors": total_sectors,
        "count_score": round(count_score),
        "spread": round(spread, 4) if spread is not None else None,
        "spread_pct": round(spread * 100, 1) if spread is not None else None,
        "spread_score": round(spread_score),
        "max_ratio": max_ratio,
        "min_ratio": min_ratio,
        "overbought_count": len(overbought),
        "overbought_sectors": [s.get("Sector", "") for s in overbought],
        "oversold_count": len(oversold),
        "oversold_sectors": [s.get("Sector", "") for s in oversold],
        "sector_details": sector_details,
    }


def _score_uptrend_count(uptrend_count: int, total_sectors: int) -> float:
    """Score based on number of sectors in uptrend.

    10-11 sectors -> 100
    8-9  sectors -> 80
    6-7  sectors -> 60
    4-5  sectors -> 40
    2-3  sectors -> 20
    0-1  sectors -> 0
    """
    if total_sectors == 0:
        return 50

    if uptrend_count >= 10:
        return 100
    elif uptrend_count >= 8:
        return 80
    elif uptrend_count >= 6:
        return 60
    elif uptrend_count >= 4:
        return 40
    elif uptrend_count >= 2:
        return 20
    else:
        return 0


def _score_spread(spread: float) -> float:
    """Score based on max-min ratio spread (0-1 scale).

    < 0.15 -> 100 (uniform participation)
    0.15-0.25 -> 80 (healthy spread)
    0.25-0.35 -> 60 (moderate dispersion)
    0.35-0.45 -> 30 (wide divergence)
    > 0.45 -> 0 (extremely selective)
    """
    if spread < 0.15:
        return 100
    elif spread < 0.25:
        return 100 - (spread - 0.15) / 0.10 * 20
    elif spread < 0.35:
        return 80 - (spread - 0.25) / 0.10 * 20
    elif spread < 0.45:
        return 60 - (spread - 0.35) / 0.10 * 30
    else:
        return max(0, 30 - (spread - 0.45) / 0.10 * 30)


def _build_signal(
    score: int, uptrend_count: int, total_sectors: int, spread: Optional[float]
) -> str:
    """Build human-readable signal."""
    spread_pct = f", spread {round(spread * 100, 1)}%" if spread is not None else ""

    if score >= 80:
        return (
            f"BROAD PARTICIPATION: {uptrend_count}/{total_sectors} sectors uptrending{spread_pct}"
        )
    elif score >= 60:
        return f"HEALTHY: {uptrend_count}/{total_sectors} sectors uptrending{spread_pct}"
    elif score >= 40:
        return f"MODERATE: {uptrend_count}/{total_sectors} sectors uptrending{spread_pct}"
    elif score >= 20:
        return f"NARROW: {uptrend_count}/{total_sectors} sectors uptrending{spread_pct}"
    else:
        return f"VERY NARROW: {uptrend_count}/{total_sectors} sectors uptrending{spread_pct}"
