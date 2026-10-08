# Literature map: urban, digital and urban × digital research

**Stage 3 report — draft.** Rendered by `scripts/stage3_analysis.py` from this template
(`scripts/report_template.md`); every number below comes from the repository's data files.
Status of the inputs: all-venue global and South Asia counts are in; India, Delhi/NCR,
Haryana, other-region and core-venue counts are **pending** (they are
fetched after the OpenAlex daily budget resets, together with the second page of the India
slices). Where a number reads "pending", that count has not been fetched yet; gaps marked
*provisional* depend on it.

Records are cited as Author (Year) [ID], where the ID is the record's row in
`outputs/bibliography.xlsx` (tab Records). Only works in the bibliography are cited.

## 1. What the analysis rests on

**The map.** 7,587 deduplicated records: 7,220 in the 48 themes and
367 found only by the supplementary query set (S1–S7). 2,036 name an
Indian place, 336 Delhi/NCR and 83 Haryana. Each theme was searched
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
  screened with the theme's own rules (median 0.42, range 0.10–0.72)
  — and, for growth, normalised per 10,000 Social Sciences works under the same filters (2026
  is a partial year, so only shares are compared). Place scopes use place names in titles and
  abstracts. Each count is given for all venues and for core venues only (the source's
  OpenAlex core flag); core-venue counts are pending.
- **The records are used as examples** (three per gap), for landmarks, and for method shares,
  which OpenAlex does not record. The tab "Sample coverage" (formerly "Gap matrix") shows
  what the sample holds by region, method and period; it is not a gap measure.

**Coverage limits.** OpenAlex is thin exactly where much Indian urban and policy writing
appears:

| Venue | OpenAlex works (all) | Years held | Map records |
|---|---:|---|---:|
| Economic & Political Weekly | 1,545 | 2024–2026 | 5 |
| Seminar (New Delhi) | – | no OpenAlex source | – |
| Contributions to Indian Sociology | 2,410 | before 2010 (1,673); 2010–2025 | 1 |
| Indian Journal of Public Administration | 6,700 | before 2010 (5,430); 2010–2026 | 3 |
| Environment and Urbanization Asia | 389 | 2010–2026 | 8 |
| Urbanisation (SAGE) | 212 | 2016–2026 | 2 |
| Shodhganga (INFLIBNET theses) | 117,655 | before 2010 (51,547); 2010–2021 | 9 |

EPW is held only from 2024, Seminar not at all, and Shodhganga theses only up to 2021, almost
all without abstracts and outside the count filters (they are theses, not articles). Every
India, Delhi/NCR or Haryana claim below carries this caveat.

## 2. Field map

The three domains differ in size by an order of magnitude. Among the urban themes, housing,
informality and slums (A3, 14,590 adjusted works in 2020–26), urban
governance (A1, 7,945) and planning (A2, 7,744)
are the largest; urban theory (A15, 502) and the night-time city
(A16, 1,386) the smallest. The digital-society themes include the
largest of all: generative AI and society (B14, 38,736, almost all
since 2023), misinformation (B9, 29,848), digital finance (B6,
21,401) and cybercrime (B10, 21,331). The
urban × digital themes are small: only smart cities (C1, 5,424) is
as large as the larger urban themes, and the next largest — digital twins (C13), proptech (C10)
and digital mobility (C9), about 2,222 each — are the size of the
smaller urban themes.

The intersection is thin relative to both parents. Most C themes hold between 3% and about a
third of the work in their nearest digital-society theme:

| Urban × digital theme | Adj. works 2020–26 | Digital parent | Adj. works | Urban parent | Adj. works | C as % of digital parent |
|---|---:|---|---:|---|---:|---:|
| C2 Platform urbanism | 776 | B1 Platforms & platform capitalism | 6,241 | A10 Urban economy, informal work & street vending | 3,459 | 12% |
| C5 Urban data governance & data justice in cities | 482 | B2 Datafication, data justice & data colonialism | 1,904 | A1 Urban governance, decentralisation & municipal finance | 7,945 | 25% |
| C6 Urban surveillance, policing & biometrics in public space | 931 | B3 Surveillance studies | 1,707 | A9 Public space, publicness & the street | 6,893 | 55% |
| C7 Algorithmic & automated urban governance, municipal AI / GenAI | 959 | B4 Algorithmic governance & AI in the public sector | 6,011 | A1 Urban governance, decentralisation & municipal finance | 7,945 | 16% |
| C8 City-level DPI & urban e-government | 1,639 | B5 Digital identity & digital public infrastructure (DPI) | 999 | A1 Urban governance, decentralisation & municipal finance | 7,945 | 164% |
| C9 Digital mobility (ride-hailing, MaaS, digital ticketing, transit apps) | 2,222 | B13 Mobile phones & everyday digital life | 4,326 | A8 Mobility & transport (social science) | 3,626 | 51% |
| C10 Proptech, housing platforms & short-term rentals | 2,242 | B1 Platforms & platform capitalism | 6,241 | A3 Housing, informality & slums | 14,590 | 36% |
| C11 Digital payments in urban economies (QR, UPI, mobile money) | 1,412 | B6 Digital finance & payments | 21,401 | A10 Urban economy, informal work & street vending | 3,459 | 7% |
| C12 Civic tech, e-participation & digital urban publics | 293 | B8 Social media, digital publics & political communication | 7,893 | A1 Urban governance, decentralisation & municipal finance | 7,945 | 4% |
| C14 Digital informality (informal settlements, vendors & digital systems) | 480 | B7 Digital divides & digital inclusion | 14,802 | A3 Housing, informality & slums | 14,590 | 3% |
| C15 Gig work in the city (urban and spatial focus) | 873 | B11 Digital labour | 6,476 | A10 Urban economy, informal work & street vending | 3,459 | 13% |
| C17 Urban cybersecurity & cyber-physical infrastructure | 1,182 | B10 Cybercrime, fraud & cybersecurity (social science) | 21,331 | A7 Urban infrastructure (water, sanitation, energy) & infrastructural citizenship | 4,087 | 6% |
| C18 Neighbourhood platforms & digital public space (WhatsApp, Nextdoor, RWA groups) | 525 | B8 Social media, digital publics & political communication | 7,893 | A9 Public space, publicness & the street | 6,893 | 7% |

