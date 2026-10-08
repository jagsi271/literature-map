"""Build outputs/bibliography.xlsx from data/processed/ (records, population counts, Stage 3 tables).

Tabs: Read me · Records · Sample coverage · Growth · Emerging terms · Candidate gaps · Methods ·
Coverage limits · Landmarks by theme · India subset · Shortlist. Sample coverage (the brief's
"Gap matrix", renamed in Stage 3) uses COUNTIFS over whole Records columns, so it updates when
rows are added to Records; it describes the sample, not the literature.
"""
import datetime as dt
import json
from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
recs = json.loads((ROOT / "data" / "processed" / "records.json").read_text())
cfg = yaml.safe_load((ROOT / "queries.yaml").read_text())
THEMES = cfg["themes"]
REGIONS = ["Global North", "China & East Asia", "South Asia", "Southeast Asia", "Africa",
           "Latin America", "Middle East", "Multi-region", "Not place-specific"]
METHODS = ["qualitative", "quantitative", "mixed", "review", "conceptual", "computational",
           "unclear"]
PERIODS = [("2010–14", 2010, 2014), ("2015–19", 2015, 2019), ("2020–26", 2020, 2026)]
HEAD = Font(bold=True, color="FFFFFF")
FILL = PatternFill("solid", fgColor="2F4F6F")
SUB = PatternFill("solid", fgColor="DCE6F0")
WRAP = Alignment(wrap_text=True, vertical="top")

wb = Workbook()


def header(ws, row, values, fill=FILL, font=HEAD):
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.fill, c.font = fill, font
        c.alignment = Alignment(wrap_text=True, vertical="center")


def widths(ws, w):
    for i, x in enumerate(w, 1):
        ws.column_dimensions[get_column_letter(i)].width = x


# ------------------------------------------------------------------ Records
cols = list(recs[0].keys())
ws_r = wb.active
ws_r.title = "Records"
header(ws_r, 1, cols)
for r in recs:
    ws_r.append([r[c] for c in cols])
ws_r.freeze_panes = "C2"
ws_r.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{len(recs) + 1}"
wmap = {"Title": 60, "Authors": 35, "Venue": 30, "One-line summary": 60, "Stated gaps": 60,
        "Places studied": 25, "Link": 30, "Open-access link": 30, "Found in": 30}
widths(ws_r, [wmap.get(c, 14) for c in cols])
L = {c: get_column_letter(i) for i, c in enumerate(cols, 1)}


def col(name):
    return f"Records!${L[name]}:${L[name]}"


NOSUP = f"{col('Supplementary')},\"<>Y\""  # supplementary-only records stay out of the matrix

# ------------------------------------------------------------------ Gap matrix
ws_g = wb.create_sheet("Sample coverage")
ws_g["A1"] = ("Sample coverage — live COUNTIFS over the Records tab (counts update when rows are "
              "added). Formerly 'Gap matrix'.")
ws_g["A1"].font = Font(bold=True, size=12)
ws_g["A2"] = ("These counts describe the sample, not the literature. The sample's region and period "
              "mix is set by the design (every theme has an India/South Asia slice and a 2022–26 "
              "slice), so they are not a gap measure: gap, growth and mismatch claims come from the "
              "OpenAlex-wide population counts in the Growth tab (precision-adjusted), and records "
              "serve only as examples (Candidate gaps tab). Method shares are given among records "
              "with a known method, with the n; no method claim is made where fewer than 50 records "
              "have a known method. Records found only by the supplementary query set "
              "(Supplementary = Y) are excluded.")
ws_g["A2"].alignment = WRAP
ws_g.merge_cells("A2:N2")
ws_g.row_dimensions[2].height = 75
row = 4


