"""Tests for calculate_exposure.py."""

import json

from calculate_exposure import (
    CRITICAL_INPUTS,
    WEIGHTS,
    calculate_composite_score,
    determine_bias,
    determine_confidence,
    determine_exposure_ceiling,
    determine_participation,
    determine_recommendation,
    extract_breadth_score,
    extract_regime_score,
    extract_top_risk_score,
    extract_uptrend_score,
    generate_markdown_report,
    generate_rationale,
    load_json_file,
)


class TestExtractBreadthScore:
    """Tests for breadth score extraction."""

    def test_direct_breadth_score(self):
        data = {"breadth_score": 75}
        assert extract_breadth_score(data) == 75

    def test_composite_score_fallback(self):
        data = {"composite_score": 60}
        assert extract_breadth_score(data) == 60

    def test_ad_ratio_calculation_high(self):
        data = {"ad_ratio": 2.0, "nh_nl_ratio": 4.0}
        assert extract_breadth_score(data) == 90

    def test_ad_ratio_calculation_mid(self):
        data = {"ad_ratio": 1.2, "nh_nl_ratio": 1.5}
        assert extract_breadth_score(data) == 65

    def test_ad_ratio_calculation_low(self):
        data = {"ad_ratio": 0.5, "nh_nl_ratio": 0.3}
        assert extract_breadth_score(data) == 20

    def test_none_input(self):
        assert extract_breadth_score(None) is None

    def test_empty_dict(self):
        assert extract_breadth_score({}) is None


class TestExtractUptrendScore:
    """Tests for uptrend score extraction."""

    def test_direct_score(self):
        data = {"uptrend_score": 80}
        assert extract_uptrend_score(data) == 80

    def test_uptrend_pct_high(self):
        data = {"uptrend_pct": 60}
        score = extract_uptrend_score(data)
        assert score >= 75

    def test_uptrend_pct_mid(self):
        data = {"uptrend_pct": 40}
        score = extract_uptrend_score(data)
        assert 50 <= score <= 80

    def test_uptrend_pct_low(self):
        data = {"uptrend_pct": 15}
        score = extract_uptrend_score(data)
        assert score < 30


class TestExtractRegimeScore:
    """Tests for regime score extraction."""

    def test_broadening_regime(self):
        data = {"regime": "Broadening"}
        assert extract_regime_score(data) == 80

    def test_contraction_regime(self):
        data = {"regime": "contraction"}
        assert extract_regime_score(data) == 20

    def test_current_regime_field(self):
        data = {"current_regime": "Transitional"}
        assert extract_regime_score(data) == 50

    def test_direct_regime_score(self):
        data = {"regime_score": 65}
        assert extract_regime_score(data) == 65


class TestExtractTopRiskScore:
    """Tests for top risk score extraction."""

    def test_direct_score(self):
        data = {"top_risk_score": 30}
        assert extract_top_risk_score(data) == 30

    def test_top_probability_high(self):
        # High probability = low score (inverted)
        data = {"top_probability": 80}
        assert extract_top_risk_score(data) == 20

    def test_top_probability_low(self):
        # Low probability = high score
        data = {"top_probability": 10}
        assert extract_top_risk_score(data) == 90

    def test_distribution_days_few(self):
        data = {"distribution_days": 1}
        assert extract_top_risk_score(data) == 90

    def test_distribution_days_many(self):
        data = {"distribution_days": 8}
        assert extract_top_risk_score(data) == 15


class TestCalculateCompositeScore:
    """Tests for composite score calculation."""

    def test_all_inputs_provided(self):
        scores = {
            "regime": 80,
            "top_risk": 70,
            "breadth": 65,
            "uptrend": 60,
            "institutional": 75,
            "sector": 70,
            "theme": 65,
            "ftd": 80,
        }
        composite, provided, missing = calculate_composite_score(scores)
        assert len(provided) == 8
        assert len(missing) == 0
        # Weighted average check
        expected = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
        assert abs(composite - expected) < 0.1

    def test_missing_critical_inputs(self):
        scores = {
            "regime": None,  # critical
            "top_risk": None,  # critical
            "breadth": 65,  # critical but present
            "uptrend": 60,
            "institutional": 75,
            "sector": 70,
            "theme": 65,
            "ftd": 80,
        }
        composite, provided, missing = calculate_composite_score(scores)
        assert "regime" in missing
        assert "top_risk" in missing
        # Haircut applied: 2 critical missing * 10 = 20
        assert len(provided) == 6

    def test_no_inputs(self):
        scores = {k: None for k in WEIGHTS}
        composite, provided, missing = calculate_composite_score(scores)
        assert composite == 50.0  # Default when no inputs
        assert len(provided) == 0
        assert len(missing) == 8


