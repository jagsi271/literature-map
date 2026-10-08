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
from fetcher import load_work  # noqa: E402
from gazetteer import names_city, places, region_label  # noqa: E402

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
def screen(title, abstract, kw_text, req, flags, domain, slice_name="", strict_once=False,
           flag_excludes=False):
    """Return (decision, score, reason). Rules v3 (Stage 2), calibrated on the 202 Stage 1
    manual decisions so that borderline cases stay under 25% per theme.

    req[0] is the core concept, req[1:] context terms (see queries.yaml header)."""
    core, context = req[0], req[1:]
    full = f"{title} {abstract}"
    has_abs = bool(abstract)
    core_title = bool(core.search(title))
    core_rest = len(core.findall(abstract))
    kw_core = bool(core.search(kw_text))
    score = 3 * core_title + min(core_rest, 3)
    if not core_title and core_rest == 0:
        # (a record without an abstract in the API record matched an abstract OpenAlex holds but
        # does not distribute, e.g. Elsevier; in A1/A2 landmarks 35 of 35 such records were
        # off-topic, so they are excluded too)
        return "exclude", 0, "core concept missing"
    ctx_ok = all(r.search(full) for r in context)
    if not ctx_ok and domain == "C" and names_city(full):
        # C themes: a named city counts as the urban context term
        ctx_ok = all(r.search(full) for r in context[1:])
    flagged = [f.pattern[:40] for f in flags if f.search(full)]
    if flagged:
        if core_title and not flag_excludes:
            return "borderline", score, "flag: " + flagged[0]
        return "exclude", score, "flag, core not in title: " + flagged[0]
    if not has_abs:
        if ctx_ok:
            return "include", score, "no abstract; core (and context) in title"
        if domain != "C":
            return "include", score, "no abstract; core in title; context terms missing"
        return "exclude", score, "no abstract; no urban context (C theme)"
    if len(abstract) < 250 or re.search(r"^\W*\"?[^.]{5,200}\"?\s*,?\s*\d+\s*\(\d+\),?\s*pp?\.", abstract):
        if core_title:
            return "borderline", score, "stub abstract (possible book review)"
        return "exclude", score, "stub abstract, core not in title"
    if not ctx_ok:
        if core_title and domain != "C":
            return "include", score, "core in title; context terms missing"
        # C themes: a work with no urban term (and no named city) belongs to the digital-only
        # B themes; in A/B themes a core term only in the abstract is not enough without context
        return "exclude", score, "context terms missing"
    if not core_title and core_rest < 2:
        if kw_core and strict_once:
            # per-theme tightening (queries.yaml screen.strict_once): the single mention must
            # be in the opening two sentences or in a sentence stating the work's aim
            ss = sentences(abstract)
            pos = next((i for i, x in enumerate(ss) if core.search(x)), -1)
            if not (0 <= pos <= 1 or (pos >= 0 and AIM.search(ss[pos]))):
                return "exclude", score, "core mentioned once, outside opening/aim (strict)"
        if kw_core:
            return "borderline", score, "core concept mentioned once"
        return "exclude", score, "core mentioned once, not in keyword tags"
    return "include", score, "rules"


def confidence(reason, has_abs, manual):
    if not has_abs:
        return "low"
    if manual:
        return "medium"
    if reason == "rules":
        return "high"
    return "medium"


REPO_PREFIXES = ("10.5281/", "10.6084/", "10.17605/", "10.31219/", "10.31235/", "10.2139/",
                 "10.48550/", "10.20944/", "10.21203/", "10.22541/", "10.13140/", "10.31234/",
                 "10.35542/", "10.1101/", "10.32388/", "10.5061/")
REPO_NAME = re.compile(r"zenodo|figshare|ssrn|repositor|eprints|research online|dspace|"
                       r"repositorio|\bhal\b|e-theses|arxiv|preprints|research square|osf|"
                       r"socarxiv|researchgate|academia\.edu|digital commons|scholarworks", re.I)


def is_repository(w) -> bool:
    """A record held only in a repository / preprint server (no journal, book or conference
    version as its primary location)."""
    src = (w.get("primary_location") or {}).get("source") or {}
    doi = (w.get("doi") or "").lower().replace("https://doi.org/", "")
    if src.get("type") == "repository" or doi.startswith(REPO_PREFIXES):
        return True
    if w.get("type") == "preprint":
        return True
    return bool(src.get("display_name") and REPO_NAME.search(src["display_name"])
                and src.get("type") not in ("journal", "book series", "conference"))


def load_manual():
    p = SCREEN / "manual_review.csv"
    if not p.exists():
        return {}
    with p.open() as f:
        return {(r["openalex_id"], r["theme"]): r for r in csv.DictReader(f)}


# --------------------------------------------------------------------------- main
def theme_cfg(cfg, t):
    """Main themes (A1..C18) and supplementary query sets (S1..) share one config shape."""
    return cfg["themes"].get(t) or cfg["supplementary"][t]


