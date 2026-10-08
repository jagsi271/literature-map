# Progress log

Read BRIEF.md first. This file says what is done, what is next, and what went wrong.

## Current stage: Stage 2 complete — waiting for approval

Stage 1 approved 2026-10-08 with eight changes for Stage 2 (direct API search with the
personal key; borderline < 25% per theme; blind precision check of 6 records per theme by a
separate subagent; recall test against seeds.csv; supplementary query set; growth-count
preparation; Repository-only flag; DataCite check for non-Crossref DOIs).

### Stage 2 report (short)
**What was done.** All 48 themes searched directly on the OpenAlex API (A1–A16, B1–B14, C1–C18;
the pilot themes kept their Stage 1 slices and gained per-query recent/India slices), screened
with rules v3, borderline cases decided by hand (`data/screening/manual_review.csv` now holds
1,791 hand decisions from Stages 1–2, each with a note), committed and pushed after each theme. Supplementary query set S1–S7, recall test, blind precision check,
100-DOI check and growth counts done.

**Counts.** 7,666 deduplicated records: 7,278 in the 48 themes (A 2,683 · B 2,434 · C 2,161;
60–217 per theme, fewest C18 60, C15 85, C3 88) and 388 found only by the supplementary
queries. India flag 2,049 · Delhi/NCR 338 · Haryana 83 · Shortlist tag 285 · Repository-only
919 · Landmark flag 2,233 · no abstract (confidence low) 1,680. This is above the brief's
3,000–5,000; see "Next".

**Borderline share** (change 2): every theme and supplementary set is under 25% under the
final rules (range 2%–23%; table below). Tightenings made on the way, each logged in
`queries.yaml`: auto-include/exclude rules calibrated on the Stage 1 hand decisions; landmark
records whose abstract OpenAlex withholds and whose title lacks the core term excluded (35/35
off-topic in A1/A2); B2 single mentions must be in the opening/aim sentences (26% → 16%);
C themes require an urban term or a named city (C6 40% → 15%, C15 46% → 5%, C12 31% → 12%,
C16 29% → 24%); supplementary sets S6/S7 exclude flagged records outright (39%/28% → 3%/2%).

**Precision** (change 3): 6 random records per theme (288), judged blind by three separate
agents that saw only title, abstract, venue and year plus the theme list (no screening data or
assigned themes; inputs and outputs in `data/screening/blind_check/`). In scope 254/288 (88%),
correct primary theme 233/288 (81%), region tag correct 246/288 (85%). Rule-included records
215/267 correct, hand-kept 18/21. By domain: A 79/96, B 75/84, C 79/108. Themes under 5/6:
A6, A7, A8, A13, B12, C7, C9, C13, C15, C16, C17, C18 (4/6 or 3/6) and C11, C14 (2/6) — six
records per theme give wide margins, so these are flags, not estimates. Main error types: (a)
biomedical/natural-science works that passed the rules (ferroelectric crystals, CT-scan data,
brain injury), (b) technical engineering works in C13/C16/C17, (c) rural works in urban
themes, (d) C-theme works the judge placed in the matching B theme (C11 → B6, C15 → B11).
**Done about it:** records whose OpenAlex primary-topic field is biomedical or a natural
science (Medicine, Materials Science, Chemistry, Agricultural & Biological Sciences, Energy …)
are now excluded unless kept by hand (in the sample 9 of 10 such records were wrong); this
removed 122 records, and on the 278 sampled records still in the map the figures are 91% in
scope / 83% correct theme. Engineering, Computer Science and Environmental Science records are
mixed (60 right / 22 wrong in the sample) and were left; type (b)–(d) errors remain.
**A9 re-check:** after themes compete for primary assignment, A9 is 5/6 on its random records
and 23/24 including the 18 Stage 1 sample records still in A9 (Stage 1: 14/19).

