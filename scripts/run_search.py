"""Run a theme's searches directly against the OpenAlex API and store the manifests.

Usage: python3 scripts/run_search.py THEME [SLICE ...]     (default slices: all three)

Stage 2 replaces the Stage 1 connector + transcription step: IDs, years and totals are
written straight from the API response. The raw responses are cached in data/raw/api/
(gzipped) and are the stored work records (indexed by work ID in data/raw/works_index.json,
so no second fetch is needed); re-running a slice uses the cache and costs nothing.

Slices (see queries.yaml `slices_stage2`):
  landmarks : the theme's queries OR-ed into one search, sort cited_by_count:desc
  recent    : one search per query string, years 2022-2026, sort relevance_score:desc
  india     : one search per query string AND south_asia_terms, sort relevance_score:desc
Per-query searches for recent / india keep rare phrases from dominating an OR-combined
relevance ranking (Stage 1 problem with A9).

Search field: title_and_abstract.search.exact (quotes = exact phrase, no stemming). Stage 1 used
title_abstract_keywords (title, abstract and the OpenAlex keywords a phrase names); in the
first Stage 2 run (A1) keyword tags alone pulled highly cited works that never use the term
into the landmark slice (e.g. Jacobs 1961 tagged "urban governance"), so Stage 2 searches
title and abstract only. Retracted works are filtered out.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_search import load  # noqa: E402
from fetcher import RAW, BudgetPaused, Fetcher, index_response  # noqa: E402

SELECT = ("id,doi,title,display_name,publication_year,publication_date,type,cited_by_count,"
          "authorships,primary_location,best_oa_location,open_access,abstract_inverted_index,"
          "is_retracted,fwci,keywords,primary_topic,language")


FIELD = "title_and_abstract"


def sa_terms(cfg):
    return " ".join(cfg["south_asia_terms"].split())


def plan_supplementary(cfg, theme, slice_name):
    """Supplementary query sets (queries.yaml `supplementary`): one combined query per slice;
    landmarks top 50 by citations, recent (2022-26) and india top 40 by relevance."""
    t = cfg["supplementary"][theme]
    q = " OR ".join(f"({x})" for x in t["queries"])
    if slice_name == "landmarks":
        return [(f"{theme}_landmarks", q, {"sort": "cited_by_count:desc", "per_page": 50})]
    if slice_name == "recent":
        return [(f"{theme}_recent", q, {"sort": "relevance_score:desc", "per_page": 40,
                                         "years": "2022-2026"})]
    if slice_name == "india":
        if theme != "S7":  # S7 (Haryana cities) is India-specific already
            q = f"({q}) AND ({sa_terms(cfg)})"
        return [(f"{theme}_india", q, {"sort": "relevance_score:desc", "per_page": 40})]
    return []


def plan(cfg, theme, slice_name, qcfg=None):
    """List of (manifest name, query, params) for one theme and slice."""
    if theme.startswith("S"):
        return plan_supplementary(cfg, theme, slice_name)
    t = qcfg or cfg["themes"][theme]
    qs = t["queries"]
    s2 = cfg["slices_stage2"]
    out = []
    if slice_name in ("landmarks", "landmarks_p2"):
        # landmarks_p2: the next 100 by citations, pulled when fewer than 25 landmark
        # records survive screening and review on page 1
        q = " OR ".join(f"({x})" for x in qs)
        page = 2 if slice_name == "landmarks_p2" else 1
        out.append((f"{theme}_{slice_name}", q, {"sort": "cited_by_count:desc", "page": page,
                                                 "per_page": s2["landmarks"]["per_page"]}))
    elif slice_name in ("recent", "india"):
        n = s2[slice_name]
        per = max(n["min_per_query"], min(n["max_per_query"], math.ceil(n["target"] / len(qs))))
        for i, x in enumerate(qs, 1):
            q = f"({x}) AND ({sa_terms(cfg)})" if slice_name == "india" else x
            p = {"sort": "relevance_score:desc", "per_page": per}
            if slice_name == "recent":
                p["years"] = "2022-2026"
            out.append((f"{theme}_{slice_name}_q{i}", q, p))
    return out


def run_one(f, theme, slice_name, name, query, p, stage="stage2", extra=None):
    filt = f"{FIELD}.search.exact:{query},is_retracted:false"
    if "years" in p:
        filt += f",publication_year:{p['years']}"
    params = {"filter": filt, "sort": p["sort"], "per_page": p["per_page"], "select": SELECT}
    if p.get("page", 1) > 1:
        params["page"] = p["page"]
    resp = f.openalex_list(params, f"search_{name}")
    index_response(f"data/raw/api/search_{name}.json.gz", resp)
    results = [[w["id"].rsplit("/", 1)[-1], w.get("publication_year") or 0]
               for w in resp["results"]]
    meta = resp["meta"]
    man = {
        "theme": theme,
        "slice": slice_name,
        "stage": stage,
        "source": "OpenAlex API /works (IDs written from the response by scripts/run_search.py)",
        "query": query,
        "mode": "exact",
        "search_in": FIELD,
        "filter": filt,
        "sort": p["sort"],
        "per_page": p["per_page"],
        "oql": (meta.get("x_query") or {}).get("oql"),
        "page": p.get("page", 1),
        "total_results": meta["count"],
        "retrieved": dt.date.today().isoformat(),
        "cache": f"data/raw/api/search_{name}.json.gz",
        **(extra or {}),
        "results": results,
    }
    (RAW / "searches" / f"{name}.json").write_text(json.dumps(man, indent=1))
    return man


def main(theme, slices):
    cfg = load()
    f = Fetcher(min_interval=0.5, label=theme)
    for sl in slices:
        for name, q, p in plan(cfg, theme, sl):
            m = run_one(f, theme, sl.replace("_p2", ""), name, q, p)
            print(f"{name}: total {m['total_results']}, got {len(m['results'])}", flush=True)
    print(f"network calls {f.network_calls}, cache hits {f.cache_hits}, credits remaining "
          f"{f.remaining}")


if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2:] or ["landmarks", "recent", "india"])
    except BudgetPaused as e:
        sys.exit(f"PAUSED: {e}")
