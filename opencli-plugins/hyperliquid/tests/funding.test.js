import { test } from 'node:test';
import assert from 'node:assert/strict';
import { normalizeFundingHistory, normalizePredictedFundings } from '../lib/funding.js';

// Shape captured live from fundingHistory.
const HISTORY = [
  { coin: 'BTC', fundingRate: '0.0000125', premium: '-0.0003305881', time: 1780808400000 },
  { coin: 'BTC', fundingRate: '0.0000125', premium: '-0.0003786101', time: 1780812000055 },
];

test('normalizeFundingHistory — rate %, APR, premium %', () => {
  const rows = normalizeFundingHistory(HISTORY);
  assert.equal(rows.length, 2);
  const r = rows[0];
  assert.equal(r.coin, 'BTC');
  assert.equal(r.fundingRatePct.toFixed(5), '0.00125'); // 0.0000125 * 100
  assert.equal(r.fundingAprPct.toFixed(4), '10.9500'); // 0.0000125 * 24 * 365 * 100
  assert.equal(r.premiumPct.toFixed(6), '-0.033059');
  assert.ok(r.time.startsWith('2026-'));
});

// Shape captured live from predictedFundings.
const PREDICTED = [
  ['0G', [
    ['BinPerp', { fundingRate: '-0.00004554', nextFundingTime: 1780819200000, fundingIntervalHours: 4 }],
    ['HlPerp', { fundingRate: '-0.0000397323', nextFundingTime: 1780812000000, fundingIntervalHours: 1 }],
    ['BybitPerp', { fundingRate: '0.00005', nextFundingTime: 1780819200000, fundingIntervalHours: 4 }],
  ]],
  ['BTC', [
    ['HlPerp', { fundingRate: '0.0000125', nextFundingTime: 1780812000000, fundingIntervalHours: 1 }],
  ]],
];

test('normalizePredictedFundings — pivots to per-coin APR + spreads', () => {
  const rows = normalizePredictedFundings(PREDICTED);
  const og = rows.find((r) => r.coin === '0G');
  // HL hourly: -0.0000397323 * 24 * 365 * 100
  assert.equal(og.hlAprPct.toFixed(2), (-0.0000397323 * 24 * 365 * 100).toFixed(2));
  // Binance 4h: -0.00004554 / 4 * 24 * 365 * 100
  assert.equal(og.binanceAprPct.toFixed(2), (-0.00004554 / 4 * 24 * 365 * 100).toFixed(2));
  assert.equal(og.bybitAprPct.toFixed(2), (0.00005 / 4 * 24 * 365 * 100).toFixed(2));
  // Spread = HL APR − Binance APR
  assert.equal(og.hlVsBinancePct.toFixed(4), (og.hlAprPct - og.binanceAprPct).toFixed(4));
  assert.ok(og.nextHlFunding.startsWith('2026-'));
});

test('normalizePredictedFundings — missing venues yield null legs/spreads', () => {
  const rows = normalizePredictedFundings(PREDICTED);
  const btc = rows.find((r) => r.coin === 'BTC');
  assert.ok(btc.hlAprPct != null);
  assert.equal(btc.binanceAprPct, null);
  assert.equal(btc.bybitAprPct, null);
  assert.equal(btc.hlVsBinancePct, null);
  assert.equal(btc.hlVsBybitPct, null);
});

test('normalizePredictedFundings — coin filter (exact, case-insensitive)', () => {
  const rows = normalizePredictedFundings(PREDICTED, 'btc');
  assert.equal(rows.length, 1);
  assert.equal(rows[0].coin, 'BTC');
});
