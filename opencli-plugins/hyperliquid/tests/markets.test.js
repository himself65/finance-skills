import { test } from 'node:test';
import assert from 'node:assert/strict';
import { normalizePerpMarkets, normalizeSpotMarkets, resolveMids } from '../lib/markets.js';

// Shapes captured live from metaAndAssetCtxs.
const PERP_META = {
  universe: [
    { name: 'BTC', maxLeverage: 40, szDecimals: 5 },
    { name: 'MATIC', maxLeverage: 20, isDelisted: true },
  ],
};
const PERP_CTXS = [
  {
    funding: '0.0000120074', openInterest: '33163.84416', prevDayPx: '61001.0',
    dayNtlVlm: '2384788662.6', premium: '-0.0004852641', oraclePx: '61822.0',
    markPx: '61791.0', midPx: '61791.5',
  },
  {
    funding: '0.000001', openInterest: '0.0', prevDayPx: '0.5',
    dayNtlVlm: '0.0', premium: '0.0', oraclePx: '0.5', markPx: '0.5', midPx: '0.5',
  },
];

test('normalizePerpMarkets — zips universe with ctxs by index', () => {
  const rows = normalizePerpMarkets(PERP_META, PERP_CTXS);
  assert.equal(rows.length, 2);
  const btc = rows[0];
  assert.equal(btc.coin, 'BTC');
  assert.equal(btc.markPx, 61791);
  assert.equal(btc.midPx, 61791.5);
  assert.equal(btc.oraclePx, 61822);
  assert.equal(btc.maxLeverage, 40);
  assert.equal(btc.delisted, false);
  // change24h = (61791 - 61001) / 61001 * 100
  assert.equal(btc.change24hPct.toFixed(4), '1.2951');
  // funding hourly % and APR
  assert.equal(btc.fundingHrPct.toFixed(6), '0.001201');
  assert.equal(btc.fundingAprPct.toFixed(2), '10.52');
  // oi notional = 33163.84416 * 61791
  assert.equal(Math.round(btc.oiNotional), Math.round(33163.84416 * 61791));
  // premium %
  assert.equal(btc.premiumPct.toFixed(6), '-0.048526');
});

test('normalizePerpMarkets — flags delisted', () => {
  const rows = normalizePerpMarkets(PERP_META, PERP_CTXS);
  assert.equal(rows[1].coin, 'MATIC');
  assert.equal(rows[1].delisted, true);
});

// Shapes captured live from spotMetaAndAssetCtxs.
const SPOT_META = {
  tokens: [
    { name: 'USDC', index: 0 },
    { name: 'PURR', index: 1 },
    { name: 'HFUN', index: 2 },
  ],
  universe: [
    { tokens: [1, 0], name: 'PURR/USDC', index: 0, isCanonical: true },
    { tokens: [2, 0], name: '@1', index: 1, isCanonical: false },
  ],
};
const SPOT_CTXS = [
  {
    prevDayPx: '0.089779', dayNtlVlm: '931726.7', markPx: '0.090247',
    midPx: '0.0901115', circulatingSupply: '595295651.9', coin: 'PURR/USDC',
  },
  {
    prevDayPx: '1.0', dayNtlVlm: '10.0', markPx: '2.0',
    midPx: '2.0', circulatingSupply: '100.0', coin: '@1',
  },
];

test('normalizeSpotMarkets — resolves base token + market cap', () => {
  const rows = normalizeSpotMarkets(SPOT_META, SPOT_CTXS);
  assert.equal(rows[0].pair, 'PURR/USDC');
  assert.equal(rows[0].base, 'PURR');
  assert.equal(rows[0].markPx, 0.090247);
  assert.equal(rows[0].canonical, true);
  // market cap = markPx * circulatingSupply
  assert.equal(Math.round(rows[0].marketCap), Math.round(0.090247 * 595295651.9));
  // change24h = (0.090247 - 0.089779) / 0.089779 * 100
  assert.equal(rows[0].change24hPct.toFixed(4), '0.5213');
  // second pair is non-canonical; base token index 2 resolves to HFUN
  assert.equal(rows[1].canonical, false);
  assert.equal(rows[1].base, 'HFUN');
});

test('resolveMids — perp keys pass through, @index resolves to BASE/QUOTE', () => {
  const allMids = { BTC: '61791.5', '@1': '2.0', '#1000': '0.5' };
  const rows = resolveMids(allMids, SPOT_META);
  const byCoin = Object.fromEntries(rows.map((r) => [r.coin, r.mid]));
  assert.equal(byCoin.BTC, 61791.5);
  assert.equal(byCoin['HFUN/USDC'], 2.0); // @1 (tokens [2,0]) → HFUN/USDC
  assert.equal(byCoin['#1000'], 0.5); // builder perp-dex key passes through
});

test('resolveMids — case-insensitive substring filter', () => {
  const allMids = { BTC: '1', ETH: '2', BTCDOM: '3' };
  const rows = resolveMids(allMids, SPOT_META, 'btc');
  const coins = rows.map((r) => r.coin).sort();
  assert.deepEqual(coins, ['BTC', 'BTCDOM']);
});
