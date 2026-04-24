#!/usr/bin/env python3
"""
Uptrend Analyzer - Main Orchestrator

Analyzes market breadth using Monty's Uptrend Ratio Dashboard data.
Generates a 0-100 composite score from 5 components:
1. Market Breadth (Overall) - 30%
2. Sector Participation - 25%
3. Sector Rotation - 15%
4. Momentum - 20%
5. Historical Context - 10%

No API key required - uses free GitHub CSV data.

Usage:
    python3 uptrend_analyzer.py
    python3 uptrend_analyzer.py --output-dir /path/to/output

Output:
    - JSON: uptrend_analysis_YYYY-MM-DD_HHMMSS.json
    - Markdown: uptrend_analysis_YYYY-MM-DD_HHMMSS.md
"""

import argparse
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from calculators.historical_context_calculator import calculate_historical_context
from calculators.market_breadth_calculator import calculate_market_breadth
from calculators.momentum_calculator import calculate_momentum
from calculators.sector_participation_calculator import calculate_sector_participation
from calculators.sector_rotation_calculator import calculate_sector_rotation
from data_fetcher import WORKSHEET_TO_DISPLAY, UptrendDataFetcher
from report_generator import generate_json_report, generate_markdown_report
from scorer import calculate_composite_score


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Uptrend Analyzer - Market Breadth Health Diagnosis"
    )
    parser.add_argument(
        "--output-dir", default="reports/", help="Output directory for reports (default: reports/)"
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    print("=" * 70)
    print("Uptrend Analyzer")
    print("Market Breadth Health Diagnosis via Monty's Uptrend Ratio Dashboard")
    print("=" * 70)
    print()

    # ========================================================================
    # Step 1: Fetch CSV Data
    # ========================================================================
    print("Step 1: Fetching CSV Data")
    print("-" * 70)

    fetcher = UptrendDataFetcher()

    print("  Fetching timeseries data...", end=" ", flush=True)
    timeseries = fetcher.fetch_timeseries()
    if timeseries:
        print(f"OK ({len(timeseries)} rows)")
    else:
        print("FAILED")
        print("ERROR: Cannot proceed without timeseries data", file=sys.stderr)
        sys.exit(1)

    print("  Fetching sector summary...", end=" ", flush=True)
    sector_summary = fetcher.fetch_sector_summary()
    if sector_summary:
        print(f"OK ({len(sector_summary)} sectors)")
    else:
        print("WARN - Sector summary unavailable, some components will use defaults")

    # Extract key data subsets
    all_timeseries = fetcher.get_all_timeseries()
    latest_all = fetcher.get_latest_all()
    sector_latest = fetcher.get_all_sector_latest()

    # Build sector -> (count, total) mapping from timeseries latest rows
    count_total_map = {}
    for ws_name, row in sector_latest.items():
        display_name = WORKSHEET_TO_DISPLAY.get(ws_name, ws_name)
        count_total_map[display_name] = (row.get("count"), row.get("total"))
    # Add count/total to each sector summary row
    for s in sector_summary:
        ct = count_total_map.get(s["Sector"], (None, None))
        s["Count"] = ct[0]
        s["Total"] = ct[1]

    if latest_all:
        ratio_pct = (
            round(latest_all["ratio"] * 100, 1) if latest_all.get("ratio") is not None else "N/A"
        )
        print(
            f"  Latest data: {latest_all.get('date', 'N/A')}, "
            f"ratio={ratio_pct}%, trend={latest_all.get('trend', 'N/A')}"
        )
    print()

    # ========================================================================
    # Step 2: Calculate Components
    # ========================================================================
    print("Step 2: Calculating Components")
    print("-" * 70)

    # Component 1: Market Breadth (30%)
    print("  [1/5] Market Breadth (Overall)...", end=" ", flush=True)
    comp1 = calculate_market_breadth(latest_all, all_timeseries)
    print(f"Score: {comp1['score']} ({comp1['signal']})")

    # Component 2: Sector Participation (25%)
    print("  [2/5] Sector Participation...", end=" ", flush=True)
    comp2 = calculate_sector_participation(sector_summary, sector_latest)
    print(f"Score: {comp2['score']} ({comp2['signal']})")

    # Component 3: Sector Rotation (15%)
    print("  [3/5] Sector Rotation...", end=" ", flush=True)
    comp3 = calculate_sector_rotation(sector_summary, sector_latest)
    print(f"Score: {comp3['score']} ({comp3['signal']})")

    # Component 4: Momentum (20%)
    print("  [4/5] Momentum...", end=" ", flush=True)
    comp4 = calculate_momentum(all_timeseries, sector_summary)
    print(f"Score: {comp4['score']} ({comp4['signal']})")

    # Component 5: Historical Context (10%)
    print("  [5/5] Historical Context...", end=" ", flush=True)
    comp5 = calculate_historical_context(all_timeseries)
    print(f"Score: {comp5['score']} ({comp5['signal']})")

    print()

    # ========================================================================
    # Step 3: Composite Score
    # ========================================================================
    print("Step 3: Calculating Composite Score")
    print("-" * 70)

    component_scores = {
        "market_breadth": comp1["score"],
        "sector_participation": comp2["score"],
        "sector_rotation": comp3["score"],
        "momentum": comp4["score"],
        "historical_context": comp5["score"],
    }

    data_availability = {
        "market_breadth": comp1.get("data_available", True),
        "sector_participation": comp2.get("data_available", True),
        "sector_rotation": comp3.get("data_available", True),
        "momentum": comp4.get("data_available", True),
        "historical_context": comp5.get("data_available", True),
    }

    # Collect warning flags from components
    warning_flags = {
        "late_cycle": comp3.get("late_cycle_flag", False),
        "high_spread": (comp2.get("spread") is not None and comp2["spread"] > 0.40),
        "divergence": comp3.get("divergence_flag", False),
    }

    composite = calculate_composite_score(
        component_scores,
        data_availability,
        warning_flags,
        historical_data_points=comp5.get("data_points"),
    )

    print(f"  Composite Score: {composite['composite_score']}/100")
    print(f"  Zone: {composite['zone']} ({composite.get('zone_detail', '')})")
    print(f"  Exposure Guidance: {composite['exposure_guidance']}")
    if composite.get("warning_penalty", 0) != 0:
        print(
            f"  Warning Penalty: {composite['warning_penalty']} "
            f"(raw score: {composite.get('composite_score_raw', 'N/A')})"
        )
    print(
        f"  Strongest: {composite['strongest_component']['label']} "
        f"({composite['strongest_component']['score']})"
    )
    print(
        f"  Weakest: {composite['weakest_component']['label']} "
        f"({composite['weakest_component']['score']})"
    )
    print()

    # ========================================================================
    # Step 4: Generate Reports
    # ========================================================================
    print("Step 4: Generating Reports")
    print("-" * 70)

    os.makedirs(args.output_dir, exist_ok=True)

    # Build full analysis
    analysis = {
        "metadata": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "Monty's Uptrend Ratio Dashboard (GitHub CSV)",
            "api_key_required": False,
            "latest_data_date": latest_all.get("date", "N/A") if latest_all else "N/A",
            "timeseries_rows": len(timeseries),
            "sectors_available": len(sector_summary),
        },
        "composite": composite,
        "components": {
            "market_breadth": comp1,
            "sector_participation": comp2,
            "sector_rotation": comp3,
            "momentum": comp4,
            "historical_context": comp5,
        },
    }

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    json_file = os.path.join(args.output_dir, f"uptrend_analysis_{timestamp}.json")
    md_file = os.path.join(args.output_dir, f"uptrend_analysis_{timestamp}.md")

    generate_json_report(analysis, json_file)
    generate_markdown_report(analysis, md_file)

    print()
    print("=" * 70)
    print("Uptrend Analysis Complete")
    print("=" * 70)
    print(f"  Composite Score: {composite['composite_score']}/100")
    print(f"  Zone: {composite['zone']}")
    print(f"  Exposure Guidance: {composite['exposure_guidance']}")
    print(f"  JSON Report: {json_file}")
    print(f"  Markdown Report: {md_file}")
    print()


if __name__ == "__main__":
    main()
