"""Recall test against seeds.csv (176 known works chosen by the researcher, mostly India).

Usage: python3 scripts/recall_test.py [LABEL]          (default label: stage2)

1. Resolve each seed in OpenAlex: DOI lookup in batches (filter doi:a|b|..., a cheap list call),
   then a title search (filter title.search) for seeds without a DOI or whose DOI is not in
   OpenAlex; a title match needs normalised-title similarity >= 0.85 (and year within 1 when
   the seed has a year). Lookups use corpus=all, so works that exist only in OpenAlex's
   expansion corpus (not searched by the pipeline) are recognised as such.
2. For each resolved seed: found if it is a record (by OpenAlex ID, merged duplicate, DOI or
   normalised title). Otherwise the reason is classified:
     not in OpenAlex       no DOI or title match
     expansion corpus only in OpenAlex, but outside the default (core) corpus the pipeline searches
     screened out         retrieved as a candidate but excluded by the rules or by hand
     below cut-off        a theme query matches the work, but it ranked outside the slice's top N
     query gap            no theme query (nor supplementary query) matches the work
   The query test runs each theme's OR-combined query restricted to the missed seeds' IDs
   (one search per theme; title_and_abstract.search.exact, as in the pipeline).
Output: data/screening/recall_seeds_{LABEL}.csv and a printed summary.
"""
import csv
import difflib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_records import norm_title  # noqa: E402
from fetcher import Fetcher  # noqa: E402
from run_search import FIELD  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
label = sys.argv[1] if len(sys.argv) > 1 else "stage2"
cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
seeds = list(csv.DictReader((ROOT / "seeds.csv").open()))
recs = json.loads((ROOT / "data/processed/records.json").read_text())
cands = list(csv.DictReader((ROOT / "data/processed/candidates.csv").open()))
f = Fetcher(min_interval=0.5, label="recall")
SEL = "id,doi,title,display_name,publication_year,type,is_xpac"

# seed categories (seeds.csv pilot_theme) -> the map's themes that should cover them
CATEGORY_THEMES = {
    "Mobility & transport": "A8 C9 S1 S2 S3 S4 S5 S6",
    "Smart city & digital governance": "C1 C5 C7 C8",
    "Platforms & gig economy": "B1 B11 C2 C15",
    "Housing, resettlement & informality": "A3 A4 C14",
    "Heritage, events & world-class city": "A13 C16",
    "Land, peri-urban & private cities": "A5 A2",
    "Small towns & census towns": "A6 S7",
    "Welfare technology & identity": "B5 B4",
    "Digital finance & payments": "B6 C11",
    "Digital divide & access": "B7 B13",
    "Bureaucracy, waiting & documents": "B5 A1 S2",
    "Digital publics & social media": "B8 C12 C18",
    "Cybercrime & fraud": "B10 C17",
    "Gender & public space": "A9 A12",
    "Knowledge access & libraries": "B7",
    "Neighbourhoods, RWAs & civil society": "C18 A1",
    "Surveillance & security": "B3 C6",
    "Street vending & informal economy": "A10 C14",
}


def clean_doi(d):
    d = (d or "").strip().lower()
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", d)


def sim(a, b):
    a, b = norm_title(a), norm_title(b)
    if not a or not b:
        return 0.0
    if a in b or b in a:
        return 1.0 if min(len(a), len(b)) > 25 else 0.9
    return difflib.SequenceMatcher(None, a, b).ratio()


# ---------------------------------------------------------------- 1. resolve
by_doi = {}
dois = sorted({clean_doi(s["doi"]) for s in seeds if clean_doi(s["doi"])})
for i in range(0, len(dois), 50):
    batch = dois[i:i + 50]
    resp = f.openalex_list({"filter": "doi:" + "|".join(batch), "per_page": 100, "select": SEL,
                            "corpus": "all"}, f"recall_doi_{label}_{i // 50}")
    for w in resp["results"]:
        by_doi[clean_doi(w.get("doi"))] = w

