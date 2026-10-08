"""Draw a seeded random sample of records for hand-checking precision and tagging.

Usage: python3 scripts/sample_precision.py STAGE N SEED
Writes data/screening/precision_sample_{STAGE}.csv with empty judgement columns
(relevant, theme_ok, region_ok, note) unless the file already exists with judgements.
"""
import csv
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
stage, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
recs = json.loads((ROOT / "data" / "processed" / "records.json").read_text())
recs.sort(key=lambda r: r["OpenAlex ID"])
sample = random.Random(seed).sample(recs, n)
out = ROOT / "data" / "screening" / f"precision_sample_{stage}.csv"
if out.exists():
    sys.exit(f"{out.name} exists; not overwriting")
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["OpenAlex ID", "Title", "Primary theme", "Region", "Places studied",
                "Screening confidence", "relevant", "theme_ok", "region_ok", "note"])
    for r in sample:
        w.writerow([r["OpenAlex ID"], r["Title"], r["Primary theme"], r["Region"],
                    r["Places studied"], r["Screening confidence"], "", "", "", ""])
print(out, len(sample))
