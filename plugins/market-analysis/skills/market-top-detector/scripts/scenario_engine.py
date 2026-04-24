#!/usr/bin/env python3
"""
What-If Scenario Analysis Engine

Generates 4 sensitivity scenarios by perturbing component scores
and re-running the composite scoring engine.
"""

from scorer import calculate_composite_score


def generate_scenarios(
    component_scores: dict[str, float], data_availability: dict[str, bool] = None
) -> list[dict]:
    """
    Generate 4 what-if scenarios based on current component scores.

    Scenarios:
    1. Breadth Deterioration: breadth_divergence -> 55
    2. Distribution Reset: distribution_days -> 55
    3. Full Deterioration: top 3 weakest components each +20pt
    4. Recovery: top 2 strongest components each -30pt

    Args:
        component_scores: Dict of component key -> score (0-100)
        data_availability: Optional data availability dict

    Returns:
        List of 4 scenario dicts with name, changes, new_score, new_zone
    """
    scenarios = []

    # Scenario 1: Breadth Deterioration
    s1 = dict(component_scores)
    s1["breadth_divergence"] = max(s1.get("breadth_divergence", 0), 55)
    s1_result = calculate_composite_score(s1, data_availability)
    scenarios.append(
        {
            "name": "Breadth Deterioration",
            "description": "Breadth divergence worsens to 55+",
            "changes": {"breadth_divergence": s1["breadth_divergence"]},
            "new_score": s1_result["composite_score"],
            "new_zone": s1_result["zone"],
            "delta": round(
                s1_result["composite_score"] - _current_score(component_scores, data_availability),
                1,
            ),
        }
    )

    # Scenario 2: Distribution Reset (ease to 55 or less)
    s2 = dict(component_scores)
    s2["distribution_days"] = min(s2.get("distribution_days", 0), 55)
    s2_result = calculate_composite_score(s2, data_availability)
    scenarios.append(
        {
            "name": "Distribution Reset",
            "description": "Distribution days ease to 55 or less",
            "changes": {"distribution_days": s2["distribution_days"]},
            "new_score": s2_result["composite_score"],
            "new_zone": s2_result["zone"],
            "delta": round(
                s2_result["composite_score"] - _current_score(component_scores, data_availability),
                1,
            ),
        }
    )

    # Scenario 3: Full Deterioration - raise lowest 3 by +20pt
    sorted_components = sorted(component_scores.items(), key=lambda x: x[1])
    s3 = dict(component_scores)
    changes_3 = {}
    for key, val in sorted_components[:3]:
        new_val = min(100, val + 20)
        s3[key] = new_val
        changes_3[key] = new_val
    s3_result = calculate_composite_score(s3, data_availability)
    scenarios.append(
        {
            "name": "Full Deterioration",
            "description": "3 weakest components each worsen by +20pt",
            "changes": changes_3,
            "new_score": s3_result["composite_score"],
            "new_zone": s3_result["zone"],
            "delta": round(
                s3_result["composite_score"] - _current_score(component_scores, data_availability),
                1,
            ),
        }
    )

    # Scenario 4: Recovery - lower highest 2 by -30pt
    sorted_desc = sorted(component_scores.items(), key=lambda x: x[1], reverse=True)
    s4 = dict(component_scores)
    changes_4 = {}
    for key, val in sorted_desc[:2]:
        new_val = max(0, val - 30)
        s4[key] = new_val
        changes_4[key] = new_val
    s4_result = calculate_composite_score(s4, data_availability)
    scenarios.append(
        {
            "name": "Recovery",
            "description": "2 strongest warning signals improve by -30pt",
            "changes": changes_4,
            "new_score": s4_result["composite_score"],
            "new_zone": s4_result["zone"],
            "delta": round(
                s4_result["composite_score"] - _current_score(component_scores, data_availability),
                1,
            ),
        }
    )

    return scenarios


def _current_score(
    component_scores: dict[str, float], data_availability: dict[str, bool] = None
) -> float:
    """Helper to get the current composite score."""
    result = calculate_composite_score(component_scores, data_availability)
    return result["composite_score"]
