"""Tests for report_generator helper functions and integration."""

import os
import tempfile

import pytest
from report_generator import (
    _format_slope,
    _score_bar,
    _zone_emoji,
    generate_json_report,
    generate_markdown_report,
)

# --- _zone_emoji ---


def test_zone_emoji_green():
    assert _zone_emoji("green") == "\U0001f7e2"


def test_zone_emoji_all_colors():
    assert _zone_emoji("green") == "\U0001f7e2"
    assert _zone_emoji("light_green") == "\U0001f7e2"
    assert _zone_emoji("yellow") == "\U0001f7e1"
    assert _zone_emoji("orange") == "\U0001f7e0"
    assert _zone_emoji("red") == "\U0001f534"


def test_zone_emoji_unknown():
    assert _zone_emoji("purple") == "\u26aa"


# --- _format_slope ---


def test_format_slope_positive():
    assert _format_slope(0.0025) == "+0.0025"


def test_format_slope_negative():
    assert _format_slope(-0.003) == "-0.0030"


def test_format_slope_none():
    assert _format_slope(None) == "N/A"


# --- _score_bar ---


def test_score_bar_all_tiers():
    assert _score_bar(80) == "\u2588\u2588\u2588\u2588"
    assert _score_bar(95) == "\u2588\u2588\u2588\u2588"
    assert _score_bar(60) == "\u2588\u2588\u2588\u2591"
    assert _score_bar(79) == "\u2588\u2588\u2588\u2591"
    assert _score_bar(40) == "\u2588\u2588\u2591\u2591"
    assert _score_bar(59) == "\u2588\u2588\u2591\u2591"
    assert _score_bar(20) == "\u2588\u2591\u2591\u2591"
    assert _score_bar(39) == "\u2588\u2591\u2591\u2591"
    assert _score_bar(19) == "\u2591\u2591\u2591\u2591"
    assert _score_bar(0) == "\u2591\u2591\u2591\u2591"


# --- generate_markdown_report integration ---