def compile_cfg(cfg, t):
    sc = theme_cfg(cfg, t).get("screen", {})
    req = [re.compile(r, re.I) for r in sc.get("require", [])]
    glob = [] if sc.get("skip_global_flags") else cfg.get("global_flags", [])
    flags = [re.compile(r, re.I) for r in glob + sc.get("flag", [])]
    return req, flags


def shared_abstracts():
    """IDs of works whose abstract is also attached to a work with a clearly different title
    (e.g. one 2020s platform-work abstract on several 1980s Annual Review articles)."""
    import difflib
    by_abs = defaultdict(dict)
    for man in sorted((RAW / "searches").glob("*_*.json")):
        if man.name.startswith("_"):
            continue
        for wid, _ in json.loads(man.read_text())["results"]:
            w = load_work(wid)
            a = abstract_text(w)
            if len(a) >= 200:
                by_abs[a[:300]][wid] = norm_title(w.get("title") or "")
    bad = set()
    for works in by_abs.values():
        if len(works) < 2:
            continue
        items = list(works.items())
        for i, (w1, t1) in enumerate(items):
            for w2, t2 in items[i + 1:]:
                if t1 and t2 and (t1 in t2 or t2 in t1):
                    continue  # same work with and without subtitle
                if difflib.SequenceMatcher(None, t1, t2).ratio() < 0.6:
                    bad.update((w1, w2))
    return bad


