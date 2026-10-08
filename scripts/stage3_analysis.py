"""Stage 3 tables and the rendered report (BRIEF §5-6). No API calls.

Usage: python3 scripts/stage3_analysis.py

Claims about gaps, growth and mismatch rest on OpenAlex-wide population counts
(data/processed/population_counts.csv, precision-adjusted as in the Growth tab); the map's
records are used only as examples, for landmarks and for method shares (OpenAlex has no method
field). The sample's region and period mix is set by the design (India and recent slices), so
record counts per region or period are never read as gaps.

Inputs : data/processed/records.json, population_counts.csv, population_baselines.json,
         emerging_terms.csv, coverage_limits.csv, data/analysis/candidate_gaps.yaml,
         data/analysis/report_choices.yaml, scripts/report_template.md
Outputs: data/processed/theme_metrics.csv     per-theme metrics derived from population counts
         data/processed/method_shares.csv     method shares among records with a known method
         data/processed/candidate_gaps.csv    the 25 candidate gaps with evidence and examples
         data/processed/landmarks_report.csv  landmark works cited in the report
         outputs/REPORT.md                    rendered from scripts/report_template.md

Template placeholders: {{v:T.field}} a metric (T = theme code or SS for the Social Sciences
baseline; missing values print as 'pending'), {{cite:W123}} a record ("Author (Year) [LM…]"),
{{stat:name}}, {{table:name}}, {{gaps:scope}}.
"""
from __future__ import annotations

import csv
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
ANA = ROOT / "data" / "analysis"
METHODS = ["qualitative", "quantitative", "mixed", "review", "conceptual", "computational"]
REGION_KEYS = ["sa", "gn", "ea", "sea", "af", "la", "me"]
REGION_NAMES = {"sa": "South Asia", "gn": "Global North", "ea": "China & East Asia",
                "sea": "Southeast Asia", "af": "Africa", "la": "Latin America",
                "me": "Middle East"}
MIN_KNOWN = 50          # no method claim below this many records with a known method
NEW_BELOW = 50          # growth ratio shown as 'new' when the adjusted 2015-19 count is below this
COVERAGE_CAVEAT = (
    "Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, "
    "and has Shodhganga theses only to 2021, almost all without abstracts and outside the "
    "count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before "
    "relying on this.")
SA_NOTE = "The Indian-venue coverage limits (Coverage limits table) apply here too."

recs_all = json.loads((PROC / "records.json").read_text())
recs = [r for r in recs_all if r["Supplementary"] != "Y"]
by_oa = {}
for r in recs_all:
    by_oa[r["OpenAlex ID"]] = r
    for d in (r["Duplicates merged"] or "").split("; "):
        if d:
            by_oa.setdefault(d, r)
cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
THEMES = list(cfg["themes"])
choices = yaml.safe_load((ANA / "report_choices.yaml").read_text())


def num(v):
    if v in ("", None):
        return None
    try:
        return float(v)
    except ValueError:
        return None


# ------------------------------------------------------------------ theme metrics
pop = {r["theme"]: r for r in csv.DictReader((PROC / "population_counts.csv").open())}
base = json.loads((PROC / "population_baselines.json").read_text())


def bsum(key, yrs):
    d = base["per_year"].get(key)
    return sum(d.get(str(y), 0) for y in yrs) if d else None


Y1519, Y2026, YALL = range(2015, 2020), range(2020, 2027), range(2010, 2027)
M = defaultdict(dict)   # M[theme][field] = value
for v in ("all", "core"):
    g, s = bsum(f"global_{v}", Y2026), bsum(f"sa_{v}", Y2026)
    i = bsum(f"india_{v}", Y2026)
    M["SS"][f"sa_share_{v}_2020-26"] = 100 * s / g if g and s else None
    M["SS"][f"india_share_{v}_2020-26"] = 100 * i / g if g and i else None
    M["SS"][f"global_{v}_2020-26"] = g