def _make_analysis(with_warnings=True):
    """Build a synthetic analysis dict for report generation."""
    warnings = []
    if with_warnings:
        warnings = [
            {
                "label": "Breadth-Momentum Divergence",
                "description": "Ratio above median but momentum weak",
                "actions": ["Monitor momentum recovery", "Tighten stops"],
            },
        ]

    return {
        "composite": {
            "composite_score": 72,
            "composite_score_raw": 77,
            "zone": "Bull",
            "zone_detail": "Bull-Upper",
            "zone_color": "light_green",
            "zone_proximity": {"at_boundary": False},
            "exposure_guidance": "Normal Exposure (80-100%)",
            "warning_penalty": -5 if with_warnings else 0,
            "active_warnings": warnings,
            "strongest_component": {"label": "Market Breadth", "score": 85},
            "weakest_component": {"label": "Momentum", "score": 38},
            "data_quality": {"label": "Good"},
            "guidance": "Market breadth is healthy.",
            "actions": ["Maintain positions", "Watch momentum"],
            "component_scores": {
                "market_breadth": {
                    "label": "Market Breadth",
                    "score": 85,
                    "weight": 0.30,
                    "weighted_contribution": 25.5,
                },
                "sector_participation": {
                    "label": "Sector Participation",
                    "score": 70,
                    "weight": 0.25,
                    "weighted_contribution": 17.5,
                },
                "sector_rotation": {
                    "label": "Sector Rotation",
                    "score": 60,
                    "weight": 0.15,
                    "weighted_contribution": 9.0,
                },
                "momentum": {
                    "label": "Momentum",
                    "score": 38,
                    "weight": 0.20,
                    "weighted_contribution": 7.6,
                },
                "historical_context": {
                    "label": "Historical Context",
                    "score": 65,
                    "weight": 0.10,
                    "weighted_contribution": 6.5,
                },
            },
        },
        "components": {
            "market_breadth": {
                "data_available": True,
                "ratio_pct": 30.0,
                "ma_10_pct": 28.0,
                "trend": "Up",
                "slope": 0.0015,
                "distance_from_upper": 0.07,
                "distance_from_lower": 0.203,
                "trend_adjustment": 5,
                "date": "2026-01-15",
                "signal": "HEALTHY BREADTH",
            },
            "sector_participation": {
                "data_available": True,
                "uptrend_count": 8,
                "total_sectors": 11,
                "count_score": 73,
                "spread_pct": 15.0,
                "spread_score": 60,
                "overbought_count": 1,
                "overbought_sectors": ["Technology"],
                "oversold_count": 0,
                "oversold_sectors": [],
                "sector_details": [
                    {
                        "sector": "Technology",
                        "ratio_pct": 35.0,
                        "ma_10": 0.33,
                        "trend": "Up",
                        "slope": 0.002,
                        "status": "Normal",
                    },
                ],
                "signal": "BROAD PARTICIPATION",
            },
            "sector_rotation": {
                "data_available": True,
                "cyclical_avg_pct": 28.0,
                "defensive_avg_pct": 20.0,
                "commodity_avg_pct": 25.0,
                "difference_pct": 8.0,
                "late_cycle_flag": False,
                "divergence_flag": False,
                "signal": "RISK-ON ROTATION",
            },
            "momentum": {
                "data_available": True,
                "slope": 0.0015,
                "slope_smoothed": 0.0014,
                "slope_smoothing": "EMA(3)",
                "slope_score": 65,
                "acceleration": 0.0002,
                "acceleration_label": "steady",
                "acceleration_score": 50,
                "acceleration_window": "10v10",
                "sector_positive_slope_count": 7,
                "sector_total": 11,
                "sector_slope_breadth_score": 64,
                "signal": "POSITIVE MOMENTUM",
            },
            "historical_context": {
                "data_available": True,
                "current_ratio_pct": 30.0,
                "percentile": 55,
                "historical_min_pct": 5.0,
                "historical_max_pct": 45.0,
                "historical_median_pct": 27.0,
                "avg_30d_pct": 29.0,
                "avg_90d_pct": 26.0,
                "data_points": 500,
                "date_range": "2023-08 to 2026-01",
                "confidence": {
                    "confidence_level": "High",
                    "sample_label": "500 pts",
                    "regime_coverage": "3/3",
                    "recency_label": "fresh",
                },
                "signal": "ABOVE MEDIAN",
            },
        },
        "metadata": {
            "generated_at": "2026-01-15T12:00:00",
        },
    }


def _generate_report(with_warnings=True):
    """Generate report to temp file and return its content."""
    analysis = _make_analysis(with_warnings=with_warnings)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        tmp_path = f.name
    try:
        generate_markdown_report(analysis, tmp_path)
        with open(tmp_path, encoding="utf-8") as f:
            return f.read()
    finally:
        os.unlink(tmp_path)


class TestMarkdownReportIntegration:
    def test_overall_assessment_section_present(self):
        content = _generate_report()
        assert "## Overall Assessment" in content

    def test_active_warnings_section_when_warnings(self):
        content = _generate_report(with_warnings=True)
        assert "## Active Warnings" in content

    def test_no_warnings_section_when_none(self):
        content = _generate_report(with_warnings=False)
        assert "## Active Warnings" not in content

    def test_component_scores_section_present(self):
        content = _generate_report()
        assert "## Component Scores" in content

    def test_sector_heatmap_section_present(self):
        content = _generate_report()
        assert "## Sector Heatmap" in content

    def test_zone_detail_row_present(self):
        content = _generate_report()
        assert "Zone Detail" in content
        assert "Bull-Upper" in content

    def test_warning_penalty_row_present(self):
        content = _generate_report(with_warnings=True)
        assert "Warning Penalty" in content

    def test_confidence_row_present(self):
        content = _generate_report()
        assert "Confidence" in content


# --- File I/O error handling ---


def test_json_report_write_error(tmp_path):
    """OSError is re-raised with stderr message."""
    bad_path = str(tmp_path / "nonexistent_dir" / "report.json")
    with pytest.raises(OSError):
        generate_json_report({"test": True}, bad_path)


def test_markdown_report_write_error(tmp_path):
    """OSError is re-raised with stderr message."""
    bad_path = str(tmp_path / "nonexistent_dir" / "report.md")
    with pytest.raises(OSError):
        generate_markdown_report(_make_analysis(), bad_path)
