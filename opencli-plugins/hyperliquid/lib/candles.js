/**
 * Candle helpers for `candleSnapshot`.
 * Wire row: { t (open ms), T (close ms), s (coin), i (interval), o, h, l, c, v, n }.
 */

import { num, isoTime } from './api.js';

/** Supported interval → milliseconds. Used to derive a startTime from a count. */
export const INTERVAL_MS = {
  '1m': 60_000,
  '3m': 180_000,
  '5m': 300_000,
  '15m': 900_000,
  '30m': 1_800_000,
  '1h': 3_600_000,
  '2h': 7_200_000,
  '4h': 14_400_000,
  '8h': 28_800_000,
  '12h': 43_200_000,
  '1d': 86_400_000,
  '3d': 259_200_000,
  '1w': 604_800_000,
  '1M': 2_592_000_000,
};

/** Normalize raw candle rows to OHLCV with ISO open time. */
export function normalizeCandles(rows) {
  return (rows ?? []).map((c) => ({
    time: isoTime(c.t),
    open: num(c.o),
    high: num(c.h),
    low: num(c.l),
    close: num(c.c),
    volume: num(c.v),
    trades: c.n ?? null,
  }));
}
