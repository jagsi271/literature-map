"""Population counts for Stage 3 gap, growth and mismatch claims (OpenAlex-wide, not the sample).

Usage: python3 scripts/population_counts.py fetch     API calls (cached; resumable; pauses at the
                                                      fetcher's credit reserve)
       python3 scripts/population_counts.py table     -> data/processed/population_counts.csv

All counts use the Growth-tab filters (scripts/growth_counts.py BASE: journal articles and book
chapters in journals / book series / ebook platforms, not retracted) and each theme's
OR-combined query on title + abstract (exact). Place scopes use place names in title/abstract,
the same notion of 'place studied' as the record tags:
  global; South Asia (queries.yaml south_asia_terms, as in Stage 2); India, Delhi/NCR, Haryana
  (scripts/region_terms.py); Global North, China & East Asia, Southeast Asia, Africa, Latin
  America, Middle East (scripts/region_terms.py, built from the gazetteer).
Each count is reported for all venues and for core venues only (primary source is_core, the
OpenAlex/CWTS core-source flag). Per-year counts: global, South Asia, India (all + core);
2010-2026 totals: Delhi/NCR, Haryana and the six other regions (group_by is_core).
Baseline: all Social Sciences works (primary_topic.domain = 2) under the same filters and scopes.
Precision adjustment as in the Growth tab: count x p, where p is the theme's estimated precision
from a random sample of its global hit set (data/processed/growth_counts.csv). For South Asia,
India, Delhi/NCR and Haryana counts, p_sa from a random sample of the theme's South Asia hit set
is used when available (fetched with the population counts), else p.
Normalised counts are per 10,000 Social Sciences works with the same filters and scope.
"""
from __future__ import annotations

import csv
import gzip
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gazetteer as gz  # noqa: E402
from build_records import abstract_text, compile_cfg, screen  # noqa: E402
from fetcher import RAW, BudgetPaused, Fetcher  # noqa: E402
from growth_counts import BASE, SAMPLE_SEL, SEED, q_of  # noqa: E402
from region_terms import DELHI, HARYANA, INDIA, or_query, terms_for  # noqa: E402
from run_search import FIELD, sa_terms  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
YEARS = "2010-2026"
CORE = "primary_location.source.is_core:true"
SS = "primary_topic.domain.id:2"
REGIONS = {"GN": gz.GN, "EA": gz.EA, "SEA": gz.SEA, "AF": gz.AF, "LA": gz.LA, "ME": gz.ME}
PERIODS = {"2010-14": range(2010, 2015), "2015-19": range(2015, 2020), "2020-26": range(2020, 2027)}


def scopes(cfg):
    s = {"sa": sa_terms(cfg), "india": or_query(INDIA), "delhi": or_query(DELHI),
         "haryana": or_query(HARYANA)}
    for k, reg in REGIONS.items():
        s[k.lower()] = or_query(terms_for(reg))
    return s


def _search(q, place=None):
    return f"{FIELD}.search.exact:" + (f"({q}) AND ({place})" if place else q)


def plan(cfg):
    """(cache name, params) for every call, in priority order."""
    sc = scopes(cfg)
    calls = []
    yb = {"group_by": "publication_year"}
    gb = {"group_by": "primary_location.source.is_core"}
    base = f"{BASE},publication_year:{YEARS}"
    # baselines (Social Sciences)
    calls.append(("pop_base_global_core", {**yb, "filter": f"{base},{SS},{CORE}"}))
    for k in ("sa", "india"):
        calls.append((f"pop_base_{k}_core", {**yb, "filter": f"{base},{SS},{CORE},"
                                                             f"{FIELD}.search.exact:{sc[k]}"}))
    calls.append(("pop_base_india_all", {**yb, "filter": f"{base},{SS},{FIELD}.search.exact:{sc['india']}"}))
    for k in ["delhi", "haryana"] + [r.lower() for r in REGIONS]:
        calls.append((f"pop_base_{k}", {**gb, "filter": f"{base},{SS},{FIELD}.search.exact:{sc[k]}"}))
    calls.append(("pop_base_global_split", {**gb, "filter": f"{base},{SS}"}))
    themes = list(cfg["themes"])
    # (a) global and South Asia per year, core venues (all-venue versions exist from Stage 2)
    for t in themes:
        q = q_of(cfg, t)
        calls.append((f"pop_{t}_global_core", {**yb, "filter": f"{base},{CORE},{_search(q)}"}))
        calls.append((f"pop_{t}_sa_core", {**yb, "filter": f"{base},{CORE},{_search(q, sc['sa'])}"}))
    # (b) India per year, all and core
    for t in themes:
        q = q_of(cfg, t)
        calls.append((f"pop_{t}_india_all", {**yb, "filter": f"{base},{_search(q, sc['india'])}"}))
        calls.append((f"pop_{t}_india_core", {**yb, "filter": f"{base},{CORE},{_search(q, sc['india'])}"}))
    # (c) Delhi/NCR and Haryana totals, split by core
    for t in themes:
        q = q_of(cfg, t)
        for k in ("delhi", "haryana"):
            calls.append((f"pop_{t}_{k}", {**gb, "filter": f"{base},{_search(q, sc[k])}"}))
    # (d) other regions, totals split by core
    for t in themes:
        q = q_of(cfg, t)
        for k in REGIONS:
            calls.append((f"pop_{t}_reg_{k}", {**gb, "filter": f"{base},{_search(q, sc[k.lower()])}"}))
    # (e) precision sample of the South Asia hit set
    for t in themes:
        q = q_of(cfg, t)
        calls.append((f"pop_{t}_sa_sample", {"filter": f"{BASE},publication_year:2015-2026,"
                                                       f"{_search(q, sc['sa'])}",
                                             "sample": 40, "seed": SEED, "per_page": 40,
                                             "select": SAMPLE_SEL}))
    return calls


