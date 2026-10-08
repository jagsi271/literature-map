# Brief: a literature map of urban, digital and urban–digital research

You are working for a PhD researcher in public policy (STS × urban policy) at IIT Delhi's
School of Public Policy. Build a large, reproducible, verified bibliography of three domains,
with a gap analysis and a map of emerging areas. Work in this repository, commit as you go,
and push your work to a branch named `literature-map`.

This is a **representative map, not an exhaustive census**. Urban studies alone runs to
millions of papers. Aim for roughly 3,000–5,000 deduplicated, relevant records that
capture each theme's landmark works, its recent work, and its India / South Asia work.

---

## 1. Domains and themes

Tag every record with one **domain** and one **primary theme** (plus an optional secondary
theme). Merge or split themes if the data shows a better structure, but explain any change.

**A. Urban (not primarily digital)**
A1 Urban governance, decentralisation & municipal finance ·
A2 Planning, master plans & land-use regulation ·
A3 Housing, informality & slums ·
A4 Eviction, resettlement & displacement ·
A5 Land, peri-urban & extended urbanisation ·
A6 Small towns, census towns & secondary cities ·
A7 Urban infrastructure (water, sanitation, energy) & infrastructural citizenship ·
A8 Mobility & transport (social science, not engineering) ·
A9 Public space, publicness & the street ·
A10 Urban economy, informal work & street vending ·
A11 Migration & the city ·
A12 Gender, caste, class & the city ·
A13 Heritage, mega-events & "world-class" city making ·
A14 Urban environment, climate & risk ·
A15 Urban & planning theory, Southern urbanism ·
A16 Night-time city & urban time

**B. Digital society (not primarily urban)**
B1 Platforms & platform capitalism ·
B2 Datafication, data justice & data colonialism ·
B3 Surveillance studies ·
B4 Algorithmic governance & AI in the public sector ·
B5 Digital identity & digital public infrastructure (DPI) ·
B6 Digital finance & payments ·
B7 Digital divides & digital inclusion ·
B8 Social media, digital publics & political communication ·
B9 Misinformation & extreme speech ·
B10 Cybercrime, fraud & cybersecurity (social science) ·
B11 Digital labour ·
B12 Infrastructure studies & STS of digital systems ·
B13 Mobile phones & everyday digital life ·
B14 Generative AI & society

**C. Urban × digital intersection**
C1 Smart cities & smart urbanism ·
C2 Platform urbanism ·
C3 Digital geographies & code/space ·
C4 Urban informatics & urban computing (tag critical vs technical) ·
C5 Urban data governance & data justice in cities ·
C6 Urban surveillance, policing & biometrics in public space ·
C7 Algorithmic & automated urban governance, municipal AI / GenAI ·
C8 City-level DPI & urban e-government ·
C9 Digital mobility (ride-hailing, MaaS, digital ticketing, transit apps) ·
C10 Proptech, housing platforms & short-term rentals ·
C11 Digital payments in urban economies (QR, UPI, mobile money) ·
C12 Civic tech, e-participation & digital urban publics ·
C13 Digital twins, simulation & visual rendering of cities ·
C14 Digital informality (informal settlements, vendors & digital systems) ·
C15 Gig work in the city (urban and spatial focus) ·
C16 Digital heritage, mapping & representation of cities ·
C17 Urban cybersecurity & cyber-physical infrastructure ·
C18 Neighbourhood platforms & digital public space (WhatsApp, Nextdoor, RWA groups)

## 2. Sources and rules

- **Primary source: OpenAlex API** (`api.openalex.org`). If an environment variable
  `OPENALEX_MAILTO` is set, add it as the `mailto` parameter. If OpenAlex requires an API
  key or keeps refusing requests, stop and report rather than working around it.
- **Crossref API** (`api.crossref.org`) to verify DOIs and fill missing metadata.
- **Semantic Scholar** only if reachable, sparingly; it rate-limits unauthenticated use.
- Do **not** scrape Google Scholar, Shodhganga, ResearchGate or publisher sites.
- **Every record must come from an API response.** Never add a reference from memory.
- Store metadata and abstracts only, never full texts of paywalled papers.
- Cache every raw API response under `data/raw/` so runs are reproducible and resumable.
- Be polite: throttle requests, back off on 429s, and resume from cache after failures.

