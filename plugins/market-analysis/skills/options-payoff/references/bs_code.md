# Black-Scholes JavaScript Implementation

Copy-paste ready. Include at the top of every widget's `<script>` block.

```js
// Normal CDF via Horner's method (accurate to 7 decimal places)
function normCDF(x) {
  const a1=0.254829592, a2=-0.284496736, a3=1.421413741,
        a4=-1.453152027, a5=1.061405429, p=0.3275911;
  const sign = x < 0 ? -1 : 1;
  x = Math.abs(x);
  const t = 1 / (1 + p * x);
  const y = 1 - (((((a5*t + a4)*t + a3)*t + a2)*t + a1)*t) * Math.exp(-x*x/2);
  return 0.5 * (1 + sign * y);
}

// Black-Scholes Put price
// S=spot, K=strike, T=years to expiry, r=rate (decimal), sigma=IV (decimal)
function bsPut(S, K, T, r, sigma) {
  if (T <= 0) return Math.max(K - S, 0);
  if (sigma <= 0) return Math.max(K - S, 0);
  const d1 = (Math.log(S/K) + (r + sigma*sigma/2)*T) / (sigma*Math.sqrt(T));
  const d2 = d1 - sigma * Math.sqrt(T);
  return K * Math.exp(-r*T) * normCDF(-d2) - S * normCDF(-d1);
}

// Black-Scholes Call price
function bsCall(S, K, T, r, sigma) {
  if (T <= 0) return Math.max(S - K, 0);
  if (sigma <= 0) return Math.max(S - K, 0);
  const d1 = (Math.log(S/K) + (r + sigma*sigma/2)*T) / (sigma*Math.sqrt(T));
  const d2 = d1 - sigma * Math.sqrt(T);
  return S * normCDF(d1) - K * Math.exp(-r*T) * normCDF(d2);
}
```

## Typical Parameter Conversions

```js
const T = dte / 365;        // DTE slider value → years
const r = rate / 100;       // rate slider % → decimal
const sigma = iv / 100;     // IV slider % → decimal
```

## Computing Greeks (for display)

```js
function bsDelta(S, K, T, r, sigma, isCall) {
  if (T <= 0) return isCall ? (S>K?1:0) : (S<K?-1:0);
  const d1 = (Math.log(S/K) + (r + sigma*sigma/2)*T) / (sigma*Math.sqrt(T));
  return isCall ? normCDF(d1) : normCDF(d1) - 1;
}

function bsTheta(S, K, T, r, sigma, isCall) {
  if (T <= 0) return 0;
  const d1 = (Math.log(S/K) + (r + sigma*sigma/2)*T) / (sigma*Math.sqrt(T));
  const d2 = d1 - sigma * Math.sqrt(T);
  const term1 = -S * Math.exp(-0.5*d1*d1) / Math.sqrt(2*Math.PI) * sigma / (2*Math.sqrt(T));
  if (isCall) return (term1 - r * K * Math.exp(-r*T) * normCDF(d2)) / 365;
  return (term1 + r * K * Math.exp(-r*T) * normCDF(-d2)) / 365;
}
```
