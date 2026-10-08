"""Emerging terms (BRIEF §5.3), from the map's records.

Usage: python3 scripts/emerging_terms.py        -> data/processed/emerging_terms.csv

Terms are the OpenAlex keywords attached to each record's work (cached API records). For each
term, its share of records is computed within each period -- records in 2018-21 carrying the
term / all records in 2018-21, and likewise for 2022-26 -- and terms are ranked by the ratio of
the two shares (with +0.5 smoothing of the earlier count). Raw counts are not compared: the
sample's period mix is fixed by the design (the recent slice covers 2022-26 only), so only
within-period shares are comparable, and even these carry the slice mix (see REPORT.md).
Only records in the 48 themes are used (supplementary-only records are left out). A term must
appear in at least 15 records in 2022-26 and in records of at least 2 themes. The final
ranking lists terms confirmed OpenAlex-wide first.
Robustness checks (columns): (1) the same share ratio within records found by an India/South
Asia slice only -- that slice spans all years with one ranking method, so its period mix is not
set by the recent slice; (2) OpenAlex-wide: the keyword's share of all Social Sciences works
(Growth-tab filters) in 2022-26 vs 2018-21, one cheap list call per keyword (filter keywords.id,
group_by year); a term is 'confirmed' when that population share also rose (ratio > 1.2).
Terms that are a theme's own query phrase are marked: the recent slice is relevance-ranked on
those phrases, which inflates their 2022-26 share in the sample.
Example papers: three 2022-24 records with the term and the highest FWCI (2025-26 works are left
out of FWCI-based choices: their citations are too young), falling back to 2025-26 records by
citation count when fewer than three exist.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetcher import Fetcher, load_work  # noqa: E402
from growth_counts import BASE  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EARLY, LATE = range(2018, 2022), range(2022, 2027)
MIN_LATE, MIN_THEMES, TOP = 15, 2, 30


def main():
    recs = [r for r in json.loads((ROOT / "data/processed/records.json").read_text())
            if r["Supplementary"] != "Y"]
    n = Counter()
    cnt = {"early": Counter(), "late": Counter()}
    themes = defaultdict(Counter)
    ex = defaultdict(list)
    for r in recs:
        y = r["Year"] or 0
        per = "early" if y in EARLY else "late" if y in LATE else None
        if per is None:
            continue
        n[per] += 1
        kws = {k["display_name"].strip() for k in (load_work(r["OpenAlex ID"]).get("keywords") or [])}
        for k in kws:
            cnt[per][k] += 1
            if per == "late":
                themes[k][r["Primary theme"]] += 1
                ex[k].append(r)
    # India-slice-only shares and keyword IDs
    nin = Counter()
    cin = {"early": Counter(), "late": Counter()}
    kid = {}
    for r in recs:
        y = r["Year"] or 0
        per = "early" if y in EARLY else "late" if y in LATE else None
        kws = load_work(r["OpenAlex ID"]).get("keywords") or []
        for x in kws:
            kid.setdefault(x["display_name"].strip(), x["id"].rsplit("/", 1)[-1])
        if per is None or ":india" not in r["Found in"]:
            continue
        nin[per] += 1
        for k in {x["display_name"].strip() for x in kws}:
            cin[per][k] += 1
    import yaml
    import re
    cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
    qph = set()
    for tc in list(cfg["themes"].values()) + list((cfg.get("supplementary") or {}).values()):
        for q in tc["queries"]:
            qph |= {m.lower() for m in re.findall(r'"([^"]+)"', q)}
            qph |= {m.lower() for m in re.findall(r"\b([A-Za-z][\w-]{3,})\b", re.sub(r'"[^"]+"', " ", q))}
    rows = []
    for k, c_late in cnt["late"].items():
        if c_late < MIN_LATE or len(themes[k]) < MIN_THEMES:
            continue
        c_early = cnt["early"].get(k, 0)
        s_e = (c_early + 0.5) / n["early"]
        s_l = c_late / n["late"]
        rs = ex[k]
        fw = sorted([x for x in rs if 2022 <= (x["Year"] or 0) <= 2024],
                    key=lambda x: -(x["FWCI"] or 0))
        young = sorted([x for x in rs if (x["Year"] or 0) >= 2025],
                       key=lambda x: -(x["Cited-by count"] or 0))
        picks = (fw + young)[:3]
        rows.append({
            "term": k, "records_2018_21": c_early, "records_2022_26": c_late,
            "share_2018_21_pct": round(100 * c_early / n["early"], 2),
            "share_2022_26_pct": round(100 * s_l, 2),
            "share_ratio": round(s_l / s_e, 2),
            "share_change_pts": round(100 * (s_l - c_early / n["early"]), 2),
            "query_phrase": "Y" if k.lower() in qph or k.lower().rstrip("s") in qph else "",
            "india_slice_2018_21": cin["early"].get(k, 0),
            "india_slice_2022_26": cin["late"].get(k, 0),
            "india_slice_share_ratio": round((cin["late"].get(k, 0) / max(nin["late"], 1)) /
                                             ((cin["early"].get(k, 0) + 0.5) / max(nin["early"], 1)), 2),
            "keyword_id": kid.get(k, ""),
            "top_themes": ", ".join(f"{t} ({v})" for t, v in themes[k].most_common(3)),
            **{f"example_{i + 1}": (f"{p['ID']} {p['Authors'].split(';')[0]} ({p['Year']}) "
                                    f"{p['Title'][:90]}") for i, p in enumerate(picks)},
        })
    rows.sort(key=lambda r: (-r["share_ratio"], -r["records_2022_26"]))
    # OpenAlex-wide check for the 75 highest-ranked terms (cheap list calls, cached)
    f = Fetcher(min_interval=0.4, label="emerging")
    pb = None
    for r in rows[:75]:
        if not r["keyword_id"]:
            continue
        flt = f"{BASE},publication_year:2018-2026,primary_topic.domain.id:2"
        resp = f.openalex_list({"filter": f"{flt},keywords.id:{r['keyword_id']}",
                                "group_by": "publication_year"}, f"emerging_kw_{r['keyword_id']}")
        if pb is None:
            pb = f.openalex_list({"filter": flt, "group_by": "publication_year"},
                                 "emerging_kw_baseline")
            pb = {int(g["key"]): g["count"] for g in pb["group_by"] if str(g["key"]).isdigit()}
        by = {int(g["key"]): g["count"] for g in resp["group_by"] if str(g["key"]).isdigit()}
        e = sum(by.get(y, 0) for y in EARLY) / sum(pb.get(y, 0) for y in EARLY)
        l_ = sum(by.get(y, 0) for y in LATE) / sum(pb.get(y, 0) for y in LATE)
        r["oa_ss_works_2018_21"] = sum(by.get(y, 0) for y in EARLY)
        r["oa_ss_works_2022_26"] = sum(by.get(y, 0) for y in LATE)
        r["oa_share_ratio"] = round(l_ / e, 2) if e else "new"
        r["confirmed"] = "Y" if (r["oa_share_ratio"] == "new" or r["oa_share_ratio"] > 1.2) else ""
    # final ranking: terms confirmed OpenAlex-wide first (by sample share ratio), then the rest
    rows.sort(key=lambda r: (r.get("confirmed") != "Y", -r["share_ratio"], -r["records_2022_26"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    out = ROOT / "data/processed/emerging_terms.csv"
    cols = ["rank", "term", "records_2018_21", "records_2022_26", "share_2018_21_pct",
            "share_2022_26_pct", "share_ratio", "share_change_pts", "query_phrase",
            "india_slice_2018_21", "india_slice_2022_26", "india_slice_share_ratio",
            "oa_ss_works_2018_21", "oa_ss_works_2022_26", "oa_share_ratio", "confirmed",
            "keyword_id", "top_themes",
            "example_1", "example_2", "example_3"]
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"records 2018-21: {n['early']}, 2022-26: {n['late']}; eligible terms {len(rows)}")
    for r in rows[:TOP]:
        print(f"{r['rank']:3d} {r['term'][:40]:40s} {r['records_2018_21']:4d} {r['records_2022_26']:4d} "
              f"{r['share_2018_21_pct']:5.2f}% -> {r['share_2022_26_pct']:5.2f}%  x{r['share_ratio']} q={r['query_phrase'] or '-'} "
              f"IN x{r['india_slice_share_ratio']} OA x{r.get('oa_share_ratio', '')}  {r['top_themes']}")
    print("credits", f.remaining)


if __name__ == "__main__":
    main()
