"use client";

import { useEffect, useRef } from "react";

// Simplex Noise (compact implementation)
const F2 = 0.5 * (Math.sqrt(3) - 1);
const G2 = (3 - Math.sqrt(3)) / 6;
const grad3 = [
  [1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0],
  [1, 0, 1], [-1, 0, 1], [1, 0, -1], [-1, 0, -1],
  [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1],
];

function createNoise(seed: number) {
  const perm = new Uint8Array(512);
  const permMod12 = new Uint8Array(512);
  const p = new Uint8Array(256);
  for (let i = 0; i < 256; i++) p[i] = i;
  for (let i = 255; i > 0; i--) {
    seed = (seed * 16807 + 0) % 2147483647;
    const j = seed % (i + 1);
    const tmp = p[i];
    p[i] = p[j];
    p[j] = tmp;
  }
  for (let i = 0; i < 512; i++) {
    perm[i] = p[i & 255];
    permMod12[i] = perm[i] % 12;
  }

  return function noise2D(xin: number, yin: number) {
    const s = (xin + yin) * F2;
    const i = Math.floor(xin + s),
      j = Math.floor(yin + s);
    const t = (i + j) * G2;
    const x0 = xin - (i - t),
      y0 = yin - (j - t);
    const i1 = x0 > y0 ? 1 : 0,
      j1 = x0 > y0 ? 0 : 1;
    const x1 = x0 - i1 + G2,
      y1 = y0 - j1 + G2;
    const x2 = x0 - 1 + 2 * G2,
      y2 = y0 - 1 + 2 * G2;
    const ii = i & 255,
      jj = j & 255;
    let n0: number, n1: number, n2: number;
    let t0 = 0.5 - x0 * x0 - y0 * y0;
    if (t0 < 0) n0 = 0;
    else {
      t0 *= t0;
      const gi = permMod12[ii + perm[jj]];
      n0 = t0 * t0 * (grad3[gi][0] * x0 + grad3[gi][1] * y0);
    }
    let t1 = 0.5 - x1 * x1 - y1 * y1;
    if (t1 < 0) n1 = 0;
    else {
      t1 *= t1;
      const gi = permMod12[ii + i1 + perm[jj + j1]];
      n1 = t1 * t1 * (grad3[gi][0] * x1 + grad3[gi][1] * y1);
    }
    let t2 = 0.5 - x2 * x2 - y2 * y2;
    if (t2 < 0) n2 = 0;
    else {
      t2 *= t2;
      const gi = permMod12[ii + 1 + perm[jj + 1]];
      n2 = t2 * t2 * (grad3[gi][0] * x2 + grad3[gi][1] * y2);
    }
    return 70 * (n0 + n1 + n2);
  };
}