def block(title, colvals, crit):
    """crit(col_value) -> list of extra COUNTIFS criteria strings."""
    global row
    ws_g.cell(row=row, column=1, value=title).font = Font(bold=True)
    row += 1
    header(ws_g, row, ["Theme", "Name"] + colvals + ["Total", "India flag"], fill=SUB,
           font=Font(bold=True))
    hdr = row
    row += 1
    first = row
    for code, t in THEMES.items():
        ws_g.cell(row=row, column=1, value=code)
        ws_g.cell(row=row, column=2, value=t["name"])
        for j, v in enumerate(colvals, 3):
            cl = get_column_letter(j)
            extra = ",".join(crit(f"{cl}${hdr}"))
            ws_g.cell(row=row, column=j,
                      value=f"=COUNTIFS({col('Primary theme')},$A{row},{NOSUP},{extra})")
        tc = get_column_letter(len(colvals) + 3)
        ws_g.cell(row=row, column=len(colvals) + 3,
                  value=f"=COUNTIFS({col('Primary theme')},$A{row},{NOSUP})")
        ws_g.cell(row=row, column=len(colvals) + 4,
                  value=f"=COUNTIFS({col('Primary theme')},$A{row},{NOSUP},{col('India flag')},\"Y\")")
        row += 1
    ws_g.cell(row=row, column=2, value="All themes").font = Font(bold=True)
    for j in range(3, len(colvals) + 5):
        cl = get_column_letter(j)
        ws_g.cell(row=row, column=j, value=f"=SUM({cl}{first}:{cl}{row - 1})").font = Font(bold=True)
    row += 3


block("Theme × region (sample; set by design)", REGIONS, lambda h: [f"{col('Region')},{h}"])
block("Theme × method (inferred from abstract; counts)", METHODS, lambda h: [f"{col('Method')},{h}"])
# method shares among records with a known method, with the n
KM = METHODS[:-1]  # 'unclear' is not a method
ws_g.cell(row=row, column=1, value="Theme × method: share among records with a known method "
          "(no method claim where known n < 50)").font = Font(bold=True)
row += 1
header(ws_g, row, ["Theme", "Name", "Known method (n)"] + KM + ["Method claims"], fill=SUB,
       font=Font(bold=True))
hdr = row
row += 1
first = row
for code, t in THEMES.items():
    ws_g.cell(row=row, column=1, value=code)
    ws_g.cell(row=row, column=2, value=t["name"])
    kn = (f"=COUNTIFS({col('Primary theme')},$A{row},{NOSUP})-COUNTIFS({col('Primary theme')},"
          f"$A{row},{NOSUP},{col('Method')},\"unclear\")")
    ws_g.cell(row=row, column=3, value=kn)
    for j, _ in enumerate(KM, 4):
        cl = get_column_letter(j)
        c = ws_g.cell(row=row, column=j, value=(
            f"=IF($C{row}=0,\"\",COUNTIFS({col('Primary theme')},$A{row},{NOSUP},"
            f"{col('Method')},{cl}${hdr})/$C{row})"))
        c.number_format = "0%"
    ws_g.cell(row=row, column=len(KM) + 4, value=f'=IF($C{row}>=50,"yes","no (n<50)")')
    row += 1
row += 2
# periods: header cell holds the label; bounds are written in the formula
ws_g.cell(row=row, column=1, value="Theme × period (publication year)").font = Font(bold=True)
row += 1
header(ws_g, row, ["Theme", "Name"] + [p[0] for p in PERIODS] + ["Before 2010", "Total"],
       fill=SUB, font=Font(bold=True))
row += 1
first = row
for code, t in THEMES.items():
    ws_g.cell(row=row, column=1, value=code)
    ws_g.cell(row=row, column=2, value=t["name"])
    for j, (_, a, b) in enumerate(PERIODS, 3):
        ws_g.cell(row=row, column=j, value=(
            f"=COUNTIFS({col('Primary theme')},$A{row},{NOSUP},{col('Year')},\">={a}\","
            f"{col('Year')},\"<={b}\")"))
    ws_g.cell(row=row, column=6, value=(
        f"=COUNTIFS({col('Primary theme')},$A{row},{NOSUP},{col('Year')},\"<2010\")"))
    ws_g.cell(row=row, column=7, value=f"=COUNTIFS({col('Primary theme')},$A{row},{NOSUP})")
    row += 1
