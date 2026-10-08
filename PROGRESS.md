# Progress log

Read BRIEF.md first. This file says what is done, what is next, and what went wrong.

## Current stage: Stage 1 (pilot) complete — waiting for approval

### Done
- 2026-10-08 · API check. Crossref: OK (HTTP 200, 1 req/s limit). OpenAlex public API without a
  key: search/list requests refused (HTTP 429, shared free daily budget for this IP used up).
  Reported to the user; the user connected the **OpenAlex connector** (personal API key).
  Single-work lookups (`/works/W…`) on the public API are free and still work without a key.
- Pipeline design (because of the above):
  1. Searches run through the OpenAlex connector (`search_works`, one call at a time).
  2. The returned IDs + years, the exact query, parameters, canonical OQL and total count are
     stored per theme/slice in `data/raw/searches/{THEME}_{slice}.json`
     (`scripts/record_search.py`).
  3. `scripts/fetch_works.py` fetches each full work record from `api.openalex.org/works/{id}`
     through the single throttled fetcher (`scripts/fetcher.py`, ≥1 s between requests,
     backoff on 429/5xx) and caches the raw JSON in `data/raw/works/`. The fetched year is
     checked against the recorded year to catch ID transcription errors
     (`data/raw/searches/_id_check.json`).
- `queries.yaml` written for all 48 themes (192 query strings, 2–5 per theme) with screening rules.
- Query mode: **exact** (no stemming). OpenAlex "stemmed phrase" search only requires the words
  to co-occur: the first C2 landmark pull returned 98,726 hits topped by IoT/robotics papers.
  Exact mode gives 2,268 hits for C2 with relevant top results. Plural/spelling variants are
  listed explicitly instead.
- **C2 platform urbanism**: landmarks (2,268 hits), recent (1,801), India/South Asia (240);
  50 IDs each, all fetched, 0 ID problems.
- **A9 public space**: queries revised once (v1 bare "publicness"/"the street" → 67k hits incl.
  public-management and generic sociology; v2 requires an urban co-term → 63,280). Landmarks
  (63,280), recent (21,102), India (2,060); 50 IDs each, all fetched, 0 ID problems.

- **B5 digital identity & DPI**: queries revised once (v1 matched "state" in "state of the art"
  and bare "development": 12,035 hits, ~5/50 top results relevant; v2 uses policy co-terms →
  8,877). Landmarks (8,877), recent (5,271), India (2,833); 50 IDs each, all fetched, 0 ID
  problems (one work has no year in OpenAlex; recorded as year 0).

- Landmarks page 2 pulled for A9 and B5 (only 22 landmarks each survived screening from page 1).
- **Screening** (`scripts/build_records.py`, rules in `queries.yaml`): 550 candidates
  (theme × slice) → 308 rule-included, 212 borderline, 30 excluded (type/retracted/no core term).
  All 212 borderline candidates (202 unique work–theme pairs) reviewed by hand in
  `data/screening/manual_review.csv` (107 kept, 95 dropped, each with a note). Rules were
  tightened twice during the pilot: (1) core concept must be in the title or twice in the
  abstract, else manual review; (2) OpenAlex keyword tags dropped from screening text (they
  attached e.g. "digital identity" to education papers); (3) stub abstracts (book reviews filed
  as articles) go to review.
- **Records**: 374 deduplicated records (C2 127, A9 130, B5 117; 17 merges by DOI/title).
  Per slice after screening (a record can be in several): C2 landmarks 42 / recent 46 / India
  47; A9 42 / 47 / 45; B5 46 / 44 / 46. India flag 144, Delhi/NCR 12, Haryana 0, shortlist 1.
  60 records have no abstract in OpenAlex.
- **Precision (random 50, seed 20261008, `data/screening/precision_sample_stage1.csv`)**:
  in scope for the map 47/50 (94%); relevant to the assigned theme 41/50 (82%) — C2 20/23,
  A9 14/19 (74%), B5 7/8; region tag correct 41/47 (87%). Fixes after the sample: continent /
  world-region words added to the gazetteer and the 'Latin America' false-positive removed
  (4 of the 6 region errors now correct; the other 2 have no abstract); stub-abstract rule
  removed two book reviews.
- **Spreadsheet** `outputs/bibliography.xlsx` (`scripts/build_xlsx.py`): Read me, Records,
  Gap matrix (COUNTIFS on whole Records columns; verified by LibreOffice recalculation against
  Python counts), Growth (OpenAlex counts per period, global and South Asia, pilot themes),
  Emerging terms (structure only), Landmarks by theme, India subset, Shortlist.
- **Crossref pilot check** (`scripts/verify_crossref.py`, 25 random DOIs): 23/25 matched
  (title + year); the 2 misses are Zenodo DOIs (DataCite, not Crossref).

### Next
- **Waiting for approval of Stage 1** before Stage 2.
- Stage 2 plan: revise core/context screening terms for the other 45 themes as done for the
  pilot; run recent and India slices per query string (≈15 each) to avoid rare-phrase dominance;
  multi-theme primary assignment; Crossref abstract fill for records without abstracts;
  100-DOI Crossref check and 50-record hand check.

### Problems / notes
- Relevance ranking on OR-combined queries favours rare phrases (A9 recent is dominated by
  "privately owned public space"/"publicness" papers). Candidate fix for Stage 2: run the
  recent and India slices per query string (≈15 each) instead of one OR-combined search.
- Landmarks sorted by citations pull in highly cited works that only mention the terms
  (e.g. obesity, linguistic landscapes in A9); left for screening to remove.
- B5 landmarks by citation are still mixed (surveillance classics, fintech, livestock and
  cohort studies pulled in via keyword tags); B5 recent/India slices contain several Zenodo
  self-deposits, some posted 2–3 times under different DOIs (deduplicated by title).
- Random samples of the full B5 result set (not just top 50) are mostly off-topic: total hit
  counts overstate theme size. Matters for Stage 3 growth figures; see report.
- OpenAlex lists some books as "book-review" records (Choice Reviews) with the book's
  citations; these are excluded by document type in screening.
- A9 precision below 80% (74% on its 19 sampled records). Most errors are in-scope works that
  belong to themes not yet run (A12 gender, A13 heritage/monuments) or are "public space" in
  the political-theory sense (public sphere). Done: stub-abstract rule; manual exclusions noted.
  Stage 2: once A12/A13 run, primary theme is chosen across all themes that found a work;
  A9 core term "right to the city" and "public life" will require an urban co-term in the
  same sentence.
- Pilot themes absorb works from un-run themes (e.g. TikTok platformisation sits in C2 but is
  B1). This resolves in Stage 2 when all themes compete for primary assignment.
- Growth counts jump in 2025–26 for every theme (OpenAlex indexed many more repository/Zenodo
  records); Stage 3 must normalise by a baseline before calling a theme fast-growing.
- Method tag 'unclear' for 114 records (60 without abstract, 54 with no method cue).
- Crossref returned HTTP 500 intermittently; the fetcher's backoff handled it.
- OpenAlex sometimes attributes a book's citations to a review record (Choice Reviews,
  Contemporary Sociology); these are excluded and noted in manual_review.csv.
