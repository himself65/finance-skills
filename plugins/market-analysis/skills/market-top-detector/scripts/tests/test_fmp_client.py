"""Tests for FMP Client VIX term structure auto-detection and endpoint fallback"""

import os
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestVixTermStructure:
    """Test VIX term structure auto-classification."""

    def _make_client(self):
        """Create a mock FMPClient without real API key."""
        with patch.dict(os.environ, {"FMP_API_KEY": "test_key"}):
            from fmp_client import FMPClient

            client = FMPClient(api_key="test_key")
        return client

    def test_steep_contango(self):
        """VIX/VIX3M < 0.85 -> steep_contango."""
        client = self._make_client()
        client.get_quote = MagicMock(
            side_effect=lambda s: [{"price": 12.0}] if "VIX3M" not in s else [{"price": 16.0}]
        )
        result = client.get_vix_term_structure()
        assert result is not None
        assert result["classification"] == "steep_contango"
        assert result["ratio"] < 0.85

    def test_contango(self):
        """VIX/VIX3M 0.85-0.95 -> contango."""
        client = self._make_client()
        client.get_quote = MagicMock(
            side_effect=lambda s: [{"price": 14.0}] if "VIX3M" not in s else [{"price": 15.5}]
        )
        result = client.get_vix_term_structure()
        assert result["classification"] == "contango"

    def test_flat(self):
        """VIX/VIX3M 0.95-1.05 -> flat."""
        client = self._make_client()
        client.get_quote = MagicMock(
            side_effect=lambda s: [{"price": 15.0}] if "VIX3M" not in s else [{"price": 15.2}]
        )
        result = client.get_vix_term_structure()
        assert result["classification"] == "flat"

    def test_backwardation(self):
        """VIX/VIX3M > 1.05 -> backwardation."""
        client = self._make_client()
        client.get_quote = MagicMock(
            side_effect=lambda s: [{"price": 22.0}] if "VIX3M" not in s else [{"price": 18.0}]
        )
        result = client.get_vix_term_structure()
        assert result["classification"] == "backwardation"

    def test_unavailable(self):
        """VIX3M unavailable -> None."""
        client = self._make_client()
        client.get_quote = MagicMock(
            side_effect=lambda s: [{"price": 15.0}] if "VIX3M" not in s else None
        )
        result = client.get_vix_term_structure()
        assert result is None


def _mock_response(status_code, json_data=None, text=""):
    """Create a mock requests.Response."""
    resp = Mock()
    resp.status_code = status_code
    resp.json = Mock(return_value=json_data)
    resp.text = text
    return resp


