"""Print a theme's screening outcome: kept records per slice and the rule-included titles.

Usage: python3 scripts/theme_report.py THEME [--titles]
Reads data/processed/candidates.csv and records.json (run build_records.py first).
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
t = sys.argv[1]
cands = [c for c in csv.DictReader((ROOT / "data/processed/candidates.csv").open()) if c["theme"] == t]
recs = json.loads((ROOT / "data/processed/records.json").read_text())
by_slice = defaultdict(set)
for c in cands:
    if c["final"] == "include":
        by_slice[c["slice"]].add(c["openalex_id"])
print(t, "kept per slice:", {k: len(v) for k, v in sorted(by_slice.items())})
prim = [r for r in recs if r["Primary theme"] == t]
print("records with primary theme", t, len(prim), "| found by", t, "but primary elsewhere:",
      sum(1 for r in recs if f"{t}:" in r["Found in"] and r["Primary theme"] != t))
if "--titles" in sys.argv:
    for r in prim:
        print(f"  {r['OpenAlex ID']} {r['Year']} [{r['Screening confidence'][0]}] {r['Title'][:110]}")
