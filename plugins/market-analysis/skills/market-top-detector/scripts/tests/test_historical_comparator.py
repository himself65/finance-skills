"""Tests for Historical Top Pattern Comparator"""

from historical_comparator import (
    COMPONENT_KEYS,
    HISTORICAL_TOPS,
    _compute_ssd,
    compare_to_historical,
)


class TestComputeSSD:
    """Test SSD calculation."""

    def test_identical_scores_zero_ssd(self):
        scores = {k: 50 for k in COMPONENT_KEYS}
        assert _compute_ssd(scores, scores) == 0.0

    def test_known_ssd(self):
        a = {k: 0 for k in COMPONENT_KEYS}
        b = {k: 10 for k in COMPONENT_KEYS}
        # Weighted: sum(weight_i * 10^2) = 100 * sum(weights) = 100 * 1.0 = 100.0
        assert _compute_ssd(a, b) == 100.0

    def test_weighted_ssd_prioritizes_high_weight(self):
        """Distribution days (25%) difference should contribute more than sentiment (10%)."""
        base = {k: 50 for k in COMPONENT_KEYS}
        # Only distribution_days differs by 20
        a = dict(base)
        a["distribution_days"] = 70
        ssd_dist = _compute_ssd(a, base)
        # Only sentiment differs by 20
        b = dict(base)
        b["sentiment"] = 70
        ssd_sent = _compute_ssd(b, base)
        # distribution_days (0.25 * 400 = 100) > sentiment (0.10 * 400 = 40)
        assert ssd_dist > ssd_sent


class TestCompareToHistorical:
    """Test comparison to historical patterns."""

    def test_all_zeros_closest(self):
        """All zeros should be closest to 2018 (lowest overall scores)."""
        scores = {k: 0 for k in COMPONENT_KEYS}
        result = compare_to_historical(scores)
        assert "2018" in result["closest_match"]
        assert len(result["comparisons"]) == 4

    def test_all_100_closest(self):
        """All 100 should be closest to 2000 (highest overall scores)."""
        scores = {k: 100 for k in COMPONENT_KEYS}
        result = compare_to_historical(scores)
        assert "2000" in result["closest_match"]

    def test_ssd_ordering(self):
        """Comparisons should be sorted by SSD ascending."""
        scores = {k: 50 for k in COMPONENT_KEYS}
        result = compare_to_historical(scores)
        ssds = [c["ssd"] for c in result["comparisons"]]
        assert ssds == sorted(ssds)

    def test_narrative_with_differences(self):
        """Large differences should appear in narrative."""
        scores = {k: 0 for k in COMPONENT_KEYS}
        scores["distribution_days"] = 100  # Very different from any top
        result = compare_to_historical(scores)
        assert "Distribution Days" in result["narrative"] or "lower" in result["narrative"]

    def test_narrative_close_match(self):
        """Scores close to a pattern should produce 'closely matches' text."""
        # Use exact 2018 scores
        scores = dict(HISTORICAL_TOPS["2018 (Q4 Correction)"])
        result = compare_to_historical(scores)
        assert result["closest_ssd"] == 0.0
        assert "closely matches" in result["narrative"]
