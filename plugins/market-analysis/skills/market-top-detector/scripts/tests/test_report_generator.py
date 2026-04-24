"""Tests for Report Generator"""

import os
import tempfile

from report_generator import _delta_arrow, generate_markdown_report


class TestDeltaArrow:
    """Test delta arrow formatting."""

    def test_first_run(self):
        assert _delta_arrow({"direction": "first_run", "delta": 0}) == "---"

    def test_worsening(self):
        result = _delta_arrow({"direction": "worsening", "delta": 10})
        assert "↑" in result
        assert "+10" in result

    def test_improving(self):
        result = _delta_arrow({"direction": "improving", "delta": -15})
        assert "↓" in result
        assert "-15" in result

    def test_stable(self):
        result = _delta_arrow({"direction": "stable", "delta": 2})
        assert result == "→"

    def test_none_input(self):
        assert _delta_arrow(None) == "---"


class TestMarkdownReportWithDelta:
    """Test Markdown report output with delta information."""

    def _make_analysis(self, delta=None):
        return {
            "metadata": {"generated_at": "2026-02-19 10:00:00", "data_mode": "test"},
            "composite": {
                "composite_score": 45,
                "zone": "Orange (Elevated Risk)",
                "zone_color": "orange",
                "risk_budget": "60-75%",
                "guidance": "Test guidance",
                "actions": ["Action 1"],
                "strongest_warning": {
                    "label": "Distribution",
                    "score": 80,
                    "component": "distribution_days",
                },
                "weakest_warning": {"label": "Sentiment", "score": 10, "component": "sentiment"},
                "data_quality": {
                    "label": "Complete (6/6)",
                    "available_count": 6,
                    "total_components": 6,
                    "missing_components": [],
                },
                "correlation_adjustment": [],
                "component_scores": {
                    k: {
                        "score": 50,
                        "adjusted_score": 50,
                        "weight": w,
                        "weighted_contribution": 50 * w,
                        "label": k.replace("_", " ").title(),
                    }
                    for k, w in [
                        ("distribution_days", 0.25),
                        ("leading_stocks", 0.20),
                        ("defensive_rotation", 0.15),
                        ("breadth_divergence", 0.15),
                        ("index_technical", 0.15),
                        ("sentiment", 0.10),
                    ]
                },
            },
            "components": {
                k: {"score": 50, "signal": "TEST"}
                for k in [
                    "distribution_days",
                    "leading_stocks",
                    "defensive_rotation",
                    "breadth_divergence",
                    "index_technical",
                    "sentiment",
                ]
            },
            "follow_through_day": {"applicable": False},
            "delta": delta,
        }

    def test_report_with_delta(self):
        """Report with delta should include Δ column."""
        delta = {
            "components": {
                "distribution_days": {"delta": 10, "direction": "worsening", "previous": 40},
                "leading_stocks": {"delta": -5, "direction": "improving", "previous": 55},
                "defensive_rotation": {"delta": 0, "direction": "stable", "previous": 50},
                "breadth_divergence": {"delta": 2, "direction": "stable", "previous": 48},
                "index_technical": {"delta": -20, "direction": "improving", "previous": 70},
                "sentiment": {"delta": 5, "direction": "worsening", "previous": 45},
            },
            "composite_delta": 3.5,
            "composite_direction": "worsening",
            "previous_date": "2026-02-18 10:00:00",
            "previous_composite": 41.5,
        }
        analysis = self._make_analysis(delta=delta)

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            path = f.name

        try:
            generate_markdown_report(analysis, path)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            assert "Δ" in content
            assert "↑" in content
            assert "vs. Previous Run" in content
        finally:
            os.unlink(path)

    def test_report_without_delta(self):
        """Report without delta should not include Δ column."""
        analysis = self._make_analysis(delta=None)

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            path = f.name

        try:
            generate_markdown_report(analysis, path)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            assert "| Δ |" not in content
        finally:
            os.unlink(path)

    def test_report_with_none_strongest_weakest(self):
        """Report should handle None component for strongest/weakest."""
        analysis = self._make_analysis()
        # Override strongest/weakest to None
        analysis["composite"]["strongest_warning"] = {
            "component": None,
            "label": "N/A",
            "score": 0,
        }
        analysis["composite"]["weakest_warning"] = {
            "component": None,
            "label": "N/A",
            "score": 0,
        }

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            path = f.name

        try:
            generate_markdown_report(analysis, path)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            assert "N/A" in content
            # Should not crash
        finally:
            os.unlink(path)

    def test_report_with_partial_data_count(self):
        """Report should include partial data note when partial_data_count > 0."""
        analysis = self._make_analysis()
        analysis["components"]["leading_stocks"] = {
            "score": 50,
            "signal": "TEST",
            "etfs_evaluated": 8,
            "etfs_deteriorating": 3,
            "deteriorating_pct": 37.5,
            "amplified": False,
            "partial_data_count": 2,
            "etf_details": {},
        }

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            path = f.name

        try:
            generate_markdown_report(analysis, path)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            assert "2 ETF(s) had insufficient history" in content
        finally:
            os.unlink(path)

    def test_first_run_note(self):
        """First run delta should show note."""
        delta = {
            "components": {
                k: {"delta": 0, "direction": "first_run"}
                for k in [
                    "distribution_days",
                    "leading_stocks",
                    "defensive_rotation",
                    "breadth_divergence",
                    "index_technical",
                    "sentiment",
                ]
            },
            "composite_delta": 0,
            "composite_direction": "first_run",
            "previous_date": None,
        }
        analysis = self._make_analysis(delta=delta)

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            path = f.name

        try:
            generate_markdown_report(analysis, path)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            assert "First run" in content
        finally:
            os.unlink(path)