for t in THEMES:
    p = pop[t]
    m = M[t]
    m["name"] = cfg["themes"][t]["name"]
    m["domain"] = t[0]
    for k in p:
        if k not in ("theme", "name"):
            m[k] = num(p[k])
    for v in ("all", "core"):
        g26, g15 = m.get(f"global_{v}_2020-26_adj"), m.get(f"global_{v}_2015-19_adj")
        gr = m.get(f"global_{v}_growth")
        m[f"global_{v}_growth_label"] = (None if g15 is None or g26 is None else
                                         "new" if g15 < NEW_BELOW else gr)
        for sc in ("sa", "india"):
            x = m.get(f"{sc}_{v}_2020-26_adj")
            m[f"{sc}_share_{v}_2020-26"] = 100 * x / g26 if x is not None and g26 else None
            b = M["SS"].get(f"{sc}_share_{v}_2020-26")
            sh = m[f"{sc}_share_{v}_2020-26"]
            m[f"lq_{sc}_{v}_2020-26"] = sh / b if sh is not None and b else None
    # region shares among region mentions, 2010-26, all venues (adjusted)
    tot = {}
    sa_all = sum(m.get(f"sa_all_{pn}_adj") or 0 for pn in ("2010-14", "2015-19", "2020-26"))
    tot["sa"] = sa_all if m.get("sa_all_2020-26_adj") is not None else None
    for k in REGION_KEYS[1:]:
        tot[k] = m.get(f"{k}_all_2010-26_adj")
    if all(tot[k] is not None for k in REGION_KEYS):
        s = sum(tot.values())
        for k in REGION_KEYS:
            m[f"{k}_share_of_region_mentions"] = 100 * tot[k] / s if s else None
        m["top_region"] = REGION_NAMES[max(tot, key=tot.get)]
    else:
        for k in REGION_KEYS:
            m[f"{k}_share_of_region_mentions"] = None
        m["top_region"] = None
    m["c18_low_precision"] = m["p"] is not None and m["p"] < 0.2

# flags (population-based)
for t in THEMES:
    m = M[t]
    gl = m["global_all_growth_label"]
    m["fast_growth"] = gl == "new" or (gl is not None and gl >= 3)
    m["saturating"] = (gl not in (None, "new") and gl <= 1.3
                       and (m["global_all_2020-26_adj"] or 0) >= 2000)
    m["flat_small"] = (gl not in (None, "new") and gl <= 1.3
                       and (m["global_all_2020-26_adj"] or 0) < 2000)
    sh = m["sa_share_all_2020-26"]
    m["sa_thin"] = sh is not None and sh <= 5.0
    m["mismatch_sa"] = m["fast_growth"] and m["sa_thin"]
    gs = m["gn_share_of_region_mentions"]
    m["gn_dominated"] = gs is not None and gs >= 50

# method shares (sample)
for t in THEMES + ["ALL", "A", "B", "C", "IN_A", "IN_B", "IN_C", "GN_A", "GN_B", "GN_C", "IN"]:
    if t in THEMES:
        rs = [r for r in recs if r["Primary theme"] == t]
    elif t == "ALL":
        rs = recs
    elif t in "ABC":
        rs = [r for r in recs if r["Domain"] == t]
    elif t == "IN":
        rs = [r for r in recs if r["India flag"] == "Y"]
    elif t.startswith("IN_"):
        rs = [r for r in recs if r["Domain"] == t[-1] and r["India flag"] == "Y"]
    else:
        rs = [r for r in recs if r["Domain"] == t[-1] and r["Region"] == "Global North"]
    c = Counter(r["Method"] for r in rs)
    known = sum(c[x] for x in METHODS)
    mm = M[t]
    mm["records_n"] = len(rs)
    mm["method_known_n"] = known
    mm["method_claims_allowed"] = known >= MIN_KNOWN
    for x in METHODS:
        mm[f"method_{x}_pct"] = 100 * c[x] / known if known else None

