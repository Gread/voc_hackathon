# One-command run on Windows: install, build the index if stale, serve.
$ErrorActionPreference = "Stop"
python -m pip install -q -e .
python -m voc serve
