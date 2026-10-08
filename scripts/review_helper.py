"""Show borderline records awaiting a hand decision, and record the decisions.

Usage:
  python3 scripts/review_helper.py show THEME        compact view of pending records
  python3 scripts/review_helper.py add THEME < decisions.txt
      one line per record: "W123 i note" (include) or "W123 e note" (exclude)
Decisions are appended to data/screening/manual_review.csv (reviewer = Claude, Stage 2).
"""
import csv
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_records import abstract_text, sentences, theme_cfg  # noqa: E402
from fetcher import load_work  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MR = ROOT / "data" / "screening" / "manual_review.csv"
cmd, theme = sys.argv[1], sys.argv[2]
pend = [r for r in csv.DictReader((ROOT / "data/processed/pending_review.csv").open())
        if r["theme"] == theme]
if cmd == "show":
    cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
    core = re.compile(theme_cfg(cfg, theme)["screen"]["require"][0], re.I)
    print(theme, theme_cfg(cfg, theme)["name"], "| pending", len(pend))
    for r in pend:
        w = load_work(r["openalex_id"])
        ab = abstract_text(w)
        ss = sentences(ab)
        hit = [s for s in ss if core.search(s)][:2]
        show = ([ss[0]] if ss and ss[0] not in hit else []) + hit
        venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        print(f"\n{r['openalex_id']} {r['year']} {r['type']} | {venue[:40]} | {r['reason'][:45]}")
        print(f"  T: {r['title'][:180]}")
        for s in show:
            print(f"  > {s[:260]}")
elif cmd == "add":
    ids = {r["openalex_id"] for r in pend}
    rows = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        wid, d, *note = line.split(" ", 2)
        assert wid in ids, f"{wid} not pending for {theme}"
        rows.append([wid, theme, {"i": "include", "e": "exclude"}[d],
                     "Claude (manual review, Stage 2)", note[0] if note else ""])
    with MR.open("a", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f"added {len(rows)} decisions; still pending {len(ids) - len(rows)}")
