"""Growth counts for Stage 3 (BRIEF §5.2), prepared in Stage 2.

Usage: python3 scripts/growth_counts.py fetch      (API calls; cached, so re-runs are free)
       python3 scripts/growth_counts.py table      (writes data/processed/growth_counts.csv)

Counts (OpenAlex API, group_by publication_year, 2010-2026), all under the same filters:
  - journal articles and book chapters only: type article|book-chapter AND primary location in a
    journal, book series or ebook platform (repository-only records such as Zenodo, SSRN or
    institutional repositories, and records without a source, are excluded); not retracted;
  - theme count     : the theme's OR-combined query (title + abstract, exact), all fields of science
  - theme SA count  : the same AND south_asia_terms
  - baseline        : all Social Sciences works (primary_topic.domain = Social Sciences) per year;
                      SA baseline = the same AND south_asia_terms
  - 2026 is a partial year (data retrieved in October 2026, with indexing lag): shares
    (theme / baseline in the same year) are comparable, raw counts are not.
Precision adjustment: a random sample (sample=40, seed 20261008) of each theme's full hit set
under the same filters for 2015-2026 is screened with the theme's own rules (scripts/
build_records.py). Estimated precision p = (rule-included + k x borderline) / n, where k is the
share of borderline records kept by hand across Stage 2. When the blind precision check
(data/screening/precision_check_stage2.csv) is available, rule-included records are further
scaled by the checked precision of rule-included records in that theme's domain (A, B or C,
pooled; `q`).
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_records import abstract_text, compile_cfg, screen  # noqa: E402
from fetcher import RAW, Fetcher  # noqa: E402
from run_search import FIELD, sa_terms  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASE = ("type:article|book-chapter,primary_location.source.type:journal|book series|ebook platform,"
        "is_retracted:false")
YEARS = "2010-2026"
SEED = 20261008
SAMPLE_SEL = ("id,doi,title,display_name,publication_year,type,abstract_inverted_index,keywords,"
              "primary_location,is_retracted")


def q_of(cfg, t):
    return " OR ".join(f"({x})" for x in cfg["themes"][t]["queries"])


def by_year(resp):
    return {int(g["key"]): g["count"] for g in resp["group_by"] if str(g["key"]).isdigit()}


def fetch():
    cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
    f = Fetcher(min_interval=0.5, label="growth")
    sa = sa_terms(cfg)
    out = {"filters": BASE, "years": YEARS, "retrieved": None, "baseline": {}, "themes": {}}
    r = f.openalex_list({"filter": f"{BASE},publication_year:{YEARS},primary_topic.domain.id:2",
                         "group_by": "publication_year"}, "growth_baseline_ss")
    out["baseline"]["global"] = by_year(r)
    r = f.openalex_list({"filter": f"{BASE},publication_year:{YEARS},primary_topic.domain.id:2,"
                                   f"{FIELD}.search.exact:{sa}",
                         "group_by": "publication_year"}, "growth_baseline_ss_sa")
    out["baseline"]["south_asia"] = by_year(r)
    for t in cfg["themes"]:
        q = q_of(cfg, t)
        g = f.openalex_list({"filter": f"{BASE},publication_year:{YEARS},{FIELD}.search.exact:{q}",
                             "group_by": "publication_year"}, f"growth_{t}_global")
        s = f.openalex_list({"filter": f"{BASE},publication_year:{YEARS},"
                                       f"{FIELD}.search.exact:({q}) AND ({sa})",
                             "group_by": "publication_year"}, f"growth_{t}_sa")
        smp = f.openalex_list({"filter": f"{BASE},publication_year:2015-2026,"
                                         f"{FIELD}.search.exact:{q}",
                               "sample": 40, "seed": SEED, "per_page": 40, "select": SAMPLE_SEL},
                              f"growth_{t}_sample")
        out["themes"][t] = {"query": q, "global": by_year(g), "south_asia": by_year(s),
                            "sample_ids": [w["id"].rsplit("/", 1)[-1] for w in smp["results"]]}
        print(t, sum(out["themes"][t]["global"].values()), len(smp["results"]),
              f"credits {f.remaining}", flush=True)
    import datetime as dt
    out["retrieved"] = dt.date.today().isoformat()
    (RAW / "counts" / "growth_stage2.json").write_text(json.dumps(out, indent=1))
    print("network calls", f.network_calls, "credits remaining", f.remaining)


def sample_screen(cfg, t):
    """Screen the theme's random sample with the theme's own rules."""
    import gzip
    p = RAW / "api" / f"growth_{t}_sample.json.gz"
    resp = json.load(gzip.open(p))
    req, flags = compile_cfg(cfg, t)
    sc = cfg["themes"][t]["screen"]
    rows = []
    for w in resp["results"]:
        title = w.get("title") or w.get("display_name") or ""
        ab = abstract_text(w)
        kw = "; ".join(k["display_name"] for k in (w.get("keywords") or []))
        d, _, reason = screen(title, ab, kw, req, flags, t[0], "sample",
                              sc.get("strict_once", False), sc.get("flag_excludes", False))
        rows.append({"theme": t, "openalex_id": w["id"].rsplit("/", 1)[-1],
                     "year": w.get("publication_year"), "title": title, "decision": d,
                     "reason": reason})
    return rows


def table():
    cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
    data = json.loads((RAW / "counts" / "growth_stage2.json").read_text())
    stats = list(csv.DictReader((ROOT / "data/processed/screening_stats.csv").open()))
    kept = sum(int(s["manual_kept"]) for s in stats)
    dropped = sum(int(s["manual_dropped"]) for s in stats)
    k = kept / (kept + dropped)
    q_by_theme = {}
    pc = ROOT / "data/screening/precision_check_stage2.csv"
    if pc.exists():
        # pooled per domain (A/B/C): six records per theme are too few for a per-theme factor
        tot, ok = defaultdict(int), defaultdict(int)
        for r in csv.DictReader(pc.open()):
            if r.get("rule_decision") == "include" and r["why"] == "random6":
                tot[r["assigned_theme"][0]] += 1
                ok[r["assigned_theme"][0]] += r["theme_ok"] == "Y"
        q_dom = {d: ok[d] / tot[d] for d in tot if tot[d]}
        q_by_theme = {t: q_dom.get(t[0], 1.0) for t in cfg["themes"]}
        print("rule-included precision by domain:", {d: round(v, 2) for d, v in q_dom.items()})
    srows, out = [], []
    base_g, base_s = data["baseline"]["global"], data["baseline"]["south_asia"]
    periods = {"2015-19": range(2015, 2020), "2020-26": range(2020, 2027)}
    for t, d in data["themes"].items():
        rows = sample_screen(cfg, t)
        srows += rows
        n = len(rows)
        inc = sum(r["decision"] == "include" for r in rows)
        bor = sum(r["decision"] == "borderline" for r in rows)
        q = q_by_theme.get(t, 1.0)
        p = (inc * q + bor * k) / n if n else 0.0
        rec = {"theme": t, "name": cfg["themes"][t]["name"], "sample_n": n,
               "sample_rule_include": inc, "sample_borderline": bor,
               "q_rule_precision_used": round(q, 3), "precision_est": round(p, 3)}
        for scope, counts, base in (("global", d["global"], base_g),
                                    ("SA", d["south_asia"], base_s)):
            for pname, yrs in periods.items():
                c = sum(int(counts.get(str(y), counts.get(y, 0))) for y in yrs)
                b = sum(int(base.get(str(y), base.get(y, 0))) for y in yrs)
                rec[f"{scope}_{pname}_raw"] = c
                rec[f"{scope}_{pname}_adj"] = round(c * p)
                rec[f"{scope}_{pname}_per10k_ss"] = round(1e4 * c * p / b, 2) if b else ""
            a, bb = rec[f"{scope}_2015-19_per10k_ss"], rec[f"{scope}_2020-26_per10k_ss"]
            rec[f"{scope}_growth_ratio"] = round(bb / a, 2) if a else ""
        rec["2026_global_raw_partial"] = int(d["global"].get("2026", 0))
        out.append(rec)
    with (ROOT / "data/processed/growth_counts.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, list(out[0]))
        w.writeheader()
        w.writerows(out)
    with (ROOT / "data/screening/growth_precision_sample.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, list(srows[0]))
        w.writeheader()
        w.writerows(srows)
    print(f"k (hand keep-rate of borderline) = {k:.2f}; themes {len(out)}")
    for r in sorted(out, key=lambda r: -(r["global_growth_ratio"] or 0))[:12]:
        print(f"  {r['theme']:4s} p={r['precision_est']:.2f} growth {r['global_growth_ratio']} "
              f"SA growth {r['SA_growth_ratio']}")


if __name__ == "__main__":
    {"fetch": fetch, "table": table}[sys.argv[1]]()