def fetch():
    cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
    f = Fetcher(min_interval=0.4, label="population")
    calls = plan(cfg)
    done = 0
    try:
        for name, params in calls:
            f.openalex_list(params, name)
            done += 1
            if done % 50 == 0:
                print(f"{done}/{len(calls)} calls, credits {f.remaining}", flush=True)
    except BudgetPaused as e:
        print(f"PAUSED after {done}/{len(calls)}: {e}")
    print(f"done {done}/{len(calls)}; network {f.network_calls}; credits {f.remaining}")


# ---------------------------------------------------------------- table
def _load(name):
    p = RAW / "api" / f"{name}.json.gz"
    return json.load(gzip.open(p)) if p.exists() else None


def _years(resp):
    if resp is None:
        return None
    return {int(g["key"]): g["count"] for g in resp["group_by"] if str(g["key"]).isdigit()}


def _split(resp):
    """group_by is_core -> (all, core)"""
    if resp is None:
        return None, None
    d = {str(g["key"]): g["count"] for g in resp["group_by"]}
    core = d.get("1", d.get("true", 0))
    return core + d.get("0", d.get("false", 0)), core


def _period(by, yrs):
    return sum(int(by.get(y, by.get(str(y), 0))) for y in yrs) if by is not None else None


def sa_precision(cfg, t, k):
    resp = _load(f"pop_{t}_sa_sample")
    if resp is None or not resp.get("results"):
        return None, 0, 0
    req, flags = compile_cfg(cfg, t)
    sc = cfg["themes"][t]["screen"]
    inc = bor = 0
    for w in resp["results"]:
        title = w.get("title") or w.get("display_name") or ""
        kw = "; ".join(x["display_name"] for x in (w.get("keywords") or []))
        d, _, _ = screen(title, abstract_text(w), kw, req, flags, t[0], "sample",
                         sc.get("strict_once", False), sc.get("flag_excludes", False))
        inc += d == "include"
        bor += d == "borderline"
    return inc, bor, len(resp["results"])