ws_g.cell(row=row, column=2, value="All themes").font = Font(bold=True)
for j in range(3, 8):
    cl = get_column_letter(j)
    ws_g.cell(row=row, column=j, value=f"=SUM({cl}{first}:{cl}{row - 1})").font = Font(bold=True)
widths(ws_g, [8, 48] + [13] * 11)
ws_g.freeze_panes = "C4"

# ------------------------------------------------------------------ Growth (population counts)
import csv  # noqa: E402

PROC = ROOT / "data" / "processed"


def table_tab(ws, r0, heads, rows, keys, fmts=None):
    """Write a header row and rows of dicts; numbers stored as numbers."""
    header(ws, r0, heads)
    for i, rr in enumerate(rows, r0 + 1):
        for j, k in enumerate(keys, 1):
            v = rr.get(k, "")
            if isinstance(v, str):
                try:
                    v = float(v) if any(ch in v for ch in ".e") else int(v)
                except ValueError:
                    pass
            c = ws.cell(row=i, column=j, value=v)
            if fmts and k in fmts:
                c.number_format = fmts[k]
    return r0 + 1 + len(rows)


def note(ws, cell, text, merge, height):
    ws[cell] = text
    ws[cell].alignment = WRAP
    ws.merge_cells(merge)
    ws.row_dimensions[ws[cell].row].height = height


ws_w = wb.create_sheet("Growth")
ws_w["A1"] = "Growth and population counts — OpenAlex-wide, precision-adjusted (basis of all gap, growth and mismatch claims)"
ws_w["A1"].font = Font(bold=True, size=12)
note(ws_w, "A2", (
    "Source: scripts/growth_counts.py and scripts/population_counts.py (raw responses in data/raw/; "
    "tables data/processed/population_counts.csv and theme_metrics.csv). Journal articles and book "
    "chapters in journals, book series or ebook platforms (repository records excluded), not "
    "retracted, 2010–2026; each theme's combined query on title + abstract (exact). Counts are "
    "multiplied by the theme's estimated precision p (random 40-work sample of its hit set, "
    "screened with the theme's rules; borderline at the hand keep-rate; × the blind-check precision "
    "of its domain) — p_sa from a sample of the South Asia hit set where fetched. 'Per 10k' = per "
    "10,000 Social Sciences works with the same filters and place scope. Growth = per-10k share "
    "2020–26 ÷ 2015–19 ('new' when fewer than 50 adjusted works in 2015–19). 2026 is a partial "
    "year: only shares are comparable. All venues vs core venues = all sources vs sources flagged "
    "core by OpenAlex. Place scopes use place names in title/abstract. LQ (location quotient) = "
    "the scope's share of the theme ÷ its share of all Social Sciences works. Region shares = each "
    "region's share of all region mentions, 2010–26. Empty cells: counts not yet fetched."),
    "A2:P2", 120)
