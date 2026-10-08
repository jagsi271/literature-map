"""Export the bibliography for Zotero: outputs/bibliography.bib (BibTeX) and outputs/bibliography.ris.

Usage: python3 scripts/export_bib.py

One entry per record in data/processed/records.json, metadata only (no abstracts). The record
ID (LMxxxxx, the row in outputs/bibliography.xlsx), domain, primary/secondary theme and the
India, Delhi/NCR, Haryana, landmark, emerging, shortlist, supplementary and repository-only
flags are written as keywords, so they become Zotero tags.
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
recs = json.loads((ROOT / "data/processed/records.json").read_text())

BIB_TYPE = {"article": "article", "review": "article", "data-paper": "article",
            "book-chapter": "incollection", "reference-entry": "incollection",
            "book": "book", "conference-paper": "inproceedings",
            "conference-abstract": "inproceedings", "dissertation": "phdthesis",
            "report": "techreport"}
RIS_TYPE = {"article": "JOUR", "review": "JOUR", "data-paper": "JOUR", "book-chapter": "CHAP",
            "reference-entry": "ENCYC", "book": "BOOK", "conference-paper": "CPAPER",
            "conference-abstract": "ABST", "dissertation": "THES", "report": "RPRT",
            "preprint": "UNPB"}
VENUE_FIELD = {"article": "journal", "incollection": "booktitle", "inproceedings": "booktitle",
               "phdthesis": "school", "techreport": "institution", "book": "publisher",
               "misc": "howpublished"}
PARTICLES = {"van", "von", "de", "da", "del", "der", "di", "du", "le", "la", "dos", "das"}


def authors(r):
    return [a.strip() for a in (r["Authors"] or "").split(";") if re.search(r"[A-Za-z]{2}", a)]


def split_name(full):
    """'First von Last' -> ('von Last', 'First')."""
    parts = full.split()
    if len(parts) == 1:
        return parts[0], ""
    i = len(parts) - 1
    while i > 1 and parts[i - 1].lower() in PARTICLES:
        i -= 1
    return " ".join(parts[i:]), " ".join(parts[:i])


def tags(r):
    t = [r["ID"], f"domain {r['Domain']}", f"theme {r['Primary theme']}"]
    if r["Secondary theme"]:
        t.append(f"theme2 {r['Secondary theme']}")
    for col, tag in [("India flag", "India"), ("Delhi/NCR flag", "Delhi-NCR"),
                     ("Haryana flag", "Haryana"), ("Landmark flag", "landmark"),
                     ("Emerging flag", "emerging"), ("Supplementary", "supplementary"),
                     ("Repository-only", "repository-only")]:
        if r[col] == "Y":
            t.append(tag)
    if r["Shortlist tag"]:
        t.append("shortlist")
    if r["Region"]:
        t.append(f"region {r['Region']}")
    if r["Method"] and r["Method"] != "unclear":
        t.append(f"method {r['Method']} (auto)")
    return t


def ascii_key(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]", "", s)


def bib_escape(s):
    s = s.replace("\\", " ").replace("{", "(").replace("}", ")")
    return re.sub(r"([&%$#_])", r"\\\1", s)


keys = Counter()
bib, ris = [], []
for r in recs:
    au = authors(r)
    first = split_name(au[0])[0] if au else (r["Title"].split() or ["anon"])[0]
    word = next((w for w in re.findall(r"[A-Za-z]+", r["Title"])
                 if w.lower() not in {"the", "a", "an", "of", "on", "in", "and"}), "x")
    base = (ascii_key(first) + str(r["Year"] or "") + ascii_key(word)).lower() or r["ID"]
    keys[base] += 1
    key = base if keys[base] == 1 else f"{base}{chr(96 + keys[base])}" if keys[base] < 27 \
        else f"{base}{keys[base]}"
    dt = r["Document type"]
    bt = BIB_TYPE.get(dt, "misc")
    f = [("title", "{" + bib_escape(r["Title"]) + "}")]
    if au:
        f.append(("author", " and ".join(
            "{" + bib_escape(a) + "}" if len(a.split()) == 1 else
            f"{bib_escape(split_name(a)[0])}, {bib_escape(split_name(a)[1])}" for a in au)))
    if r["Year"]:
        f.append(("year", str(r["Year"])))
    if r["Venue"]:
        f.append((VENUE_FIELD.get(bt, "howpublished"), bib_escape(r["Venue"])))
    if r["DOI"]:
        f.append(("doi", r["DOI"].replace("https://doi.org/", "")))
    url = r["Link"] or r["Open-access link"]
    if url:
        f.append(("url", url))
    f.append(("keywords", bib_escape(", ".join(tags(r)))))
    f.append(("note", bib_escape(f"Literature map {r['ID']}; OpenAlex {r['OpenAlex ID']}; "
                                 f"OpenAlex type {dt}")))
    bib.append(f"@{bt}{{{key},\n" + ",\n".join(f"  {k} = {{{v}}}" if not v.startswith("{")
                                                 else f"  {k} = {v}" for k, v in f) + "\n}\n")

    ty = RIS_TYPE.get(dt, "GEN")
    lines = [f"TY  - {ty}", f"TI  - {r['Title']}"]
    lines += [f"AU  - {split_name(a)[0]}, {split_name(a)[1]}".rstrip(", ") for a in au]
    if r["Year"]:
        lines.append(f"PY  - {r['Year']}")
    if r["Venue"]:
        lines.append(f"{'T2' if ty in ('CHAP', 'CPAPER', 'ENCYC') else 'JO' if ty == 'JOUR' else 'PB'}"
                     f"  - {r['Venue']}")
    if r["DOI"]:
        lines.append(f"DO  - {r['DOI'].replace('https://doi.org/', '')}")
    if url:
        lines.append(f"UR  - {url}")
    if r["Open-access link"] and r["Open-access link"] != url:
        lines.append(f"L1  - {r['Open-access link']}")
    lines += [f"KW  - {t}" for t in tags(r)]
    lines.append(f"N1  - Literature map {r['ID']}; OpenAlex {r['OpenAlex ID']}; OpenAlex type {dt}")
    lines.append(f"ID  - {r['ID']}")
    lines.append("ER  - ")
    ris.append("\n".join(lines) + "\n")

out = ROOT / "outputs"
(out / "bibliography.bib").write_text(
    "% Literature map: urban, digital and urban x digital research. Generated by "
    "scripts/export_bib.py from data/processed/records.json.\n\n" + "\n".join(bib))
(out / "bibliography.ris").write_text("\n".join(ris))
print(f"{len(bib)} BibTeX entries, {len(ris)} RIS records; "
      f"types {Counter(BIB_TYPE.get(r['Document type'], 'misc') for r in recs).most_common()}")
