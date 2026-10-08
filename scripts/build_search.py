"""Print the exact search string for a theme and slice, built from queries.yaml.

Usage: python3 scripts/build_search.py C2 landmarks
The printed string is what is sent as `query` to the OpenAlex connector's search_works
(keyword mode, search_in = title_abstract_keywords). Slice parameters (sort, years,
limit) are printed too; scripts/record_search.py stores them with the returned IDs.
"""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load():
    return yaml.safe_load((ROOT / "queries.yaml").read_text())


def search_string(cfg, theme, slice_name):
    qs = cfg["themes"][theme]["queries"]
    core = " OR ".join(f"({q})" for q in qs)
    if slice_name == "india":
        sa = " ".join(cfg["south_asia_terms"].split())
        return f"({core}) AND ({sa})"
    return core


if __name__ == "__main__":
    cfg = load()
    theme, sl = sys.argv[1], sys.argv[2]
    print(json.dumps({"query": search_string(cfg, theme, sl), "mode": cfg["mode"], **cfg["slices"][sl]}, indent=1))
