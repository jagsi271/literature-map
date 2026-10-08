"""Coverage limits: how many works OpenAlex holds per year for selected Indian venues.

Usage: python3 scripts/coverage_check.py find      list candidate OpenAlex sources per name
       python3 scripts/coverage_check.py count     works per year for the chosen source IDs
                                                    -> data/processed/coverage_limits.csv

Source IDs are chosen by hand from the `find` output (SOURCES below); counts are cheap list calls
(filter primary_location.source.id, group_by publication_year, corpus core and all) and are
compared with the number of map records from each source. Raw responses: data/raw/coverage/.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetcher import RAW, Fetcher  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NAMES = ["Economic and Political Weekly", "Seminar", "Contributions to Indian Sociology",
         "Indian Journal of Public Administration", "Environment and Urbanization ASIA",
         "Urbanisation", "Shodhganga"]
# chosen from `find` (name -> list of source IDs; empty = no OpenAlex source)
SOURCES = json.loads((RAW / "coverage" / "chosen_sources.json").read_text()) \
    if (RAW / "coverage" / "chosen_sources.json").exists() else {}


def find():
    f = Fetcher(min_interval=0.5, label="coverage")
    for n in NAMES:
        d = f.get_json("https://api.openalex.org/sources",
                       {"search": n, "per_page": 8,
                        "select": "id,display_name,type,works_count,issn_l,"
                                  "host_organization_name,is_core"},
                       RAW / "coverage" / f"sources_search_{n.replace(' ', '_')}.json")
        print("##", n)
        for s in d["results"]:
            print("  ", s["id"].rsplit("/", 1)[-1], "|", s["display_name"][:60], "|", s["type"],
                  "|", s["works_count"], "|", s.get("issn_l"), "|",
                  (s.get("host_organization_name") or "")[:30], "| core", s.get("is_core"))
    print("credits remaining", f.remaining)


def count():
    f = Fetcher(min_interval=0.5, label="coverage")
    recs = json.loads((ROOT / "data/processed/records.json").read_text())
    years = list(range(2010, 2027))
    rows = []
    for name, sids in SOURCES.items():
        row = {"venue": name, "openalex_source_ids": " ".join(sids)}
        if not sids:
            row.update({"note": "no OpenAlex source found"})
            rows.append(row)
            continue
        for corpus in ("core", "all"):
            d = f.openalex_list({"filter": f"primary_location.source.id:{'|'.join(sids)}",
                                 "group_by": "publication_year", "corpus": corpus},
                                f"../coverage/count_{name.split(' (')[0].replace(' ', '_').replace('&', 'and')}_{corpus}")
            by = {int(g["key"]): g["count"] for g in d["group_by"] if str(g["key"]).isdigit()}
            row[f"total_{corpus}"] = sum(by.values())
            if corpus == "core":
                row["before_2010"] = sum(v for y, v in by.items() if y < 2010)
                for y in years:
                    row[str(y)] = by.get(y, 0)
        from fetcher import load_work
        row["records_in_map"] = sum(
            1 for r in recs
            if (((load_work(r["OpenAlex ID"]).get("primary_location") or {}).get("source") or {})
                .get("id", "").rsplit("/", 1)[-1] in sids))
        rows.append(row)
    cols = ["venue", "openalex_source_ids", "total_core", "total_all", "before_2010"] + \
        [str(y) for y in years] + ["records_in_map", "note"]
    with (ROOT / "data/processed/coverage_limits.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)
    print("credits remaining", f.remaining)


if __name__ == "__main__":
    {"find": find, "count": count}[sys.argv[1]]()
