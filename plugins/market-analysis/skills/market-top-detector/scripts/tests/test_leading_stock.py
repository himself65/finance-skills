"""Tests for Leading Stock Calculator"""

from calculators.leading_stock_calculator import (
    CANDIDATE_POOL,
    DEFAULT_LEADING_ETFS,
    _evaluate_etf,
    calculate_leading_stock_health,
    select_dynamic_basket,
)


class TestEvaluateETF:
    """Test individual ETF evaluation."""

    def test_near_highs_healthy(self):
        quote = {"price": 100, "yearHigh": 102, "yearLow": 80}
        history = [{"close": 100 - i * 0.1, "volume": 1000000} for i in range(60)]
        result = _evaluate_etf("TEST", quote, history)
        assert result["deterioration_score"] <= 20

    def test_deep_correction(self):
        quote = {"price": 70, "yearHigh": 100, "yearLow": 65}
        history = [{"close": 70 + i * 0.3, "volume": 1000000} for i in range(60)]
        result = _evaluate_etf("TEST", quote, history)
        assert result["deterioration_score"] >= 30


class TestCalculateLeadingStockHealth:
    """Test composite leading stock calculation."""

    def test_no_data_returns_50(self):
        """No quotes -> score 50 (neutral), data_available=False."""
        result = calculate_leading_stock_health({}, {})
        assert result["score"] == 50
        assert result["etfs_evaluated"] == 0
        assert result["data_available"] is False

    def test_healthy_leaders(self):
        quotes = {}
        historical = {}
        for sym in ["ARKK", "WCLD", "IGV"]:
            quotes[sym] = {"price": 100, "yearHigh": 102, "yearLow": 80}
            historical[sym] = [{"close": 100 - i * 0.05, "volume": 1000000} for i in range(60)]
        result = calculate_leading_stock_health(quotes, historical)
        assert result["score"] <= 30  # Healthy
        assert result["data_available"] is True

    def test_amplification_at_60pct(self):
        """60%+ ETFs deteriorating triggers 1.3x amplification."""
        quotes = {}
        historical = {}
        for sym in ["ARKK", "WCLD", "IGV", "XBI", "SOXX", "SMH", "KWEB", "TAN"]:
            quotes[sym] = {"price": 70, "yearHigh": 100, "yearLow": 60}
            historical[sym] = [
                {"close": 70 + i * 0.5, "high": 72 + i * 0.5, "volume": 1000000} for i in range(60)
            ]
        result = calculate_leading_stock_health(quotes, historical)
        assert result["amplified"] is True


class TestFetchSuccessRate:
    """Test fetch success rate tracking."""

    def test_all_fetched(self):
        """All ETFs have quotes -> success rate = 1.0."""
        quotes = {}
        historical = {}
        for sym in ["A", "B", "C"]:
            quotes[sym] = {"price": 100, "yearHigh": 102, "yearLow": 80}
            historical[sym] = [{"close": 100, "volume": 1000000} for _ in range(60)]
        result = calculate_leading_stock_health(quotes, historical)
        assert result["fetch_success_rate"] == 1.0
        assert result["data_available"] is True

    def test_partial_fetched(self):
        """Some ETFs missing quotes -> lower success rate."""
        quotes = {"A": {"price": 100, "yearHigh": 102, "yearLow": 80}}
        historical = {"A": [{"close": 100, "volume": 1000000} for _ in range(60)]}
        # Only 1 out of 1 in quotes -> 1.0
        result = calculate_leading_stock_health(quotes, historical)
        assert result["fetch_success_rate"] == 1.0

    def test_below_threshold_marks_unavailable(self):
        """Below 75% success rate -> data_available=False."""
        # quotes has 4 keys but only 2 have actual data
        quotes = {
            "A": {"price": 100, "yearHigh": 102, "yearLow": 80},
            "B": None,
            "C": None,
            "D": None,
        }
        historical = {"A": [{"close": 100, "volume": 1000000} for _ in range(60)]}
        result = calculate_leading_stock_health(quotes, historical)
        # 1 success out of 4 = 0.25 < 0.75
        assert result["fetch_success_rate"] < 0.75
        assert result["data_available"] is False