tm = list(csv.DictReader((PROC / "theme_metrics.csv").open())) if (PROC / "theme_metrics.csv").exists() else []
gcols = [("theme", "Theme"), ("name", "Name"), ("p", "p"), ("p_sa", "p_sa"),
         ("global_all_2015-19_adj", "Global all 2015–19 (adj.)"),
         ("global_all_2020-26_adj", "Global all 2020–26 (adj.)"),
         ("global_all_2015-19_per10k", "Per 10k SS 2015–19"),
         ("global_all_2020-26_per10k", "Per 10k SS 2020–26"),
         ("global_all_growth_label", "Growth (all venues)"),
         ("global_core_2015-19_adj", "Global core 2015–19 (adj.)"),
         ("global_core_2020-26_adj", "Global core 2020–26 (adj.)"),
         ("global_core_growth_label", "Growth (core venues)"),
         ("sa_all_2020-26_adj", "South Asia all 2020–26 (adj.)"),
         ("sa_share_all_2020-26", "SA share 2020–26 (%)"),
         ("lq_sa_all_2020-26", "SA LQ 2020–26"), ("sa_all_growth", "SA growth (all)"),
         ("sa_core_2020-26_adj", "SA core 2020–26 (adj.)"),
         ("sa_share_core_2020-26", "SA share core (%)"),
         ("india_all_2020-26_adj", "India all 2020–26 (adj.)"),
         ("india_share_all_2020-26", "India share 2020–26 (%)"),
         ("lq_india_all_2020-26", "India LQ 2020–26"),
         ("india_core_2020-26_adj", "India core 2020–26 (adj.)"),
         ("india_share_core_2020-26", "India share core (%)"),
         ("delhi_all_2010-26_adj", "Delhi/NCR all 2010–26 (adj.)"),
         ("delhi_core_2010-26_adj", "Delhi/NCR core 2010–26 (adj.)"),
         ("haryana_all_2010-26_adj", "Haryana all 2010–26 (adj.)"),
         ("haryana_core_2010-26_adj", "Haryana core 2010–26 (adj.)"),
         ("sa_share_of_region_mentions", "South Asia % of region mentions"),
         ("gn_share_of_region_mentions", "Global North %"),
         ("ea_share_of_region_mentions", "China & East Asia %"),
         ("sea_share_of_region_mentions", "Southeast Asia %"),
         ("af_share_of_region_mentions", "Africa %"),
         ("la_share_of_region_mentions", "Latin America %"),
         ("me_share_of_region_mentions", "Middle East %"),
         ("fast_growth", "Fast growth (≥3 or new)"), ("saturating", "Saturating (≤1.3, large)"),
         ("sa_thin", "SA share ≤ 5%"), ("mismatch_sa", "Fast & SA-thin"),
         ("gn_dominated", "Global North ≥ 50%")]
rr = table_tab(ws_w, 4, [h for _, h in gcols], tm, [k for k, _ in gcols],
               {k: "0.00" for k, _ in gcols if k.startswith(("lq", "p")) or "per10k" in k
                or "growth" in k or "share" in k})
ws_w.freeze_panes = "C5"
gj = ROOT / "data" / "raw" / "counts" / "growth_stage2.json"
if gj.exists():
    gd = json.loads(gj.read_text())
    years = list(range(2010, 2027))
    rr += 2
    ws_w.cell(row=rr, column=1, value="Per-year raw counts, all venues (before precision adjustment)").font = Font(bold=True)
    rr += 1
    header(ws_w, rr, ["Theme", "Scope"] + years, fill=SUB, font=Font(bold=True))
    series = [("SS baseline", "global", gd["baseline"]["global"]),
              ("SS baseline", "south_asia", gd["baseline"]["south_asia"])]
    series += [(t, sc, d[sc]) for t, d in gd["themes"].items() for sc in ("global", "south_asia")]
    for name, sc, d in series:
        rr += 1
        ws_w.cell(row=rr, column=1, value=name)
        ws_w.cell(row=rr, column=2, value=sc)
        for j, y in enumerate(years, 3):
            ws_w.cell(row=rr, column=j, value=int(d.get(str(y), d.get(y, 0))))
widths(ws_w, [8, 44] + [12] * 40)

# ------------------------------------------------------------------ Emerging terms
ws_e = wb.create_sheet("Emerging terms")
ws_e["A1"] = "Emerging terms — share of each period's records, 2018–21 vs 2022–26"
ws_e["A1"].font = Font(bold=True, size=12)
note(ws_e, "A2", (
    "Source: scripts/emerging_terms.py → data/processed/emerging_terms.csv. Terms = OpenAlex keywords "
    "on the map's records (48 themes; supplementary-only records left out). The sample's period mix "
    "is set by the design, so terms are ranked by the change in their share of the period's records "
    "(+0.5 smoothing), not by raw counts; a term needs ≥15 records in 2022–26 and records in ≥2 "
    "themes. Checks: the same ratio within India/South Asia-slice records only, and OpenAlex-wide "
    "(the keyword's share of all Social Sciences works, same filters as Growth); 'confirmed' = the "
    "OpenAlex-wide share rose by more than 20%. Confirmed terms are ranked first; the top 30 are the "
    "report's list. 'Query phrase' = the term is a theme query phrase (its recent share is inflated "
    "by the relevance-ranked recent slice). Examples: 2022–24 records with the highest FWCI (2025–26 "
    "works are left out of FWCI-based signals: their citations are too young)."), "A2:L2", 105)
