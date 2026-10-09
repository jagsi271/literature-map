# Literature map: urban, digital and urban × digital research

**Stage 3 report.** Rendered by `scripts/stage3_analysis.py` from `scripts/report_template.md`;
every number comes from the repository's data files (counts retrieved 8–9 October 2026).
Records are cited as Author (Year) [ID], the ID being the record's row in
`outputs/bibliography.xlsx`. Only works in the bibliography are cited.

## 1. What the analysis rests on

**The map.** {{stat:records}} deduplicated records: {{stat:records_themes}} in the 48 themes and
{{stat:records_supp}} found only by the supplementary query set for the researcher's leads
(S1–S7). {{stat:india}} name an Indian place, {{stat:delhi}} Delhi/NCR and {{stat:haryana}}
Haryana. Each theme was searched in three slices — most-cited works, 2022–26 works by relevance,
and India/South Asia works by relevance (two pages per query) — and screened by rules and by
hand. A blind check of six random records per theme found 88% in scope and 81% with the right
primary theme, weakest in the technical-leaning C themes. Of 176 seed works chosen by the
researcher, {{stat:recall_found}} are in the map, {{stat:recall_below}} match a theme query but
rank below the slice cut-off, {{stat:recall_gap}} match no query, {{stat:recall_out}} were
screened out and {{stat:recall_outside}} are outside OpenAlex's searched corpus. The most-cited records of every theme were read by hand and clearly off-topic
works removed.

**Two kinds of evidence.** The map is a designed sample: every theme has an India slice and a
2022–26 slice, so counting records by region or period would measure the design. Therefore:

- **Gap, growth and mismatch claims rest on population counts**: OpenAlex-wide counts of each
  theme's combined query (title + abstract, exact phrases), journal articles and book chapters
  only, 2010–2026, each multiplied by the theme's estimated precision (a random 40-work sample of
  its hit set screened with its own rules; median {{stat:p_median}}, range
  {{stat:p_min}}–{{stat:p_max}}; South Asia, India, Delhi and Haryana counts use a separate
  sample of the South Asia hit set). Growth is normalised per 10,000 Social Sciences works under
  the same filters; 2026 is a partial year, so only shares are compared. Places are read from
  titles and abstracts. Every count is given for all venues and for core venues only (sources
  OpenAlex flags as core).
- **Records are used only as examples** (three per gap), for landmarks, and for method shares,
  which OpenAlex does not record. The "Sample coverage" tab (formerly "Gap matrix") describes the
  sample, not the literature.

**Coverage limits.** OpenAlex is thin exactly where much Indian urban and policy writing
appears:

{{table:coverage}}

Every India, Delhi/NCR or Haryana claim below carries this caveat.

## 2. Field map

Among the urban themes, housing, informality and slums (A3, {{v:A3.global_all_2020-26_adj}}
adjusted works in 2020–26), urban governance (A1, {{v:A1.global_all_2020-26_adj}}) and planning
(A2, {{v:A2.global_all_2020-26_adj}}) are the largest; urban theory (A15,
{{v:A15.global_all_2020-26_adj}}) and the night-time city (A16, {{v:A16.global_all_2020-26_adj}})
the smallest. The digital-society themes include the largest of all: generative AI (B14,
{{v:B14.global_all_2020-26_adj}}, almost all since 2023), misinformation (B9,
{{v:B9.global_all_2020-26_adj}}), digital finance (B6, {{v:B6.global_all_2020-26_adj}}) and
cybercrime (B10, {{v:B10.global_all_2020-26_adj}}). The urban × digital themes are small: only
smart cities (C1, {{v:C1.global_all_2020-26_adj}}) matches the larger urban themes. Most C themes
hold between 3% and a third of the work in their nearest digital-society theme:

{{table:intersections}}

The urban turn of platform, labour and payment research is recent and small (C2, C15 and C11
against B1, B11 and B6). City e-government (C8) is larger than its digital parent because it is
an older, policy-led field. Digital geographies (C3), digital heritage and mapping (C16),
digital informality (C14), urban data governance (C5), civic tech (C12) and neighbourhood
platforms (C18) are the smallest corners, each about 500 adjusted works or fewer in seven years.

