import { test } from 'node:test';
import assert from 'node:assert/strict';
import { normalizeMarginSummary, normalizePositions, normalizeSpotBalances } from '../lib/account.js';

// Shape captured live from clearinghouseState.
const STATE = {
  marginSummary: {
    accountValue: '3068411.2214310002', totalNtlPos: '3249530.5273230001',
    totalRawUsd: '2836958.3107520002', totalMarginUsed: '162476.526307',
  },
  crossMarginSummary: { accountValue: '3068000.0' },
  crossMaintenanceMarginUsed: '50000.0',
  withdrawable: '2900000.0',
  assetPositions: [
    {
      type: 'oneWay',
      position: {
        coin: 'BTC', szi: '-0.68254', leverage: { type: 'cross', value: 20 },
        entryPx: '61725.4', positionValue: '42174.82914', unrealizedPnl: '-44.758088',
        returnOnEquity: '-0.021247573', liquidationPx: '4465719.47', marginUsed: '2108.741457',
        maxLeverage: 50, cumFunding: { allTime: '167111.9', sinceOpen: '-54.85748', sinceChange: '0.0' },
      },
    },
    {
      type: 'oneWay',
      position: {
        coin: 'ETH', szi: '12.5', leverage: { type: 'isolated', value: 10 },
        entryPx: '1600.0', positionValue: '20000.0', unrealizedPnl: '187.5',
        returnOnEquity: '0.09', liquidationPx: '900.0', marginUsed: '2000.0',
        cumFunding: { sinceOpen: '3.21' },
      },
    },
  ],
  time: 1780813167365,
};

test('normalizeMarginSummary — single summary row', () => {
  const [row] = normalizeMarginSummary(STATE);
  assert.equal(row.accountValue, 3068411.2214310002);
  assert.equal(row.totalMarginUsed, 162476.526307);
  assert.equal(row.crossAccountValue, 3068000);
  assert.equal(row.crossMaintenanceMarginUsed, 50000);
  assert.equal(row.withdrawable, 2900000);
  assert.equal(row.numPositions, 2);
  assert.equal(row.time, '2026-06-07T06:19:27.365Z');
});

test('normalizePositions — side from sign of szi, abs size, ROE %', () => {
  const rows = normalizePositions(STATE);
  assert.equal(rows.length, 2);
  const btc = rows[0];
  assert.equal(btc.coin, 'BTC');
  assert.equal(btc.side, 'short');
  assert.equal(btc.size, 0.68254);
  assert.equal(btc.entryPx, 61725.4);
  assert.equal(btc.unrealizedPnl, -44.758088);
  assert.equal(btc.roePct.toFixed(4), '-2.1248');
  assert.equal(btc.leverage, 20);
  assert.equal(btc.leverageType, 'cross');
  assert.equal(btc.fundingSinceOpen, -54.85748);

  const eth = rows[1];
  assert.equal(eth.side, 'long');
  assert.equal(eth.size, 12.5);
  assert.equal(eth.leverageType, 'isolated');
});

test('normalizePositions — empty when no positions', () => {
  assert.deepEqual(normalizePositions({ assetPositions: [] }), []);
  assert.deepEqual(normalizePositions({}), []);
});

test('normalizeSpotBalances — available = total − hold', () => {
  const state = {
    balances: [
      { coin: 'USDC', total: '1000.5', hold: '200.0', entryNtl: '0.0' },
      { coin: 'PURR', total: '500.0', hold: '0.0', entryNtl: '45.0' },
    ],
  };
  const rows = normalizeSpotBalances(state);
  assert.equal(rows[0].coin, 'USDC');
  assert.equal(rows[0].available, 800.5);
  assert.equal(rows[1].available, 500);
  assert.equal(rows[1].entryNtl, 45);
});

test('normalizeSpotBalances — empty balances', () => {
  assert.deepEqual(normalizeSpotBalances({ balances: [] }), []);
});