with (PROC / "theme_metrics.csv").open("w", newline="") as fh:
    cols = ["theme", "name", "p", "p_sa", "records_n", "global_all_2015-19_adj",
            "global_all_2020-26_adj", "global_all_2015-19_per10k", "global_all_2020-26_per10k",
            "global_all_growth_label", "global_core_2015-19_adj", "global_core_2020-26_adj",
            "global_core_growth_label", "sa_all_2020-26_adj", "sa_share_all_2020-26",
            "lq_sa_all_2020-26", "sa_all_growth", "sa_core_2020-26_adj", "sa_share_core_2020-26",
            "lq_sa_core_2020-26", "india_all_2020-26_adj", "india_share_all_2020-26",
            "lq_india_all_2020-26", "india_core_2020-26_adj", "india_share_core_2020-26",
            "delhi_all_2010-26_adj", "delhi_core_2010-26_adj", "haryana_all_2010-26_adj",
            "haryana_core_2010-26_adj"] + \
        [f"{k}_share_of_region_mentions" for k in REGION_KEYS] + \
        ["top_region", "fast_growth", "saturating", "flat_small", "sa_thin", "mismatch_sa",
         "gn_dominated", "method_known_n", "method_claims_allowed"] + \
        [f"method_{x}_pct" for x in METHODS]
    w = csv.writer(fh)
    w.writerow(cols)
    for t in THEMES:
        row = [t] + [M[t].get(c) for c in cols[1:]]
        w.writerow(["" if x is None else round(x, 3) if isinstance(x, float) else
                    "Y" if x is True else "" if x is False else x for x in row])

with (PROC / "method_shares.csv").open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["group", "records_n", "method_known_n", "claims_allowed (known >= 50)"]
               + [f"{x}_pct_of_known" for x in METHODS])
    for t in THEMES + ["ALL", "A", "B", "C", "IN", "IN_A", "IN_B", "IN_C", "GN_A", "GN_B", "GN_C"]:
        mm = M[t]
        w.writerow([t, mm["records_n"], mm["method_known_n"],
                    "Y" if mm["method_claims_allowed"] else "N"]
                   + [round(mm[f"method_{x}_pct"], 1) if mm[f"method_{x}_pct"] is not None
                      else "" for x in METHODS])


# ------------------------------------------------------------------ formatting helpers
def fmt(v, field=""):
    if v is None or v == "":
        return "pending"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, str):
        return v
    if "pct" in field or "share" in field:
        return f"{v:.1f}%"
    if field.startswith("lq") or field in ("p", "p_sa") or "growth" in field or "per10k" in field:
        return f"{v:.2f}"
    if float(v).is_integer() or abs(v) >= 100:
        return f"{round(v):,}"
    return f"{v:.2f}"


PARTICLES = {"van", "von", "de", "da", "del", "der", "di", "du", "le", "la", "dos", "das"}


def surname(full):
    full = full.strip()
    if not full:
        return ""
    if full.isupper():
        full = full.title()
    parts = full.split()
    s = parts[-1]
    if len(parts) > 2 and parts[-2].lower() in PARTICLES:
        s = parts[-2] + " " + s
    return s


def cite(r):
    au = [a for a in (r["Authors"] or "").split("; ") if re.search(r"[A-Za-z]{2}", a)]
    if not au:
        who = "“" + " ".join(r["Title"].split()[:5]) + "…”"
    elif len(au) == 1:
        who = surname(au[0])
    elif len(au) == 2:
        who = f"{surname(au[0])} & {surname(au[1])}"
    else:
        who = f"{surname(au[0])} et al."
    return f"{who} ({r['Year']}) [{r['ID']}]"


def cite_long(r, n=5):
    words = r["Title"].split()
    short = " ".join(words[:n]) + ("…" if len(words) > n else "")
    return f"{cite(r)}, *{short}*"


# ------------------------------------------------------------------ landmarks for the report
skip = set(choices.get("landmark_skip", {}))


def twords(title):
    w = re.sub(r"[^a-z ]", " ", title.lower()).split()
    return [x for x in w if x not in ("the", "a", "an")]


def same_work(a, b):
    """Two records of one work: one title is a word-prefix of the other (book vs. article
    versions, reviews titled after the book)."""
    x, y = twords(a), twords(b)
    n = min(len(x), len(y))
    return n >= 2 and x[:n] == y[:n]


