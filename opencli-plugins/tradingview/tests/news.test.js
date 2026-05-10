import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  astToText,
  buildHeadlinesUrl,
  buildStoryUrl,
  epochToIso,
  normalizeHeadline,
} from '../lib/news.js';

test('buildHeadlinesUrl — base URL with default lang', () => {
  const url = buildHeadlinesUrl({});
  assert.match(url, /^https:\/\/news-headlines\.tradingview\.com\/v2\/headlines\?/);
  assert.match(url, /client=web/);
  assert.match(url, /lang=en/);
  assert.match(url, /streaming=false/);
});

test('buildHeadlinesUrl — symbol + category + section', () => {
  const url = buildHeadlinesUrl({ symbol: 'NASDAQ:AAPL', category: 'stock', section: 'analysis' });
  const parsed = new URL(url);
  assert.equal(parsed.searchParams.get('symbol'), 'NASDAQ:AAPL');
  assert.equal(parsed.searchParams.get('category'), 'stock');
  assert.equal(parsed.searchParams.get('section'), 'analysis');
});

test('buildStoryUrl — id + lang', () => {
  const url = buildStoryUrl('story-123', 'zh');
  const parsed = new URL(url);
  assert.equal(parsed.searchParams.get('id'), 'story-123');
  assert.equal(parsed.searchParams.get('lang'), 'zh');
});

test('astToText — flat text node', () => {
  assert.equal(astToText({ type: 'text', value: 'hello' }), 'hello');
  assert.equal(astToText('plain string'), 'plain string');
});

test('astToText — paragraph wraps in double newline', () => {
  const out = astToText({ type: 'p', children: [{ type: 'text', value: 'one' }] });
  assert.equal(out, 'one\n\n');
});

test('astToText — nested paragraphs and links', () => {
  const ast = {
    type: 'root',
    children: [
      { type: 'p', children: [{ type: 'text', value: 'Hello ' }, { type: 'a', href: 'x', children: [{ type: 'text', value: 'world' }] }] },
      { type: 'p', children: [{ type: 'text', value: 'Second.' }] },
    ],
  };
  const out = astToText(ast);
  assert.match(out, /Hello world/);
  assert.match(out, /Second\./);
  assert.equal(out.split('\n\n').length, 3); // two p's = two trailing breaks → splits to 3 segments
});

test('astToText — list-items prefix with dash', () => {
  const ast = {
    type: 'list',
    children: [
      { type: 'list-item', children: [{ type: 'text', value: 'a' }] },
      { type: 'list-item', children: [{ type: 'text', value: 'b' }] },
    ],
  };
  assert.equal(astToText(ast), '- a\n- b\n\n');
});

test('astToText — handles missing/null gracefully', () => {
  assert.equal(astToText(null), '');
  assert.equal(astToText(undefined), '');
  assert.equal(astToText({}), '');
  assert.equal(astToText({ type: 'unknown' }), '');
});

test('epochToIso — seconds + ms autodetected', () => {
  assert.equal(epochToIso(1746000000), '2025-04-30T08:00:00.000Z');
  assert.equal(epochToIso(1746000000000), '2025-04-30T08:00:00.000Z');
  assert.equal(epochToIso(0), '');
  assert.equal(epochToIso(null), '');
  assert.equal(epochToIso('not-a-number'), '');
});

test('normalizeHeadline — full headline shape', () => {
  const item = {
    id: 'tag:reuters.com,2026:newsml_L1N3GH04T:0',
    title: 'Apple beats expectations',
    source: 'reuters',
    published: 1746000000,
    urgency: 2,
    relatedSymbols: ['NASDAQ:AAPL', 'NASDAQ:MSFT', { symbol: 'NASDAQ:GOOGL' }],
    storyPath: '/news/reuters/AAPL-beat',
  };
  const row = normalizeHeadline(item);
  assert.equal(row.id, item.id);
  assert.equal(row.title, item.title);
  assert.equal(row.provider, 'reuters');
  assert.equal(row.urgency, 2);
  assert.equal(row.related_symbols, 'NASDAQ:AAPL,NASDAQ:MSFT,NASDAQ:GOOGL');
  assert.equal(row.link, 'https://www.tradingview.com/news/reuters/AAPL-beat');
});

test('normalizeHeadline — limits relatedSymbols list', () => {
  const item = {
    id: 'x', title: 't', source: 's', published: 1,
    relatedSymbols: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    storyPath: '/p',
  };
  const row = normalizeHeadline(item, { limitRelatedSymbols: 3 });
  assert.equal(row.related_symbols, 'A,B,C');
});