**Recall** (change 4): of 176 seeds, 165 resolve in OpenAlex (143 by DOI, 23 by title), 10 do
not, 1 is only in OpenAlex's expansion corpus (not searched). The first test found a pipeline
bug: OpenAlex runs unparenthesised `a OR b OR c AND d` as `c AND d` although the OQL it echoes
shows the intended reading; 17 queries in 12 themes were affected. They were rewritten with
explicit parentheses (`scripts/query_parens.py`), 9 queries were added for the query gaps the
seeds exposed (Delhi unauthorised/resettlement colonies, urban villages and private cities,
undercounted urbanisation, metro/suburban-rail ethnographies and fares, old-city heritage,
biometric enrolment, WhatsApp/Hindutva politics, mobile use in India, e-commerce freight;
"waiting for the state" in S2), and the affected slices were re-run. A second flaw: hand
exclusions noted "belongs to theme X" dropped works that theme X never retrieved; such works
(126 candidates) now move to theme X. Result: found 28 → 52, query gaps 42 → 12, screened out
3 → 1. The 12 remaining gaps are mostly outside the brief's theme list (national e-government
portals 3, public libraries 3, paper bureaucracy 2) plus 4 single works. **100 seeds match a
theme query but rank below the per-query cut-off** of the recent/India slices (top 15–25 by
relevance): recall of these niche India works is limited by sampling depth, not by the
queries. No seed was added directly. Table below; per-seed detail in
`data/screening/recall_seeds_stage2.csv`.

