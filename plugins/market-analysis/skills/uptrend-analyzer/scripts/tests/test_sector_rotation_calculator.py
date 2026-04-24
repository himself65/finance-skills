"""Tests for sector rotation calculator."""

import pytest
from calculators.sector_rotation_calculator import (
    COMMODITY_SECTORS,
    CYCLICAL_SECTORS,
    DEFENSIVE_SECTORS,
    _avg,
    _difference_to_score,
    _get_group_ratios,
    calculate_sector_rotation,
)
from helpers import make_sector_summary_row

# ── _get_group_ratios ───────────────────────────────────────────────


class TestGetGroupRatios:
    def test_get_group_ratios_normal(self):
        sector_map = {
            "Technology": {"Sector": "Technology", "Ratio": 0.35},
            "Consumer Cyclical": {"Sector": "Consumer Cyclical", "Ratio": 0.30},
            "Communication Services": {"Sector": "Communication Services", "Ratio": 0.28},
            "Financial": {"Sector": "Financial", "Ratio": 0.27},
            "Industrials": {"Sector": "Industrials", "Ratio": 0.32},
        }
        ratios = _get_group_ratios(sector_map, CYCLICAL_SECTORS)
        assert ratios == [0.35, 0.30, 0.28, 0.27, 0.32]

    def test_get_group_ratios_missing(self):
        sector_map = {
            "Technology": {"Sector": "Technology", "Ratio": 0.35},
            "Financial": {"Sector": "Financial", "Ratio": 0.27},
        }
        ratios = _get_group_ratios(sector_map, CYCLICAL_SECTORS)
        assert ratios == [0.35, 0.27]
        assert len(ratios) == 2


# ── _avg ────────────────────────────────────────────────────────────


class TestAvg:
    def test_avg_simple(self):
        assert _avg([10, 20, 30]) == pytest.approx(20.0)
        assert _avg([0.35, 0.30, 0.28, 0.27, 0.32]) == pytest.approx(0.304)


# ── _difference_to_score ────────────────────────────────────────────


class TestDifferenceToScore:
    def test_diff_strong_risk_on(self):
        # diff=0.20 -> 90 + (0.05/0.10)*10 = 95
        assert _difference_to_score(0.20) == pytest.approx(95.0, abs=1)

    def test_diff_risk_on(self):
        # diff=0.10 -> 70 + (0.05/0.10)*19 = 79.5
        assert _difference_to_score(0.10) == pytest.approx(79.5, abs=1)

    def test_diff_balanced_positive(self):
        # diff=0.03 -> 45 + (0.08/0.10)*24 = 64.2
        assert _difference_to_score(0.03) == pytest.approx(64.2, abs=1)

    def test_diff_balanced_zero(self):
        # diff=0.0 -> 45 + (0.05/0.10)*24 = 57
        assert _difference_to_score(0.0) == pytest.approx(57.0, abs=1)

    def test_diff_defensive_tilt(self):
        # diff=-0.10 -> 20 + (0.05/0.10)*24 = 32
        assert _difference_to_score(-0.10) == pytest.approx(32.0, abs=1)

    def test_diff_strong_risk_off(self):
        # diff=-0.20 -> 19 + (-0.05/0.10)*19 = 9.5
        assert _difference_to_score(-0.20) == pytest.approx(9.5, abs=1)


# ── Late cycle / commodity penalty ──────────────────────────────────


