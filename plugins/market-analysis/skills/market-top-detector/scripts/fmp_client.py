#!/usr/bin/env python3
"""
FMP API Client for Market Top Detector

Provides rate-limited access to Financial Modeling Prep API endpoints
for market top detection analysis.

Features:
- Rate limiting (0.3s between requests)
- Automatic retry on 429 errors
- Session caching for duplicate requests
- Batch quote support for ETF baskets
"""

import os
import sys
import time
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library not found. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


# --- FMP endpoint fallback: stable (new users) -> v3 (legacy users) ---


def _stable_quote_url(base, symbols_str, params):
    """stable/quote?symbol=^GSPC"""
    params["symbol"] = symbols_str
    return base, params


def _v3_quote_url(base, symbols_str, params):
    """api/v3/quote/^GSPC"""
    return f"{base}/{symbols_str}", params


def _stable_hist_url(base, symbols_str, params):
    """stable/historical-price-eod/full?symbol=^GSPC&timeseries=80"""
    params["symbol"] = symbols_str
    return base, params


def _v3_hist_url(base, symbols_str, params):
    """api/v3/historical-price-full/^GSPC?timeseries=80"""
    return f"{base}/{symbols_str}", params


_FMP_ENDPOINTS = {
    "quote": [
        ("https://financialmodelingprep.com/stable/quote", _stable_quote_url),
        ("https://financialmodelingprep.com/api/v3/quote", _v3_quote_url),
    ],
    "historical": [
        ("https://financialmodelingprep.com/stable/historical-price-eod/full", _stable_hist_url),
        ("https://financialmodelingprep.com/api/v3/historical-price-full", _v3_hist_url),
    ],
}


