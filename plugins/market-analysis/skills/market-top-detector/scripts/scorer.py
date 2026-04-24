#!/usr/bin/env python3
"""
Market Top Detector - Composite Scoring Engine

Combines 6 component scores into a weighted composite (0-100).

Component Weights:
1. Distribution Day Count:       25%
2. Leading Stock Health:         20%
3. Defensive Sector Rotation:    15%
4. Market Breadth Divergence:    15%
5. Index Technical Condition:    15%
6. Sentiment & Speculation:      10%
Total: 100%

Risk Zone Mapping:
  0-20:  Green  (Normal)              - Risk Budget: 100%
  21-40: Yellow (Early Warning)       - Risk Budget: 80-90%
  41-60: Orange (Elevated Risk)       - Risk Budget: 60-75%
  61-80: Red    (High Probability Top)- Risk Budget: 40-55%
  81-100:Critical(Top Formation)      - Risk Budget: 20-35%
"""

from typing import Optional

COMPONENT_WEIGHTS = {
    "distribution_days": 0.25,
    "leading_stocks": 0.20,
    "defensive_rotation": 0.15,
    "breadth_divergence": 0.15,
    "index_technical": 0.15,
    "sentiment": 0.10,
}

COMPONENT_LABELS = {
    "distribution_days": "Distribution Day Count",
    "leading_stocks": "Leading Stock Health",
    "defensive_rotation": "Defensive Sector Rotation",
    "breadth_divergence": "Market Breadth Divergence",
    "index_technical": "Index Technical Condition",
    "sentiment": "Sentiment & Speculation",
}

# Correlated component pairs: when both are extreme, discount the lower-weight one
CORRELATION_PAIRS = [("distribution_days", "defensive_rotation")]
CORRELATION_THRESHOLD = 80
CORRELATION_DISCOUNT = 0.8


def _apply_correlation_adjustment(component_scores: dict[str, float]) -> dict:
    """
    Discount correlated components when both are extreme.

    When both components in a CORRELATION_PAIR are >= CORRELATION_THRESHOLD,
    the lower-weight component gets multiplied by CORRELATION_DISCOUNT.

    Returns:
        Dict with 'adjusted_scores' and 'adjustments' details.
    """
    adjusted = dict(component_scores)
    adjustments = []

    for comp_a, comp_b in CORRELATION_PAIRS:
        score_a = component_scores.get(comp_a, 0)
        score_b = component_scores.get(comp_b, 0)
        if score_a >= CORRELATION_THRESHOLD and score_b >= CORRELATION_THRESHOLD:
            # Discount the lower-weight component
            weight_a = COMPONENT_WEIGHTS.get(comp_a, 0)
            weight_b = COMPONENT_WEIGHTS.get(comp_b, 0)
            if weight_a >= weight_b:
                discounted = comp_b
                original = score_b
            else:
                discounted = comp_a
                original = score_a
            adjusted[discounted] = original * CORRELATION_DISCOUNT
            adjustments.append(
                {
                    "pair": [comp_a, comp_b],
                    "discounted_component": discounted,
                    "original_score": original,
                    "adjusted_score": adjusted[discounted],
                    "discount_factor": CORRELATION_DISCOUNT,
                }
            )

    return {"adjusted_scores": adjusted, "adjustments": adjustments}


