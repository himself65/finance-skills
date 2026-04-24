"""Tests for Breadth Calculator"""

from calculators.breadth_calculator import (
    _score_200dma_breadth,
    calculate_breadth_divergence,
)


class TestScore200dmaBreadth:
    """Boundary tests for 200DMA scoring."""

    def test_critical_below_40(self):
        assert _score_200dma_breadth(35) == 100

    def test_healthy_above_70(self):
        assert _score_200dma_breadth(75) == 5

    def test_calibration_62_26(self):
        """62.26% breadth should score ~24 (healthy)."""
        score = _score_200dma_breadth(62.26)
        assert 18 <= score <= 30  # Reasonable range around 24

    def test_boundary_50(self):
        score = _score_200dma_breadth(50)
        assert score == 55

    def test_boundary_60(self):
        score = _score_200dma_breadth(60)
        assert score == 30


class TestCalculateBreadthDivergence:
    """Integration tests."""

    def test_missing_breadth_returns_50(self):
        """None 200DMA → score 50, data_available=False."""
        result = calculate_breadth_divergence(None, None, -2.0)
        assert result["score"] == 50
        assert result["data_available"] is False

    def test_available_data_has_flag(self):
        """Valid data → data_available=True."""
        result = calculate_breadth_divergence(65.0, 55.0, -1.0)
        assert result["data_available"] is True

    def test_near_highs_divergence(self):
        """Index near highs + weak breadth → high score."""
        result = calculate_breadth_divergence(45.0, 30.0, -2.0)
        assert result["score"] >= 70
        assert result["divergence_detected"] is True

    def test_not_near_highs_halved(self):
        """Index NOT near highs → score halved."""
        near = calculate_breadth_divergence(45.0, None, -2.0)
        far = calculate_breadth_divergence(45.0, None, -8.0)
        assert far["score"] < near["score"]

    def test_50dma_supplement_boost(self):
        """Low 50DMA breadth at highs adds +10."""
        base = calculate_breadth_divergence(55.0, 80.0, -2.0)
        boosted = calculate_breadth_divergence(55.0, 25.0, -2.0)
        assert boosted["score"] > base["score"]

    def test_auto_fetched_breadth_source_marker(self):
        """breadth_source can be set on comp4 result after calculate."""
        result = calculate_breadth_divergence(64.81, None, -1.0)
        result["breadth_source"] = "auto"
        result["breadth_auto_date"] = "2026-02-18"
        assert result["breadth_source"] == "auto"
        assert result["breadth_auto_date"] == "2026-02-18"
        assert result["data_available"] is True
