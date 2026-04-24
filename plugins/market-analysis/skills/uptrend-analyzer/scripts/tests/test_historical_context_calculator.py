"""Tests for historical_context_calculator.py"""

import pytest
from calculators.historical_context_calculator import (
    _avg_last_n,
    calculate_historical_context,
)
from helpers import make_timeseries_row


def _make_ts(ratios):
    """Create timeseries from ratio list."""
    return [make_timeseries_row(ratio=r, date=f"2026-01-{i + 1:02d}") for i, r in enumerate(ratios)]


# --- _avg_last_n tests ---


def test_avg_last_n_normal():
    """10 values, n=5 -> average of last 5."""
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = _avg_last_n(values, 5)
    assert result == pytest.approx(8.0)  # (6+7+8+9+10)/5


def test_avg_last_n_fewer():
    """3 values, n=10 -> average of all 3."""
    values = [10, 20, 30]
    result = _avg_last_n(values, 10)
    assert result == pytest.approx(20.0)  # (10+20+30)/3


def test_avg_last_n_empty():
    """Empty list -> None."""
    result = _avg_last_n([], 5)
    assert result is None


# --- Percentile rank tests ---


def test_percentile_lowest():
    """Current value is the lowest -> percentile near 0."""
    # 10 values from 0.10 to 0.19 ascending; current (last) is 0.05
    ratios = [0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.05]
    result = calculate_historical_context(_make_ts(ratios))
    # 0.05 is below all others; below_count=0, equal_count=1
    # percentile = (0 + 1*0.5)/10 * 100 = 5.0
    assert result["percentile"] == pytest.approx(5.0, abs=0.1)
    assert result["score"] <= 10


def test_percentile_highest():
    """Current value is the highest -> percentile near 100."""
    ratios = [0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.50]
    result = calculate_historical_context(_make_ts(ratios))
    # 0.50 is above all others; below_count=9, equal_count=1
    # percentile = (9 + 1*0.5)/10 * 100 = 95.0
    assert result["percentile"] == pytest.approx(95.0, abs=0.1)
    assert result["score"] >= 90


def test_percentile_median():
    """Current value is in the middle -> percentile near 50."""
    ratios = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.50]
    result = calculate_historical_context(_make_ts(ratios))
    # current=0.50; below_count=4 (0.10,0.20,0.30,0.40); equal_count=2 (two 0.50s)
    # percentile = (4 + 2*0.5)/10 * 100 = 50.0
    assert result["percentile"] == pytest.approx(50.0, abs=0.1)


def test_percentile_with_duplicates():
    """Duplicates are handled correctly in percentile calculation."""
    ratios = [0.30, 0.30, 0.30, 0.30, 0.30]
    result = calculate_historical_context(_make_ts(ratios))
    # All equal: below_count=0, equal_count=5
    # percentile = (0 + 5*0.5)/5 * 100 = 50.0
    assert result["percentile"] == pytest.approx(50.0, abs=0.1)
    assert result["score"] == 50


# --- Statistics tests ---


def test_stats_min_max():
    """Min and max are correctly calculated."""
    ratios = [0.15, 0.45, 0.25, 0.35, 0.10, 0.50]
    result = calculate_historical_context(_make_ts(ratios))
    assert result["historical_min"] == pytest.approx(0.10, abs=0.0001)
    assert result["historical_max"] == pytest.approx(0.50, abs=0.0001)


def test_stats_median_odd():
    """Odd count of ratios -> median is middle element."""
    ratios = [0.10, 0.20, 0.30, 0.40, 0.50]
    result = calculate_historical_context(_make_ts(ratios))
    # sorted: [0.10, 0.20, 0.30, 0.40, 0.50], median = 0.30
    assert result["historical_median"] == pytest.approx(0.30, abs=0.0001)


def test_stats_median_even():
    """Even count of ratios -> median is average of two middle elements."""
    ratios = [0.10, 0.20, 0.40, 0.50]
    result = calculate_historical_context(_make_ts(ratios))
    # sorted: [0.10, 0.20, 0.40, 0.50], median = (0.20 + 0.40)/2 = 0.30
    assert result["historical_median"] == pytest.approx(0.30, abs=0.0001)


# --- Full calculation test ---


def test_full_calculation():
    """Full flow with 20+ data points returns all expected fields."""
    ratios = [0.10 + i * 0.02 for i in range(25)]
    result = calculate_historical_context(_make_ts(ratios))

    assert result["data_available"] is True
    assert result["data_points"] == 25
    assert 0 <= result["score"] <= 100
    assert result["percentile"] is not None
    assert result["current_ratio"] == pytest.approx(ratios[-1], abs=0.0001)
    assert result["historical_min"] is not None
    assert result["historical_max"] is not None
    assert result["historical_median"] is not None
    assert result["avg_30d"] is not None
    assert result["avg_90d"] is not None
    assert "signal" in result
    assert "date_range" in result


# --- Edge case tests ---


def test_empty_timeseries():
    """Empty list -> score=50, data_available=False."""
    result = calculate_historical_context([])
    assert result["score"] == 50
    assert result["data_available"] is False
    assert result["percentile"] is None
    assert result["current_ratio"] is None


def test_single_datapoint():
    """1 data point -> insufficient data."""
    result = calculate_historical_context(_make_ts([0.30]))
    assert result["score"] == 50
    assert result["data_available"] is False
    assert "INSUFFICIENT" in result["signal"]
    assert result["data_points"] == 1


def test_two_datapoints():
    """Minimum 2 points needed for valid calculation."""
    result = calculate_historical_context(_make_ts([0.20, 0.40]))
    assert result["data_available"] is True
    assert result["data_points"] == 2
    assert 0 <= result["score"] <= 100
    assert result["percentile"] is not None