class TestDetermineExposureCeiling:
    """Tests for exposure ceiling mapping."""

    def test_high_composite(self):
        assert determine_exposure_ceiling(90) >= 90

    def test_mid_composite(self):
        ceiling = determine_exposure_ceiling(60)
        assert 50 <= ceiling <= 80

    def test_low_composite(self):
        ceiling = determine_exposure_ceiling(25)
        assert ceiling <= 30

    def test_very_low_composite(self):
        ceiling = determine_exposure_ceiling(10)
        assert ceiling <= 10


class TestDetermineRecommendation:
    """Tests for recommendation logic."""

    def test_cash_priority_low_composite(self):
        rec = determine_recommendation(25, 50, 0)
        assert rec == "CASH_PRIORITY"

    def test_cash_priority_low_top_risk(self):
        rec = determine_recommendation(60, 20, 0)
        assert rec == "CASH_PRIORITY"

    def test_reduce_only_mid_composite(self):
        rec = determine_recommendation(45, 50, 0)
        assert rec == "REDUCE_ONLY"

    def test_reduce_only_missing_critical(self):
        rec = determine_recommendation(60, 50, 2)
        assert rec == "REDUCE_ONLY"

    def test_new_entry_allowed(self):
        rec = determine_recommendation(70, 60, 0)
        assert rec == "NEW_ENTRY_ALLOWED"


class TestDetermineBias:
    """Tests for bias determination."""

    def test_inflationary_regime(self):
        bias = determine_bias("Inflationary", 50, None, None)
        assert bias == "VALUE"

    def test_contraction_regime(self):
        bias = determine_bias("Contraction", 50, None, None)
        assert bias == "DEFENSIVE"

    def test_broadening_with_strong_theme(self):
        bias = determine_bias("Broadening", 75, None, None)
        assert bias == "GROWTH"

    def test_sector_leadership_technology(self):
        sector_data = {"leadership": "Technology"}
        bias = determine_bias("Transitional", 50, sector_data, None)
        assert bias == "GROWTH"

    def test_sector_leadership_financials(self):
        sector_data = {"leadership": "Financials"}
        bias = determine_bias("Transitional", 50, sector_data, None)
        assert bias == "VALUE"

    def test_neutral_default(self):
        bias = determine_bias("Transitional", 50, None, None)
        assert bias == "NEUTRAL"


class TestDetermineParticipation:
    """Tests for participation assessment."""

    def test_broad_participation(self):
        part = determine_participation(70, 65, {"dispersion": 0.05})
        assert part == "BROAD"

    def test_narrow_participation(self):
        part = determine_participation(30, 35, {"dispersion": 0.25})
        assert part == "NARROW"

    def test_moderate_participation(self):
        part = determine_participation(55, 40, {"dispersion": 0.10})
        assert part == "MODERATE"


class TestDetermineConfidence:
    """Tests for confidence level."""

    def test_high_confidence(self):
        provided = list(WEIGHTS.keys())[:6]
        missing = list(WEIGHTS.keys())[6:]
        # Remove critical from missing
        missing = [m for m in missing if m not in CRITICAL_INPUTS]
        conf = determine_confidence(provided, missing)
        assert conf == "HIGH"

    def test_medium_confidence(self):
        provided = ["regime", "breadth", "uptrend", "sector"]
        missing = ["top_risk", "ftd", "theme", "institutional"]
        conf = determine_confidence(provided, missing)
        assert conf == "MEDIUM"

    def test_low_confidence(self):
        provided = ["sector", "theme"]
        missing = ["regime", "top_risk", "breadth", "uptrend", "ftd", "institutional"]
        conf = determine_confidence(provided, missing)
        assert conf == "LOW"


class TestGenerateRationale:
    """Tests for rationale generation."""

    def test_rationale_includes_participation(self):
        rationale = generate_rationale(
            70, "NEW_ENTRY_ALLOWED", "BROAD", "GROWTH", {"top_risk": 80, "regime": 75}, []
        )
        assert "Broad participation" in rationale

    def test_rationale_includes_missing_inputs(self):
        rationale = generate_rationale(
            60, "REDUCE_ONLY", "MODERATE", "NEUTRAL", {"breadth": 60}, ["regime", "top_risk"]
        )
        assert "Missing critical inputs" in rationale

    def test_rationale_cash_priority(self):
        rationale = generate_rationale(
            25, "CASH_PRIORITY", "NARROW", "DEFENSIVE", {"top_risk": 20}, []
        )
        assert "preservation" in rationale.lower()


