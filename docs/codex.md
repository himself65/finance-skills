# OpenAI Codex installation and releases

Finance Skills shares the same skill sources across Codex, Claude, and other Agent Skills clients. The six plugin roots use the portable Agent Plugins 1.0 format documented in [OpenAI's packaging guide](https://developers.openai.com/plugins/build/plugins). Generated compatibility manifests also support clients that load `.codex-plugin/plugin.json`.

## Install from GitHub

With a Codex CLI that provides `codex plugin`:

```bash
codex plugin marketplace add himself65/finance-skills
codex plugin add finance-market-analysis@finance-skills
```

Replace `finance-market-analysis` with any group listed in the [README](../README.md). To pin a published release, add the marketplace with `--ref vX.Y.Z`, replacing `vX.Y.Z` with a tag containing this support. To refresh a tracked Git source, run `codex plugin marketplace upgrade finance-skills` and refresh/reinstall the selected plugin in your client.

The desktop app can browse the **Finance Skills** source after registration. The marketplace makes all six groups available; it does not install every group automatically. If your CLI does not offer `plugin`, update the client or use the skills-only installer:

```bash
npx skills add himself65/finance-skills -a codex --skill yfinance-data
```

## Import a release archive

Download assets from [GitHub Releases](https://github.com/himself65/finance-skills/releases). Releases created before Codex packaging was added only contain individual skill ZIPs.

| Asset | Use |
| --- | --- |
| `finance-market-analysis.zip` (and the other five `finance-<group>.zip` files) | One self-contained plugin per ZIP. Select this in a client that offers plugin ZIP import. It contains the manifest, all group skills, supporting references, and MCP configuration when applicable. |
| `finance-skills-marketplace.zip` | All groups plus a local marketplace. Extract it to a persistent directory, then run `codex plugin marketplace add /absolute/path/to/extracted-directory`. This is a marketplace bundle, not a single-plugin upload. |
| `<skill-name>.zip` | Existing standalone Agent Skill format. It contains one skill and its references, with no plugin manifest or MCP setup. |
| `SHA256SUMS` | SHA-256 checksums for every ZIP. |

With all release files downloaded into one directory, verify them with `sha256sum -c SHA256SUMS` on Linux or `shasum -a 256 -c SHA256SUMS` on macOS.

## Runtime requirements

- Financial analysis and external readers need the shell, network access, credentials, and binaries described in each skill. Importing a plugin does not install Python packages or log in to third-party services.
- The full `finance-data-providers` plugin includes TradingView's pinned local MCP server. It requires `uvx` and a compatible Python version. Its portable `mcp.json` declares `stdio`; `.mcp.json` remains available for legacy clients. Web-only hosts cannot launch this local process. Installing only `tradingview-mcp.zip` does not configure the server.
- Claude's command-preprocessing syntax is not assumed to run in Codex. Skills containing those probes explicitly instruct other hosts to run the enclosed command using their shell tool and use the real result.
- `options-payoff` and `generative-ui` use an available visualization tool, or save standalone HTML with its own styles and dependencies. Claude-only `show_widget`, injected CSS, and `sendPrompt` are not assumed to exist in Codex.
- All market and brokerage operations remain read-only; these plugins do not execute trades.

## Maintain the package metadata

Edit these source files:

- `plugins/<group>/plugin.json`: portable identity, version, and OpenAI presentation under `extensions.com.openai.interface`.
- `.claude-plugin/marketplace.json`: plugin inventory and release version for the existing installer.
- `plugins/data-providers/.mcp.json`: canonical pinned TradingView command.
- `plugins/<group>/skills/`: shared skill sources.

Run `npm run plugins:sync` after changing source metadata. It generates `.agents/plugins/marketplace.json`, each `.codex-plugin/plugin.json`, and portable `mcp.json`. Do not edit these generated files directly. The marketplace's `source.path` is relative to the repository/extracted marketplace root.

Python 3.10+ is sufficient for packaging; no Python dependencies or Node package installation are needed for these commands:

```bash
python3 scripts/package_plugins.py sync
python3 scripts/package_plugins.py check
python3 -m unittest discover -s scripts/tests -v
python3 scripts/package_plugins.py build
```

Equivalent npm scripts are `plugins:sync`, `plugins:check`, `test:plugins`, and `plugins:build`. Outputs go to ignored `dist/`. Packaging includes only plugin components and the license, skips local caches and `.env` files, rejects symlinks, preserves individual skill archive names, and writes reproducible ZIPs with checksums. The check fails on stale generated files, missing plugins, duplicate skill archive names, or inconsistent versions.

With Codex installed, run `npm run plugins:smoke` after building. It extracts the actual marketplace ZIP into a temporary directory and uses Codex's `plugin/read` API to verify all skills, versions, and MCP declarations in combined, portable-only, and compatibility-only layouts. It does not install plugins, change account configuration, or invoke market-data tools. This smoke test uses the experimental app-server API and may need adjustment when that API changes.

## Release

From a clean checkout, the existing release command now synchronizes Codex metadata before committing and tagging:

```bash
pnpm bump minor
```

`ccbump` updates the source versions, runs the metadata generator, then commits, tags, and pushes according to its options. To prepare files without committing, tagging, or pushing:

```bash
pnpm bump minor --no-commit --no-tag --no-push
```

The `v*` workflow tests the packager, checks that the tag matches every manifest, and publishes all plugin, marketplace, and skill ZIPs with `SHA256SUMS`. Prerelease tags create prereleases and do not replace the latest stable release. The PR workflow checks generated files and builds the same assets before merge.

GitHub distribution and local import do not publish a listing in OpenAI's public directory. Public-directory submission is a separate process with publisher, listing, and review requirements.
