# Literature map: urban, digital and urban × digital research

**Stage 3 report — draft.** Rendered by `scripts/stage3_analysis.py` from this template
(`scripts/report_template.md`); every number below comes from the repository's data files.
Status of the inputs: all-venue global and South Asia counts are in; India, Delhi/NCR,
Haryana, other-region and core-venue counts are **{{stat:india_counts_status}}** (they are
fetched after the OpenAlex daily budget resets, together with the second page of the India
slices). Where a number reads "pending", that count has not been fetched yet; gaps marked
*provisional* depend on it.

Records are cited as Author (Year) [ID], where the ID is the record's row in
`outputs/bibliography.xlsx` (tab Records). Only works in the bibliography are cited.

## 1. What the analysis rests on

**The map.** {{stat:records}} deduplicated records: {{stat:records_themes}} in the 48 themes and
{{stat:records_supp}} found only by the supplementary query set (S1–S7). {{stat:india}} name an
Indian place, {{stat:delhi}} Delhi/NCR and {{stat:haryana}} Haryana. Each theme was searched
in three slices (landmarks by citations, 2022–26 by relevance, India/South Asia by relevance),
screened by rules and by hand. The Stage 2 blind check (six random records per theme, judged
by agents that did not see the screening) found 88% in scope and 81% with the right primary
theme, weakest in the technical-leaning C themes; recall against 176 seed works was limited
mainly by slice depth (100 seeds match a theme query but rank below the cut-off). For this
report, the most-cited landmark records of every theme were checked by hand and 38 clearly
off-topic works (battery chemistry, control theory, a journal-title record and the like) were
removed.

**Two kinds of evidence.** The map is a designed sample: its region and period mix is set by
the slices (an India slice for every theme, a 2022–26 slice for every theme). Counting records
by region or period would therefore measure the design, not the literature. So:

- **Gap, growth and mismatch claims rest on population counts**: OpenAlex-wide counts of each
  theme's combined query (title + abstract, exact phrases), journal articles and book chapters
  only (repository records excluded), 2010–2026, not retracted. Each count is multiplied by
  the theme's estimated precision — a random sample of 40 works from its full hit set,
  screened with the theme's own rules (median {{stat:p_median}}, range {{stat:p_min}}–{{stat:p_max}})
  — and, for growth, normalised per 10,000 Social Sciences works under the same filters (2026
  is a partial year, so only shares are compared). Place scopes use place names in titles and
  abstracts. Each count is given for all venues and for core venues only (the source's
  OpenAlex core flag); core-venue counts are {{stat:core_counts_status}}.
- **The records are used as examples** (three per gap), for landmarks, and for method shares,
  which OpenAlex does not record. The tab "Sample coverage" (formerly "Gap matrix") shows
  what the sample holds by region, method and period; it is not a gap measure.

**Coverage limits.** OpenAlex is thin exactly where much Indian urban and policy writing
appears:

{{table:coverage}}

EPW is held only from 2024, Seminar not at all, and Shodhganga theses only up to 2021, almost
all without abstracts and outside the count filters (they are theses, not articles). Every
India, Delhi/NCR or Haryana claim below carries this caveat.

## 2. Field map

The three domains differ in size by an order of magnitude. Among the urban themes, housing,
informality and slums (A3, {{v:A3.global_all_2020-26_adj}} adjusted works in 2020–26), urban
governance (A1, {{v:A1.global_all_2020-26_adj}}) and planning (A2, {{v:A2.global_all_2020-26_adj}})
are the largest; urban theory (A15, {{v:A15.global_all_2020-26_adj}}) and the night-time city
(A16, {{v:A16.global_all_2020-26_adj}}) the smallest. The digital-society themes include the
largest of all: generative AI and society (B14, {{v:B14.global_all_2020-26_adj}}, almost all
since 2023), misinformation (B9, {{v:B9.global_all_2020-26_adj}}), digital finance (B6,
{{v:B6.global_all_2020-26_adj}}) and cybercrime (B10, {{v:B10.global_all_2020-26_adj}}). The
urban × digital themes are small: only smart cities (C1, {{v:C1.global_all_2020-26_adj}}) is
as large as the larger urban themes, and the next largest — digital twins (C13), proptech (C10)
and digital mobility (C9), about {{v:C9.global_all_2020-26_adj}} each — are the size of the
smaller urban themes.

The intersection is thin relative to both parents. Most C themes hold between 3% and about a
third of the work in their nearest digital-society theme:

