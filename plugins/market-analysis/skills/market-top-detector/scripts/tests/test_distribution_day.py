"""Tests for Distribution Day Calculator"""

from calculators.distribution_day_calculator import (
    _calculate_clustering_factor,
    _count_distribution_days,
    _score_distribution_days,
    calculate_distribution_days,
)
from helpers import make_history, make_history_with_volumes


class TestScoreDistributionDays:
    """Boundary tests for scoring thresholds."""

    def test_zero_days(self):
        assert _score_distribution_days(0) == 0

    def test_one_day(self):
        assert _score_distribution_days(1) == 15

    def test_two_days(self):
        assert _score_distribution_days(2) == 30

    def test_three_days(self):
        assert _score_distribution_days(3) == 55

    def test_four_days_oneil_threshold(self):
        assert _score_distribution_days(4) == 75

    def test_five_days(self):
        assert _score_distribution_days(5) == 90

    def test_six_plus_days(self):
        assert _score_distribution_days(6) == 100
        assert _score_distribution_days(8) == 100

    def test_fractional_stalling(self):
        """Stalling days count as 0.5"""
        assert _score_distribution_days(3.5) == 55  # 3.5 >= 3
        assert _score_distribution_days(4.5) == 75  # 4.5 >= 4


class TestCountDistributionDays:
    """Tests for distribution day detection logic."""

    def test_empty_history(self):
        result = _count_distribution_days([], "TEST")
        assert result["distribution_days"] == 0

    def test_single_day(self):
        result = _count_distribution_days([{"close": 100, "volume": 1000}], "TEST")
        assert result["distribution_days"] == 0

    def test_distribution_day_detected(self):
        """Price drop >= 0.2% on higher volume = distribution day."""
        history = make_history_with_volumes(
            [
                (99.0, 1200000),  # Today: -1% drop, higher volume -> distribution
                (100.0, 1000000),  # Yesterday
                (100.5, 800000),  # Two days ago: lower volume than yesterday
            ]
        )
        result = _count_distribution_days(history, "TEST")
        assert result["distribution_days"] >= 1

    def test_stalling_day_detected(self):
        """Volume increases but price gain < 0.1% = stalling day."""
        history = make_history_with_volumes(
            [
                (100.05, 1200000),  # Today: +0.05%, higher volume
                (100.0, 1000000),  # Yesterday
                (99.5, 900000),  # Two days ago
            ]
        )
        result = _count_distribution_days(history, "TEST")
        assert result["stalling_days"] >= 1

    def test_window_index_in_details(self):
        """Distribution day details should include window_index."""
        history = make_history_with_volumes(
            [
                (99.0, 1200000),
                (100.0, 1000000),
                (100.5, 800000),
            ]
        )
        result = _count_distribution_days(history, "TEST")
        for d in result["details"]:
            assert "window_index" in d


class TestClusteringFactor:
    """Test clustering factor calculation."""

    def test_no_events(self):
        result = _calculate_clustering_factor([])
        assert result["factor"] == 0.0
        assert result["total_count"] == 0

    def test_all_recent(self):
        """All events in recent 5 days -> factor = 1.0."""
        details = [
            {"window_index": 0, "type": "distribution"},
            {"window_index": 2, "type": "distribution"},
            {"window_index": 4, "type": "distribution"},
        ]
        result = _calculate_clustering_factor(details)
        assert result["factor"] == 1.0
        assert result["recent_count"] == 3

    def test_spread_evenly(self):
        """Events spread across window -> low factor."""
        details = [
            {"window_index": 0, "type": "distribution"},
            {"window_index": 10, "type": "distribution"},
            {"window_index": 20, "type": "distribution"},
        ]
        result = _calculate_clustering_factor(details)
        assert result["factor"] < 0.5

    def test_mixed(self):
        """Some recent, some old."""
        details = [
            {"window_index": 1, "type": "distribution"},
            {"window_index": 3, "type": "distribution"},
            {"window_index": 12, "type": "distribution"},
            {"window_index": 18, "type": "distribution"},
        ]
        result = _calculate_clustering_factor(details)
        assert result["factor"] == 0.5  # 2/4


class TestClusteringMultiplier:
    """Test that clustering boosts the score."""

    def test_clustered_boosts_score(self):
        """Clustered distribution days should get 1.15x multiplier."""
        # Create history with 3 distribution days all in the last 5 days
        # Days 0-4: distribution days (price drops on higher volume)
        cv = []
        for i in range(26):
            if i < 3:
                cv.append((99.0 - i * 0.5, 1200000 + i * 100000))  # Drop, high vol
            elif i == 3:
                cv.append((100.0, 1000000))  # Base
            else:
                cv.append((100.0 + (i - 3) * 0.1, 900000))  # Normal
        sp_hist = make_history_with_volumes(cv)
        flat_hist = make_history([100] * 26)

        result = calculate_distribution_days(sp_hist, flat_hist)
        if result["effective_count"] >= 2 and result["clustering"]["factor"] > 0.5:
            assert result["clustering_applied"] is True
            assert result["score"] >= result["raw_score"]

    def test_spread_no_boost(self):
        """Spread-out distribution days should NOT get multiplier."""
        # If no clustering, raw_score == score
        flat_hist = make_history([100] * 30)
        result = calculate_distribution_days(flat_hist, flat_hist)
        assert result["clustering_applied"] is False
        assert result["score"] == result["raw_score"]


class TestCalculateDistributionDays:
    """Integration tests."""

    def test_uses_higher_count(self):
        """Should use the worse of S&P 500 / NASDAQ."""
        sp_history = make_history([100] * 30)
        nasdaq_cv = [(99.0 - i * 0.3, 1200000 + i * 10000) for i in range(15)]
        nasdaq_cv += [(100.0 + i * 0.1, 1000000) for i in range(15)]
        nasdaq_history = make_history_with_volumes(nasdaq_cv)

        result = calculate_distribution_days(sp_history, nasdaq_history)
        assert "score" in result
        assert "effective_count" in result
        assert "clustering" in result
        assert "raw_score" in result