class TestGenerateMarkdownReport:
    """Tests for markdown report generation."""

    def test_markdown_contains_exposure(self):
        result = {
            "generated_at": "2026-03-16T07:00:00Z",
            "confidence": "HIGH",
            "exposure_ceiling_pct": 75,
            "component_scores": {
                "breadth_score": 65,
                "regime_score": 80,
            },
            "recommendation": "NEW_ENTRY_ALLOWED",
            "bias": "GROWTH",
            "participation": "BROAD",
            "rationale": "Test rationale.",
            "inputs_missing": [],
        }
        md = generate_markdown_report(result)
        assert "75%" in md
        assert "NEW_ENTRY_ALLOWED" in md
        assert "GROWTH" in md

    def test_markdown_includes_missing(self):
        result = {
            "generated_at": "2026-03-16T07:00:00Z",
            "confidence": "MEDIUM",
            "exposure_ceiling_pct": 50,
            "component_scores": {"breadth_score": 60},
            "recommendation": "REDUCE_ONLY",
            "bias": "NEUTRAL",
            "participation": "NARROW",
            "rationale": "Caution advised.",
            "inputs_missing": ["regime", "top_risk"],
        }
        md = generate_markdown_report(result)
        assert "Missing Inputs" in md
        assert "regime" in md


class TestLoadJsonFile:
    """Tests for JSON file loading."""

    def test_load_valid_file(self, tmp_path):
        test_file = tmp_path / "test.json"
        test_data = {"key": "value"}
        test_file.write_text(json.dumps(test_data))
        result = load_json_file(test_file)
        assert result == test_data

    def test_load_nonexistent_file(self, tmp_path):
        result = load_json_file(tmp_path / "nonexistent.json")
        assert result is None

    def test_load_none_path(self):
        result = load_json_file(None)
        assert result is None

    def test_load_invalid_json(self, tmp_path):
        test_file = tmp_path / "invalid.json"
        test_file.write_text("not valid json")
        result = load_json_file(test_file)
        assert result is None


class TestIntegration:
    """Integration tests for the full pipeline."""

    def test_full_pipeline_with_all_inputs(self, tmp_path):
        """Test complete flow with all inputs provided."""
        import sys

        from calculate_exposure import main

        # Create mock input files
        breadth_file = tmp_path / "breadth.json"
        breadth_file.write_text(json.dumps({"breadth_score": 70}))

        regime_file = tmp_path / "regime.json"
        regime_file.write_text(json.dumps({"regime": "Broadening"}))

        top_risk_file = tmp_path / "top_risk.json"
        top_risk_file.write_text(json.dumps({"top_risk_score": 75}))

        uptrend_file = tmp_path / "uptrend.json"
        uptrend_file.write_text(json.dumps({"uptrend_score": 65}))

        output_dir = tmp_path / "reports"

        # Mock sys.argv
        original_argv = sys.argv
        sys.argv = [
            "calculate_exposure.py",
            "--breadth",
            str(breadth_file),
            "--regime",
            str(regime_file),
            "--top-risk",
            str(top_risk_file),
            "--uptrend",
            str(uptrend_file),
            "--output-dir",
            str(output_dir),
            "--json-only",
        ]

        try:
            result = main()
            assert result == 0

            # Check output files exist
            json_files = list(output_dir.glob("exposure_posture_*.json"))
            assert len(json_files) == 1

            # Validate JSON content
            with open(json_files[0]) as f:
                data = json.load(f)
            assert "exposure_ceiling_pct" in data
            assert "recommendation" in data
            assert data["confidence"] in ["HIGH", "MEDIUM", "LOW"]
        finally:
            sys.argv = original_argv

    def test_partial_inputs_reduce_confidence(self, tmp_path):
        """Test that missing critical inputs reduce confidence."""
        import sys

        from calculate_exposure import main

        # Create only one non-critical input
        sector_file = tmp_path / "sector.json"
        sector_file.write_text(json.dumps({"sector_score": 60}))

        output_dir = tmp_path / "reports"

        original_argv = sys.argv
        sys.argv = [
            "calculate_exposure.py",
            "--sector",
            str(sector_file),
            "--output-dir",
            str(output_dir),
            "--json-only",
        ]

        try:
            result = main()
            assert result == 0

            json_files = list(output_dir.glob("exposure_posture_*.json"))
            with open(json_files[0]) as f:
                data = json.load(f)

            # All critical inputs missing → LOW confidence
            assert data["confidence"] == "LOW"
            # Missing critical inputs triggers haircut → lower exposure
            assert data["exposure_ceiling_pct"] < 50
        finally:
            sys.argv = original_argv
