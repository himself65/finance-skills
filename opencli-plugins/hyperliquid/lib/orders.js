/**
 * Normalizers for `frontendOpenOrders` and `userFills`.
 * Hyperliquid encodes side as "A" (ask = sell) / "B" (bid = buy).
 */

import { num, isoTime } from './api.js';

const SIDE = { A: 'sell', B: 'buy' };

/** One row per resting open order. */
export function normalizeOpenOrders(orders) {
  return (orders ?? []).map((o) => ({
    coin: o.coin,
    side: SIDE[o.side] ?? o.side,
    orderType: o.orderType ?? null,
    limitPx: num(o.limitPx),
    sz: num(o.sz),
    origSz: num(o.origSz),
    oid: o.oid ?? null,
    tif: o.tif ?? null,
    reduceOnly: o.reduceOnly === true,
    triggerCondition: o.triggerCondition && o.triggerCondition !== 'N/A' ? o.triggerCondition : null,
    triggerPx: o.isTrigger ? num(o.triggerPx) : null,
    time: isoTime(o.timestamp),
  }));
}

/**
 * One row per fill (trade). The API returns most-recent-first; `limit` caps
 * the count after normalization.
 */
export function normalizeFills(fills, limit) {
  const rows = (fills ?? []).map((f) => {
    const px = num(f.px);
    const sz = num(f.sz);
    return {
      coin: f.coin,
      dir: f.dir ?? null,
      side: SIDE[f.side] ?? f.side,
      px,
      sz,
      notional: px != null && sz != null ? px * sz : null,
      closedPnl: num(f.closedPnl),
      fee: num(f.fee),
      feeToken: f.feeToken ?? null,
      crossed: f.crossed === true,
      hash: f.hash ?? null,
      time: isoTime(f.time),
    };
  });
  const n = Number(limit);
  return Number.isFinite(n) && n > 0 ? rows.slice(0, n) : rows;
}
