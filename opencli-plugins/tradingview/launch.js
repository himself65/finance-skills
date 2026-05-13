/**
 * tradingview launch — relaunch TradingView.app with --remote-debugging-port enabled.
 *
 * macOS only. Quits any running TradingView, then re-opens it with the CDP flag
 * and polls /json/version until reachable.
 */

import { spawn } from 'node:child_process';
import { platform } from 'node:os';
import { cli, Strategy } from '@jackwener/opencli/registry';

const DEFAULT_PORT = 9222;
const READY_TIMEOUT_MS = 15_000;
const POLL_INTERVAL_MS = 250;

cli({
  site: 'tradingview',
  name: 'launch',
  description: 'Relaunch TradingView.app with --remote-debugging-port enabled (macOS only)',
  access: 'write',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'port', type: 'int', default: DEFAULT_PORT, help: `CDP port (default ${DEFAULT_PORT})` },
  ],
  columns: ['port', 'pid', 'ready'],
  func: async (args) => {
    if (platform() !== 'darwin') {
      throw new Error('tradingview launch is macOS-only (uses `open -a TradingView`).');
    }
    const port = Number(args.port) || DEFAULT_PORT;

    await quitApp('TradingView');
    const pid = await openWithFlag(port);
    const ready = await waitForCdp(port, READY_TIMEOUT_MS);

    return [{ port, pid, ready }];
  },
});

function quitApp(appName) {
  return new Promise((resolve) => {
    const p = spawn('osascript', ['-e', `tell application "${appName}" to quit`], { stdio: 'ignore' });
    p.on('exit', () => resolve());
    p.on('error', () => resolve());
    setTimeout(() => resolve(), 5_000);
  });
}

function openWithFlag(port) {
  return new Promise((resolve, reject) => {
    const p = spawn(
      'open',
      ['-a', 'TradingView', '--args', `--remote-debugging-port=${port}`],
      { stdio: 'ignore', detached: true },
    );
    p.on('error', reject);
    p.on('exit', (code) => {
      if (code === 0) resolve(p.pid ?? null);
      else reject(new Error(`open exited with code ${code}`));
    });
  });
}

async function waitForCdp(port, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (res.ok) return true;
    } catch {
      // keep polling
    }
    await sleep(POLL_INTERVAL_MS);
  }
  return false;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