**Supplementary set** (change 5): S1 railway stations, S2 waiting/waiting rooms, S3 night-time
transit, S4 fare integration/NCMC, S5 rail-led urbanism/TOD, S6 elevated rail and undersides,
S7 Haryana secondary cities (Gurugram and Faridabad excluded). 388 records found only there
(tag Supplementary = Y, primary theme = the set's home theme); the Gap matrix COUNTIFS exclude
them. S2, S6 and S7 needed stricter rules (physics "waiting time", vibration engineering,
Rohtak medical studies).

**Growth counts for Stage 3** (change 6): `scripts/growth_counts.py` →
`data/processed/growth_counts.csv` and the Growth tab. Journal articles and book chapters in
journals/book series/ebook platforms only (repository records excluded), 2010–2026,
normalised per 10,000 Social Sciences works under the same filters (2026 partial, so only
shares are compared), and adjusted by each theme's precision on a random 40-record sample of
its full 2015–26 hit set (rules + hand keep-rate 0.42 for borderline, × rule-included
precision of the theme's domain from the blind check: A 0.81, B 0.88, C 0.74). Estimated
precision of full hit sets ranges 0.10 (C18) to 0.9, so raw hit counts would mislead.
Fastest relative growth 2015–19 → 2020–26: B14 (from ~0), C7, C15, B4, B1, C17, C2. Analysis
is for Stage 3.

**Repository-only flag** (change 7): 919 records (all merged versions in a repository or on a
preprint server); excluded from the Landmark flag and the Landmarks tab.

**DOI check** (change 8): 100 random record DOIs: 98 resolve in Crossref, 2 in DataCite
(api.datacite.org), 0 in neither; 96/100 match on title and year; the 4 misses have identical
titles and a publication year 2+ years apart (online-first vs issue year).
(`data/screening/crossref_check_stage2.csv`)

**API use.** 873 logged OpenAlex calls today (≈ 858 search-equivalents, $0.86 of the $1 daily
allowance), plus 3 unlogged test calls; 1,019 credits left when work stopped, above the 800
reserve. No connector calls were needed. The key does not appear in any committed file (checked
before every commit).

**Problems / caveats.** (1) Records total 7,666, above the 3,000–5,000 target. (2) C themes are
the weakest on precision (technical works; B/C boundary). (3) 1,680 records have no abstract
(mostly Elsevier, which OpenAlex does not distribute): they are screened on the title only and
their method/region tags are thin. (4) Recall of niche India works is limited by slice depth.
(5) Per-theme precision rests on 6 records each.

**Next (Stage 3), options for you to decide:** (a) keep all 7,666 records or trim to ~5,000
(e.g. drop no-abstract records without a title-level core match, or cap recent/India slices);
(b) deepen the India slices (≈ 2 searches per query, ~1,900 credits, one day's budget) if India
recall matters more than size; (c) hand-check the Engineering/Computer-Science records in the
C themes (~1,000) to lift C precision. Then gap and emergence analysis, report and exports.

### Stage 2 blind precision check, per theme (generated)
<!-- AUTO:PRECISION -->
| Theme | In scope | Correct theme | Region correct | Theme | In scope | Correct theme | Region correct |
|---|---|---|---|---|---|---|---|
| A1 | 6/6 | 6/6 | 5/6 | A2 | 6/6 | 5/6 | 6/6 |
| A3 | 6/6 | 6/6 | 5/6 | A4 | 5/6 | 5/6 | 6/6 |
| A5 | 6/6 | 5/6 | 4/6 | A6 | 6/6 | 4/6 ⚠ | 4/6 |
| A7 | 3/6 | 3/6 ⚠ | 6/6 | A8 | 4/6 | 3/6 ⚠ | 6/6 |
| A9 | 6/6 | 5/6 | 5/6 | A10 | 6/6 | 6/6 | 4/6 |
| A11 | 6/6 | 6/6 | 5/6 | A12 | 5/6 | 5/6 | 5/6 |
| A13 | 3/6 | 3/6 ⚠ | 6/6 | A14 | 6/6 | 6/6 | 4/6 |
| A15 | 6/6 | 6/6 | 6/6 | A16 | 5/6 | 5/6 | 4/6 |
| B1 | 6/6 | 6/6 | 6/6 | B2 | 6/6 | 6/6 | 5/6 |
| B3 | 5/6 | 5/6 | 5/6 | B4 | 5/6 | 5/6 | 4/6 |
| B5 | 5/6 | 5/6 | 6/6 | B6 | 5/6 | 5/6 | 5/6 |
| B7 | 6/6 | 6/6 | 6/6 | B8 | 6/6 | 6/6 | 5/6 |
| B9 | 6/6 | 6/6 | 4/6 | B10 | 6/6 | 6/6 | 6/6 |
| B11 | 6/6 | 6/6 | 5/6 | B12 | 3/6 | 3/6 ⚠ | 4/6 |
| B13 | 5/6 | 5/6 | 5/6 | B14 | 5/6 | 5/6 | 6/6 |
| C1 | 6/6 | 6/6 | 6/6 | C2 | 6/6 | 5/6 | 5/6 |
| C3 | 6/6 | 6/6 | 6/6 | C4 | 6/6 | 6/6 | 5/6 |
| C5 | 6/6 | 5/6 | 5/6 | C6 | 5/6 | 5/6 | 6/6 |
| C7 | 5/6 | 4/6 ⚠ | 6/6 | C8 | 6/6 | 6/6 | 4/6 |
| C9 | 5/6 | 4/6 ⚠ | 6/6 | C10 | 5/6 | 5/6 | 5/6 |
| C11 | 5/6 | 2/6 ⚠ | 6/6 | C12 | 6/6 | 6/6 | 5/6 |
| C13 | 3/6 | 3/6 ⚠ | 4/6 | C14 | 4/6 | 2/6 ⚠ | 6/6 |
| C15 | 6/6 | 4/6 ⚠ | 6/6 | C16 | 4/6 | 3/6 ⚠ | 4/6 |
| C17 | 4/6 | 3/6 ⚠ | 6/6 | C18 | 6/6 | 4/6 ⚠ | 2/6 |

All: in scope 254/288, correct theme 233/288, region 246/288 (sample drawn before the primary-topic-field rule; see log).
<!-- /AUTO:PRECISION -->

### Stage 2 recall against seeds.csv (generated)
<!-- AUTO:RECALL -->
| Seed category (seeds.csv) | Map themes | Seeds | found | below cut-off | query gap | screened out | not in OpenAlex | expansion corpus only |
|---|---|---|---|---|---|---|---|---|
| Mobility & transport | A8 C9 S1 S2 S3 S4 S5 S6 | 25 | 5 | 15 | 2 | 0 | 3 | 0 |
| Smart city & digital governance | C1 C5 C7 C8 | 19 | 4 | 11 | 3 | 0 | 1 | 0 |
| Platforms & gig economy | B1 B11 C2 C15 | 19 | 9 | 10 | 0 | 0 | 0 | 0 |
| Housing, resettlement & informality | A3 A4 C14 | 15 | 4 | 10 | 0 | 1 | 0 | 0 |
| Heritage, events & world-class city | A13 C16 | 12 | 4 | 7 | 1 | 0 | 0 | 0 |
| Land, peri-urban & private cities | A5 A2 | 11 | 3 | 7 | 0 | 1 | 0 | 0 |
| Small towns & census towns | A6 S7 | 10 | 5 | 3 | 0 | 0 | 2 | 0 |
| Welfare technology & identity | B5 B4 | 9 | 3 | 5 | 0 | 0 | 1 | 0 |
| Digital finance & payments | B6 C11 | 8 | 0 | 8 | 0 | 0 | 0 | 0 |
| Digital divide & access | B7 B13 | 8 | 3 | 5 | 0 | 0 | 0 | 0 |
| Bureaucracy, waiting & documents | B5 A1 S2 | 7 | 3 | 1 | 2 | 0 | 0 | 1 |
| Digital publics & social media | B8 C12 C18 | 6 | 3 | 2 | 1 | 0 | 0 | 0 |
| Cybercrime & fraud | B10 C17 | 6 | 0 | 6 | 0 | 0 | 0 | 0 |
| Gender & public space | A9 A12 | 6 | 2 | 2 | 0 | 0 | 2 | 0 |
| Knowledge access & libraries | B7 | 6 | 0 | 2 | 3 | 0 | 1 | 0 |
| Neighbourhoods, RWAs & civil society | C18 A1 | 5 | 3 | 2 | 0 | 0 | 0 | 0 |
| Surveillance & security | B3 C6 | 2 | 0 | 2 | 0 | 0 | 0 | 0 |
| Street vending & informal economy | A10 C14 | 2 | 0 | 2 | 0 | 0 | 0 | 0 |
| **All** | | 176 | 51 | 100 | 12 | 2 | 10 | 1 |

Found seeds by the map's primary theme: A3 2, A4 1, A5 4, A6 5, A8 5, A9 1, A13 4, A16 3, B5 4, B8 2, B11 3, B13 3, C1 3, C2 4, C8 1, C15 2, C18 4.
<!-- /AUTO:RECALL -->

### Stage 2 log
- 2026-10-08 · Branch: continued from `literature-map` (merged `main` for seeds.csv).
- **Direct API.** `scripts/fetcher.py` sends `OPENALEX_API_KEY` as `api_key`; the key is
  stripped from every logged URL/error and responses are refused for caching if they contain
  it. `scripts/run_search.py` writes manifests (IDs, years, totals, OQL) straight from API
  responses; raw responses are cached gzipped in `data/raw/api/` and double as the stored work
  records (`data/raw/works_index.json`). Every call is logged in `data/raw/api_ledger.csv`; the
  fetcher pauses when fewer than 800 credits remain (free key: 10,000 credits/day; search = 10).
  Check: the direct API reproduces the pilot's C2 count (2,273 vs 2,268 via the connector).
- **Search field.** Stage 2 searches title + abstract (`title_and_abstract.search.exact`).
  In the first A1 run, `title_abstract_keywords` let OpenAlex keyword tags alone pull
  highly cited works that never use the term into landmarks (e.g. Jacobs 1961 tagged "urban
  governance"); A1 was re-run (18 → 37 rule-kept landmarks before review).
- **Slices.** Landmarks: OR-combined query, top 100 by citations. Recent (2022–26) and India:
  one search per query string (fixes Stage 1's rare-phrase dominance), 70 per slice per theme
  (A1: 100).
- **Screening rules v3** (header of `queries.yaml`): calibrated on the 202 Stage 1 hand
  decisions (e.g. core term in the title of a record without abstract: 46/53 kept by hand →
  auto-include, low confidence; flag match without core in title: 1/16 kept → auto-exclude;
  core once in abstract and not in keyword tags: 3/19 kept → auto-exclude). Core terms for
  the other 45 themes are now theme-specific phrases. A hand decision on a work–theme pair
  overrides the rules. Pilot themes under v3: borderline A9 22%, B5 23%, C2 13%.
- Later additions (all in `queries.yaml` / `scripts/build_records.py` comments): shared-abstract
  guard (an abstract attached to works with different titles is ignored — one platform-work
  abstract sat on four 1980s Annual Review articles); C-theme urban-context rule; B3 query
  restricted to social-science "surveillance studies"; C6/C7/C18 flags for computer vision,
  "AI/AN" and waste-engineering ML, and medical "residents"; landmarks page 2 for A6; query
  parenthesis fix and recall additions; hand-move rule; primary-topic-field rule.

### Stage 2 per-theme screening (generated by `scripts/stage2_log.py`)
<!-- AUTO:SCREENING -->
| Theme | Name | Candidates | Rule incl. | Borderline (share) | Hand kept / dropped | Records found | Primary here |
|---|---|---|---|---|---|---|---|
| A1 | Urban governance, decentralisation & municipa | 264 | 187 | 30 (11%) | 12 / 18 | 176 | 170 |
| A2 | Planning, master plans & land-use regulation | 239 | 165 | 11 (5%) | 3 / 8 | 161 | 243 |
| A3 | Housing, informality & slums | 265 | 171 | 43 (16%) | 17 / 26 | 175 | 170 |
| A4 | Eviction, resettlement & displacement | 219 | 165 | 16 (7%) | 8 / 8 | 165 | 158 |
| A5 | Land, peri-urban & extended urbanisation | 277 | 162 | 21 (8%) | 10 / 11 | 169 | 166 |
| A6 | Small towns, census towns & secondary cities | 364 | 150 | 23 (6%) | 11 / 12 | 157 | 205 |
| A7 | Urban infrastructure (water, sanitation, ener | 242 | 154 | 21 (9%) | 9 / 12 | 160 | 185 |
| A8 | Mobility & transport (social science) | 274 | 196 | 21 (8%) | 7 / 14 | 199 | 274 |
| A9 | Public space, publicness & the street | 287 | 188 | 36 (12%) | 21 / 15 | 212 | 211 |
| A10 | Urban economy, informal work & street vending | 228 | 152 | 24 (10%) | 11 / 13 | 166 | 163 |
| A11 | Migration & the city | 236 | 173 | 19 (8%) | 8 / 11 | 169 | 165 |
| A12 | Gender, caste, class & the city | 233 | 160 | 21 (9%) | 11 / 10 | 169 | 164 |
| A13 | Heritage, mega-events & "world-class" city ma | 246 | 176 | 21 (8%) | 11 / 10 | 184 | 182 |
| A14 | Urban environment, climate & risk | 246 | 193 | 29 (12%) | 10 / 19 | 192 | 189 |
| A15 | Urban & planning theory, Southern urbanism | 233 | 144 | 39 (17%) | 24 / 15 | 159 | 155 |
| A16 | Night-time city & urban time | 241 | 121 | 29 (12%) | 17 / 12 | 134 | 211 |
| B1 | Platforms & platform capitalism | 239 | 177 | 33 (14%) | 16 / 17 | 186 | 167 |
| B2 | Datafication, data justice & data colonialism | 240 | 149 | 36 (15%) | 19 / 17 | 162 | 158 |
| B3 | Surveillance studies | 229 | 152 | 30 (13%) | 11 / 19 | 156 | 147 |
| B4 | Algorithmic governance & AI in the public sec | 240 | 200 | 13 (5%) | 4 / 9 | 184 | 184 |
| B5 | Digital identity & digital public infrastruct | 298 | 203 | 50 (17%) | 16 / 34 | 203 | 199 |
| B6 | Digital finance & payments | 217 | 181 | 13 (6%) | 8 / 5 | 187 | 187 |
| B7 | Digital divides & digital inclusion | 236 | 183 | 26 (11%) | 15 / 11 | 181 | 177 |
| B8 | Social media, digital publics & political com | 272 | 217 | 22 (8%) | 16 / 6 | 220 | 217 |
| B9 | Misinformation & extreme speech | 238 | 159 | 44 (18%) | 29 / 15 | 180 | 179 |
| B10 | Cybercrime, fraud & cybersecurity (social sci | 240 | 172 | 24 (10%) | 10 / 14 | 173 | 173 |
| B11 | Digital labour | 238 | 203 | 12 (5%) | 8 / 4 | 204 | 196 |
| B12 | Infrastructure studies & STS of digital syste | 239 | 138 | 39 (16%) | 16 / 23 | 149 | 146 |
| B13 | Mobile phones & everyday digital life | 269 | 153 | 28 (10%) | 7 / 21 | 154 | 151 |
| B14 | Generative AI & society | 237 | 146 | 26 (11%) | 9 / 17 | 153 | 153 |
| C1 | Smart cities & smart urbanism | 219 | 187 | 15 (7%) | 3 / 12 | 199 | 194 |
| C2 | Platform urbanism | 246 | 191 | 21 (8%) | 12 / 9 | 195 | 181 |
| C3 | Digital geographies & code/space | 199 | 81 | 22 (11%) | 10 / 12 | 91 | 88 |
| C4 | Urban informatics & urban computing | 227 | 126 | 20 (9%) | 9 / 11 | 132 | 123 |
| C5 | Urban data governance & data justice in citie | 230 | 117 | 44 (19%) | 11 / 33 | 125 | 115 |
| C6 | Urban surveillance, policing & biometrics in  | 240 | 104 | 37 (15%) | 12 / 25 | 115 | 112 |
| C7 | Algorithmic & automated urban governance, mun | 226 | 123 | 33 (15%) | 6 / 27 | 127 | 120 |
| C8 | City-level DPI & urban e-government | 217 | 114 | 31 (14%) | 13 / 18 | 129 | 121 |
| C9 | Digital mobility (ride-hailing, MaaS, digital | 227 | 126 | 19 (8%) | 6 / 13 | 130 | 186 |
| C10 | Proptech, housing platforms & short-term rent | 226 | 144 | 34 (15%) | 7 / 27 | 146 | 144 |
| C11 | Digital payments in urban economies (QR, UPI, | 218 | 110 | 13 (6%) | 3 / 10 | 108 | 100 |
| C12 | Civic tech, e-participation & digital urban p | 239 | 87 | 28 (12%) | 13 / 15 | 98 | 92 |
| C13 | Digital twins, simulation & visual rendering  | 228 | 151 | 18 (8%) | 7 / 11 | 157 | 153 |
| C14 | Digital informality (informal settlements, ve | 191 | 113 | 29 (15%) | 9 / 20 | 112 | 103 |
| C15 | Gig work in the city (urban and spatial focus | 222 | 108 | 10 (4%) | 7 / 3 | 107 | 85 |
| C16 | Digital heritage, mapping & representation of | 213 | 120 | 49 (23%) | 15 / 34 | 128 | 126 |
| C17 | Urban cybersecurity & cyber-physical infrastr | 228 | 110 | 40 (18%) | 13 / 27 | 123 | 118 |
| C18 | Neighbourhood platforms & digital public spac | 217 | 56 | 30 (14%) | 6 / 24 | 61 | 60 |
| S1 | Railway stations | 126 | 75 | 11 (9%) | 4 / 7 | 79 | 0 |
| S2 | Waiting and waiting rooms | 127 | 30 | 11 (9%) | 5 / 6 | 32 | 0 |
| S3 | Night-time transit and transit operating hour | 105 | 46 | 5 (5%) | 2 / 3 | 47 | 0 |
| S4 | Fare integration and transit cards (incl. NCM | 127 | 66 | 24 (19%) | 7 / 17 | 70 | 0 |
| S5 | Rail-led urbanism and transit-oriented develo | 119 | 89 | 10 (8%) | 6 / 4 | 94 | 0 |
| S6 | Elevated rail and infrastructure undersides | 118 | 32 | 3 (2%) | 3 / 0 | 34 | 0 |
| S7 | Haryana secondary cities (excluding Gurugram  | 109 | 44 | 2 (2%) | 1 / 1 | 50 | 0 |

Total deduplicated records: 7666.
<!-- /AUTO:SCREENING -->

### OpenAlex API usage (generated from `data/raw/api_ledger.csv`)
<!-- AUTO:API -->
| UTC day | Calls by this pipeline | Cost (USD) | ≈ searches | Credits left at last call |
|---|---|---|---|---|
| 2026-10-08 | 873 | 0.858 | 858 | 1019 |
<!-- /AUTO:API -->

## Stage 1 (pilot) — approved

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