Three things stand out. First, the urban turn of platform, labour and payment research is
recent and small: platform urbanism is 776 works against
6,241 on platforms; gig work with an urban or spatial focus
873 against 6,476 on digital labour;
payments in urban economies 1,412 against
21,401 on digital finance. Second, city e-government (C8) is larger than its digital parent (B5) because it is an
older, policy-led field; smart cities (C1), the largest C theme, has no single parent. Third,
digital geographies (C3), digital heritage and mapping (C16), digital informality (C14), urban
data governance (C5), civic tech (C12) and neighbourhood platforms (C18) are the smallest
corners of the map, each about 500 adjusted works or fewer in seven years.

## 3. Landmark works per theme

The two most-cited landmark-slice records per theme (repository-only records excluded; a few
records judged off-theme for this table are listed in `data/analysis/report_choices.yaml` and
stay in the bibliography). Citation counts favour older, English-language, Global North work;
the India subset tab and the gap examples below balance this.

| Theme | Landmark works (most cited in the map; full list in the Landmarks tab) |
|---|---|
| A1 Urban governance, decentralisation & municipal finance | Harvey (1989) [LM00001]; Brenner (2004) [LM00002] |
| A2 Planning, master plans & land-use regulation | Harvey (2009) [LM00171]; Campbell (1996) [LM00173] |
| A3 Housing, informality & slums | Kling et al. (2007) [LM00414]; Roy (2005) [LM00415] |
| A4 Eviction, resettlement & displacement | Lees (2008) [LM00586]; Slater (2006) [LM00587] |
| A5 Land, peri-urban & extended urbanisation | Seto et al. (2011) [LM00743]; Brenner & Schmid (2015) [LM00744] |
| A6 Small towns, census towns & secondary cities | Pojani & Stead (2015) [LM00908]; Giffinger et al. (2008) [LM00909] |
| A7 Urban infrastructure (water, sanitation, energy) & infrastructural citizenship | Graham & Marvin (2002) [LM01111]; Pritchett et al. (2003) [LM01112] |
| A8 Mobility & transport (social science) | Pereira et al. (2016) [LM01294]; McCann (2010) [LM01295] |
| A9 Public space, publicness & the street | Butler (2015) [LM01568]; Sampson & Raudenbush (1999) [LM01569] |
| A10 Urban economy, informal work & street vending | Bonnet (2018) [LM01780]; Moser (1978) [LM01781] |
| A11 Migration & the city | Harris & Todaro (1970) [LM01941]; Chan & Zhang (1999) [LM01942] |
| A12 Gender, caste, class & the city | Ley (1997) [LM02106]; Massey (1990) [LM02107] |
| A13 Heritage, mega-events & "world-class" city making | Huyssen (2003) [LM02268]; Kavaratzis (2004) [LM02269] |
| A14 Urban environment, climate & risk | Meerow et al. (2015) [LM02451]; Hallegatte et al. (2013) [LM02452] |
| A15 Urban & planning theory, Southern urbanism | Davoudi et al. (2012) [LM02638]; Gündoğan & Murray (2007) [LM02639] |
| A16 Night-time city & urban time | “Rhythmanalysis: Space, Time and Everyday…” (2005) [LM02793]; Chatterton & Hollands (2003) [LM02796] |
| B1 Platforms & platform capitalism | van Dijck et al. (2018) [LM03001]; Nieborg & Poell (2018) [LM03002] |
| B2 Datafication, data justice & data colonialism | Zuboff (2015) [LM03168]; Zuboff (2019) [LM03169] |
| B3 Surveillance studies | Haggerty & Ericson (2000) [LM03326]; Kitchin (2014) [LM03327] |
| B4 Algorithmic governance & AI in the public sector | Jobin et al. (2019) [LM03472]; Dwivedi et al. (2019) [LM03473] |
| B5 Digital identity & digital public infrastructure (DPI) | Caplan & Torpey (2001) [LM03656]; Sullivan & Burger (2017) [LM03661] |
| B6 Digital finance & payments | Demirgüç‐Kunt et al. (2018) [LM03853]; Ozili (2018) [LM03854] |
| B7 Digital divides & digital inclusion | Norris (2001) [LM04040]; Jenkins et al. (2009) [LM04041] |
| B8 Social media, digital publics & political communication | Bennett & Segerberg (2012) [LM04217]; Valenzuela et al. (2009) [LM04218] |
| B9 Misinformation & extreme speech | Allcott & Gentzkow (2017) [LM04434]; Lazer et al. (2018) [LM04435] |
| B10 Cybercrime, fraud & cybersecurity (social science) | von Solms & van Niekerk (2013) [LM04613]; Farwell & Rohozinski (2011) [LM04614] |
| B11 Digital labour | Wood et al. (2018) [LM04783]; Lee (2018) [LM04784] |
| B12 Infrastructure studies & STS of digital systems | Jasanoff & Kim (2009) [LM04979]; Plantin et al. (2016) [LM04980] |
| B13 Mobile phones & everyday digital life | Aker & Mbiti (2010) [LM05125]; Kim et al. (2005) [LM05126] |
| B14 Generative AI & society | Dwivedi et al. (2023) [LM05276]; Chang et al. (2024) [LM05277] |
| C1 Smart cities & smart urbanism | Zanella et al. (2014) [LM05428]; Hollands (2008) [LM05429] |
| C2 Platform urbanism | Leszczynski (2019) [LM05622]; Barns (2019) [LM05623] |
| C3 Digital geographies & code/space | Kitchin & Dodge (2011) [LM05803]; Ash et al. (2016) [LM05804] |
| C4 Urban informatics & urban computing | Zheng et al. (2014) [LM05891]; Salamon et al. (2014) [LM05892] |
| C5 Urban data governance & data justice in cities | Barns (2017) [LM06012]; Li et al. (2018) [LM06013] |
| C6 Urban surveillance, policing & biometrics in public space | Chun & Barnett (2021) [LM06126]; Shabazz (2015) [LM06127] |
| C7 Algorithmic & automated urban governance, municipal AI / GenAI | Son et al. (2023) [LM06237]; Cugurullo (2020) [LM06238] |
| C8 City-level DPI & urban e-government | Moon (2002) [LM06354]; Norris & Moon (2005) [LM06355] |
| C9 Digital mobility (ride-hailing, MaaS, digital ticketing, transit apps) | Rayle et al. (2015) [LM06475]; Pelletier et al. (2011) [LM06476] |
| C10 Proptech, housing platforms & short-term rentals | Zervas et al. (2017) [LM06625]; Guttentag (2013) [LM06626] |
| C11 Digital payments in urban economies (QR, UPI, mobile money) | Yan et al. (2020) [LM06769]; Mas & Morawczynski (2009) [LM06770] |
| C12 Civic tech, e-participation & digital urban publics | Capdevila & Zarlenga (2015) [LM06867]; Shelton & Lodato (2019) [LM06868] |
| C13 Digital twins, simulation & visual rendering of cities | Fuller et al. (2020) [LM06959]; Gröger & Plümer (2012) [LM06962] |
| C14 Digital informality (informal settlements, vendors & digital systems) | Kim (2021) [LM07111]; Kelikume (2021) [LM07112] |
| C15 Gig work in the city (urban and spatial focus) | Rosenblat (2018) [LM07205]; Rosenblat (2018) [LM07206] |
| C16 Digital heritage, mapping & representation of cities | Doersch et al. (2012) [LM07291]; Gong et al. (2018) [LM07292] |
| C17 Urban cybersecurity & cyber-physical infrastructure | Cui et al. (2018) [LM07416]; Vattapparamban et al. (2016) [LM07417] |
| C18 Neighbourhood platforms & digital public space (WhatsApp, Nextdoor, RWA groups) | Williams et al. (2014) [LM07530]; Kurwa (2019) [LM07531] |

