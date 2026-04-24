#!/usr/bin/env python3
"""
Component 3: Sector Rotation - Weight: 15%

Evaluates whether cyclical (risk-on) or defensive (risk-off) sectors are
leading, plus commodity sector dynamics for late-cycle detection.

Data Source: Sector Summary CSV

Sector Groups:
  Cyclical:  Technology, Consumer Cyclical, Communication Services, Financial, Industrials
  Defensive: Utilities, Consumer Defensive, Healthcare, Real Estate
  Commodity:  Energy, Basic Materials

Primary score: cyclical_avg - defensive_avg difference
  > +0.15  -> 90-100 (strong risk-on)
  +0.05~+0.15 -> 70-89 (healthy cyclical lead)
  -0.05~+0.05 -> 45-69 (balanced)
  -0.15~-0.05 -> 20-44 (defensive tilt)
  < -0.15  -> 0-19  (strong risk-off)

Commodity adjustment: if commodity_avg > both groups -> late cycle flag, penalty
"""

import math
import sys

from data_fetcher import build_summary_from_timeseries

# Sector classification
CYCLICAL_SECTORS = [
    "Technology",
    "Consumer Cyclical",
    "Communication Services",
    "Financial",
    "Industrials",
]
DEFENSIVE_SECTORS = [
    "Utilities",
    "Consumer Defensive",
    "Healthcare",
    "Real Estate",
]
COMMODITY_SECTORS = [
    "Energy",
    "Basic Materials",
]


