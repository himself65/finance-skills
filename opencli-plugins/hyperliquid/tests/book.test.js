import { test } from 'node:test';
import assert from 'node:assert/strict';
import { normalizeBook, bookSpread } from '../lib/book.js';

// Shape captured live from l2Book.
const BOOK = {
  coin: 'BTC', time: 1780813166432,
  levels: [
    [ // bids (highest first)
      { px: '61794.0', sz: '19.80703', n: 156 },
      { px: '61793.0', sz: '2.87733', n: 25 },
      { px: '61792.0', sz: '2.44433', n: 10 },
    ],
    [ // asks (lowest first)
      { px: '61795.0', sz: '5.0', n: 12 },
      { px: '61796.0', sz: '3.0', n: 8 },
    ],
  ],
};

test('normalizeBook — bids then asks, capped at depth', () => {
  const rows = normalizeBook(BOOK, 2);
  assert.equal(rows.length, 4); // 2 bids + 2 asks
  assert.deepEqual(rows[0], { side: 'bid', level: 1, px: 61794, sz: 19.80703, orders: 156 });
  assert.equal(rows[1].side, 'bid');
  assert.equal(rows[2].side, 'ask');
  assert.equal(rows[2].px, 61795);
  assert.equal(rows[3].px, 61796);
});

test('normalizeBook — default depth 10, fewer levels ok', () => {
  const rows = normalizeBook(BOOK);
  assert.equal(rows.filter((r) => r.side === 'bid').length, 3);
  assert.equal(rows.filter((r) => r.side === 'ask').length, 2);
});

test('normalizeBook — empty payload', () => {
  assert.deepEqual(normalizeBook({}, 5), []);
  assert.deepEqual(normalizeBook({ levels: [[], []] }, 5), []);
});

test('bookSpread — best bid/ask, mid, spread, bps', () => {
  const s = bookSpread(BOOK);
  assert.equal(s.bestBid, 61794);
  assert.equal(s.bestAsk, 61795);
  assert.equal(s.mid, 61794.5);
  assert.equal(s.spread, 1);
  assert.equal(s.spreadBps.toFixed(4), (1 / 61794.5 * 10000).toFixed(4));
});

test('bookSpread — missing side → nulls', () => {
  const s = bookSpread({ levels: [[], []] });
  assert.equal(s.mid, null);
  assert.equal(s.spread, null);
});
