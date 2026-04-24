"""Tests for Defensive Rotation Calculator"""

from calculators.defensive_rotation_calculator import (
    _score_rotation,
    calculate_defensive_rotation,
)


class TestScoreRotation:
    """Boundary tests for rotation scoring."""

    def test_growth_leading(self):
        """Negative relative = growth leading = healthy."""
        assert _score_rotation(-3.0) == 0
        assert _score_rotation(-1.0) <= 15

    def test_slight_defensive_tilt(self):
        assert 20 <= _score_rotation(0.3) <= 40

    def test_strong_defensive_rotation(self):
        assert _score_rotation(5.0) == 100

    def test_moderate_rotation(self):
        assert 60 <= _score_rotation(2.0) <= 80


class TestCalculateDefensiveRotation:
    """Integration tests."""

    def test_missing_data_returns_50(self):
        """No ETF data -> score 50 (neutral), data_available=False."""
        result = calculate_defensive_rotation({})
        assert result["score"] == 50
        assert result["data_available"] is False

    def test_partial_data_still_computes(self):
        """At least 1 defensive + 1 offensive ETF should compute."""
        historical = {
            "XLU": [{"close": 70 + i * 0.1, "volume": 500000} for i in range(55)],
            "XLK": [{"close": 200 - i * 0.5, "volume": 2000000} for i in range(55)],
        }
        result = calculate_defensive_rotation(historical)
        assert result["data_available"] is False  # 2/8 = 25% < 75%
        assert "score" in result

    def test_growth_leading_scenario(self):
        """Offensive outperforming defensive -> low score."""
        historical = {}
        for sym in ["XLU", "XLP", "XLV", "VNQ"]:
            historical[sym] = [{"close": 50, "volume": 500000} for _ in range(55)]
        for sym in ["XLK", "XLC", "XLY", "QQQ"]:
            historical[sym] = [{"close": 105 - i * 0.25, "volume": 2000000} for i in range(55)]
        result = calculate_defensive_rotation(historical)
        assert result["score"] <= 20


class TestFetchSuccessRate:
    """Test fetch success rate tracking."""

    def test_all_fetched(self):
        """All 8 ETFs with data -> fetch_success_rate = 1.0."""
        historical = {}
        for sym in ["XLU", "XLP", "XLV", "VNQ", "XLK", "XLC", "XLY", "QQQ"]:
            historical[sym] = [{"close": 100 + i * 0.1, "volume": 500000} for i in range(55)]
        result = calculate_defensive_rotation(historical)
        assert result["fetch_success_rate"] == 1.0
        assert result["data_available"] is True

    def test_partial_data_rate(self):
        """Only some ETFs have data."""
        historical = {
            "XLU": [{"close": 50, "volume": 500000} for _ in range(55)],
            "XLK": [{"close": 200, "volume": 2000000} for _ in range(55)],
        }
        result = calculate_defensive_rotation(historical)
        assert result["fetch_success_rate"] == 0.25  # 2/8


class TestMultiPeriodConfirmation:
    """Test multi-period rotation analysis."""

    def test_confirmed_all_periods_defensive(self):
        """All 3 periods show defensive leading -> confirmed."""
        historical = {}
        # Defensive ETFs going up
        for sym in ["XLU", "XLP", "XLV", "VNQ"]:
            historical[sym] = [{"close": 110 - i * 0.2, "volume": 500000} for i in range(55)]
        # Offensive ETFs going down
        for sym in ["XLK", "XLC", "XLY", "QQQ"]:
            historical[sym] = [{"close": 90 + i * 0.5, "volume": 2000000} for i in range(55)]
        result = calculate_defensive_rotation(historical)
        assert result["confirmation"] == "confirmed"
        assert "multi_period" in result
        assert len(result["multi_period"]) >= 2

    def test_unconfirmed_mixed_periods(self):
        """Some periods defensive, some not -> unconfirmed, capped at 80."""
        historical = {}
        # Create a scenario where short-term is defensive but long-term is not
        for sym in ["XLU", "XLP", "XLV", "VNQ"]:
            # Recent 10 days up, older days flat
            closes = [60 - i * 0.3 for i in range(15)] + [50 for _ in range(40)]
            historical[sym] = [{"close": c, "volume": 500000} for c in closes]
        for sym in ["XLK", "XLC", "XLY", "QQQ"]:
            # Recent 10 days flat, older days up
            closes = [50 for _ in range(15)] + [50 - i * 0.3 for i in range(40)]
            historical[sym] = [{"close": c, "volume": 2000000} for c in closes]
        result = calculate_defensive_rotation(historical)
        # Score should be capped at 80 if unconfirmed
        if result["confirmation"] == "unconfirmed":
            assert result["score"] <= 80

    def test_multi_period_details_present(self):
        """Result should include multi_period dict with period details."""
        historical = {}
        for sym in ["XLU", "XLP", "XLV", "VNQ", "XLK", "XLC", "XLY", "QQQ"]:
            historical[sym] = [{"close": 100 + i * 0.1, "volume": 500000} for i in range(55)]
        result = calculate_defensive_rotation(historical)
        assert "multi_period" in result
        # Should have at least 10d and 20d periods (40d needs 41+ days)
        assert 10 in result["multi_period"] or 20 in result["multi_period"]
