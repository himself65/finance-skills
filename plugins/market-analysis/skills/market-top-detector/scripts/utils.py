"""
Market Top Detector - Shared Utilities

Common helper functions used across multiple modules.
"""

from datetime import date, timedelta


def count_business_days(start_date: date, end_date: date) -> int:
    """Count business days between start (exclusive) and end (inclusive).

    Friday→Monday = 1 business day.
    Returns -1 if start_date > end_date (future date).
    """
    if start_date > end_date:
        return -1
    count = 0
    current = start_date
    while current < end_date:
        current += timedelta(days=1)
        if current.weekday() < 5:
            count += 1
    return count
