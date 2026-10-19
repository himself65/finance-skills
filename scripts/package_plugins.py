#!/usr/bin/env python3
"""Generate Codex metadata and build release archives using only the stdlib."""

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
MARKETPLACE = Path(".agents/plugins/marketplace.json")
SEMVER = re.compile(
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)
IGNORED = {".git", ".DS_Store", "node_modules", "__pycache__", ".pytest_cache"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def catalog(root, version=None):
    marketplace = read_json(root / ".claude-plugin/marketplace.json")
    current = marketplace["metadata"]["version"]
    require(SEMVER.fullmatch(current), f"Invalid version: {current}")
    if version is not None:
        require(version.removeprefix("v") == current,
                f"Release tag {version} does not match manifest version {current}")
    plugins = []
    names, skill_names, paths = set(), set(), set()
    for entry in marketplace["plugins"]:
        source = entry["source"]
        require(re.fullmatch(r"\./plugins/[a-z0-9-]+", source),
                f"Unsupported plugin source: {source}")
        path = Path(source)
        require(not (root / path).is_symlink(), f"Symlink plugin: {path}")
        manifest = read_json(root / path / "plugin.json")
        name = manifest["name"]
        require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) and len(name) <= 64,
                f"Invalid plugin name: {name}")
        require(name == entry["name"] and name not in names, f"Duplicate/mismatched plugin: {name}")
        require(manifest["version"] == entry["version"] == current, f"Version drift: {name}")
        require(manifest.get("$schema") == PLUGIN_SCHEMA, f"Missing portable schema: {name}")
        require(not {"skills", "mcpServers", "apps", "interface"}.intersection(manifest),
                f"Legacy fields at portable root: {name}")
        interface = manifest["extensions"]["com.openai"]["interface"]
        for field in ("displayName", "shortDescription"):
            value = interface[field]
            require(isinstance(value, str) and 0 < len(value.strip()) <= 30,
                    f"{name}: {field} must contain 1-30 characters")
        require(interface.get("category"), f"Missing category: {name}")
        skills = sorted((root / path / "skills").iterdir())
        skills = [skill for skill in skills if not skill.name.startswith(".") and skill.is_dir()]
        require(skills, f"No skills: {name}")
        for skill in skills:
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            require(text.startswith("---\n") and "\n---\n" in text[4:], f"No frontmatter: {skill}")
            frontmatter = text.split("---", 2)[1]
            require(re.search(rf"^name: {re.escape(skill.name)}$", frontmatter, re.M),
                    f"Skill name mismatch: {skill}")
            require(re.search(r"^description: \S", frontmatter, re.M), f"No description: {skill}")
            require(skill.name not in skill_names, f"Duplicate skill archive name: {skill.name}")
            skill_names.add(skill.name)
        names.add(name)
        paths.add(path)
        plugins.append((path, manifest, skills))
    actual = {path.parent.relative_to(root) for path in (root / "plugins").glob("*/plugin.json")}
    require(paths == actual, "Marketplace must list every plugin exactly once")
    require(plugins, "No plugins in marketplace")
    return marketplace, plugins


