"""Tests for Phase 2+ new features:
- Group divergence detection (sector_rotation_calculator)
- Warning penalties (scorer)
- Zone detail and proximity (scorer)
- EMA smoothing (momentum_calculator)
- Smoothed acceleration (momentum_calculator)
- Historical confidence (historical_context_calculator)
"""

import pytest
from helpers import make_full_sector_summary, make_sector_summary_row, make_timeseries_row

# ============================================================
# Group Divergence Detection (sector_rotation_calculator.py)
# ============================================================


class TestGroupDivergence:
    """Tests for _calculate_group_divergence and _analyze_group."""

    def test_high_std_dev_flags(self):
        """Cyclical group with std > 8pp triggers divergence."""
        from calculators.sector_rotation_calculator import _calculate_group_divergence

        summary = make_full_sector_summary(
            ratios={
                "Technology": 0.50,
                "Consumer Cyclical": 0.10,
                "Communication Services": 0.30,
                "Financial": 0.30,
                "Industrials": 0.30,
            }
        )
        sector_map = {s["Sector"]: s for s in summary}
        result = _calculate_group_divergence(sector_map)
        assert result["divergence_flag"] is True
        assert result["cyclical_divergence"]["flagged"] is True
        assert result["cyclical_divergence"]["std_dev"] > 0.08

    def test_high_spread_flags(self):
        """Group with max-min > 20pp triggers divergence."""
        from calculators.sector_rotation_calculator import _calculate_group_divergence

        summary = make_full_sector_summary(
            ratios={
                "Technology": 0.45,
                "Consumer Cyclical": 0.20,
                "Communication Services": 0.30,
                "Financial": 0.30,
                "Industrials": 0.30,
            }
        )
        sector_map = {s["Sector"]: s for s in summary}
        result = _calculate_group_divergence(sector_map)
        assert result["cyclical_divergence"]["spread"] > 0.20
        assert result["cyclical_divergence"]["flagged"] is True

    def test_trend_dissenter_flags(self):
        """Sector with opposing trend triggers divergence."""
        from calculators.sector_rotation_calculator import _calculate_group_divergence

        summary = make_full_sector_summary(
            ratios={
                "Technology": 0.30,
                "Consumer Cyclical": 0.28,
                "Communication Services": 0.29,
                "Financial": 0.27,
                "Industrials": 0.30,
            },
            trends={
                "Technology": "Up",
                "Consumer Cyclical": "Up",
                "Communication Services": "Up",
                "Financial": "Down",
                "Industrials": "Up",
            },
        )
        sector_map = {s["Sector"]: s for s in summary}
        result = _calculate_group_divergence(sector_map)
        assert result["cyclical_divergence"]["flagged"] is True
        assert len(result["cyclical_divergence"]["trend_dissenters"]) == 1
        assert result["cyclical_divergence"]["trend_dissenters"][0]["sector"] == "Financial"

    def test_no_divergence(self):
        """Uniform group does not flag."""
        from calculators.sector_rotation_calculator import _calculate_group_divergence

        summary = make_full_sector_summary(
            ratios={
                "Technology": 0.30,
                "Consumer Cyclical": 0.29,
                "Communication Services": 0.30,
                "Financial": 0.31,
                "Industrials": 0.30,
                "Utilities": 0.20,
                "Consumer Defensive": 0.21,
                "Healthcare": 0.20,
                "Real Estate": 0.21,
            }
        )
        sector_map = {s["Sector"]: s for s in summary}
        result = _calculate_group_divergence(sector_map)
        assert result["divergence_flag"] is False

    def test_divergence_penalty(self):
        """Divergence flag applies -5 penalty."""
        from calculators.sector_rotation_calculator import _calculate_group_divergence

        summary = make_full_sector_summary(ratios={"Technology": 0.50, "Consumer Cyclical": 0.10})
        sector_map = {s["Sector"]: s for s in summary}
        result = _calculate_group_divergence(sector_map)
        assert result["divergence_flag"] is True
        assert result["divergence_penalty"] == -5

    def test_no_divergence_zero_penalty(self):
        """No divergence means zero penalty."""
        from calculators.sector_rotation_calculator import _calculate_group_divergence

        summary = make_full_sector_summary(
            ratios={
                "Technology": 0.30,
                "Consumer Cyclical": 0.30,
                "Communication Services": 0.30,
                "Financial": 0.30,
                "Industrials": 0.30,
                "Utilities": 0.20,
                "Consumer Defensive": 0.20,
                "Healthcare": 0.20,
                "Real Estate": 0.20,
            }
        )
        sector_map = {s["Sector"]: s for s in summary}
        result = _calculate_group_divergence(sector_map)
        assert result["divergence_penalty"] == 0

    def test_outlier_detection(self):
        """Outlier sectors are identified."""
        from calculators.sector_rotation_calculator import _analyze_group

        sector_map = {
            "Technology": make_sector_summary_row("Technology", ratio=0.50),
            "Consumer Cyclical": make_sector_summary_row("Consumer Cyclical", ratio=0.10),
            "Communication Services": make_sector_summary_row("Communication Services", ratio=0.30),
            "Financial": make_sector_summary_row("Financial", ratio=0.30),
            "Industrials": make_sector_summary_row("Industrials", ratio=0.30),
        }
        from calculators.sector_rotation_calculator import CYCLICAL_SECTORS

        result = _analyze_group(sector_map, CYCLICAL_SECTORS)
        outlier_names = [o["sector"] for o in result["outliers"]]
        assert "Technology" in outlier_names or "Consumer Cyclical" in outlier_names


