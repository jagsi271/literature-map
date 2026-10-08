"""Screen, tag and deduplicate the fetched works into one record table.

Usage: python3 scripts/build_records.py [THEME ...]     (default: every theme with manifests)

Inputs : data/raw/searches/*.json, data/raw/works/*.json, queries.yaml,
         data/screening/manual_review.csv (my decisions on borderline records)
Outputs: data/processed/candidates.csv   one row per (work, theme, slice) with screening result
         data/processed/pending_review.csv  borderline records still lacking a manual decision
         data/processed/records.csv / records.json  deduplicated, tagged records (BRIEF §4)

Screening (per theme, on title + abstract; OpenAlex keyword tags are ignored):
  - excluded document types and retracted works are dropped;
  - `screen.require[0]` (core concept) in the title or twice in abstract/keywords and every
    context term somewhere -> 'include'; core concept absent -> 'exclude';
  - one core mention, missing context, a `flag` match or a missing abstract -> 'borderline';
  - borderline records are kept or dropped by data/screening/manual_review.csv.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gazetteer import places, region_label  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
SCREEN = ROOT / "data" / "screening"

EXCLUDED_TYPES = {
    "book-review", "paratext", "erratum", "peer-review", "retraction", "supplementary-materials",
    "dataset", "software", "libguides", "grant", "standard", "letter", "editorial",
}

# --------------------------------------------------------------------------- text helpers
def abstract_text(w) -> str:
    inv = w.get("abstract_inverted_index") or {}
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def norm_title(t: str) -> str:
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z“\"(])")


def sentences(text):
    return [s.strip() for s in SENT_SPLIT.split(text) if len(s.strip()) > 20]


AIM = re.compile(r"\b(this (paper|article|study|chapter|book|essay|research)|we (argue|examine|"
                 r"explore|investigate|analy[sz]e|show|propose|develop|study)|i (argue|examine|"
                 r"explore|show|analy[sz]e|suggest)|aims? to|the purpose of)\b", re.I)
GAP = re.compile(r"\b(gaps?\b|little (is known|attention|research)|scant|under-?(researched|"
                 r"studied|explored|theori[sz]ed)|overlooked|neglected|remains? (unclear|"
                 r"unexplored|limited)|future (research|studies|work)|further research|"
                 r"limitations?|lacks?\b|lack of|has yet to|have yet to|calls? for)", re.I)


def summary(abstract):
    ss = sentences(abstract)
    if not ss:
        return ""
    pick = next((s for s in ss if AIM.search(s)), ss[0])
    return "auto: " + (pick[:297] + "…" if len(pick) > 300 else pick)


def stated_gaps(abstract):
    ss = [s for s in sentences(abstract) if GAP.search(s)]
    if not ss:
        return ""
    txt = " | ".join(ss[:2])
    return "auto: " + (txt[:497] + "…" if len(txt) > 500 else txt)


METHOD_RX = {
    "review": r"\b(systematic (literature )?review|literature review|scoping review|meta-analy|"
              r"bibliometric|review of (the )?(literature|research|studies)|state of the art review)",
    "computational": r"\b(machine learning|deep learning|neural network|simulation|agent-based|"
                     r"computational|text mining|topic model|natural language processing|"
                     r"big data analytics|network analysis|remote sensing|spatial analysis|gis\b|"
                     r"geospatial|algorithm(s)? (to|for))",
    "quantitative": r"\b(survey(ed)?|regression|econometric|statistical|quantitative|panel data|"
                    r"difference-in-differences|randomi[sz]ed|questionnaire|structural equation|"
                    r"sem\b|logit|probit|respondents|sample of \d|n ?= ?\d|data (from|on) \d|rcts?\b|"
                    r"observations were|results (consistently )?(show|indicate)|geocoded|dataset|"
                    r"database of|descriptive statistics|correlat)",
    "qualitative": r"\b(interviews?|ethnograph|fieldwork|focus groups?|qualitative|participant "
                   r"observation|case stud(y|ies)|discourse analysis|archival|oral histor|"
                   r"document analysis|thematic analysis|in-depth|uses (this|the) case|the case of|"
                   r"drawing on (empirical|fieldwork|research)|narratives?)",
    "conceptual": r"\b(we argue|i argue|this (paper|article|essay|chapter) argues|theor(y|ies|"
                  r"etical|i[sz]e)|conceptual|framework|critique|reflect(s|ion)|essay|"
                  r"intervention|commentary|agenda|debates?|perspectives?|approach(es)? to|"
                  r"discuss(es)?|explores? how|summari[sz]e)",
}
METHOD_RX = {k: re.compile(v, re.I) for k, v in METHOD_RX.items()}


def method(text):
    hit = {k for k, rx in METHOD_RX.items() if rx.search(text)}
    if "review" in hit:
        return "review"
    if re.search(r"mixed[- ]methods?", text, re.I) or {"quantitative", "qualitative"} <= hit:
        return "mixed"
    for k in ("computational", "quantitative", "qualitative", "conceptual"):
        if k in hit:
            return k
    return "unclear"


SHORTLIST = re.compile(
    r"\b(railway stations?|train stations?|rail(way)? station|metro stations?|bus (stations?|"
    r"terminals?|depots?)|waiting rooms?|politics of waiting|waithood|time spent waiting|"
    r"waiting (for|at|in) (the )?(bus|buses|train|trains|metro|transit|state)|night-?time "
    r"(mobility|travel|transport|transit|commut\w*)|night (travel|buses|shift)|after dark|"
    r"operating hours|service hours|late-night (transit|transport|buses|trains)|fare "
    r"integration|integrated (fare|ticketing)|transit cards?|(transit|transport|bus|metro|fare) smart ?cards?|smart ?cards? (for|in) (transit|public transport|buses|metro)|ncmc|national common "
    r"mobility card|rail-led|transit-oriented development|metro rail|elevated (rail|metro|railway|"
    r"road|expressway|corridor)|flyovers?|underpass(es)?|under the (flyover|bridge|metro)|"
    r"infrastructur\w* undersides?|viaducts?)\b", re.I)


def shortlist_tag(text, haryana):
    tags = sorted({m.group(0).lower() for m in SHORTLIST.finditer(text)})
    if haryana and re.search(r"\b(secondary|small|medium|census|satellite) (cit|town)", text, re.I):
        tags.append("Haryana secondary city")
    return "; ".join(tags)


# --------------------------------------------------------------------------- screening
def compile_theme(cfg, t):
    sc = cfg["themes"][t].get("screen", {})
    req = [re.compile(r, re.I) for r in sc.get("require", [])]
    flags = [re.compile(r, re.I) for r in cfg.get("global_flags", []) + sc.get("flag", [])]
    return req, flags


def screen(text_t, text_rest, has_abs, req, flags):
    """Return (decision, score, reason).

    req[0] is the core concept, req[1:] context terms (see queries.yaml header)."""
    core, context = req[0], req[1:]
    full = f"{text_t} {text_rest}"
    core_title = bool(core.search(text_t))
    core_rest = len(core.findall(text_rest))
    if not core_title and core_rest == 0:
        return ("borderline" if not has_abs else "exclude"), 0, "core concept missing"
    score = 3 * core_title + min(core_rest, 3)
    if not all(r.search(full) for r in context):
        return "borderline", score, "context terms missing"
    flagged = [f.pattern[:40] for f in flags if f.search(full)]
    if flagged:
        return "borderline", score, "flag: " + flagged[0]
    if not has_abs:
        return "borderline", score, "no abstract"
    if len(text_rest) < 250 or re.search(r"^\W*\"?[^.]{5,200}\"?\s*,?\s*\d+\s*\(\d+\),?\s*pp?\.", text_rest):
        return "borderline", score, "stub abstract (possible book review)"
    if not core_title and core_rest < 2:
        return "borderline", score, "core concept mentioned once"
    return "include", score, "rules"


def load_manual():
    p = SCREEN / "manual_review.csv"
    if not p.exists():
        return {}
    with p.open() as f:
        return {(r["openalex_id"], r["theme"]): r for r in csv.DictReader(f)}


# --------------------------------------------------------------------------- main
def main(themes_wanted):
    cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
    idcheck = json.loads((RAW / "searches" / "_id_check.json").read_text())
    manual = load_manual()
    cands = []
    for man in sorted((RAW / "searches").glob("*_*.json")):
        if man.name.startswith("_"):
            continue
        m = json.loads(man.read_text())
        t = m["theme"]
        if themes_wanted and t not in themes_wanted:
            continue
        req, flags = compile_theme(cfg, t)
        for rank, (wid, _) in enumerate(m["results"], 1):
            w = json.loads((RAW / "works" / f"{wid}.json").read_text())
            title = w.get("title") or w.get("display_name") or ""
            abstract = abstract_text(w)
            kw = "; ".join(k["display_name"] for k in (w.get("keywords") or []))
            full = f"{title} {abstract} {kw}"
            c = dict(openalex_id=wid, theme=t, slice=m["slice"], rank=rank, title=title,
                     year=w.get("publication_year"), type=w.get("type"),
                     cited_by=w.get("cited_by_count", 0), has_abstract=bool(abstract))
            if idcheck.get(wid) != "ok":
                c.update(decision="exclude", score=0, reason=f"id check {idcheck.get(wid)}")
            elif w.get("is_retracted"):
                c.update(decision="exclude", score=0, reason="retracted")
            elif w.get("type") in EXCLUDED_TYPES:
                c.update(decision="exclude", score=0, reason=f"type {w.get('type')}")
            else:
                # OpenAlex keyword tags are not used: in testing they attached e.g. "digital
                # identity" to education papers, producing false core matches.
                d, s, r = screen(title, abstract, bool(abstract), req, flags)
                c.update(decision=d, score=s, reason=r)
            c["final"] = c["decision"]
            if c["decision"] == "borderline":
                mr = manual.get((wid, t))
                c["final"] = mr["decision"] if mr else "pending"
                c["reason"] += f" | manual: {mr['note']}" if mr and mr.get("note") else ""
            c["_w"], c["_abs"], c["_full"] = w, abstract, full
            cands.append(c)

    OUT.mkdir(parents=True, exist_ok=True)
    cols = ["openalex_id", "theme", "slice", "rank", "title", "year", "type", "cited_by",
            "has_abstract", "decision", "score", "reason", "final"]
    with (OUT / "candidates.csv").open("w", newline="") as f:
        wr = csv.DictWriter(f, cols, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(cands)
    pend = [c for c in cands if c["final"] == "pending"]
    seen = set()
    with (OUT / "pending_review.csv").open("w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["openalex_id", "theme", "reason", "title", "abstract_start"])
        for c in pend:
            if (c["openalex_id"], c["theme"]) in seen:
                continue
            seen.add((c["openalex_id"], c["theme"]))
            wr.writerow([c["openalex_id"], c["theme"], c["reason"], c["title"], c["_abs"][:400]])

    # ---- merge kept candidates by work, then deduplicate by DOI and normalised title
    kept = [c for c in cands if c["final"] == "include"]
    by_work = defaultdict(list)
    for c in kept:
        by_work[c["openalex_id"]].append(c)

    def quality(wid):
        w = by_work[wid][0]["_w"]
        venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        repo = bool(re.search(r"zenodo|figshare|ssrn|repository|eprints|research online|dspace|"
                              r"repositorio|hal\b|e-theses", venue, re.I))
        return (bool(w.get("doi")) and not repo, w.get("cited_by_count", 0), -int(wid[1:]))

    groups, key_of = {}, {}
    for wid in sorted(by_work, key=quality, reverse=True):
        w = by_work[wid][0]["_w"]
        doi = (w.get("doi") or "").lower().replace("https://doi.org/", "")
        nt = norm_title(w.get("title") or "")
        k = None
        if doi and ("doi", doi) in key_of:
            k = key_of[("doi", doi)]
        elif nt and len(nt) > 15 and ("t", nt) in key_of:
            k = key_of[("t", nt)]
        if k is None:
            k = wid
            groups[k] = []
        groups[k].append(wid)
        if doi:
            key_of.setdefault(("doi", doi), k)
        if nt:
            key_of.setdefault(("t", nt), k)

    records = []
    for k, members in groups.items():
        w = by_work[k][0]["_w"]
        allc = [c for wid in members for c in by_work[wid]]
        theme_score = defaultdict(int)
        for c in allc:
            theme_score[c["theme"]] = max(theme_score[c["theme"]], c["score"])
        ranked = sorted(theme_score, key=lambda t: (-theme_score[t], t))
        primary, secondary = ranked[0], (ranked[1] if len(ranked) > 1 else "")
        slices = sorted({f"{c['theme']}:{c['slice']}" for c in allc})
        title = w.get("title") or ""
        abstract = by_work[k][0]["_abs"]
        text = f"{title}. {abstract}"
        pl, regs, india, delhi, haryana = places(text)
        loc = w.get("primary_location") or {}
        src = loc.get("source") or {}
        best = w.get("best_oa_location") or {}
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        manual_kept = any(c["decision"] == "borderline" for c in allc)
        title_hit = any(c["score"] >= 3 for c in allc if c["theme"] == primary)
        conf = "medium" if manual_kept else ("high" if title_hit else "medium")
        if not abstract:
            conf = "low"
        rec = {
            "ID": "",
            "Title": title,
            "Year": w.get("publication_year"),
            "Authors": "; ".join(a["author"]["display_name"] for a in w.get("authorships", [])[:10])
                       + (" et al." if len(w.get("authorships", [])) > 10 else ""),
            "Venue": src.get("display_name") or "",
            "Document type": w.get("type"),
            "DOI": doi,
            "OpenAlex ID": k,
            "Link": w.get("doi") or loc.get("landing_page_url") or f"https://openalex.org/{k}",
            "Open-access link": best.get("pdf_url") or best.get("landing_page_url")
                                or (w.get("open_access") or {}).get("oa_url") or "",
            "Cited-by count": w.get("cited_by_count", 0),
            "Domain": primary[0],
            "Primary theme": primary,
            "Secondary theme": secondary,
            "Places studied": "; ".join(pl),
            "Region": region_label(regs),
            "India flag": "Y" if india else "",
            "Delhi/NCR flag": "Y" if delhi else "",
            "Haryana flag": "Y" if haryana else "",
            "Method": method(text) if abstract else "unclear",
            "Landmark flag": "Y" if any(c["slice"] == "landmarks" for c in allc) else "",
            "Emerging flag": "Y" if (w.get("publication_year") or 0) >= 2022
                                    and (w.get("fwci") or 0) >= 1.5 else "",
            "One-line summary": summary(abstract),
            "Stated gaps": stated_gaps(abstract),
            "Shortlist tag": shortlist_tag(text, haryana),
            "Screening confidence": conf,
            "Found in": "; ".join(slices),
            "Duplicates merged": "; ".join(m for m in members if m != k),
            "FWCI": w.get("fwci"),
        }
        records.append(rec)
    records.sort(key=lambda r: (r["Primary theme"], -(r["Cited-by count"] or 0)))
    for i, r in enumerate(records, 1):
        r["ID"] = f"LM{i:05d}"
    with (OUT / "records.csv").open("w", newline="") as f:
        wr = csv.DictWriter(f, list(records[0]))
        wr.writeheader()
        wr.writerows(records)
    (OUT / "records.json").write_text(json.dumps(records, indent=1, ensure_ascii=False))

    # ---- summary
    print(f"candidates {len(cands)} | include(rules) "
          f"{sum(c['decision']=='include' for c in cands)} | borderline "
          f"{sum(c['decision']=='borderline' for c in cands)} | exclude "
          f"{sum(c['decision']=='exclude' for c in cands)} | pending manual {len(seen)}")
    print(f"kept candidates {len(kept)} -> unique works {len(by_work)} -> records {len(records)}")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
