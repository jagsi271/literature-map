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

# ---- blind precision check (6 random records per theme)
prec = []
pc = ROOT / "data/screening/precision_check_stage2.csv"
if pc.exists():
    rows = [r for r in csv.DictReader(pc.open()) if r["why"] == "random6"]
    by = defaultdict(list)
    for r in rows:
        by[r["assigned_theme"]].append(r)
    prec = ["| Theme | In scope | Correct theme | Region correct | Theme | In scope | Correct theme | Region correct |",
            "|---|---|---|---|---|---|---|---|"]
    cells = []
    for t in list(cfg["themes"]):
        v = by.get(t, [])
        ok = sum(x["theme_ok"] == "Y" for x in v)
        cells.append(f"{t} | {sum(x['in_scope'] == 'Y' for x in v)}/{len(v)} | "
                     f"{ok}/{len(v)}{' ⚠' if v and ok / len(v) < 0.8 else ''} | "
                     f"{sum(x['region_ok'] == 'Y' for x in v)}/{len(v)}")
    for i in range(0, len(cells), 2):
        prec.append("| " + " | ".join(cells[i:i + 2]) + " |")
    prec.append(f"\nAll: in scope {sum(r['in_scope'] == 'Y' for r in rows)}/{len(rows)}, correct "
                f"theme {sum(r['theme_ok'] == 'Y' for r in rows)}/{len(rows)}, region "
                f"{sum(r['region_ok'] == 'Y' for r in rows)}/{len(rows)} (sample drawn before the "
                f"primary-topic-field rule; see log).")

# ---- recall against seeds.csv
rec_t = []
rp = ROOT / "data/screening/recall_seeds_stage2.csv"
if rp.exists():
    rr = list(csv.DictReader(rp.open()))
    sts = ["found", "below cut-off", "query gap", "screened out", "not in OpenAlex",
           "expansion corpus only"]
    rec_t = ["| Seed category (seeds.csv) | Map themes | Seeds | " + " | ".join(sts) + " |",
             "|---|---|---|" + "---|" * len(sts)]
    byc = defaultdict(Counter)
    exp = {}
    for r in rr:
        byc[r["category"]][r["status"]] += 1
        exp[r["category"]] = r["expected_themes"]
    for c_, v in sorted(byc.items(), key=lambda x: -sum(x[1].values())):
        rec_t.append(f"| {c_} | {exp[c_]} | {sum(v.values())} | " + " | ".join(str(v.get(x, 0)) for x in sts) + " |")
    tot = Counter(r["status"] for r in rr)
    rec_t.append(f"| **All** | | {len(rr)} | " + " | ".join(str(tot.get(x, 0)) for x in sts) + " |")
    fp = Counter(r["primary_theme"] for r in rr if r["status"] == "found")
    rec_t.append("\nFound seeds by the map's primary theme: " +
                 ", ".join(f"{k} {v}" for k, v in sorted(fp.items(), key=lambda x: (x[0][0], int(x[0][1:])))) + ".")

p = ROOT / "PROGRESS.md"
txt = p.read_text()
for tag, body in (("SCREENING", "\n".join(lines)), ("API", "\n".join(api)),
                  ("PRECISION", "\n".join(prec)), ("RECALL", "\n".join(rec_t))):
    txt = re.sub(rf"(<!-- AUTO:{tag} -->\n).*?(<!-- /AUTO:{tag} -->)",
                 lambda m: m.group(1) + body + "\n" + m.group(2), txt, flags=re.S)
p.write_text(txt)
print("PROGRESS.md tables updated")
