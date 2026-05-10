/**
 * Lightweight CDP client — find TradingView tabs, evaluate JS on a tab,
 * capture page screenshots.
 *
 * Used by chart-state.js and screenshot.js so they don't depend on opencli's
 * Electron-app registry (apps.yaml). Uses Node's built-in WebSocket (Node 22+).
 */

import { getCdpEndpoint } from './cookies.js';

const DEFAULT_TIMEOUT_MS = 8_000;

export function isTradingViewUrl(url) {
  if (typeof url !== 'string') return false;
  if (!url.startsWith('https://www.tradingview.com/')) return false;
  if (url.includes('app.asar')) return false;
  return true;
}

export function classifyTab(url) {
  if (typeof url !== 'string') return 'other';
  if (url.includes('/chart/')) return 'chart';
  if (url.includes('/symbols/') && url.includes('/options-chain/')) return 'options';
  if (url.includes('/symbols/')) return 'symbol';
  return 'other';
}

/**
 * List active TradingView tabs reachable via CDP.
 * @returns {Promise<Array<{id:string, type:string, url:string, title:string, webSocketDebuggerUrl:string}>>}
 */
export async function listTradingViewTabs() {
  const endpoint = getCdpEndpoint();
  let raw;
  try {
    const res = await fetch(`${endpoint}/json`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    raw = await res.json();
  } catch (err) {
    throw new Error(
      `Cannot reach CDP at ${endpoint}: ${err instanceof Error ? err.message : String(err)}. ` +
        `Is TradingView running with --remote-debugging-port? Try: opencli tradingview launch`,
    );
  }
  return (Array.isArray(raw) ? raw : [])
    .filter((t) => t.type === 'page' && isTradingViewUrl(t.url) && t.webSocketDebuggerUrl)
    .map((t) => ({
      id: t.id,
      type: classifyTab(t.url),
      url: t.url,
      title: t.title ?? '',
      webSocketDebuggerUrl: t.webSocketDebuggerUrl,
    }));
}

/**
 * Pick a TradingView tab. If `tabId` is set, returns that tab (or throws).
 * Otherwise prefers `chart` > `symbol` > `other`.
 * @param {string} [tabId]
 */
export async function pickTab(tabId) {
  const tabs = await listTradingViewTabs();
  if (tabs.length === 0) {
    throw new Error('No TradingView tab found. Open a chart in TradingView, then retry.');
  }
  if (tabId) {
    const match = tabs.find((t) => t.id === tabId);
    if (!match) {
      throw new Error(
        `Tab id "${tabId}" not found. Run "opencli tradingview status" to list tabs.`,
      );
    }
    return match;
  }
  const order = { chart: 0, symbol: 1, options: 2, other: 3 };
  return [...tabs].sort((a, b) => (order[a.type] ?? 9) - (order[b.type] ?? 9))[0];
}

/**
 * Open a CDP WebSocket session against a specific tab. Returns helpers to
 * `send(method, params)` and `close()`. Caller is responsible for `close()`.
 *
 * @param {{webSocketDebuggerUrl: string}} tab
 */
export async function openSession(tab) {
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(new Error('CDP open timeout')), DEFAULT_TIMEOUT_MS);
    ws.addEventListener('open', () => { clearTimeout(t); resolve(); }, { once: true });
    ws.addEventListener('error', () => { clearTimeout(t); reject(new Error('CDP open error')); }, { once: true });
  });

  let nextId = 1;
  const pending = new Map();
  ws.addEventListener('message', (ev) => {
    let msg;
    try {
      msg = JSON.parse(typeof ev.data === 'string' ? ev.data : ev.data.toString());
    } catch {
      return;
    }
    if (msg.id && pending.has(msg.id)) {
      const p = pending.get(msg.id);
      pending.delete(msg.id);
      p.resolve(msg);
    }
  });

  function send(method, params = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
    return new Promise((resolve, reject) => {
      const id = nextId++;
      const t = setTimeout(() => {
        pending.delete(id);
        reject(new Error(`CDP ${method} timeout (${timeoutMs}ms)`));
      }, timeoutMs);
      pending.set(id, {
        resolve: (msg) => {
          clearTimeout(t);
          if (msg.error) reject(new Error(`CDP ${method} error: ${msg.error.message}`));
          else resolve(msg.result);
        },
      });
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  function close() {
    try { ws.close(); } catch { /* ignore */ }
  }

  return { send, close };
}

/**
 * Run a JS expression in a tab and return the result by value.
 *
 * @param {{webSocketDebuggerUrl: string}} tab
 * @param {string} expression
 * @param {{awaitPromise?: boolean, timeoutMs?: number}} [opts]
 */
export async function evaluateOnTab(tab, expression, opts = {}) {
  const session = await openSession(tab);
  try {
    const result = await session.send('Runtime.evaluate', {
      expression,
      awaitPromise: Boolean(opts.awaitPromise),
      returnByValue: true,
    }, opts.timeoutMs);
    if (result.exceptionDetails) {
      const text = result.exceptionDetails.text || result.exceptionDetails.exception?.description || 'Runtime.evaluate exception';
      throw new Error(text);
    }
    return result.result?.value;
  } finally {
    session.close();
  }
}

/**
 * Capture a PNG screenshot of a tab.
 * @param {{webSocketDebuggerUrl: string}} tab
 * @param {{format?: 'png'|'jpeg'}} [opts]
 * @returns {Promise<Buffer>}
 */
export async function screenshotTab(tab, opts = {}) {
  const session = await openSession(tab);
  try {
    const result = await session.send('Page.captureScreenshot', {
      format: opts.format ?? 'png',
    }, 15_000);
    if (!result?.data) throw new Error('Page.captureScreenshot returned no data');
    return Buffer.from(result.data, 'base64');
  } finally {
    session.close();
  }
}
