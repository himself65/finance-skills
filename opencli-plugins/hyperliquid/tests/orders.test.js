import { test } from 'node:test';
import assert from 'node:assert/strict';
import { normalizeOpenOrders, normalizeFills } from '../lib/orders.js';

// Shape captured live from frontendOpenOrders.
const ORDERS = [
  {
    coin: 'BTC', side: 'A', limitPx: '61862.0', sz: '0.02075', oid: 461332213736,
    timestamp: 1780813213847, triggerCondition: 'N/A', isTrigger: false, triggerPx: '0.0',
    isPositionTpsl: false, reduceOnly: false, orderType: 'Limit', origSz: '0.02075', tif: 'Alo',
  },
  {
    coin: 'ETH', side: 'B', limitPx: '1500.0', sz: '2.0', oid: 999,
    timestamp: 1780813213847, triggerCondition: 'Below 1500.0', isTrigger: true, triggerPx: '1500.0',
    reduceOnly: true, orderType: 'Stop Limit', origSz: '2.0', tif: 'Gtc',
  },
];

test('normalizeOpenOrders — side decode + trigger handling', () => {
  const rows = normalizeOpenOrders(ORDERS);
  const btc = rows[0];
  assert.equal(btc.side, 'sell'); // A
  assert.equal(btc.orderType, 'Limit');
  assert.equal(btc.limitPx, 61862);
  assert.equal(btc.tif, 'Alo');
  assert.equal(btc.reduceOnly, false);
  assert.equal(btc.triggerCondition, null); // "N/A" suppressed
  assert.equal(btc.triggerPx, null); // not a trigger order
  assert.equal(btc.time, '2026-06-07T06:20:13.847Z');

  const eth = rows[1];
  assert.equal(eth.side, 'buy'); // B
  assert.equal(eth.reduceOnly, true);
  assert.equal(eth.triggerCondition, 'Below 1500.0');
  assert.equal(eth.triggerPx, 1500);
});

// Shape captured live from userFills.
const FILLS = [
  {
    coin: 'OP', px: '0.09506', sz: '165.4', side: 'B', time: 1780813213454,
    dir: 'Close Short', closedPnl: '-0.05789', hash: '0xabc', oid: 1, crossed: true,
    fee: '0.01', tid: 1, feeToken: 'USDC',
  },
  {
    coin: 'BTC', px: '61800.0', sz: '0.1', side: 'A', time: 1780813000000,
    dir: 'Open Short', closedPnl: '0.0', hash: '0xdef', oid: 2, crossed: false,
    fee: '0.5', tid: 2, feeToken: 'USDC',
  },
];

test('normalizeFills — notional, side decode, fields', () => {
  const rows = normalizeFills(FILLS);
  const op = rows[0];
  assert.equal(op.coin, 'OP');
  assert.equal(op.side, 'buy'); // B
  assert.equal(op.dir, 'Close Short');
  assert.equal(op.px, 0.09506);
  assert.equal(op.notional.toFixed(5), (0.09506 * 165.4).toFixed(5));
  assert.equal(op.closedPnl, -0.05789);
  assert.equal(op.crossed, true);
  assert.equal(op.feeToken, 'USDC');
  assert.equal(rows[1].side, 'sell'); // A
  assert.equal(rows[1].crossed, false);
});

test('normalizeFills — limit slices most-recent-first', () => {
  const rows = normalizeFills(FILLS, 1);
  assert.equal(rows.length, 1);
  assert.equal(rows[0].coin, 'OP');
});

test('normalizeFills — no limit returns all', () => {
  assert.equal(normalizeFills(FILLS).length, 2);
  assert.equal(normalizeFills(FILLS, 0).length, 2);
  assert.equal(normalizeFills([]).length, 0);
});
