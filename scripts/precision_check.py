"""Blind precision check (Stage 2): 6 random records per theme, judged by a separate agent that
does not see the screening decisions or the assigned themes.

Usage:
  python3 scripts/precision_check.py sample OUTDIR     writes OUTDIR/blind_{1..3}.jsonl (judge input)
                                                       and data/screening/precision_key_stage2.csv
  python3 scripts/precision_check.py score JUDGED...   merges judge outputs (JSONL) with the key into
                                                       data/screening/precision_check_stage2.csv

Sample: for each of the 48 themes, 6 records whose primary theme is that theme (supplementary-
only records excluded), drawn with random.Random(20261008) from records sorted by OpenAlex ID;
plus the A9 records of the Stage 1 precision sample (re-check of A9 after themes compete for
primary assignment). The judge sees only: an opaque item number, title, year, venue, document
type and abstract, together with the list of 48 themes and the region categories of BRIEF.md.
It returns: in_scope (Y/N), best_theme, other_fitting_themes, region, note.
A record counts as correct for its theme when it is in scope and the assigned primary theme is
the judge's best theme or one of the other fitting themes. Region is correct when the judge's
region equals the record's region tag.
"""
import csv
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_records import abstract_text  # noqa: E402
from fetcher import load_work  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261008
KEY = ROOT / "data/screening/precision_key_stage2.csv"
OUT = ROOT / "data/screening/precision_check_stage2.csv"


def sample(outdir):
    cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
    recs = json.loads((ROOT / "data/processed/records.json").read_text())
    recs = [r for r in recs if r["Supplementary"] != "Y"]
    recs.sort(key=lambda r: r["OpenAlex ID"])
    rng = random.Random(SEED)
    by_t = defaultdict(list)
    for r in recs:
        by_t[r["Primary theme"]].append(r)
    picked = []
    for t in cfg["themes"]:
        for r in rng.sample(by_t[t], min(6, len(by_t[t]))):
            picked.append((r, "random6"))
    # Stage 1 A9 sample records, wherever they are now
    s1 = [x for x in csv.DictReader((ROOT / "data/screening/precision_sample_stage1.csv").open())
          if x["Primary theme"] == "A9"]
    by_id = {}
    for r in recs:
        by_id[r["OpenAlex ID"]] = r
        for d in (r["Duplicates merged"] or "").split("; "):
            if d:
                by_id[d] = r
    have = {r["OpenAlex ID"] for r, _ in picked}
    s1_missing = []
    for x in s1:
        r = by_id.get(x["OpenAlex ID"])
        if r is None:
            s1_missing.append(x["OpenAlex ID"])
        elif r["OpenAlex ID"] not in have:
            picked.append((r, "stage1_A9"))
            have.add(r["OpenAlex ID"])
    order = list(range(len(picked)))
    random.Random(SEED + 1).shuffle(order)
    rows, items = [], []
    for n, i in enumerate(order, 1):
        r, why = picked[i]
        w = load_work(r["OpenAlex ID"])
        ab = abstract_text(w)
        items.append({"item": n, "title": r["Title"], "year": r["Year"], "venue": r["Venue"],
                      "type": r["Document type"], "abstract": ab[:1500] or "(no abstract)"})
        rows.append({"item": n, "ID": r["ID"], "openalex_id": r["OpenAlex ID"], "why": why,
                     "assigned_theme": r["Primary theme"], "secondary_theme": r["Secondary theme"],
                     "region": r["Region"], "confidence": r["Screening confidence"],
                     "found_in": r["Found in"]})
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    k = 3
    for j in range(k):
        part = items[j::k]
        with (outdir / f"blind_{j + 1}.jsonl").open("w") as fh:
            for it in part:
                fh.write(json.dumps(it, ensure_ascii=False) + "\n")
    with KEY.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    themes_txt = "\n".join(f"{t} {v['name']}" for t, v in cfg["themes"].items())
    (outdir / "themes.txt").write_text(themes_txt + "\n")
    print(f"{len(items)} items ({sum(w == 'random6' for _, w in picked)} random, "
          f"{sum(w == 'stage1_A9' for _, w in picked)} Stage 1 A9); Stage 1 A9 records no longer "
          f"in the map: {len(s1_missing)}")


def rule_decision(found_in, theme, wid):
    """'include' when the record's primary-theme candidate passed the rules (not by hand)."""
    cands = [c for c in csv.DictReader((ROOT / "data/processed/candidates.csv").open())
             if c["openalex_id"] == wid and c["theme"] == theme]
    if any(c["decision"] == "include" and "manual override" not in c["reason"] for c in cands):
        return "include"
    return "hand"


def score(files):
    key = {r["item"]: r for r in csv.DictReader(KEY.open())}
    judged = {}
    for fp in files:
        for line in Path(fp).read_text().splitlines():
            if line.strip():
                j = json.loads(line)
                judged[str(j["item"])] = j
    rows = []
    cands = list(csv.DictReader((ROOT / "data/processed/candidates.csv").open()))
    ci = defaultdict(list)
    for c in cands:
        ci[(c["openalex_id"], c["theme"])].append(c)
    for item, k in key.items():
        j = judged.get(item)
        if not j:
            continue
        fit = {j.get("best_theme", "")} | set(j.get("other_fitting_themes") or [])
        in_scope = j.get("in_scope") == "Y"
        cs = ci[(k["openalex_id"], k["assigned_theme"])]
        rd = "include" if any(c["decision"] == "include" and "override" not in c["reason"]
                              for c in cs) else "hand"
        rows.append({**k, "rule_decision": rd, "judge_in_scope": j.get("in_scope"),
                     "judge_best": j.get("best_theme"),
                     "judge_other": " ".join(j.get("other_fitting_themes") or []),
                     "judge_region": j.get("region"), "judge_note": j.get("note", ""),
                     "in_scope": "Y" if in_scope else "N",
                     "theme_ok": "Y" if in_scope and k["assigned_theme"] in fit else "N",
                     "region_ok": "Y" if j.get("region") == k["region"] else "N"})
    with OUT.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    rnd = [r for r in rows if r["why"] == "random6"]
    print(f"judged {len(rows)} of {len(key)}; random sample {len(rnd)}")
    print(f"in scope {sum(r['in_scope'] == 'Y' for r in rnd)}/{len(rnd)}; theme correct "
          f"{sum(r['theme_ok'] == 'Y' for r in rnd)}/{len(rnd)}; region correct "
          f"{sum(r['region_ok'] == 'Y' for r in rnd)}/{len(rnd)}")
    by = defaultdict(list)
    for r in rnd:
        by[r["assigned_theme"]].append(r)
    low = [(t, sum(x["theme_ok"] == "Y" for x in v), len(v)) for t, v in by.items()]
    print("themes with < 5/6 correct:", [f"{t} {a}/{b}" for t, a, b in sorted(low) if a < 5])
    a9 = [r for r in rows if r["assigned_theme"] == "A9"]
    print(f"A9 (random + Stage 1 sample still in A9): {sum(r['theme_ok'] == 'Y' for r in a9)}/"
          f"{len(a9)}")


if __name__ == "__main__":
    if sys.argv[1] == "sample":
        sample(sys.argv[2])
    else:
        score(sys.argv[2:])
