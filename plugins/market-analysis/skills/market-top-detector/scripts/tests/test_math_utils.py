"""Tests for EMA/SMA shared utilities"""

import pytest
from calculators.math_utils import calc_ema, calc_sma


class TestCalcEma:
    """Boundary and correctness tests for calc_ema."""

    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="prices must not be empty"):
            calc_ema([], 10)

    def test_period_zero_raises(self):
        with pytest.raises(ValueError, match="period must be >= 1"):
            calc_ema([100.0], 0)

    def test_period_negative_raises(self):
        with pytest.raises(ValueError, match="period must be >= 1"):
            calc_ema([100.0], -1)

    def test_period_one(self):
        """Period=1 EMA should approximate most recent price."""
        prices = [100.0, 90.0, 80.0]
        result = calc_ema(prices, 1)
        # With k=1.0 for period=1, EMA should be the last chronological value = 100.0
        assert abs(result - 100.0) < 0.01

    def test_period_exceeds_length(self):
        """period > len(prices) → simple average of all."""
        prices = [100.0, 110.0]
        result = calc_ema(prices, 10)
        assert abs(result - 105.0) < 0.01

    def test_known_ema_value(self):
        """Verify EMA calculation with known values."""
        # 5 prices (most recent first): 105, 104, 103, 102, 101
        # Chronological: 101, 102, 103, 104, 105
        # SMA(3) of first 3 = (101+102+103)/3 = 102.0
        # k = 2/(3+1) = 0.5
        # EMA after 104: 104*0.5 + 102*0.5 = 103.0
        # EMA after 105: 105*0.5 + 103*0.5 = 104.0
        prices = [105, 104, 103, 102, 101]
        result = calc_ema(prices, 3)
        assert abs(result - 104.0) < 0.01


class TestCalcSma:
    """Boundary and correctness tests for calc_sma."""

    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="prices must not be empty"):
            calc_sma([], 10)

    def test_period_zero_raises(self):
        with pytest.raises(ValueError, match="period must be >= 1"):
            calc_sma([100.0], 0)

    def test_period_negative_raises(self):
        with pytest.raises(ValueError, match="period must be >= 1"):
            calc_sma([100.0], -1)

    def test_period_one(self):
        """Period=1 SMA = most recent price."""
        prices = [100.0, 90.0, 80.0]
        result = calc_sma(prices, 1)
        assert result == 100.0

    def test_period_exceeds_length(self):
        """period > len(prices) → simple average of all."""
        prices = [100.0, 110.0]
        result = calc_sma(prices, 10)
        assert abs(result - 105.0) < 0.01

    def test_known_sma_value(self):
        """SMA of first N prices (most recent first)."""
        prices = [105, 104, 103, 102, 101]
        result = calc_sma(prices, 3)
        assert abs(result - (105 + 104 + 103) / 3) < 0.01