LM = {}
for t in THEMES:
    cand = sorted([r for r in recs if r["Primary theme"] == t and r["Landmark flag"] == "Y"
                   and r["OpenAlex ID"] not in skip],
                  key=lambda r: -(r["Cited-by count"] or 0))
    out = []
    for r in cand:
        if any(same_work(r["Title"], o["Title"]) for o in out):
            continue
        out.append(r)
        if len(out) == 3:
            break
    LM[t] = out
with (PROC / "landmarks_report.csv").open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["theme", "rank", "ID", "OpenAlex ID", "cited_by", "citation", "title"])
    for t in THEMES:
        for i, r in enumerate(LM[t], 1):
            w.writerow([t, i, r["ID"], r["OpenAlex ID"], r["Cited-by count"], cite(r), r["Title"]])

# ------------------------------------------------------------------ candidate gaps
GAPS = yaml.safe_load((ANA / "candidate_gaps.yaml").read_text())
SCOPE_FILTER = {
    "any": lambda r: True,
    "sa": lambda r: r["Region"] == "South Asia" or r["India flag"] == "Y",
    "india": lambda r: r["India flag"] == "Y",
    "delhi": lambda r: r["Delhi/NCR flag"] == "Y",
    "haryana": lambda r: r["Haryana flag"] == "Y",
    "gn": lambda r: r["Region"] == "Global North",
}


def examples(spec):
    pins = [by_oa[w] for w in spec.get("pin", []) if w in by_oa]
    themes = set(spec.get("themes", []))
    f = SCOPE_FILTER[spec.get("filter", "any")]
    rx = re.compile(spec["regex"], re.I) if spec.get("regex") else None
    meth = spec.get("method")
    pool = [r for r in recs_all
            if (not themes or r["Primary theme"] in themes or r["Secondary theme"] in themes
                or {x.split(" ")[0] for x in (r["Supplementary query"] or "").split("; ")} & themes)
            and f(r) and (rx is None or rx.search(r["Title"] + " " + r["One-line summary"]))
            and (meth is None or r["Method"] == meth)
            and r["OpenAlex ID"] not in spec.get("pin", []) and r["OpenAlex ID"] not in skip]
    if spec.get("sort") == "recent":
        pool.sort(key=lambda r: (-(r["Year"] or 0), -(r["Cited-by count"] or 0)))
    else:
        pool.sort(key=lambda r: -(r["Cited-by count"] or 0))
    out = []
    for r in pins + pool:
        fa = (r["Authors"] or "").split(";")[0]
        if any(same_work(r["Title"], o["Title"]) or (fa and fa == (o["Authors"] or "").split(";")[0])
               for o in out):
            continue
        out.append(r)
        if len(out) == spec.get("n", 3):
            break
    return out, len(pool) + len(pins)


def render_values(text):
    def v(mo):
        t, field = mo.group(1), mo.group(2)
        return fmt(M[t].get(field), field)

    def rank(mo):
        t, field, grp = mo.group(1), mo.group(2), mo.group(3)
        ts = [x for x in THEMES if grp == "all" or x[0] == t[0]]
        vals = sorted((M[x].get(field), x) for x in ts if isinstance(M[x].get(field), float))
        if t not in [x for _, x in vals]:
            return "rank pending"
        k = [x for _, x in vals].index(t) + 1
        dom = {"A": "urban (A)", "B": "digital-society (B)", "C": "urban × digital (C)"}[t[0]]
        what = f"all {len(vals)} themes" if grp == "all" else f"the {len(vals)} {dom} themes"
        nth = {1: "", 2: "second-", 3: "third-", 4: "fourth-", 5: "fifth-", 6: "sixth-",
               7: "seventh-", 8: "eighth-", 9: "ninth-", 10: "tenth-"}.get(k, f"{k}th-")
        return f"the {nth}lowest of {what}"

    text = re.sub(r"\{\{rank:([A-C]\d+)\.([\w\-]+):(dom|all)\}\}", rank, text)
    text = re.sub(r"\{\{v:([A-Z]+\d*|SS|ALL|IN|IN_[ABC]|GN_[ABC])\.([\w\-]+)\}\}", v, text)
    text = re.sub(r"\{\{cite:(W\d+)\}\}",
                  lambda mo: cite(by_oa[mo.group(1)]) if mo.group(1) in by_oa
                  else f"[{mo.group(1)} not in map]", text)
    return text


