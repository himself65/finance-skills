#!/usr/bin/env python3
"""
Market Top Detector - Report Generator

Generates JSON and Markdown reports for market top detection analysis.
"""

import json
from typing import Optional


def generate_json_report(analysis: dict, output_file: str):
    """Save full analysis as JSON"""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, default=str)
    print(f"JSON report saved to: {output_file}")


def _delta_arrow(delta_info: Optional[dict]) -> str:
    """Convert delta info to direction arrow."""
    if delta_info is None:
        return "---"
    direction = delta_info.get("direction", "first_run")
    delta = delta_info.get("delta", 0)
    if direction == "first_run":
        return "---"
    elif direction == "worsening":
        return f"+{delta:.0f} ↑"
    elif direction == "improving":
        return f"{delta:.0f} ↓"
    else:
        return "→"


def generate_markdown_report(analysis: dict, output_file: str):
    """Generate comprehensive Markdown report"""
    lines = []
    composite = analysis.get("composite", {})
    components = analysis.get("components", {})
    metadata = analysis.get("metadata", {})
    ftd = analysis.get("follow_through_day", {})
    delta = analysis.get("delta", {})

    score = composite.get("composite_score", 0)
    zone = composite.get("zone", "Unknown")
    risk_budget = composite.get("risk_budget", "N/A")

    # Header
    lines.append("# Market Top Detector Report")
    lines.append("")
    lines.append(f"**Generated:** {metadata.get('generated_at', 'N/A')}")
    lines.append(f"**Data Mode:** {metadata.get('data_mode', 'N/A')}")
    lines.append("")

    # Overall Assessment Box
    lines.append("---")
    lines.append("")
    lines.append("## Overall Assessment")
    lines.append("")
    zone_emoji = _zone_emoji(composite.get("zone_color", ""))
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| **Composite Score** | **{score}/100** |")
    lines.append(f"| **Risk Zone** | {zone_emoji} {zone} |")
    lines.append(f"| **Risk Budget** | {risk_budget} |")
    strongest = composite.get("strongest_warning", {})
    weakest = composite.get("weakest_warning", {})
    strongest_label = strongest.get("label", "N/A") or "N/A"
    weakest_label = weakest.get("label", "N/A") or "N/A"
    strongest_score = strongest.get("score", 0) or 0
    weakest_score = weakest.get("score", 0) or 0
    lines.append(f"| **Strongest Warning** | {strongest_label} ({strongest_score}/100) |")
    lines.append(f"| **Weakest Warning** | {weakest_label} ({weakest_score}/100) |")
    dq = composite.get("data_quality", {})
    if dq:
        lines.append(f"| **Data Quality** | {dq.get('label', 'N/A')} |")
    lines.append("")

    # Guidance
    lines.append(f"> **Guidance:** {composite.get('guidance', '')}")
    lines.append("")

    # Component Scores Table
    lines.append("---")
    lines.append("")
    lines.append("## Component Scores")
    lines.append("")
    lines.append(
        "> **Reading Guide:** Higher score = higher market top risk. "
        "A low score (e.g., Leading Stocks 20/100) means that component "
        "is **healthy** and not signaling danger."
    )
    lines.append("")
    delta_components = delta.get("components", {}) if delta else {}
    has_delta = delta and delta.get("composite_direction") != "first_run"

    if has_delta:
        lines.append("| # | Component | Weight | Score | Δ | Contribution | Signal |")
        lines.append("|---|-----------|--------|-------|---|--------------|--------|")
    else:
        lines.append("| # | Component | Weight | Score | Contribution | Signal |")
        lines.append("|---|-----------|--------|-------|--------------|--------|")

    component_order = [
        "distribution_days",
        "leading_stocks",
        "defensive_rotation",
        "breadth_divergence",
        "index_technical",
        "sentiment",
    ]

    for i, key in enumerate(component_order, 1):
        comp = composite.get("component_scores", {}).get(key, {})
        detail = components.get(key, {})
        signal = detail.get("signal", "N/A")
        score_val = comp.get("score", 0)
        weight_pct = f"{comp.get('weight', 0) * 100:.0f}%"
        contribution = comp.get("weighted_contribution", 0)
        bar = _score_bar(score_val)

        if has_delta:
            d_info = delta_components.get(key)
            arrow = _delta_arrow(d_info)
            lines.append(
                f"| {i} | **{comp.get('label', key)}** | {weight_pct} | "
                f"{bar} {score_val} | {arrow} | {contribution:.1f} | {signal} |"
            )
        else:
            lines.append(
                f"| {i} | **{comp.get('label', key)}** | {weight_pct} | "
                f"{bar} {score_val} | {contribution:.1f} | {signal} |"
            )

    lines.append("")

    # Delta summary
    if has_delta:
        prev_date = delta.get("previous_date", "N/A")
        prev_composite = delta.get("previous_composite", 0)
        comp_delta = delta.get("composite_delta", 0)
        comp_dir = delta.get("composite_direction", "stable")
        dir_arrow = "↑" if comp_dir == "worsening" else "↓" if comp_dir == "improving" else "→"
        lines.append(
            f"**vs. Previous Run ({prev_date}):** Score {prev_composite} → "
            f"{score} ({comp_delta:+.1f} {dir_arrow})"
        )
        lines.append("")
    elif delta and delta.get("composite_direction") == "first_run":
        lines.append("*First run - no comparison available.*")
        lines.append("")

    # Detailed Component Breakdowns
    lines.append("---")
    lines.append("")
    lines.append("## Component Details")
    lines.append("")

    # Component 1: Distribution Days
    dist = components.get("distribution_days", {})
    lines.append("### 1. Distribution Day Count")
    lines.append("")
    if dist:
        sp = dist.get("sp500", {})
        nq = dist.get("nasdaq", {})
        lines.append(
            f"- **Effective Count:** {dist.get('effective_count', 0)} "
            f"(Primary: {dist.get('primary_index', 'N/A')})"
        )
        lines.append(
            f"- **S&P 500:** {sp.get('distribution_days', 0)} distribution + "
            f"{sp.get('stalling_days', 0)} stalling"
        )
        lines.append(
            f"- **NASDAQ:** {nq.get('distribution_days', 0)} distribution + "
            f"{nq.get('stalling_days', 0)} stalling"
        )
        # Distribution day details
        for idx_name, idx_data in [("S&P 500", sp), ("NASDAQ", nq)]:
            details = idx_data.get("details", [])
            if details:
                lines.append(f"\n**{idx_name} Distribution Events:**")
                for d in details[:5]:
                    lines.append(
                        f"  - {d.get('date', '?')}: {d.get('type', '?')} "
                        f"({d.get('pct_change', 0):+.2f}%, vol {d.get('volume_change', 0):+.1f}%)"
                    )
    lines.append("")

    # Component 2: Leading Stock Health
    lead = components.get("leading_stocks", {})
    lines.append("### 2. Leading Stock Health")
    lines.append("")
    if lead:
        lines.append(f"- **ETFs Evaluated:** {lead.get('etfs_evaluated', 0)}")
        lines.append(
            f"- **ETFs Deteriorating:** {lead.get('etfs_deteriorating', 0)} "
            f"({lead.get('deteriorating_pct', 0):.0f}%)"
        )
        lines.append(
            f"- **Amplification Applied:** {'Yes (60%+ deteriorating)' if lead.get('amplified') else 'No'}"
        )
        partial_count = lead.get("partial_data_count", 0)
        if partial_count > 0:
            lines.append(
                f"- **Note:** {partial_count} ETF(s) had insufficient history for full analysis."
            )
        etf_details = lead.get("etf_details", {})
        if etf_details:
            lines.append("")
            lines.append("| ETF | Score | Distance from High | Flags |")
            lines.append("|-----|-------|--------------------|-------|")
            for sym, det in sorted(
                etf_details.items(), key=lambda x: x[1].get("deterioration_score", 0), reverse=True
            ):
                flags = det.get("flags", [])
                flags_joined = "; ".join(flags)
                flags_str = flags_joined if len(flags_joined) <= 80 else flags_joined[:77] + "..."
                lines.append(
                    f"| {sym} | {det.get('deterioration_score', 0)} | "
                    f"{det.get('distance_from_high_pct', 0):+.1f}% | {flags_str} |"
                )
    lines.append("")

    # Component 3: Defensive Rotation
    defr = components.get("defensive_rotation", {})
    lines.append("### 3. Defensive Sector Rotation")
    lines.append("")
    if defr:
        lines.append(
            f"- **Relative Performance (Def - Off):** "
            f"{defr.get('relative_performance', 0):+.2f}% "
            f"(over {defr.get('lookback_days', 20)} days)"
        )
        lines.append(f"- **Defensive Avg Return:** {defr.get('defensive_avg_return', 0):+.2f}%")
        lines.append(f"- **Offensive Avg Return:** {defr.get('offensive_avg_return', 0):+.2f}%")

        def_det = defr.get("defensive_details", {})
        off_det = defr.get("offensive_details", {})
        if def_det or off_det:
            lines.append("")
            lines.append("| Defensive ETF | Return | | Offensive ETF | Return |")
            lines.append("|---------------|--------|-|---------------|--------|")
            def_items = list(def_det.items())
            off_items = list(off_det.items())
            max_len = max(len(def_items), len(off_items))
            for j in range(max_len):
                d_sym = def_items[j][0] if j < len(def_items) else ""
                d_ret = f"{def_items[j][1]:+.2f}%" if j < len(def_items) else ""
                o_sym = off_items[j][0] if j < len(off_items) else ""
                o_ret = f"{off_items[j][1]:+.2f}%" if j < len(off_items) else ""
                lines.append(f"| {d_sym} | {d_ret} | | {o_sym} | {o_ret} |")
    lines.append("")

    # Component 4: Breadth
    brd = components.get("breadth_divergence", {})
    lines.append("### 4. Market Breadth Divergence")
    lines.append("")
    if brd:
        breadth_source = brd.get("breadth_source", "cli")
        if breadth_source == "auto":
            auto_date = brd.get("breadth_auto_date", "N/A")
            source_label = f"auto (TraderMonty CSV, {auto_date})"
        else:
            source_label = "manual (CLI input)"
        lines.append(f"- **200DMA Breadth:** {brd.get('breadth_200dma', 'N/A')}% — {source_label}")
        lines.append(f"- **50DMA Breadth:** {brd.get('breadth_50dma', 'N/A')}%")
        lines.append(
            f"- **Index Near Highs:** {'Yes' if brd.get('index_near_highs') else 'No'} "
            f"({brd.get('index_distance_from_high_pct', 0):+.1f}% from 52wk high)"
        )
        lines.append(
            f"- **Divergence Detected:** {'YES' if brd.get('divergence_detected') else 'No'}"
        )
    lines.append("")

    # Component 5: Index Technical
    tech = components.get("index_technical", {})
    lines.append("### 5. Index Technical Condition")
    lines.append("")
    if tech:
        for idx_name in ["sp500", "nasdaq"]:
            idx = tech.get(idx_name, {})
            if idx:
                label = "S&P 500" if idx_name == "sp500" else "NASDAQ"
                lines.append(f"**{label}:** (Score: {idx.get('raw_score', 0)})")
                for flag in idx.get("flags", []):
                    lines.append(f"  - {flag}")
                mas = idx.get("mas", {})
                if mas:
                    ma_str = ", ".join([f"{k}: ${v}" for k, v in mas.items()])
                    lines.append(f"  - Moving Averages: {ma_str}")
                lines.append("")
    lines.append("")

    # Component 6: Sentiment
    sent = components.get("sentiment", {})
    lines.append("### 6. Sentiment & Speculation")
    lines.append("")
    if sent:
        details = sent.get("details", {})
        pc = details.get("put_call_ratio", {})
        vix = details.get("vix_level", {})
        vts = details.get("vix_term_structure", {})
        md = details.get("margin_debt", {})

        lines.append(
            f"- **Put/Call Ratio:** {pc.get('value', 'N/A')} "
            f"(+{pc.get('points', 0)}pt) - {pc.get('interpretation', '')}"
        )
        lines.append(
            f"- **VIX Level:** {vix.get('value', 'N/A')} "
            f"({vix.get('points', 0):+d}pt) - {vix.get('interpretation', '')}"
        )
        lines.append(
            f"- **VIX Term Structure:** {vts.get('value', 'N/A')} "
            f"({vts.get('points', 0):+d}pt) - {vts.get('interpretation', '')}"
        )
        if md:
            lines.append(
                f"- **Margin Debt YoY:** {md.get('yoy_pct', 'N/A')}% "
                f"({md.get('points', 0):+d}pt) - {md.get('interpretation', '')}"
            )
    lines.append("")

    # Follow-Through Day Monitor
    if ftd and ftd.get("applicable"):
        lines.append("---")
        lines.append("")
        lines.append("## Follow-Through Day Monitor")
        lines.append("")
        if ftd.get("ftd_detected"):
            lines.append(f"**FTD DETECTED** on {ftd.get('ftd_day', 'N/A')}")
        else:
            lines.append(f"- Rally Day Count: {ftd.get('rally_day_count', 0)}")
        lines.append(f"- {ftd.get('reason', '')}")
        lines.append("")

    # Recommended Actions
    lines.append("---")
    lines.append("")
    lines.append("## Recommended Actions")
    lines.append("")
    lines.append(f"**Risk Zone:** {zone}")
    lines.append(f"**Risk Budget:** {risk_budget}")
    lines.append("")
    for action in composite.get("actions", []):
        lines.append(f"- {action}")
    lines.append("")

    # Historical Comparison
    hist_comp = analysis.get("historical_comparison", {})
    if hist_comp:
        lines.append("---")
        lines.append("")
        lines.append("## Historical Comparison")
        lines.append("")
        lines.append(
            f"**Closest Pattern:** {hist_comp.get('closest_match', 'N/A')} "
            f"(SSD: {hist_comp.get('closest_ssd', 'N/A')})"
        )
        lines.append("")
        lines.append(f"> {hist_comp.get('narrative', '')}")
        lines.append("")

        comparisons = hist_comp.get("comparisons", [])
        if comparisons:
            lines.append("| Historical Top | SSD (lower = closer) |")
            lines.append("|---------------|---------------------|")
            for c in comparisons:
                lines.append(f"| {c['name']} | {c['ssd']} |")
            lines.append("")

    # What-If Scenarios
    scenarios = analysis.get("scenarios", [])
    if scenarios:
        lines.append("---")
        lines.append("")
        lines.append("## What-If Scenarios")
        lines.append("")
        lines.append("| Scenario | Description | New Score | Zone | Delta |")
        lines.append("|----------|-------------|-----------|------|-------|")
        for s in scenarios:
            delta_str = f"{s['delta']:+.1f}" if s["delta"] != 0 else "0.0"
            lines.append(
                f"| **{s['name']}** | {s['description']} | "
                f"{s['new_score']} | {s['new_zone']} | {delta_str} |"
            )
        lines.append("")

    # Additional Context
    extra = analysis.get("additional_context", {})
    if extra:
        lines.append("---")
        lines.append("")
        lines.append("## Additional Context (Not Scored)")
        lines.append("")
        for key, value in extra.items():
            lines.append(f"- **{key}:** {value}")
        lines.append("")

    # Methodology
    lines.append("---")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("This analysis integrates three complementary market top detection approaches:")
    lines.append("")
    lines.append(
        "1. **O'Neil (Distribution Days):** Institutional selling pressure via volume-confirmed declines"
    )
    lines.append(
        "2. **Minervini (Leading Stock Deterioration):** Growth leadership breakdown pattern"
    )
    lines.append(
        "3. **Monty (Defensive Rotation):** Capital flow from offensive to defensive sectors"
    )
    lines.append("")
    lines.append(
        "Additional components (Breadth, Technical, Sentiment) provide confirmation signals."
    )
    lines.append("Composite score is a weighted average of all 6 components (0-100 scale).")
    lines.append("")
    lines.append("For detailed methodology, see `references/market_top_methodology.md`.")
    lines.append("")

    # Disclaimer
    lines.append("---")
    lines.append("")
    lines.append(
        "**Disclaimer:** This analysis is for educational and informational purposes only. "
        "Not investment advice. Past patterns may not predict future outcomes. "
        "Conduct your own research and consult a financial advisor before making "
        "investment decisions."
    )
    lines.append("")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Markdown report saved to: {output_file}")


def _zone_emoji(color: str) -> str:
    mapping = {
        "green": "🟢",
        "yellow": "🟡",
        "orange": "🟠",
        "red": "🔴",
        "critical": "⚫",
    }
    return mapping.get(color, "⚪")


def _score_bar(score: int) -> str:
    """Simple text bar for score visualization"""
    if score >= 80:
        return "████"
    elif score >= 60:
        return "███░"
    elif score >= 40:
        return "██░░"
    elif score >= 20:
        return "█░░░"
    else:
        return "░░░░"
