#!/usr/bin/env bash
# One-command run: install, build the index if stale, serve.
set -euo pipefail
python -m pip install -q -e .
python -m voc serve
