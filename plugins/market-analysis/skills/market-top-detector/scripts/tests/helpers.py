"""Importable test helpers for Market Top Detector tests"""


def make_daily_bar(close, volume=1000000, date="2026-01-15", open_=None, high=None, low=None):
    """Helper to create a daily OHLCV bar dict."""
    if open_ is None:
        open_ = close
    if high is None:
        high = close * 1.005
    if low is None:
        low = close * 0.995
    return {
        "date": date,
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "adjClose": close,
        "volume": volume,
    }


def make_history(closes, base_volume=1000000, start_date="2026-01-15"):
    """Create a list of daily bars from a list of closes (most recent first)."""
    bars = []
    for i, close in enumerate(closes):
        vol = base_volume + (i * 1000)  # Slight volume variation
        bars.append(
            make_daily_bar(
                close=close,
                volume=vol,
                date=f"day-{i}",
            )
        )
    return bars


def make_history_with_volumes(close_volume_pairs, start_date="2026-01-15"):
    """Create bars from list of (close, volume) tuples (most recent first)."""
    bars = []
    for i, (close, volume) in enumerate(close_volume_pairs):
        bars.append(
            make_daily_bar(
                close=close,
                volume=volume,
                date=f"day-{i}",
            )
        )
    return bars
