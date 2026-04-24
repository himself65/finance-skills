"""Tests for momentum calculator."""

import pytest
from calculators.momentum_calculator import (
    _score_acceleration_from_values,
    _score_sector_slope_breadth,
    _score_slope,
    calculate_momentum,
)
from helpers import make_sector_summary_row

# ── _score_slope ────────────────────────────────────────────────────


class TestScoreSlope:
    def test_slope_strong_bullish(self):
        # 0.025 -> 95 + (0.005/0.01)*5 = 97.5
        assert _score_slope(0.025) == pytest.approx(97.5, abs=1)

    def test_slope_bullish(self):
        # 0.015 -> 75 + (0.005/0.01)*19 = 84.5
        assert _score_slope(0.015) == pytest.approx(84.5, abs=1)

    def test_slope_mild_positive(self):
        # 0.005 -> 55 + (0.005/0.01)*19 = 64.5
        assert _score_slope(0.005) == pytest.approx(64.5, abs=1)

    def test_slope_zero(self):
        # 0.0 -> 55
        assert _score_slope(0.0) == pytest.approx(55.0, abs=1)

    def test_slope_mild_negative(self):
        # -0.005 -> 35 + (0.005/0.01)*19 = 44.5
        assert _score_slope(-0.005) == pytest.approx(44.5, abs=1)

    def test_slope_bearish(self):
        # -0.015 -> 10 + (0.005/0.01)*24 = 22
        assert _score_slope(-0.015) == pytest.approx(22.0, abs=1)

    def test_slope_strong_bearish(self):
        # -0.025 -> 9 + (-0.005/0.01)*9 = 4.5
        assert _score_slope(-0.025) == pytest.approx(4.5, abs=1)


# ── _score_acceleration ────────────────────────────────────────────


class TestScoreAcceleration:
    def _make_slope_list(self, prior_slope, recent_slope, window=5):
        """Build flat slope list with distinct prior and recent values."""
        return [prior_slope] * window + [recent_slope] * window

    def test_accel_strong_accelerating(self):
        # recent_avg - prior_avg = 0.010 - 0.001 = 0.009 > 0.005
        slopes = self._make_slope_list(prior_slope=0.001, recent_slope=0.010)
        score, value, label = _score_acceleration_from_values(slopes, window=5)
        assert score == 90
        assert label == "strong_accelerating"
        assert value == pytest.approx(0.009, abs=0.001)

    def test_accel_accelerating(self):
        # recent_avg - prior_avg = 0.005 - 0.002 = 0.003 > 0.001
        slopes = self._make_slope_list(prior_slope=0.002, recent_slope=0.005)
        score, value, label = _score_acceleration_from_values(slopes, window=5)
        assert score == 75
        assert label == "accelerating"

    def test_accel_steady(self):
        # recent_avg - prior_avg = 0.003 - 0.003 = 0.0
        slopes = self._make_slope_list(prior_slope=0.003, recent_slope=0.003)
        score, value, label = _score_acceleration_from_values(slopes, window=5)
        assert score == 50
        assert label == "steady"

    def test_accel_decelerating(self):
        # recent_avg - prior_avg = 0.002 - 0.005 = -0.003
        slopes = self._make_slope_list(prior_slope=0.005, recent_slope=0.002)
        score, value, label = _score_acceleration_from_values(slopes, window=5)
        assert score == 25
        assert label == "decelerating"

    def test_accel_strong_decelerating(self):
        # recent_avg - prior_avg = 0.001 - 0.010 = -0.009 < -0.005
        slopes = self._make_slope_list(prior_slope=0.010, recent_slope=0.001)
        score, value, label = _score_acceleration_from_values(slopes, window=5)
        assert score == 10
        assert label == "strong_decelerating"

    def test_accel_insufficient_data(self):
        slopes = [0.002] * 5  # Only 5 points, need 10 for window=5
        score, value, label = _score_acceleration_from_values(slopes, window=5)
        assert score == 50
        assert value is None
        assert label == "insufficient_data"

    def test_accel_exact_boundary_window(self):
        """Exactly window*2 data points should calculate normally."""
        slopes = [0.002] * 5 + [0.005] * 5
        score, value, label = _score_acceleration_from_values(slopes, window=5)
        assert label == "accelerating"
        assert score == 75


# ── _score_sector_slope_breadth ─────────────────────────────────────


class TestSectorSlopeBreadth:
    def test_sector_breadth_all_positive(self):
        sectors = [
            "Technology",
            "Consumer Cyclical",
            "Communication Services",
            "Financial",
            "Industrials",
            "Utilities",
            "Consumer Defensive",
            "Healthcare",
            "Real Estate",
            "Energy",
            "Basic Materials",
        ]
        summary = [make_sector_summary_row(sector=s, slope=0.003) for s in sectors]
        score, positive, total = _score_sector_slope_breadth(summary)
        assert score == pytest.approx(100.0, abs=1)
        assert positive == 11
        assert total == 11

    def test_sector_breadth_none_positive(self):
        sectors = [
            "Technology",
            "Consumer Cyclical",
            "Communication Services",
            "Financial",
            "Industrials",
            "Utilities",
            "Consumer Defensive",
            "Healthcare",
            "Real Estate",
            "Energy",
            "Basic Materials",
        ]
        summary = [make_sector_summary_row(sector=s, slope=-0.003) for s in sectors]
        score, positive, total = _score_sector_slope_breadth(summary)
        assert score == pytest.approx(0.0, abs=1)
        assert positive == 0

    def test_sector_breadth_half(self):
        summary = []
        for i in range(5):
            summary.append(make_sector_summary_row(sector=f"Pos{i}", slope=0.003))
        for i in range(5):
            summary.append(make_sector_summary_row(sector=f"Neg{i}", slope=-0.003))
        score, positive, total = _score_sector_slope_breadth(summary)
        assert score == pytest.approx(50.0, abs=1)
        assert positive == 5
        assert total == 10


# ── Full momentum calculation ──────────────────────────────────────


class TestFullMomentum:
    def test_full_momentum_no_data(self):
        result = calculate_momentum([], [])
        assert result["score"] == 50
        assert result["data_available"] is False
        assert result["slope"] is None