em = list(csv.DictReader((PROC / "emerging_terms.csv").open())) if (PROC / "emerging_terms.csv").exists() else []
ecols = [("rank", "Rank"), ("term", "Term"), ("records_2018_21", "Records 2018–21"),
         ("records_2022_26", "Records 2022–26"), ("share_2018_21_pct", "Share 2018–21 (%)"),
         ("share_2022_26_pct", "Share 2022–26 (%)"), ("share_ratio", "Share ratio"),
         ("india_slice_share_ratio", "India-slice share ratio"),
         ("oa_ss_works_2018_21", "OpenAlex SS works 2018–21"),
         ("oa_ss_works_2022_26", "OpenAlex SS works 2022–26"),
         ("oa_share_ratio", "OpenAlex-wide share ratio"), ("confirmed", "Confirmed"),
         ("query_phrase", "Query phrase"), ("top_themes", "Top themes"),
         ("example_1", "Example 1"), ("example_2", "Example 2"), ("example_3", "Example 3")]
table_tab(ws_e, 4, [h for _, h in ecols], em, [k for k, _ in ecols])
ws_e.freeze_panes = "C5"
widths(ws_e, [6, 30, 10, 10, 10, 10, 9, 10, 12, 12, 11, 9, 8, 26, 50, 50, 50])

# ------------------------------------------------------------------ Candidate gaps
ws_c = wb.create_sheet("Candidate gaps")
ws_c["A1"] = "Candidate gaps — leads to check, not proofs"
ws_c["A1"].font = Font(bold=True, size=12)
note(ws_c, "A2", (
    "Source: data/analysis/candidate_gaps.yaml rendered by scripts/stage3_analysis.py "
    "(data/processed/candidate_gaps.csv); full text in outputs/REPORT.md §7–8. Evidence = "
    "OpenAlex-wide population counts (Growth tab), all venues and core venues; 'pending' = counts "
    "not yet fetched. Examples are records from this bibliography (IDs in the Records tab), used "
    "only as examples. Every India, Delhi/NCR or Haryana gap carries the Coverage limits caveat: "
    "check EPW and Shodhganga by hand before relying on it. Method gaps use method shares among "
    "records with a known method (n ≥ 50)."), "A2:I2", 75)
cg = list(csv.DictReader((PROC / "candidate_gaps.csv").open())) if (PROC / "candidate_gaps.csv").exists() else []
ccols = [("id", "ID"), ("scope", "Scope"), ("themes", "Themes"), ("title", "Gap"),
         ("status", "Status"), ("evidence", "Evidence (population counts)"),
         ("examples", "Example records"), ("missing", "What is missing"), ("caveat", "Caveat"),
         ("matching_records_in_map", "Matching records in map")]
end = table_tab(ws_c, 4, [h for _, h in ccols], cg, [k for k, _ in ccols])
for row_ in ws_c.iter_rows(min_row=5, max_row=end - 1):
    for c in row_:
        c.alignment = WRAP
widths(ws_c, [5, 12, 9, 34, 14, 60, 60, 50, 50, 10])
ws_c.freeze_panes = "E5"

