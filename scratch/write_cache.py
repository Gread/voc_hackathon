import json, pathlib, sys

bundle_num = sys.argv[1]
records_file = sys.argv[2]

b = json.load(open(f"data/work/extract_bundles/bundle_{bundle_num}.json", encoding="utf-8"))
cache_keys = {r["call_id"]: r["cache_key"] for r in b["records"]}

recs = json.load(open(records_file, encoding="utf-8"))

out = pathlib.Path("data/cache/extract")
out.mkdir(parents=True, exist_ok=True)

written = 0
for call_id, response in recs.items():
    key = cache_keys[call_id]
    payload = {
        "key": key,
        "prompt_version": "ext-1.0",
        "schema_version": "1",
        "taxonomy_version": "1",
        "call_id": call_id,
        "model": "claude-agent-build",
        "produced_by": "claude_agent",
        "created_at": "2026-09-11T12:00:00Z",
        "usage": None,
        "response": response,
    }
    (out / f"{call_id}.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    written += 1

print(f"bundle {bundle_num}: wrote {written} cache files")