class TestEndpointFallback:
    """Test stable/v3 endpoint fallback logic in FMPClient."""

    def _make_client(self):
        """Create FMPClient with mocked session."""
        with patch.dict(os.environ, {"FMP_API_KEY": "test_key"}):
            from fmp_client import FMPClient

            client = FMPClient(api_key="test_key")
        client.RATE_LIMIT_DELAY = 0  # disable rate limiting in tests
        return client

    # ------------------------------------------------------------------
    # Tier A — Fallback logic (4 tests)
    # ------------------------------------------------------------------

    def test_quote_stable_success(self):
        """Stable 200 returns data, v3 is NOT called."""
        client = self._make_client()
        quote_data = [{"symbol": "^GSPC", "price": 5500.0}]

        call_log = []

        def mock_get(url, params=None, timeout=None):
            call_log.append(url)
            if "stable" in url:
                return _mock_response(200, quote_data)
            return _mock_response(403, text="Forbidden")

        client.session.get = mock_get
        result = client.get_quote("^GSPC")

        assert result == quote_data
        assert len(call_log) == 1
        assert "stable" in call_log[0]

    def test_quote_stable_403_falls_back_to_v3(self):
        """Stable 403, v3 200 returns v3 data."""
        client = self._make_client()
        v3_data = [{"symbol": "^GSPC", "price": 5500.0}]

        def mock_get(url, params=None, timeout=None):
            if "stable" in url:
                return _mock_response(403, text="Forbidden")
            return _mock_response(200, v3_data)

        client.session.get = mock_get
        result = client.get_quote("^GSPC")
        assert result == v3_data

    def test_quote_both_fail(self):
        """Both endpoints 403 returns None."""
        client = self._make_client()

        def mock_get(url, params=None, timeout=None):
            return _mock_response(403, text="Forbidden")

        client.session.get = mock_get
        result = client.get_quote("^GSPC")
        assert result is None

    def test_historical_fallback_to_v3(self):
        """Stable 403, v3 200 returns v3 data for historical."""
        client = self._make_client()
        v3_data = {"symbol": "^GSPC", "historical": [{"date": "2026-03-20", "close": 5500.0}]}

        def mock_get(url, params=None, timeout=None):
            if "stable" in url:
                return _mock_response(403, text="Forbidden")
            return _mock_response(200, v3_data)

        client.session.get = mock_get
        result = client.get_historical_prices("^GSPC", days=80)
        assert result == v3_data
        assert "historical" in result

    # ------------------------------------------------------------------
    # Tier B — Response normalization (4 tests)
    # ------------------------------------------------------------------

    def test_historical_stable_v3_format_passthrough(self):
        """Stable returns v3-compatible format {'historical': [...]} — returned as-is."""
        client = self._make_client()
        data = {"symbol": "^GSPC", "historical": [{"date": "2026-03-20", "close": 5500.0}]}

        def mock_get(url, params=None, timeout=None):
            return _mock_response(200, data)

        client.session.get = mock_get
        result = client.get_historical_prices("^GSPC", days=80)
        assert result == data

    def test_historical_stable_batch_format_exact_match(self):
        """Stable returns historicalStockList with matching symbol — normalized."""
        client = self._make_client()
        batch_data = {
            "historicalStockList": [
                {
                    "symbol": "^GSPC",
                    "historical": [{"date": "2026-03-20", "close": 5500.0}],
                }
            ]
        }

        def mock_get(url, params=None, timeout=None):
            return _mock_response(200, batch_data)

        client.session.get = mock_get
        result = client.get_historical_prices("^GSPC", days=80)
        assert result is not None
        assert "historical" in result
        assert result["historical"] == [{"date": "2026-03-20", "close": 5500.0}]

    def test_historical_stable_batch_no_match_falls_back_to_v3(self):
        """Stable batch has wrong symbol, falls back to v3 which succeeds."""
        client = self._make_client()
        batch_data = {
            "historicalStockList": [
                {
                    "symbol": "SPY",
                    "historical": [{"date": "2026-03-20", "close": 550.0}],
                }
            ]
        }
        v3_data = {"symbol": "^GSPC", "historical": [{"date": "2026-03-20", "close": 5500.0}]}

        def mock_get(url, params=None, timeout=None):
            if "stable" in url:
                return _mock_response(200, batch_data)
            return _mock_response(200, v3_data)

        client.session.get = mock_get
        result = client.get_historical_prices("^GSPC", days=80)
        assert result == v3_data

    def test_historical_batch_no_match_returns_none_when_v3_also_fails(self):
        """Stable batch no match + v3 403 returns None."""
        client = self._make_client()
        batch_data = {
            "historicalStockList": [
                {
                    "symbol": "SPY",
                    "historical": [{"date": "2026-03-20", "close": 550.0}],
                }
            ]
        }

        def mock_get(url, params=None, timeout=None):
            if "stable" in url:
                return _mock_response(200, batch_data)
            return _mock_response(403, text="Forbidden")

        client.session.get = mock_get
        result = client.get_historical_prices("^GSPC", days=80)
        assert result is None

    # ------------------------------------------------------------------
    # Tier B+ — Shape validation (2 tests)
    # ------------------------------------------------------------------

    def test_quote_rejects_non_list_response(self):
        """Stable returns truthy dict — skipped, falls back to v3."""
        client = self._make_client()
        error_dict = {"Error Message": "Invalid API KEY."}
        v3_data = [{"symbol": "^GSPC", "price": 5500.0}]

        def mock_get(url, params=None, timeout=None):
            if "stable" in url:
                return _mock_response(200, error_dict)
            return _mock_response(200, v3_data)

        client.session.get = mock_get
        result = client.get_quote("^GSPC")
        assert result == v3_data

    def test_historical_rejects_non_dict_response(self):
        """Stable returns truthy list — skipped, falls back to v3."""
        client = self._make_client()
        bad_data = [1, 2, 3]
        v3_data = {"symbol": "^GSPC", "historical": [{"date": "2026-03-20", "close": 5500.0}]}

        def mock_get(url, params=None, timeout=None):
            if "stable" in url:
                return _mock_response(200, bad_data)
            return _mock_response(200, v3_data)

        client.session.get = mock_get
        result = client.get_historical_prices("^GSPC", days=80)
        assert result == v3_data

    # ------------------------------------------------------------------
    # Symbol mismatch protection
    # ------------------------------------------------------------------

    def test_quote_symbol_mismatch_falls_back(self):
        """Single-symbol quote returning wrong symbol is rejected."""
        client = self._make_client()
        wrong = _mock_response(200, [{"symbol": "SPY", "price": 500.0}])
        correct = _mock_response(200, [{"symbol": "^GSPC", "price": 5000.0}])
        client.session.get = MagicMock(side_effect=[wrong, correct])

        result = client.get_quote("^GSPC")
        assert result == [{"symbol": "^GSPC", "price": 5000.0}]
        assert client.session.get.call_count == 2

    def test_historical_symbol_mismatch_falls_back(self):
        """Single-symbol historical returning wrong symbol is rejected."""
        client = self._make_client()
        wrong = _mock_response(200, {"symbol": "SPY", "historical": [{"close": 500}]})
        correct = _mock_response(200, {"symbol": "^GSPC", "historical": [{"close": 5000}]})
        client.session.get = MagicMock(side_effect=[wrong, correct])

        result = client.get_historical_prices("^GSPC", days=80)
        assert result["symbol"] == "^GSPC"
        assert client.session.get.call_count == 2

    def test_batch_quote_skips_symbol_check(self):
        """Multi-symbol (batch) quote does not apply symbol mismatch check."""
        client = self._make_client()
        batch_data = [{"symbol": "^GSPC", "price": 5000}, {"symbol": "^VIX", "price": 20}]
        resp = _mock_response(200, batch_data)
        client.session.get = MagicMock(return_value=resp)

        result = client.get_quote("^GSPC,^VIX")
        assert result == batch_data
        assert client.session.get.call_count == 1

    # ------------------------------------------------------------------
    # Skill-specific tests
    # ------------------------------------------------------------------

    def test_vix_term_structure_works_via_fallback(self):
        """VIX term structure succeeds when get_quote uses stable->v3 fallback."""
        client = self._make_client()

        vix_data = [{"symbol": "^VIX", "price": 18.0}]
        vix3m_data = [{"symbol": "^VIX3M", "price": 20.0}]

        def mock_get(url, params=None, timeout=None):
            if "stable" in url:
                return _mock_response(403, text="Forbidden")
            # v3 fallback: route by symbol in URL path
            if "^VIX3M" in url:
                return _mock_response(200, vix3m_data)
            if "^VIX" in url:
                return _mock_response(200, vix_data)
            return _mock_response(404, text="Not Found")

        client.session.get = mock_get
        result = client.get_vix_term_structure()

        assert result is not None
        assert result["vix"] == 18.0
        assert result["vix3m"] == 20.0
        # 18/20 = 0.9 -> contango
        assert result["classification"] == "contango"
        assert result["ratio"] == 0.9

    def test_market_top_exits_on_sp500_failure(self):
        """main() exits with code 1 when S&P 500 data unavailable."""
        from fmp_client import FMPClient

        with (
            patch.object(FMPClient, "__init__", lambda self, **kw: None),
            patch.object(FMPClient, "get_quote", return_value=None),
            patch.object(FMPClient, "get_historical_prices", return_value=None),
            patch.object(
                FMPClient,
                "get_api_stats",
                return_value={
                    "cache_entries": 0,
                    "api_calls_made": 0,
                    "rate_limit_reached": False,
                },
            ),
            patch("sys.argv", ["market_top_detector.py"]),
        ):
            # Need to set required attributes that __init__ would set
            def fake_init(self, **kw):
                self.api_key = "test"  # pragma: allowlist secret
                self.session = MagicMock()
                self.cache = {}
                self.last_call_time = 0
                self.rate_limit_reached = False
                self.retry_count = 0
                self.max_retries = 1
                self.api_calls_made = 0

            with patch.object(FMPClient, "__init__", fake_init):
                import market_top_detector

                with pytest.raises(SystemExit) as exc_info:
                    market_top_detector.main()
                assert exc_info.value.code == 1

    def test_market_top_continues_on_vix_failure(self, capsys):
        """main() continues with warning when VIX unavailable (non-fatal)."""
        from fmp_client import FMPClient

        sp500_quote = [{"symbol": "^GSPC", "price": 5500.0, "yearHigh": 5600.0}]
        sp500_hist = {
            "symbol": "^GSPC",
            "historical": [
                {
                    "date": f"2026-03-{20 - i:02d}",
                    "close": 5500.0 - i * 10,
                    "volume": 3_000_000_000,
                    "open": 5490.0 - i * 10,
                    "high": 5510.0 - i * 10,
                    "low": 5480.0 - i * 10,
                }
                for i in range(260)
            ],
        }
        qqq_quote = [{"symbol": "QQQ", "price": 480.0, "yearHigh": 500.0}]
        qqq_hist = {
            "symbol": "QQQ",
            "historical": [
                {
                    "date": f"2026-03-{20 - i:02d}",
                    "close": 480.0 - i,
                    "volume": 50_000_000,
                    "open": 479.0 - i,
                    "high": 481.0 - i,
                    "low": 478.0 - i,
                }
                for i in range(260)
            ],
        }

        def mock_quote(symbols):
            if symbols == "^GSPC":
                return sp500_quote
            if symbols == "QQQ":
                return qqq_quote
            if symbols == "^VIX":
                return None  # VIX fails
            if symbols == "^VIX3M":
                return None
            # Return generic quote for ETFs
            return [
                {
                    "symbol": symbols.split(",")[0],
                    "price": 100.0,
                    "yearHigh": 110.0,
                    "changesPercentage": 0.5,
                    "volume": 1_000_000,
                    "avgVolume": 1_000_000,
                }
            ]

        def mock_hist(symbol, days=365):
            if symbol == "^GSPC":
                return sp500_hist
            if symbol == "QQQ":
                return qqq_hist
            # Generic history for ETFs
            return {
                "symbol": symbol,
                "historical": [
                    {
                        "date": f"2026-03-{20 - i:02d}",
                        "close": 100.0 + i * 0.1,
                        "volume": 1_000_000,
                        "open": 99.9 + i * 0.1,
                        "high": 100.1 + i * 0.1,
                        "low": 99.8 + i * 0.1,
                    }
                    for i in range(min(days, 260))
                ],
            }

        def mock_batch_quotes(symbols):
            result = {}
            for s in symbols:
                q = mock_quote(s)
                if q:
                    for item in q:
                        result[item.get("symbol", s)] = item
            return result

        def mock_batch_hist(symbols, days=50):
            result = {}
            for s in symbols:
                d = mock_hist(s, days)
                if d and "historical" in d:
                    result[s] = d["historical"]
            return result

        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            with (
                patch.dict(os.environ, {"FMP_API_KEY": "test_key"}),  # pragma: allowlist secret
                patch(
                    "sys.argv",
                    [
                        "market_top_detector.py",
                        "--static-basket",
                        "--no-auto-breadth",
                        "--breadth-200dma",
                        "60.0",
                        "--put-call",
                        "0.70",
                        "--vix-term",
                        "contango",
                        "--output-dir",
                        tmpdir,
                    ],
                ),
            ):
                from fmp_client import FMPClient

                with (
                    patch.object(FMPClient, "get_quote", side_effect=mock_quote),
                    patch.object(FMPClient, "get_historical_prices", side_effect=mock_hist),
                    patch.object(FMPClient, "get_batch_quotes", side_effect=mock_batch_quotes),
                    patch.object(FMPClient, "get_batch_historical", side_effect=mock_batch_hist),
                ):
                    import importlib

                    import market_top_detector

                    importlib.reload(market_top_detector)

                    # Should NOT raise SystemExit — VIX failure is non-fatal
                    try:
                        market_top_detector.main()
                    except SystemExit:
                        pytest.fail("main() should not exit when only VIX fails")

            captured = capsys.readouterr()
            assert "WARN" in captured.out or "VIX unavailable" in captured.out