## 3. Landmark works per theme

The two most-cited landmark-slice records per theme (repository-only records excluded; a few
off-theme records passed over are listed in `data/analysis/report_choices.yaml`). Citation
counts favour older, English-language, Global North work; the gap examples below balance this.

{{table:landmarks}}

## 4. Growth and saturation

Growth is the change in a theme's share of all Social Sciences works from 2015–19 to 2020–26
("new" below 50 adjusted works in 2015–19); 1 means the theme kept pace with the social
sciences.

**Fast-growing themes** (ratio ≥ 3 or new, all venues): {{stat:n_fast}} of 48, all digital-society
or urban × digital themes. {{stat:n_fast_core}} of them also grow at least threefold in core
venues; for {{stat:n_core_lower}} of the {{stat:n_core_both}} themes with both ratios, growth is
slower in core venues than in all venues, i.e. faster outside core venues.

{{table:fast}}

Generative AI (B14), municipal AI (C7) and urban gig work (C15) are effectively new fields.
Algorithmic governance (B4, ×{{v:B4.global_all_growth}}) and platforms (B1,
×{{v:B1.global_all_growth}}) grew from small bases into large literatures, and their urban
versions (C7, C2) followed. The shares of digital finance (B6), digital divides (B7) and
misinformation (B9) grew five- to sevenfold from already large bases. No urban theme reaches ×3;
urban environment and climate (A14, ×{{v:A14.global_all_growth}}) and mobility (A8,
×{{v:A8.global_all_growth}}) grow fastest.

**Saturating or flat themes** (ratio ≤ 1.3):

{{table:saturating}}

Housing and informality (A3), migration (A11) and heritage and mega-events (A13) are large and
only keep pace: mature fields. Digital geographies and code/space (C3) is the only theme whose
share fell, perhaps because its questions moved under platform urbanism (C2) and smart urbanism
(C1). Urban theory (A15) is small and flat,
though "southern urbanism" is among the rising terms (Section 5).

## 5. Emerging terms

Terms are the OpenAlex keywords on the map's records, ranked by the change in their **share of
each period's records** (2018–21 vs 2022–26), not raw counts, because the sample's period mix is
fixed by design; a term needs 15 records in 2022–26 in at least two themes. Each term was checked
OpenAlex-wide (its share of all Social Sciences works) and terms whose share also rose by more
than 20% ("confirmed") are listed first. Examples are 2022–24 records with the highest
field-weighted citation impact; 2025–26 works are left out of all FWCI-based signals, including
the spreadsheet's Emerging flag, because their citations are too young.

{{table:emerging}}

Four clusters dominate. **Generative AI** (generative AI, large language models, ChatGPT,
foundation models, AI regulation) moves from nothing to about 3% of recent records. **Indian
digital public infrastructure** (UPI, digital public infrastructure, Direct Benefit Transfer)
rises in B5, C8 and C11. **Indian privacy and data-protection law** (the Digital Personal Data
Protection Act 2023, the Puttaswamy judgment, the IT Act 2000, proportionality) rises in B3 and
B4. These two Indian clusters also rise OpenAlex-wide, but the deeper India slices amplify them
in the sample. **Platform logistics and surveillance in the city** (gig workers, last-mile
delivery, urban logistics, face recognition) rises in C2, C15 and C6. Terms that rose in the
sample but not OpenAlex-wide (for example land-use regulation, the night-time economy) are left
unconfirmed.

## 6. Mismatch

**Fast globally, thin in South Asia.** South Asian places are named in
{{v:SS.sa_share_all_2020-26}} of all Social Sciences works in 2020–26
({{v:SS.sa_share_core_2020-26}} in core venues). The location quotient (LQ) divides a theme's
South Asia share by that baseline. Most urban and development themes sit well above 1, so the
informative cases are the themes with the lowest South Asia share:

{{table:mismatch}}