def calculate_composite_score(
    component_scores: dict[str, float], data_availability: Optional[dict[str, bool]] = None
) -> dict:
    """
    Calculate weighted composite market top probability score.

    Args:
        component_scores: Dict with keys matching COMPONENT_WEIGHTS,
                         each value 0-100
        data_availability: Optional dict mapping component key -> bool indicating
                          if data was actually available (vs neutral default)

    Returns:
        Dict with composite_score, zone, risk_budget, guidance,
        weakest/strongest components, component breakdown, and data_quality
    """
    if data_availability is None:
        data_availability = {}

    # Apply correlation adjustment
    corr_result = _apply_correlation_adjustment(component_scores)
    adjusted_scores = corr_result["adjusted_scores"]
    correlation_adjustment = corr_result["adjustments"]

    # Build effective weights once: redistribute from unavailable to available
    available_weight = 0.0
    for key, weight in COMPONENT_WEIGHTS.items():
        if data_availability.get(key, True):
            available_weight += weight

    effective_weights = {}
    for key, weight in COMPONENT_WEIGHTS.items():
        if data_availability.get(key, True):
            effective_weights[key] = weight / available_weight if available_weight > 0 else weight

    # Calculate weighted composite using adjusted scores and effective weights
    composite = 0.0
    for key in effective_weights:
        score = adjusted_scores.get(key, 0)
        composite += score * effective_weights[key]

    composite = round(composite, 1)

    # Identify strongest and weakest from available components only
    available_scores = {k: v for k, v in component_scores.items() if k in effective_weights}

    if available_scores:
        strongest_warning = max(available_scores, key=available_scores.get)
        weakest_warning = min(available_scores, key=available_scores.get)
    else:
        strongest_warning = None
        weakest_warning = None

    # Get zone interpretation
    zone_info = _interpret_zone(composite)

    # Calculate data quality
    available_count = sum(
        1
        for k in COMPONENT_WEIGHTS
        if data_availability.get(k, True)  # Default True for backward compat
    )
    total_components = len(COMPONENT_WEIGHTS)
    missing_components = [
        COMPONENT_LABELS[k] for k in COMPONENT_WEIGHTS if not data_availability.get(k, True)
    ]

    if available_count == total_components:
        quality_label = f"Complete ({available_count}/{total_components} components)"
    elif available_count >= total_components - 2:
        quality_label = (
            f"Partial ({available_count}/{total_components} components) - interpret with caution"
        )
    else:
        quality_label = (
            f"Limited ({available_count}/{total_components} components) - low confidence"
        )

    data_quality = {
        "available_count": available_count,
        "total_components": total_components,
        "label": quality_label,
        "missing_components": missing_components,
    }

    # Build strongest/weakest dicts (handle None when no available components)
    if strongest_warning is not None:
        strongest_dict = {
            "component": strongest_warning,
            "label": COMPONENT_LABELS.get(strongest_warning, strongest_warning),
            "score": available_scores.get(strongest_warning, 0),
        }
    else:
        strongest_dict = {"component": None, "label": "N/A", "score": 0}

    if weakest_warning is not None:
        weakest_dict = {
            "component": weakest_warning,
            "label": COMPONENT_LABELS.get(weakest_warning, weakest_warning),
            "score": available_scores.get(weakest_warning, 0),
        }
    else:
        weakest_dict = {"component": None, "label": "N/A", "score": 0}

    return {
        "composite_score": composite,
        "zone": zone_info["zone"],
        "zone_color": zone_info["color"],
        "risk_budget": zone_info["risk_budget"],
        "guidance": zone_info["guidance"],
        "actions": zone_info["actions"],
        "strongest_warning": strongest_dict,
        "weakest_warning": weakest_dict,
        "data_quality": data_quality,
        "correlation_adjustment": correlation_adjustment,
        "component_scores": {
            k: {
                "score": component_scores.get(k, 0),
                "adjusted_score": adjusted_scores.get(k, component_scores.get(k, 0)),
                "weight": w,
                "weighted_contribution": round(adjusted_scores.get(k, 0) * effective_weights[k], 1)
                if k in effective_weights
                else 0.0,
                "label": COMPONENT_LABELS[k],
            }
            for k, w in COMPONENT_WEIGHTS.items()
        },
    }


def _interpret_zone(composite: float) -> dict:
    """Map composite score to risk zone"""
    if composite <= 20:
        return {
            "zone": "Green (Normal)",
            "color": "green",
            "risk_budget": "100%",
            "guidance": "Normal market conditions. Maintain standard position management.",
            "actions": [
                "Normal position sizing",
                "Standard stop-loss levels",
                "New position entries allowed",
            ],
        }
    elif composite <= 40:
        return {
            "zone": "Yellow (Early Warning)",
            "color": "yellow",
            "risk_budget": "80-90%",
            "guidance": "Early warning signs detected. Tighten stops and reduce new entries.",
            "actions": [
                "Tighten stop-losses by 10-20%",
                "Reduce new position sizes by 25-50%",
                "Review weakest positions for exits",
                "Monitor distribution days closely",
            ],
        }
    elif composite <= 60:
        return {
            "zone": "Orange (Elevated Risk)",
            "color": "orange",
            "risk_budget": "60-75%",
            "guidance": "Elevated risk of correction. Begin profit-taking on weaker positions.",
            "actions": [
                "Take profits on weakest 25-30% of positions",
                "No new momentum entries",
                "Only quality stocks near support",
                "Raise cash allocation",
                "Watch for Follow-Through Day if market pulls back",
            ],
        }
    elif composite <= 80:
        return {
            "zone": "Red (High Probability Top)",
            "color": "red",
            "risk_budget": "40-55%",
            "guidance": "High probability of market top. Aggressive profit-taking recommended.",
            "actions": [
                "Aggressive profit-taking (sell 40-50% of positions)",
                "Maximum cash allocation",
                "Only hold strongest leaders",
                "Consider hedges (put options, inverse ETFs)",
                "Prepare short watchlist",
            ],
        }
    else:
        return {
            "zone": "Critical (Top Formation)",
            "color": "critical",
            "risk_budget": "20-35%",
            "guidance": "Top formation in progress. Maximum defensive posture.",
            "actions": [
                "Sell most positions (keep only 20-35% invested)",
                "Full hedge implementation",
                "Short positions on weakest leaders",
                "Preserve capital as primary objective",
                "Watch for capitulation/Follow-Through Day for re-entry",
            ],
        }


