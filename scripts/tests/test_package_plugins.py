import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

SCRIPT = Path(__file__).resolve().parents[1] / "package_plugins.py"
SPEC = importlib.util.spec_from_file_location("package_plugins", SCRIPT)
packages = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(packages)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for folder in ("plugins", ".claude-plugin", ".agents", "docs"):
            shutil.copytree(packages.ROOT / folder, self.root / folder)
        for name in ("LICENSE", "README.md"):
            shutil.copyfile(packages.ROOT / name, self.root / name)

    def edit_json(self, path, edit):
        target = self.root / path
        data = json.loads(target.read_text())
        edit(data)
        target.write_bytes(packages.json_bytes(data))

    def test_generated_metadata_is_current_and_mcp_pin_is_preserved(self):
        plugins = packages.sync(self.root, check=True)
        self.assertEqual(len(plugins), 6)
        legacy = packages.read_json(self.root / "plugins/data-providers/.mcp.json")
        portable = packages.read_json(self.root / "plugins/data-providers/mcp.json")
        self.assertEqual(portable["$schema"], packages.MCP_SCHEMA)
        server = portable["mcpServers"]["tradingview"]
        self.assertEqual(server, {"type": "stdio", **legacy["mcpServers"]["tradingview"]})
        marketplace = packages.read_json(self.root / packages.MARKETPLACE)
        for entry in marketplace["plugins"]:
            plugin_root = self.root / entry["source"]["path"]
            manifest = packages.read_json(plugin_root / "plugin.json")
            self.assertEqual(entry["name"], manifest["name"])
            overlay = packages.read_json(plugin_root / ".codex-plugin/plugin.json")
            self.assertEqual(overlay["version"], manifest["version"])
            self.assertEqual(overlay["interface"], manifest["extensions"]["com.openai"]["interface"])

    def test_detects_and_repairs_stale_generated_metadata(self):
        self.edit_json("plugins/market-analysis/.codex-plugin/plugin.json",
                       lambda data: data.update(version="0.0.0"))
        with self.assertRaisesRegex(ValueError, "Stale generated file"):
            packages.sync(self.root, check=True)
        packages.sync(self.root)
        packages.sync(self.root, check=True)

    def test_release_rejects_mismatched_tag_and_manifest_versions(self):
        with self.assertRaisesRegex(ValueError, "does not match"):
            packages.build(self.root, version="v0.0.0")
        self.assertFalse((self.root / "dist").exists())
        self.edit_json("plugins/market-analysis/plugin.json", lambda data: data.update(version="0.0.0"))
        with self.assertRaisesRegex(ValueError, "Version drift"):
            packages.sync(self.root)

    def test_schema_and_marketplace_omissions_fail(self):
        self.edit_json("plugins/market-analysis/plugin.json", lambda data: data.pop("$schema"))
        with self.assertRaisesRegex(ValueError, "portable schema"):
            packages.sync(self.root)
        self.edit_json(".claude-plugin/marketplace.json", lambda data: data["plugins"].pop(0))
        with self.assertRaisesRegex(ValueError, "list every plugin"):
            packages.sync(self.root)

    def test_duplicate_skill_archives_fail_instead_of_overwriting(self):
        source = self.root / "plugins/market-analysis/skills/yfinance-data"
        shutil.copytree(source, self.root / "plugins/startup-tools/skills/yfinance-data")
        with self.assertRaisesRegex(ValueError, "Duplicate skill archive"):
            packages.build(self.root)

    def test_symlinks_are_rejected(self):
        skill = self.root / "plugins/startup-tools/skills/startup-analysis"
        (skill / "linked-secret").symlink_to(self.root / "LICENSE")
        with self.assertRaisesRegex(ValueError, "Symlink component"):
            packages.build(self.root)

    def test_archives_are_self_contained_complete_reproducible_and_clean(self):
        skill = self.root / "plugins/startup-tools/skills/startup-analysis"
        (skill / ".env").write_text("SECRET=excluded")
        (skill / ".env.local").write_text("SECRET=excluded")
        (skill / "__pycache__").mkdir()
        (skill / "__pycache__/junk.pyc").write_text("excluded")
        version = packages.read_json(self.root / ".claude-plugin/marketplace.json")["metadata"]["version"]
        count = packages.build(self.root, version=f"v{version}")
        output = self.root / "dist"
        _, plugins = packages.catalog(self.root)
        self.assertEqual(count, len(plugins) + sum(len(skills) for _, _, skills in plugins) + 1)
        before = {file.name: file.read_bytes() for file in output.iterdir()}
        for path, manifest, skills in plugins:
            name = manifest["name"]
            with ZipFile(output / f"{name}.zip") as archive:
                entries = archive.namelist()
                self.assertTrue(all(entry.startswith(f"{name}/") for entry in entries))
                self.assertFalse(any("marketplace.json" in entry for entry in entries))
                self.assertFalse(any(".env" in entry or "__pycache__" in entry for entry in entries))
                self.assertEqual(json.loads(archive.read(f"{name}/plugin.json")), manifest)
                self.assertIn(f"{name}/.codex-plugin/plugin.json", entries)
                for skill_dir in skills:
                    key = f"skills/{skill_dir.name}/SKILL.md"
                    self.assertEqual(archive.read(f"{name}/{key}"), (skill_dir / "SKILL.md").read_bytes())
                if name == "finance-data-providers":
                    self.assertIn(f"{name}/mcp.json", entries)
                    self.assertIn(f"{name}/.mcp.json", entries)
            for skill_dir in skills:
                with ZipFile(output / f"{skill_dir.name}.zip") as archive:
                    self.assertIn(f"{skill_dir.name}/SKILL.md", archive.namelist())
        with ZipFile(output / "finance-skills-marketplace.zip") as archive:
            unpacked = self.root / "unpacked"
            archive.extractall(unpacked)
            marketplace = packages.read_json(unpacked / packages.MARKETPLACE)
            for entry in marketplace["plugins"]:
                self.assertTrue((unpacked / entry["source"]["path"] / "plugin.json").is_file())
        for line in (output / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ")
            self.assertEqual(digest, hashlib.sha256((output / name).read_bytes()).hexdigest())
        (output / "stale.zip").write_text("old release")
        packages.build(self.root)
        self.assertEqual(before, {file.name: file.read_bytes() for file in output.iterdir()})


if __name__ == "__main__":
    unittest.main()
