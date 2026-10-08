"""Resolve a seeded random sample of record DOIs through Crossref (and DataCite) and report
the match rate.

Usage: python3 scripts/verify_crossref.py N SEED LABEL
Each DOI is looked up in Crossref (api.crossref.org); a DOI Crossref does not know (HTTP 404,
e.g. Zenodo, figshare or other DataCite DOIs) is looked up in DataCite (api.datacite.org).
A DOI 'matches' when the registry returns the work and its title agrees with the OpenAlex title
(normalised similarity >= 0.85, or one contains the other) and the year is within ±1.
Results: data/screening/crossref_check_{LABEL}.csv. Raw responses are cached in
data/raw/crossref/ and data/raw/datacite/ by the shared throttled fetcher.
"""
import csv
import difflib
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_records import norm_title  # noqa: E402
from fetcher import Fetcher  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
n, seed, label = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
recs = [r for r in json.loads((ROOT / "data/processed/records.json").read_text()) if r["DOI"]]
recs.sort(key=lambda r: r["OpenAlex ID"])
sample = random.Random(seed).sample(recs, min(n, len(recs)))
f = Fetcher(min_interval=1.1)
rows, ok = [], 0
agency = {"Crossref": 0, "DataCite": 0, "neither": 0}
for r in sample:
    cr = f.crossref_work(r["DOI"])
    reg = "Crossref"
    if cr is not None:
        m = cr["message"]
        ct = (m.get("title") or [""])[0]
        cy = None
        for k in ("published-print", "published-online", "issued", "created"):
            if m.get(k, {}).get("date-parts", [[None]])[0][0]:
                cy = m[k]["date-parts"][0][0]
                break
    else:
        dc = f.datacite_work(r["DOI"])
        if dc is None:
            agency["neither"] += 1
            rows.append([r["ID"], r["DOI"], "neither", r["Title"], "", "", "not found in Crossref or DataCite"])
            continue
        reg = "DataCite"
        a = dc["data"]["attributes"]
        ct = ((a.get("titles") or [{}])[0]).get("title", "")
        cy = a.get("publicationYear")
        cy = int(cy) if cy else None
    agency[reg] += 1
    a_, b_ = norm_title(r["Title"]), norm_title(ct)
    sim = difflib.SequenceMatcher(None, a_, b_).ratio()
    tmatch = sim >= 0.85 or (a_ and b_ and (a_ in b_ or b_ in a_))
    ymatch = cy is None or r["Year"] is None or abs(cy - r["Year"]) <= 1
    status = "match" if tmatch and ymatch else ("title mismatch" if not tmatch else "year mismatch")
    ok += status == "match"
    rows.append([r["ID"], r["DOI"], reg, r["Title"], ct, cy, f"{status} (sim {sim:.2f})"])
out = ROOT / "data" / "screening" / f"crossref_check_{label}.csv"
with out.open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["ID", "DOI", "registry", "OpenAlex title", "registry title", "registry year",
                "result"])
    w.writerows(rows)
print(f"{ok}/{len(sample)} matched; registries {agency}; network calls {f.network_calls}")
for row in rows:
    if not row[6].startswith("match"):
        print(row)
