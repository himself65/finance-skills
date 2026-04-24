"""Tests for shared utilities."""

from datetime import date

from utils import count_business_days


class TestCountBusinessDays:
    """Test business day counting."""

    def test_same_day(self):
        """Same day -> 0 business days."""
        d = date(2026, 3, 16)  # Monday
        assert count_business_days(d, d) == 0

    def test_fri_to_mon(self):
        """Friday to Monday = 1 business day."""
        fri = date(2026, 3, 13)  # Friday
        mon = date(2026, 3, 16)  # Monday
        assert count_business_days(fri, mon) == 1

    def test_fri_to_wed(self):
        """Friday to Wednesday = 3 business days."""
        fri = date(2026, 3, 13)  # Friday
        wed = date(2026, 3, 18)  # Wednesday
        assert count_business_days(fri, wed) == 3

    def test_mon_to_fri(self):
        """Monday to Friday = 4 business days."""
        mon = date(2026, 3, 16)  # Monday
        fri = date(2026, 3, 20)  # Friday
        assert count_business_days(mon, fri) == 4

    def test_future_returns_negative_one(self):
        """start > end -> returns -1."""
        future = date(2026, 3, 20)
        past = date(2026, 3, 16)
        assert count_business_days(future, past) == -1

    def test_full_week(self):
        """Monday to next Monday = 5 business days."""
        mon1 = date(2026, 3, 16)  # Monday
        mon2 = date(2026, 3, 23)  # Next Monday
        assert count_business_days(mon1, mon2) == 5

    def test_weekend_only(self):
        """Saturday to Sunday = 0 business days."""
        sat = date(2026, 3, 14)  # Saturday
        sun = date(2026, 3, 15)  # Sunday
        assert count_business_days(sat, sun) == 0
