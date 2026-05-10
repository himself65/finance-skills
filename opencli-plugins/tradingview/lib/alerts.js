/**
 * Alerts response normalizer.
 *
 * Wire shape (captured from live pricealerts.tradingview.com/list_alerts):
 *   { s: "ok", id: "<session>", r: [ { id, symbol, condition, ... } ] }
 *
 * Older community docs reference `alerts`/`fires`/`items`/`data` keys —
 * we accept all of them as fallbacks.
 */

export function normalizeAlerts(payload) {
  const arr = pickAlertList(payload);
  return arr.map((a) => ({
    id: a.id ?? a.alert_id ?? null,
    name: a.name ?? a.title ?? '',
    symbol: parseSymbol(a),
    type: a.type ?? a.alert_type ?? '',
    condition: extractCondition(a),
    value: numericOrNull(extractValue(a)),
    active: a.active ?? a.is_active ?? null,
    status: a.status ?? a.s ?? '',
    fired_at: a.fired_at ?? a.last_fire ?? a.created_at ?? '',
  }));
}

function pickAlertList(payload) {
  if (!payload) return [];
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload.r)) return payload.r;
  if (Array.isArray(payload.alerts)) return payload.alerts;
  if (Array.isArray(payload.fires)) return payload.fires;
  if (Array.isArray(payload.items)) return payload.items;
  if (Array.isArray(payload.log)) return payload.log;
  if (Array.isArray(payload.data)) return payload.data;
  return [];
}

function parseSymbol(a) {
  // TradingView wraps the resolution metadata in a JSON-encoded string field
  // named `symbol` or `ticker`, prefixed with `=`.
  const raw = a.symbol ?? a.ticker ?? a.name ?? '';
  if (typeof raw !== 'string') return String(raw);
  if (raw.startsWith('=')) {
    try {
      const parsed = JSON.parse(raw.slice(1));
      return parsed.symbol ?? parsed.ticker ?? raw;
    } catch {
      return raw;
    }
  }
  return raw;
}

function extractCondition(a) {
  if (!a.condition) return '';
  if (typeof a.condition === 'string') return a.condition;
  if (typeof a.condition === 'object') {
    return a.condition.type ?? a.condition.cond ?? JSON.stringify(a.condition);
  }
  return String(a.condition);
}

function extractValue(a) {
  if (a.value != null) return a.value;
  if (a.price != null) return a.price;
  if (a.condition?.value != null) return a.condition.value;
  if (Array.isArray(a.condition?.params) && a.condition.params.length > 0) {
    return a.condition.params[0];
  }
  return null;
}

function numericOrNull(v) {
  if (v == null) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}
