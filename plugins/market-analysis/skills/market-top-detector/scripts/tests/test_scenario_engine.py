"""Tests for What-If Scenario Engine"""

from scenario_engine import generate_scenarios
from scorer import COMPONENT_WEIGHTS


class TestGenerateScenarios:
    """Test scenario generation."""

    def test_returns_4_scenarios(self):
        scores = {k: 50 for k in COMPONENT_WEIGHTS}
        scenarios = generate_scenarios(scores)
        assert len(scenarios) == 4

    def test_scenario_names(self):
        scores = {k: 50 for k in COMPONENT_WEIGHTS}
        scenarios = generate_scenarios(scores)
        names = {s["name"] for s in scenarios}
        assert "Breadth Deterioration" in names
        assert "Distribution Reset" in names
        assert "Full Deterioration" in names
        assert "Recovery" in names

    def test_breadth_deterioration_raises_score(self):
        """Low breadth -> raising to 55 should increase composite."""
        scores = {k: 30 for k in COMPONENT_WEIGHTS}
        scores["breadth_divergence"] = 10
        scenarios = generate_scenarios(scores)
        breadth_scenario = next(s for s in scenarios if s["name"] == "Breadth Deterioration")
        assert breadth_scenario["delta"] >= 0

    def test_recovery_lowers_score(self):
        """Reducing top 2 strongest by -30pt should lower composite."""
        scores = {
            "distribution_days": 80,
            "leading_stocks": 70,
            "defensive_rotation": 60,
            "breadth_divergence": 50,
            "index_technical": 40,
            "sentiment": 30,
        }
        scenarios = generate_scenarios(scores)
        recovery = next(s for s in scenarios if s["name"] == "Recovery")
        assert recovery["delta"] <= 0

    def test_distribution_reset_lowers_high_score(self):
        """Distribution Reset should reduce score when distribution_days > 55."""
        scores = {
            "distribution_days": 100,
            "leading_stocks": 50,
            "defensive_rotation": 50,
            "breadth_divergence": 50,
            "index_technical": 50,
            "sentiment": 50,
        }
        scenarios = generate_scenarios(scores)
        reset = next(s for s in scenarios if s["name"] == "Distribution Reset")
        assert reset["delta"] < 0, (
            f"Distribution Reset with dd=100 should lower score, got delta={reset['delta']}"
        )
        assert reset["changes"]["distribution_days"] == 55

    def test_distribution_reset_no_change_when_below_55(self):
        """Distribution Reset should not raise score when distribution_days < 55."""
        scores = {
            "distribution_days": 30,
            "leading_stocks": 50,
            "defensive_rotation": 50,
            "breadth_divergence": 50,
            "index_technical": 50,
            "sentiment": 50,
        }
        scenarios = generate_scenarios(scores)
        reset = next(s for s in scenarios if s["name"] == "Distribution Reset")
        assert reset["delta"] == 0
        assert reset["changes"]["distribution_days"] == 30

    def test_scores_clamped_0_100(self):
        """Scores should never exceed 0-100 range."""
        scores = {k: 90 for k in COMPONENT_WEIGHTS}
        scenarios = generate_scenarios(scores)
        for s in scenarios:
            assert 0 <= s["new_score"] <= 100

    def test_deterministic_with_equal_scores(self):
        """Equal scores should still produce deterministic results."""
        scores = {k: 50 for k in COMPONENT_WEIGHTS}
        s1 = generate_scenarios(scores)
        s2 = generate_scenarios(scores)
        for a, b in zip(s1, s2):
            assert a["new_score"] == b["new_score"]
