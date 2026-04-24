"""Tests for data_fetcher helper functions and UptrendDataFetcher (mocked HTTP)."""

from unittest.mock import MagicMock, patch

import requests
from data_fetcher import (
    UptrendDataFetcher,
    _parse_sector_summary_row,
    _parse_timeseries_row,
    _safe_float,
    _safe_int,
    build_summary_from_timeseries,
)

# --- _safe_float ---


def test_safe_float_normal():
    assert _safe_float("0.123") == 0.123


def test_safe_float_int():
    assert _safe_float("42") == 42.0


def test_safe_float_empty():
    assert _safe_float("") is None


def test_safe_float_none():
    assert _safe_float(None) is None


def test_safe_float_invalid():
    assert _safe_float("abc") is None


# --- _safe_int ---


def test_safe_int_normal():
    assert _safe_int("42") == 42


def test_safe_int_float_input():
    assert _safe_int("42.7") == 42


def test_safe_int_empty():
    assert _safe_int("") is None


def test_safe_int_none():
    assert _safe_int(None) is None


def test_safe_int_invalid():
    assert _safe_int("xyz") is None


# --- _parse_timeseries_row ---


def test_parse_timeseries_row_valid():
    row = {
        "worksheet": "sec_technology",
        "date": "2026-01-15",
        "count": "120",
        "total": "400",
        "ratio": "0.300",
        "ma_10": "0.280",
        "slope": "0.0015",
        "trend": "up",
    }
    result = _parse_timeseries_row(row)
    assert result is not None
    assert result["worksheet"] == "sec_technology"
    assert result["date"] == "2026-01-15"
    assert result["count"] == 120
    assert result["total"] == 400
    assert result["ratio"] == 0.300
    assert result["ma_10"] == 0.280
    assert result["slope"] == 0.0015
    assert result["trend"] == "up"


def test_parse_timeseries_row_missing():
    row = {
        "worksheet": "all",
        "date": "2026-02-01",
        "count": "",
        "total": "",
        "ratio": "",
        "ma_10": "",
        "slope": "",
        "trend": "",
    }
    result = _parse_timeseries_row(row)
    assert result is not None
    assert result["worksheet"] == "all"
    assert result["date"] == "2026-02-01"
    assert result["count"] is None
    assert result["total"] is None
    assert result["ratio"] is None
    assert result["ma_10"] is None
    assert result["slope"] is None
    assert result["trend"] == ""


# --- _parse_sector_summary_row ---


def test_parse_sector_summary_row_valid():
    row = {
        "Sector": "Technology",
        "Ratio": "0.288",
        "10MA": "0.266",
        "Trend": "Up",
        "Slope": "0.0020",
        "Status": "Normal",
    }
    result = _parse_sector_summary_row(row)
    assert result is not None
    assert result["Sector"] == "Technology"
    assert result["Ratio"] == 0.288
    assert result["10MA"] == 0.266
    assert result["Trend"] == "Up"
    assert result["Slope"] == 0.0020
    assert result["Status"] == "Normal"


# --- build_summary_from_timeseries ---


def test_build_summary_overbought_oversold():
    sector_ts = {
        "sec_technology": {
            "ratio": 0.40,
            "ma_10": 0.38,
            "slope": 0.002,
            "trend": "up",
        },
        "sec_utilities": {
            "ratio": 0.05,
            "ma_10": 0.06,
            "slope": -0.001,
            "trend": "down",
        },
    }
    result = build_summary_from_timeseries(sector_ts)
    assert len(result) == 2

    by_sector = {r["Sector"]: r for r in result}

    tech = by_sector["Technology"]
    assert tech["Ratio"] == 0.40
    assert tech["10MA"] == 0.38
    assert tech["Slope"] == 0.002
    assert tech["Trend"] == "Up"
    assert tech["Status"] == "Overbought"

    util = by_sector["Utilities"]
    assert util["Ratio"] == 0.05
    assert util["10MA"] == 0.06
    assert util["Slope"] == -0.001
    assert util["Trend"] == "Down"
    assert util["Status"] == "Oversold"


# --- UptrendDataFetcher (mocked HTTP) ---

SAMPLE_CSV = (
    "worksheet,date,count,total,ratio,ma_10,slope,trend\n"
    "all,2026-01-15,840,2800,0.300,0.280,0.0015,up\n"
    "sec_technology,2026-01-15,120,400,0.300,0.280,0.0020,up\n"
)


class TestUptrendDataFetcherMocked:
    def _make_mock_response(self, text, status_code=200):
        mock_resp = MagicMock()
        mock_resp.text = text
        mock_resp.status_code = status_code
        mock_resp.raise_for_status = MagicMock()
        return mock_resp

    def test_successful_fetch_returns_parsed_rows(self):
        fetcher = UptrendDataFetcher()
        mock_resp = self._make_mock_response(SAMPLE_CSV)
        with patch.object(fetcher.session, "get", return_value=mock_resp):
            rows = fetcher.fetch_timeseries()
        assert len(rows) == 2
        assert rows[0]["worksheet"] == "all"
        assert rows[0]["ratio"] == 0.300
        assert rows[1]["worksheet"] == "sec_technology"

    def test_http_404_returns_empty_list(self):
        fetcher = UptrendDataFetcher()
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("404")
        with patch.object(fetcher.session, "get", return_value=mock_resp):
            rows = fetcher.fetch_timeseries()
        assert rows == []

    def test_timeout_returns_empty_list(self):
        fetcher = UptrendDataFetcher()
        with patch.object(
            fetcher.session,
            "get",
            side_effect=requests.exceptions.Timeout("timeout"),
        ):
            rows = fetcher.fetch_timeseries()
        assert rows == []

    def test_malformed_csv_no_exception(self):
        fetcher = UptrendDataFetcher()
        malformed = "not,a,valid,csv\nwith,bad,data,here\n"
        mock_resp = self._make_mock_response(malformed)
        with patch.object(fetcher.session, "get", return_value=mock_resp):
            rows = fetcher.fetch_timeseries()
        # Should not raise; rows may be empty or partial
        assert isinstance(rows, list)

    def test_caching_prevents_second_http_call(self):
        fetcher = UptrendDataFetcher()
        mock_resp = self._make_mock_response(SAMPLE_CSV)
        with patch.object(fetcher.session, "get", return_value=mock_resp) as mock_get:
            fetcher.fetch_timeseries()
            fetcher.fetch_timeseries()
            assert mock_get.call_count == 1


# --- build_summary_from_timeseries edge cases ---


def test_build_summary_empty_dict():
    """Empty input returns empty list."""
    result = build_summary_from_timeseries({})
    assert result == []


def test_build_summary_none_ratio():
    """None ratio maps to 'Normal' status."""
    sector_ts = {"sec_technology": {"ratio": None, "ma_10": 0.28, "slope": 0.002, "trend": "up"}}
    result = build_summary_from_timeseries(sector_ts)
    assert result[0]["Ratio"] is None
    assert result[0]["Status"] == "Normal"


def test_build_summary_unknown_worksheet():
    """Unknown worksheet key falls back to raw name."""
    sector_ts = {"custom_ws": {"ratio": 0.25, "ma_10": 0.24, "slope": 0.001, "trend": "up"}}
    result = build_summary_from_timeseries(sector_ts)
    assert result[0]["Sector"] == "custom_ws"
