"""Tests for market_breadth_calculator.py"""

import pytest
from calculators.market_breadth_calculator import _ratio_to_score, calculate_market_breadth
from helpers import make_all_timeseries, make_timeseries_row

# ---------------------------------------------------------------------------
# _ratio_to_score: Crisis band (< 0.097)
# ---------------------------------------------------------------------------


def test_ratio_to_score_crisis_zero():
    """ratio=0 maps to score=0."""
    assert _ratio_to_score(0) == pytest.approx(0, abs=1)


def test_ratio_to_score_crisis_below_lower():
    """ratio=0.05 maps to ~4.6 (crisis band, linear 0-9)."""
    assert _ratio_to_score(0.05) == pytest.approx(4.6, abs=1)


# ---------------------------------------------------------------------------
# _ratio_to_score: Weak band boundary (0.097)
# ---------------------------------------------------------------------------


def test_ratio_to_score_at_lower_threshold():
    """ratio=0.097 maps to 10 (bottom of weak band)."""
    assert _ratio_to_score(0.097) == pytest.approx(10, abs=1)


# ---------------------------------------------------------------------------
# _ratio_to_score: Weak band (0.097-0.25)
# ---------------------------------------------------------------------------


def test_ratio_to_score_weak_midpoint():
    """ratio=0.17 maps to ~24 (mid-weak band)."""
    assert _ratio_to_score(0.17) == pytest.approx(23.8, abs=1)


# ---------------------------------------------------------------------------
# _ratio_to_score: Neutral band (0.25-0.37)
# ---------------------------------------------------------------------------


def test_ratio_to_score_at_025():
    """ratio=0.25 maps to 40 (bottom of neutral band)."""
    assert _ratio_to_score(0.25) == pytest.approx(40, abs=1)


def test_ratio_to_score_neutral_midpoint():
    """ratio=0.31 maps to ~54.5 (mid-neutral band)."""
    assert _ratio_to_score(0.31) == pytest.approx(54.5, abs=1)


# ---------------------------------------------------------------------------
# _ratio_to_score: Bullish band (0.37-0.50)
# ---------------------------------------------------------------------------


def test_ratio_to_score_at_upper_threshold():
    """ratio=0.37 maps to 70 (bottom of bullish band)."""
    assert _ratio_to_score(0.37) == pytest.approx(70, abs=1)


def test_ratio_to_score_bullish_midpoint():
    """ratio=0.43 maps to ~78.8 (mid-bullish band)."""
    assert _ratio_to_score(0.43) == pytest.approx(78.8, abs=1)


# ---------------------------------------------------------------------------
# _ratio_to_score: Strong Bull band (>= 0.50)
# ---------------------------------------------------------------------------


def test_ratio_to_score_at_050():
    """ratio=0.50 maps to 90 (bottom of strong bull band)."""
    assert _ratio_to_score(0.50) == pytest.approx(90, abs=1)


def test_ratio_to_score_strong_bull():
    """ratio=0.55 maps to 95."""
    assert _ratio_to_score(0.55) == pytest.approx(95, abs=1)


def test_ratio_to_score_max_cap():
    """ratio=0.70 is capped at 100."""
    assert _ratio_to_score(0.70) == pytest.approx(100, abs=1)


# ---------------------------------------------------------------------------
# Trend adjustment in calculate_market_breadth
# ---------------------------------------------------------------------------


def test_trend_adjustment_up():
    """trend='up' with positive slope adds +5."""
    latest = make_timeseries_row(ratio=0.30, trend="up", slope=0.002)
    ts = make_all_timeseries(n=5, base_ratio=0.30, slope=0.001)
    result = calculate_market_breadth(latest, ts)
    base = _ratio_to_score(0.30)
    assert result["score"] == round(min(100, max(0, base + 5)))
    assert result["trend_adjustment"] == 5


def test_trend_adjustment_down():
    """trend='down' with negative slope subtracts -5."""
    latest = make_timeseries_row(ratio=0.30, trend="down", slope=-0.002)
    ts = make_all_timeseries(n=5, base_ratio=0.30, slope=-0.001)
    result = calculate_market_breadth(latest, ts)
    base = _ratio_to_score(0.30)
    assert result["score"] == round(min(100, max(0, base - 5)))
    assert result["trend_adjustment"] == -5


def test_trend_adjustment_none_slope():
    """trend='up' but slope=None gives no adjustment."""
    latest = make_timeseries_row(ratio=0.30, trend="up", slope=None)
    ts = make_all_timeseries(n=5, base_ratio=0.30)
    result = calculate_market_breadth(latest, ts)
    assert result["trend_adjustment"] == 0


def test_trend_adjustment_mismatch():
    """trend='up' but negative slope gives no adjustment."""
    latest = make_timeseries_row(ratio=0.30, trend="up", slope=-0.001)
    ts = make_all_timeseries(n=5, base_ratio=0.30)
    result = calculate_market_breadth(latest, ts)
    assert result["trend_adjustment"] == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_no_data_returns_neutral():
    """None input returns neutral score 50."""
    result = calculate_market_breadth(None, [])
    assert result["score"] == 50
    assert result["data_available"] is False


def test_full_calculation_bull():
    """Full calculation: ratio=0.40 with uptrend -> ~79."""
    latest = make_timeseries_row(ratio=0.40, trend="up", slope=0.003)
    ts = make_all_timeseries(n=10, base_ratio=0.38, slope=0.002)
    result = calculate_market_breadth(latest, ts)
    # base = 70 + (0.40 - 0.37) / (0.50 - 0.37) * 19 ≈ 74.4, +5 = 79.4 -> 79
    assert result["score"] == pytest.approx(79, abs=1)
    assert result["data_available"] is True
    assert result["trend"] == "up"


def test_score_clamped_0_100():
    """Score is clamped between 0 and 100 even with trend adjustment."""
    # Very high ratio + up trend: should cap at 100
    latest_high = make_timeseries_row(ratio=0.70, trend="up", slope=0.005)
    ts = make_all_timeseries(n=5, base_ratio=0.65)
    result_high = calculate_market_breadth(latest_high, ts)
    assert result_high["score"] <= 100

    # Very low ratio + down trend: should not go below 0
    latest_low = make_timeseries_row(ratio=0.0, trend="down", slope=-0.005)
    ts_low = make_all_timeseries(n=5, base_ratio=0.02, slope=-0.001)
    result_low = calculate_market_breadth(latest_low, ts_low)
    assert result_low["score"] >= 0