# ------------------------------------------------------------------ Methods
ws_m = wb.create_sheet("Methods")
ws_m["A1"] = "Method shares among records with a known method (sample)"
ws_m["A1"].font = Font(bold=True, size=12)
note(ws_m, "A2", (
    "Source: data/processed/method_shares.csv. Method is inferred from the abstract by keyword cues "
    "('unclear' when there is no abstract or no cue) and is known for about 63% of records; shares "
    "are among records with a known method, with the n. No method claim is made where fewer than "
    "50 records have a known method. Groups: themes (primary theme), domains, India-flagged (IN_) "
    "and Global North (GN_) records by domain. These describe the map's records, not the "
    "literature."), "A2:J2", 60)
ms = list(csv.DictReader((PROC / "method_shares.csv").open())) if (PROC / "method_shares.csv").exists() else []
if ms:
    table_tab(ws_m, 4, list(ms[0].keys()), ms, list(ms[0].keys()))
widths(ws_m, [10, 10, 14, 16] + [16] * 6)

# ------------------------------------------------------------------ Coverage limits
ws_v = wb.create_sheet("Coverage limits")
ws_v["A1"] = "Coverage limits — OpenAlex holdings of selected Indian venues, works per year"
ws_v["A1"].font = Font(bold=True, size=12)
note(ws_v, "A2", (
    "Source: scripts/coverage_check.py → data/processed/coverage_limits.csv (OpenAlex source IDs "
    "chosen by name and ISSN). EPW is held only from 2024 (almost all 2025–26); Seminar has no "
    "OpenAlex source; Shodhganga theses are held only to 2021, almost all without abstracts, and "
    "are outside the population-count filters (theses, not articles). Indian writing in these "
    "venues is therefore largely invisible to the counts: check EPW and Shodhganga by hand before "
    "relying on any India, Delhi/NCR or Haryana gap."), "A2:L2", 60)
cl = list(csv.DictReader((PROC / "coverage_limits.csv").open())) if (PROC / "coverage_limits.csv").exists() else []
if cl:
    table_tab(ws_v, 4, list(cl[0].keys()), cl, list(cl[0].keys()))
widths(ws_v, [34, 16] + [9] * 22)

# ------------------------------------------------------------------ Landmarks, India, Shortlist
SHORT = ["ID", "Primary theme", "Title", "Year", "Authors", "Venue", "Cited-by count", "DOI",
         "Region", "Places studied", "Found in"]


def subset(name, rows, note, extra=()):
    ws = wb.create_sheet(name)
    ws["A1"] = note
    ws["A1"].alignment = WRAP
    ws.merge_cells(f"A1:{get_column_letter(len(SHORT) + len(extra))}1")
    ws.row_dimensions[1].height = 32
    header(ws, 2, SHORT + list(extra))
    for r in rows:
        ws.append([r[c] for c in SHORT + list(extra)])
    ws.freeze_panes = "D3"
    widths(ws, [10, 8, 60, 7, 30, 28, 9, 26, 16, 22, 26] + [30] * len(extra))
    return ws


subset("Landmarks by theme",
       sorted([r for r in recs if r["Landmark flag"] == "Y"],
              key=lambda r: (r["Primary theme"], -(r["Cited-by count"] or 0))),
       "Records found in a theme's 'landmarks' slice (top cited works for the query, any year) "
       "and kept after screening (the most-cited were checked by hand in Stage 3); repository-only "
       "records are excluded; sorted by theme, then citations.")
subset("India subset",
       sorted([r for r in recs if r["India flag"] == "Y"],
              key=lambda r: (r["Primary theme"], -(r["Year"] or 0))),
       "Records whose title/abstract name India or an Indian place (Delhi/NCR and Haryana flags "
       "in the extra columns).", extra=("Delhi/NCR flag", "Haryana flag"))
subset("Shortlist",
       [r for r in recs if r["Shortlist tag"]],
       "Records touching the researcher's current leads (stations, waiting, night-time "
       "mobility, fare integration/NCMC, rail-led urbanism, elevated infrastructure, Haryana "
       "secondary cities). Tagging only; it does not affect search or screening.",
       extra=("Shortlist tag",))