def detect_follow_through_day(index_history: list[dict], composite_score: float) -> dict:
    """
    Detect Follow-Through Day (FTD) signal for bottom confirmation.
    Only relevant when composite > 40 (Orange zone or worse).

    O'Neil's Strict FTD Rules:
    1. Identify swing low: significant decline (3+ down days, -3%+ from recent high)
    2. Rally Day 1: first up day (close > previous close) after swing low
    3. FTD: Day 4-7 of rally, gain >= 1.5% on volume higher than previous day
    4. Rally resets if price closes below swing low

    Args:
        index_history: Daily OHLCV (most recent first)
        composite_score: Current composite score

    Returns:
        Dict with ftd_detected, rally_day_count, details
    """
    if composite_score < 40:
        return {
            "ftd_detected": False,
            "applicable": False,
            "reason": "Composite < 40 (Green/Yellow zone) - FTD monitoring not needed",
        }

    if not index_history or len(index_history) < 10:
        return {
            "ftd_detected": False,
            "applicable": True,
            "reason": "Insufficient data for FTD analysis",
        }

    # Work in chronological order (oldest first)
    history = list(reversed(index_history))
    n = len(history)

    # Only look at the most recent 40 trading days
    lookback = min(40, n)
    history = history[n - lookback :]
    n = len(history)

    # Step 1: Find swing low within the lookback window
    # Swing low = lowest close after a decline of 3%+ from a recent high
    swing_low_idx = None
    swing_low_price = None

    # Scan for the most recent swing low
    for i in range(n - 1, 2, -1):  # from recent to old
        low_close = history[i].get("close", 0)
        if low_close <= 0:
            continue

        # Look back from this point for a recent high (within 20 days)
        search_start = max(0, i - 20)
        recent_high = 0
        for j in range(search_start, i):
            c = history[j].get("close", 0)
            if c > recent_high:
                recent_high = c

        if recent_high <= 0:
            continue

        decline_pct = (low_close - recent_high) / recent_high * 100

        # Check for 3%+ decline from recent high
        if decline_pct <= -3.0:
            # Verify at least 3 down days in the decline
            down_days = 0
            for j in range(search_start + 1, i + 1):
                prev_c = history[j - 1].get("close", 0)
                curr_c = history[j].get("close", 0)
                if prev_c > 0 and curr_c < prev_c:
                    down_days += 1

            if down_days >= 3:
                # Check this is actually a local low
                is_local_low = True
                if i > 0 and history[i - 1].get("close", 0) < low_close:
                    is_local_low = False
                if i + 1 < n and history[i + 1].get("close", 0) < low_close:
                    is_local_low = False

                if is_local_low:
                    swing_low_idx = i
                    swing_low_price = low_close
                    break

    if swing_low_idx is None:
        return {
            "ftd_detected": False,
            "applicable": True,
            "reason": "No qualifying swing low found (need 3%+ decline with 3+ down days)",
            "rally_day_count": 0,
        }

    # Step 2 & 3: Find Rally Day 1 and count rally days with reset handling
    # Uses seeking_rally_day_1 flag to properly re-seek Day 1 after resets.
    # TODO: FTD logic here mirrors ftd-detector skill's state machine.
    #       Consider extracting shared FTD core if both need changes.
    rally_day_1_idx = None
    rally_day_count = 0
    ftd_detected = False
    ftd_day = None
    seeking_rally_day_1 = True
    reset_count = 0

    for i in range(swing_low_idx + 1, n):
        curr_close = history[i].get("close", 0)
        prev_close = history[i - 1].get("close", 0) if i > 0 else 0

        # Check for rally reset: price closes below swing low
        if curr_close < swing_low_price:
            swing_low_idx = i
            swing_low_price = curr_close
            rally_day_count = 0
            ftd_detected = False
            seeking_rally_day_1 = True
            reset_count += 1
            rally_day_1_idx = None
            continue

        # Seek Rally Day 1: first up close (or range top 50%) after swing low
        if seeking_rally_day_1:
            if prev_close <= 0:
                continue
            high = history[i].get("high", curr_close)
            low = history[i].get("low", curr_close)
            bar_range = high - low
            range_position = (curr_close - low) / bar_range if bar_range > 0 else 0
            if curr_close > prev_close or range_position >= 0.5:
                rally_day_1_idx = i
                rally_day_count = 1
                seeking_rally_day_1 = False
            continue

        # Normal rally day counting (all days after Day 1 count)
        rally_day_count += 1

        # Check FTD on days 4-7
        if 4 <= rally_day_count <= 7 and prev_close > 0:
            gain_pct = (curr_close - prev_close) / prev_close * 100
            curr_volume = history[i].get("volume", 0)
            prev_volume = history[i - 1].get("volume", 0)

            if gain_pct >= 1.5 and prev_volume > 0 and curr_volume > prev_volume:
                ftd_detected = True
                ftd_day = history[i].get("date", f"day-{i}")
                break

    if rally_day_1_idx is None:
        return {
            "ftd_detected": False,
            "applicable": True,
            "reason": "No rally attempt started after swing low",
            "rally_day_count": 0,
            "swing_low_date": history[swing_low_idx].get("date", "N/A"),
            "swing_low_price": swing_low_price,
            "reset_count": reset_count,
        }

    # Cap rally_day_count for reporting
    days_since_rally_start = n - rally_day_1_idx
    rally_day_count = min(rally_day_count, days_since_rally_start)

    swing_low_date = history[swing_low_idx].get("date", "N/A")

    if ftd_detected:
        reason = f"Follow-Through Day detected on {ftd_day} (Day {rally_day_count} of rally from {swing_low_date} low)"
    elif rally_day_count >= 7:
        reason = (
            f"Rally attempt: Day {rally_day_count} from {swing_low_date} low - "
            "FTD window (Day 4-7) passed without qualifying day"
        )
    else:
        reason = (
            f"Rally attempt: Day {rally_day_count} from {swing_low_date} low "
            f"(FTD requires Day 4-7 with >= 1.5% gain on higher volume)"
        )

    return {
        "ftd_detected": ftd_detected,
        "applicable": True,
        "rally_day_count": rally_day_count,
        "ftd_day": ftd_day,
        "swing_low_date": swing_low_date,
        "swing_low_price": swing_low_price,
        "reset_count": reset_count,
        "reason": reason,
    }


