#!/usr/bin/env python3
"""
Shared EMA/SMA calculation utilities for Market Top Detector.

All functions expect prices in most-recent-first order.
"""


def calc_ema(prices: list[float], period: int) -> float:
    """
    Calculate Exponential Moving Average from prices (most recent first).

    Args:
        prices: List of prices, most recent first.
        period: EMA period (must be >= 1).

    Returns:
        EMA value as float.

    Raises:
        ValueError: If prices is empty or period < 1.
    """
    if not prices:
        raise ValueError("prices must not be empty")
    if period < 1:
        raise ValueError("period must be >= 1")

    if len(prices) < period:
        return sum(prices) / len(prices)

    prices_rev = prices[::-1]
    sma = sum(prices_rev[:period]) / period
    ema = sma
    k = 2 / (period + 1)
    for p in prices_rev[period:]:
        ema = p * k + ema * (1 - k)
    return ema


def calc_sma(prices: list[float], period: int) -> float:
    """
    Calculate Simple Moving Average from prices (most recent first).

    Args:
        prices: List of prices, most recent first.
        period: SMA period (must be >= 1).

    Returns:
        SMA value as float.

    Raises:
        ValueError: If prices is empty or period < 1.
    """
    if not prices:
        raise ValueError("prices must not be empty")
    if period < 1:
        raise ValueError("period must be >= 1")

    if len(prices) < period:
        return sum(prices) / len(prices)
    return sum(prices[:period]) / period
