"""Fetch the full OpenAlex record for every work ID in the search manifests.

Usage: python3 scripts/fetch_works.py [THEME ...]
Requests run one at a time through scripts/fetcher.py (>=1 s apart, backoff on 429/5xx);
raw JSON is cached in data/raw/works/, so re-runs only fetch what is missing. Each fetched
record's publication year is compared with the year recorded in the manifest; mismatches
(which would indicate a transcription error in an ID) are written to
data/raw/searches/_id_check.json and those IDs are excluded downstream.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetcher import Fetcher, RAW  # noqa: E402

themes = set(sys.argv[1:])
f = Fetcher(min_interval=1.0)
check_path = RAW / "searches" / "_id_check.json"
checks = json.loads(check_path.read_text()) if check_path.exists() else {}
for man in sorted((RAW / "searches").glob("*_*.json")):
    if man.name.startswith("_"):
        continue
    m = json.loads(man.read_text())
    if themes and m["theme"] not in themes:
        continue
    bad = 0
    for wid, year in m["results"]:
        w = f.openalex_work(wid)
        if w is None:
            status = "not_found"
        elif year == 0 and w.get("publication_year") is None:
            status = "ok"  # no year in the search response (recorded as 0) nor in the record
        elif w.get("publication_year") != year:
            status = f"year_mismatch:{w.get('publication_year')}"
        else:
            status = "ok"
        if status != "ok":
            bad += 1
        checks[wid] = status
    print(f"{man.name}: {len(m['results'])} ids, {bad} problems", flush=True)
check_path.write_text(json.dumps(checks, indent=0, sort_keys=True))
print(f"network calls {f.network_calls}, cache hits {f.cache_hits}")
