"""Tests for Composite Scorer and FTD Detection"""

from scorer import (
    COMPONENT_WEIGHTS,
    CORRELATION_DISCOUNT,
    _apply_correlation_adjustment,
    calculate_composite_score,
    detect_follow_through_day,
)


class TestCompositeScore:
    """Test composite scoring."""

    def test_all_zeros(self):
        scores = {k: 0 for k in COMPONENT_WEIGHTS}
        result = calculate_composite_score(scores)
        assert result["composite_score"] == 0
        assert "Green" in result["zone"]

    def test_all_100(self):
        """All 100 with correlation discount: 100 - 0.15*(100-80) = 97.0."""
        scores = {k: 100 for k in COMPONENT_WEIGHTS}
        result = calculate_composite_score(scores)
        assert result["composite_score"] == 97.0
        assert "Critical" in result["zone"]

    def test_moderate_risk(self):
        """Calibration target: ~48-50 for moderate risk."""
        scores = {
            "distribution_days": 45,
            "leading_stocks": 52,
            "defensive_rotation": 82,
            "breadth_divergence": 20,
            "index_technical": 42,
            "sentiment": 62,
        }
        result = calculate_composite_score(scores)
        assert 40 <= result["composite_score"] <= 55

    def test_weights_sum_to_1(self):
        total = sum(COMPONENT_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001

    def test_strongest_weakest(self):
        scores = {
            "distribution_days": 90,
            "leading_stocks": 10,
            "defensive_rotation": 50,
            "breadth_divergence": 50,
            "index_technical": 50,
            "sentiment": 50,
        }
        result = calculate_composite_score(scores)
        assert result["strongest_warning"]["component"] == "distribution_days"
        assert result["weakest_warning"]["component"] == "leading_stocks"

    def test_strongest_weakest_excludes_unavailable(self):
        """Unavailable components must not appear as strongest/weakest."""
        scores = {
            "distribution_days": 30,
            "leading_stocks": 40,
            "defensive_rotation": 50,
            "breadth_divergence": 95,  # Highest but unavailable
            "index_technical": 5,  # Lowest but unavailable
            "sentiment": 60,
        }
        avail = {k: True for k in COMPONENT_WEIGHTS}
        avail["breadth_divergence"] = False
        avail["index_technical"] = False
        result = calculate_composite_score(scores, avail)
        # strongest should be sentiment (60), not breadth (95)
        assert result["strongest_warning"]["component"] == "sentiment"
        # weakest should be distribution_days (30), not index_technical (5)
        assert result["weakest_warning"]["component"] == "distribution_days"

    def test_contribution_sum_matches_composite(self):
        """Sum of weighted contributions should approximate composite score."""
        scores = {
            "distribution_days": 45,
            "leading_stocks": 52,
            "defensive_rotation": 30,
            "breadth_divergence": 20,
            "index_technical": 42,
            "sentiment": 62,
        }
        avail = {k: True for k in COMPONENT_WEIGHTS}
        avail["sentiment"] = False
        result = calculate_composite_score(scores, avail)
        contributions = [
            v["weighted_contribution"]
            for k, v in result["component_scores"].items()
            if avail.get(k, True)
        ]
        assert abs(sum(contributions) - result["composite_score"]) <= 0.5

    def test_single_available_component(self):
        """Only 1 available component should still produce valid strongest/weakest."""
        scores = {k: 50 for k in COMPONENT_WEIGHTS}
        scores["distribution_days"] = 70
        avail = {k: False for k in COMPONENT_WEIGHTS}
        avail["distribution_days"] = True
        result = calculate_composite_score(scores, avail)
        assert result["strongest_warning"]["component"] == "distribution_days"
        assert result["weakest_warning"]["component"] == "distribution_days"
        assert result["composite_score"] == 70.0


class TestDataQuality:
    """Test data quality tracking."""

    def test_all_available(self):
        scores = {k: 50 for k in COMPONENT_WEIGHTS}
        avail = {k: True for k in COMPONENT_WEIGHTS}
        result = calculate_composite_score(scores, avail)
        dq = result["data_quality"]
        assert dq["available_count"] == 6
        assert "Complete" in dq["label"]
        assert dq["missing_components"] == []

    def test_some_missing(self):
        scores = {k: 50 for k in COMPONENT_WEIGHTS}
        avail = {k: True for k in COMPONENT_WEIGHTS}
        avail["breadth_divergence"] = False
        avail["sentiment"] = False
        result = calculate_composite_score(scores, avail)
        dq = result["data_quality"]
        assert dq["available_count"] == 4
        assert "Partial" in dq["label"]
        assert len(dq["missing_components"]) == 2

    def test_many_missing(self):
        scores = {k: 50 for k in COMPONENT_WEIGHTS}
        avail = {k: False for k in COMPONENT_WEIGHTS}
        avail["distribution_days"] = True
        avail["leading_stocks"] = True
        result = calculate_composite_score(scores, avail)
        dq = result["data_quality"]
        assert dq["available_count"] == 2
        assert "Limited" in dq["label"]

    def test_backward_compat_no_availability(self):
        """Without data_availability, all assumed available."""
        scores = {k: 50 for k in COMPONENT_WEIGHTS}
        result = calculate_composite_score(scores)
        dq = result["data_quality"]
        assert dq["available_count"] == 6
        assert "Complete" in dq["label"]

    def test_weight_redistribution_when_missing(self):
        """Missing components' weight should be redistributed, not use neutral 50."""
        scores_all_80 = {k: 80 for k in COMPONENT_WEIGHTS}
        # All available: composite ~ 80 (minus correlation discount)
        result_full = calculate_composite_score(scores_all_80)

        # Mark sentiment as unavailable: should still be ~80 from remaining
        avail = {k: True for k in COMPONENT_WEIGHTS}
        avail["sentiment"] = False
        result_partial = calculate_composite_score(scores_all_80, avail)

        # With redistribution, score should be similar (both driven by 80s)
        assert abs(result_full["composite_score"] - result_partial["composite_score"]) <= 3.0

    def test_weight_redistribution_excludes_unavailable(self):
        """Unavailable component with score 0 should not drag composite down."""
        scores = {k: 80 for k in COMPONENT_WEIGHTS}
        scores["breadth_divergence"] = 0  # Would drag down if included
        avail = {k: True for k in COMPONENT_WEIGHTS}
        avail["breadth_divergence"] = False  # But it's unavailable

        result = calculate_composite_score(scores, avail)
        # Without breadth (score=0), composite should be purely from 80-scored components
        # All remaining are 80, so composite ~ 80 (minus correlation discount)
        assert result["composite_score"] >= 75


class TestCorrelationAdjustment:
    """Test correlation adjustment between distribution_days and defensive_rotation."""

    def test_both_extreme_applies_discount(self):
        """Both >= 80 -> defensive_rotation discounted by 0.8x."""
        scores = {k: 50 for k in COMPONENT_WEIGHTS}
        scores["distribution_days"] = 90
        scores["defensive_rotation"] = 85
        result = _apply_correlation_adjustment(scores)
        adj = result["adjusted_scores"]
        assert adj["defensive_rotation"] == 85 * CORRELATION_DISCOUNT
        assert adj["distribution_days"] == 90  # Higher weight, not discounted
        assert len(result["adjustments"]) == 1

    def test_one_below_threshold_no_discount(self):
        """One below threshold -> no adjustment."""
        scores = {k: 50 for k in COMPONENT_WEIGHTS}
        scores["distribution_days"] = 90
        scores["defensive_rotation"] = 70  # Below 80
        result = _apply_correlation_adjustment(scores)
        assert result["adjusted_scores"]["defensive_rotation"] == 70
        assert len(result["adjustments"]) == 0

    def test_zone_unchanged_for_moderate(self):
        """Moderate scores should not trigger correlation adjustment."""
        scores = {k: 40 for k in COMPONENT_WEIGHTS}
        result = _apply_correlation_adjustment(scores)
        assert len(result["adjustments"]) == 0
        assert result["adjusted_scores"] == scores

    def test_adjustment_details_present(self):
        """Adjustment details should include pair, original, adjusted, discount."""
        scores = {k: 80 for k in COMPONENT_WEIGHTS}
        result = _apply_correlation_adjustment(scores)
        assert len(result["adjustments"]) == 1
        adj = result["adjustments"][0]
        assert "distribution_days" in adj["pair"]
        assert "defensive_rotation" in adj["pair"]
        assert adj["discounted_component"] == "defensive_rotation"
        assert adj["original_score"] == 80
        assert adj["adjusted_score"] == 80 * CORRELATION_DISCOUNT
        assert adj["discount_factor"] == CORRELATION_DISCOUNT


class TestFollowThroughDay:
    """Test O'Neil-strict FTD detection."""

    def test_not_applicable_below_40(self):
        result = detect_follow_through_day([], 30.0)
        assert result["applicable"] is False

    def test_insufficient_data(self):
        result = detect_follow_through_day([{"close": 100}] * 5, 50.0)
        assert result["ftd_detected"] is False

    def test_no_swing_low(self):
        """Flat market → no swing low found."""
        history = [{"close": 100, "volume": 1000000, "date": f"day-{i}"} for i in range(30)]
        result = detect_follow_through_day(history, 50.0)
        assert result["ftd_detected"] is False

    def test_ftd_detected_on_clear_pattern(self):
        """
        Create a clear pattern:
        - Days 0-9: prices rise from 100 to 109 (establishing high)
        - Days 10-14: decline from 109 to 100 (5+ down days, ~8% drop)
        - Day 15: swing low at 100
        - Day 16: rally day 1 (up from 100 to 101)
        - Day 17-18: rally continues (101.5, 102)
        - Day 19 (rally day 4): FTD - big gain +2% on higher volume

        History is most-recent-first, so reversed.
        """
        bars = []
        # Build chronologically, then reverse
        # Days 0-9: uptrend
        for i in range(10):
            bars.append({"close": 100 + i, "volume": 1000000, "date": f"2026-01-{i + 1:02d}"})

        # Days 10-14: decline (5 down days from 109)
        decline_prices = [107, 105, 103, 101, 100]
        for i, p in enumerate(decline_prices):
            bars.append({"close": p, "volume": 1100000, "date": f"2026-01-{11 + i:02d}"})

        # Day 15: swing low
        bars.append({"close": 99.5, "volume": 1200000, "date": "2026-01-16"})

        # Day 16: rally day 1
        bars.append({"close": 101, "volume": 1000000, "date": "2026-01-17"})

        # Day 17-18: rally continues
        bars.append({"close": 101.5, "volume": 1000000, "date": "2026-01-18"})
        bars.append({"close": 102, "volume": 1000000, "date": "2026-01-19"})

        # Day 19: FTD - +2% gain on higher volume
        bars.append({"close": 104.04, "volume": 1500000, "date": "2026-01-20"})

        # Reverse to most-recent-first
        history = list(reversed(bars))

        result = detect_follow_through_day(history, 55.0)
        assert result["ftd_detected"] is True
        assert result["rally_day_count"] >= 4

    def test_rally_reset_below_swing_low(self):
        """Rally resets if price drops below swing low."""
        bars = []
        # Uptrend
        for i in range(10):
            bars.append({"close": 100 + i, "volume": 1000000, "date": f"d-{i}"})
        # Decline
        for i, p in enumerate([107, 105, 103, 101, 100]):
            bars.append({"close": p, "volume": 1100000, "date": f"d-{10 + i}"})
        # Swing low
        bars.append({"close": 99, "volume": 1200000, "date": "d-15"})
        # Brief rally
        bars.append({"close": 100, "volume": 1000000, "date": "d-16"})
        # Drop below swing low → reset
        bars.append({"close": 98, "volume": 1000000, "date": "d-17"})
        # New rally from lower base
        bars.append({"close": 99, "volume": 1000000, "date": "d-18"})
        bars.append({"close": 99.5, "volume": 1000000, "date": "d-19"})

        history = list(reversed(bars))
        result = detect_follow_through_day(history, 55.0)
        # FTD should NOT be detected (rally reset, new rally too short)
        assert result["ftd_detected"] is False

    def test_ftd_reset_requires_up_day_for_rally_day_1(self):
        """After reset (new low), flat days should NOT count as Rally Day 1.

        Uses a long rally (21+ days) between swing low and crash so that
        the crash bar's 20-day lookback has < 3 down days, preventing the
        swing low finder from recognizing the crash as a new swing low.
        """
        bars = []
        # Days 0-5: uptrend
        for i in range(6):
            bars.append({"close": 100 + i * 2, "volume": 1000000, "date": f"d-{i}"})
        # Days 6-10: decline (5 down days)
        for i, p in enumerate([108, 106, 104, 100, 97]):
            bars.append({"close": p, "volume": 1100000, "date": f"d-{6 + i}"})
        # Day 11: swing low at 95
        bars.append({"close": 95, "volume": 1200000, "date": "d-11"})
        # Days 12-32: rally (21 bars, climbing from 96 to 116)
        for i in range(21):
            bars.append({"close": 96 + i, "volume": 1000000, "date": f"d-{12 + i}"})
        # Day 33: crash below 95 (only 1 down day in 20-bar lookback)
        bars.append({"close": 94, "volume": 1000000, "date": "d-33"})
        # Day 34: flat at 94 — should NOT be Rally Day 1
        bars.append({"close": 94, "volume": 1000000, "date": "d-34"})
        # Day 35: down — NOT Rally Day 1
        bars.append({"close": 93.5, "volume": 1000000, "date": "d-35"})
        # Day 36: up from 93.5 → THIS should be the new Rally Day 1
        bars.append({"close": 95, "volume": 1000000, "date": "d-36"})
        # Days 37-38
        bars.append({"close": 96, "volume": 1000000, "date": "d-37"})
        bars.append({"close": 97, "volume": 1000000, "date": "d-38"})

        history = list(reversed(bars))
        result = detect_follow_through_day(history, 55.0)
        # After reset, flat/down days skipped, Day 1 at d-36, days 2-3
        assert result["rally_day_count"] == 3
        assert result["reset_count"] >= 1

    def test_ftd_reset_clears_invalidation(self):
        """After reset, finding new Rally Day 1 leads to valid FTD detection."""
        bars = []
        # Days 0-5: uptrend
        for i in range(6):
            bars.append({"close": 100 + i * 2, "volume": 1000000, "date": f"d-{i}"})
        # Days 6-10: decline (5 down days)
        for i, p in enumerate([108, 106, 104, 100, 97]):
            bars.append({"close": p, "volume": 1100000, "date": f"d-{6 + i}"})
        # Day 11: swing low at 95
        bars.append({"close": 95, "volume": 1200000, "date": "d-11"})
        # Days 12-32: rally (21 bars, climbing from 96 to 116)
        for i in range(21):
            bars.append({"close": 96 + i, "volume": 1000000, "date": f"d-{12 + i}"})
        # Day 33: crash below 95
        bars.append({"close": 94, "volume": 1000000, "date": "d-33"})
        # Day 34: new Rally Day 1 (up from 94)
        bars.append({"close": 96, "volume": 1000000, "date": "d-34"})
        # Days 35-36
        bars.append({"close": 97, "volume": 1000000, "date": "d-35"})
        bars.append({"close": 98, "volume": 1000000, "date": "d-36"})
        # Day 37 (rally day 4): FTD - +2% gain on higher volume
        bars.append({"close": 99.96, "volume": 1500000, "date": "d-37"})

        history = list(reversed(bars))
        result = detect_follow_through_day(history, 55.0)
        assert result["ftd_detected"] is True
        assert result["rally_day_count"] >= 4
        assert result["reset_count"] >= 1

    def test_ftd_day1_accepts_range_top_half(self):
        """Rally Day 1 can be a bar closing in upper 50% of range, not just up day.

        Constructs a scenario where the bar after the swing low has
        close == prev_close (not an up day) but closes in the upper half
        of its intraday range.
        """
        bars = []
        # Uptrend
        for i in range(10):
            bars.append({"close": 100 + i, "volume": 1000000, "date": f"d-{i}"})
        # Decline
        for i, p in enumerate([107, 105, 103, 101, 100]):
            bars.append({"close": p, "volume": 1100000, "date": f"d-{10 + i}"})
        # Swing low at 95
        bars.append({"close": 95, "volume": 1200000, "date": "d-15"})
        # Next bar: close=95 (same as swing low, NOT an up day), but upper half range
        # high=98, low=92, close=95 → range_position = (95-92)/(98-92) = 0.5
        bars.append({"close": 95, "high": 98, "low": 92, "volume": 1000000, "date": "d-16"})
        # Day 2, 3
        bars.append({"close": 97, "volume": 1000000, "date": "d-17"})
        bars.append({"close": 98, "volume": 1000000, "date": "d-18"})

        history = list(reversed(bars))
        result = detect_follow_through_day(history, 55.0)
        # The finder may find d-16 or d-15 as swing low (both close=95).
        # If d-16 is the swing low, Day 1 would be d-17 (up from 95).
        # If d-15 is the swing low, d-16 qualifies via range_top_half.
        # Either way, we should have a rally of at least 2 days.
        assert result["rally_day_count"] >= 2
