"""Store the result of one connector search as a manifest under data/raw/searches/.

The OpenAlex connector's search_works results come back to the agent, not to disk, so the
returned work IDs (with publication year as a transcription check) are recorded here together
with the exact query, parameters, canonical OQL and total count from the response. Full records
are then fetched one by one from the public API by scripts/fetch_works.py and the fetched year
is checked against the year recorded here.

Usage: python3 scripts/record_search.py THEME SLICE TOTAL "OQL" "W1:2019 W2:2020 ..." [PAGE]
(use year 0 for a work the response listed without a year)
"""
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_search import load, search_string  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

theme, sl, total, oql, ids = sys.argv[1:6]
page = int(sys.argv[6]) if len(sys.argv) > 6 else 1
cfg = load()
results = []
for tok in ids.split():
    wid, year = tok.split(":")
    assert wid.startswith("W") and wid[1:].isdigit(), tok
    results.append([wid, int(year)])
assert len({r[0] for r in results}) == len(results), "duplicate IDs"
out = {
    "theme": theme,
    "slice": sl,
    "source": "OpenAlex connector search_works (IDs transcribed from the response)",
    "query": search_string(cfg, theme, sl),
    "mode": cfg["mode"],
    "search_in": "title_abstract_keywords",
    **cfg["slices"][sl],
    "oql": oql,
    "page": page,
    "total_results": int(total),
    "retrieved": dt.date.today().isoformat(),
    "results": results,
}
p = ROOT / "data" / "raw" / "searches" / (f"{theme}_{sl}.json" if page == 1 else f"{theme}_{sl}_p{page}.json")
p.write_text(json.dumps(out, indent=1))
print(p.name, len(results), "ids; total", total)