class FMPClient:
    """Client for Financial Modeling Prep API with rate limiting and caching"""

    BASE_URL = "https://financialmodelingprep.com/api/v3"
    RATE_LIMIT_DELAY = 0.3  # 300ms between requests

    _ENDPOINT_FAILURE_THRESHOLD = 3  # disable endpoint after N consecutive failures

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FMP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "FMP API key required. Set FMP_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.session = requests.Session()
        self.session.headers.update({"apikey": self.api_key})
        self.cache = {}
        self.last_call_time = 0
        self.rate_limit_reached = False
        self.retry_count = 0
        self.max_retries = 1
        self.api_calls_made = 0
        # Circuit breaker: track consecutive failures per endpoint URL prefix
        self._endpoint_failures: dict[str, int] = {}
        self._disabled_endpoints: set[str] = set()

    def _rate_limited_get(
        self, url: str, params: Optional[dict] = None, quiet: bool = False
    ) -> Optional[dict]:
        if self.rate_limit_reached:
            return None

        if params is None:
            params = {}
        else:
            params = dict(params)

        params.setdefault("apikey", self.api_key)

        elapsed = time.time() - self.last_call_time
        if elapsed < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed)

        try:
            response = self.session.get(url, params=params, timeout=30)
            self.last_call_time = time.time()
            self.api_calls_made += 1

            if response.status_code == 200:
                self.retry_count = 0
                return response.json()
            elif response.status_code == 429:
                self.retry_count += 1
                if self.retry_count <= self.max_retries:
                    print("WARNING: Rate limit exceeded. Waiting 60 seconds...", file=sys.stderr)
                    time.sleep(60)
                    return self._rate_limited_get(url, params, quiet=quiet)
                else:
                    print("ERROR: Daily API rate limit reached.", file=sys.stderr)
                    self.rate_limit_reached = True
                    return None
            else:
                if not quiet:
                    print(
                        f"ERROR: API request failed: {response.status_code} - {response.text[:200]}",
                        file=sys.stderr,
                    )
                return None
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request exception: {e}", file=sys.stderr)
            return None

    def _request_with_fallback(self, endpoint_key, symbols_str, extra_params=None):
        """Try stable endpoint first, fall back to v3 for legacy users.

        Returns parsed JSON in v3-compatible shape, or None if all fail.
        Non-last endpoints use quiet=True to suppress expected 403 stderr.
        """
        params = dict(extra_params) if extra_params else {}
        endpoints = _FMP_ENDPOINTS[endpoint_key]
        is_single = "," not in symbols_str

        for i, (base_url, url_builder) in enumerate(endpoints):
            # Circuit breaker: skip endpoints with too many consecutive failures
            if base_url in self._disabled_endpoints:
                continue

            url, final_params = url_builder(base_url, symbols_str, dict(params))
            is_last = i == len(endpoints) - 1
            data = self._rate_limited_get(url, final_params, quiet=not is_last)
            if not data:  # falsy (None, [], {}) — try next endpoint
                self._record_endpoint_failure(base_url)
                continue

            # Shape validation: reject truthy-but-wrong-shape responses
            valid = True
            if endpoint_key == "quote":
                if not isinstance(data, list) or len(data) == 0:
                    valid = False
                elif is_single and not any(
                    q.get("symbol", "").replace("-", ".") == symbols_str.replace("-", ".")
                    for q in data
                ):
                    valid = False

            if endpoint_key == "historical":
                if isinstance(data, list):
                    # stable historical-price-eod/full returns a plain list of bars.
                    if data and all(isinstance(row, dict) for row in data):
                        self._endpoint_failures[base_url] = 0
                        return {"symbol": symbols_str, "historical": data}
                    valid = False
                elif not isinstance(data, dict):
                    valid = False
                elif "historicalStockList" in data:
                    # stable batch format -> v3 single format (exact match only)
                    norm = symbols_str.replace("-", ".")
                    found = None
                    for entry in data["historicalStockList"]:
                        if entry.get("symbol", "").replace("-", ".") == norm:
                            found = {
                                "symbol": entry.get("symbol"),
                                "historical": entry.get("historical", []),
                            }
                            break
                    if found:
                        self._endpoint_failures[base_url] = 0
                        return found
                    valid = False
                elif "historical" not in data:
                    valid = False
                elif is_single and data.get("symbol"):
                    if data["symbol"].replace("-", ".") != symbols_str.replace("-", "."):
                        valid = False

            if valid:
                self._endpoint_failures[base_url] = 0
                return data
            self._record_endpoint_failure(base_url)
        return None

    def _record_endpoint_failure(self, base_url: str) -> None:
        """Track consecutive failures and disable endpoint after threshold."""
        failures = self._endpoint_failures.get(base_url, 0) + 1
        self._endpoint_failures[base_url] = failures
        if failures >= self._ENDPOINT_FAILURE_THRESHOLD:
            self._disabled_endpoints.add(base_url)

    def get_quote(self, symbols: str) -> Optional[list[dict]]:
        """Fetch real-time quote data for one or more symbols (comma-separated)"""
        cache_key = f"quote_{symbols}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        data = self._request_with_fallback("quote", symbols)
        if data:
            self.cache[cache_key] = data
        return data

    def get_historical_prices(self, symbol: str, days: int = 365) -> Optional[dict]:
        """Fetch historical daily OHLCV data"""
        cache_key = f"prices_{symbol}_{days}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        data = self._request_with_fallback("historical", symbol, {"timeseries": days})
        if data:
            self.cache[cache_key] = data
        return data

    def get_batch_quotes(self, symbols: list[str]) -> dict[str, dict]:
        """Fetch quotes for a list of symbols.

        FMP's stable quote endpoint may reject comma-separated symbols on some
        subscriptions, so request one symbol at a time for broad compatibility.
        """
        results = {}
        for symbol in symbols:
            quotes = self.get_quote(symbol)
            if quotes:
                for q in quotes:
                    results[q["symbol"]] = q
        return results

    def get_batch_historical(self, symbols: list[str], days: int = 50) -> dict[str, list[dict]]:
        """Fetch historical prices for multiple symbols"""
        results = {}
        for symbol in symbols:
            data = self.get_historical_prices(symbol, days=days)
            if data and "historical" in data:
                results[symbol] = data["historical"]
        return results

    def calculate_ema(self, prices: list[float], period: int) -> float:
        """Calculate EMA (thin wrapper around math_utils for backward compat)."""
        from calculators.math_utils import calc_ema

        return calc_ema(prices, period)

    def calculate_sma(self, prices: list[float], period: int) -> float:
        """Calculate SMA (thin wrapper around math_utils for backward compat)."""
        from calculators.math_utils import calc_sma

        return calc_sma(prices, period)

    def get_vix_term_structure(self) -> Optional[dict]:
        """
        Auto-detect VIX term structure by comparing VIX to VIX3M.

        Returns:
            Dict with ratio, classification, or None if VIX3M unavailable.
        """
        vix_quotes = self.get_quote("^VIX")
        vix3m_quotes = self.get_quote("^VIX3M")

        if not vix_quotes or not vix3m_quotes:
            return None

        vix_price = vix_quotes[0].get("price", 0)
        vix3m_price = vix3m_quotes[0].get("price", 0)

        if vix3m_price <= 0:
            return None

        ratio = vix_price / vix3m_price

        if ratio < 0.85:
            classification = "steep_contango"
        elif ratio < 0.95:
            classification = "contango"
        elif ratio <= 1.05:
            classification = "flat"
        else:
            classification = "backwardation"

        return {
            "vix": round(vix_price, 2),
            "vix3m": round(vix3m_price, 2),
            "ratio": round(ratio, 3),
            "classification": classification,
        }

    def get_api_stats(self) -> dict:
        return {
            "cache_entries": len(self.cache),
            "api_calls_made": self.api_calls_made,
            "rate_limit_reached": self.rate_limit_reached,
        }