export function StockTickerBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const noise = createNoise(7);
    const noise2 = createNoise(42);
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    let W: number, H: number;
    function resize() {
      W = window.innerWidth;
      H = window.innerHeight;
      canvas!.width = W * dpr;
      canvas!.height = H * dpr;
      ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    window.addEventListener("resize", resize);
    resize();

    // Price state
    const BASE_PRICE = 150;
    let price = BASE_PRICE;
    let momentum = 0;
    const priceHistory: { price: number; volume: number }[] = [];
    const MAX_HISTORY = 4000;
    const TICK_SPEED = 60;
    const VOLATILITY = 1.0;
    const PX_PER_TICK = 2;

    function nextTick() {
      const shock = (Math.random() - 0.5) * 0.8 * VOLATILITY;
      const reversion = (BASE_PRICE - price) * 0.001;
      momentum = momentum * 0.95 + shock * 0.3;
      const jump =
        Math.random() < 0.003 ? (Math.random() - 0.5) * 4 * VOLATILITY : 0;
      price += shock + reversion + momentum + jump;
      price = Math.max(BASE_PRICE * 0.5, Math.min(BASE_PRICE * 1.5, price));
      const volume = Math.abs(shock + jump) * 2 + Math.random() * 0.3;
      priceHistory.push({ price, volume });
      if (priceHistory.length > MAX_HISTORY) priceHistory.shift();
    }

    // Pre-fill history
    for (let i = 0; i < 600; i++) nextTick();

    let tickAccum = 0;

    // Colors
    const GREEN = { r: 34, g: 197, b: 94 };
    const RED = { r: 239, g: 68, b: 68 };

    // Particles
    const particles: {
      x: number;
      y: number;
      vx: number;
      vy: number;
      size: number;
      alpha: number;
      life: number;
      decay: number;
    }[] = [];

    function drawGrid(
      chartTop: number,
      chartBottom: number,
      chartLeft: number,
      chartRight: number,
      priceMin: number,
      priceMax: number,
    ) {
      ctx!.strokeStyle = "rgba(200, 149, 108, 0.04)";
      ctx!.lineWidth = 1;
      const priceRange = priceMax - priceMin;
      const step = priceRange > 30 ? 10 : priceRange > 15 ? 5 : 2;
      const firstLine = Math.ceil(priceMin / step) * step;
      for (let p = firstLine; p < priceMax; p += step) {
        const y =
          chartBottom -
          ((p - priceMin) / (priceMax - priceMin)) * (chartBottom - chartTop);
        ctx!.beginPath();
        ctx!.moveTo(chartLeft, y);
        ctx!.lineTo(chartRight, y);
        ctx!.stroke();
      }
      ctx!.strokeStyle = "rgba(200, 149, 108, 0.03)";
      for (let x = chartLeft; x <= chartRight; x += 80) {
        ctx!.beginPath();
        ctx!.moveTo(x, chartTop);
        ctx!.lineTo(x, chartBottom);
        ctx!.stroke();
      }
    }

    let lastTimestamp: number | null = null;
    let animId: number;

    function draw(timestamp: number) {
      if (!lastTimestamp) lastTimestamp = timestamp;
      const dt = Math.min((timestamp - lastTimestamp) / 1000, 0.05);
      lastTimestamp = timestamp;

      tickAccum += dt * TICK_SPEED;
      while (tickAccum >= PX_PER_TICK) {
        nextTick();
        tickAccum -= PX_PER_TICK;
      }

      ctx!.fillStyle = "#0a0a0a";
      ctx!.fillRect(0, 0, W, H);

      const chartLeft = 20;
      const chartRight = W - 60;
      const chartTop = H * 0.08;
      const chartBottom = H * 0.78;
      const chartWidth = chartRight - chartLeft;
      const chartHeight = chartBottom - chartTop;
      const volumeBottom = H * 0.96;
      const volumeHeight = volumeBottom - H * 0.82;

      const visibleTicks = Math.floor(chartWidth / PX_PER_TICK);
      const startIdx = Math.max(0, priceHistory.length - visibleTicks);
      const visibleData = priceHistory.slice(startIdx);

      if (visibleData.length < 2) {
        animId = requestAnimationFrame(draw);
        return;
      }

      let priceMin = Infinity,
        priceMax = -Infinity;
      let maxVol = 0;
      for (const d of visibleData) {
        if (d.price < priceMin) priceMin = d.price;
        if (d.price > priceMax) priceMax = d.price;
        if (d.volume > maxVol) maxVol = d.volume;
      }
      const pricePad = (priceMax - priceMin) * 0.15 + 1;
      priceMin -= pricePad;
      priceMax += pricePad;
      if (maxVol < 0.01) maxVol = 1;

      drawGrid(chartTop, chartBottom, chartLeft, chartRight, priceMin, priceMax);

      // Volume bars
      const barW = Math.max(1, PX_PER_TICK - 1);
      for (let i = 0; i < visibleData.length; i++) {
        const d = visibleData[i];
        const prevPrice = i > 0 ? visibleData[i - 1].price : d.price;
        const isUp = d.price >= prevPrice;
        const col = isUp ? GREEN : RED;
        const barH = (d.volume / maxVol) * volumeHeight;
        const sx =
          chartLeft + (i / (visibleData.length - 1)) * chartWidth;
        ctx!.fillStyle = `rgba(${col.r},${col.g},${col.b}, 0.18)`;
        ctx!.fillRect(sx - barW / 2, volumeBottom - barH, barW, barH);
      }

      // Build screen points
      const points: { x: number; y: number }[] = [];
      for (let i = 0; i < visibleData.length; i++) {
        const x =
          chartLeft + (i / (visibleData.length - 1)) * chartWidth;
        const y =
          chartBottom -
          ((visibleData[i].price - priceMin) / (priceMax - priceMin)) *
            chartHeight;
        points.push({ x, y });
      }

      const trendUp =
        visibleData[visibleData.length - 1].price >= visibleData[0].price;
      const trendColor = trendUp ? GREEN : RED;

      // Gradient fill
      ctx!.beginPath();
      ctx!.moveTo(points[0].x, chartBottom);
      for (const p of points) ctx!.lineTo(p.x, p.y);
      ctx!.lineTo(points[points.length - 1].x, chartBottom);
      ctx!.closePath();
      const fillGrad = ctx!.createLinearGradient(0, chartTop, 0, chartBottom);
      fillGrad.addColorStop(
        0,
        `rgba(${trendColor.r},${trendColor.g},${trendColor.b}, 0.10)`,
      );
      fillGrad.addColorStop(
        0.6,
        `rgba(${trendColor.r},${trendColor.g},${trendColor.b}, 0.03)`,
      );
      fillGrad.addColorStop(
        1,
        `rgba(${trendColor.r},${trendColor.g},${trendColor.b}, 0.0)`,
      );
      ctx!.fillStyle = fillGrad;
      ctx!.fill();

      // Price line
      for (let i = 1; i < points.length; i++) {
        const isUp = points[i].y <= points[i - 1].y;
        const col = isUp ? GREEN : RED;

        // Glow
        ctx!.beginPath();
        ctx!.moveTo(points[i - 1].x, points[i - 1].y);
        ctx!.lineTo(points[i].x, points[i].y);
        ctx!.strokeStyle = `rgba(${col.r},${col.g},${col.b}, 0.12)`;
        ctx!.lineWidth = 10;
        ctx!.lineCap = "round";
        ctx!.stroke();

        // Crisp
        ctx!.beginPath();
        ctx!.moveTo(points[i - 1].x, points[i - 1].y);
        ctx!.lineTo(points[i].x, points[i].y);
        ctx!.strokeStyle = `rgba(${col.r},${col.g},${col.b}, 0.85)`;
        ctx!.lineWidth = 2;
        ctx!.lineCap = "round";
        ctx!.stroke();
      }

      // Live tip
      const tip = points[points.length - 1];
      const tipUp =
        visibleData.length >= 2 &&
        visibleData[visibleData.length - 1].price >=
          visibleData[visibleData.length - 2].price;
      const tipColor = tipUp ? GREEN : RED;

      const time = timestamp / 1000;
      const pulse = 0.5 + 0.5 * Math.sin(time * 4);
      const glowR = 18 + pulse * 10;

      const glow = ctx!.createRadialGradient(
        tip.x,
        tip.y,
        0,
        tip.x,
        tip.y,
        glowR,
      );
      glow.addColorStop(
        0,
        `rgba(${tipColor.r},${tipColor.g},${tipColor.b}, 0.45)`,
      );
      glow.addColorStop(
        0.35,
        `rgba(${tipColor.r},${tipColor.g},${tipColor.b}, 0.12)`,
      );
      glow.addColorStop(
        1,
        `rgba(${tipColor.r},${tipColor.g},${tipColor.b}, 0)`,
      );
      ctx!.beginPath();
      ctx!.arc(tip.x, tip.y, glowR, 0, Math.PI * 2);
      ctx!.fillStyle = glow;
      ctx!.fill();

      ctx!.beginPath();
      ctx!.arc(tip.x, tip.y, 4, 0, Math.PI * 2);
      ctx!.fillStyle = `rgba(${Math.min(255, tipColor.r + 60)},${Math.min(255, tipColor.g + 60)},${Math.min(255, tipColor.b + 40)}, 0.95)`;
      ctx!.fill();

      // Particles near live edge
      if (Math.random() < 0.4) {
        particles.push({
          x: tip.x + (Math.random() - 0.5) * 30,
          y: tip.y + (Math.random() - 0.5) * 40,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.8,
          size: 0.8 + Math.random() * 2,
          alpha: 0.15 + Math.random() * 0.5,
          life: 1.0,
          decay: 0.005 + Math.random() * 0.01,
        });
      }
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.life -= p.decay;
        if (p.life <= 0) {
          particles.splice(i, 1);
          continue;
        }
        p.x += p.vx;
        p.y += p.vy;
        p.vy += (Math.random() - 0.5) * 0.1;
        p.vx *= 0.99;
        const a = p.alpha * p.life;
        const col = tipColor;
        const gr = ctx!.createRadialGradient(
          p.x,
          p.y,
          0,
          p.x,
          p.y,
          p.size * 3,
        );
        gr.addColorStop(
          0,
          `rgba(${col.r},${col.g},${col.b}, ${a * 0.35})`,
        );
        gr.addColorStop(1, `rgba(${col.r},${col.g},${col.b}, 0)`);
        ctx!.beginPath();
        ctx!.arc(p.x, p.y, p.size * 3, 0, Math.PI * 2);
        ctx!.fillStyle = gr;
        ctx!.fill();
        ctx!.beginPath();
        ctx!.arc(p.x, p.y, p.size * 0.4, 0, Math.PI * 2);
        ctx!.fillStyle = `rgba(${Math.min(255, col.r + 80)},${Math.min(255, col.g + 80)},${Math.min(255, col.b + 60)}, ${a})`;
        ctx!.fill();
      }
      while (particles.length > 60) particles.shift();

      // Scan line
      const scanY = (time * 50) % H;
      const scanGrad = ctx!.createLinearGradient(0, scanY - 2, 0, scanY + 2);
      scanGrad.addColorStop(0, "rgba(200, 149, 108, 0)");
      scanGrad.addColorStop(0.5, "rgba(200, 149, 108, 0.012)");
      scanGrad.addColorStop(1, "rgba(200, 149, 108, 0)");
      ctx!.fillStyle = scanGrad;
      ctx!.fillRect(0, scanY - 2, W, 4);

      animId = requestAnimationFrame(draw);
    }

    animId = requestAnimationFrame(draw);

    return () => {
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(animId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 w-screen h-screen -z-10 pointer-events-none"
      style={{ opacity: 0.4 }}
    />
  );
}