resolved = []
for n, s in enumerate(seeds):
    w, method = by_doi.get(clean_doi(s["doi"])), "doi"
    if w is None:
        q = re.sub(r"[^\w\s]", " ", s["title"]).strip()
        q = " ".join(q.split()[:25])
        resp = f.openalex_list({"filter": f"title.search:{q}", "per_page": 5, "select": SEL,
                                "corpus": "all"}, f"recall_title_{label}_{n:03d}")
        best, bs = None, 0.0
        for c in resp["results"]:
            sc = sim(s["title"], c.get("title") or c.get("display_name") or "")
            yr_ok = not s["year"] or not c.get("publication_year") or \
                abs(int(s["year"]) - c["publication_year"]) <= 1
            if sc >= 0.85 and yr_ok and sc > bs:
                best, bs = c, sc
        w, method = best, ("title" if best else "")
    resolved.append((s, w, method))

# ---------------------------------------------------------------- 2. classify
rec_by_id, rec_by_doi, rec_by_title = {}, {}, {}
for r in recs:
    for wid in [r["OpenAlex ID"]] + [x for x in r["Duplicates merged"].split("; ") if x]:
        rec_by_id[wid] = r
    if r["DOI"]:
        rec_by_doi[r["DOI"].lower()] = r
    rec_by_title[norm_title(r["Title"])] = r
cand_by_id = defaultdict(list)
for c in cands:
    cand_by_id[c["openalex_id"]].append(c)

rows, missed = [], {}
for s, w, method in resolved:
    row = {"title": s["title"], "year": s["year"], "doi": clean_doi(s["doi"]),
           "category": s["pilot_theme"], "expected_themes": CATEGORY_THEMES.get(s["pilot_theme"], ""),
           "openalex_id": "", "match": method, "status": "", "record_id": "",
           "primary_theme": "", "detail": ""}
    if w is None:
        row["status"] = "not in OpenAlex"
        rows.append(row)
        continue
    wid = w["id"].rsplit("/", 1)[-1]
    row["openalex_id"] = wid
    r = rec_by_id.get(wid) or rec_by_doi.get(clean_doi(w.get("doi"))) or \
        rec_by_title.get(norm_title(w.get("title") or ""))
    if r:
        row.update(status="found", record_id=r["ID"], primary_theme=r["Primary theme"],
                   detail=("Supplementary only" if r["Supplementary"] == "Y" else ""))
    elif w.get("is_xpac"):
        row.update(status="expansion corpus only",
                   detail="OpenAlex expansion corpus; pipeline searches the core corpus")
    elif cand_by_id.get(wid):
        cs = cand_by_id[wid]
        row.update(status="screened out", detail="; ".join(
            sorted({f"{c['theme']}:{c['slice']} {c['final']} ({c['reason'][:90]})" for c in cs})))
    else:
        missed[wid] = row
    rows.append(row)

# query test for seeds never retrieved
themes = list(cfg["themes"]) + list(cfg.get("supplementary") or {})
match = defaultdict(list)
ids = sorted(missed)
for t in themes:
    tc = cfg["themes"].get(t) or cfg["supplementary"][t]
    q = " OR ".join(f"({x})" for x in tc["queries"])
    for i in range(0, len(ids), 100):
        batch = ids[i:i + 100]
        resp = f.openalex_list({"filter": f"openalex_id:{'|'.join(batch)},"
                                          f"{FIELD}.search.exact:{q}",
                                "per_page": 100, "select": "id"},
                               f"recall_query_{label}_{t}_{i // 100}")
        for w in resp["results"]:
            match[w["id"].rsplit("/", 1)[-1]].append(t)
for wid, row in missed.items():
    if match.get(wid):
        row.update(status="below cut-off",
                   detail="query matches " + " ".join(match[wid]))
    else:
        row.update(status="query gap", detail="no theme or supplementary query matches")

out = ROOT / "data" / "screening" / f"recall_seeds_{label}.csv"
with out.open("w", newline="") as fh:
    wr = csv.DictWriter(fh, list(rows[0]))
    wr.writeheader()
    wr.writerows(rows)

st = Counter(r["status"] for r in rows)
print(f"seeds {len(rows)}: " + ", ".join(f"{k} {v}" for k, v in st.most_common()))
print(f"resolved by DOI {sum(r['match'] == 'doi' for r in rows)}, by title "
      f"{sum(r['match'] == 'title' for r in rows)}")
bycat = defaultdict(Counter)
for r in rows:
    bycat[r["category"]][r["status"]] += 1
for k, v in sorted(bycat.items(), key=lambda x: -sum(x[1].values())):
    print(f"  {k:40s} {sum(v.values()):3d}  " + ", ".join(f"{a} {b}" for a, b in v.most_common()))
print(f"network calls {f.network_calls}, credits remaining {f.remaining}")
