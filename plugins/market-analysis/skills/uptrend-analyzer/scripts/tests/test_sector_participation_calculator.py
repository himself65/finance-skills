"""Tests for sector_participation_calculator.py"""

import pytest
from calculators.sector_participation_calculator import (
    _score_spread,
    _score_uptrend_count,
    calculate_sector_participation,
)
from helpers import make_full_sector_summary

# ---------------------------------------------------------------------------
# _score_uptrend_count
# ---------------------------------------------------------------------------


def test_count_score_zero():
    """0 sectors in uptrend -> score 0."""
    assert _score_uptrend_count(0, 11) == 0


def test_count_score_one():
    """1 sector in uptrend -> score 0."""
    assert _score_uptrend_count(1, 11) == 0


def test_count_score_two():
    """2 sectors in uptrend -> score 20."""
    assert _score_uptrend_count(2, 11) == 20


def test_count_score_five():
    """5 sectors in uptrend -> score 40."""
    assert _score_uptrend_count(5, 11) == 40


def test_count_score_seven():
    """7 sectors in uptrend -> score 60."""
    assert _score_uptrend_count(7, 11) == 60


def test_count_score_nine():
    """9 sectors in uptrend -> score 80."""
    assert _score_uptrend_count(9, 11) == 80


def test_count_score_eleven():
    """11 sectors in uptrend -> score 100."""
    assert _score_uptrend_count(11, 11) == 100


def test_count_score_zero_total():
    """total_sectors=0 returns 50 (neutral fallback)."""
    assert _score_uptrend_count(0, 0) == 50


# ---------------------------------------------------------------------------
# _score_spread
# ---------------------------------------------------------------------------


def test_spread_uniform():
    """spread=0.10 (< 0.15) -> 100."""
    assert _score_spread(0.10) == pytest.approx(100, abs=1)


def test_spread_healthy():
    """spread=0.20 -> ~90."""
    assert _score_spread(0.20) == pytest.approx(90, abs=1)


def test_spread_moderate():
    """spread=0.30 -> ~70."""
    assert _score_spread(0.30) == pytest.approx(70, abs=1)


def test_spread_wide():
    """spread=0.40 -> ~45."""
    assert _score_spread(0.40) == pytest.approx(45, abs=1)


def test_spread_extreme():
    """spread=0.50 -> ~15."""
    assert _score_spread(0.50) == pytest.approx(15, abs=1)


def test_spread_very_extreme():
    """spread=0.60 -> 0 (clamped)."""
    assert _score_spread(0.60) == pytest.approx(0, abs=1)


# ---------------------------------------------------------------------------
# Overbought / oversold detection
# ---------------------------------------------------------------------------


def test_overbought_detection():
    """Sectors with ratio >= 0.37 are detected as overbought."""
    summary = make_full_sector_summary(ratios={"Technology": 0.45, "Industrials": 0.40})
    result = calculate_sector_participation(summary, {})
    assert result["overbought_count"] == 2
    assert "Technology" in result["overbought_sectors"]
    assert "Industrials" in result["overbought_sectors"]


def test_oversold_detection():
    """Sectors with ratio < 0.097 are detected as oversold."""
    summary = make_full_sector_summary(ratios={"Energy": 0.05, "Utilities": 0.08})
    result = calculate_sector_participation(summary, {})
    assert result["oversold_count"] == 2
    assert "Energy" in result["oversold_sectors"]
    assert "Utilities" in result["oversold_sectors"]


# ---------------------------------------------------------------------------
# Full calculation
# ---------------------------------------------------------------------------


def test_full_calculation():
    """Full flow with 11 sectors all uptrending.

    Default helper ratios: max=0.35, min=0.18, spread=0.17
    count_score = 100 (11 uptrending)
    spread_score = 100 - (0.17-0.15)/0.10*20 = 96
    composite = 100*0.60 + 96*0.40 = 98.4 -> 98
    """
    summary = make_full_sector_summary()
    result = calculate_sector_participation(summary, {})
    assert result["score"] == pytest.approx(98, abs=1)
    assert result["data_available"] is True
    assert result["uptrend_count"] == 11
    assert result["total_sectors"] == 11


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_empty_data_neutral():
    """Empty sector_summary and no timeseries -> neutral score 50."""
    result = calculate_sector_participation([], {})
    assert result["score"] == 50
    assert result["data_available"] is False


def test_fallback_from_timeseries():
    """When sector_summary is empty but timeseries available, fallback builds summary."""
    sector_ts = {
        "sec_technology": {
            "ratio": 0.35,
            "ma_10": 0.33,
            "trend": "up",
            "slope": 0.002,
        },
        "sec_financial": {
            "ratio": 0.28,
            "ma_10": 0.26,
            "trend": "up",
            "slope": 0.001,
        },
        "sec_energy": {
            "ratio": 0.20,
            "ma_10": 0.19,
            "trend": "down",
            "slope": -0.001,
        },
    }
    result = calculate_sector_participation([], sector_ts)
    assert result["data_available"] is True
    assert result["total_sectors"] == 3
    # 2 uptrending out of 3 -> count_score=20
    assert result["uptrend_count"] == 2