## 3. Search strategy

For each theme, write 2–5 query strings in `queries.yaml` (title-and-abstract searches,
OpenAlex topic/concept filters where useful). For each theme collect three slices:

1. **Landmarks:** most-cited works, any year (about 40–60).
2. **Recent:** 2022–2026, by relevance (about 40–60).
3. **India / South Asia:** the same queries restricted to India or South Asian places
   (about 30–50). Also record whether any Delhi/NCR or Haryana city is named.

Then screen for relevance: a rule-based filter on title and abstract keywords, followed by
your own review of borderline records. Estimate precision on a random sample of 50 records
per stage and report it.

## 4. Record schema (one row per work)

ID · Title · Year · Authors · Venue · Document type · DOI · OpenAlex ID · Link · Open-access link ·
Cited-by count · Domain (A/B/C) · Primary theme · Secondary theme · Places studied ·
Region (Global North / China & East Asia / South Asia / Southeast Asia / Africa / Latin America /
Middle East / Multi-region / Not place-specific) · India flag · Delhi/NCR flag · Haryana flag ·
Method (qualitative / quantitative / mixed / review / conceptual / computational, inferred from
the abstract) · Landmark flag · Emerging flag · One-line summary (only from the abstract;
mark it "auto") · Stated gaps (sentences from the abstract about gaps, limits or future
research; mark "auto") · Shortlist tag (see below) · Screening confidence (high/medium/low)

**Shortlist tag:** mark records touching railway stations, waiting and waiting rooms,
night-time mobility or transit operating hours, fare integration or transit cards (NCMC),
rail-led urbanism, elevated rail or infrastructure undersides, or secondary cities in Haryana.
These are the researcher's current leads; do not let them bias the rest of the map.

Deduplicate by DOI, then by normalised title. Exclude retracted works.

## 5. Gap and emergence analysis

1. **Coverage matrix:** theme × region, theme × method, and theme × period
   (2010–14, 2015–19, 2020–26).
2. **Growth:** compare each theme's record counts in 2015–19 and 2020–26 (using OpenAlex
   counts for the queries, not just your sample) to find fast-growing themes.
3. **Emerging terms:** keywords or topics whose frequency rose fastest from 2018–21 to
   2022–26. List the top 30 with counts and example papers.
4. **Mismatch:** themes that are growing fast globally but thin in India or South Asia, and
   themes studied mostly in the Global North.
5. **Candidate gaps:** 25 specific gaps, each with the evidence (counts, three example
   papers, what is missing) and a caveat. Treat a gap as a lead to check, not a proof.

## 6. Outputs (commit all to `literature-map`)

- `outputs/bibliography.xlsx` with tabs: Read me · Records · Gap matrix (built with
  COUNTIFS formulas so it updates when rows are added) · Growth · Emerging terms ·
  Landmarks by theme · India subset · Shortlist.
- `outputs/bibliography.bib` and `outputs/bibliography.ris` for import into Zotero.
- `outputs/REPORT.md` (about 3,000–5,000 words): field map, landmark works per theme,
  saturated areas, emerging areas, gaps (global, South Asia, India, Haryana), and
  methodological gaps. Cite only works in the bibliography.
- `scripts/` with the code that produced everything, and `PROGRESS.md` with a log.

## 7. Verification (report the results)

- Resolve a random sample of 100 DOIs through Crossref and report the match rate.
- Hand-check 50 random records for theme and region tagging and report the error rate.
- List any themes where precision fell below 80% and what you did about it.

## 8. Stages (stop after each and report)

- **Stage 1 (pilot):** write `queries.yaml` for all themes, run three themes end to end
  (suggested: C2 platform urbanism, A9 public space, B5 digital identity & DPI), build the
  spreadsheet structure and report precision. Then **stop and wait for approval**.
- **Stage 2:** run all remaining themes, deduplicate, tag, and verify.
- **Stage 3:** gap and emergence analysis, report, final spreadsheet and exports.

Keep each stage's summary short: what you did, counts, precision, problems, next step.