def table():
    cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
    g2 = json.loads((RAW / "counts" / "growth_stage2.json").read_text())
    growth = {r["theme"]: r for r in csv.DictReader((ROOT / "data/processed/growth_counts.csv").open())}
    k = None
    stats = list(csv.DictReader((ROOT / "data/processed/screening_stats.csv").open()))
    kept = sum(int(s["manual_kept"]) for s in stats)
    dropped = sum(int(s["manual_dropped"]) for s in stats)
    k = kept / (kept + dropped)
    qdom = {}
    pc = ROOT / "data/screening/precision_check_stage2.csv"
    if pc.exists():
        tot, ok = {}, {}
        for r in csv.DictReader(pc.open()):
            if r["why"] == "random6" and r["rule_decision"] == "include":
                d = r["assigned_theme"][0]
                tot[d] = tot.get(d, 0) + 1
                ok[d] = ok.get(d, 0) + (r["theme_ok"] == "Y")
        qdom = {d: ok[d] / tot[d] for d in tot}

    # baselines
    base = {"global_all": {int(y): v for y, v in g2["baseline"]["global"].items()},
            "sa_all": {int(y): v for y, v in g2["baseline"]["south_asia"].items()},
            "global_core": _years(_load("pop_base_global_core")),
            "sa_core": _years(_load("pop_base_sa_core")),
            "india_all": _years(_load("pop_base_india_all")),
            "india_core": _years(_load("pop_base_india_core"))}
    btot = {}
    for key in ["delhi", "haryana"] + [r.lower() for r in REGIONS] + ["global_split"]:
        btot[key] = _split(_load(f"pop_base_{key}"))

    rows = []
    for t in cfg["themes"]:
        gr = growth[t]
        p = float(gr["precision_est"])
        sp = sa_precision(cfg, t, k)
        if sp and sp[0] is not None and sp[2]:
            inc, bor, n = sp
            p_sa = (inc * qdom.get(t[0], 1.0) + bor * k) / n
            p_sa_n = n
        else:
            p_sa, p_sa_n = p, 0
        d2 = g2["themes"][t]
        series = {"global_all": {int(y): v for y, v in d2["global"].items()},
                  "sa_all": {int(y): v for y, v in d2["south_asia"].items()},
                  "global_core": _years(_load(f"pop_{t}_global_core")),
                  "sa_core": _years(_load(f"pop_{t}_sa_core")),
                  "india_all": _years(_load(f"pop_{t}_india_all")),
                  "india_core": _years(_load(f"pop_{t}_india_core"))}
        row = {"theme": t, "name": cfg["themes"][t]["name"], "p": round(p, 3),
               "p_sa": round(p_sa, 3), "p_sa_sample_n": p_sa_n}
        for key, by in series.items():
            scope = key.split("_")[0]
            pp = p if scope == "global" else p_sa
            for pn, yrs in PERIODS.items():
                raw = _period(by, yrs)
                b = _period(base.get(key), yrs)
                row[f"{key}_{pn}_raw"] = raw if raw is not None else ""
                row[f"{key}_{pn}_adj"] = round(raw * pp) if raw is not None else ""
                row[f"{key}_{pn}_per10k"] = (round(1e4 * raw * pp / b, 2)
                                             if raw is not None and b else "")
            a, c = row[f"{key}_2015-19_per10k"], row[f"{key}_2020-26_per10k"]
            row[f"{key}_growth"] = round(c / a, 2) if a not in ("", 0) and c != "" else ""
        for kk in ["delhi", "haryana"] + list(REGIONS):
            al, co = _split(_load(f"pop_{t}_{kk.lower()}" if kk in ("delhi", "haryana")
                                  else f"pop_{t}_reg_{kk}"))
            pp = p_sa if kk in ("delhi", "haryana") else p
            row[f"{kk.lower()}_all_2010-26_raw"] = al if al is not None else ""
            row[f"{kk.lower()}_core_2010-26_raw"] = co if co is not None else ""
            row[f"{kk.lower()}_all_2010-26_adj"] = round(al * pp) if al is not None else ""
            row[f"{kk.lower()}_core_2010-26_adj"] = round(co * pp) if co is not None else ""
        # location quotients: theme's share of a place scope relative to Social Sciences' share
        gtot = _period(series["global_all"], range(2010, 2027))
        bg = _period(base["global_all"], range(2010, 2027))
        for kk in ["sa", "india"]:
            v = _period(series[f"{kk}_all"], range(2010, 2027))
            bv = _period(base.get(f"{kk}_all"), range(2010, 2027))
            row[f"lq_{kk}"] = (round((v / gtot) / (bv / bg), 2)
                               if v is not None and gtot and bv and bg else "")
        for kk in ["delhi", "haryana"] + [r.lower() for r in REGIONS]:
            al = row.get(f"{kk}_all_2010-26_raw")
            ball = btot.get(kk, (None, None))[0]
            row[f"lq_{kk}"] = (round((al / gtot) / (ball / bg), 2)
                               if al not in ("", None) and gtot and ball else "")
        rows.append(row)
    out = ROOT / "data/processed/population_counts.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    bout = ROOT / "data/processed/population_baselines.json"
    bout.write_text(json.dumps({"per_year": {k: v for k, v in base.items()},
                                "totals_2010_26_all_core": btot}, indent=1, default=str))
    have = sum(1 for r in rows if r["india_all_2010-14_raw"] != "")
    print(f"{out.name}: {len(rows)} themes; India counts for {have}; SA precision samples for "
          f"{sum(1 for r in rows if r['p_sa_sample_n'])}")


if __name__ == "__main__":
    {"fetch": fetch, "table": table}[sys.argv[1]]()