# ============================================================
# Warning Penalties (scorer.py)
# ============================================================


class TestWarningPenalties:
    """Tests for _calculate_warning_penalties."""

    def test_single_late_cycle(self):
        from scorer import _calculate_warning_penalties

        result = _calculate_warning_penalties({"late_cycle": True})
        assert result["total_penalty"] == -5

    def test_single_high_spread(self):
        from scorer import _calculate_warning_penalties

        result = _calculate_warning_penalties({"high_spread": True})
        assert result["total_penalty"] == -3

    def test_single_divergence(self):
        from scorer import _calculate_warning_penalties

        result = _calculate_warning_penalties({"divergence": True})
        assert result["total_penalty"] == -3

    def test_multiple_warnings_with_discount(self):
        """Two or more warnings get multi-warning discount (+1)."""
        from scorer import _calculate_warning_penalties

        result = _calculate_warning_penalties({"late_cycle": True, "high_spread": True})
        # -5 + -3 + 1 = -7
        assert result["total_penalty"] == -7

    def test_all_three_warnings(self):
        from scorer import _calculate_warning_penalties

        result = _calculate_warning_penalties(
            {"late_cycle": True, "high_spread": True, "divergence": True}
        )
        # -5 + -3 + -3 + 1 = -10
        assert result["total_penalty"] == -10

    def test_no_warnings(self):
        from scorer import _calculate_warning_penalties

        result = _calculate_warning_penalties({})
        assert result["total_penalty"] == 0
        assert result["breakdown"] == []

    def test_penalty_applied_to_composite(self):
        """Composite score is reduced by penalty."""
        from scorer import calculate_composite_score

        scores = {
            "market_breadth": 80,
            "sector_participation": 80,
            "sector_rotation": 80,
            "momentum": 80,
            "historical_context": 80,
        }
        result = calculate_composite_score(scores, warning_flags={"late_cycle": True})
        assert result["composite_score_raw"] == 80.0
        assert result["warning_penalty"] == -5
        assert result["composite_score"] == 75.0

    def test_penalty_clamped_at_zero(self):
        """Penalty cannot make composite negative."""
        from scorer import calculate_composite_score

        scores = {
            "market_breadth": 2,
            "sector_participation": 2,
            "sector_rotation": 2,
            "momentum": 2,
            "historical_context": 2,
        }
        result = calculate_composite_score(
            scores, warning_flags={"late_cycle": True, "high_spread": True, "divergence": True}
        )
        assert result["composite_score"] >= 0


# ============================================================
# Zone Detail (scorer.py)
# ============================================================


