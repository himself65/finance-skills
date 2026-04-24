"""Tests for Breadth CSV Client (TraderMonty auto-fetch)."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import requests
from breadth_csv_client import fetch_breadth_200dma

# Sample CSV content matching TraderMonty's format
SAMPLE_CSV = (
    "Date,S&P500_Price,Breadth_Index_Raw,Breadth_Index_200MA,"
    "Breadth_Index_8MA,Breadth_200MA_Trend,Bearish_Signal,"
    "Is_Peak,Is_Trough,Is_Trough_8MA_Below_04\n"
    "2026-02-14,6100.50,0.6200,0.5800,0.6300,1,False,False,False,False\n"
    "2026-02-18,6150.25,0.6481,0.5850,0.6400,1,False,False,False,False\n"
)


def _mock_response(text, status_code=200):
    resp = MagicMock()
    resp.text = text
    resp.status_code = status_code
    resp.raise_for_status = MagicMock()
    return resp


class TestFetchBreadth200dma:
    @patch("breadth_csv_client.requests.get")
    def test_fetch_success_returns_value(self, mock_get):
        """Normal fetch returns a dict with value in 0-100 range."""
        mock_get.return_value = _mock_response(SAMPLE_CSV)
        result = fetch_breadth_200dma()
        assert result is not None
        assert 0 <= result["value"] <= 100
        assert result["source"] == "TraderMonty CSV"

    @patch("breadth_csv_client.requests.get")
    def test_fetch_scales_raw_to_percent(self, mock_get):
        """Breadth_Index_Raw=0.6481 should become value=64.81."""
        mock_get.return_value = _mock_response(SAMPLE_CSV)
        result = fetch_breadth_200dma()
        assert result["value"] == 64.81

    @patch("breadth_csv_client.requests.get")
    def test_fetch_returns_latest_date(self, mock_get):
        """Should return the date of the latest (last) row."""
        mock_get.return_value = _mock_response(SAMPLE_CSV)
        result = fetch_breadth_200dma()
        assert result["date"] == "2026-02-18"

    @patch("breadth_csv_client.requests.get")
    @patch("breadth_csv_client.datetime")
    def test_fetch_freshness_check(self, mock_dt, mock_get):
        """Data from today should be is_fresh=True."""
        mock_get.return_value = _mock_response(SAMPLE_CSV)
        mock_dt.strptime = datetime.strptime
        mock_dt.now.return_value = datetime(2026, 2, 18, 12, 0, 0)
        result = fetch_breadth_200dma()
        assert result["is_fresh"] is True
        assert result["days_old"] == 0

    @patch("breadth_csv_client.requests.get")
    def test_fetch_failure_returns_none(self, mock_get):
        """Network error should return None."""
        mock_get.side_effect = requests.ConnectionError("Connection refused")
        result = fetch_breadth_200dma()
        assert result is None

    @patch("breadth_csv_client.requests.get")
    def test_fetch_empty_csv_returns_none(self, mock_get):
        """CSV with only header (no data rows) should return None."""
        header_only = (
            "Date,S&P500_Price,Breadth_Index_Raw,Breadth_Index_200MA,"
            "Breadth_Index_8MA,Breadth_200MA_Trend,Bearish_Signal,"
            "Is_Peak,Is_Trough,Is_Trough_8MA_Below_04\n"
        )
        mock_get.return_value = _mock_response(header_only)
        result = fetch_breadth_200dma()
        assert result is None


class TestCheckDataFreshness:
    """Test _check_data_freshness function."""

    def test_future_date_returns_not_fresh(self):
        """Future date should return is_fresh=False, days_old=None."""
        from breadth_csv_client import _check_data_freshness

        # Use a date far in the future
        result = _check_data_freshness("2099-12-31")
        assert result["is_fresh"] is False
        assert result["days_old"] is None

    def test_invalid_date_returns_not_fresh(self):
        """Invalid date string should return is_fresh=False, days_old=None."""
        from breadth_csv_client import _check_data_freshness

        result = _check_data_freshness("not-a-date")
        assert result["is_fresh"] is False
        assert result["days_old"] is None