gap_rows = []
for g in GAPS:
    ex, pool_n = examples(g["examples"])
    caveat = g.get("caveat", "").strip()
    if g["scope"] in ("india", "delhi_haryana"):
        caveat = (caveat + " " if caveat else "") + COVERAGE_CAVEAT
    elif g["scope"] == "south_asia":
        caveat = (caveat + " " if caveat else "") + SA_NOTE
    gap_rows.append({
        "id": g["id"], "scope": g["scope"], "themes": " ".join(g["themes"]),
        "title": g["title"], "evidence": render_values(" ".join(g["evidence"].split())),
        "missing": " ".join(g["missing"].split()), "caveat": " ".join(caveat.split()),
        "examples": "; ".join(cite_long(r) for r in ex),
        "example_ids": " ".join(r["ID"] for r in ex),
        "matching_records_in_map": pool_n,
        "status": g.get("status", ""),
    })
with (PROC / "candidate_gaps.csv").open("w", newline="") as fh:
    w = csv.DictWriter(fh, list(gap_rows[0]))
    w.writeheader()
    w.writerows(gap_rows)


def gaps_md(scope):
    out = []
    for g in gap_rows:
        if g["scope"] != scope:
            continue
        st = f" *({g['status']})*" if g["status"] else ""
        out.append(f"**{g['id']}. {g['title']}**{st} ({g['themes']})  \n"
                   f"*Evidence.* {g['evidence']}  \n"
                   f"*Examples* ({g['matching_records_in_map']} matching records in the map): "
                   f"{g['examples'] or 'none'}.  \n"
                   f"*Missing.* {g['missing']}  \n"
                   f"*Caveat.* {g['caveat']}\n")
    return "\n".join(out)


# ------------------------------------------------------------------ tables
def t_landmarks():
    rows = ["| Theme | Landmark works (most cited in the map; full list in the Landmarks tab) |",
            "|---|---|"]
    for t in THEMES:
        rows.append(f"| {t} {cfg['themes'][t]['name']} | "
                    + "; ".join(cite(r) for r in LM[t][:2]) + " |")
    return "\n".join(rows)


def t_growth(ts, extra=()):
    rows = ["| Theme | Adj. works 2020–26 (all venues) | Per 10k SS 2015–19 → 2020–26 | "
            "Growth (all) | Growth (core venues) | SA share 2020–26 | SA LQ 2020–26 |"
            + "".join(f" {h} |" for h, _ in extra),
            "|---|---:|---:|---:|---:|---:|---:|" + "---:|" * len(extra)]
    for t in ts:
        m = M[t]
        rows.append(
            f"| {t} {m['name']} | {fmt(m['global_all_2020-26_adj'])} | "
            f"{fmt(m['global_all_2015-19_per10k'], 'per10k')} → "
            f"{fmt(m['global_all_2020-26_per10k'], 'per10k')} | "
            f"{fmt(m['global_all_growth_label'], 'growth')} | "
            f"{fmt(m['global_core_growth_label'], 'growth')} | "
            f"{fmt(m['sa_share_all_2020-26'], 'share')} | {fmt(m['lq_sa_all_2020-26'], 'lq')} |"
            + "".join(f" {fmt(m.get(f), f)} |" for _, f in extra))
    return "\n".join(rows)


def growth_sorted():
    def k(t):
        gl = M[t]["global_all_growth_label"]
        return 1e9 if gl == "new" else (gl or 0)
    return sorted(THEMES, key=k, reverse=True)


def t_fast():
    return t_growth([t for t in growth_sorted() if M[t]["fast_growth"]])


def t_saturating():
    return t_growth([t for t in growth_sorted()[::-1] if M[t]["saturating"] or M[t]["flat_small"]])


def t_mismatch():
    ts = sorted([t for t in THEMES if M[t]["sa_thin"]],
                key=lambda t: M[t]["sa_share_all_2020-26"])
    return t_growth(ts, extra=(("India share 2020–26", "india_share_all_2020-26"),))