class TestZoneDetail:
    """Tests for _interpret_zone_detail."""

    def test_strong_bull(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(85) == "Strong Bull"

    def test_bull_upper(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(75) == "Bull-Upper"

    def test_bull_lower(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(65) == "Bull-Lower"

    def test_neutral(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(50) == "Neutral"

    def test_cautious_upper(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(35) == "Cautious-Upper"

    def test_cautious_lower(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(25) == "Cautious-Lower"

    def test_bear(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(10) == "Bear"

    def test_boundary_80(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(80) == "Strong Bull"

    def test_boundary_70(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(70) == "Bull-Upper"

    def test_boundary_60(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(60) == "Bull-Lower"

    def test_boundary_40(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(40) == "Neutral"

    def test_boundary_30(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(30) == "Cautious-Upper"

    def test_boundary_20(self):
        from scorer import _interpret_zone_detail

        assert _interpret_zone_detail(20) == "Cautious-Lower"


# ============================================================
# Zone Proximity (scorer.py)
# ============================================================


class TestZoneProximity:
    """Tests for _calculate_zone_proximity."""

    def test_at_boundary(self):
        from scorer import _calculate_zone_proximity

        result = _calculate_zone_proximity(66)
        assert result["at_boundary"] is True
        assert result["nearest_boundary"] == 60
        assert result["distance"] == pytest.approx(6.0, abs=0.1)

    def test_not_at_boundary(self):
        from scorer import _calculate_zone_proximity

        result = _calculate_zone_proximity(50)
        assert result["at_boundary"] is True  # 50 is 10 from 40 and 10 from 60
        # Actually 50 is 10 from both 40 and 60, so at_boundary should be True

    def test_far_from_boundary(self):
        from scorer import _calculate_zone_proximity

        result = _calculate_zone_proximity(90)
        assert result["at_boundary"] is True  # 90 is 10 from 80
        assert result["nearest_boundary"] == 80

    def test_exactly_at_boundary(self):
        from scorer import _calculate_zone_proximity

        result = _calculate_zone_proximity(60)
        assert result["at_boundary"] is True
        assert result["distance"] == 0.0

    def test_well_below_boundary(self):
        from scorer import _calculate_zone_proximity

        result = _calculate_zone_proximity(5)
        assert result["nearest_boundary"] == 20
        assert result["at_boundary"] is False


# ============================================================
# EMA Smoothing (momentum_calculator.py)
# ============================================================


class TestEMA:
    """Tests for _ema function."""

    def test_empty_list(self):
        from calculators.momentum_calculator import _ema

        assert _ema([]) == []

    def test_single_value(self):
        from calculators.momentum_calculator import _ema

        assert _ema([5.0]) == [5.0]

    def test_three_period_ema(self):
        """EMA(3) with alpha=0.5: ema[0]=v[0], ema[i]=0.5*v[i]+0.5*ema[i-1]"""
        from calculators.momentum_calculator import _ema

        values = [1.0, 2.0, 3.0, 4.0]
        result = _ema(values, span=3)
        assert len(result) == 4
        # alpha = 2/(3+1) = 0.5
        assert result[0] == pytest.approx(1.0)
        assert result[1] == pytest.approx(0.5 * 2.0 + 0.5 * 1.0)  # 1.5
        assert result[2] == pytest.approx(0.5 * 3.0 + 0.5 * 1.5)  # 2.25
        assert result[3] == pytest.approx(0.5 * 4.0 + 0.5 * 2.25)  # 3.125

    def test_constant_values(self):
        """EMA of constant should return constant."""
        from calculators.momentum_calculator import _ema

        result = _ema([5.0, 5.0, 5.0, 5.0], span=3)
        for v in result:
            assert v == pytest.approx(5.0)


# ============================================================
# Smoothed Acceleration (momentum_calculator.py)
# ============================================================


class TestSmoothedAcceleration:
    """Tests for _score_acceleration_smoothed."""

    def test_insufficient_data(self):
        from calculators.momentum_calculator import _score_acceleration_smoothed

        score, value, label = _score_acceleration_smoothed([0.01, 0.02])
        assert score == 50
        assert label == "insufficient_data"

    def test_with_20_points_steady(self):
        from calculators.momentum_calculator import _score_acceleration_smoothed

        slopes = [0.01] * 20
        score, value, label = _score_acceleration_smoothed(slopes)
        assert label == "steady"
        assert score == 50

    def test_with_20_points_accelerating(self):
        from calculators.momentum_calculator import _score_acceleration_smoothed

        # First 10 values low, next 10 higher
        slopes = [0.001] * 10 + [0.010] * 10
        score, value, label = _score_acceleration_smoothed(slopes)
        assert label in ("accelerating", "strong_accelerating")
        assert score >= 75

    def test_fallback_to_5v5(self):
        """With 10-19 points, falls back to 5v5."""
        from calculators.momentum_calculator import _score_acceleration_smoothed

        slopes = [0.01] * 15
        score, value, label = _score_acceleration_smoothed(slopes)
        assert label == "steady"


# ============================================================
# Historical Confidence (historical_context_calculator.py)
# ============================================================


class TestHistoricalConfidence:
    """Tests for _assess_confidence."""

    def test_high_confidence(self):
        """1000+ points with both regimes."""
        from calculators.historical_context_calculator import _assess_confidence

        ratios = [i * 0.001 for i in range(1, 1001)]  # 0.001 to 1.0
        result = _assess_confidence(ratios)
        assert result["confidence_level"] == "High"
        assert result["sample_label"] == "full"

    def test_moderate_confidence(self):
        """500-999 points."""
        from calculators.historical_context_calculator import _assess_confidence

        ratios = [0.05 + i * 0.001 for i in range(650)]  # 0.05 to 0.70
        result = _assess_confidence(ratios)
        assert result["confidence_level"] in ("Moderate", "High")
        assert result["sample_label"] == "moderate"

    def test_low_confidence_small_sample(self):
        """<200 points with narrow range."""
        from calculators.historical_context_calculator import _assess_confidence

        ratios = [0.20 + i * 0.001 for i in range(100)]  # 0.20 to 0.30
        result = _assess_confidence(ratios)
        assert result["confidence_level"] in ("Low", "Very Low")
        assert result["sample_label"] == "minimal"

    def test_regime_coverage_both(self):
        """Data covers both bear (<10%) and bull (>40%)."""
        from calculators.historical_context_calculator import _assess_confidence

        ratios = [0.05, 0.10, 0.20, 0.30, 0.45]
        result = _assess_confidence(ratios)
        assert result["has_bear_data"] is True
        assert result["has_bull_data"] is True
        assert result["regime_coverage"] == "Both"

    def test_regime_coverage_partial(self):
        """Data covers only bull side."""
        from calculators.historical_context_calculator import _assess_confidence

        ratios = [0.20, 0.30, 0.40, 0.50]
        result = _assess_confidence(ratios)
        assert result["has_bear_data"] is False
        assert result["has_bull_data"] is True
        assert result["regime_coverage"] == "Partial"

    def test_regime_coverage_narrow(self):
        """Data in narrow range."""
        from calculators.historical_context_calculator import _assess_confidence

        ratios = [0.20, 0.22, 0.25, 0.28]
        result = _assess_confidence(ratios)
        assert result["has_bear_data"] is False
        assert result["has_bull_data"] is False
        assert result["regime_coverage"] == "Narrow"

    def test_confidence_in_full_calculation(self):
        """Confidence included in calculate_historical_context output."""
        from calculators.historical_context_calculator import calculate_historical_context

        ts = [
            make_timeseries_row(ratio=0.10 + i * 0.01, date=f"2026-01-{i + 1:02d}")
            for i in range(20)
        ]
        result = calculate_historical_context(ts)
        assert "confidence" in result
        assert result["confidence"]["confidence_level"] in ("Low", "Very Low", "Moderate")


# ============================================================
# Divergence Warning in Scorer
# ============================================================


class TestDivergenceWarning:
    """Tests for divergence flag in warning overlays."""

    def test_divergence_warning_generated(self):
        from scorer import _apply_warning_overlays

        zone_info = {
            "zone": "Bull",
            "color": "light_green",
            "exposure_guidance": "Normal Exposure (80-100%)",
            "guidance": "Test.",
            "actions": [],
        }
        result, _ = _apply_warning_overlays(zone_info, {"divergence": True})
        assert len(result) == 1
        assert result[0]["flag"] == "divergence"
        assert "DIVERGENCE" in result[0]["label"]

    def test_zone_detail_in_composite(self):
        """zone_detail field is present in composite output."""
        from scorer import calculate_composite_score

        scores = {
            "market_breadth": 65,
            "sector_participation": 65,
            "sector_rotation": 65,
            "momentum": 65,
            "historical_context": 65,
        }
        result = calculate_composite_score(scores)
        assert result["zone_detail"] == "Bull-Lower"
        assert result["zone"] == "Bull"
