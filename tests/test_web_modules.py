"""Static checks on the front end. There is no build step and no JS test runner, so these guard the
two mistakes that actually broke the page: a module using a helper it never imported, and the
percentage helper being handed a value that is already a percentage."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

WEB = Path(__file__).resolve().parent.parent / "voc" / "web"
MODULES = sorted(WEB.glob("js/*.js")) + [WEB / "app.js"]
FORMAT = WEB / "js" / "format.js"


def exported_names() -> set[str]:
    return set(re.findall(r"export (?:function|const) (\w+)", FORMAT.read_text(encoding="utf-8")))


@pytest.mark.parametrize("module", MODULES, ids=lambda p: p.name)
def test_module_imports_every_formatter_it_uses(module: Path):
    if module.name == "format.js":
        return
    src = module.read_text(encoding="utf-8")
    match = re.search(r'import \{([^}]*)\} from "\.{1,2}/(?:js/)?format\.js"', src)
    imported = {name.strip() for name in match.group(1).split(",")} if match else set()
    used = {name for name in exported_names() if re.search(rf"(?<![\w.]){name}\(", src)}
    assert not (used - imported), f"{module.name} uses {sorted(used - imported)} without importing it"


def test_percentage_helpers_are_used_with_the_right_kind_of_value():
    """`pct` takes a fraction, `pctOf` takes a percentage: 0.4 meaning "0.4 per cent" is otherwise
    indistinguishable from 0.4 meaning "40 per cent"."""
    for module in MODULES:
        if module.name == "format.js":      # where the helpers are defined, not called
            continue
        src = module.read_text(encoding="utf-8")
        for call in re.findall(r"(?<![\w.])pct\(([^),]*)", src):
            assert "_pct" not in call, f"{module.name}: pct({call.strip()}) is already a percentage, use pctOf"
        for call in re.findall(r"(?<![\w.])pctOf\(([^),]*)", src):
            arg = call.strip()
            assert arg.endswith("_pct") or "pct" in arg.lower(), \
                f"{module.name}: pctOf({arg}) should take a value that is already a percentage"


@pytest.mark.parametrize("module", MODULES, ids=lambda p: p.name)
def test_module_parses(module: Path):
    node = subprocess.run(["node", "--check", str(module)], capture_output=True, text=True)
    if node.returncode == 127 or "not found" in (node.stderr or ""):
        pytest.skip("node is not available")
    assert node.returncode == 0, node.stderr
