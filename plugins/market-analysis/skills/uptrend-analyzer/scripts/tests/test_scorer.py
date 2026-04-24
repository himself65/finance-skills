"""Tests for scorer.py"""

import pytest
from scorer import (
    COMPONENT_WEIGHTS,
    _apply_warning_overlays,
    _interpret_zone,
    calculate_composite_score,
)


def _all_scores(value):
    """Return component_scores dict with all components set to the same value."""
    return {k: value for k in COMPONENT_WEIGHTS}


def _all_available():
    """Return data_availability dict with all components available."""
    return {k: True for k in COMPONENT_WEIGHTS}


# --- _interpret_zone tests ---


def test_zone_bear():
    """score=10 -> Bear, red."""
    zone = _interpret_zone(10)
    assert zone["zone"] == "Bear"
    assert zone["color"] == "red"


def test_zone_bear_boundary():
    """score=19 -> Bear (< 20)."""
    zone = _interpret_zone(19)
    assert zone["zone"] == "Bear"


def test_zone_cautious():
    """score=30 -> Cautious, orange."""
    zone = _interpret_zone(30)
    assert zone["zone"] == "Cautious"
    assert zone["color"] == "orange"


def test_zone_cautious_boundary():
    """score=20 -> Cautious (>= 20)."""
    zone = _interpret_zone(20)
    assert zone["zone"] == "Cautious"
    assert zone["color"] == "orange"


def test_zone_neutral():
    """score=50 -> Neutral, yellow."""
    zone = _interpret_zone(50)
    assert zone["zone"] == "Neutral"
    assert zone["color"] == "yellow"


def test_zone_neutral_boundary():
    """score=40 -> Neutral (>= 40)."""
    zone = _interpret_zone(40)
    assert zone["zone"] == "Neutral"
    assert zone["color"] == "yellow"


def test_zone_bull():
    """score=70 -> Bull, light_green."""
    zone = _interpret_zone(70)
    assert zone["zone"] == "Bull"
    assert zone["color"] == "light_green"


def test_zone_bull_boundary():
    """score=60 -> Bull (>= 60)."""
    zone = _interpret_zone(60)
    assert zone["zone"] == "Bull"
    assert zone["color"] == "light_green"


def test_zone_strong_bull():
    """score=90 -> Strong Bull, green."""
    zone = _interpret_zone(90)
    assert zone["zone"] == "Strong Bull"
    assert zone["color"] == "green"


def test_zone_strong_bull_boundary():
    """score=80 -> Strong Bull (>= 80)."""
    zone = _interpret_zone(80)
    assert zone["zone"] == "Strong Bull"
    assert zone["color"] == "green"


# --- Composite calculation tests ---


def test_composite_weighted_sum():
    """Verify weighted calculation with specific per-component scores."""
    scores = {
        "market_breadth": 80,  # 80 * 0.30 = 24.0
        "sector_participation": 60,  # 60 * 0.25 = 15.0
        "sector_rotation": 40,  # 40 * 0.15 = 6.0
        "momentum": 70,  # 70 * 0.20 = 14.0
        "historical_context": 50,  # 50 * 0.10 = 5.0
    }
    # Expected composite: 24.0 + 15.0 + 6.0 + 14.0 + 5.0 = 64.0
    result = calculate_composite_score(scores)
    assert result["composite_score"] == pytest.approx(64.0, abs=0.1)


def test_composite_all_100():
    """All scores 100 -> composite=100."""
    result = calculate_composite_score(_all_scores(100))
    assert result["composite_score"] == pytest.approx(100.0, abs=0.1)


def test_composite_all_0():
    """All scores 0 -> composite=0."""
    result = calculate_composite_score(_all_scores(0))
    assert result["composite_score"] == pytest.approx(0.0, abs=0.1)


def test_strongest_weakest():
    """Correctly identifies max/min components."""
    scores = {
        "market_breadth": 50,
        "sector_participation": 90,
        "sector_rotation": 30,
        "momentum": 70,
        "historical_context": 60,
    }
    result = calculate_composite_score(scores)
    assert result["strongest_component"]["component"] == "sector_participation"
    assert result["strongest_component"]["score"] == 90
    assert result["weakest_component"]["component"] == "sector_rotation"
    assert result["weakest_component"]["score"] == 30


# --- Warning overlay tests ---


def test_warning_late_cycle():
    """late_cycle flag generates warning."""
    zone_info = _interpret_zone(85)
    warnings, _ = _apply_warning_overlays(zone_info, {"late_cycle": True})
    assert len(warnings) == 1
    assert warnings[0]["flag"] == "late_cycle"
    assert "LATE CYCLE" in warnings[0]["label"]


def test_warning_high_spread():
    """high_spread flag generates warning."""
    zone_info = _interpret_zone(85)
    warnings, _ = _apply_warning_overlays(zone_info, {"high_spread": True})
    assert len(warnings) == 1
    assert warnings[0]["flag"] == "high_spread"
    assert "SELECTIVITY" in warnings[0]["label"]


def test_warning_both_active():
    """Both flags active -> two warnings."""
    zone_info = _interpret_zone(85)
    warnings, _ = _apply_warning_overlays(zone_info, {"late_cycle": True, "high_spread": True})
    assert len(warnings) == 2
    flags = {w["flag"] for w in warnings}
    assert flags == {"late_cycle", "high_spread"}


def test_warning_tightens_bull_exposure():
    """Bull zone with warning -> exposure tightened to 80-90%."""
    zone_info = _interpret_zone(70)  # Bull zone
    assert zone_info["zone"] == "Bull"
    _, returned_zone_info = _apply_warning_overlays(zone_info, {"late_cycle": True})
    assert "80-90%" in returned_zone_info["exposure_guidance"]


def test_warning_tightens_strong_bull():
    """Strong Bull with warning -> exposure tightened to 90-100%."""
    zone_info = _interpret_zone(90)  # Strong Bull zone
    assert zone_info["zone"] == "Strong Bull"
    _, returned_zone_info = _apply_warning_overlays(zone_info, {"high_spread": True})
    assert "90-100%" in returned_zone_info["exposure_guidance"]


def test_warning_overlay_does_not_mutate_original():
    """Original zone_info dict is not modified."""
    zone_info = _interpret_zone(70)
    original_guidance = zone_info["exposure_guidance"]
    _, returned_zone_info = _apply_warning_overlays(zone_info, {"late_cycle": True})
    assert zone_info["exposure_guidance"] == original_guidance  # not mutated
    assert "80-90%" in returned_zone_info["exposure_guidance"]  # returned one is modified


# --- Data quality test ---


def test_data_quality_complete():
    """All components available -> 'Complete (5/5 components)'."""
    result = calculate_composite_score(
        _all_scores(50),
        data_availability=_all_available(),
    )
    assert result["data_quality"]["available_count"] == 5
    assert result["data_quality"]["total_components"] == 5
    assert "Complete (5/5 components)" in result["data_quality"]["label"]
    assert result["data_quality"]["missing_components"] == []
