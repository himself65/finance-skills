"""Tests for Data Freshness Management"""

from datetime import date, timedelta

from utils import count_business_days


def _expected_factor(biz_days: int) -> float:
    """Map business days to expected freshness factor."""
    if biz_days <= 1:
        return 1.0
    elif biz_days <= 3:
        return 0.95
    elif biz_days <= 7:
        return 0.85
    else:
        return 0.70


class TestDataFreshness:
    """Test data freshness computation."""

    def test_today_returns_1(self):
        """Data from today -> freshness factor 1.0."""
        from market_top_detector import compute_data_freshness

        today = date.today().isoformat()
        result = compute_data_freshness({"breadth_200dma_date": today})
        assert result["breadth_200dma"]["factor"] == 1.0

    def test_recent_data_factor(self):
        """Data from a few calendar days ago uses business day counting."""
        from market_top_detector import compute_data_freshness

        d = date.today() - timedelta(days=2)
        result = compute_data_freshness({"breadth_200dma_date": d.isoformat()})
        biz = count_business_days(d, date.today())
        assert result["breadth_200dma"]["factor"] == _expected_factor(biz)

    def test_week_old_data_factor(self):
        """Data from ~1 week ago uses business day counting."""
        from market_top_detector import compute_data_freshness

        d = date.today() - timedelta(days=5)
        result = compute_data_freshness({"breadth_200dma_date": d.isoformat()})
        biz = count_business_days(d, date.today())
        assert result["breadth_200dma"]["factor"] == _expected_factor(biz)

    def test_old_data_returns_070(self):
        """Data from many calendar days ago -> 0.70 (business days > 7)."""
        from market_top_detector import compute_data_freshness

        # 20 calendar days guarantees 14+ business days -> factor 0.70
        d = (date.today() - timedelta(days=20)).isoformat()
        result = compute_data_freshness({"breadth_200dma_date": d})
        assert result["breadth_200dma"]["factor"] == 0.70

    def test_no_date_returns_1(self):
        """No date provided -> assume fresh (1.0)."""
        from market_top_detector import compute_data_freshness

        result = compute_data_freshness({})
        assert result["overall_confidence"] == 1.0

    def test_no_value_returns_none(self):
        """Date given but no value -> entry should still compute."""
        from market_top_detector import compute_data_freshness

        d = date.today().isoformat()
        result = compute_data_freshness({"put_call_date": d})
        assert result["put_call"]["factor"] == 1.0

    def test_overall_confidence_is_min(self):
        """Overall confidence = min of all provided factors."""
        from market_top_detector import compute_data_freshness

        today = date.today().isoformat()
        # 20 calendar days -> 14+ business days -> factor 0.70
        old = (date.today() - timedelta(days=20)).isoformat()
        result = compute_data_freshness(
            {
                "breadth_200dma_date": today,
                "put_call_date": old,
            }
        )
        assert result["overall_confidence"] == 0.70

    def test_future_date_returns_070(self):
        """Future date should be treated as anomaly with factor 0.70."""
        from market_top_detector import compute_data_freshness

        future = (date.today() + timedelta(days=5)).isoformat()
        result = compute_data_freshness({"breadth_200dma_date": future})
        assert result["breadth_200dma"]["factor"] == 0.70
        assert result["breadth_200dma"]["age_days"] is None

    def test_weekend_tolerance(self):
        """Friday data should still be fresh on Monday (1 business day).

        Instead of mocking date, we test the underlying count_business_days
        that compute_data_freshness now uses.
        """
        from utils import count_business_days

        friday = date(2026, 3, 13)  # Friday
        monday = date(2026, 3, 16)  # Monday
        biz_days = count_business_days(friday, monday)
        # 1 business day -> factor would be 1.0 (<=1 threshold)
        assert biz_days == 1
