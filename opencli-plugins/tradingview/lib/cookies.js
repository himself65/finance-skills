/**
 * CDP cookie harvest + Node-direct fetch.
 *
 * Why: TradingView desktop pages are subject to browser CORS preflight
 * rejection when calling cross-origin POSTs to scanner.tradingview.com from
 * page context. Even though TradingView's own pages call those endpoints,
 * they do so from Electron's main process (Node network stack, no CORS).
 *
 * This helper replicates that path:
 *   1. Connect to the desktop app's CDP /json/version endpoint
 *   2. Open the browser-level WebSocket
 *   3. Call Storage.getCookies (browser-wide)
 *   4. Build a Cookie header for .tradingview.com
 *   5. Run fetch from Node directly with that cookie — no CORS involvement
 *
 * The cookie value is cached for the process lifetime (each opencli command
 * is a fresh process, but a single command may issue multiple fetches).
 */

const DEFAULT_ENDPOINT = 'http://127.0.0.1:9222';
const HARVEST_TIMEOUT_MS = 5000;

let _cachedCookieHeader = null;

export const TV_HEADERS = {
  Origin: 'https://www.tradingview.com',
  Referer: 'https://www.tradingview.com/',
  'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' +
    'TradingView/3.1.0 Chrome/140.0.7339.133 Electron/38.2.2 Safari/537.36 TVDesktop/3.1.0',
};

export function getCdpEndpoint() {
  return (process.env.OPENCLI_CDP_ENDPOINT ?? DEFAULT_ENDPOINT).replace(/\/$/, '');
}

async function fetchBrowserWsUrl(endpoint) {
  const url = `${endpoint}/json/version`;
  let meta;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    meta = await res.json();
  } catch (err) {
    throw new Error(
      `Cannot reach CDP at ${endpoint}: ${err instanceof Error ? err.message : String(err)}. ` +
        `Is TradingView running with --remote-debugging-port? Try: opencli tradingview launch`,
    );
  }
  if (!meta.webSocketDebuggerUrl) {
    throw new Error(`CDP /json/version missing webSocketDebuggerUrl — incompatible browser?`);
  }
  return meta.webSocketDebuggerUrl;
}

function harvestCookies(browserWsUrl) {
  return new Promise((resolve, reject) => {
    let ws;
    try {
      ws = new WebSocket(browserWsUrl);
    } catch (err) {
      reject(new Error(`Cannot create WebSocket to ${browserWsUrl}: ${err}`));
      return;
    }

    const timeout = setTimeout(() => {
      try { ws.close(); } catch { /* ignore */ }
      reject(new Error(`CDP Storage.getCookies timeout (${HARVEST_TIMEOUT_MS}ms)`));
    }, HARVEST_TIMEOUT_MS);

    const reqId = 1;

    ws.addEventListener('message', (ev) => {
      let msg;
      try {
        msg = JSON.parse(typeof ev.data === 'string' ? ev.data : ev.data.toString());
      } catch {
        return;
      }
      if (msg.id !== reqId) return;
      clearTimeout(timeout);
      try { ws.close(); } catch { /* ignore */ }
      if (msg.error) {
        reject(new Error(`CDP error: ${msg.error.message}`));
        return;
      }
      resolve(msg.result?.cookies ?? []);
    });

    ws.addEventListener('error', () => {
      clearTimeout(timeout);
      reject(new Error(`CDP WebSocket error connecting to ${browserWsUrl}`));
    });

    ws.addEventListener('open', () => {
      ws.send(JSON.stringify({ id: reqId, method: 'Storage.getCookies', params: {} }));
    });
  });
}

/**
 * Get a Cookie header string with all .tradingview.com cookies.
 * Cached for the process lifetime.
 */
export async function getTradingViewCookieHeader() {
  if (_cachedCookieHeader != null) return _cachedCookieHeader;

  const endpoint = getCdpEndpoint();
  const wsUrl = await fetchBrowserWsUrl(endpoint);
  const cookies = await harvestCookies(wsUrl);
  const tvCookies = cookies.filter(
    (c) =>
      c?.domain &&
      (c.domain === 'tradingview.com' ||
        c.domain === '.tradingview.com' ||
        c.domain.endsWith('.tradingview.com')),
  );
  if (tvCookies.length === 0) {
    throw new Error(
      'No tradingview.com cookies found. Make sure you are signed into the TradingView desktop app.',
    );
  }
  _cachedCookieHeader = tvCookies.map((c) => `${c.name}=${c.value}`).join('; ');
  return _cachedCookieHeader;
}

/**
 * Fetch a TradingView endpoint from Node with cookies + standard headers
 * attached. Use this for ALL cross-origin TradingView API calls — page-context
 * fetch is blocked by CORS preflight.
 *
 * @param {string} url
 * @param {RequestInit} [init]
 */
export async function tradingViewFetch(url, init = {}) {
  const cookieHeader = await getTradingViewCookieHeader();
  return fetch(url, {
    ...init,
    headers: {
      ...TV_HEADERS,
      Cookie: cookieHeader,
      ...(init.headers ?? {}),
    },
  });
}

/** Test helper — reset the cached cookie header. */
export function _resetCookieCache() {
  _cachedCookieHeader = null;
}
