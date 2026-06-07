/**
 * Account-state normalizers for `clearinghouseState` (perp) and
 * `spotClearinghouseState` (spot). All public — read by 0x address, no auth.
 */

import { num, isoTime } from './api.js';

/** Perp account-level margin summary as a single-row array. */
export function normalizeMarginSummary(state) {
  const m = state?.marginSummary ?? {};
  const cross = state?.crossMarginSummary ?? {};
  return [{
    accountValue: num(m.accountValue),
    totalNtlPos: num(m.totalNtlPos),
    totalRawUsd: num(m.totalRawUsd),
    totalMarginUsed: num(m.totalMarginUsed),
    crossAccountValue: num(cross.accountValue),
    crossMaintenanceMarginUsed: num(state?.crossMaintenanceMarginUsed),
    withdrawable: num(state?.withdrawable),
    numPositions: (state?.assetPositions ?? []).length,
    time: isoTime(state?.time),
  }];
}

/** One row per open perp position. Side derived from the sign of `szi`. */
export function normalizePositions(state) {
  const aps = state?.assetPositions ?? [];
  return aps.map((ap) => {
    const p = ap.position ?? {};
    const szi = num(p.szi);
    const roe = num(p.returnOnEquity);
    return {
      coin: p.coin,
      side: szi == null ? null : szi >= 0 ? 'long' : 'short',
      size: szi == null ? null : Math.abs(szi),
      entryPx: num(p.entryPx),
      positionValue: num(p.positionValue),
      unrealizedPnl: num(p.unrealizedPnl),
      roePct: roe == null ? null : roe * 100,
      leverage: num(p.leverage?.value),
      leverageType: p.leverage?.type ?? null,
      liquidationPx: num(p.liquidationPx),
      marginUsed: num(p.marginUsed),
      fundingSinceOpen: num(p.cumFunding?.sinceOpen),
    };
  });
}

/** One row per spot token balance. `available` = total − hold. */
export function normalizeSpotBalances(state) {
  const balances = state?.balances ?? [];
  return balances.map((b) => {
    const total = num(b.total);
    const hold = num(b.hold);
    return {
      coin: b.coin,
      total,
      hold,
      available: total != null && hold != null ? total - hold : null,
      entryNtl: num(b.entryNtl),
    };
  });
}