## 4. Growth and saturation

Growth is the change in a theme's share of all Social Sciences works between 2015–19 and
2020–26 (precision-adjusted; "new" where the theme had fewer than 50 adjusted works in
2015–19). Social Sciences output itself grew in this period, so a ratio of 1 means the theme
kept pace, not that it stood still.

**Fast-growing themes** (ratio ≥ 3 or new): 21 of 48, all of them digital-society
or urban × digital themes.

| Theme | Adj. works 2020–26 (all venues) | Per 10k SS 2015–19 → 2020–26 | Growth (all) | Growth (core venues) | SA share 2020–26 | SA LQ 2020–26 |
|---|---:|---:|---:|---:|---:|---:|
| B14 Generative AI & society | 38,736 | 0.02 → 24.80 | new | pending | 2.2% | 0.77 |
| C7 Algorithmic & automated urban governance, municipal AI / GenAI | 959 | 0.04 → 0.61 | new | pending | 8.2% | 2.88 |
| C15 Gig work in the city (urban and spatial focus) | 873 | 0.04 → 0.56 | new | pending | 14.2% | 4.96 |
| B4 Algorithmic governance & AI in the public sector | 6,011 | 0.28 → 3.85 | 13.75 | pending | 6.5% | 2.27 |
| B1 Platforms & platform capitalism | 6,241 | 0.32 → 4.00 | 12.50 | pending | 6.4% | 2.25 |
| C17 Urban cybersecurity & cyber-physical infrastructure | 1,182 | 0.09 → 0.76 | 8.44 | pending | 7.4% | 2.60 |
| C2 Platform urbanism | 776 | 0.07 → 0.50 | 7.14 | pending | 10.2% | 3.56 |
| C18 Neighbourhood platforms & digital public space (WhatsApp, Nextdoor, RWA groups) | 525 | 0.05 → 0.34 | 6.80 | pending | 9.7% | 3.39 |
| B6 Digital finance & payments | 21,401 | 2.09 → 13.70 | 6.56 | pending | 20.1% | 7.02 |
| C13 Digital twins, simulation & visual rendering of cities | 2,600 | 0.27 → 1.67 | 6.19 | pending | 2.2% | 0.78 |
| B7 Digital divides & digital inclusion | 14,802 | 1.65 → 9.48 | 5.75 | pending | 12.1% | 4.21 |
| B11 Digital labour | 6,476 | 0.74 → 4.15 | 5.61 | pending | 9.6% | 3.34 |
| B9 Misinformation & extreme speech | 29,848 | 3.57 → 19.11 | 5.35 | pending | 4.7% | 1.65 |
| B2 Datafication, data justice & data colonialism | 1,904 | 0.24 → 1.22 | 5.08 | pending | 3.7% | 1.30 |
| B12 Infrastructure studies & STS of digital systems | 993 | 0.13 → 0.64 | 4.92 | pending | 6.5% | 2.29 |
| C14 Digital informality (informal settlements, vendors & digital systems) | 480 | 0.07 → 0.31 | 4.43 | pending | 28.8% | 10.05 |
| B10 Cybercrime, fraud & cybersecurity (social science) | 21,331 | 3.22 → 13.66 | 4.24 | pending | 6.9% | 2.42 |
| C5 Urban data governance & data justice in cities | 482 | 0.08 → 0.31 | 3.88 | pending | 5.6% | 1.96 |
| C9 Digital mobility (ride-hailing, MaaS, digital ticketing, transit apps) | 2,222 | 0.41 → 1.42 | 3.46 | pending | 4.1% | 1.45 |
| B5 Digital identity & digital public infrastructure (DPI) | 999 | 0.20 → 0.64 | 3.20 | pending | 39.4% | 13.78 |
| C11 Digital payments in urban economies (QR, UPI, mobile money) | 1,412 | 0.29 → 0.90 | 3.10 | pending | 36.1% | 12.62 |

Generative AI (B14), municipal AI (C7) and urban gig work (C15) are effectively new fields.
Behind them, algorithmic governance (B4, ×13.75) and platforms (B1,
×12.50) grew from small bases into large literatures, and the urban
versions of both (C7, C2) followed. The shares of digital finance (B6), digital
divides (B7) and misinformation (B9) grew five- to sevenfold from already large bases. Among the urban themes
none reaches ×3: urban environment, climate and risk (A14, ×2.75) and
mobility (A8, ×1.97) grow fastest.

**Saturating or flat themes** (ratio ≤ 1.3):

