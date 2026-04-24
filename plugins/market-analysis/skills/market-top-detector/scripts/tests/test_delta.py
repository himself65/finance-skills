"""Tests for Delta Tracking (load_previous_report, compute_deltas)"""

import json
import os
import tempfile

from market_top_detector import _compute_deltas, _load_previous_report


class TestLoadPreviousReport:
    """Test loading previous JSON report."""

    def test_no_files_returns_none(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = _load_previous_report(tmpdir)
            assert result is None

    def test_loads_latest_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create two report files
            for ts in ["2026-02-18_100000", "2026-02-19_100000"]:
                path = os.path.join(tmpdir, f"market_top_{ts}.json")
                with open(path, "w") as f:
                    json.dump({"timestamp": ts}, f)
            result = _load_previous_report(tmpdir)
            assert result["timestamp"] == "2026-02-19_100000"

    def test_invalid_json_returns_none(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "market_top_2026-02-19_100000.json")
            with open(path, "w") as f:
                f.write("not json")
            result = _load_previous_report(tmpdir)
            assert result is None


class TestComputeDeltas:
    """Test delta computation."""

    def test_no_previous_all_first_run(self):
        scores = {
            "distribution_days": 50,
            "leading_stocks": 40,
            "defensive_rotation": 30,
            "breadth_divergence": 20,
            "index_technical": 10,
            "sentiment": 5,
        }
        result = _compute_deltas(scores, None)
        for _key, info in result["components"].items():
            assert info["direction"] == "first_run"
        assert result["composite_direction"] == "first_run"

    def test_worsening_detected(self):
        scores = {
            "distribution_days": 80,
            "leading_stocks": 50,
            "defensive_rotation": 50,
            "breadth_divergence": 50,
            "index_technical": 50,
            "sentiment": 50,
        }
        prev = {
            "components": {
                "distribution_days": {"score": 60},
                "leading_stocks": {"score": 50},
                "defensive_rotation": {"score": 50},
                "breadth_divergence": {"score": 50},
                "index_technical": {"score": 50},
                "sentiment": {"score": 50},
            },
            "composite": {"composite_score": 52},
            "metadata": {"generated_at": "2026-02-18 10:00:00"},
        }
        result = _compute_deltas(scores, prev)
        assert result["components"]["distribution_days"]["direction"] == "worsening"
        assert result["components"]["distribution_days"]["delta"] == 20

    def test_improving_detected(self):
        scores = {
            "distribution_days": 30,
            "leading_stocks": 50,
            "defensive_rotation": 50,
            "breadth_divergence": 50,
            "index_technical": 50,
            "sentiment": 50,
        }
        prev = {
            "components": {
                "distribution_days": {"score": 60},
                "leading_stocks": {"score": 50},
                "defensive_rotation": {"score": 50},
                "breadth_divergence": {"score": 50},
                "index_technical": {"score": 50},
                "sentiment": {"score": 50},
            },
            "composite": {"composite_score": 52},
            "metadata": {"generated_at": "2026-02-18"},
        }
        result = _compute_deltas(scores, prev)
        assert result["components"]["distribution_days"]["direction"] == "improving"
        assert result["components"]["distribution_days"]["delta"] == -30

    def test_stable_within_3(self):
        scores = {
            "distribution_days": 52,
            "leading_stocks": 50,
            "defensive_rotation": 50,
            "breadth_divergence": 50,
            "index_technical": 50,
            "sentiment": 50,
        }
        prev = {
            "components": {
                "distribution_days": {"score": 50},
                "leading_stocks": {"score": 50},
                "defensive_rotation": {"score": 50},
                "breadth_divergence": {"score": 50},
                "index_technical": {"score": 50},
                "sentiment": {"score": 50},
            },
            "composite": {"composite_score": 50},
            "metadata": {"generated_at": "2026-02-18"},
        }
        result = _compute_deltas(scores, prev)
        assert result["components"]["distribution_days"]["direction"] == "stable"
