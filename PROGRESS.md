# Progress log

Read BRIEF.md first. This file says what is done, what is next, and what went wrong.

## Current stage: Stage 1 (pilot), in progress

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

### Next
- B5 digital identity & DPI: three slices, fetch, commit.
- Screening (`scripts/screen.py`): rule-based filter + manual review of borderline records.
- Tagging/record building (`scripts/build_records.py`), spreadsheet structure
  (`scripts/build_xlsx.py`), 50-record precision sample, Stage 1 report. Then stop for approval.

### Problems / notes
- Relevance ranking on OR-combined queries favours rare phrases (A9 recent is dominated by
  "privately owned public space"/"publicness" papers). Candidate fix for Stage 2: run the
  recent and India slices per query string (≈15 each) instead of one OR-combined search.
- Landmarks sorted by citations pull in highly cited works that only mention the terms
  (e.g. obesity, linguistic landscapes in A9); left for screening to remove.
- OpenAlex lists some books as "book-review" records (Choice Reviews) with the book's
  citations; these are excluded by document type in screening.