def calculate_sector_rotation(
    sector_summary: list[dict], sector_timeseries: dict[str, list[dict]]
) -> dict:
    """
    Calculate sector rotation score.

    Args:
        sector_summary: List of sector summary rows
        sector_timeseries: Dict mapping sector -> timeseries rows (reserved)

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
                "cyclical_avg": None,
                "defensive_avg": None,
                "commodity_avg": None,
                "difference": None,
            }

    # Build lookup by sector name
    sector_map = {s["Sector"]: s for s in sector_summary if s.get("Sector")}

    # Calculate group averages
    cyclical_ratios = _get_group_ratios(sector_map, CYCLICAL_SECTORS)
    defensive_ratios = _get_group_ratios(sector_map, DEFENSIVE_SECTORS)
    commodity_ratios = _get_group_ratios(sector_map, COMMODITY_SECTORS)

    cyclical_avg = _avg(cyclical_ratios) if cyclical_ratios else None
    defensive_avg = _avg(defensive_ratios) if defensive_ratios else None
    commodity_avg = _avg(commodity_ratios) if commodity_ratios else None

    if cyclical_avg is None or defensive_avg is None:
        return {
            "score": 50,
            "signal": "INCOMPLETE DATA: Cannot calculate rotation (neutral default)",
            "data_available": False,
            "cyclical_avg": cyclical_avg,
            "defensive_avg": defensive_avg,
            "commodity_avg": commodity_avg,
            "difference": None,
        }

    difference = cyclical_avg - defensive_avg

    # Map difference to base score
    base_score = _difference_to_score(difference)

    # Commodity adjustment: late-cycle penalty
    late_cycle_flag = False
    commodity_penalty = 0
    if commodity_avg is not None:
        if commodity_avg > cyclical_avg and commodity_avg > defensive_avg:
            late_cycle_flag = True
            # Stronger penalty if commodity leads by a lot
            excess = commodity_avg - max(cyclical_avg, defensive_avg)
            if excess > 0.10:
                commodity_penalty = -10
            else:
                commodity_penalty = -5

    # Group divergence detection
    divergence_result = _calculate_group_divergence(sector_map)
    divergence_penalty = divergence_result.get("divergence_penalty", 0)

    score = round(min(100, max(0, base_score + commodity_penalty + divergence_penalty)))

    signal = _build_signal(score, difference, late_cycle_flag)

    # Build group details
    cyclical_details = _build_group_details(sector_map, CYCLICAL_SECTORS)
    defensive_details = _build_group_details(sector_map, DEFENSIVE_SECTORS)
    commodity_details = _build_group_details(sector_map, COMMODITY_SECTORS)

    return {
        "score": score,
        "signal": signal,
        "data_available": True,
        "cyclical_avg": round(cyclical_avg, 4),
        "cyclical_avg_pct": round(cyclical_avg * 100, 1),
        "defensive_avg": round(defensive_avg, 4),
        "defensive_avg_pct": round(defensive_avg * 100, 1),
        "commodity_avg": round(commodity_avg, 4) if commodity_avg is not None else None,
        "commodity_avg_pct": round(commodity_avg * 100, 1) if commodity_avg is not None else None,
        "difference": round(difference, 4),
        "difference_pct": round(difference * 100, 1),
        "late_cycle_flag": late_cycle_flag,
        "commodity_penalty": commodity_penalty,
        "divergence_flag": divergence_result.get("divergence_flag", False),
        "divergence_penalty": divergence_penalty,
        "cyclical_divergence": divergence_result.get("cyclical_divergence"),
        "defensive_divergence": divergence_result.get("defensive_divergence"),
        "cyclical_details": cyclical_details,
        "defensive_details": defensive_details,
        "commodity_details": commodity_details,
    }


def _get_group_ratios(sector_map: dict[str, dict], sector_names: list[str]) -> list[float]:
    """Extract ratios for a group of sectors."""
    ratios = []
    for name in sector_names:
        sector = sector_map.get(name)
        if sector and sector.get("Ratio") is not None:
            ratios.append(sector["Ratio"])
    return ratios


def _avg(values: list[float]) -> float:
    """Simple average."""
    return sum(values) / len(values)


def _difference_to_score(diff: float) -> float:
    """Map cyclical-defensive difference to score.

    > +0.15  -> 90-100 (strong risk-on)
    +0.05~+0.15 -> 70-89 (healthy cyclical lead)
    -0.05~+0.05 -> 45-69 (balanced)
    -0.15~-0.05 -> 20-44 (defensive tilt)
    < -0.15  -> 0-19  (strong risk-off)
    """
    if diff > 0.15:
        return min(100, 90 + (diff - 0.15) / 0.10 * 10)
    elif diff > 0.05:
        return 70 + (diff - 0.05) / 0.10 * 19
    elif diff > -0.05:
        return 45 + (diff + 0.05) / 0.10 * 24
    elif diff > -0.15:
        return 20 + (diff + 0.15) / 0.10 * 24
    else:
        return max(0, 19 + (diff + 0.15) / 0.10 * 19)


def _build_signal(score: int, difference: float, late_cycle: bool) -> str:
    """Build human-readable signal."""
    diff_pct = round(difference * 100, 1)
    late_str = " [LATE CYCLE WARNING]" if late_cycle else ""

    if score >= 90:
        return f"STRONG RISK-ON: Cyclical leads by {diff_pct}pp{late_str}"
    elif score >= 70:
        return f"RISK-ON: Cyclical leads by {diff_pct}pp{late_str}"
    elif score >= 45:
        return f"BALANCED: Cyclical-Defensive gap {diff_pct}pp{late_str}"
    elif score >= 20:
        return f"DEFENSIVE TILT: Defensive leads by {abs(diff_pct)}pp{late_str}"
    else:
        return f"STRONG RISK-OFF: Defensive leads by {abs(diff_pct)}pp{late_str}"


def _calculate_group_divergence(sector_map: dict[str, dict]) -> dict:
    """Detect intra-group divergence in Cyclical and Defensive groups.

    Divergence flag triggers when any of:
    - Group internal std_dev > 8pp (0.08)
    - Group internal max-min > 20pp (0.20)
    - A sector's trend opposes the majority trend within its group

    Returns:
        Dict with divergence_flag, divergence_penalty, cyclical_divergence,
        defensive_divergence
    """
    cyclical_div = _analyze_group(sector_map, CYCLICAL_SECTORS)
    defensive_div = _analyze_group(sector_map, DEFENSIVE_SECTORS)

    flag = cyclical_div["flagged"] or defensive_div["flagged"]
    penalty = -5 if flag else 0

    return {
        "divergence_flag": flag,
        "divergence_penalty": penalty,
        "cyclical_divergence": cyclical_div,
        "defensive_divergence": defensive_div,
    }


def _analyze_group(sector_map: dict[str, dict], sector_names: list[str]) -> dict:
    """Analyze divergence within a sector group."""
    ratios = []
    trends = []
    names_with_data = []

    for name in sector_names:
        sector = sector_map.get(name)
        if sector and sector.get("Ratio") is not None:
            ratios.append(sector["Ratio"])
            trends.append(sector.get("Trend", "").lower())
            names_with_data.append(name)

    if len(ratios) < 2:
        return {
            "flagged": False,
            "std_dev": None,
            "spread": None,
            "outliers": [],
            "trend_dissenters": [],
        }

    mean = sum(ratios) / len(ratios)
    variance = sum((r - mean) ** 2 for r in ratios) / len(ratios)
    std_dev = math.sqrt(variance)
    spread = max(ratios) - min(ratios)

    # Outlier detection: sectors more than 1.5 * std_dev from mean
    outliers = []
    for _i, (name, ratio) in enumerate(zip(names_with_data, ratios)):
        if abs(ratio - mean) > 1.5 * std_dev and std_dev > 0:
            outliers.append({"sector": name, "ratio": ratio, "deviation": round(ratio - mean, 4)})

    # Trend dissenter detection: sectors opposing the majority
    trend_dissenters = []
    if trends:
        up_count = sum(1 for t in trends if t == "up")
        down_count = sum(1 for t in trends if t == "down")
        majority = "up" if up_count >= down_count else "down"

        for name, trend in zip(names_with_data, trends):
            if trend and trend != majority:
                trend_dissenters.append({"sector": name, "trend": trend, "majority": majority})

    # Divergence flag conditions
    flagged = std_dev > 0.08 or spread > 0.20 or len(trend_dissenters) > 0

    return {
        "flagged": flagged,
        "std_dev": round(std_dev, 4),
        "spread": round(spread, 4),
        "outliers": outliers,
        "trend_dissenters": trend_dissenters,
    }


def _build_group_details(sector_map: dict[str, dict], sector_names: list[str]) -> list[dict]:
    """Build detail rows for a sector group."""
    details = []
    for name in sector_names:
        sector = sector_map.get(name)
        if sector:
            details.append(
                {
                    "sector": name,
                    "ratio": sector.get("Ratio"),
                    "ratio_pct": round(sector["Ratio"] * 100, 1)
                    if sector.get("Ratio") is not None
                    else None,
                    "trend": sector.get("Trend", ""),
                    "slope": sector.get("Slope"),
                }
            )
        else:
            details.append(
                {
                    "sector": name,
                    "ratio": None,
                    "ratio_pct": None,
                    "trend": "N/A",
                    "slope": None,
                }
            )
    return details