def main(themes_wanted):
    cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
    idcheck = json.loads((RAW / "searches" / "_id_check.json").read_text())
    manual = load_manual()
    cands = []
    shared = shared_abstracts()
    for man in sorted((RAW / "searches").glob("*_*.json")):
        if man.name.startswith("_"):
            continue
        m = json.loads(man.read_text())
        t = m["theme"]
        if themes_wanted and t not in themes_wanted:
            continue
        stage2 = m.get("stage") == "stage2"
        req, flags = compile_cfg(cfg, t)
        domain = theme_cfg(cfg, t).get("domain", "S")
        for rank, (wid, _) in enumerate(m["results"], 1):
            w = load_work(wid)
            title = w.get("title") or w.get("display_name") or ""
            abstract = abstract_text(w)
            if wid in shared:
                # the same abstract is attached to works with different titles: an OpenAlex
                # metadata error, so the work is screened on its title alone
                abstract = ""
            kw = "; ".join(k["display_name"] for k in (w.get("keywords") or []))
            full = f"{title} {abstract} {kw}"
            c = dict(openalex_id=wid, theme=t, slice=m["slice"], manifest=man.stem, rank=rank,
                     title=title, year=w.get("publication_year"), type=w.get("type"),
                     cited_by=w.get("cited_by_count", 0), has_abstract=bool(abstract))
            if not stage2 and idcheck.get(wid) != "ok":
                c.update(decision="exclude", score=0, reason=f"id check {idcheck.get(wid)}")
            elif w.get("is_retracted"):
                c.update(decision="exclude", score=0, reason="retracted")
            elif w.get("type") in EXCLUDED_TYPES:
                c.update(decision="exclude", score=0, reason=f"type {w.get('type')}")
            else:
                # OpenAlex keyword tags are not used as evidence of relevance on their own: in
                # testing they attached e.g. "digital identity" to education papers. They only
                # decide whether a single core mention goes to review or is excluded.
                sc_cfg = theme_cfg(cfg, t)["screen"]
                d, sc_, r = screen(title, abstract, kw, req, flags, domain, m["slice"],
                                   sc_cfg.get("strict_once", False),
                                   sc_cfg.get("flag_excludes", False))
                c.update(decision=d, score=sc_, reason=r)
            c["final"] = c["decision"]
            c["rule_reason"] = c["reason"]
            mr = manual.get((wid, t))
            if c["decision"] == "borderline":
                c["final"] = mr["decision"] if mr else "pending"
                c["reason"] += f" | manual: {mr['note']}" if mr and mr.get("note") else ""
            elif mr and not c["reason"].startswith(("id check", "retracted", "type ")):
                # a hand decision on this work-theme pair (made when an earlier rule version
                # sent it to review) overrides the current rules
                c["final"] = mr["decision"]
                c["reason"] += f" | manual override: {mr.get('note', '')}"
            c["_w"], c["_abs"], c["_full"] = w, abstract, full
            cands.append(c)

    OUT.mkdir(parents=True, exist_ok=True)
    cols = ["openalex_id", "theme", "slice", "manifest", "rank", "title", "year", "type",
            "cited_by", "has_abstract", "decision", "score", "reason", "final"]
    with (OUT / "candidates.csv").open("w", newline="") as f:
        wr = csv.DictWriter(f, cols, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(cands)
    pend = [c for c in cands if c["final"] == "pending"]
    seen = set()
    with (OUT / "pending_review.csv").open("w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["openalex_id", "theme", "reason", "title", "year", "type", "abstract"])
        for c in pend:
            if (c["openalex_id"], c["theme"]) in seen:
                continue
            seen.add((c["openalex_id"], c["theme"]))
            wr.writerow([c["openalex_id"], c["theme"], c["reason"], c["title"], c["year"],
                         c["type"], c["_abs"][:900]])

    # ---- screening statistics per theme (unique work-theme pairs; first decision wins)
    pair = {}
    for c in cands:
        pair.setdefault((c["openalex_id"], c["theme"]), c)
    stats = defaultdict(lambda: defaultdict(int))
    for (wid, t), c in pair.items():
        st = stats[t]
        st["candidates"] += 1
        st[c["decision"]] += 1
        if c["decision"] == "borderline":
            st["manual_" + c["final"]] += 1
    with (OUT / "screening_stats.csv").open("w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["theme", "candidates", "include_rules", "borderline", "exclude",
                     "borderline_share", "manual_kept", "manual_dropped", "pending"])
        for t in sorted(stats, key=lambda x: (x[0], int(x[1:]))):
            st = stats[t]
            wr.writerow([t, st["candidates"], st["include"], st["borderline"], st["exclude"],
                         f"{st['borderline'] / st['candidates']:.3f}", st["manual_include"],
                         st["manual_exclude"], st["manual_pending"]])

    # ---- merge kept candidates by work, then deduplicate by DOI and normalised title
    kept = [c for c in cands if c["final"] == "include"]
    by_work = defaultdict(list)
    for c in kept:
        by_work[c["openalex_id"]].append(c)

    def quality(wid):
        w = by_work[wid][0]["_w"]
        return (bool(w.get("doi")) and not is_repository(w), w.get("cited_by_count", 0),
                -int(wid[1:]))

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

    supp_names = {k: v["name"] for k, v in (cfg.get("supplementary") or {}).items()}
    records = []
    for k, members in groups.items():
        w = by_work[k][0]["_w"]
        allc = [c for wid in members for c in by_work[wid]]
        mainc = [c for c in allc if c["theme"] in cfg["themes"]]
        suppc = [c for c in allc if c["theme"] not in cfg["themes"]]
        theme_score, theme_hits = defaultdict(int), defaultdict(int)
        for c in mainc:
            theme_score[c["theme"]] = max(theme_score[c["theme"]], c["score"])
            theme_hits[c["theme"]] += 1
        if mainc:
            ranked = sorted(theme_score, key=lambda t: (-theme_score[t], -theme_hits[t],
                                                        t[0], int(t[1:])))
        else:  # found only by the supplementary query set: home theme of that query
            ranked = []
            for c in suppc:
                h = cfg["supplementary"][c["theme"]]["home_theme"]
                if h not in ranked:
                    ranked.append(h)
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
        prim_c = [c for c in allc if c["theme"] == primary] or allc
        manual_kept = all(c["decision"] == "borderline" or "manual override" in c["reason"]
                          for c in prim_c)
        reason = next((c["rule_reason"] for c in prim_c if c["decision"] == "include"),
                      prim_c[0]["rule_reason"])
        conf = confidence(reason, bool(abstract), manual_kept)
        repo_only = all(is_repository(by_work[m_][0]["_w"]) for m_ in members)
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
            "Landmark flag": "Y" if any(c["slice"] == "landmarks" for c in mainc)
                                    and not repo_only else "",
            "Emerging flag": "Y" if (w.get("publication_year") or 0) >= 2022
                                    and (w.get("fwci") or 0) >= 1.5 else "",
            "One-line summary": summary(abstract),
            "Stated gaps": stated_gaps(abstract),
            "Shortlist tag": shortlist_tag(text, haryana),
            "Screening confidence": conf,
            "Repository-only": "Y" if repo_only else "",
            "Supplementary": "Y" if not mainc else "",
            "Supplementary query": "; ".join(sorted({f"{c['theme']} {supp_names[c['theme']]}"
                                                     for c in suppc})),
            "C4 orientation": c4_orientation(text) if primary == "C4" else "",
            "Found in": "; ".join(slices),
            "Duplicates merged": "; ".join(m_ for m_ in members if m_ != k),
            "FWCI": w.get("fwci"),
        }
        records.append(rec)
    records.sort(key=lambda r: (r["Primary theme"][0], int(r["Primary theme"][1:]),
                                -(r["Cited-by count"] or 0)))
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


C4_CRITICAL = re.compile(r"\b(critic\w*|critique|politic\w*|power|governance|epistem\w*|social|"
                         r"justice|ethic\w*|citizen\w*|neoliberal\w*|discours\w*|imaginar\w*)\b", re.I)


def c4_orientation(text):
    """C4 urban informatics: 'critical' when the abstract engages politics/power/society,
    otherwise 'technical' (BRIEF §1 asks for the tag)."""
    return "critical" if len(C4_CRITICAL.findall(text)) >= 2 else "technical"


if __name__ == "__main__":
    main(set(sys.argv[1:]))
