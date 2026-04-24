"""Tests for Sentiment Calculator"""

from calculators.sentiment_calculator import calculate_sentiment


class TestSentimentMissingData:
    """Test missing data handling."""

    def test_all_none_returns_50(self):
        """All inputs None -> score=50, data_available=False."""
        result = calculate_sentiment()
        assert result["score"] == 50
        assert result["data_available"] is False
        assert "NO DATA" in result["signal"]

    def test_partial_data_is_available(self):
        """At least one input -> data_available=True."""
        result = calculate_sentiment(vix_level=15.0)
        assert result["data_available"] is True

    def test_vix_only(self):
        result = calculate_sentiment(vix_level=15.0)
        assert result["score"] == 8  # VIX 15 -> +8pt

    def test_put_call_only(self):
        result = calculate_sentiment(put_call_ratio=0.65)
        assert result["score"] == 25  # PC < 0.70 -> +25pt


class TestSentimentScoring:
    """Boundary tests for sentiment scoring."""

    def test_extreme_complacency_without_margin(self):
        """Low VIX + low P/C + steep contango (no margin) = 85."""
        result = calculate_sentiment(
            vix_level=11.0,
            put_call_ratio=0.55,
            vix_term_structure="steep_contango",
        )
        # 25+35+25=85
        assert result["score"] == 85

    def test_extreme_complacency_with_margin(self):
        """All components maxed = 100."""
        result = calculate_sentiment(
            vix_level=11.0,
            put_call_ratio=0.55,
            vix_term_structure="steep_contango",
            margin_debt_yoy_pct=35.0,
        )
        # 25+35+25+15=100
        assert result["score"] == 100

    def test_high_fear(self):
        """High VIX + high P/C + backwardation = 0."""
        result = calculate_sentiment(
            vix_level=30.0,
            put_call_ratio=0.95,
            vix_term_structure="backwardation",
        )
        # -8+0+(-8) = -16 -> clamped to 0
        assert result["score"] == 0

    def test_moderate_sentiment(self):
        result = calculate_sentiment(
            vix_level=15.0,
            put_call_ratio=0.75,
            vix_term_structure="contango",
        )
        # VIX 15->8, PC 0.75->12, contango->12 = 32
        assert result["score"] == 32

    def test_margin_debt_scored(self):
        """Margin debt should now affect score."""
        without = calculate_sentiment(vix_level=15.0)
        with_margin = calculate_sentiment(vix_level=15.0, margin_debt_yoy_pct=40.0)
        assert with_margin["score"] > without["score"]

    def test_margin_debt_thresholds(self):
        """Test margin debt scoring thresholds."""
        # <= 10% -> 0pt
        r1 = calculate_sentiment(vix_level=15.0, margin_debt_yoy_pct=5.0)
        assert r1["score"] == 8  # VIX only

        # > 10% -> 5pt
        r2 = calculate_sentiment(vix_level=15.0, margin_debt_yoy_pct=15.0)
        assert r2["score"] == 13  # 8 + 5

        # > 20% -> 10pt
        r3 = calculate_sentiment(vix_level=15.0, margin_debt_yoy_pct=25.0)
        assert r3["score"] == 18  # 8 + 10

        # > 30% -> 15pt
        r4 = calculate_sentiment(vix_level=15.0, margin_debt_yoy_pct=36.0)
        assert r4["score"] == 23  # 8 + 15

    def test_margin_debt_details_has_points(self):
        """Margin debt details should include points field."""
        result = calculate_sentiment(vix_level=15.0, margin_debt_yoy_pct=25.0)
        md = result["details"]["margin_debt"]
        assert "points" in md
        assert md["points"] == 10
        assert "note" not in md  # Old "not scored" note removed
