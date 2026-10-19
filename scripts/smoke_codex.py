#!/usr/bin/env python3
"""Read the built marketplace with a real Codex loader without installing plugins."""

import json
import queue
import subprocess
import tempfile
import threading
from pathlib import Path
from zipfile import ZipFile

from package_plugins import ROOT, MARKETPLACE, require


def main():
    print(subprocess.check_output(["codex", "--version"], text=True).strip(), flush=True)
    with tempfile.TemporaryDirectory(prefix="finance-codex-smoke-") as temporary:
        root = Path(temporary)
        with ZipFile(ROOT / "dist/finance-skills-marketplace.zip") as archive:
            archive.extractall(root)
        marketplace = root / MARKETPLACE
        entries = json.loads(marketplace.read_text())["plugins"]
        expected = {}
        originals = {}
        for entry in entries:
            path = root / entry["source"]["path"]
            manifest = json.loads((path / "plugin.json").read_text())
            expected[entry["name"]] = {
                "version": manifest["version"],
                "skills": {f"{entry['name']}:{skill.parent.name}" for skill in (path / "skills").glob("*/SKILL.md")},
                "mcp": set(json.loads((path / "mcp.json").read_text())["mcpServers"]) if (path / "mcp.json").exists() else set(),
            }
            for relative in ("plugin.json", "mcp.json", ".codex-plugin/plugin.json", ".mcp.json"):
                file = path / relative
                if file.exists():
                    originals[file] = file.read_bytes()

        with tempfile.TemporaryFile(mode="w+") as log:
            process = subprocess.Popen(["codex", "app-server", "--stdio"], cwd=root,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=log, text=True)
            replies = queue.Queue()

            def read_replies():
                for line in process.stdout:
                    replies.put(json.loads(line))

            threading.Thread(target=read_replies, daemon=True).start()

            def request(request_id, method, params):
                process.stdin.write(json.dumps({"id": request_id, "method": method, "params": params}) + "\n")
                process.stdin.flush()
                while True:
                    response = replies.get(timeout=30)
                    if response.get("id") == request_id:
                        require("error" not in response, str(response.get("error")))
                        return response["result"]

            try:
                request(1, "initialize", {"clientInfo": {"name": "finance_package_check", "version": "1.0.0"},
                                          "capabilities": {"experimentalApi": True}})
                request_id = 1
                for mode in ("combined", "portable", "compatibility"):
                    for file, content in originals.items():
                        file.write_bytes(content)
                    for file in originals:
                        legacy = file.parent.name == ".codex-plugin" or file.name == ".mcp.json"
                        if (mode == "portable" and legacy) or (mode == "compatibility" and not legacy):
                            file.unlink()
                    for entry in entries:
                        request_id += 1
                        plugin = request(request_id, "plugin/read", {
                            "marketplacePath": str(marketplace), "pluginName": entry["name"],
                        })["plugin"]
                        want = expected[entry["name"]]
                        require({skill["name"] for skill in plugin["skills"]} == want["skills"],
                                f"{mode}: missing skills in {entry['name']}")
                        require(set(plugin["mcpServers"]) == want["mcp"], f"{mode}: MCP discovery mismatch")
                        require(plugin["summary"]["localVersion"] == want["version"], f"{mode}: version mismatch")
                        require(plugin["summary"]["availability"] == "AVAILABLE", f"{mode}: plugin unavailable")
                    print(f"{mode}: loaded {len(entries)} plugins, "
                          f"{sum(len(value['skills']) for value in expected.values())} skills, "
                          f"{sum(len(value['mcp']) for value in expected.values())} MCP server", flush=True)
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


if __name__ == "__main__":
    main()