{{stat:n_mismatch}} themes are both fast-growing worldwide and at or below a 5% South Asia share:
{{stat:mismatch_list}}. Generative AI, digital twins, datafication, digital mobility and urban data
governance become gaps S1, S2, S5, S4 and (for India) I3. Misinformation does not: its South
Asia volume ({{v:B9.sa_all_2020-26_adj}} adjusted works) is large in absolute terms. Nor do
platforms: South Asian platform research sits largely in digital labour and urban gig work
(B11, C15), where South Asia's share is {{v:B11.sa_share_all_2020-26}} and
{{v:C15.sa_share_all_2020-26}}. The reverse also holds: digital identity and DPI
(B5, {{v:B5.sa_share_all_2020-26}}), payments in urban economies (C11,
{{v:C11.sa_share_all_2020-26}}) and gender, caste and class in the city (A12,
{{v:A12.sa_share_all_2020-26}}) are fields where South Asia leads.

**Themes studied mostly in the Global North.** Share of each region among all region mentions
(2010–26, all venues, adjusted; a work naming two regions counts for both):

{{table:gn}}

The Global North accounts for about half or more of the region mentions in proptech and
short-term rentals (C10, {{v:C10.gn_share_of_region_mentions}}), digital geographies (C3,
{{v:C3.gn_share_of_region_mentions}}), the night-time city (A16,
{{v:A16.gn_share_of_region_mentions}}) and digital twins (C13, {{v:C13.gn_share_of_region_mentions}}),
and nearly half in datafication (B2), surveillance studies (B3), civic tech (C12) and algorithmic
governance (B4): in these themes most place-specific work is about Northern cities. Fourteen themes
are led by another region: South Asia leads A12, B5, B6, B13, C11, C14, C15 and C18; Africa
leads peri-urban land, infrastructure and the informal urban economy (A5, A7, A10); China and
East Asia lead migration (A11) and urban computing (C4); Southeast Asia leads city e-government
(C8).

**India.** Indian places are named in {{v:SS.india_share_all_2020-26}} of all Social Sciences
works in 2020–26 ({{v:SS.india_share_core_2020-26}} in core venues). The themes with the lowest
India share:

{{table:india}}

Two patterns stand out. First, the India-thin themes are the computational and
Northern-framed corners of the map (proptech, urban informatics, digital twins, generative AI,
datafication) plus, among urban themes, the night-time city, planning and land-use regulation,
and public space. Second, India's share drops sharply from all venues to core venues for
{{stat:india_core_low}}: on these topics Indian work is more often published outside core
venues than work on other places.

## 7. Candidate gaps

Twenty-five leads, each with population-count evidence (all venues and core venues), three
example records (titles in the Candidate gaps tab) and a caveat. A gap means a topic is thin in
OpenAlex relative to its neighbours or to the rest of the world: a lead to check, not a proof. Four provisional India and Delhi gaps of the
draft were dropped once the India and Delhi counts came in (municipal AI, urban surveillance and
urban cybersecurity in India; digital mobility in Delhi), because India's or Delhi's share of
those themes is above its share of all social science works.

### 7.1 Global

{{gaps:global}}

### 7.2 South Asia

{{gaps:south_asia}}

### 7.3 India

{{gaps:india}}

### 7.4 Delhi/NCR and Haryana

{{gaps:delhi_haryana}}

## 8. Methodological gaps

Method is inferred from abstracts by keyword cues and is known for {{stat:known_methods}} of
{{stat:records_themes}} theme records; shares below are among records with a known method, with
the n. No method claim is made where fewer than 50 records have a known method (one theme,
C18). Per-theme shares are in the Methods tab.

{{table:methods_compact}}

The urban themes lean qualitative and conceptual; the C themes carry most computational work
({{v:C.method_computational_pct}} of known-method C records). India-flagged urban records are
less often quantitative than Global North ones ({{v:IN_A.method_quantitative_pct}} against
{{v:GN_A.method_quantitative_pct}}), while in the C themes the order reverses
({{v:IN_C.method_quantitative_pct}} against {{v:GN_C.method_quantitative_pct}}); these are
differences within the sample. Three gaps stand out:

{{gaps:method}}

## 9. Shortlist leads (S1–S7)

The researcher's leads were searched separately so as not to bias the map. OpenAlex-wide counts
(same filters, precision-adjusted with a 40-work sample of each set's India hit set, which is
small for S3 and S4) and the map's records:

{{table:shortlist}}

India-flagged records per lead (S7: Haryana-flagged), by method (inferred; known n) and venue
type. Method shares support no claim where fewer than 50 records have a known method (all leads
except S5):

{{table:shortlist_india}}

**Railway stations (S1).** India-named station research is mostly transport planning — transfer
facilities, willingness to pay, service quality — and engineering. The strongest qualitative work
treats stations as social spaces: {{cite:W3193675826}} on caste, waste and cleaning labour, and
{{cite:W4380875513}} on waiting. Haryana-named station work is almost absent
({{sl:S1.haryana_all_adj}} adjusted works). Missing: stations as public and labour spaces, and
suburban and NCR stations.

**Waiting (S2).** The India work is on waiting for the state, not in transit:
{{cite:W2889381623}}, {{cite:W4296837992}} and {{cite:W4401334352}}, alongside *Timepass*,
{{cite:W633285982}}. The OpenAlex count is uncertain (estimated precision
{{sl:S2.p}}: most "waiting" hits are queueing models). Missing: waiting rooms, platforms and bus
stops as social and temporal experience.

**Night-time transit (S3).** Near-absent worldwide ({{sl:S3.global_all_adj}} adjusted works,
{{sl:S3.india_all_adj}} India-named). The India records are on night-time fear and the night
economy — {{cite:W7124766099}}, {{cite:W4377027842}} — not on night transport. Missing: night bus
services and operating hours, night-shift commuting, women's travel after dark.

**Fare integration and transit cards (S4).** {{sl:S4.india_all_adj}} India-named adjusted works
({{sl:S4.india_core_adj}} in core venues); the India-flagged records include no core-venue
journal article, and no record in the map names the National Common Mobility Card in its title
or abstract. The nearest are {{cite:W3195574909}}, a case study of fare integration in Ahmedabad, and
{{cite:W1560868062}}, a thesis on integrating rickshaws with BRT in Dhaka. Missing: the social science of NCMC and fare integration — who
gains, fare policy, data.

**Rail-led urbanism and TOD (S5).** The best-covered lead: India accounts for
{{sl:S5.india_all_adj}} of {{sl:S5.global_all_adj}} adjusted works worldwide. Most India work sets
planning criteria (influence zones, land value capture); the strongest qualitative and policy studies are {{cite:W3180616926}} on
metro-TOD policy, {{cite:W1892601992}} on Mumbai and {{cite:W2505890949}} on East Delhi's metro.
Missing: TOD and value capture in Haryana (Gurugram, the RRTS corridor) and corridor
displacement.

**Elevated rail and undersides (S6).** India-named: {{sl:S6.india_all_adj}} adjusted works, mostly
engineering. One strong qualitative work: {{cite:W2790024163}} on Mumbai's flyovers and
skywalks. Missing: undersides as livelihood and shelter spaces, and elevated metros and street
life.

**Haryana secondary cities (S7).** {{sl:S7.global_all_adj}} adjusted works name these cities with
urban content ({{sl:S7.global_core_adj}} in core venues). Most Haryana-flagged records in the
map are urban-growth mapping, air-quality and waste studies; the social-science works are few
and descriptive: {{cite:W659497186}},
{{cite:W2609601743}}, {{cite:W4399084735}}. Missing: governance, economy, everyday life and
digital change in these cities (gap H1).

## 10. Limits

- **Precision.** Counts are adjusted by 40-work samples, and the blind check behind the domain
  factors used six records per theme; it predates the India page-2 records (about a fifth of the
  map), which went through the same rules and hand review. Least certain: C18 (estimated precision {{v:C18.p}}), C6
  ({{v:C6.p}}), C11 ({{v:C11.p}}), C15 ({{v:C15.p}}), C3 ({{v:C3.p}}) and lead S2.
- **Place signal.** Places come from titles and abstracts, not affiliations; works naming no
  place count for no region, which matters most for generative AI and conceptual themes.
- **Coverage.** Indian venues and theses are under-covered (Section 1); about a fifth of the
  records have no abstract, and their method and region tags are thin.
- **Vocabulary.** Exact-phrase queries miss work that uses other words; each gap names the
  likely blind spot.