| Theme | Adj. works 2020–26 (all venues) | Per 10k SS 2015–19 → 2020–26 | Growth (all) | Growth (core venues) | SA share 2020–26 | SA LQ 2020–26 |
|---|---:|---:|---:|---:|---:|---:|
| C3 Digital geographies & code/space | 180 | 0.13 → 0.12 | 0.92 | pending | 1.7% | 0.58 |
| A15 Urban & planning theory, Southern urbanism | 502 | 0.29 → 0.32 | 1.10 | pending | 7.0% | 2.44 |
| A11 Migration & the city | 2,840 | 1.49 → 1.82 | 1.22 | pending | 17.4% | 6.07 |
| A3 Housing, informality & slums | 14,590 | 7.66 → 9.34 | 1.22 | pending | 15.9% | 5.57 |
| A13 Heritage, mega-events & "world-class" city making | 3,736 | 1.91 → 2.39 | 1.25 | pending | 5.7% | 1.99 |

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

| # | Term | Records 2018–21 → 2022–26 | Share of period's records | Share ratio | OpenAlex-wide SS share ratio | Example (2022–24, highest FWCI) |
|---:|---|---:|---:|---:|---:|---|
| 1 | generative AI | 0 → 124 | 0.0% → 3.09% | ×76.63 | ×247.26 | Jan et al. (2023) [LM05275] |
| 2 | large language models | 0 → 78 | 0.0% → 1.95% | ×48.2 | ×342.67 | Ray (2023) [LM05278] |
| 3 | ChatGPT | 0 → 67 | 0.0% → 1.67% | ×41.4 | ×2677.4 | Dwivedi et al. (2023) [LM05276] |
| 4 | Unified Payments Interface | 0 → 57 | 0.0% → 1.42% | ×35.22 | ×15.0 | Gupta et al. (2023) [LM06778] |
| 5 | digital public infrastructure | 0 → 54 | 0.0% → 1.35% | ×33.37 | ×25.15 | Alonso et al. (2023) [LM03703] |
| 6 | digital sovereignty | 0 → 28 | 0.0% → 0.7% | ×17.3 | ×5.32 | Thumfart (2024) [LM05055] |
| 7 | participatory governance | 0 → 24 | 0.0% → 0.6% | ×14.83 | ×3.22 | Lim & Yiğitcanlar (2022) [LM06894] |
| 8 | Digital Personal Data Protection Act 2023 | 0 → 21 | 0.0% → 0.52% | ×12.98 | ×356.95 | Estarla (2024) [LM03616] |
| 9 | last-mile delivery | 0 → 18 | 0.0% → 0.45% | ×11.12 | ×2.69 | Cano et al. (2022) [LM05649] |
| 10 | state capacity | 0 → 15 | 0.0% → 0.37% | ×9.27 | ×1.21 | Khosla & Tushnet (2022) [LM03741] |
| 11 | facial recognition technology | 0 → 15 | 0.0% → 0.37% | ×9.27 | ×2.69 | Wang et al. (2024) [LM03374] |
| 12 | face recognition | 1 → 25 | 0.08% → 0.62% | ×5.15 | ×2.33 | McElroy & Vergerio (2022) [LM00651] |
| 13 | gig workers | 3 → 55 | 0.24% → 1.37% | ×4.86 | ×3.84 | Wu & Huang (2024) [LM04857] |
| 14 | digital literacy | 8 → 126 | 0.65% → 3.14% | ×4.58 | ×7.1 | Xia et al. (2024) [LM05343] |
| 15 | national security | 1 → 20 | 0.08% → 0.5% | ×4.12 | ×1.31 | Küfeoğlu & Akgün (2023) [LM07468] |
| 16 | southern urbanism | 1 → 18 | 0.08% → 0.45% | ×3.71 | ×3.56 | Chakrabarti (2023) [LM02715] |
| 17 | online fraud | 2 → 29 | 0.16% → 0.72% | ×3.58 | ×3.23 | Ambashtha & Kumar (2023) [LM04681] |
| 18 | online harassment | 1 → 17 | 0.08% → 0.42% | ×3.5 | ×1.62 | Prawira et al. (2024) [LM04357] |
| 19 | foundation models | 1 → 17 | 0.08% → 0.42% | ×3.5 | ×63.51 | Huang et al. (2024) [LM05364] |
| 20 | urban local bodies | 2 → 27 | 0.16% → 0.67% | ×3.34 | ×1.53 | De (2023) [LM01198] |
| 21 | transaction costs | 1 → 16 | 0.08% → 0.4% | ×3.3 | ×1.24 | Yu et al. (2024) [LM06395] |
| 22 | AI regulation | 3 → 35 | 0.24% → 0.87% | ×3.09 | ×6.16 | Dwivedi et al. (2023) [LM05276] |
| 23 | sustainable urban planning | 1 → 15 | 0.08% → 0.37% | ×3.09 | ×2.28 | Xia et al. (2022) [LM06975] |
| 24 | Nigeria | 1 → 15 | 0.08% → 0.37% | ×3.09 | ×1.58 | Odoyi & Riekkinen (2022) [LM00469] |
| 25 | right to privacy | 2 → 23 | 0.16% → 0.57% | ×2.84 | ×1.25 | DE STEFANO & Taes (2022) [LM04859] |
| 26 | urban digital twins | 2 → 22 | 0.16% → 0.55% | ×2.72 | new | Mazzetto (2024) [LM06989] |
| 27 | ransomware | 2 → 22 | 0.16% → 0.55% | ×2.72 | ×2.75 | Park et al. (2022) [LM07449] |
| 28 | digital exclusion | 3 → 30 | 0.24% → 0.75% | ×2.65 | ×3.59 | Tomczyk et al. (2023) [LM04116] |
| 29 | regional disparities | 2 → 21 | 0.16% → 0.52% | ×2.6 | ×1.62 | Bharathi et al. (2022) [LM02165] |
| 30 | waste management | 2 → 21 | 0.16% → 0.52% | ×2.6 | ×2.4 | Aye & Sarma (2022) [LM01665] |

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
2.9% of all Social Sciences works in 2020–26. The location quotient
(LQ) divides a theme's South Asia share by that baseline. Most urban and digital-development
themes sit well above 1 (South Asia is over-represented in urban research generally), so the
informative cases are the themes where South Asia's share is lowest:

