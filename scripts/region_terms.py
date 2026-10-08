"""Place-name search terms per region for OpenAlex population counts (Stage 3).

Built from scripts/gazetteer.py (countries, unambiguous demonyms, cities, world-region words) so
that population counts use the same notion of 'place studied' as the record tags. South Asia
keeps the Stage 2 list in queries.yaml (south_asia_terms) so Stage 2 and Stage 3 counts match.
Ambiguous words are left out: America/American (also 'Latin American'), Georgia, Jordan.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gazetteer as gz  # noqa: E402

REGION_WORDS = {
    gz.GN: ["Europe", "European", "Scandinavia", "Scandinavian", "Nordic", "North America",
            "North American", "United States", "USA"],
    gz.EA: ["East Asia", "East Asian"],
    gz.SEA: ["Southeast Asia", "Southeast Asian", "South-East Asia", "ASEAN"],
    gz.AF: ["Africa", "African", "sub-Saharan"],
    gz.LA: ["Latin America", "Latin American", "South America", "Central America", "Caribbean"],
    gz.ME: ["Middle East", "Middle Eastern", "MENA", "Gulf states", "Central Asia"],
}
SKIP = {"America", "American", "Georgia", "Jordan", "U.S.", "UK", "UAE"}


def terms_for(region):
    out = list(REGION_WORDS.get(region, []))
    countries = {c for c, r in gz.COUNTRIES.items() if r == region}
    out += sorted(countries)
    out += sorted(a for a, c in gz.ALIASES.items() if c in countries)
    out += sorted(city for city, c in gz.CITIES.items() if c in countries)
    seen, res = set(), []
    for t in out:
        if t in SKIP or t in seen:
            continue
        seen.add(t)
        res.append(t)
    return res


def or_query(terms):
    return " OR ".join(f'"{t}"' if " " in t or "-" in t else t for t in terms)


INDIA = ["India", "Indian"] + sorted({c for c, k in gz.CITIES.items() if k == "India"})
DELHI = [t for t in gz.DELHI_NCR if t not in ("NCR",)]
HARYANA = list(gz.HARYANA)

if __name__ == "__main__":
    for reg in (gz.GN, gz.EA, gz.SEA, gz.AF, gz.LA, gz.ME):
        t = terms_for(reg)
        print(reg, len(t), len(or_query(t)))
    print("India", len(INDIA), len(or_query(INDIA)), "| Delhi", len(DELHI), "| Haryana", len(HARYANA))