{{table:intersections}}

Three things stand out. First, the urban turn of platform, labour and payment research is
recent and small: platform urbanism is {{v:C2.global_all_2020-26_adj}} works against
{{v:B1.global_all_2020-26_adj}} on platforms; gig work with an urban or spatial focus
{{v:C15.global_all_2020-26_adj}} against {{v:B11.global_all_2020-26_adj}} on digital labour;
payments in urban economies {{v:C11.global_all_2020-26_adj}} against
{{v:B6.global_all_2020-26_adj}} on digital finance. Second, city e-government (C8) is larger than its digital parent (B5) because it is an
older, policy-led field; smart cities (C1), the largest C theme, has no single parent. Third,
digital geographies (C3), digital heritage and mapping (C16), digital informality (C14), urban
data governance (C5), civic tech (C12) and neighbourhood platforms (C18) are the smallest
corners of the map, each about 500 adjusted works or fewer in seven years.

## 3. Landmark works per theme

The two most-cited landmark-slice records per theme (repository-only records excluded; a few
records judged off-theme for this table are listed in `data/analysis/report_choices.yaml` and
stay in the bibliography). Citation counts favour older, English-language, Global North work;
the India subset tab and the gap examples below balance this.

{{table:landmarks}}

## 4. Growth and saturation

Growth is the change in a theme's share of all Social Sciences works between 2015–19 and
2020–26 (precision-adjusted; "new" where the theme had fewer than 50 adjusted works in
2015–19). Social Sciences output itself grew in this period, so a ratio of 1 means the theme
kept pace, not that it stood still.

**Fast-growing themes** (ratio ≥ 3 or new): {{stat:n_fast}} of 48, all of them digital-society
or urban × digital themes.

{{table:fast}}

Generative AI (B14), municipal AI (C7) and urban gig work (C15) are effectively new fields.
Behind them, algorithmic governance (B4, ×{{v:B4.global_all_growth}}) and platforms (B1,
×{{v:B1.global_all_growth}}) grew from small bases into large literatures, and the urban
versions of both (C7, C2) followed. The shares of digital finance (B6), digital
divides (B7) and misinformation (B9) grew five- to sevenfold from already large bases. Among the urban themes
none reaches ×3: urban environment, climate and risk (A14, ×{{v:A14.global_all_growth}}) and
mobility (A8, ×{{v:A8.global_all_growth}}) grow fastest.

**Saturating or flat themes** (ratio ≤ 1.3):

{{table:saturating}}

Housing, informality and slums (A3), migration and the city (A11) and heritage and mega-events
(A13) are large and only keep pace with the social sciences: mature fields where new work
mostly extends established debates. Digital geographies and code/space (C3) is the only theme
whose share fell: the conceptual vocabulary of the early 2010s has not grown with the digital
city it described, and its questions now appear under platform urbanism (C2) and smart
urbanism (C1). Urban and planning theory (A15) is small and flat by this measure, though
Southern urbanism is among the rising terms in the records (Section 5).

## 5. Emerging terms

Terms are the OpenAlex keywords on the map's records. Because the sample's period mix is fixed
by design, terms are ranked by the change in their **share of the period's records** (2018–21
vs 2022–26), not by raw counts; a term needs 15 records in 2022–26 and records in two themes.
Each term was then checked against OpenAlex as a whole (its share of all Social Sciences works,
2022–26 vs 2018–21; "confirmed" when that share also rose by more than 20%), and confirmed
terms are listed first. Example papers are 2022–24 records with the highest field-weighted
citation impact: 2025–26 works are left out of all FWCI-based signals, including the
spreadsheet's Emerging flag, because their citations are too young.

{{table:emerging}}

Three clusters dominate. **Generative AI** (generative AI, large language models, ChatGPT,
foundation models, AI regulation) moves from nothing to 3% of recent records, across B14, C7,
B4 and B12. **Indian digital public infrastructure** (Unified Payments Interface, digital
public infrastructure, the Digital Personal Data Protection Act 2023) rises in B5, C8 and C11;
these terms also rise OpenAlex-wide, so the rise is not only an artefact of the India slices.
**Platform work and surveillance in the city** (gig workers, last-mile delivery, facial and face
recognition) rises in C2, C15 and C6. Several terms from the sample did not rise OpenAlex-wide
and are left unconfirmed (for example land-use regulation and the night-time economy); they
reflect the sample, not the field. Terms that are themselves query phrases (marked in
`data/processed/emerging_terms.csv`) are inflated by the relevance-ranked recent slice.

