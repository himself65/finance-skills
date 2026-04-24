"""Tests for Index Technical Calculator"""

from calculators.index_technical_calculator import (
    _evaluate_index,
    calculate_index_technical,
)
from helpers import make_history


class TestEvaluateIndex:
    """Test single index evaluation."""

    def test_insufficient_data(self):
        """Less than 21 days → data_available=False."""
        result = _evaluate_index("TEST", [{"close": 100}] * 10)
        assert result["data_available"] is False
        assert result["raw_score"] == 0

    def test_sufficient_data(self):
        """21+ days → data_available=True."""
        history = make_history([100 - i * 0.1 for i in range(50)])
        result = _evaluate_index("TEST", history)
        assert result["data_available"] is True

    def test_below_21ema_adds_8(self):
        """Price significantly below 21 EMA should trigger flag."""
        # Create downtrend: recent prices well below earlier ones
        closes = [90] * 5 + [100 + i * 0.5 for i in range(45)]
        history = make_history(closes)
        result = _evaluate_index("TEST", history)
        assert any("21 EMA" in f for f in result["flags"])


class TestCalculateIndexTechnical:
    """Test composite index technical score."""

    def test_both_available(self):
        """Both S&P and NASDAQ have data → average them."""
        sp = make_history([100 - i * 0.1 for i in range(50)])
        nq = make_history([200 - i * 0.2 for i in range(50)])
        result = calculate_index_technical(sp, nq)
        assert result["data_available"] is True
        assert result["sp500"]["data_available"] is True
        assert result["nasdaq"]["data_available"] is True

    def test_nasdaq_missing_uses_sp_only(self):
        """NASDAQ insufficient data → use S&P 500 only, no halving."""
        sp = make_history([100 - i * 0.1 for i in range(50)])
        nq_short = [{"close": 200}] * 5  # Too short

        calculate_index_technical(sp, sp)  # Both = S&P (warm up)
        result_sp_only = calculate_index_technical(sp, nq_short)

        # S&P-only score should equal S&P's raw_score (not halved)
        sp_raw = result_sp_only["sp500"]["raw_score"]
        assert result_sp_only["score"] == round(min(100, max(0, sp_raw)))
        assert result_sp_only["nasdaq"]["data_available"] is False

    def test_both_missing_returns_50(self):
        """Both insufficient → score=50, data_available=False."""
        short = [{"close": 100}] * 5
        result = calculate_index_technical(short, short)
        assert result["score"] == 50
        assert result["data_available"] is False
        assert "NO DATA" in result["signal"]

    def test_sp_missing_nasdaq_available(self):
        """S&P insufficient, NASDAQ available → use NASDAQ only."""
        sp_short = [{"close": 100}] * 5
        nq = make_history([200 - i * 0.2 for i in range(50)])
        result = calculate_index_technical(sp_short, nq)
        nq_raw = result["nasdaq"]["raw_score"]
        assert result["score"] == round(min(100, max(0, nq_raw)))