| Theme | Adj. works 2020–26 (all venues) | Per 10k SS 2015–19 → 2020–26 | Growth (all) | Growth (core venues) | SA share 2020–26 | SA LQ 2020–26 | India share 2020–26 |
|---|---:|---:|---:|---:|---:|---:|---:|
| C3 Digital geographies & code/space | 180 | 0.13 → 0.12 | 0.92 | pending | 1.7% | 0.58 | pending |
| C10 Proptech, housing platforms & short-term rentals | 2,242 | 0.81 → 1.44 | 1.78 | pending | 1.7% | 0.61 | pending |
| B14 Generative AI & society | 38,736 | 0.02 → 24.80 | new | pending | 2.2% | 0.77 | pending |
| C13 Digital twins, simulation & visual rendering of cities | 2,600 | 0.27 → 1.67 | 6.19 | pending | 2.2% | 0.78 | pending |
| C4 Urban informatics & urban computing | 1,414 | 0.38 → 0.91 | 2.39 | pending | 2.6% | 0.91 | pending |
| B2 Datafication, data justice & data colonialism | 1,904 | 0.24 → 1.22 | 5.08 | pending | 3.7% | 1.30 | pending |
| C9 Digital mobility (ride-hailing, MaaS, digital ticketing, transit apps) | 2,222 | 0.41 → 1.42 | 3.46 | pending | 4.1% | 1.45 | pending |
| C16 Digital heritage, mapping & representation of cities | 445 | 0.11 → 0.28 | 2.55 | pending | 4.5% | 1.57 | pending |
| A9 Public space, publicness & the street | 6,893 | 2.86 → 4.41 | 1.54 | pending | 4.6% | 1.61 | pending |
| B9 Misinformation & extreme speech | 29,848 | 3.57 → 19.11 | 5.35 | pending | 4.7% | 1.65 | pending |

5 themes are both fast-growing worldwide (ratio ≥ 3) and at or below a 5%
South Asia share: generative AI (B14), digital twins (C13), datafication and data justice
(B2), digital mobility (C9) and misinformation (B9). The first four are gaps S1, S2, S5 and S4
below; misinformation is not, because its South Asia volume
(1,412 adjusted works) is large in absolute terms. Proptech and rental
platforms (C10), digital geographies (C3), urban informatics (C4), digital mapping (C16) and
public space (A9) are thin in South Asia without growing as fast (C16 and A9 are gaps S7 and
S6). The reverse also holds: digital identity and DPI (B5,
39.4%), payments in urban economies (C11,
36.1%) and digital informality (C14, 28.8%)
are areas where South Asia leads the field. One caution applies throughout: works that name no
place lower every region's share, and this matters most for generative AI and conceptual
themes.

**Themes studied mostly in the Global North.** Share of each region among all region mentions
(works naming places in a region, 2010–26, all venues, adjusted):

*Pending: region counts (Global North, China & East Asia, Southeast Asia, Africa, Latin America, Middle East) are fetched with the population counts after the OpenAlex budget resets.*

**India.** India-named counts per theme (all and core venues) are
pending; the India gaps below rest on the South Asia counts until then.

## 7. Candidate gaps

Twenty-five leads, each with population-count evidence, three example records and a caveat.
A gap here means that a topic is thin in OpenAlex relative to its neighbours or to the rest of
the world; it is a lead to check, not a proof. Records are examples only, and "matching
records" counts how many of the map's records fit the example filter.

### 7.1 Global

**G1. Neighbourhood platforms and resident groups as digital public space** (C18)  
*Evidence.* About 525 works in 2020–26 worldwide (all venues; raw 5,524 hits × estimated precision 0.10); core venues pending. For comparison, B8 social media and digital publics: 7,893 (core pending).  
*Examples* (58 matching records in the map): Williams et al. (2014) [LM07530], *The Value of UK Hyperlocal…*; Kurwa (2019) [LM07531], *Building the Digitally Gated Community:…*; Barnett & Townend (2014) [LM07532], *Plurality, Policy and the Local*.  
*Missing.* Neighbourhood WhatsApp/Telegram groups, resident-welfare-association groups and Nextdoor-type platforms as infrastructures of local governance and exclusion, especially outside the US and UK; most existing work is on hyperlocal journalism.  
*Caveat.* Precision is very low (4 of 40 sampled hits in scope), so the count is uncertain; such groups also go by names the queries miss.

**G2. AI and generative AI inside city governments** (C7)  
*Evidence.* Municipal/urban AI (C7): 959 works in 2020–26 (core pending), against 6,011 for algorithmic governance and public-sector AI in general (B4) and 38,736 for generative AI and society (B14). C7 grew ×15.25 in normalised share from 2015–19, but from a very small base.  
*Examples* (103 matching records in the map): Son et al. (2023) [LM06237], *Algorithmic urban planning for smart…*; Cugurullo (2020) [LM06238], *Urban Artificial Intelligence: From Automation…*; Yiğitcanlar et al. (2021) [LM06239], *Responsible Urban Innovation with Local…*.  
*Missing.* Empirical studies of AI and GenAI systems that city governments actually run (procurement, frontline use, effects on residents), rather than frameworks, reviews and visions.  
*Caveat.* City deployments are often called 'smart city analytics' or 'decision support' and may sit under C1 or C4.

**G3. Social science of urban cybersecurity and cyber-physical infrastructure** (C17)  
*Evidence.* C17: 1,182 works in 2020–26 (core pending; precision 0.35), against 21,331 for cybercrime and cybersecurity in general (B10).  
*Examples* (65 matching records in the map): Elmaghraby & Losavio (2014) [LM05475], *Cyber security challenges in Smart…*; Cui et al. (2018) [LM07416], *Security and Privacy in Smart…*; Habibzadeh et al. (2019) [LM04658], *A survey on cybersecurity, data…*.  
*Missing.* Governance and political-economy studies of attacks on city systems (municipal ransomware, control-room and utility security, who bears the costs), rather than engineering designs.  
*Caveat.* Engineering dominates the hit set; social-science work may say 'resilience' or 'critical infrastructure' instead of 'cyber'.

**G4. How city governments govern data** (C5)  
*Evidence.* C5 urban data governance and data justice: 482 works in 2020–26 (core pending), against 1,904 on datafication and data justice in general (B2) and 5,424 on smart cities (C1).  
*Examples* (97 matching records in the map): van Zoonen (2016) [LM05482], *Privacy concerns in smart cities*; Barns (2017) [LM06012], *Smart cities and urban data…*; Pereira et al. (2016) [LM06014], *Delivering public value through open…*.  
*Missing.* Municipal data practice (data-sharing agreements, city data officers, data trusts, vendor lock-in) and data-justice claims at city scale, especially outside Europe and North America.  
*Caveat.* Overlaps smart-city governance (C1); open-data portal studies dominate the matches.

