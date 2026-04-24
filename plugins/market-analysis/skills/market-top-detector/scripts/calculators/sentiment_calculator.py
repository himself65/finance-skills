#!/usr/bin/env python3
"""
Component 6: Sentiment & Speculation (Weight: 10%)

Data sources:
- VIX: FMP API quote
- Put/Call ratio: CLI argument (from WebSearch)
- VIX term structure: CLI argument (from WebSearch) or auto-detected
- Margin Debt YoY: CLI argument (from WebSearch)

Scoring (additive, max 100):
  Put/Call < 0.60 -> +35pt (extreme call buying = complacency)
  Put/Call < 0.70 -> +25pt
  Put/Call < 0.80 -> +12pt
  Put/Call >= 0.80 -> +0pt (healthy caution)

  VIX < 12       -> +25pt (extreme low fear)
  VIX < 14       -> +17pt
  VIX < 16       -> +8pt
  VIX 16-20      -> +0pt (normal)
  VIX > 25       -> -8pt (fear already present, top less likely)

  VIX term structure:
    Steep contango (normal) -> +25pt (complacency)
    Normal contango        -> +12pt
    Flat                   -> +0pt
    Backwardation          -> -8pt (hedging demand = fear)

  Margin Debt YoY:
    > 30%  -> +15pt (extreme leverage)
    > 20%  -> +10pt
    > 10%  -> +5pt
    <= 10% -> +0pt
"""

from typing import Optional

# VIX term structure states
STEEP_CONTANGO = "steep_contango"
NORMAL_CONTANGO = "contango"
FLAT = "flat"
BACKWARDATION = "backwardation"


def calculate_sentiment(
    vix_level: Optional[float] = None,
    put_call_ratio: Optional[float] = None,
    vix_term_structure: Optional[str] = None,
    margin_debt_yoy_pct: Optional[float] = None,
) -> dict:
    """
    Calculate sentiment and speculation score.

    Args:
        vix_level: Current VIX value (from FMP API)
        put_call_ratio: CBOE equity put/call ratio (from WebSearch/CLI)
        vix_term_structure: One of 'steep_contango', 'contango', 'flat', 'backwardation'
        margin_debt_yoy_pct: Year-over-year margin debt change % (optional extra context)

    Returns:
        Dict with score (0-100), signal, component details
    """
    # All inputs missing -> neutral default
    if vix_level is None and put_call_ratio is None and vix_term_structure is None:
        return {
            "score": 50,
            "signal": "NO DATA: All sentiment inputs missing (neutral default)",
            "data_available": False,
            "total_points": 0,
            "details": {},
        }

    total_points = 0
    details = {}

    # 1. Put/Call Ratio scoring (max 35pt)
    pc_points = 0
    if put_call_ratio is not None:
        if put_call_ratio < 0.60:
            pc_points = 35
        elif put_call_ratio < 0.70:
            pc_points = 25
        elif put_call_ratio < 0.80:
            pc_points = 12
        else:
            pc_points = 0
        details["put_call_ratio"] = {
            "value": put_call_ratio,
            "points": pc_points,
            "interpretation": _interpret_put_call(put_call_ratio),
        }
    else:
        details["put_call_ratio"] = {"value": None, "points": 0, "interpretation": "No data"}

    total_points += pc_points

    # 2. VIX Level scoring (max 25pt)
    vix_points = 0
    if vix_level is not None:
        if vix_level < 12:
            vix_points = 25
        elif vix_level < 14:
            vix_points = 17
        elif vix_level < 16:
            vix_points = 8
        elif vix_level <= 25:
            vix_points = 0
        else:
            vix_points = -8  # High fear = top less likely
        details["vix_level"] = {
            "value": round(vix_level, 2),
            "points": vix_points,
            "interpretation": _interpret_vix(vix_level),
        }
    else:
        details["vix_level"] = {"value": None, "points": 0, "interpretation": "No data"}

    total_points += vix_points

    # 3. VIX Term Structure scoring (max 25pt)
    vts_points = 0
    if vix_term_structure:
        if vix_term_structure == STEEP_CONTANGO:
            vts_points = 25
        elif vix_term_structure == NORMAL_CONTANGO:
            vts_points = 12
        elif vix_term_structure == FLAT:
            vts_points = 0
        elif vix_term_structure == BACKWARDATION:
            vts_points = -8
        details["vix_term_structure"] = {
            "value": vix_term_structure,
            "points": vts_points,
            "interpretation": _interpret_vix_term(vix_term_structure),
        }
    else:
        details["vix_term_structure"] = {"value": None, "points": 0, "interpretation": "No data"}

    total_points += vts_points

    # 4. Margin Debt YoY scoring (max 15pt)
    md_points = 0
    if margin_debt_yoy_pct is not None:
        if margin_debt_yoy_pct > 30:
            md_points = 15
        elif margin_debt_yoy_pct > 20:
            md_points = 10
        elif margin_debt_yoy_pct > 10:
            md_points = 5
        else:
            md_points = 0
        details["margin_debt"] = {
            "yoy_pct": margin_debt_yoy_pct,
            "points": md_points,
            "interpretation": _interpret_margin_debt(margin_debt_yoy_pct),
        }

    total_points += md_points

    # Clamp to 0-100
    score = max(0, min(100, total_points))

    # Signal
    if score >= 70:
        signal = "CRITICAL: Extreme complacency / speculation"
    elif score >= 50:
        signal = "WARNING: Elevated complacency"
    elif score >= 30:
        signal = "CAUTION: Some speculative excess"
    elif score >= 10:
        signal = "MIXED: Moderate sentiment"
    else:
        signal = "HEALTHY: No excessive speculation"

    return {
        "score": score,
        "signal": signal,
        "data_available": True,
        "total_points": total_points,
        "details": details,
    }


def _interpret_put_call(ratio: float) -> str:
    if ratio < 0.60:
        return "Extreme call buying - maximum complacency"
    elif ratio < 0.70:
        return "Elevated call buying - notable optimism"
    elif ratio < 0.80:
        return "Slightly optimistic"
    elif ratio < 0.90:
        return "Normal range"
    else:
        return "Elevated put buying - caution/fear present"


def _interpret_vix(level: float) -> str:
    if level < 12:
        return "Extreme low fear - complacency zone"
    elif level < 14:
        return "Low fear"
    elif level < 16:
        return "Mildly low volatility"
    elif level <= 20:
        return "Normal range"
    elif level <= 25:
        return "Elevated fear"
    else:
        return "High fear - panic present"


def _interpret_vix_term(structure: str) -> str:
    mapping = {
        STEEP_CONTANGO: "Market expects calm - complacency in term structure",
        NORMAL_CONTANGO: "Normal term structure",
        FLAT: "Uncertainty - no clear expectation",
        BACKWARDATION: "Hedging demand elevated - fear in term structure",
    }
    return mapping.get(structure, "Unknown")


def _interpret_margin_debt(yoy_pct: float) -> str:
    if yoy_pct >= 30:
        return f"DANGER: Margin debt surging +{yoy_pct:.0f}% YoY"
    elif yoy_pct >= 20:
        return f"WARNING: Rapid leverage increase +{yoy_pct:.0f}% YoY"
    elif yoy_pct >= 10:
        return f"Elevated: +{yoy_pct:.0f}% YoY"
    elif yoy_pct >= 0:
        return f"Normal: +{yoy_pct:.0f}% YoY"
    else:
        return f"Deleveraging: {yoy_pct:.0f}% YoY"
