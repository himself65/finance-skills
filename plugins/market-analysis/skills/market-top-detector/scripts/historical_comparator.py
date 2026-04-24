#!/usr/bin/env python3
"""
Historical Top Pattern Comparator

Compares current component scores to estimated score patterns from
historical market tops (2000, 2007, 2018, 2022) using Sum of Squared
Differences (SSD) to find the closest match.
"""

# Component weights (must match scorer.py)
COMPONENT_WEIGHTS = {
    "distribution_days": 0.25,
    "leading_stocks": 0.20,
    "defensive_rotation": 0.15,
    "breadth_divergence": 0.15,
    "index_technical": 0.15,
    "sentiment": 0.10,
}

# Estimated median component scores during historical tops
# Based on references/historical_tops.md analysis
HISTORICAL_TOPS = {
    "2000 (Dot-Com Bubble)": {
        "distribution_days": 90,
        "leading_stocks": 85,
        "defensive_rotation": 70,
        "breadth_divergence": 95,
        "index_technical": 60,
        "sentiment": 90,
    },
    "2007 (Financial Crisis)": {
        "distribution_days": 80,
        "leading_stocks": 75,
        "defensive_rotation": 85,
        "breadth_divergence": 80,
        "index_technical": 70,
        "sentiment": 75,
    },
    "2018 (Q4 Correction)": {
        "distribution_days": 60,
        "leading_stocks": 50,
        "defensive_rotation": 40,
        "breadth_divergence": 55,
        "index_technical": 65,
        "sentiment": 55,
    },
    "2022 (Rate Hike Bear)": {
        "distribution_days": 75,
        "leading_stocks": 90,
        "defensive_rotation": 60,
        "breadth_divergence": 70,
        "index_technical": 80,
        "sentiment": 65,
    },
}

COMPONENT_KEYS = [
    "distribution_days",
    "leading_stocks",
    "defensive_rotation",
    "breadth_divergence",
    "index_technical",
    "sentiment",
]


def _compute_ssd(current: dict[str, float], historical: dict[str, float]) -> float:
    """Compute weighted sum of squared differences between two score dicts.

    Each component's squared difference is multiplied by its weight,
    aligning the distance metric with the composite score design.
    """
    ssd = 0.0
    for key in COMPONENT_KEYS:
        diff = current.get(key, 0) - historical.get(key, 0)
        weight = COMPONENT_WEIGHTS.get(key, 1.0 / len(COMPONENT_KEYS))
        ssd += weight * diff * diff
    return ssd


def compare_to_historical(current_scores: dict[str, float]) -> dict:
    """
    Compare current scores to historical top patterns.

    Args:
        current_scores: Dict of component key -> score (0-100)

    Returns:
        Dict with closest_match, all_comparisons, narrative
    """
    comparisons = []
    for name, hist_scores in HISTORICAL_TOPS.items():
        ssd = _compute_ssd(current_scores, hist_scores)
        comparisons.append(
            {
                "name": name,
                "ssd": round(ssd, 1),
                "scores": hist_scores,
            }
        )

    comparisons.sort(key=lambda x: x["ssd"])
    closest = comparisons[0]

    narrative = _generate_narrative(current_scores, closest)

    return {
        "closest_match": closest["name"],
        "closest_ssd": closest["ssd"],
        "comparisons": comparisons,
        "narrative": narrative,
    }


def _generate_narrative(current_scores: dict[str, float], closest: dict) -> str:
    """Generate a textual comparison highlighting key differences."""
    hist_scores = closest["scores"]
    name = closest["name"]
    diffs = []

    for key in COMPONENT_KEYS:
        curr = current_scores.get(key, 0)
        hist = hist_scores.get(key, 0)
        diff = curr - hist
        if abs(diff) >= 15:
            direction = "higher" if diff > 0 else "lower"
            label = key.replace("_", " ").title()
            diffs.append(f"{label} is {abs(diff):.0f}pt {direction} than {name}")

    if not diffs:
        return f"Current pattern closely matches {name} across all components."

    diff_text = "; ".join(diffs)
    return f"Closest to {name}. Key differences: {diff_text}."