**G5. The night-time city beyond the night-time economy** (A16)  
*Evidence.* A16: 1,386 works in 2020–26 (core pending), 0.89 per 10,000 social science works; normalised growth ×1.39 from 2015–19, the fifth-lowest of the 16 urban (A) themes.  
*Examples* (113 matching records in the map): Chatterton & Hollands (2003) [LM02796], *Urban Nightscapes*; Tomsen (2003) [LM02800], *Bouncers: Violence and Governance in…*; Cressey (2008) [LM02801], *The Taxi-Dance Hall: A Sociological…*.  
*Missing.* Night as a dimension of urban governance beyond leisure and alcohol: night work, night-time services and mobility, access and safety at night, operating hours.  
*Caveat.* The vocabulary of night and urban time is scattered; adjacent work may be missed.

**G6. Small towns and secondary cities outside metropolitan research** (A6)  
*Evidence.* A6: 1,816 works in 2020–26 (core pending), 1.16 per 10,000 social science works, against 4.39 for peri-urban and extended urbanisation (A5) and 9.34 for housing and informality (A3).  
*Examples* (203 matching records in the map): Pojani & Stead (2015) [LM00908], *Sustainable Urban Transport in the…*; Giffinger et al. (2008) [LM00909], *City-ranking of European Medium-Sized Cities*; Kyttä (2002) [LM00910], *AFFORDANCES OF CHILDREN'S ENVIRONMENTS IN…*.  
*Missing.* Governance, services, economy and digital change in small and secondary cities studied in their own right, not as a backdrop to metropolitan or rural questions.  
*Caveat.* Studies of named small cities often avoid the generic terms the queries use, so counts understate the field.

**G7. City-level civic tech after the pilot stage** (C12)  
*Evidence.* C12: 293 works in 2020–26 (core pending; precision 0.31), against 5,424 on smart cities (C1).  
*Examples* (98 matching records in the map): Cardullo & Kitchin (2018) [LM05449], *Being a ‘citizen’ in the…*; Gabrys (2014) [LM05453], *Programming Environments: Environmentality and Citizen…*; Capdevila & Zarlenga (2015) [LM06867], *Smart city or smart citizens?…*.  
*Missing.* Longitudinal studies of civic-tech and e-participation platforms after launch (uptake, who participates, effects on decisions), and of grievance apps in Global South cities.  
*Caveat.* National e-participation studies fall outside this urban theme.


### 7.2 South Asia

**S1. Generative AI and society in South Asia** (B14)  
*Evidence.* South Asian places are named in 2.2% of B14 works in 2020–26 (all venues; 849 works), against 2.9% for all social science works (location quotient 0.77, the lowest of the 14 digital-society (B) themes); core venues: pending. Globally B14 is new since 2022 (38,736 works).  
*Examples* (41 matching records in the map): Kumar et al. (2025) [LM05352], *Generative artificial intelligence (GenAI) revolution:…*; Sharma et al. (2023) [LM05356], *Integrating Generative AI Into K-12…*; Ren et al. (2024) [LM05359], *Reconciling the contrasting narratives on…*.  
*Missing.* Social-science studies of GenAI use and governance in South Asian workplaces, public services and languages, beyond adoption surveys in higher education.  
*Caveat.* GenAI papers rarely name a place, lowering every region's share; the region counts will show whether South Asia is also low relative to other regions. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S2. Digital twins and 3D city models in South Asian cities** (C13)  
*Evidence.* 58 South Asia works in 2020–26 (2.2% of C13; location quotient 0.78; core pending), while C13 grew ×6.19 worldwide.  
*Examples* (28 matching records in the map): Bauer et al. (2021) [LM07030], *Urban Digital Twins – A…*; Saran et al. (2015) [LM07038], *CityGML at semantic level for…*; Naveed et al. (2025) [LM07042], *Machine learning assisted predictive urban…*.  
*Missing.* Digital twins and 3D city models in South Asian smart-city programmes: whose data, which vendors, how models enter planning, who is left out.  
*Caveat.* Remote-sensing and GIS work on South Asian cities is large but sits outside C13 unless it uses twin or 3D-model vocabulary. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S3. Proptech, rental platforms and short-term rentals in South Asia** (C10)  
*Evidence.* 39 South Asia works in 2020–26 (1.7% of C10, location quotient 0.61, the second-lowest of all 48 themes; core pending).  
*Examples* (28 matching records in the map): Tamilmani et al. (2020) [LM06679], *Indian Travellers’ Adoption of Airbnb…*; Chatterjee et al. (2019) [LM06682], *Airbnb in India: comparison with…*; Kaur & Solomon (2021) [LM06686], *A study on automated property…*.  
*Missing.* Rental and housing platforms, broker apps and short-term rentals in South Asian cities and their effects on rents, informal tenancy and regulation.  
*Caveat.* C10 is dominated by Airbnb studies; South Asian platforms may be studied as marketing or tourism. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S4. Digital mobility in South Asian cities** (C9)  
*Evidence.* 92 South Asia works in 2020–26 (4.1% of C9, location quotient 1.45, against 3.88 for mobility and transport in general, A8; core pending), while C9 grew ×3.46 worldwide.  
*Examples* (37 matching records in the map): Agarwal et al. (2023) [LM06534], *The Impact of Ride-Hailing Services…*; Kanuri et al. (2019) [LM06536], *Leveraging innovation for last-mile connectivity…*; Singh (2019) [LM06537], *India’s shift from mass transit…*.  
*Missing.* Ride-hailing, app-based paratransit, digital ticketing and transit apps in South Asian cities: access, gender, informal operators, fares and data.  
*Caveat.* Engineering studies are excluded by design; some social-science work sits in A8 or C15. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S5. Datafication and data justice beyond identity and payments in South Asia** (B2 B5)  
*Evidence.* B2 datafication and data justice: South Asia share 3.7% in 2020–26 (location quotient 1.30; 71 works), against 39.4% for digital identity and DPI (B5, quotient 13.78) and 20.1% for digital finance (B6).  
*Examples* (43 matching records in the map): Krishna (2020) [LM03230], *Digital identity, datafication and social…*; Thakkar et al. (2022) [LM03231], *When is Machine Learning Data…*; Taylor & Richter (2017) [LM03234], *The Power of Smart Solutions:…*.  
*Missing.* Datafication beyond Aadhaar and UPI: welfare and police databases, municipal, health and land records, and data-justice claims by affected groups.  
*Caveat.* Much South Asian datafication work is framed through identity and counted under B5. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S6. Public space and the street in South Asian cities** (A9)  
*Evidence.* South Asia share of A9 works in 2020–26: 4.6% (location quotient 1.61, the lowest of the 16 urban (A) themes; 318 works; core pending), against 17.1% for urban economy and street vending (A10).  
*Examples* (78 matching records in the map): Anjaria (2009) [LM01610], *Guardians of the Bourgeois City:…*; Roy & Bailey (2021) [LM01615], *Safe in the City? Negotiating…*; Mahadevia & Lathia (2019) [LM01614], *Women’s Safety and Public Spaces:…*.  
*Missing.* Publicness, access and everyday use of streets, parks and squares in South Asian cities (gender, caste and class in access; regulation; design).  
*Caveat.* South Asian street research often sits under vending (A10) or informality (A3), or uses words such as 'footpath', 'bazaar' or 'maidan'. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S7. Digital mapping and representation of South Asian cities** (C16)  
*Evidence.* 20 South Asia works in 2020–26 (4.5% of C16, location quotient 1.57; core pending).  
*Examples* (15 matching records in the map): Luthra (2018) [LM07343], *‘Old habits die hard’: discourses…*; Meggi (2017) [LM07354], *Towards a digital heritage: Evaluating…*; Janu (2026) [LM07398], *Archiving Erasure: Countermaps from Delhi*.  
*Missing.* How South Asian cities are digitally mapped and represented: map coverage of informal settlements, digital heritage of historic cores, street-view imagery.  
*Caveat.* Technical mapping of South Asian cities appears in remote-sensing venues that the screening excludes. The Indian-venue coverage limits (Coverage limits table) apply here too.


