"""Population counts for the shortlist leads (supplementary query sets S1-S7), for REPORT §9.

Usage: python3 scripts/shortlist_counts.py fetch     API calls (cached; pauses at the reserve)
       python3 scripts/shortlist_counts.py table     -> data/processed/shortlist_counts.csv

Same filters as the theme population counts (scripts/population_counts.py): journal articles and
book chapters in journals / book series / ebook platforms, not retracted, 2010-2026, the set's
combined query on title + abstract (exact). Scopes: worldwide, India-named and Haryana-named
(scripts/region_terms.py); S7 names Haryana cities itself, so only its worldwide count is taken.
Each count is split into all venues and core venues (group_by primary_location.source.is_core).
Precision: a random 40-work sample of the set's India hit set (S7: of its whole hit set),
screened with the set's own rules (queries.yaml), p = (rule-included x q + borderline x k) / n,
with q the blind-check precision of the home theme's domain and k the hand keep-rate, as in the
Growth tab. One p per set is applied to every scope.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_records import abstract_text, compile_cfg, screen, theme_cfg  # noqa: E402
from fetcher import BudgetPaused, Fetcher  # noqa: E402
from growth_counts import BASE, SAMPLE_SEL, SEED  # noqa: E402
from population_counts import _load, _search, _split  # noqa: E402
from region_terms import HARYANA, INDIA, or_query  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
YEARS = "2010-2026"
GB = {"group_by": "primary_location.source.is_core"}


def q_of(cfg, s):
    return " OR ".join(f"({x})" for x in cfg["supplementary"][s]["queries"])


def plan(cfg):
    calls = []
    base = f"{BASE},publication_year:{YEARS}"
    for s in cfg["supplementary"]:
        q = q_of(cfg, s)
        calls.append((f"sl_{s}_global", {**GB, "filter": f"{base},{_search(q)}"}))
        if s != "S7":
            calls.append((f"sl_{s}_india", {**GB, "filter": f"{base},{_search(q, or_query(INDIA))}"}))
            calls.append((f"sl_{s}_haryana", {**GB, "filter": f"{base},{_search(q, or_query(HARYANA))}"}))
        place = None if s == "S7" else or_query(INDIA)
        calls.append((f"sl_{s}_sample", {"filter": f"{BASE},publication_year:2010-2026,{_search(q, place)}",
                                         "sample": 40, "seed": SEED, "per_page": 40,
                                         "select": SAMPLE_SEL}))
    return calls


def fetch():
    cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
    f = Fetcher(min_interval=0.4, label="shortlist")
    done = 0
    try:
        for name, params in plan(cfg):
            f.openalex_list(params, name)
            done += 1
    except BudgetPaused as e:
        print(f"PAUSED after {done}: {e}")
    print(f"done {done}; network {f.network_calls}; credits {f.remaining}")


def table():
    cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
    stats = list(csv.DictReader((ROOT / "data/processed/screening_stats.csv").open()))
    kept = sum(int(s["manual_kept"]) for s in stats)
    dropped = sum(int(s["manual_dropped"]) for s in stats)
    k = kept / (kept + dropped)
    tot, ok = {}, {}
    for r in csv.DictReader((ROOT / "data/screening/precision_check_stage2.csv").open()):
        if r["why"] == "random6" and r["rule_decision"] == "include":
            d = r["assigned_theme"][0]
            tot[d] = tot.get(d, 0) + 1
            ok[d] = ok.get(d, 0) + (r["theme_ok"] == "Y")
    qdom = {d: ok[d] / tot[d] for d in tot}
    rows = []
    for s, sc in cfg["supplementary"].items():
        row = {"set": s, "name": sc["name"], "home_theme": sc["home_theme"]}
        smp = _load(f"sl_{s}_sample")
        if smp and smp.get("results"):
            req, flags = compile_cfg(cfg, s)
            scr = theme_cfg(cfg, s)["screen"]
            inc = bor = 0
            for w in smp["results"]:
                title = w.get("title") or w.get("display_name") or ""
                kw = "; ".join(x["display_name"] for x in (w.get("keywords") or []))
                d, _, _ = screen(title, abstract_text(w), kw, req, flags, sc["home_theme"][0],
                                 "sample", scr.get("strict_once", False),
                                 scr.get("flag_excludes", False))
                inc += d == "include"
                bor += d == "borderline"
            n = len(smp["results"])
            p = (inc * qdom.get(sc["home_theme"][0], 1.0) + bor * k) / n
            row.update(p=round(p, 3), sample_n=n)
        else:
            p = None
            row.update(p="", sample_n=0)
        for scope in ("global", "india", "haryana"):
            name = f"sl_{s}_{scope}" if not (s == "S7" and scope != "global") else None
            al, co = _split(_load(name)) if name else (None, None)
            if s == "S7" and scope == "haryana":
                al, co = _split(_load(f"sl_{s}_global"))
            for v, x in (("all", al), ("core", co)):
                row[f"{scope}_{v}_raw"] = "" if x is None else x
                row[f"{scope}_{v}_adj"] = "" if x is None or p is None else round(x * p)
        rows.append(row)
    out = ROOT / "data/processed/shortlist_counts.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    {"fetch": fetch, "table": table}[sys.argv[1]]()
