import json, sys

bundle_num = sys.argv[1]
records_file = sys.argv[2]

b = json.load(open(f"data/work/extract_bundles/bundle_{bundle_num}.json", encoding="utf-8"))
texts = {r["call_id"]: r["text"] for r in b["records"]}
cache_keys = {r["call_id"]: r["cache_key"] for r in b["records"]}
shapes = {r["call_id"]: r["shape"] for r in b["records"]}

recs = json.load(open(records_file, encoding="utf-8"))

errors = []
for call_id, resp in recs.items():
    if call_id not in texts:
        errors.append(f"{call_id}: not in bundle {bundle_num}")
        continue
    text = texts[call_id]

    cr = resp["contact_reasons"]
    if not (1 <= len(cr) <= 3):
        errors.append(f"{call_id}: contact_reasons count {len(cr)}")
    primaries = [r for r in cr if r["is_primary"]]
    if len(primaries) != 1:
        errors.append(f"{call_id}: {len(primaries)} primary contact reasons")

    prods = resp["products"]
    if not (1 <= len(prods) <= 3):
        errors.append(f"{call_id}: products count {len(prods)}")

    svcs = resp["services"]
    if not (0 <= len(svcs) <= 3):
        errors.append(f"{call_id}: services count {len(svcs)}")

    topics = resp["topics"]
    if not (1 <= len(topics) <= 5):
        errors.append(f"{call_id}: topics count {len(topics)}")

    for t in topics:
        if not isinstance(t["sentiment"], int) or not (-2 <= t["sentiment"] <= 2):
            errors.append(f"{call_id}: bad topic sentiment {t['sentiment']}")
        ev = t["evidence"]
        if not (1 <= len(ev) <= 3):
            errors.append(f"{call_id}: topic '{t['topic_label']}' evidence count {len(ev)}")
        for e in ev:
            q = e["quote"]
            if q not in text:
                errors.append(f"{call_id}: NOT SUBSTRING: {q!r}")
            if not (8 <= len(q) <= 300):
                errors.append(f"{call_id}: quote length {len(q)}: {q!r}")
            expected_speaker = "narrative" if shapes[call_id] == "narrative" else e["speaker"]
            if shapes[call_id] == "narrative" and e["speaker"] != "narrative":
                errors.append(f"{call_id}: speaker should be narrative, got {e['speaker']}")
        if len(t["topic_label"]) < 2 or len(t["topic_label"].split()) > 6:
            pass
        if len(t["issue_statement"]) > 220:
            errors.append(f"{call_id}: issue_statement too long ({len(t['issue_statement'])})")
        if len(t["driver"]) > 200:
            errors.append(f"{call_id}: driver too long ({len(t['driver'])})")

    pm = resp["positive_moments"]
    if not (0 <= len(pm) <= 3):
        errors.append(f"{call_id}: positive_moments count {len(pm)}")
    for p in pm:
        q = p["quote"]
        if q not in text:
            errors.append(f"{call_id}: POSMOMENT NOT SUBSTRING: {q!r}")
        if not (8 <= len(q) <= 300):
            errors.append(f"{call_id}: posmoment quote length {len(q)}")

    os_ = resp["overall_sentiment"]
    if not isinstance(os_, int) or not (-2 <= os_ <= 2):
        errors.append(f"{call_id}: bad overall_sentiment {os_}")

    if len(resp["stated_reason"]) < 1:
        errors.append(f"{call_id}: empty stated_reason")

if errors:
    print(f"BUNDLE {bundle_num}: {len(errors)} ERRORS")
    for e in errors:
        print(" -", e)
else:
    print(f"BUNDLE {bundle_num}: all {len(recs)} records OK (structure + quote substrings)")