### 7.3 India

**I1. AI and GenAI in Indian urban local bodies and city police** *(provisional until the India counts are in)* (C7)  
*Evidence.* India-named C7 works in 2020–26: pending (core pending; India share pending); South Asia 79 (8.2%).  
*Examples* (68 matching records in the map): Varghese (2024) [LM03570], *E-Governance and Smart Policing in…*; Marwaha et al. (2024) [LM06276], *The emerging role of Artificial…*; Inakhiya et al. (2025) [LM06290], *Artificial intelligence and smart cities…*.  
*Missing.* AI and GenAI in Indian municipal corporations, smart-city companies and city police (grievance chatbots, traffic and policing analytics): procurement, use, accountability, effects.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**I2. CCTV, facial recognition and command centres in Indian public space** *(provisional until the India counts are in)* (C6)  
*Evidence.* India-named C6 works in 2020–26: pending (core pending); South Asia 72 (7.7% of C6). 'Facial recognition technology' is among the fastest-rising terms in the map's records (see Emerging terms).  
*Examples* (67 matching records in the map): Marda & Narayan (2020) [LM06158], *Data in New Delhi's predictive…*; Sen (2022) [LM06164], *“No city for lovers:” anti-Romeo…*; Ilyas & Garg (2025) [LM06183], *Stigmatized buses, world-class metro: how…*.  
*Missing.* CCTV networks, facial recognition and command-and-control centres in Indian cities: how police and municipalities use them, oversight, effects on public space.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**I3. Municipal data governance in Indian cities** *(provisional until the India counts are in)* (C5)  
*Evidence.* India-named C5 works in 2020–26: pending (core pending); South Asia 27 (5.6% of C5).  
*Examples* (16 matching records in the map): Singh & Upadhyay (2022) [LM05539], *Fractured smart cities: Missing links…*; Kennedy et al. (2020) [LM03240], *Interrogating data justice on Hyderabad’s…*; Long (2015) [LM06072], *Big/open data for urban management*.  
*Missing.* How Indian city governments and smart-city companies collect, share and govern data (data policies and officers, command-centre data, vendor contracts), and city-level data-justice claims.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**I4. Cybersecurity of Indian city systems** *(provisional until the India counts are in)* (C17)  
*Evidence.* India-named C17 works in 2020–26: pending (core pending); South Asia 88 (7.4% of C17).  
*Examples* (20 matching records in the map): Kitchin et al. (2018) [LM07446], *Creating Smart Cities*; Ahmad et al. (2021) [LM07451], *Cyber-Physical Systems and Smart Cities…*; Jabbar et al. (2021) [LM07465], *Future challenges for cyber-security in…*.  
*Missing.* Cyber incidents affecting Indian urban services (utilities, transit, municipal systems, command centres) and how cities govern that risk.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**I5. The night-time city in India** *(provisional until the India counts are in)* (A16)  
*Evidence.* India-named A16 works in 2020–26: pending (core pending); South Asia 98 (7.1% of A16).  
*Examples* (42 matching records in the map): Pathak (2011) [LM02831], *Timepass: Youth, Class, and the…*; Carswell et al. (2018) [LM02835], *Waiting for the state: Gender,…*; Parikh (2017) [LM02841], *Politics of presence: women’s safety…*.  
*Missing.* Night-time work, services, mobility and access in Indian cities beyond women's safety: operating hours, night shifts, night markets.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.


### 7.4 Delhi/NCR and Haryana

