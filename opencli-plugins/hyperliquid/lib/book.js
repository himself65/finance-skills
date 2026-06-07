/**
 * Order-book normalizer for `l2Book`.
 * Payload: { coin, time, levels: [ bids[], asks[] ] }, each level { px, sz, n }.
 */

import { num } from './api.js';

/**
 * Flatten an l2 snapshot into rows capped at `depth` levels per side.
 * Bids first (best/highest px first as returned), then asks.
 */
export function normalizeBook(payload, depth) {
  const levels = payload?.levels ?? [[], []];
  const d = Number.isFinite(Number(depth)) && Number(depth) > 0 ? Number(depth) : 10;
  const mk = (side) => (lvl, i) => ({
    side,
    level: i + 1,
    px: num(lvl.px),
    sz: num(lvl.sz),
    orders: lvl.n ?? null,
  });
  const bids = (levels[0] ?? []).slice(0, d).map(mk('bid'));
  const asks = (levels[1] ?? []).slice(0, d).map(mk('ask'));
  return [...bids, ...asks];
}

/** Best-bid/ask spread summary from a raw l2 payload (for skill prose). */
export function bookSpread(payload) {
  const levels = payload?.levels ?? [[], []];
  const bestBid = num(levels[0]?.[0]?.px);
  const bestAsk = num(levels[1]?.[0]?.px);
  if (bestBid == null || bestAsk == null) {
    return { bestBid, bestAsk, mid: null, spread: null, spreadBps: null };
  }
  const mid = (bestBid + bestAsk) / 2;
  const spread = bestAsk - bestBid;
  return { bestBid, bestAsk, mid, spread, spreadBps: mid ? (spread / mid) * 10000 : null };
}
