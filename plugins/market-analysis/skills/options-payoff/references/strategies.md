# Options Strategy Payoff Formulas

## Butterfly (Put or Call)

**Structure**: Buy K1, Sell 2×K2, Buy K3 (K1 < K2 < K3, wings equal: K2-K1 = K3-K2)
**Cost**: Net debit (long butterfly)
**Max profit**: wing_width - premium, at K2
**Max loss**: premium paid, outside K1 or K3

```js
function expiryValue(S, k1, k2, k3) {
  if (S >= k3) return 0;
  if (S >= k2) return k3 - S;
  if (S >= k1) return S - k1;
  return 0;
}
function theoreticalValue(S, k1, k2, k3, T, r, iv) {
  const s = iv/100;
  return bsPut(S,k1,T,r,s) - 2*bsPut(S,k2,T,r,s) + bsPut(S,k3,T,r,s);
}
```

**Broken wing butterfly**: K3-K2 ≠ K2-K1 → one side has residual directional exposure. Adjust formula accordingly.

---

## Vertical Spread

### Call Debit Spread (bullish)
Buy K1 call, Sell K2 call (K1 < K2)
```js
function expiryValue(S, k1, k2) {
  return Math.max(S-k1, 0) - Math.max(S-k2, 0);
}
function theoreticalValue(S, k1, k2, T, r, iv) {
  return bsCall(S,k1,T,r,iv/100) - bsCall(S,k2,T,r,iv/100);
}
```
Max profit: K2-K1-debit | Max loss: debit paid

### Put Debit Spread (bearish)
Buy K2 put, Sell K1 put (K1 < K2)
```js
function expiryValue(S, k1, k2) {
  return Math.max(k2-S, 0) - Math.max(k1-S, 0);
}
```
Max profit: K2-K1-debit | Max loss: debit paid

### Credit Spread
Sell the near strike, buy the far strike for protection. Net credit received.
Expiry payoff = -(debit_spread expiry). Max profit = credit, Max loss = width - credit.

---

## Calendar Spread (Time Spread)

**Structure**: Buy far-DTE option at K, Sell near-DTE option at K (same strike)
**Key**: Cannot show a simple expiry curve — instead show value as DTE_near approaches 0.

```js
// T_near = DTE_near/365, T_far = DTE_far/365
function theoreticalValue(S, K, T_near, T_far, r, iv_near, iv_far, isCall) {
  if (isCall) return bsCall(S,K,T_far,r,iv_far/100) - bsCall(S,K,T_near,r,iv_near/100);
  return bsPut(S,K,T_far,r,iv_far/100) - bsPut(S,K,T_near,r,iv_near/100);
}
// At near expiry (T_near=0): near leg expires, far leg retains time value
function atNearExpiry(S, K, T_far, r, iv_far, isCall) {
  if (isCall) return bsCall(S,K,T_far,r,iv_far/100);
  return bsPut(S,K,T_far,r,iv_far/100);
}
```

**UI note for calendar**: Show TWO sliders for DTE (near and far). "Expiry" curve = at-near-expiry value minus premium paid.
**Max profit**: When spot = K at near expiry (maximum time value difference)
**Max loss**: Premium paid (if spot moves far from K in either direction)

---

## Iron Condor

**Structure**: Sell K2 put, Buy K1 put (put spread) + Sell K3 call, Buy K4 call (call spread)
K1 < K2 < K3 < K4. Net credit received.

```js
function expiryValue(S, k1, k2, k3, k4) {
  const putSpread = Math.max(k2-S,0) - Math.max(k1-S,0); // loss on short put spread
  const callSpread = Math.max(S-k3,0) - Math.max(S-k4,0); // loss on short call spread
  return -(putSpread + callSpread); // net payoff from short spreads
}
// credit = premium_received. P&L = credit + expiryValue
function theoreticalValue(S, k1, k2, k3, k4, T, r, iv) {
  const s=iv/100;
  return -(bsPut(S,k2,T,r,s)-bsPut(S,k1,T,r,s)) - (bsCall(S,k3,T,r,s)-bsCall(S,k4,T,r,s));
}
```
Max profit: credit received | Max loss: max(K2-K1, K4-K3) - credit

---

## Straddle

**Structure**: Buy call at K + Buy put at K (same strike, same expiry)
```js
function expiryValue(S, k) {
  return Math.abs(S - k); // = max(S-K,0) + max(K-S,0)
}
function theoreticalValue(S, k, T, r, iv) {
  return bsCall(S,k,T,r,iv/100) + bsPut(S,k,T,r,iv/100);
}
```
Breakevens: K ± premium. Max loss: premium paid (if S=K at expiry).

---

## Strangle

**Structure**: Buy OTM put at K1 + Buy OTM call at K2 (K1 < K2)
```js
function expiryValue(S, k1, k2) {
  return Math.max(k1-S, 0) + Math.max(S-k2, 0);
}
function theoreticalValue(S, k1, k2, T, r, iv) {
  return bsPut(S,k1,T,r,iv/100) + bsCall(S,k2,T,r,iv/100);
}
```
Breakevens: K1 - premium, K2 + premium. Max loss: premium if K1 ≤ S ≤ K2.

---

## Covered Call

**Structure**: Long 100 shares at cost_basis + Sell call at K
```js
function expiryValue(S, K, costBasis) {
  const stockPnl = S - costBasis;
  const shortCallPnl = -Math.max(S-K, 0) + premium; // premium = call premium received
  return stockPnl + shortCallPnl;
}
```
Max profit: K - costBasis + premium | Max loss: costBasis - premium (stock goes to 0)

---

## Naked / Cash-Secured Put

**Structure**: Sell put at K, receive premium
```js
function expiryValue(S, K, premium) {
  return premium - Math.max(K-S, 0);
}
```
Max profit: premium | Max loss: K - premium (stock goes to 0)

---

## Edge Cases

- **DTE = 0**: skip BS entirely, use intrinsic value only
- **IV = 0**: BS undefined (σ=0), use max(intrinsic, 0)  
- **K1 > K2**: warn user, auto-sort strikes ascending
- **Negative theoretical value**: clip to 0 for display (arbitrage-free floor)
- **Calendar with IV skew**: use separate IV sliders for near vs far leg