class TestLateCycleAndCommodityPenalty:
    def _make_summary(self, cyclical_ratio, defensive_ratio, commodity_ratio):
        """Build minimal sector summary with uniform ratios per group."""
        rows = []
        for s in CYCLICAL_SECTORS:
            rows.append(make_sector_summary_row(sector=s, ratio=cyclical_ratio))
        for s in DEFENSIVE_SECTORS:
            rows.append(make_sector_summary_row(sector=s, ratio=defensive_ratio))
        for s in COMMODITY_SECTORS:
            rows.append(make_sector_summary_row(sector=s, ratio=commodity_ratio))
        return rows

    def test_late_cycle_flag_triggered(self):
        # commodity (0.50) > cyclical (0.30) and defensive (0.20)
        summary = self._make_summary(0.30, 0.20, 0.50)
        result = calculate_sector_rotation(summary, {})
        assert result["late_cycle_flag"] is True

    def test_late_cycle_flag_not_triggered(self):
        # commodity (0.25) < cyclical (0.35)
        summary = self._make_summary(0.35, 0.20, 0.25)
        result = calculate_sector_rotation(summary, {})
        assert result["late_cycle_flag"] is False

    def test_commodity_penalty_small(self):
        # commodity=0.38 > cyclical=0.30, excess=0.08 <= 0.10, penalty=-5
        summary = self._make_summary(0.30, 0.20, 0.38)
        result = calculate_sector_rotation(summary, {})
        assert result["late_cycle_flag"] is True
        assert result["commodity_penalty"] == -5

    def test_commodity_penalty_large(self):
        # commodity=0.50 > cyclical=0.30, excess=0.20 > 0.10, penalty=-10
        summary = self._make_summary(0.30, 0.20, 0.50)
        result = calculate_sector_rotation(summary, {})
        assert result["late_cycle_flag"] is True
        assert result["commodity_penalty"] == -10

    def test_no_commodity_data(self):
        # No commodity sectors -> no penalty
        rows = []
        for s in CYCLICAL_SECTORS:
            rows.append(make_sector_summary_row(sector=s, ratio=0.35))
        for s in DEFENSIVE_SECTORS:
            rows.append(make_sector_summary_row(sector=s, ratio=0.20))
        result = calculate_sector_rotation(rows, {})
        assert result["late_cycle_flag"] is False
        assert result["commodity_penalty"] == 0


# ── Full calculation ────────────────────────────────────────────────


class TestFullCalculation:
    def test_full_calculation_risk_on(self):
        # Cyclical 0.40 vs Defensive 0.20 -> diff=0.20 -> base ~95
        rows = []
        for s in CYCLICAL_SECTORS:
            rows.append(make_sector_summary_row(sector=s, ratio=0.40))
        for s in DEFENSIVE_SECTORS:
            rows.append(make_sector_summary_row(sector=s, ratio=0.20))
        for s in COMMODITY_SECTORS:
            rows.append(make_sector_summary_row(sector=s, ratio=0.25))
        result = calculate_sector_rotation(rows, {})
        assert result["data_available"] is True
        assert result["score"] >= 85
        assert "RISK-ON" in result["signal"]

    def test_full_calculation_defensive(self):
        # Cyclical 0.15 vs Defensive 0.35 -> diff=-0.20 -> base ~9.5
        rows = []
        for s in CYCLICAL_SECTORS:
            rows.append(make_sector_summary_row(sector=s, ratio=0.15))
        for s in DEFENSIVE_SECTORS:
            rows.append(make_sector_summary_row(sector=s, ratio=0.35))
        for s in COMMODITY_SECTORS:
            rows.append(make_sector_summary_row(sector=s, ratio=0.10))
        result = calculate_sector_rotation(rows, {})
        assert result["data_available"] is True
        assert result["score"] <= 20
        assert "RISK-OFF" in result["signal"] or "DEFENSIVE" in result["signal"]

    def test_empty_data_neutral(self):
        result = calculate_sector_rotation([], {})
        assert result["score"] == 50
        assert result["data_available"] is False

    def test_missing_cyclical_or_defensive(self):
        # Only cyclical, no defensive -> incomplete
        rows = [make_sector_summary_row(sector=s, ratio=0.30) for s in CYCLICAL_SECTORS]
        result = calculate_sector_rotation(rows, {})
        assert result["score"] == 50
        assert result["data_available"] is False