def t_gn():
    rows = ["| Theme | " + " | ".join(REGION_NAMES[k] for k in REGION_KEYS) + " |",
            "|---|" + "---:|" * len(REGION_KEYS)]
    ts = [t for t in THEMES if M[t]["gn_share_of_region_mentions"] is not None]
    if not ts:
        return ("*Pending: region counts (Global North, China & East Asia, Southeast Asia, "
                "Africa, Latin America, Middle East) are fetched with the population counts "
                "after the OpenAlex budget resets.*")
    ts.sort(key=lambda t: -M[t]["gn_share_of_region_mentions"])
    for t in ts:
        rows.append(f"| {t} {M[t]['name']} | " + " | ".join(
            fmt(M[t][f"{k}_share_of_region_mentions"], "share") for k in REGION_KEYS) + " |")
    return "\n".join(rows)


def t_methods():
    rows = ["| Group | Records | Known method (n) | " + " | ".join(x.capitalize() for x in METHODS)
            + " |", "|---|---:|---:|" + "---:|" * len(METHODS)]
    for t in THEMES + ["A", "B", "C", "IN_A", "IN_B", "IN_C", "GN_A", "GN_B", "GN_C"]:
        mm = M[t]
        label = (f"{t} {cfg['themes'][t]['name']}" if t in THEMES else
                 {"A": "Domain A (all)", "B": "Domain B (all)", "C": "Domain C (all)",
                  "IN_A": "A, India-flagged", "IN_B": "B, India-flagged",
                  "IN_C": "C, India-flagged", "GN_A": "A, Global North",
                  "GN_B": "B, Global North", "GN_C": "C, Global North"}[t])
        if not mm["method_claims_allowed"]:
            label += " (n < 50: no method claim)"
        rows.append(f"| {label} | {mm['records_n']} | {mm['method_known_n']} | " + " | ".join(
            f"{mm[f'method_{x}_pct']:.0f}%" if mm[f"method_{x}_pct"] is not None else "–"
            for x in METHODS) + " |")
    return "\n".join(rows)


def t_emerging():
    em = list(csv.DictReader((PROC / "emerging_terms.csv").open()))[:30]
    rows = ["| # | Term | Records 2018–21 → 2022–26 | Share of period's records | Share ratio | "
            "OpenAlex-wide SS share ratio | Example (2022–24, highest FWCI) |",
            "|---:|---|---:|---:|---:|---:|---|"]
    for e in em:
        exid = (e["example_1"] or "").split(" ")[0]
        ex = next((r for r in recs_all if r["ID"] == exid), None)
        rows.append(f"| {e['rank']} | {e['term']} | {e['records_2018_21']} → {e['records_2022_26']}"
                    f" | {e['share_2018_21_pct']}% → {e['share_2022_26_pct']}% | ×{e['share_ratio']}"
                    f" | {'new' if e['oa_share_ratio'] == 'new' else '×' + e['oa_share_ratio']} | "
                    f"{cite(ex) if ex else ''} |")
    return "\n".join(rows)


def t_coverage():
    rows = ["| Venue | OpenAlex works (all) | Years held | Map records |", "|---|---:|---|---:|"]
    for r in csv.DictReader((PROC / "coverage_limits.csv").open()):
        yrs = [int(k) for k, v in r.items() if k.isdigit() and v not in ("", "0")]
        held = (f"{min(yrs)}–{max(yrs)}" if yrs else "–")
        if r.get("before_2010") not in ("", "0", None):
            held = f"before 2010 ({int(r['before_2010']):,}); " + held
        rows.append(f"| {r['venue']} | {int(r['total_all']):,} | {held} | {r['records_in_map']} |"
                    if r["total_all"] else f"| {r['venue']} | – | no OpenAlex source | – |")
    return "\n".join(rows)


def t_intersections():
    rows = ["| Urban × digital theme | Adj. works 2020–26 | Digital parent | Adj. works | "
            "Urban parent | Adj. works | C as % of digital parent |",
            "|---|---:|---|---:|---|---:|---:|"]
    for c, (b, a) in choices["parents"].items():
        mc, mb, ma = M[c], M[b], M[a]
        pct = 100 * mc["global_all_2020-26_adj"] / mb["global_all_2020-26_adj"]
        rows.append(f"| {c} {mc['name']} | {fmt(mc['global_all_2020-26_adj'])} | {b} {mb['name']} | "
                    f"{fmt(mb['global_all_2020-26_adj'])} | {a} {ma['name']} | "
                    f"{fmt(ma['global_all_2020-26_adj'])} | {pct:.0f}% |")
    return "\n".join(rows)