# ------------------------------------------------------------------ Read me
ws = wb.create_sheet("Read me", 0)
_rp = ROOT / "data" / "screening" / "recall_seeds_stage2.csv"
RECALL = {}
if _rp.exists():
    for _r in csv.DictReader(_rp.open()):
        RECALL[_r["status"]] = RECALL.get(_r["status"], 0) + 1
n = len(recs)
by_theme = {}
for r in recs:
    by_theme[r["Primary theme"]] = by_theme.get(r["Primary theme"], 0) + 1
sup = sum(r["Supplementary"] == "Y" for r in recs)
repo = sum(r["Repository-only"] == "Y" for r in recs)
lines = [
    ("Literature map: urban, digital and urban–digital research", "title"),
    (f"Stage 3 build, {dt.date.today().isoformat()}. {n} deduplicated records, of which {sup} "
     f"come only from the supplementary query set and {repo} are repository-only. Records per "
     f"primary theme: {', '.join(f'{k}: {v}' for k, v in sorted(by_theme.items(), key=lambda x: (x[0][0], int(x[0][1:]))))}.", ""),
    ("What this is", "h"),
    ("A representative, reproducible map — not a census — of three domains (A urban, B digital "
     "society, C urban × digital), 48 themes. Every record comes from an OpenAlex API response; "
     "raw responses are cached in data/raw/ of the repository. See BRIEF.md, queries.yaml, "
     "PROGRESS.md and scripts/.", ""),
    ("Tabs", "h"),
    ("Records — one row per work (schema below). Sample coverage (the brief's 'Gap matrix', "
     "renamed) — live COUNTIFS of theme × region, theme × method (with shares among records with "
     "a known method and the n) and theme × period, supplementary-only records excluded. Growth — "
     "OpenAlex-wide population counts per theme, precision-adjusted, for all venues and core "
     "venues, globally and for South Asia, India, Delhi/NCR, Haryana and six other regions. "
     "Emerging terms — keywords whose share of records rose most from 2018–21 to 2022–26, checked "
     "OpenAlex-wide. Candidate gaps — 25 leads with evidence, examples and caveats. Methods — "
     "method shares among records with a known method. Coverage limits — OpenAlex holdings of "
     "Indian venues. Landmarks by theme — records from the 'landmarks' slice, repository-only "
     "records excluded. India subset — India-flagged records. Shortlist — records touching "
     "current leads. The full analysis is in outputs/REPORT.md.", ""),
    ("Why the gap tab was renamed", "h"),
    ("The sample's region and period mix is set by the design: every theme has an India/South Asia "
     "slice and a 2022–26 slice. Counting records by region or period therefore measures the "
     "design, not the literature, so the brief's 'Gap matrix' is now called 'Sample coverage' and "
     "is not used to find gaps. Every gap, growth and mismatch claim rests on OpenAlex-wide counts "
     "with the same filters as the Growth tab, precision-adjusted; records are used only as "
     "examples. India, Delhi/NCR and Haryana gaps also carry the Coverage limits caveat (EPW, "
     "Seminar and Shodhganga are poorly covered by OpenAlex): check EPW and Shodhganga by hand "
     "before relying on them.", ""),
    ("How records were found", "h"),
    ("For each theme, 2–6 queries (queries.yaml) run against the OpenAlex API in exact-phrase "
     "mode over title and abstract (Stage 1 pilot slices: title, abstract and keywords), in "
     "three slices: landmarks (the theme's queries OR-ed, top 100 by citations; page 2 where "
     "fewer than 25 survived), recent (2022–2026, one search per query string, top 15–25 by "
     "relevance), India/South Asia (each query AND South Asian place names, top 15–25 by "
     "relevance). A supplementary query set (S1–S7: railway stations, waiting, night-time "
     "transit, fare integration/NCMC, rail-led urbanism, elevated rail, Haryana secondary "
     "cities) was searched separately; records found only there are tagged Supplementary = Y "
     "and given the query's home theme.", ""),
    ("Screening", "h"),
    ("Rule-based on title + abstract (rules v3, queries.yaml header): the theme's core concept "
     "in the title or twice in the abstract, plus its context terms (for C themes the urban "
     "context, or a named city, is required). Borderline cases (single mention named by a "
     "keyword tag, flagged technical/biomedical terms with the core in the title, stub "
     "abstracts) were decided by hand (data/screening/manual_review.csv). Records whose OpenAlex "
     "primary-topic field is biomedical or natural-science are excluded unless kept by hand. "
     "Book reviews, errata, paratext, editorials, datasets and retracted works are excluded. "
     "A work is assigned the primary theme with the strongest match among the themes whose "
     "searches found it. Deduplicated by DOI, then by normalised title.", ""),
    ("Columns that are inferred automatically (check before citing)", "h"),
    ("Places studied / Region: place names matched in title + abstract (not author "
     "affiliations). Region buckets: Global North (Europe, North America, Australia, NZ, "
     "Russia), China & East Asia, South Asia, Southeast Asia (incl. Pacific islands), Africa "
     "(incl. North Africa), Latin America (incl. Caribbean), Middle East (incl. Central Asia "
     "and Caucasus); two or more buckets = Multi-region; none = Not place-specific. India / "
     "Delhi-NCR / Haryana flags: same matching. Method: keyword cues in the abstract; 'unclear' "
     "when there is no abstract or no cue. Landmark flag: found in a landmarks slice and not "
     "repository-only. Repository-only: every merged version sits only in a repository or "
     "preprint server (Zenodo, SSRN, arXiv, institutional repositories). C4 orientation: "
     "critical vs technical (keyword cues). Emerging flag: published 2022–24 with FWCI ≥ 1.5 "
     "(2025–26 works are left out: their citations are too young). One-line summary and Stated gaps: sentences copied from the abstract, marked "
     "'auto:'. Screening confidence: high = rule-included with the core concept and context; "
     "medium = rule-included via other routes or kept by hand; low = no abstract.", ""),
    ("Known limits", "h"),
    ("Blind check of 6 random records per theme (data/screening/precision_check_stage2.csv): "
     "about 88–91% in scope, 81–83% with a correct primary theme; weakest in technical-leaning C "
     "themes. In Stage 3 the most-cited landmark records of every theme were checked by hand and "
     "38 clearly off-topic works were removed. Recall against 176 researcher-chosen seeds "
     f"(data/screening/recall_seeds_stage2.csv): {RECALL.get('found', 0)} found; "
     f"{RECALL.get('below cut-off', 0)} match a theme query but rank below the per-query cut-off "
     f"of the recent/India slices; {RECALL.get('query gap', 0)} query gaps; "
     f"{RECALL.get('screened out', 0)} screened out; {RECALL.get('not in OpenAlex', 0)} not in "
     "OpenAlex. OpenAlex covers Indian venues poorly (Coverage limits tab). Place tags come from "
     "titles and abstracts only. See PROGRESS.md and outputs/REPORT.md.", ""),
    ("Extra columns", "h"),
    ("Supplementary / Supplementary query = found only by / also by the supplementary query "
     "set; Found in = theme:slice combinations that returned the work ('<-X' marks a work moved "
     "by hand from theme X); Duplicates merged = other OpenAlex IDs folded into this record; "
     "FWCI = OpenAlex field-weighted citation impact.", ""),
]
r = 1
for text, kind in lines:
    c = ws.cell(row=r, column=1, value=text)
    c.alignment = WRAP
    if kind == "title":
        c.font = Font(bold=True, size=14)
    elif kind == "h":
        c.font = Font(bold=True)
        c.fill = SUB
    else:
        ws.row_dimensions[r].height = max(15, 15 * (len(text) // 110 + 1))
    r += 1
ws.column_dimensions["A"].width = 130

out = ROOT / "outputs" / "bibliography.xlsx"
out.parent.mkdir(exist_ok=True)
wb.save(out)
print(out, n, "records")
