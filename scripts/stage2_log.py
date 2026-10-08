"""Rewrite the generated Stage 2 tables in PROGRESS.md (between the AUTO markers).

Usage: python3 scripts/stage2_log.py
Tables: per-theme screening (candidates, borderline share, hand decisions, records) from
data/processed/screening_stats.csv + records.json, and OpenAlex API usage per UTC day from
data/raw/api_ledger.csv.
"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
stats = {r["theme"]: r for r in csv.DictReader((ROOT / "data/processed/screening_stats.csv").open())}
recs = json.loads((ROOT / "data/processed/records.json").read_text())
prim = Counter(r["Primary theme"] for r in recs)
found = Counter(t for r in recs for t in {x.split(":")[0] for x in r["Found in"].split("; ")})
lines = ["| Theme | Name | Candidates | Rule incl. | Borderline (share) | Hand kept / dropped | "
         "Records found | Primary here |", "|---|---|---|---|---|---|---|---|"]
allt = list(cfg["themes"]) + list(cfg.get("supplementary") or {})
for t in allt:
    if t not in stats:
        continue
    s = stats[t]
    name = (cfg["themes"].get(t) or cfg["supplementary"][t])["name"]
    share = float(s["borderline_share"])
    lines.append(f"| {t} | {name[:45]} | {s['candidates']} | {s['include_rules']} | "
                 f"{s['borderline']} ({share:.0%}){' ⚠' if share >= 0.25 else ''} | "
                 f"{s['manual_kept']} / {s['manual_dropped']}"
                 f"{' (+' + s['pending'] + ' pending)' if s['pending'] != '0' else ''} | "
                 f"{found.get(t, 0)} | {prim.get(t, 0)} |")
lines.append(f"\nTotal deduplicated records: {len(recs)}.")

usage = defaultdict(lambda: [0, 0.0, None])
led = ROOT / "data/raw/api_ledger.csv"
if led.exists():
    for r in csv.DictReader(led.open()):
        u = usage[r["utc"][:10]]
        u[0] += 1
        u[1] += float(r["cost_usd"] or 0)
        u[2] = r["credits_remaining"]
api = ["| UTC day | Calls by this pipeline | Cost (USD) | ≈ searches | Credits left at last call |",
       "|---|---|---|---|---|"]
for d, (n, c, rem) in sorted(usage.items()):
    api.append(f"| {d} | {n} | {c:.3f} | {c / 0.001:.0f} | {rem} |")

p = ROOT / "PROGRESS.md"
txt = p.read_text()
for tag, body in (("SCREENING", "\n".join(lines)), ("API", "\n".join(api))):
    txt = re.sub(rf"(<!-- AUTO:{tag} -->\n).*?(<!-- /AUTO:{tag} -->)",
                 lambda m: m.group(1) + body + "\n" + m.group(2), txt, flags=re.S)
p.write_text(txt)
print("PROGRESS.md tables updated")
