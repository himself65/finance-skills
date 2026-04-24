#!/usr/bin/env python3
"""
Uptrend Analyzer - CSV Data Fetcher

Downloads and parses Monty's Uptrend Ratio Dashboard CSV data from GitHub.
No API key required - uses publicly available CSV files.

Data Sources:
- Timeseries: uptrend_ratio_timeseries.csv (all + 11 sectors, 2023/08~present)
- Sector Summary: sector_summary.csv (latest snapshot)
"""

import csv
import io
import sys
from typing import Optional

import requests

TIMESERIES_URL = (
    "https://raw.githubusercontent.com/tradermonty/uptrend-dashboard/"
    "main/data/uptrend_ratio_timeseries.csv"
)
SECTOR_SUMMARY_URL = (
    "https://raw.githubusercontent.com/tradermonty/uptrend-dashboard/main/data/sector_summary.csv"
)


WORKSHEET_TO_DISPLAY = {
    "sec_basicmaterials": "Basic Materials",
    "sec_communicationservices": "Communication Services",
    "sec_consumercyclical": "Consumer Cyclical",
    "sec_consumerdefensive": "Consumer Defensive",
    "sec_energy": "Energy",
    "sec_financial": "Financial",
    "sec_healthcare": "Healthcare",
    "sec_industrials": "Industrials",
    "sec_realestate": "Real Estate",
    "sec_technology": "Technology",
    "sec_utilities": "Utilities",
}

# Monty's official dashboard thresholds (same as in sector_participation_calculator)
OVERBOUGHT_THRESHOLD = 0.37
OVERSOLD_THRESHOLD = 0.097


def build_summary_from_timeseries(sector_timeseries: dict[str, dict]) -> list[dict]:
    """Build sector_summary-compatible list from timeseries latest rows.

    Used as fallback when sector_summary.csv is unavailable.

    Args:
        sector_timeseries: Dict mapping worksheet name -> latest timeseries row
            e.g. {"sec_technology": {"ratio": 0.288, "ma_10": 0.266, ...}}

    Returns:
        List of dicts matching sector_summary format:
            [{"Sector": "Technology", "Ratio": 0.288, "10MA": 0.266, ...}]
    """
    rows = []
    for ws_name, row in sector_timeseries.items():
        display_name = WORKSHEET_TO_DISPLAY.get(ws_name, ws_name)
        ratio = row.get("ratio")
        status = (
            "Overbought"
            if ratio is not None and ratio > OVERBOUGHT_THRESHOLD
            else "Oversold"
            if ratio is not None and ratio < OVERSOLD_THRESHOLD
            else "Normal"
        )
        rows.append(
            {
                "Sector": display_name,
                "Ratio": ratio,
                "10MA": row.get("ma_10"),
                "Trend": (row.get("trend") or "").capitalize(),
                "Slope": row.get("slope"),
                "Status": status,
                "Count": row.get("count"),
                "Total": row.get("total"),
            }
        )
    return rows


class UptrendDataFetcher:
    """Client for Monty's Uptrend Ratio Dashboard CSV data"""

    def __init__(self):
        self.session = requests.Session()
        self._timeseries_cache: Optional[list[dict]] = None
        self._sector_summary_cache: Optional[list[dict]] = None

    def fetch_timeseries(self) -> list[dict]:
        """Download and parse the timeseries CSV.

        Returns:
            List of dicts with keys: worksheet, date, count, total, ratio,
            ma_10, slope, trend. Numeric fields cast to float/int.
        """
        if self._timeseries_cache is not None:
            return self._timeseries_cache

        try:
            response = self.session.get(TIMESERIES_URL, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"WARNING: Failed to fetch timeseries CSV: {e}", file=sys.stderr)
            return []

        rows = []
        reader = csv.DictReader(io.StringIO(response.text))
        for row in reader:
            parsed = _parse_timeseries_row(row)
            if parsed:
                rows.append(parsed)

        self._timeseries_cache = rows
        return rows

    def fetch_sector_summary(self) -> list[dict]:
        """Download and parse the sector summary CSV.

        Returns:
            List of dicts with keys: Sector, Ratio, 10MA, Trend, Slope, Status.
            Numeric fields cast to float.
        """
        if self._sector_summary_cache is not None:
            return self._sector_summary_cache

        try:
            response = self.session.get(SECTOR_SUMMARY_URL, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"WARNING: Failed to fetch sector summary CSV: {e}", file=sys.stderr)
            return []

        rows = []
        reader = csv.DictReader(io.StringIO(response.text))
        for row in reader:
            parsed = _parse_sector_summary_row(row)
            if parsed:
                rows.append(parsed)

        self._sector_summary_cache = rows
        return rows

    def get_all_timeseries(self) -> list[dict]:
        """Get timeseries filtered to worksheet=='all', sorted by date ascending."""
        data = self.fetch_timeseries()
        filtered = [r for r in data if r["worksheet"] == "all"]
        filtered.sort(key=lambda r: r["date"])
        return filtered

    def get_sector_timeseries(self, sector: str) -> list[dict]:
        """Get timeseries for a specific sector worksheet, sorted by date ascending."""
        data = self.fetch_timeseries()
        filtered = [r for r in data if r["worksheet"] == sector]
        filtered.sort(key=lambda r: r["date"])
        return filtered

    def get_latest_all(self) -> Optional[dict]:
        """Get the most recent 'all' row."""
        ts = self.get_all_timeseries()
        return ts[-1] if ts else None

    def get_all_sector_latest(self) -> dict[str, dict]:
        """Get latest row for each sector (excluding 'all').

        Returns:
            Dict mapping sector name -> latest timeseries row
        """
        data = self.fetch_timeseries()
        sectors: dict[str, dict] = {}
        for row in data:
            ws = row["worksheet"]
            if ws == "all":
                continue
            if ws not in sectors or row["date"] > sectors[ws]["date"]:
                sectors[ws] = row
        return sectors


def _parse_timeseries_row(row: dict) -> Optional[dict]:
    """Parse a timeseries CSV row, casting numeric fields."""
    try:
        return {
            "worksheet": row.get("worksheet", "").strip(),
            "date": row.get("date", "").strip(),
            "count": _safe_int(row.get("count")),
            "total": _safe_int(row.get("total")),
            "ratio": _safe_float(row.get("ratio")),
            "ma_10": _safe_float(row.get("ma_10")),
            "slope": _safe_float(row.get("slope")),
            "trend": row.get("trend", "").strip(),
        }
    except (ValueError, TypeError):
        return None


def _parse_sector_summary_row(row: dict) -> Optional[dict]:
    """Parse a sector summary CSV row, casting numeric fields."""
    try:
        return {
            "Sector": row.get("Sector", "").strip(),
            "Ratio": _safe_float(row.get("Ratio")),
            "10MA": _safe_float(row.get("10MA")),
            "Trend": row.get("Trend", "").strip(),
            "Slope": _safe_float(row.get("Slope")),
            "Status": row.get("Status", "").strip(),
        }
    except (ValueError, TypeError):
        return None


def _safe_float(value) -> Optional[float]:
    """Convert to float, return None if empty or invalid."""
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _safe_int(value) -> Optional[int]:
    """Convert to int, return None if empty or invalid."""
    if value is None or str(value).strip() == "":
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None
