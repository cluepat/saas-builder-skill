#!/usr/bin/env python3
"""Validate installable paths, skill metadata and local reference links."""
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/saas-builder"
text = (SKILL / "SKILL.md").read_text()
match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
assert match, "SKILL.md requires YAML frontmatter"
metadata = yaml.safe_load(match.group(1))
assert metadata["name"] == "saas-builder"
assert isinstance(metadata["description"], str) and len(metadata["description"]) <= 1024
assert "[TODO" not in text and "TODO:" not in text
ui = yaml.safe_load((SKILL / "agents/openai.yaml").read_text())
assert "$saas-builder" in ui["interface"]["default_prompt"]
manifest = json.loads((ROOT / "plugin.json").read_text())
assert manifest == json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
assert manifest["version"] == metadata["metadata"]["version"]
assert (ROOT / manifest["skills"]).resolve() == SKILL.parent.resolve()
market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
assert market["name"] == "cluepat" and market["plugins"][0]["name"] == manifest["name"]
assert (ROOT / market["plugins"][0]["source"]["path"]).resolve() == ROOT
assert (ROOT / "LICENSE").read_text() == (SKILL / "LICENSE").read_text()
for path in [ROOT / "README.md", *SKILL.rglob("*.md")]:
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
        if "://" in target or target.startswith("#"):
            continue
        destination = (path.parent / target.split("#")[0]).resolve()
        assert destination.is_relative_to(ROOT), f"Reference outside package: {path.name}"
        assert destination.exists(), f"Missing reference: {path.name} -> {target}"
print("Skill metadata, plugin manifests, license and local references are valid.")
