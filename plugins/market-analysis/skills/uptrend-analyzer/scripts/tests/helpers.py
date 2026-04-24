"""Importable test helpers for Uptrend Analyzer tests"""


def make_timeseries_row(
    ratio=0.30,
    ma_10=0.28,
    slope=0.002,
    trend="up",
    worksheet="all",
    date="2026-01-15",
    count=840,
    total=2800,
):
    """Create a timeseries data row."""
    return {
        "worksheet": worksheet,
        "date": date,
        "count": count,
        "total": total,
        "ratio": ratio,
        "ma_10": ma_10,
        "slope": slope,
        "trend": trend,
    }


def make_sector_summary_row(
    sector="Technology", ratio=0.30, ma_10=0.28, trend="Up", slope=0.002, status="Normal"
):
    """Create a sector summary row."""
    return {
        "Sector": sector,
        "Ratio": ratio,
        "10MA": ma_10,
        "Trend": trend,
        "Slope": slope,
        "Status": status,
    }


def make_full_sector_summary(ratios=None, trends=None):
    """Create a full 11-sector summary.

    Args:
        ratios: Optional dict of sector -> ratio overrides
        trends: Optional dict of sector -> trend overrides
    """
    sectors = [
        "Technology",
        "Consumer Cyclical",
        "Communication Services",
        "Financial",
        "Industrials",
        "Utilities",
        "Consumer Defensive",
        "Healthcare",
        "Real Estate",
        "Energy",
        "Basic Materials",
    ]
    default_ratios = {
        "Technology": 0.35,
        "Consumer Cyclical": 0.30,
        "Communication Services": 0.28,
        "Financial": 0.27,
        "Industrials": 0.32,
        "Utilities": 0.20,
        "Consumer Defensive": 0.22,
        "Healthcare": 0.25,
        "Real Estate": 0.18,
        "Energy": 0.24,
        "Basic Materials": 0.26,
    }
    if ratios:
        default_ratios.update(ratios)
    default_trends = {s: "Up" for s in sectors}
    if trends:
        default_trends.update(trends)

    rows = []
    for s in sectors:
        r = default_ratios.get(s, 0.25)
        t = default_trends.get(s, "Up")
        slope = 0.002 if t == "Up" else -0.002
        status = "Overbought" if r > 0.37 else "Oversold" if r < 0.097 else "Normal"
        rows.append(
            make_sector_summary_row(
                sector=s,
                ratio=r,
                ma_10=r - 0.01,
                trend=t,
                slope=slope,
                status=status,
            )
        )
    return rows


def make_all_timeseries(n=20, base_ratio=0.30, slope=0.001):
    """Create a list of 'all' timeseries rows with increasing ratios.

    Returns list sorted by date ascending (oldest first).
    """
    rows = []
    for i in range(n):
        ratio = base_ratio + slope * i
        ratio = max(0, min(1.0, ratio))
        ma_10 = ratio - 0.005
        rows.append(
            make_timeseries_row(
                ratio=round(ratio, 4),
                ma_10=round(ma_10, 4),
                slope=round(slope, 6),
                trend="up" if slope > 0 else "down",
                date=f"2026-01-{i + 1:02d}",
            )
        )
    return rows
