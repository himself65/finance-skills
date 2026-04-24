#!/usr/bin/env python3
"""
Exposure Coach - Calculate market posture and exposure recommendation.

Synthesizes signals from multiple upstream skills to produce a unified
exposure ceiling, bias direction, and action recommendation.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Component weights for composite score
WEIGHTS = {
    "regime": 0.25,
    "top_risk": 0.20,
    "breadth": 0.15,
    "uptrend": 0.15,
    "institutional": 0.10,
    "sector": 0.05,
    "theme": 0.05,
    "ftd": 0.05,
}

# Critical inputs that reduce confidence when missing
CRITICAL_INPUTS = {"regime", "top_risk", "breadth"}

# Regime to baseline score mapping
REGIME_SCORES = {
    "broadening": 80,
    "concentration": 60,
    "transitional": 50,
    "inflationary": 40,
    "contraction": 20,
}


def load_json_file(path: Optional[Path]) -> Optional[dict]:
    """Load a JSON file if it exists and is valid."""
    if path is None or not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load {path}: {e}", file=sys.stderr)
        return None


def extract_breadth_score(data: Optional[dict]) -> Optional[int]:
    """Extract breadth score from breadth analyzer output."""
    if data is None:
        return None
    # Support various field names from upstream skill
    if "breadth_score" in data:
        return int(data["breadth_score"])
    if "composite_score" in data:
        return int(data["composite_score"])
    if isinstance(data.get("composite"), dict) and "composite_score" in data["composite"]:
        return int(data["composite"]["composite_score"])
    if "ad_ratio" in data and "nh_nl_ratio" in data:
        ad = data["ad_ratio"]
        nh_nl = data["nh_nl_ratio"]
        if ad > 1.5 and nh_nl > 3.0:
            return 90
        elif ad >= 1.0 and nh_nl >= 1.0:
            return 65
        elif ad >= 0.7 and nh_nl >= 0.5:
            return 40
        else:
            return 20
    return None


def extract_uptrend_score(data: Optional[dict]) -> Optional[int]:
    """Extract uptrend participation score."""
    if data is None:
        return None
    if "uptrend_score" in data:
        return int(data["uptrend_score"])
    if "composite_score" in data:
        return int(data["composite_score"])
    if isinstance(data.get("composite"), dict) and "composite_score" in data["composite"]:
        return int(data["composite"]["composite_score"])
    if "uptrend_pct" in data:
        pct = data["uptrend_pct"]
        if pct > 50:
            return min(100, int(50 + pct))
        elif pct >= 35:
            return int(35 + pct)
        elif pct >= 20:
            return int(20 + pct)
        else:
            return int(pct)
    return None


def extract_regime_score(data: Optional[dict]) -> Optional[int]:
    """Extract regime score from macro-regime-detector output."""
    if data is None:
        return None
    if "regime_score" in data:
        return int(data["regime_score"])
    if "regime" in data:
        regime = data["regime"].lower().strip()
        return REGIME_SCORES.get(regime, 50)
    if "current_regime" in data:
        regime = data["current_regime"].lower().strip()
        return REGIME_SCORES.get(regime, 50)
    return None


def extract_regime_name(data: Optional[dict]) -> str:
    """Extract regime name from data."""
    if data is None:
        return "Unknown"
    if "regime" in data:
        return data["regime"].capitalize()
    if "current_regime" in data:
        return data["current_regime"].capitalize()
    return "Unknown"


def extract_top_risk_score(data: Optional[dict]) -> Optional[int]:
    """Extract top risk score (inverted - high risk = low score)."""
    if data is None:
        return None
    if "top_risk_score" in data:
        return int(data["top_risk_score"])
    if "top_probability" in data:
        prob = data["top_probability"]
        # Invert: high probability = low score
        return max(0, min(100, int(100 - prob)))
    if isinstance(data.get("composite"), dict) and "composite_score" in data["composite"]:
        prob = data["composite"]["composite_score"]
        return max(0, min(100, int(100 - prob)))
    if "distribution_days" in data:
        days = data["distribution_days"]
        if days <= 2:
            return 90
        elif days <= 4:
            return 65
        elif days <= 6:
            return 40
        else:
            return 15
    return None


def extract_ftd_score(data: Optional[dict]) -> Optional[int]:
    """Extract FTD score (inverted - high FTD = low score)."""
    if data is None:
        return None
    if "ftd_score" in data:
        return int(data["ftd_score"])
    if "anomaly_level" in data:
        level = data["anomaly_level"].lower()
        mapping = {"none": 90, "low": 80, "moderate": 55, "elevated": 35, "critical": 15}
        return mapping.get(level, 50)
    return None


def extract_theme_score(data: Optional[dict]) -> Optional[int]:
    """Extract theme strength score."""
    if data is None:
        return None
    if "theme_score" in data:
        return int(data["theme_score"])
    if "theme_strength" in data:
        strength = data["theme_strength"].lower()
        mapping = {"strong": 85, "stable": 65, "rotating": 40, "collapsing": 20}
        return mapping.get(strength, 50)
    return None


def extract_sector_score(data: Optional[dict]) -> Optional[int]:
    """Extract sector condition score."""
    if data is None:
        return None
    if "sector_score" in data:
        return int(data["sector_score"])
    if "dispersion" in data and "leadership" in data:
        disp = data["dispersion"]
        lead = data["leadership"].lower()
        if disp < 0.1 and lead in ["technology", "consumer discretionary"]:
            return 85
        elif disp < 0.2:
            return 65
        elif lead in ["utilities", "staples", "healthcare"]:
            return 35
        else:
            return 50
    return None


def extract_institutional_score(data: Optional[dict]) -> Optional[int]:
    """Extract institutional flow score."""
    if data is None:
        return None
    if "institutional_score" in data:
        return int(data["institutional_score"])
    if "net_flow" in data:
        flow = data["net_flow"]
        if flow > 0.5:
            return 90
        elif flow > 0:
            return 70
        elif flow > -0.5:
            return 40
        else:
            return 20
    if "flow_direction" in data:
        direction = data["flow_direction"].lower()
        mapping = {
            "strong_buying": 90,
            "buying": 70,
            "neutral": 50,
            "selling": 30,
            "strong_selling": 15,
        }
        return mapping.get(direction, 50)
    return None


def calculate_composite_score(
    scores: dict[str, Optional[int]],
) -> tuple[float, list[str], list[str]]:
    """
    Calculate weighted composite score.

    Returns:
        Tuple of (composite_score, inputs_provided, inputs_missing)
    """
    provided = []
    missing = []
    weighted_sum = 0.0
    total_weight = 0.0

    for key, weight in WEIGHTS.items():
        score = scores.get(key)
        if score is not None:
            weighted_sum += score * weight
            total_weight += weight
            provided.append(key)
        else:
            missing.append(key)

    if total_weight == 0:
        return 50.0, provided, missing

    composite = weighted_sum / total_weight

    # Apply haircut for missing critical inputs
    missing_critical = set(missing) & CRITICAL_INPUTS
    haircut = len(missing_critical) * 10
    composite = max(0, composite - haircut)

    return composite, provided, missing


def determine_exposure_ceiling(composite: float) -> int:
    """Map composite score to exposure ceiling percentage."""
    if composite >= 80:
        return min(100, int(90 + (composite - 80)))
    elif composite >= 65:
        return int(70 + (composite - 65) * 1.3)
    elif composite >= 50:
        return int(50 + (composite - 50) * 1.3)
    elif composite >= 35:
        return int(30 + (composite - 35) * 1.3)
    elif composite >= 20:
        return int(10 + (composite - 20) * 1.3)
    else:
        return max(0, int(composite / 2))


def determine_recommendation(
    composite: float, top_risk_score: Optional[int], missing_critical: int
) -> str:
    """Determine action recommendation."""
    # CASH_PRIORITY conditions
    if composite < 30:
        return "CASH_PRIORITY"
    if top_risk_score is not None and top_risk_score < 25:
        return "CASH_PRIORITY"

    # REDUCE_ONLY conditions
    if composite < 50:
        return "REDUCE_ONLY"
    if top_risk_score is not None and top_risk_score < 40:
        return "REDUCE_ONLY"
    if missing_critical >= 2:
        return "REDUCE_ONLY"

    return "NEW_ENTRY_ALLOWED"


def determine_bias(
    regime_name: str,
    theme_score: Optional[int],
    sector_data: Optional[dict],
    institutional_data: Optional[dict],
) -> str:
    """Determine growth vs value bias."""
    regime_lower = regime_name.lower()

    # Strong regime signals
    if regime_lower == "inflationary":
        return "VALUE"
    if regime_lower == "contraction":
        return "DEFENSIVE"

    # Theme strength indicates growth momentum
    if theme_score is not None and theme_score > 60:
        if regime_lower in ["broadening", "concentration"]:
            return "GROWTH"

    # Sector leadership
    if sector_data and "leadership" in sector_data:
        lead = sector_data["leadership"].lower()
        if lead in ["technology", "consumer discretionary", "communications"]:
            return "GROWTH"
        if lead in ["financials", "energy", "materials", "industrials"]:
            return "VALUE"
        if lead in ["utilities", "staples", "healthcare"]:
            return "DEFENSIVE"

    # Institutional flow
    if institutional_data and "sector_flows" in institutional_data:
        flows = institutional_data["sector_flows"]
        if isinstance(flows, dict):
            growth_flow = sum(flows.get(s, 0) for s in ["Technology", "Consumer Discretionary"])
            value_flow = sum(flows.get(s, 0) for s in ["Financials", "Energy", "Industrials"])
            if growth_flow > value_flow + 0.2:
                return "GROWTH"
            if value_flow > growth_flow + 0.2:
                return "VALUE"

    return "NEUTRAL"


def determine_participation(
    uptrend_score: Optional[int], breadth_score: Optional[int], sector_data: Optional[dict]
) -> str:
    """Assess market participation breadth."""
    # Check uptrend and breadth scores
    uptrend_broad = uptrend_score is not None and uptrend_score >= 50
    breadth_broad = breadth_score is not None and breadth_score >= 50

    # Check sector dispersion if available
    low_dispersion = True
    if sector_data and "dispersion" in sector_data:
        low_dispersion = sector_data["dispersion"] < 0.15

    if uptrend_broad and breadth_broad and low_dispersion:
        return "BROAD"
    elif (uptrend_broad or breadth_broad) and low_dispersion:
        return "MODERATE"
    else:
        return "NARROW"


def determine_confidence(provided: list[str], missing: list[str]) -> str:
    """Determine confidence level based on input completeness."""
    n_provided = len(provided)
    missing_critical = len(set(missing) & CRITICAL_INPUTS)

    if n_provided >= 6 and missing_critical == 0:
        return "HIGH"
    elif n_provided >= 4 or missing_critical <= 1:
        return "MEDIUM"
    else:
        return "LOW"


def generate_rationale(
    composite: float,
    recommendation: str,
    participation: str,
    bias: str,
    scores: dict[str, Optional[int]],
    missing: list[str],
) -> str:
    """Generate human-readable rationale."""
    parts = []

    # Participation assessment
    if participation == "BROAD":
        parts.append("Broad participation indicates healthy market internals.")
    elif participation == "NARROW":
        parts.append("Narrow participation suggests fragile market structure.")

    # Top risk assessment
    top_risk = scores.get("top_risk")
    if top_risk is not None:
        if top_risk >= 70:
            parts.append("Low distribution day count supports risk-on posture.")
        elif top_risk < 40:
            parts.append("Elevated top risk signals warrant caution.")

    # Regime context
    regime = scores.get("regime")
    if regime is not None:
        if regime >= 70:
            parts.append("Favorable macro regime supports elevated exposure.")
        elif regime < 40:
            parts.append("Challenging macro regime limits upside exposure.")

    # Missing inputs
    if missing:
        critical_missing = set(missing) & CRITICAL_INPUTS
        if critical_missing:
            parts.append(
                f"Missing critical inputs ({', '.join(critical_missing)}) reduce confidence."
            )

    # Recommendation context
    if recommendation == "CASH_PRIORITY":
        parts.append("Capital preservation is the priority.")
    elif recommendation == "REDUCE_ONLY":
        parts.append("New entries not recommended; consider trimming on strength.")
    else:
        parts.append(f"New positions allowed within the {int(composite)}% ceiling.")

    return " ".join(parts)


def generate_markdown_report(result: dict) -> str:
    """Generate markdown report from result dict."""
    lines = [
        "# Market Posture Summary",
        f"**Date:** {result['generated_at'][:10]} | **Confidence:** {result['confidence']}",
        "",
        f"## Exposure Ceiling: {result['exposure_ceiling_pct']}%",
        "",
        "| Dimension | Score | Status |",
        "|-----------|-------|--------|",
    ]

    # Add component scores
    status_map = {
        (70, 101): "Strong",
        (50, 70): "Healthy",
        (30, 50): "Cautious",
        (0, 30): "Weak",
    }

    for key in [
        "breadth",
        "uptrend",
        "regime",
        "top_risk",
        "ftd",
        "theme",
        "sector",
        "institutional",
    ]:
        score = result["component_scores"].get(f"{key}_score")
        if score is not None:
            status = "N/A"
            for (lo, hi), label in status_map.items():
                if lo <= score < hi:
                    status = label
                    break
            display_name = key.replace("_", " ").title()
            lines.append(f"| {display_name} | {score} | {status} |")

    lines.extend(
        [
            "",
            f"## Recommendation: {result['recommendation']}",
            "",
            f"**Bias:** {result['bias']}",
            f"**Participation:** {result['participation']}",
            "",
            "### Rationale",
            result["rationale"],
            "",
        ]
    )

    if result["inputs_missing"]:
        lines.extend(
            [
                "### Missing Inputs",
                ", ".join(result["inputs_missing"]),
                "",
            ]
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate market exposure posture from upstream skill outputs"
    )
    parser.add_argument("--breadth", type=Path, help="Path to breadth analyzer JSON")
    parser.add_argument("--uptrend", type=Path, help="Path to uptrend analyzer JSON")
    parser.add_argument("--regime", type=Path, help="Path to macro-regime-detector JSON")
    parser.add_argument("--top-risk", type=Path, help="Path to market-top-detector JSON")
    parser.add_argument("--ftd", type=Path, help="Path to ftd-detector JSON")
    parser.add_argument("--theme", type=Path, help="Path to theme-detector JSON")
    parser.add_argument("--sector", type=Path, help="Path to sector-analyst JSON")
    parser.add_argument(
        "--institutional", type=Path, help="Path to institutional-flow-tracker JSON"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Output directory for reports (default: reports/)",
    )
    parser.add_argument("--json-only", action="store_true", help="Output JSON only, skip markdown")

    args = parser.parse_args()

    # Load all inputs
    breadth_data = load_json_file(args.breadth)
    uptrend_data = load_json_file(args.uptrend)
    regime_data = load_json_file(args.regime)
    top_risk_data = load_json_file(args.top_risk)
    ftd_data = load_json_file(args.ftd)
    theme_data = load_json_file(args.theme)
    sector_data = load_json_file(args.sector)
    institutional_data = load_json_file(args.institutional)

    # Extract scores
    scores: dict[str, Optional[int]] = {
        "breadth": extract_breadth_score(breadth_data),
        "uptrend": extract_uptrend_score(uptrend_data),
        "regime": extract_regime_score(regime_data),
        "top_risk": extract_top_risk_score(top_risk_data),
        "ftd": extract_ftd_score(ftd_data),
        "theme": extract_theme_score(theme_data),
        "sector": extract_sector_score(sector_data),
        "institutional": extract_institutional_score(institutional_data),
    }

    # Calculate composite
    composite, provided, missing = calculate_composite_score(scores)

    # Determine outputs
    exposure_ceiling = determine_exposure_ceiling(composite)
    missing_critical = len(set(missing) & CRITICAL_INPUTS)
    recommendation = determine_recommendation(composite, scores["top_risk"], missing_critical)

    regime_name = extract_regime_name(regime_data)
    bias = determine_bias(regime_name, scores["theme"], sector_data, institutional_data)
    participation = determine_participation(scores["uptrend"], scores["breadth"], sector_data)
    confidence = determine_confidence(provided, missing)

    rationale = generate_rationale(composite, recommendation, participation, bias, scores, missing)

    # Build result
    now = datetime.now(timezone.utc)
    result = {
        "schema_version": "1.0",
        "generated_at": now.isoformat(),
        "exposure_ceiling_pct": exposure_ceiling,
        "bias": bias,
        "participation": participation,
        "recommendation": recommendation,
        "confidence": confidence,
        "composite_score": round(composite, 1),
        "component_scores": {f"{k}_score": v for k, v in scores.items() if v is not None},
        "inputs_provided": provided,
        "inputs_missing": missing,
        "rationale": rationale,
    }

    # Ensure output directory exists
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamp for filenames
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")

    # Write JSON
    json_path = args.output_dir / f"exposure_posture_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"JSON report: {json_path}")

    # Write markdown unless --json-only
    if not args.json_only:
        md_content = generate_markdown_report(result)
        md_path = args.output_dir / f"exposure_posture_{timestamp}.md"
        with open(md_path, "w") as f:
            f.write(md_content)
        print(f"Markdown report: {md_path}")

    # Print summary to stdout
    print(f"\nExposure Ceiling: {exposure_ceiling}%")
    print(f"Recommendation: {recommendation}")
    print(f"Bias: {bias}")
    print(f"Confidence: {confidence}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