# Testing
if __name__ == "__main__":
    print("Testing Market Top Scorer...\n")

    # Test 1: Moderate risk scenario (calibration target: ~50)
    test_scores = {
        "distribution_days": 45,
        "leading_stocks": 52,
        "defensive_rotation": 82,
        "breadth_divergence": 20,
        "index_technical": 42,
        "sentiment": 62,
    }

    result = calculate_composite_score(test_scores)
    print("Test 1 - Moderate Risk:")
    print(f"  Composite: {result['composite_score']}/100")
    print(f"  Zone: {result['zone']}")
    print(f"  Risk Budget: {result['risk_budget']}")
    print(
        f"  Strongest Warning: {result['strongest_warning']['label']} "
        f"({result['strongest_warning']['score']})"
    )
    print()

    # Test 2: Healthy market
    healthy = {
        "distribution_days": 0,
        "leading_stocks": 10,
        "defensive_rotation": 0,
        "breadth_divergence": 10,
        "index_technical": 5,
        "sentiment": 15,
    }
    result2 = calculate_composite_score(healthy)
    print("Test 2 - Healthy Market:")
    print(f"  Composite: {result2['composite_score']}/100")
    print(f"  Zone: {result2['zone']}")
    print()

    # Test 3: Crisis
    crisis = {
        "distribution_days": 100,
        "leading_stocks": 90,
        "defensive_rotation": 85,
        "breadth_divergence": 80,
        "index_technical": 75,
        "sentiment": 70,
    }
    result3 = calculate_composite_score(crisis)
    print("Test 3 - Crisis:")
    print(f"  Composite: {result3['composite_score']}/100")
    print(f"  Zone: {result3['zone']}")
    print()

    # Test 4: Data quality tracking
    partial_scores = {
        "distribution_days": 45,
        "leading_stocks": 52,
        "defensive_rotation": 50,
        "breadth_divergence": 50,
        "index_technical": 42,
        "sentiment": 50,
    }
    partial_availability = {
        "distribution_days": True,
        "leading_stocks": True,
        "defensive_rotation": False,
        "breadth_divergence": False,
        "index_technical": True,
        "sentiment": False,
    }
    result4 = calculate_composite_score(partial_scores, partial_availability)
    print("Test 4 - Partial Data:")
    print(f"  Composite: {result4['composite_score']}/100")
    print(f"  Data Quality: {result4['data_quality']['label']}")
    print(f"  Missing: {result4['data_quality']['missing_components']}")
    print()

    print("All tests completed.")