**H1. Haryana's secondary cities beyond Gurugram and Faridabad** *(provisional until the Haryana counts are in)* (A6)  
*Evidence.* Haryana-named A6 works 2010–26: pending (core pending), against pending naming Delhi/NCR.  
*Examples* (45 matching records in the map): Fatewar & Yadav (2023) [LM01024], *Subaltern Urbanisation in the State…*; Dangi (2026) [LM01074], *Evaluation of Financial Performance of…*; Bhagwan (1974) [LM01079], *Municipal government and politics in…*.  
*Missing.* Governance, economy, infrastructure and digital change in Haryana's secondary cities (Rohtak, Hisar, Panipat, Karnal, Sonipat, Ambala, Yamunanagar, Rewari and others); most records found are remote-sensing studies of urban growth.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**H2. Digital identity and e-government in Haryana** *(provisional until the Haryana counts are in)* (B5 C8)  
*Evidence.* Haryana-named works 2010–26: B5 pending (core pending), C8 pending (core pending).  
*Examples* (2 matching records in the map): . & Phougat (2026) [LM03810], *UNDERSTANDING BENEFICIARY EXPERIENCE AT FAIR…*; Gond & Yadav (2023) [LM06451], *A Study of E-Governance Service…*.  
*Missing.* Haryana's state family-ID database and city-level e-government: how eligibility data are produced and corrected, and how residents and officials work with them.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**H3. Digital mobility in Delhi/NCR** *(provisional until the Delhi counts are in)* (C9 A8)  
*Evidence.* Delhi/NCR-named works 2010–26: C9 pending (core pending), against A8 mobility and transport pending (core pending).  
*Examples* (53 matching records in the map): Kant et al. (2023) [LM06543], *Assessment of drivers and barriers…*; Gupta & Sinha (2022) [LM06548], *Assessing the Factors Impacting Transport…*; Mazumdar (2025) [LM05717], *Unequal taxi geographies: Antagonisms in…*.  
*Missing.* App-based and digitally ticketed mobility in Delhi/NCR (ride-hailing and app autos, metro and bus digital ticketing) and how fares and apps shape who travels when.  
*Caveat.* Overlaps the shortlist leads; listed because of the counts, and to be dropped if the Delhi counts do not support it. Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.


## 8. Methodological gaps

Method is inferred from abstracts by keyword cues, so it is known for only
4,567 of 7,220 theme records; shares below are among records
with a known method, with the n. No method claim is made where fewer than 50 records have a
known method (one theme, C18). Full per-theme shares are in `data/processed/method_shares.csv`
and the Methods tab.

| Group | Records | Known method (n) | Qualitative | Quantitative | Mixed | Review | Conceptual | Computational |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Domain A (all records) | 2672 | 1593 | 30% | 13% | 11% | 5% | 37% | 4% |
| Domain B (all records) | 2427 | 1545 | 24% | 19% | 9% | 5% | 35% | 8% |
| Domain C (all records) | 2121 | 1429 | 24% | 18% | 11% | 7% | 25% | 14% |
| A, India-flagged | 792 | 463 | 36% | 10% | 13% | 4% | 33% | 5% |
| A, Global North | 328 | 237 | 32% | 18% | 6% | 1% | 39% | 4% |
| B, India-flagged | 616 | 405 | 31% | 14% | 12% | 5% | 33% | 5% |
| B, Global North | 232 | 179 | 27% | 26% | 10% | 3% | 28% | 6% |
| C, India-flagged | 495 | 357 | 28% | 24% | 16% | 5% | 16% | 10% |
| C, Global North | 324 | 255 | 33% | 17% | 8% | 4% | 25% | 13% |

The urban themes lean qualitative and conceptual; the C themes carry most of the computational
work (14.4% of known-method C records). India-flagged records in the
urban themes are less often quantitative than Global North records
(9.7% against 18.1%), while in the C
themes the order reverses (24.1% against
17.3%); these are differences within the sample and may reflect the
slices' relevance ranking. Three gaps stand out at theme level:

**M1. Few qualitative studies of digital twins and city models in use** (C13)  
*Evidence.* Among the 112 C13 records with a known method, 7.1% are qualitative and 47.3% computational (the map's records; the method is inferred from abstracts).  
*Examples* (8 matching records in the map): Nochta et al. (2020) [LM06997], *A Socio-Technical Perspective on Urban…*; Peldon et al. (2024) [LM07027], *Navigating urban complexity: The transformative…*; Saeidian et al. (2023) [LM07037], *A semantic 3D city model…*.  
*Missing.* Ethnographic and interview studies of how digital twins and city models are built, bought and used in planning offices.  
*Caveat.* Method shares come from the map's records and are inferred from abstracts.

**M2. Few field studies of municipal and generative AI in use** (C7 B14)  
*Evidence.* Qualitative records: C7 12.0% of 92 with a known method, B14 11.2% of 116; reviews make up 17.4% and 13.8%.  
*Examples* (24 matching records in the map): Tlili et al. (2023) [LM05280], *What if the devil is…*; Cooper (2023) [LM05287], *Examining Science Education in ChatGPT:…*; Cugurullo (2020) [LM06238], *Urban Artificial Intelligence: From Automation…*.  
*Missing.* Field studies (observation, interviews, documents) of AI and GenAI inside public organisations and cities, rather than reviews, frameworks and perception surveys.  
*Caveat.* Method shares come from the map's records and are inferred from abstracts; B14 is very young.

**M3. Digital payments studied mostly through adoption surveys** (B6 C11)  
*Evidence.* Qualitative records: B6 10.4% of 106 with a known method (quantitative 50.9%); C11 16.9% of 71 (quantitative and mixed 39.4% and 23.9%).  
*Examples* (41 matching records in the map): Hughes & Lonie (2007) [LM03875], *M-PESA: Mobile Money for the…*; Maurer (2012) [LM03897], *Mobile Money: Communication, Consumption and…*; Leong et al. (2017) [LM03898], *Nurturing a FinTech ecosystem: The…*.  
*Missing.* Ethnographies of payment practice among urban vendors, workers and households: how QR and UPI payments change credit, record-keeping, tax visibility and bargaining.  
*Caveat.* 


## 9. Shortlist leads (S1–S7)

*Pending: written after the India page-2 searches and the India/Haryana population counts.*

## 10. Limits

- **Precision.** Counts are adjusted by a 40-work sample per theme, and the blind check behind
  the domain factors used six records per theme. The least certain are C18 (estimated
  precision 0.10), C6 (0.27), C11 (0.28), C15 (0.29) and C3
  (0.29).
- **Place signal.** Places are read from titles and abstracts, not author affiliations, so
  works that never name a place count for no region.
- **Coverage.** Indian venues and theses are under-covered (Section 1); about a fifth of the
  records have no abstract (mostly Elsevier journals), and their method and region tags are thin.
- **Vocabulary.** Exact-phrase queries miss work that uses other words for the same thing;
  each gap's caveat names the likely blind spot.
- **What changes next.** India page-2 searches add records (and examples); India, Delhi/NCR,
  Haryana, region and core-venue counts complete Sections 6, 7.3–7.4 and 9; the provisional
  gaps are then kept, revised or replaced.