## 6. Mismatch

**Fast globally, thin in South Asia.** South Asian places are named in
{{v:SS.sa_share_all_2020-26}} of all Social Sciences works in 2020–26. The location quotient
(LQ) divides a theme's South Asia share by that baseline. Most urban and digital-development
themes sit well above 1 (South Asia is over-represented in urban research generally), so the
informative cases are the themes where South Asia's share is lowest:

{{table:mismatch}}

{{stat:n_mismatch}} themes are both fast-growing worldwide (ratio ≥ 3) and at or below a 5%
South Asia share: generative AI (B14), digital twins (C13), datafication and data justice
(B2), digital mobility (C9) and misinformation (B9). The first four are gaps S1, S2, S5 and S4
below; misinformation is not, because its South Asia volume
({{v:B9.sa_all_2020-26_adj}} adjusted works) is large in absolute terms. Proptech and rental
platforms (C10), digital geographies (C3), urban informatics (C4), digital mapping (C16) and
public space (A9) are thin in South Asia without growing as fast (C16 and A9 are gaps S7 and
S6). The reverse also holds: digital identity and DPI (B5,
{{v:B5.sa_share_all_2020-26}}), payments in urban economies (C11,
{{v:C11.sa_share_all_2020-26}}) and digital informality (C14, {{v:C14.sa_share_all_2020-26}})
are areas where South Asia leads the field. One caution applies throughout: works that name no
place lower every region's share, and this matters most for generative AI and conceptual
themes.

**Themes studied mostly in the Global North.** Share of each region among all region mentions
(works naming places in a region, 2010–26, all venues, adjusted):

{{table:gn}}

**India.** India-named counts per theme (all and core venues) are
{{stat:india_counts_status}}; the India gaps below rest on the South Asia counts until then.

## 7. Candidate gaps

Twenty-five leads, each with population-count evidence, three example records and a caveat.
A gap here means that a topic is thin in OpenAlex relative to its neighbours or to the rest of
the world; it is a lead to check, not a proof. Records are examples only, and "matching
records" counts how many of the map's records fit the example filter.

### 7.1 Global

{{gaps:global}}

### 7.2 South Asia

{{gaps:south_asia}}

### 7.3 India

{{gaps:india}}

### 7.4 Delhi/NCR and Haryana

{{gaps:delhi_haryana}}

## 8. Methodological gaps

Method is inferred from abstracts by keyword cues, so it is known for only
{{stat:known_methods}} of {{stat:records_themes}} theme records; shares below are among records
with a known method, with the n. No method claim is made where fewer than 50 records have a
known method (one theme, C18). Full per-theme shares are in `data/processed/method_shares.csv`
and the Methods tab.

{{table:methods_compact}}

The urban themes lean qualitative and conceptual; the C themes carry most of the computational
work ({{v:C.method_computational_pct}} of known-method C records). India-flagged records in the
urban themes are less often quantitative than Global North records
({{v:IN_A.method_quantitative_pct}} against {{v:GN_A.method_quantitative_pct}}), while in the C
themes the order reverses ({{v:IN_C.method_quantitative_pct}} against
{{v:GN_C.method_quantitative_pct}}); these are differences within the sample and may reflect the
slices' relevance ranking. Three gaps stand out at theme level:

{{gaps:method}}

## 9. Shortlist leads (S1–S7)

*Pending: written after the India page-2 searches and the India/Haryana population counts.*

## 10. Limits

- **Precision.** Counts are adjusted by a 40-work sample per theme, and the blind check behind
  the domain factors used six records per theme. The least certain are C18 (estimated
  precision {{v:C18.p}}), C6 ({{v:C6.p}}), C11 ({{v:C11.p}}), C15 ({{v:C15.p}}) and C3
  ({{v:C3.p}}).
- **Place signal.** Places are read from titles and abstracts, not author affiliations, so
  works that never name a place count for no region.
- **Coverage.** Indian venues and theses are under-covered (Section 1); about a fifth of the
  records have no abstract (mostly Elsevier journals), and their method and region tags are thin.
- **Vocabulary.** Exact-phrase queries miss work that uses other words for the same thing;
  each gap's caveat names the likely blind spot.
- **What changes next.** India page-2 searches add records (and examples); India, Delhi/NCR,
  Haryana, region and core-venue counts complete Sections 6, 7.3–7.4 and 9; the provisional
  gaps are then kept, revised or replaced.
