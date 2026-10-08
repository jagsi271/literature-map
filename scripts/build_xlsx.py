"""Build outputs/bibliography.xlsx from data/processed/records.json and data/raw/counts/.

Tabs: Read me · Records · Gap matrix · Growth · Emerging terms · Landmarks by theme ·
India subset · Shortlist. The Gap matrix uses COUNTIFS over whole Records columns, so it
updates when rows are added to Records.
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
ws_g = wb.create_sheet("Gap matrix")
ws_g["A1"] = "Gap matrix — live COUNTIFS over the Records tab (counts update when rows are added)"
ws_g["A1"].font = Font(bold=True, size=12)
ws_g["A2"] = ("Counts are of records in this bibliography (a sample), not of all literature; "
              "use the Growth tab for OpenAlex-wide counts. Records found only by the "
              "supplementary query set (Supplementary = Y) are excluded.")
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


block("Theme × region", REGIONS, lambda h: [f"{col('Region')},{h}"])
block("Theme × method (inferred from abstract)", METHODS, lambda h: [f"{col('Method')},{h}"])
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

# ------------------------------------------------------------------ Growth
import csv  # noqa: E402

ws_w = wb.create_sheet("Growth")
ws_w["A1"] = "Growth — OpenAlex-wide counts per theme (prepared in Stage 2 for the Stage 3 analysis)"
ws_w["A1"].font = Font(bold=True, size=12)
ws_w["A2"] = ("Source: scripts/growth_counts.py (data/raw/counts/growth_stage2.json, "
              "data/processed/growth_counts.csv). Journal articles and book chapters only "
              "(primary location in a journal, book series or ebook platform: repository-only "
              "records such as Zenodo are excluded), 2010–2026, each theme's combined query. "
              "Counts are multiplied by the theme's estimated precision (random sample of 40 from "
              "the full 2015–26 hit set, screened with the theme's rules; borderline counted at "
              "the hand keep-rate) and normalised per 10,000 Social Sciences works in the same "
              "period under the same filters. 2026 is a partial year (retrieved October 2026); "
              "the normalised shares stay comparable because the baseline is equally partial. "
              "Growth ratio = normalised share 2020–26 ÷ 2015–19. One precision estimate per theme "
              "is applied to both periods.")
ws_w["A2"].alignment = WRAP
ws_w.row_dimensions[2].height = 105
ws_w.merge_cells("A2:N2")
gpath = ROOT / "data" / "processed" / "growth_counts.csv"
grows = list(csv.DictReader(gpath.open())) if gpath.exists() else []
gcols = ["theme", "name", "precision_est", "global_2015-19_raw", "global_2020-26_raw",
         "global_2015-19_per10k_ss", "global_2020-26_per10k_ss", "global_growth_ratio",
         "SA_2015-19_raw", "SA_2020-26_raw", "SA_2015-19_per10k_ss", "SA_2020-26_per10k_ss",
         "SA_growth_ratio", "2026_global_raw_partial"]
header(ws_w, 4, ["Theme", "Name", "Precision est.", "Raw 2015–19", "Raw 2020–26",
                 "Adj. per 10k SS 2015–19", "Adj. per 10k SS 2020–26", "Growth ratio",
                 "SA raw 2015–19", "SA raw 2020–26", "SA adj. per 10k SA-SS 2015–19",
                 "SA adj. per 10k SA-SS 2020–26", "SA growth ratio", "2026 raw (partial)"])
for i, g in enumerate(grows, 5):
    for j, c in enumerate(gcols, 1):
        v = g[c]
        try:
            v = float(v) if "." in v else int(v)
        except ValueError:
            pass
        ws_w.cell(row=i, column=j, value=v)
rr = 5 + len(grows) + 2
gj = ROOT / "data" / "raw" / "counts" / "growth_stage2.json"
if gj.exists():
    gd = json.loads(gj.read_text())
    years = list(range(2010, 2027))
    ws_w.cell(row=rr, column=1, value="Per-year raw counts (same filters)").font = Font(bold=True)
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
widths(ws_w, [8, 44] + [12] * 17)

# ------------------------------------------------------------------ Emerging terms
ws_e = wb.create_sheet("Emerging terms")
ws_e["A1"] = "Emerging terms — Stage 3"
ws_e["A1"].font = Font(bold=True, size=12)
ws_e["A2"] = ("Top 30 keywords/topics whose frequency rose fastest from 2018–21 to 2022–26, with "
              "counts and example papers. To be filled in Stage 3.")
header(ws_e, 4, ["Rank", "Term", "Count 2018–21", "Count 2022–26", "Growth", "Themes",
                 "Example paper 1 (ID)", "Example paper 2 (ID)", "Example paper 3 (ID)"])
widths(ws_e, [6, 30, 14, 14, 10, 20, 22, 22, 22])

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
       "and kept after screening; repository-only records are excluded; sorted by theme, then "
       "citations.")
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
n = len(recs)
by_theme = {}
for r in recs:
    by_theme[r["Primary theme"]] = by_theme.get(r["Primary theme"], 0) + 1
sup = sum(r["Supplementary"] == "Y" for r in recs)
repo = sum(r["Repository-only"] == "Y" for r in recs)
lines = [
    ("Literature map: urban, digital and urban–digital research", "title"),
    (f"Stage 2 build, {dt.date.today().isoformat()}. {n} deduplicated records, of which {sup} "
     f"come only from the supplementary query set and {repo} are repository-only. Records per "
     f"primary theme: {', '.join(f'{k}: {v}' for k, v in sorted(by_theme.items(), key=lambda x: (x[0][0], int(x[0][1:]))))}.", ""),
    ("What this is", "h"),
    ("A representative, reproducible map — not a census — of three domains (A urban, B digital "
     "society, C urban × digital), 48 themes. Every record comes from an OpenAlex API response; "
     "raw responses are cached in data/raw/ of the repository. See BRIEF.md, queries.yaml, "
     "PROGRESS.md and scripts/.", ""),
    ("Tabs", "h"),
    ("Records — one row per work (schema below). Gap matrix — live COUNTIFS of theme × region, "
     "theme × method, theme × period (supplementary-only records excluded). Growth — "
     "OpenAlex-wide counts per theme, precision-adjusted and normalised (Stage 3 input). "
     "Emerging terms — Stage 3. Landmarks by theme — records from the 'landmarks' slice, "
     "repository-only records excluded. India subset — India-flagged records. Shortlist — "
     "records touching current leads.", ""),
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
     "critical vs technical (keyword cues). Emerging flag (provisional): published 2022+ with "
     "FWCI ≥ 1.5. One-line summary and Stated gaps: sentences copied from the abstract, marked "
     "'auto:'. Screening confidence: high = rule-included with the core concept and context; "
     "medium = rule-included via other routes or kept by hand; low = no abstract.", ""),
    ("Known limits", "h"),
    ("Blind check of 6 random records per theme (data/screening/precision_check_stage2.csv): "
     "about 88–91% in scope, 81–83% with a correct primary theme; weakest in technical-leaning C "
     "themes. Recall against 176 researcher-chosen seeds: 51 of the 165 resolvable seeds are in "
     "the map; most misses match a theme query but rank below the per-query cut-off of the "
     "recent/India slices. See PROGRESS.md.", ""),
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