def t_methods_compact():
    rows = ["| Group | Records | Known method (n) | " + " | ".join(x.capitalize() for x in METHODS)
            + " |", "|---|---:|---:|" + "---:|" * len(METHODS)]
    for t in ["A", "B", "C", "IN_A", "GN_A", "IN_B", "GN_B", "IN_C", "GN_C"]:
        mm = M[t]
        label = {"A": "Domain A (all records)", "B": "Domain B (all records)",
                 "C": "Domain C (all records)", "IN_A": "A, India-flagged",
                 "IN_B": "B, India-flagged", "IN_C": "C, India-flagged",
                 "GN_A": "A, Global North", "GN_B": "B, Global North", "GN_C": "C, Global North"}[t]
        rows.append(f"| {label} | {mm['records_n']} | {mm['method_known_n']} | " + " | ".join(
            f"{mm[f'method_{x}_pct']:.0f}%" for x in METHODS) + " |")
    return "\n".join(rows)


TABLES = {"intersections": t_intersections, "methods_compact": t_methods_compact,
          "landmarks": t_landmarks, "fast": t_fast, "saturating": t_saturating,
          "mismatch": t_mismatch, "gn": t_gn, "methods": t_methods, "emerging": t_emerging,
          "coverage": t_coverage}

# ------------------------------------------------------------------ stats
pk = [M[t]["p"] for t in THEMES]
STATS = {
    "records": f"{len(recs_all):,}",
    "records_themes": f"{len(recs):,}",
    "records_supp": f"{len(recs_all) - len(recs):,}",
    "india": f"{sum(r['India flag'] == 'Y' for r in recs_all):,}",
    "delhi": f"{sum(r['Delhi/NCR flag'] == 'Y' for r in recs_all):,}",
    "haryana": f"{sum(r['Haryana flag'] == 'Y' for r in recs_all):,}",
    "shortlist": f"{sum(bool(r['Shortlist tag']) for r in recs_all):,}",
    "landmarks": f"{sum(r['Landmark flag'] == 'Y' for r in recs_all):,}",
    "known_methods": f"{M['ALL']['method_known_n']:,}",
    "p_median": f"{statistics.median(pk):.2f}",
    "p_min": f"{min(pk):.2f}", "p_max": f"{max(pk):.2f}",
    "n_fast": str(sum(M[t]["fast_growth"] for t in THEMES)),
    "n_mismatch": str(sum(M[t]["mismatch_sa"] for t in THEMES)),
    "india_counts_status": ("available" if M["A1"].get("india_all_2020-26_adj") is not None
                            else "pending"),
    "core_counts_status": ("available" if M["A1"].get("global_core_2020-26_adj") is not None
                           else "pending"),
}

# ------------------------------------------------------------------ render report
tpl = (ROOT / "scripts" / "report_template.md").read_text()
tpl = re.sub(r"\{\{table:(\w+)\}\}", lambda mo: TABLES[mo.group(1)](), tpl)
tpl = re.sub(r"\{\{gaps:(\w+)\}\}", lambda mo: gaps_md(mo.group(1)), tpl)
tpl = re.sub(r"\{\{stat:(\w+)\}\}", lambda mo: STATS[mo.group(1)], tpl)
tpl = render_values(tpl)
left = re.findall(r"\{\{[^}]*\}\}", tpl)
if left:
    sys.exit(f"unrendered placeholders: {left[:5]}")
(ROOT / "outputs" / "REPORT.md").write_text(tpl)
prose = re.sub(r"^\|.*$", "", tpl, flags=re.M)
print(f"REPORT.md: {len(tpl.split()):,} words ({len(prose.split()):,} outside tables); "
      f"gaps {len(gap_rows)}; fast-growing {STATS['n_fast']}; SA mismatch {STATS['n_mismatch']}")
