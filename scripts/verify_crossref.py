"""Resolve a seeded random sample of record DOIs through Crossref and report the match rate.

Usage: python3 scripts/verify_crossref.py N SEED LABEL
A DOI 'matches' when Crossref returns the work (HTTP 200) and its title agrees with the
OpenAlex title (normalised similarity >= 0.85, or one contains the other) and the year is
within ±1. Results: data/screening/crossref_check_{LABEL}.csv. Raw responses are cached in
data/raw/crossref/ by the shared throttled fetcher (Crossref allows ~1 request/s here).
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
for r in sample:
    cr = f.crossref_work(r["DOI"])
    if cr is None:
        rows.append([r["ID"], r["DOI"], r["Title"], "", "", "not found in Crossref"])
        continue
    m = cr["message"]
    ct = (m.get("title") or [""])[0]
    cy = None
    for k in ("published-print", "published-online", "issued", "created"):
        if m.get(k, {}).get("date-parts", [[None]])[0][0]:
            cy = m[k]["date-parts"][0][0]
            break
    a, b = norm_title(r["Title"]), norm_title(ct)
    sim = difflib.SequenceMatcher(None, a, b).ratio()
    tmatch = sim >= 0.85 or (a and b and (a in b or b in a))
    ymatch = cy is None or r["Year"] is None or abs(cy - r["Year"]) <= 1
    status = "match" if tmatch and ymatch else ("title mismatch" if not tmatch else "year mismatch")
    ok += status == "match"
    rows.append([r["ID"], r["DOI"], r["Title"], ct, cy, f"{status} (sim {sim:.2f})"])
out = ROOT / "data" / "screening" / f"crossref_check_{label}.csv"
with out.open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["ID", "DOI", "OpenAlex title", "Crossref title", "Crossref year", "result"])
    w.writerows(rows)
print(f"{ok}/{len(sample)} matched; network calls {f.network_calls}")
for row in rows:
    if not row[5].startswith("match"):
        print(row)
