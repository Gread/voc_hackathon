"""Print the data profile table from data/profile.json (no network, no recompute)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from voc.ingest.profile import format_table  # noqa: E402
from voc.paths import get_paths  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=None, help="profile.json (default: data/profile.json)")
    args = ap.parse_args(argv)
    path = args.path or get_paths().profile
    if not path.exists():
        print(f"missing {path}; run `python -m voc ingest profile` first", file=sys.stderr)
        return 1
    print(format_table(json.loads(path.read_text(encoding="utf-8"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
