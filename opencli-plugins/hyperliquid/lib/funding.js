/**
 * Funding normalizers: historical funding (`fundingHistory`) and the
 * cross-venue predicted-funding screen (`predictedFundings`).
 */

import { num, isoTime, fundingToApr } from './api.js';

/** One row per historical hourly funding print for a coin. */
export function normalizeFundingHistory(rows) {
  return (rows ?? []).map((r) => {
    const rate = num(r.fundingRate);
    const premium = num(r.premium);
    return {
      coin: r.coin,
      fundingRatePct: rate == null ? null : rate * 100,
      fundingAprPct: fundingToApr(r.fundingRate, 1),
      premiumPct: premium == null ? null : premium * 100,
      time: isoTime(r.time),
    };
  });
}

const VENUE_KEYS = { HlPerp: 'hl', BinPerp: 'binance', BybitPerp: 'bybit' };

/**
 * Pivot `predictedFundings` into one row per coin with each venue's funding
 * normalized to APR %, plus HL-vs-venue spreads — a funding-arb screen.
 *
 * Wire shape:
 *   [ [coin, [ [venueName, {fundingRate, fundingIntervalHours, nextFundingTime}], ... ]], ... ]
 *
 * Venue funding intervals differ (HL hourly, Binance/Bybit usually 4h), so
 * each leg is annualized with its own `fundingIntervalHours`.
 *
 * @param {Array} data
 * @param {string} [coinFilter]  exact (case-insensitive) coin match
 */
export function normalizePredictedFundings(data, coinFilter) {
  const filter = coinFilter ? String(coinFilter).toUpperCase() : null;
  const rows = [];
  for (const entry of data ?? []) {
    const coin = entry?.[0];
    if (filter && String(coin).toUpperCase() !== filter) continue;
    const apr = {};
    let nextHl = null;
    for (const [vName, v] of entry?.[1] ?? []) {
      const key = VENUE_KEYS[vName];
      if (!key || !v) continue;
      apr[key] = fundingToApr(v.fundingRate, v.fundingIntervalHours);
      if (key === 'hl') nextHl = v.nextFundingTime;
    }
    const hl = apr.hl ?? null;
    rows.push({
      coin,
      hlAprPct: hl,
      binanceAprPct: apr.binance ?? null,
      bybitAprPct: apr.bybit ?? null,
      hlVsBinancePct: hl != null && apr.binance != null ? hl - apr.binance : null,
      hlVsBybitPct: hl != null && apr.bybit != null ? hl - apr.bybit : null,
      nextHlFunding: isoTime(nextHl),
    });
  }
  return rows;
}