def generated_files(root, marketplace, plugins):
    entries, files = [], {}
    for path, manifest, _ in plugins:
        interface = manifest["extensions"]["com.openai"]["interface"]
        entries.append({
            "name": manifest["name"],
            "source": {"source": "local", "path": f"./{path.as_posix()}"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"},
            "category": interface["category"],
        })
        overlay = {key: value for key, value in manifest.items() if key not in ("$schema", "extensions")}
        overlay.update(manifest["extensions"]["com.openai"])
        overlay["skills"] = "./skills/"
        legacy_mcp = root / path / ".mcp.json"
        if legacy_mcp.exists():
            servers = read_json(legacy_mcp)["mcpServers"]
            require(servers, f"Empty MCP configuration: {path}")
            portable_servers = {}
            for name, server in servers.items():
                # This repo bundles a pinned local stdio server. Reject new transports
                # until their portable/auth mapping is deliberately implemented.
                require(server.get("command") and "url" not in server, f"Unsupported MCP transport: {name}")
                portable_servers[name] = {"type": "stdio", **server}
            files[path / "mcp.json"] = json_bytes({"$schema": MCP_SCHEMA, "mcpServers": portable_servers})
            overlay["mcpServers"] = "./.mcp.json"
        else:
            require(not (root / path / "mcp.json").exists(), f"Orphan generated mcp.json: {path}")
        files[path / ".codex-plugin/plugin.json"] = json_bytes(overlay)
    files[MARKETPLACE] = json_bytes({
        "name": marketplace["name"],
        "interface": {"displayName": "Finance Skills"},
        "plugins": entries,
    })
    return files


def sync(root=ROOT, check=False, version=None):
    marketplace, plugins = catalog(root, version)
    for path, content in generated_files(root, marketplace, plugins).items():
        destination = root / path
        if check:
            require(destination.is_file() and destination.read_bytes() == content,
                    f"Stale generated file: {path}; run npm run plugins:sync")
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
    return plugins


def component_files(directory):
    """Include components, excluding local caches and credentials at any depth."""
    require(not directory.is_symlink(), f"Symlink component: {directory}")
    for path in sorted(directory.iterdir()):
        if (path.name in IGNORED or path.name == ".env" or path.name.startswith(".env.")
                or path.suffix in {".pyc", ".swp", ".swo"} or path.name.endswith("~")):
            continue
        require(not path.is_symlink(), f"Symlink component: {path}")
        if path.is_dir():
            yield from component_files(path)
        elif path.is_file():
            yield path


def plugin_files(root, path):
    directory = root / path
    files = [directory / "plugin.json", directory / ".codex-plugin/plugin.json"]
    for name in ("mcp.json", ".mcp.json"):
        if (directory / name).exists():
            files.append(directory / name)
    for name in ("skills", "assets"):
        if (directory / name).exists():
            files.extend(component_files(directory / name))
    for file in files:
        require(not file.is_symlink(), f"Symlink component: {file}")
    return {file.relative_to(directory).as_posix(): file.read_bytes() for file in files}


def write_zip(path, files):
    # Fixed timestamps and ordering make repeated builds byte-for-byte identical.
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    with ZipFile(path) as archive:
        require(archive.testzip() is None, f"Corrupt ZIP: {path}")


def build(root=ROOT, output=None, version=None):
    plugins = sync(root, check=True, version=version)
    output = output or root / "dist"
    # Validate and build before replacing previous outputs.
    with tempfile.TemporaryDirectory(prefix="finance-release-") as temporary:
        staging = Path(temporary)
        marketplace_files = {
            MARKETPLACE.as_posix(): (root / MARKETPLACE).read_bytes(),
            "README.md": (root / "README.md").read_bytes(),
            "docs/codex.md": (root / "docs/codex.md").read_bytes(),
            "LICENSE": (root / "LICENSE").read_bytes(),
        }
        for path, manifest, skills in plugins:
            files = plugin_files(root, path)
            files["LICENSE"] = (root / "LICENSE").read_bytes()
            prefix = manifest["name"]
            write_zip(staging / f"{prefix}.zip", {f"{prefix}/{key}": value for key, value in files.items()})
            marketplace_files.update({f"{path.as_posix()}/{key}": value for key, value in files.items()})
            for skill in skills:
                write_zip(staging / f"{skill.name}.zip", {
                    file.relative_to(skill.parent).as_posix(): file.read_bytes()
                    for file in component_files(skill)
                })
        write_zip(staging / "finance-skills-marketplace.zip", marketplace_files)
        archives = sorted(staging.glob("*.zip"))
        checksums = "".join(f"{hashlib.sha256(file.read_bytes()).hexdigest()}  {file.name}\n" for file in archives)
        (staging / "SHA256SUMS").write_text(checksums, encoding="utf-8")
        output.mkdir(parents=True, exist_ok=True)
        # dist is dedicated to this build. Remove stale release assets only.
        for old in output.glob("*.zip"):
            old.unlink()
        for file in staging.iterdir():
            (output / file.name).write_bytes(file.read_bytes())
    return len(archives)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("sync", "check", "build"))
    parser.add_argument("--version", help="Expected release version or v-prefixed tag")
    args = parser.parse_args()
    try:
        if args.command == "build":
            print(f"Built {build(version=args.version)} archives and SHA256SUMS in dist/")
        else:
            plugins = sync(check=args.command == "check", version=args.version)
            print(f"{args.command}: {len(plugins)} plugins verified")
    except (ValueError, KeyError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