class TestSelectDynamicBasket:
    """Test dynamic basket selection."""

    def test_selects_top_n_by_proximity(self):
        """Should select ETFs closest to 52-week high."""
        quotes = {
            "SMH": {"price": 98, "yearHigh": 100},
            "SOXX": {"price": 90, "yearHigh": 100},
            "IGV": {"price": 95, "yearHigh": 100},
            "WCLD": {"price": 80, "yearHigh": 100},
            "XBI": {"price": 70, "yearHigh": 100},
            "ARKK": {"price": 60, "yearHigh": 100},
        }
        result = select_dynamic_basket(quotes, top_n=3)
        assert len(result) == 3
        assert result[0] == "SMH"  # 98% proximity
        assert result[1] == "IGV"  # 95% proximity
        assert result[2] == "SOXX"  # 90% proximity

    def test_fallback_when_too_few_candidates(self):
        """Fewer than 5 valid candidates -> fall back to default basket."""
        quotes = {
            "SMH": {"price": 100, "yearHigh": 100},
            "SOXX": {"price": 90, "yearHigh": 100},
        }
        result = select_dynamic_basket(quotes)
        assert result == list(DEFAULT_LEADING_ETFS)

    def test_skips_invalid_quotes(self):
        """Symbols with price=0 or yearHigh=0 should be skipped."""
        quotes = {}
        for i, sym in enumerate(CANDIDATE_POOL[:8]):
            quotes[sym] = {"price": 100 - i * 5, "yearHigh": 100}
        # Add invalid entries
        quotes["BAD1"] = {"price": 0, "yearHigh": 100}
        quotes["BAD2"] = {"price": 50, "yearHigh": 0}
        result = select_dynamic_basket(quotes, top_n=5)
        assert len(result) == 5
        assert "BAD1" not in result
        assert "BAD2" not in result

    def test_empty_quotes_returns_default(self):
        """Empty quotes dict -> default basket."""
        result = select_dynamic_basket({})
        assert result == list(DEFAULT_LEADING_ETFS)


class TestPartialDataTracking:
    """Test partial data detection (quote but insufficient history)."""

    def test_quote_only_not_available(self):
        """8 ETFs with quotes but no history -> data_available=False, partial=8."""
        symbols = ["A", "B", "C", "D", "E", "F", "G", "H"]
        quotes = {s: {"price": 100, "yearHigh": 102, "yearLow": 80} for s in symbols}
        historical = {}  # No history at all
        result = calculate_leading_stock_health(quotes, historical, etf_list=symbols)
        assert result["data_available"] is False
        assert result["partial_data_count"] == 8
        assert result["fetch_success_rate"] == 0.0

    def test_mixed_full_and_partial_above_threshold(self):
        """6 full + 2 partial out of 8 -> data_available=True (75%), partial=2."""
        symbols = ["A", "B", "C", "D", "E", "F", "G", "H"]
        quotes = {s: {"price": 100, "yearHigh": 102, "yearLow": 80} for s in symbols}
        historical = {}
        for s in symbols[:6]:
            # Full history (50+ bars)
            historical[s] = [{"close": 100 - i * 0.1, "volume": 1000000} for i in range(60)]
        for s in symbols[6:]:
            # Partial history (< 50 bars)
            historical[s] = [{"close": 100 - i * 0.1, "volume": 1000000} for i in range(20)]
        result = calculate_leading_stock_health(quotes, historical, etf_list=symbols)
        assert result["data_available"] is True  # 6/8 = 0.75
        assert result["partial_data_count"] == 2
        assert result["fetch_success_rate"] == 0.75

    def test_mixed_full_and_partial_below_threshold(self):
        """5 full + 3 partial out of 8 -> data_available=False (62.5%), partial=3."""
        symbols = ["A", "B", "C", "D", "E", "F", "G", "H"]
        quotes = {s: {"price": 100, "yearHigh": 102, "yearLow": 80} for s in symbols}
        historical = {}
        for s in symbols[:5]:
            historical[s] = [{"close": 100 - i * 0.1, "volume": 1000000} for i in range(60)]
        for s in symbols[5:]:
            historical[s] = [{"close": 100 - i * 0.1, "volume": 1000000} for i in range(20)]
        result = calculate_leading_stock_health(quotes, historical, etf_list=symbols)
        assert result["data_available"] is False  # 5/8 = 0.625 < 0.75
        assert result["partial_data_count"] == 3

    def test_no_data_includes_partial_count(self):
        """No data case should also include partial_data_count."""
        result = calculate_leading_stock_health({}, {})
        assert "partial_data_count" in result
        assert result["partial_data_count"] == 0


class TestBasketModeInResult:
    """Test basket_mode and basket fields in result."""

    def test_static_basket_mode(self):
        """Passing DEFAULT_LEADING_ETFS as etf_list -> static mode."""
        quotes = {"A": {"price": 100, "yearHigh": 102, "yearLow": 80}}
        historical = {"A": [{"close": 100, "volume": 1000000} for _ in range(60)]}
        result = calculate_leading_stock_health(
            quotes, historical, etf_list=list(DEFAULT_LEADING_ETFS)
        )
        assert result["basket_mode"] == "static"
        assert result["basket"] == list(DEFAULT_LEADING_ETFS)

    def test_dynamic_basket_mode(self):
        """Passing custom etf_list -> dynamic mode."""
        etfs = ["SMH", "SOXX", "IGV"]
        quotes = {}
        historical = {}
        for sym in etfs:
            quotes[sym] = {"price": 100, "yearHigh": 102, "yearLow": 80}
            historical[sym] = [{"close": 100, "volume": 1000000} for _ in range(60)]
        result = calculate_leading_stock_health(quotes, historical, etf_list=etfs)
        assert result["basket_mode"] == "dynamic"
        assert result["basket"] == etfs
