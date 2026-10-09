# Literature map: urban, digital and urban × digital research

**Stage 3 report.** Rendered by `scripts/stage3_analysis.py` from `scripts/report_template.md`;
every number comes from the repository's data files (counts retrieved 8–9 October 2026).
Records are cited as Author (Year) [ID], the ID being the record's row in
`outputs/bibliography.xlsx`. Only works in the bibliography are cited.

## 1. What the analysis rests on

**The map.** 9,405 deduplicated records: 8,949 in the 48 themes and
456 found only by the supplementary query set for the researcher's leads
(S1–S7). 3,336 name an Indian place, 506 Delhi/NCR and 127
Haryana. Each theme was searched in three slices — most-cited works, 2022–26 works by relevance,
and India/South Asia works by relevance (two pages per query) — and screened by rules and by
hand. A blind check of six random records per theme found 88% in scope and 81% with the right
primary theme, weakest in the technical-leaning C themes. Of 176 seed works chosen by the
researcher, 66 are in the map, 83 match a theme query but
rank below the slice cut-off, 12 match no query, 4 were
screened out and 11 are outside OpenAlex's searched corpus. The most-cited records of every theme were read by hand and clearly off-topic
works removed.

**Two kinds of evidence.** The map is a designed sample: every theme has an India slice and a
2022–26 slice, so counting records by region or period would measure the design. Therefore:

- **Gap, growth and mismatch claims rest on population counts**: OpenAlex-wide counts of each
  theme's combined query (title + abstract, exact phrases), journal articles and book chapters
  only, 2010–2026, each multiplied by the theme's estimated precision (a random 40-work sample of
  its hit set screened with its own rules; median 0.42, range
  0.10–0.72; South Asia, India, Delhi and Haryana counts use a separate
  sample of the South Asia hit set). Growth is normalised per 10,000 Social Sciences works under
  the same filters; 2026 is a partial year, so only shares are compared. Places are read from
  titles and abstracts. Every count is given for all venues and for core venues only (sources
  OpenAlex flags as core).
- **Records are used only as examples** (three per gap), for landmarks, and for method shares,
  which OpenAlex does not record. The "Sample coverage" tab (formerly "Gap matrix") describes the
  sample, not the literature.

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

Every India, Delhi/NCR or Haryana claim below carries this caveat.

## 2. Field map

Among the urban themes, housing, informality and slums (A3, 14,504
adjusted works in 2020–26), urban governance (A1, 7,926) and planning
(A2, 7,730) are the largest; urban theory (A15,
501) and the night-time city (A16, 1,382)
the smallest. The digital-society themes include the largest of all: generative AI (B14,
38,613, almost all since 2023), misinformation (B9,
29,729), digital finance (B6, 21,371) and
cybercrime (B10, 21,267). The urban × digital themes are small: only
smart cities (C1, 5,399) matches the larger urban themes. Most C themes
hold between 3% and a third of the work in their nearest digital-society theme:

| Urban × digital theme | Adj. works 2020–26 | Digital parent | Adj. works | Urban parent | Adj. works | C as % of digital parent |
|---|---:|---|---:|---|---:|---:|
| C2 Platform urbanism | 772 | B1 Platforms & platform capitalism | 6,213 | A10 Urban economy, informal work & street vending | 3,447 | 12% |
| C5 Urban data governance & data justice in cities | 478 | B2 Datafication, data justice & data colonialism | 1,899 | A1 Urban governance, decentralisation & municipal finance | 7,926 | 25% |
| C6 Urban surveillance, policing & biometrics in public space | 924 | B3 Surveillance studies | 1,701 | A9 Public space, publicness & the street | 6,877 | 54% |
| C7 Algorithmic & automated urban governance, municipal AI / GenAI | 957 | B4 Algorithmic governance & AI in the public sector | 6,001 | A1 Urban governance, decentralisation & municipal finance | 7,926 | 16% |
| C8 City-level DPI & urban e-government | 1,633 | B5 Digital identity & digital public infrastructure (DPI) | 994 | A1 Urban governance, decentralisation & municipal finance | 7,926 | 164% |
| C9 Digital mobility (ride-hailing, MaaS, digital ticketing, transit apps) | 2,217 | B13 Mobile phones & everyday digital life | 4,313 | A8 Mobility & transport (social science) | 3,620 | 51% |
| C10 Proptech, housing platforms & short-term rentals | 2,238 | B1 Platforms & platform capitalism | 6,213 | A3 Housing, informality & slums | 14,504 | 36% |
| C11 Digital payments in urban economies (QR, UPI, mobile money) | 1,407 | B6 Digital finance & payments | 21,371 | A10 Urban economy, informal work & street vending | 3,447 | 7% |
| C12 Civic tech, e-participation & digital urban publics | 291 | B8 Social media, digital publics & political communication | 7,893 | A1 Urban governance, decentralisation & municipal finance | 7,926 | 4% |
| C14 Digital informality (informal settlements, vendors & digital systems) | 475 | B7 Digital divides & digital inclusion | 14,709 | A3 Housing, informality & slums | 14,504 | 3% |
| C15 Gig work in the city (urban and spatial focus) | 870 | B11 Digital labour | 6,466 | A10 Urban economy, informal work & street vending | 3,447 | 13% |
| C17 Urban cybersecurity & cyber-physical infrastructure | 1,175 | B10 Cybercrime, fraud & cybersecurity (social science) | 21,267 | A7 Urban infrastructure (water, sanitation, energy) & infrastructural citizenship | 4,087 | 6% |
| C18 Neighbourhood platforms & digital public space (WhatsApp, Nextdoor, RWA groups) | 525 | B8 Social media, digital publics & political communication | 7,893 | A9 Public space, publicness & the street | 6,877 | 7% |

The urban turn of platform, labour and payment research is recent and small (C2, C15 and C11
against B1, B11 and B6). City e-government (C8) is larger than its digital parent because it is
an older, policy-led field. Digital geographies (C3), digital heritage and mapping (C16),
digital informality (C14), urban data governance (C5), civic tech (C12) and neighbourhood
platforms (C18) are the smallest corners, each about 500 adjusted works or fewer in seven years.

## 3. Landmark works per theme

The two most-cited landmark-slice records per theme (repository-only records excluded; a few
off-theme records passed over are listed in `data/analysis/report_choices.yaml`). Citation
counts favour older, English-language, Global North work; the gap examples below balance this.

| Theme | Landmark works (most cited in the map; full list in the Landmarks tab) |
|---|---|
| A1 Urban governance, decentralisation & municipal finance | Harvey (1989) [LM00001]; Brenner (2004) [LM00002] |
| A2 Planning, master plans & land-use regulation | Harvey (2009) [LM00237]; Campbell (1996) [LM00239] |
| A3 Housing, informality & slums | Kling et al. (2007) [LM00553]; Roy (2005) [LM00554] |
| A4 Eviction, resettlement & displacement | Lees (2008) [LM00797]; Slater (2006) [LM00798] |
| A5 Land, peri-urban & extended urbanisation | Seto et al. (2011) [LM00997]; Brenner & Schmid (2015) [LM00998] |
| A6 Small towns, census towns & secondary cities | Pojani & Stead (2015) [LM01227]; Giffinger et al. (2008) [LM01228] |
| A7 Urban infrastructure (water, sanitation, energy) & infrastructural citizenship | Graham & Marvin (2002) [LM01493]; Pritchett et al. (2003) [LM01494] |
| A8 Mobility & transport (social science) | Pereira et al. (2016) [LM01736]; McCann (2010) [LM01737] |
| A9 Public space, publicness & the street | Butler (2015) [LM02105]; Sampson & Raudenbush (1999) [LM02106] |
| A10 Urban economy, informal work & street vending | Bonnet (2018) [LM02350]; Moser (1978) [LM02351] |
| A11 Migration & the city | Harris & Todaro (1970) [LM02569]; Chan & Zhang (1999) [LM02570] |
| A12 Gender, caste, class & the city | Ley (1997) [LM02791]; Massey (1990) [LM02792] |
| A13 Heritage, mega-events & "world-class" city making | Huyssen (2003) [LM03001]; Kavaratzis (2004) [LM03002] |
| A14 Urban environment, climate & risk | Meerow et al. (2015) [LM03235]; Hallegatte et al. (2013) [LM03236] |
| A15 Urban & planning theory, Southern urbanism | Davoudi et al. (2012) [LM03476]; Gündoğan & Murray (2007) [LM03477] |
| A16 Night-time city & urban time | “Rhythmanalysis: Space, Time and Everyday…” (2005) [LM03657]; Chatterton & Hollands (2003) [LM03660] |
| B1 Platforms & platform capitalism | van Dijck et al. (2018) [LM03877]; Nieborg & Poell (2018) [LM03878] |
| B2 Datafication, data justice & data colonialism | Zuboff (2015) [LM04087]; Zuboff (2019) [LM04088] |
| B3 Surveillance studies | Haggerty & Ericson (2000) [LM04265]; Kitchin (2014) [LM04266] |
| B4 Algorithmic governance & AI in the public sector | Jobin et al. (2019) [LM04446]; Dwivedi et al. (2019) [LM04447] |
| B5 Digital identity & digital public infrastructure (DPI) | Caplan & Torpey (2001) [LM04680]; Sullivan & Burger (2017) [LM04685] |
| B6 Digital finance & payments | Demirgüç‐Kunt et al. (2018) [LM04911]; Ozili (2018) [LM04912] |
| B7 Digital divides & digital inclusion | Norris (2001) [LM05147]; Jenkins et al. (2009) [LM05148] |
| B8 Social media, digital publics & political communication | Bennett & Segerberg (2012) [LM05377]; Valenzuela et al. (2009) [LM05378] |
| B9 Misinformation & extreme speech | Allcott & Gentzkow (2017) [LM05671]; Lazer et al. (2018) [LM05672] |
| B10 Cybercrime, fraud & cybersecurity (social science) | von Solms & van Niekerk (2013) [LM05907]; Farwell & Rohozinski (2011) [LM05908] |
| B11 Digital labour | Wood et al. (2018) [LM06140]; Lee (2018) [LM06141] |
| B12 Infrastructure studies & STS of digital systems | Jasanoff & Kim (2009) [LM06381]; Plantin et al. (2016) [LM06382] |
| B13 Mobile phones & everyday digital life | Aker & Mbiti (2010) [LM06535]; Kim et al. (2005) [LM06536] |
| B14 Generative AI & society | Dwivedi et al. (2023) [LM06741]; Chang et al. (2024) [LM06742] |
| C1 Smart cities & smart urbanism | Zanella et al. (2014) [LM06929]; Hollands (2008) [LM06930] |
| C2 Platform urbanism | Leszczynski (2019) [LM07172]; Barns (2019) [LM07173] |
| C3 Digital geographies & code/space | Kitchin & Dodge (2011) [LM07371]; Ash et al. (2016) [LM07372] |
| C4 Urban informatics & urban computing | Zheng et al. (2014) [LM07459]; Salamon et al. (2014) [LM07460] |
| C5 Urban data governance & data justice in cities | Barns (2017) [LM07590]; Li et al. (2018) [LM07591] |
| C6 Urban surveillance, policing & biometrics in public space | Chun & Barnett (2021) [LM07710]; Shabazz (2015) [LM07711] |
| C7 Algorithmic & automated urban governance, municipal AI / GenAI | Son et al. (2023) [LM07847]; Cugurullo (2020) [LM07848] |
| C8 City-level DPI & urban e-government | Moon (2002) [LM07984]; Norris & Moon (2005) [LM07985] |
| C9 Digital mobility (ride-hailing, MaaS, digital ticketing, transit apps) | Rayle et al. (2015) [LM08124]; Pelletier et al. (2011) [LM08125] |
| C10 Proptech, housing platforms & short-term rentals | Zervas et al. (2017) [LM08286]; Guttentag (2013) [LM08287] |
| C11 Digital payments in urban economies (QR, UPI, mobile money) | Yan et al. (2020) [LM08444]; Mas & Morawczynski (2009) [LM08445] |
| C12 Civic tech, e-participation & digital urban publics | Capdevila & Zarlenga (2015) [LM08572]; Shelton & Lodato (2019) [LM08573] |
| C13 Digital twins, simulation & visual rendering of cities | Fuller et al. (2020) [LM08664]; Gröger & Plümer (2012) [LM08667] |
| C14 Digital informality (informal settlements, vendors & digital systems) | Kim (2021) [LM08832]; Kelikume (2021) [LM08833] |
| C15 Gig work in the city (urban and spatial focus) | Rosenblat (2018) [LM08952]; Berger et al. (2019) [LM08954] |
| C16 Digital heritage, mapping & representation of cities | Doersch et al. (2012) [LM09068]; Gong et al. (2018) [LM09069] |
| C17 Urban cybersecurity & cyber-physical infrastructure | Cui et al. (2018) [LM09206]; Vattapparamban et al. (2016) [LM09207] |
| C18 Neighbourhood platforms & digital public space (WhatsApp, Nextdoor, RWA groups) | Williams et al. (2014) [LM09331]; Kurwa (2019) [LM09332] |

## 4. Growth and saturation

Growth is the change in a theme's share of all Social Sciences works from 2015–19 to 2020–26
("new" below 50 adjusted works in 2015–19); 1 means the theme kept pace with the social
sciences.

**Fast-growing themes** (ratio ≥ 3 or new, all venues): 21 of 48, all digital-society
or urban × digital themes. 16 of them also grow at least threefold in core
venues; for 34 of the 41 themes with both ratios, growth is
slower in core venues than in all venues, i.e. faster outside core venues.

| Theme | Adj. works 2020–26 (all venues) | Per 10k SS 2015–19 → 2020–26 | Growth (all) | Growth (core venues) | SA share 2020–26 | SA LQ 2020–26 |
|---|---:|---:|---:|---:|---:|---:|
| B14 Generative AI & society | 38,613 | 0.02 → 24.73 | new | new | 1.8% | 0.62 |
| C7 Algorithmic & automated urban governance, municipal AI / GenAI | 957 | 0.04 → 0.61 | new | new | 5.5% | 1.94 |
| C15 Gig work in the city (urban and spatial focus) | 870 | 0.04 → 0.56 | new | new | 19.5% | 6.83 |
| B4 Algorithmic governance & AI in the public sector | 6,001 | 0.28 → 3.84 | 13.71 | 7.14 | 7.7% | 2.71 |
| B1 Platforms & platform capitalism | 6,213 | 0.32 → 3.98 | 12.44 | 7.80 | 4.7% | 1.63 |
| C17 Urban cybersecurity & cyber-physical infrastructure | 1,175 | 0.09 → 0.75 | 8.33 | new | 9.4% | 3.30 |
| C2 Platform urbanism | 772 | 0.07 → 0.49 | 7.00 | new | 12.4% | 4.35 |
| C18 Neighbourhood platforms & digital public space (WhatsApp, Nextdoor, RWA groups) | 525 | 0.05 → 0.34 | 6.80 | new | 20.6% | 7.19 |
| B6 Digital finance & payments | 21,371 | 2.09 → 13.68 | 6.55 | 4.67 | 20.4% | 7.13 |
| C13 Digital twins, simulation & visual rendering of cities | 2,586 | 0.27 → 1.66 | 6.15 | 4.67 | 1.5% | 0.53 |
| B7 Digital divides & digital inclusion | 14,709 | 1.64 → 9.42 | 5.74 | 3.49 | 15.0% | 5.23 |
| B11 Digital labour | 6,466 | 0.74 → 4.14 | 5.59 | 4.70 | 8.5% | 2.96 |
| B9 Misinformation & extreme speech | 29,729 | 3.56 → 19.04 | 5.35 | 4.64 | 4.0% | 1.41 |
| B2 Datafication, data justice & data colonialism | 1,899 | 0.24 → 1.22 | 5.08 | 3.61 | 2.7% | 0.96 |
| B12 Infrastructure studies & STS of digital systems | 987 | 0.13 → 0.63 | 4.85 | 3.26 | 5.8% | 2.02 |
| C14 Digital informality (informal settlements, vendors & digital systems) | 475 | 0.07 → 0.30 | 4.29 | new | 32.2% | 11.26 |
| B10 Cybercrime, fraud & cybersecurity (social science) | 21,267 | 3.21 → 13.62 | 4.24 | 2.73 | 6.9% | 2.43 |
| C5 Urban data governance & data justice in cities | 478 | 0.08 → 0.31 | 3.88 | 2.46 | 3.8% | 1.32 |
| C9 Digital mobility (ride-hailing, MaaS, digital ticketing, transit apps) | 2,217 | 0.41 → 1.42 | 3.46 | 2.94 | 3.8% | 1.34 |
| B5 Digital identity & digital public infrastructure (DPI) | 994 | 0.20 → 0.64 | 3.20 | 1.89 | 52.6% | 18.39 |
| C11 Digital payments in urban economies (QR, UPI, mobile money) | 1,407 | 0.29 → 0.90 | 3.10 | 2.33 | 56.7% | 19.82 |

Generative AI (B14), municipal AI (C7) and urban gig work (C15) are effectively new fields.
Algorithmic governance (B4, ×13.71) and platforms (B1,
×12.44) grew from small bases into large literatures, and their urban
versions (C7, C2) followed. The shares of digital finance (B6), digital divides (B7) and
misinformation (B9) grew five- to sevenfold from already large bases. No urban theme reaches ×3;
urban environment and climate (A14, ×2.76) and mobility (A8,
×1.97) grow fastest.

**Saturating or flat themes** (ratio ≤ 1.3):

| Theme | Adj. works 2020–26 (all venues) | Per 10k SS 2015–19 → 2020–26 | Growth (all) | Growth (core venues) | SA share 2020–26 | SA LQ 2020–26 |
|---|---:|---:|---:|---:|---:|---:|
| C3 Digital geographies & code/space | 179 | 0.13 → 0.11 | 0.85 | 0.97 | 1.7% | 0.59 |
| A15 Urban & planning theory, Southern urbanism | 501 | 0.29 → 0.32 | 1.10 | 1.10 | 8.8% | 3.07 |
| A11 Migration & the city | 2,835 | 1.49 → 1.82 | 1.22 | 1.16 | 14.3% | 4.99 |
| A3 Housing, informality & slums | 14,504 | 7.62 → 9.29 | 1.22 | 1.19 | 13.4% | 4.68 |
| A13 Heritage, mega-events & "world-class" city making | 3,736 | 1.91 → 2.39 | 1.25 | 1.16 | 5.6% | 1.95 |

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

| # | Term | Records 2018–21 → 2022–26 | Share of period's records | Share ratio | OpenAlex-wide SS share ratio | Example (2022–24, highest FWCI) |
|---:|---|---:|---:|---:|---:|---|
| 1 | generative AI | 0 → 158 | 0.0% → 3.22% | ×102.41 | ×247.26 | Jan et al. (2023) [LM06740] |
| 2 | large language models | 0 → 95 | 0.0% → 1.94% | ×61.58 | ×342.67 | Ray (2023) [LM06743] |
| 3 | Unified Payments Interface | 0 → 89 | 0.0% → 1.82% | ×57.69 | ×15.0 | Gupta et al. (2023) [LM08453] |
| 4 | ChatGPT | 0 → 73 | 0.0% → 1.49% | ×47.32 | ×2677.4 | Dwivedi et al. (2023) [LM06741] |
| 5 | digital public infrastructure | 0 → 59 | 0.0% → 1.2% | ×38.24 | ×25.15 | Alonso et al. (2023) [LM04727] |
| 6 | Digital Personal Data Protection Act 2023 | 0 → 48 | 0.0% → 0.98% | ×31.11 | ×356.95 | Kashyap (2024) [LM05037] |
| 7 | digital sovereignty | 0 → 35 | 0.0% → 0.71% | ×22.69 | ×5.32 | Thumfart (2024) [LM06457] |
| 8 | participatory governance | 0 → 33 | 0.0% → 0.67% | ×21.39 | ×3.22 | Lim & Yiğitcanlar (2022) [LM08599] |
| 9 | last-mile delivery | 0 → 28 | 0.0% → 0.57% | ×18.15 | ×2.69 | Cano et al. (2022) [LM07199] |
| 10 | proportionality | 0 → 21 | 0.0% → 0.43% | ×13.61 | ×1.62 | Sukumar (2024) [LM07959] |
| 11 | urban logistics | 0 → 18 | 0.0% → 0.37% | ×11.67 | ×1.53 | Gatta et al. (2023) [LM07224] |
| 12 | UPI | 0 → 18 | 0.0% → 0.37% | ×11.67 | ×8.64 | Sandeep & Mahara (2023) [LM08487] |
| 13 | state capacity | 0 → 16 | 0.0% → 0.33% | ×10.37 | ×1.21 | Khosla & Tushnet (2022) [LM04773] |
| 14 | K.S. Puttaswamy v. Union of India | 0 → 16 | 0.0% → 0.33% | ×10.37 | ×5.43 | Kaur (2024) [LM04348] |
| 15 | EU AI Act | 0 → 15 | 0.0% → 0.31% | ×9.72 | ×29.85 | Laux et al. (2023) [LM04477] |
| 16 | Information Technology Act 2000 | 1 → 30 | 0.06% → 0.61% | ×6.48 | ×5.13 | Siva & Nagarjun (2024) [LM04543] |
| 17 | gig workers | 4 → 77 | 0.25% → 1.57% | ×5.55 | ×3.84 | Wu & Huang (2024) [LM06213] |
| 18 | AI regulation | 3 → 57 | 0.19% → 1.16% | ×5.28 | ×6.16 | Dwivedi et al. (2023) [LM06741] |
| 19 | digital literacy | 12 → 192 | 0.76% → 3.92% | ×4.98 | ×7.1 | Xia et al. (2024) [LM06808] |
| 20 | face recognition | 2 → 37 | 0.13% → 0.75% | ×4.8 | ×2.33 | McElroy & Vergerio (2022) [LM00864] |
| 21 | southern urbanism | 1 → 21 | 0.06% → 0.43% | ×4.54 | ×3.56 | Chakrabarti (2023) [LM03558] |
| 22 | Direct Benefit Transfer | 1 → 19 | 0.06% → 0.39% | ×4.11 | ×5.16 | Pandey & Mehrotra (2024) [LM06679] |
| 23 | responsible AI | 1 → 18 | 0.06% → 0.37% | ×3.89 | ×17.28 | Wach et al. (2023) [LM06786] |
| 24 | facial recognition technology | 1 → 18 | 0.06% → 0.37% | ×3.89 | ×2.69 | Wang et al. (2024) [LM04314] |
| 25 | data breaches | 1 → 17 | 0.06% → 0.35% | ×3.67 | ×2.63 | Larasati et al. (2022) [LM04532] |
| 26 | sustainable urban planning | 1 → 16 | 0.06% → 0.33% | ×3.46 | ×2.28 | Xia et al. (2022) [LM08680] |
| 27 | critical thinking | 1 → 16 | 0.06% → 0.33% | ×3.46 | ×2.41 | Cooper (2023) [LM06752] |
| 28 | Nigeria | 1 → 16 | 0.06% → 0.33% | ×3.46 | ×1.58 | Odoyi & Riekkinen (2022) [LM00619] |
| 29 | foundation models | 1 → 16 | 0.06% → 0.33% | ×3.46 | ×63.51 | Huang et al. (2024) [LM06830] |
| 30 | artificial intelligence in education | 2 → 25 | 0.13% → 0.51% | ×3.24 | ×18.7 | Dwivedi et al. (2023) [LM06741] |

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
2.9% of all Social Sciences works in 2020–26
(3.7% in core venues). The location quotient (LQ) divides a theme's
South Asia share by that baseline. Most urban and development themes sit well above 1, so the
informative cases are the themes with the lowest South Asia share:

| Theme | Adj. works 2020–26 (all venues) | Per 10k SS 2015–19 → 2020–26 | Growth (all) | Growth (core venues) | SA share 2020–26 | SA LQ 2020–26 | India share 2020–26 |
|---|---:|---:|---:|---:|---:|---:|---:|
| C10 Proptech, housing platforms & short-term rentals | 2,238 | 0.81 → 1.43 | 1.77 | 1.80 | 1.1% | 0.39 | 1.0% |
| C4 Urban informatics & urban computing | 1,407 | 0.38 → 0.90 | 2.37 | 2.13 | 1.4% | 0.50 | 1.1% |
| C13 Digital twins, simulation & visual rendering of cities | 2,586 | 0.27 → 1.66 | 6.15 | 4.67 | 1.5% | 0.53 | 1.4% |
| C3 Digital geographies & code/space | 179 | 0.13 → 0.11 | 0.85 | 0.97 | 1.7% | 0.59 | 1.7% |
| B14 Generative AI & society | 38,613 | 0.02 → 24.73 | new | new | 1.8% | 0.62 | 1.3% |
| B2 Datafication, data justice & data colonialism | 1,899 | 0.24 → 1.22 | 5.08 | 3.61 | 2.7% | 0.96 | 2.2% |
| A16 Night-time city & urban time | 1,382 | 0.64 → 0.88 | 1.38 | 1.21 | 2.8% | 0.99 | 2.5% |
| C5 Urban data governance & data justice in cities | 478 | 0.08 → 0.31 | 3.88 | 2.46 | 3.8% | 1.32 | 3.1% |
| C9 Digital mobility (ride-hailing, MaaS, digital ticketing, transit apps) | 2,217 | 0.41 → 1.42 | 3.46 | 2.94 | 3.8% | 1.34 | 2.8% |
| B9 Misinformation & extreme speech | 29,729 | 3.56 → 19.04 | 5.35 | 4.64 | 4.0% | 1.41 | 2.8% |
| A2 Planning, master plans & land-use regulation | 7,730 | 3.05 → 4.95 | 1.62 | 1.65 | 4.4% | 1.52 | 3.2% |
| B1 Platforms & platform capitalism | 6,213 | 0.32 → 3.98 | 12.44 | 7.80 | 4.7% | 1.63 | 4.0% |
| C16 Digital heritage, mapping & representation of cities | 444 | 0.11 → 0.28 | 2.55 | 2.23 | 4.7% | 1.65 | 3.4% |
| C12 Civic tech, e-participation & digital urban publics | 291 | 0.09 → 0.19 | 2.11 | 1.27 | 4.8% | 1.68 | 3.4% |
| A9 Public space, publicness & the street | 6,877 | 2.85 → 4.40 | 1.54 | 1.61 | 4.8% | 1.69 | 3.8% |

7 themes are both fast-growing worldwide and at or below a 5% South Asia share:
digital twins (C13, 1.5%), generative AI (B14, 1.8%), datafication (B2, 2.7%), urban data governance (C5, 3.8%), digital mobility (C9, 3.8%), misinformation (B9, 4.0%), platforms (B1, 4.7%). Generative AI, digital twins, datafication, digital mobility and urban data
governance become gaps S1, S2, S5, S4 and (for India) I3. Misinformation does not: its South
Asia volume (1,198 adjusted works) is large in absolute terms. Nor do
platforms: South Asian platform research sits largely in digital labour and urban gig work
(B11, C15), where South Asia's share is 8.5% and
19.5%. The reverse also holds: digital identity and DPI
(B5, 52.6%), payments in urban economies (C11,
56.7%) and gender, caste and class in the city (A12,
55.3%) are fields where South Asia leads.

**Themes studied mostly in the Global North.** Share of each region among all region mentions
(2010–26, all venues, adjusted; a work naming two regions counts for both):

| Theme | South Asia | Global North | China & East Asia | Southeast Asia | Africa | Latin America | Middle East |
|---|---:|---:|---:|---:|---:|---:|---:|
| C10 Proptech, housing platforms & short-term rentals | 2.3% | 63.1% | 11.9% | 7.5% | 4.6% | 7.0% | 3.5% |
| C3 Digital geographies & code/space | 5.1% | 60.2% | 13.6% | 4.2% | 5.1% | 6.8% | 5.1% |
| A16 Night-time city & urban time | 2.7% | 50.4% | 11.6% | 6.8% | 11.3% | 9.7% | 7.4% |
| C13 Digital twins, simulation & visual rendering of cities | 4.3% | 49.7% | 19.9% | 9.3% | 4.6% | 3.7% | 8.6% |
| B2 Datafication, data justice & data colonialism | 6.2% | 49.2% | 11.7% | 4.9% | 13.1% | 10.9% | 4.0% |
| B3 Surveillance studies | 11.7% | 48.8% | 12.8% | 5.3% | 8.9% | 5.9% | 6.5% |
| C12 Civic tech, e-participation & digital urban publics | 5.8% | 48.5% | 11.2% | 10.4% | 9.2% | 8.8% | 6.2% |
| B4 Algorithmic governance & AI in the public sector | 14.6% | 45.6% | 9.9% | 9.6% | 7.6% | 5.3% | 7.5% |
| B9 Misinformation & extreme speech | 8.3% | 44.3% | 8.6% | 11.6% | 12.6% | 8.4% | 6.2% |
| A9 Public space, publicness & the street | 6.0% | 44.1% | 12.4% | 8.3% | 8.7% | 13.1% | 7.4% |
| C5 Urban data governance & data justice in cities | 5.2% | 42.3% | 18.3% | 11.6% | 9.8% | 7.5% | 5.4% |
| C16 Digital heritage, mapping & representation of cities | 6.0% | 41.8% | 13.4% | 8.3% | 13.4% | 12.1% | 4.9% |
| B12 Infrastructure studies & STS of digital systems | 7.8% | 41.4% | 17.4% | 7.8% | 14.7% | 6.2% | 4.7% |
| C6 Urban surveillance, policing & biometrics in public space | 14.0% | 40.9% | 14.0% | 10.8% | 8.6% | 6.7% | 4.9% |
| C17 Urban cybersecurity & cyber-physical infrastructure | 21.6% | 40.5% | 8.6% | 9.5% | 8.0% | 2.6% | 9.3% |
| B11 Digital labour | 15.7% | 39.9% | 14.3% | 13.6% | 6.2% | 7.2% | 3.1% |
| B1 Platforms & platform capitalism | 8.1% | 39.8% | 17.9% | 13.4% | 8.5% | 7.0% | 5.4% |
| A4 Eviction, resettlement & displacement | 13.2% | 39.3% | 11.2% | 7.8% | 15.6% | 7.8% | 5.1% |
| A2 Planning, master plans & land-use regulation | 5.5% | 38.7% | 20.2% | 9.0% | 11.9% | 6.9% | 7.9% |
| A13 Heritage, mega-events & "world-class" city making | 6.9% | 38.2% | 19.5% | 9.1% | 7.3% | 9.6% | 9.4% |
| A8 Mobility & transport (social science) | 10.3% | 38.1% | 9.5% | 8.6% | 17.9% | 11.5% | 4.1% |
| A15 Urban & planning theory, Southern urbanism | 10.5% | 38.0% | 16.2% | 6.5% | 17.0% | 7.3% | 4.5% |
| C9 Digital mobility (ride-hailing, MaaS, digital ticketing, transit apps) | 6.0% | 38.0% | 28.7% | 14.9% | 4.6% | 5.0% | 2.9% |
| A6 Small towns, census towns & secondary cities | 13.2% | 36.5% | 22.2% | 5.0% | 10.7% | 9.1% | 3.2% |
| A14 Urban environment, climate & risk | 11.2% | 35.8% | 18.0% | 8.5% | 12.7% | 8.5% | 5.2% |
| B10 Cybercrime, fraud & cybersecurity (social science) | 14.1% | 35.5% | 8.8% | 19.2% | 12.7% | 2.6% | 7.1% |
| B14 Generative AI & society | 6.9% | 35.5% | 26.9% | 11.9% | 7.0% | 5.2% | 6.6% |
| C1 Smart cities & smart urbanism | 17.2% | 34.9% | 17.9% | 13.4% | 5.7% | 4.2% | 6.6% |
| C7 Algorithmic & automated urban governance, municipal AI / GenAI | 10.8% | 34.7% | 21.3% | 10.6% | 11.3% | 5.2% | 6.1% |
| B8 Social media, digital publics & political communication | 9.8% | 34.2% | 8.7% | 18.6% | 13.4% | 7.1% | 8.2% |
| C2 Platform urbanism | 16.8% | 32.0% | 20.3% | 12.9% | 6.1% | 7.1% | 4.8% |
| C4 Urban informatics & urban computing | 2.6% | 30.5% | 48.5% | 6.4% | 4.5% | 3.7% | 3.8% |
| A3 Housing, informality & slums | 17.1% | 29.9% | 7.9% | 8.5% | 23.5% | 9.9% | 3.1% |
| A1 Urban governance, decentralisation & municipal finance | 12.5% | 29.0% | 15.0% | 23.0% | 10.7% | 6.8% | 3.0% |
| B7 Digital divides & digital inclusion | 21.6% | 26.1% | 11.1% | 12.5% | 16.3% | 8.3% | 4.2% |
| C15 Gig work in the city (urban and spatial focus) | 25.9% | 25.3% | 18.6% | 17.0% | 4.0% | 7.1% | 2.1% |
| C8 City-level DPI & urban e-government | 12.0% | 24.7% | 11.6% | 32.0% | 9.3% | 4.5% | 5.9% |
| B13 Mobile phones & everyday digital life | 31.7% | 22.7% | 13.8% | 7.0% | 16.3% | 4.2% | 4.3% |
| A12 Gender, caste, class & the city | 47.6% | 21.6% | 6.9% | 5.0% | 8.7% | 6.5% | 3.7% |
| A5 Land, peri-urban & extended urbanisation | 17.1% | 18.9% | 15.3% | 12.0% | 26.0% | 8.6% | 2.1% |
| A7 Urban infrastructure (water, sanitation, energy) & infrastructural citizenship | 21.3% | 18.5% | 9.6% | 7.8% | 29.8% | 8.9% | 4.2% |
| C18 Neighbourhood platforms & digital public space (WhatsApp, Nextdoor, RWA groups) | 29.4% | 17.7% | 3.7% | 22.4% | 14.7% | 5.7% | 6.2% |
| B5 Digital identity & digital public infrastructure (DPI) | 55.6% | 15.6% | 4.3% | 9.2% | 8.6% | 3.2% | 3.5% |
| A11 Migration & the city | 11.8% | 13.6% | 38.3% | 8.8% | 16.7% | 5.7% | 5.1% |
| C14 Digital informality (informal settlements, vendors & digital systems) | 30.1% | 12.0% | 4.6% | 11.7% | 27.0% | 11.0% | 3.7% |
| A10 Urban economy, informal work & street vending | 19.4% | 10.0% | 5.2% | 15.4% | 25.6% | 22.1% | 2.3% |
| B6 Digital finance & payments | 31.3% | 9.7% | 8.0% | 23.4% | 21.4% | 2.4% | 3.7% |
| C11 Digital payments in urban economies (QR, UPI, mobile money) | 55.4% | 4.3% | 3.7% | 27.4% | 6.2% | 1.9% | 1.0% |

The Global North accounts for about half or more of the region mentions in proptech and
short-term rentals (C10, 63.1%), digital geographies (C3,
60.2%), the night-time city (A16,
50.4%) and digital twins (C13, 49.7%),
and nearly half in datafication (B2), surveillance studies (B3), civic tech (C12) and algorithmic
governance (B4): in these themes most place-specific work is about Northern cities. Fourteen themes
are led by another region: South Asia leads A12, B5, B6, B13, C11, C14, C15 and C18; Africa
leads peri-urban land, infrastructure and the informal urban economy (A5, A7, A10); China and
East Asia lead migration (A11) and urban computing (C4); Southeast Asia leads city e-government
(C8).

**India.** Indian places are named in 2.2% of all Social Sciences
works in 2020–26 (2.8% in core venues). The themes with the lowest
India share:

| Theme | Growth (all) | India adj. 2020–26 (all / core) | India share 2020–26 (all / core) | India LQ | Delhi/NCR adj. 2010–26 (all / core) | Haryana adj. 2010–26 (all / core) |
|---|---:|---:|---:|---:|---:|---:|
| C10 Proptech, housing platforms & short-term rentals | 1.77 | 22 / 7 | 1.0% / 0.6% | 0.44 | 1 / 0 | 0 / 0 |
| C4 Urban informatics & urban computing | 2.37 | 16 / 7 | 1.1% / 0.7% | 0.51 | 1 / 0 | 0 / 0 |
| B14 Generative AI & society | new | 513 / 207 | 1.3% / 1.0% | 0.60 | 24 / 11 | 3 / 0 |
| C13 Digital twins, simulation & visual rendering of cities | 6.15 | 36 / 14 | 1.4% / 0.8% | 0.63 | 3 / 2 | 0 / 0 |
| C3 Digital geographies & code/space | 0.85 | 3 / 2 | 1.7% / 1.8% | 0.76 | 0 / 0 | 0 / 0 |
| B2 Datafication, data justice & data colonialism | 5.08 | 41 / 17 | 2.2% / 1.9% | 0.98 | 1 / 1 | 0 / 0 |
| A16 Night-time city & urban time | 1.38 | 35 / 11 | 2.5% / 1.9% | 1.14 | 6 / 3 | 1 / 0 |
| C9 Digital mobility (ride-hailing, MaaS, digital ticketing, transit apps) | 3.46 | 62 / 29 | 2.8% / 1.8% | 1.26 | 9 / 6 | 0 / 0 |
| B9 Misinformation & extreme speech | 5.35 | 836 / 316 | 2.8% / 2.4% | 1.27 | 38 / 20 | 12 / 6 |
| C5 Urban data governance & data justice in cities | 3.88 | 15 / 5 | 3.1% / 2.3% | 1.42 | 1 / 0 | 0 / 0 |
| A2 Planning, master plans & land-use regulation | 1.62 | 250 / 120 | 3.2% / 3.3% | 1.46 | 54 / 26 | 12 / 6 |
| C16 Digital heritage, mapping & representation of cities | 2.55 | 15 / 7 | 3.4% / 2.6% | 1.53 | 2 / 1 | 0 / 0 |
| C12 Civic tech, e-participation & digital urban publics | 2.11 | 10 / 3 | 3.4% / 2.6% | 1.55 | 1 / 0 | 1 / 0 |
| A9 Public space, publicness & the street | 1.54 | 262 / 96 | 3.8% / 3.7% | 1.72 | 65 / 26 | 5 / 3 |

Two patterns stand out. First, the India-thin themes are the computational and
Northern-framed corners of the map (proptech, urban informatics, digital twins, generative AI,
datafication) plus, among urban themes, the night-time city, planning and land-use regulation,
and public space. Second, India's share drops sharply from all venues to core venues for
urban cybersecurity (C17, 8.3% → 2.9%), cybercrime (B10, 5.6% → 3.2%), platform urbanism (C2, 11.7% → 6.9%), digital divides (B7, 12.6% → 7.5%), digital twins (C13, 1.4% → 0.8%): on these topics Indian work is more often published outside core
venues than work on other places.

## 7. Candidate gaps

Twenty-five leads, each with population-count evidence (all venues and core venues), three
example records (titles in the Candidate gaps tab) and a caveat. A gap means a topic is thin in
OpenAlex relative to its neighbours or to the rest of the world: a lead to check, not a proof. Four provisional India and Delhi gaps of the
draft were dropped once the India and Delhi counts came in (municipal AI, urban surveillance and
urban cybersecurity in India; digital mobility in Delhi), because India's or Delhi's share of
those themes is above its share of all social science works.

### 7.1 Global

**G1. Neighbourhood platforms and resident groups as digital public space** (C18)  
*Evidence.* About 525 works in 2020–26 worldwide (all venues; raw 5,524 hits × estimated precision 0.10); core venues 145. For comparison, B8 social media and digital publics: 7,893 (core 2,558).  
*Examples* (77 matching records): Williams et al. (2014) [LM09331]; Kurwa (2019) [LM09332]; Barnett & Townend (2014) [LM09333].  
*Missing.* Neighbourhood WhatsApp/Telegram groups, resident-welfare-association groups and Nextdoor-type platforms as infrastructures of local governance and exclusion, especially outside the US and UK; most existing work is on hyperlocal journalism.  
*Caveat.* Precision is very low (4 of 40 sampled hits in scope), so the count is uncertain; such groups also go by names the queries miss.

**G2. AI and generative AI inside city governments** (C7)  
*Evidence.* Municipal/urban AI (C7): 957 works in 2020–26 (core 428), against 6,001 for algorithmic governance and public-sector AI in general (B4) and 38,613 for generative AI and society (B14). C7 grew ×15.25 in normalised share from 2015–19, but from a very small base.  
*Examples* (112 matching records): Son et al. (2023) [LM07847]; Cugurullo (2020) [LM07848]; Yiğitcanlar et al. (2021) [LM07849].  
*Missing.* Empirical studies of AI and GenAI systems that city governments actually run (procurement, frontline use, effects on residents), rather than frameworks, reviews and visions.  
*Caveat.* City deployments are often called 'smart city analytics' or 'decision support' and may sit under C1 or C4.

**G3. Social science of urban cybersecurity and cyber-physical infrastructure** (C17)  
*Evidence.* C17: 1,175 works in 2020–26 (core 416; precision 0.34), against 21,267 for cybercrime and cybersecurity in general (B10).  
*Examples* (70 matching records): Elmaghraby & Losavio (2014) [LM06976]; Cui et al. (2018) [LM09206]; Habibzadeh et al. (2019) [LM05952].  
*Missing.* Governance and political-economy studies of attacks on city systems (municipal ransomware, control-room and utility security, who bears the costs), rather than engineering designs.  
*Caveat.* Engineering dominates the hit set; social-science work may say 'resilience' or 'critical infrastructure' instead of 'cyber'.

**G4. How city governments govern data** (C5)  
*Evidence.* C5 urban data governance and data justice: 478 works in 2020–26 (core 214), against 1,899 on datafication and data justice in general (B2) and 5,399 on smart cities (C1).  
*Examples* (99 matching records): van Zoonen (2016) [LM06983]; Barns (2017) [LM07590]; Pereira et al. (2016) [LM07592].  
*Missing.* Municipal data practice (data-sharing agreements, city data officers, data trusts, vendor lock-in) and data-justice claims at city scale, especially outside Europe and North America.  
*Caveat.* Overlaps smart-city governance (C1); open-data portal studies dominate the matches.

**G5. The night-time city beyond the night-time economy** (A16)  
*Evidence.* A16: 1,382 works in 2020–26 (core 580), 0.88 per 10,000 social science works; normalised growth ×1.38 from 2015–19, the fifth-lowest of the 16 urban (A) themes.  
*Examples* (122 matching records): Chatterton & Hollands (2003) [LM03660]; Tomsen (2003) [LM03664]; Cressey (2008) [LM03665].  
*Missing.* Night as a dimension of urban governance beyond leisure and alcohol: night work, night-time services and mobility, access and safety at night, operating hours.  
*Caveat.* The vocabulary of night and urban time is scattered; adjacent work may be missed.

**G6. Small towns and secondary cities outside metropolitan research** (A6)  
*Evidence.* A6: 1,805 works in 2020–26 (core 927), 1.16 per 10,000 social science works, against 4.37 for peri-urban and extended urbanisation (A5) and 9.29 for housing and informality (A3).  
*Examples* (267 matching records): Pojani & Stead (2015) [LM01227]; Giffinger et al. (2008) [LM01228]; Kyttä (2002) [LM01229].  
*Missing.* Governance, services, economy and digital change in small and secondary cities studied in their own right, not as a backdrop to metropolitan or rural questions.  
*Caveat.* Studies of named small cities often avoid the generic terms the queries use, so counts understate the field.

**G7. City-level civic tech after the pilot stage** (C12)  
*Evidence.* C12: 291 works in 2020–26 (core 117; precision 0.30), against 5,399 on smart cities (C1).  
*Examples* (101 matching records): Cardullo & Kitchin (2018) [LM06950]; Gabrys (2014) [LM06954]; Capdevila & Zarlenga (2015) [LM08572].  
*Missing.* Longitudinal studies of civic-tech and e-participation platforms after launch (uptake, who participates, effects on decisions), and of grievance apps in Global South cities.  
*Caveat.* National e-participation studies fall outside this urban theme.


### 7.2 South Asia

**S1. Generative AI and society in South Asia** (B14)  
*Evidence.* South Asian places are named in 1.8% of B14 works in 2020–26 (all venues; 684 works), against 2.9% for all social science works (location quotient 0.62, the lowest of the 14 digital-society (B) themes); core venues: 1.3%. Globally B14 is new since 2022 (38,613 works).  
*Examples* (79 matching records): Agrawal (2023) [LM06815]; Kumar et al. (2025) [LM06818]; Sharma et al. (2023) [LM06822].  
*Missing.* Social-science studies of GenAI use and governance in South Asian workplaces, public services and languages, beyond adoption surveys in higher education.  
*Caveat.* GenAI papers rarely name a place, which lowers every region's share; among B14 works that do name a region, 6.9% name South Asia, against 26.9% China and East Asia and 35.5% the Global North. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S2. Digital twins and 3D city models in South Asian cities** (C13)  
*Evidence.* 39 South Asia works in 2020–26 (1.5% of C13; location quotient 0.53; core 1.0%), while C13 grew ×6.15 worldwide.  
*Examples* (48 matching records): Bauer et al. (2021) [LM08735]; Saran et al. (2015) [LM08743]; Naveed et al. (2025) [LM08747].  
*Missing.* Digital twins and 3D city models in South Asian smart-city programmes: whose data, which vendors, how models enter planning, who is left out.  
*Caveat.* Remote-sensing and GIS work on South Asian cities is large but sits outside C13 unless it uses twin or 3D-model vocabulary. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S3. Proptech, rental platforms and short-term rentals in South Asia** (C10)  
*Evidence.* 25 South Asia works in 2020–26 (1.1% of C10, location quotient 0.39, the lowest of all 48 themes; core 0.7%).  
*Examples* (42 matching records): Tamilmani et al. (2020) [LM08340]; Chatterjee et al. (2019) [LM08343]; Negi & Tripathi (2022) [LM08344].  
*Missing.* Rental and housing platforms, broker apps and short-term rentals in South Asian cities and their effects on rents, informal tenancy and regulation.  
*Caveat.* C10 is dominated by Airbnb studies; South Asian platforms may be studied as marketing or tourism. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S4. Digital mobility in South Asian cities** (C9)  
*Evidence.* 85 South Asia works in 2020–26 (3.8% of C9, location quotient 1.34, against 2.83 for mobility and transport in general, A8; core 2.5%), while C9 grew ×3.46 worldwide.  
*Examples* (48 matching records): Agarwal et al. (2023) [LM08183]; Kanuri et al. (2019) [LM08185]; Singh (2019) [LM08186].  
*Missing.* Ride-hailing, app-based paratransit, digital ticketing and transit apps in South Asian cities: access, gender, informal operators, fares and data.  
*Caveat.* Engineering studies are excluded by design; some social-science work sits in A8 or C15. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S5. Datafication and data justice beyond identity and payments in South Asia** (B2 B5)  
*Evidence.* B2 datafication and data justice: South Asia share 2.7% in 2020–26 (location quotient 0.96; 52 works), against 52.6% for digital identity and DPI (B5, quotient 18.39) and 20.4% for digital finance (B6).  
*Examples* (62 matching records): Thakkar et al. (2022) [LM04149]; Krishna (2020) [LM04735]; Taylor & Richter (2017) [LM04152].  
*Missing.* Datafication beyond Aadhaar and UPI: welfare and police databases, municipal, health and land records, and data-justice claims by affected groups.  
*Caveat.* Much South Asian datafication work is framed through identity and counted under B5. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S6. Public space and the street in South Asian cities** (A9)  
*Evidence.* South Asia share of A9 works in 2020–26: 4.8% (location quotient 1.69, the third-lowest of the 16 urban (A) themes; 333 works; core 4.8%), against 18.1% for urban economy and street vending (A10).  
*Examples* (109 matching records): Anjaria (2009) [LM02147]; Roy & Bailey (2021) [LM02154]; Mahadevia & Lathia (2019) [LM02153].  
*Missing.* Publicness, access and everyday use of streets, parks and squares in South Asian cities (gender, caste and class in access; regulation; design).  
*Caveat.* South Asian street research often sits under vending (A10) or informality (A3), or uses words such as 'footpath', 'bazaar' or 'maidan'. The Indian-venue coverage limits (Coverage limits table) apply here too.

**S7. Digital mapping and representation of South Asian cities** (C16)  
*Evidence.* 21 South Asia works in 2020–26 (4.7% of C16, location quotient 1.65; core 4.1%).  
*Examples* (27 matching records): Luthra (2018) [LM09120]; Meggi (2017) [LM09133]; Janu (2026) [LM09184].  
*Missing.* How South Asian cities are digitally mapped and represented: map coverage of informal settlements, digital heritage of historic cores, street-view imagery.  
*Caveat.* Technical mapping of South Asian cities appears in remote-sensing venues that the screening excludes. The Indian-venue coverage limits (Coverage limits table) apply here too.


### 7.3 India

**I1. Urban informatics and urban computing on Indian cities** (C4)  
*Evidence.* Indian places are named in 1.1% of C4 works in 2020–26 (16 adjusted works; core venues 0.7%, 7 works), against 2.2% of all social science works (location quotient 0.51, the second-lowest of all 48 themes). C4's region mentions are led by China and East Asia (48.5%).  
*Examples* (85 matching records): Shukla et al. (2016) [LM07510]; Bauer et al. (2021) [LM08735]; Saran et al. (2015) [LM08743].  
*Missing.* Urban-data and urban-computing work on Indian cities, critical as well as technical: what city data exist and who holds them, and analyses built on them.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**I2. Master plans and land-use regulation in India** (A2)  
*Evidence.* India share of A2 works in 2020–26: 3.2% (core 3.3%; 250 adjusted works), location quotient 1.46, the second-lowest of the 16 urban (A) themes; against 10.7% for housing and informality (A3) and 12.1% for peri-urban land (A5).  
*Examples* (113 matching records): Cervero et al. (2013) [LM00276]; Sundaresan (2017) [LM00295]; Kumar & Pushplata (2013) [LM00309].  
*Missing.* Studies of how master plans, development control rules and land-use regulation are made, contested and enforced in Indian cities, beyond critiques of individual plans.  
*Caveat.* Much Indian planning writing appears in EPW and planning-practice outlets that OpenAlex barely holds. Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**I3. Municipal data governance in Indian cities** (C5)  
*Evidence.* India share of C5 works in 2020–26: 3.1% (core 2.3%), 15 adjusted works (core 5); location quotient 1.42, against 3.47 for smart cities (C1).  
*Examples* (22 matching records): Singh & Upadhyay (2022) [LM07047]; Kennedy et al. (2020) [LM04159]; Long (2015) [LM07651].  
*Missing.* How Indian city governments and smart-city companies collect, share and govern data (data policies and officers, command-centre data, vendor contracts), and city-level data-justice claims.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**I4. Civic tech and e-participation in Indian cities** (C12)  
*Evidence.* India share of C12 works in 2020–26: 3.4% (core 2.6%), 10 adjusted works (core 3); location quotient 1.55.  
*Examples* (51 matching records): Gupta et al. (2016) [LM08017]; Samuel et al. (2020) [LM08021]; Sintomer et al. (2014) [LM08618].  
*Missing.* Grievance apps, participatory-budgeting platforms and ward-level digital participation in Indian cities: who uses them and what changes.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**I5. The night-time city in India** (A16)  
*Evidence.* India share of A16 works in 2020–26: 2.5% (core 1.9%), 35 adjusted works (core 11); location quotient 1.14, the lowest of the 16 urban (A) themes.  
*Examples* (50 matching records): Jeffrey (2010) [LM03676]; Carswell et al. (2018) [LM03699]; Parikh (2017) [LM03705].  
*Missing.* Night-time work, services, mobility and access in Indian cities beyond women's safety: operating hours, night shifts, night markets.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.


### 7.4 Delhi/NCR and Haryana

**H1. Haryana's secondary cities beyond Gurugram and Faridabad** (A6)  
*Evidence.* Works naming Haryana's secondary cities with urban content (supplementary set S7), 2010–26: 387 adjusted works, 127 in core venues; small-town and secondary-city works (A6) naming any Haryana place: 10 (core 4).  
*Examples* (59 matching records): Fatewar & Yadav (2023) [LM01390]; Dangi (2026) [LM01443]; Bhagwan (1974) [LM01448].  
*Missing.* Governance, economy, infrastructure and digital change in Rohtak, Hisar, Panipat, Karnal, Sonipat, Ambala, Yamunanagar, Rewari and other Haryana cities (what the map holds is described in §9).  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**H2. Digital identity and e-government in Haryana** (B5 C8)  
*Evidence.* Haryana-named works 2010–26: B5 5 adjusted (core 0), C8 4 (core 1); Delhi/NCR-named B5 works 28.  
*Examples* (3 matching records): Anchal & Phougat (2026) [LM04858]; Gond & Yadav (2023) [LM08093]; Meena (2026) [LM08114].  
*Missing.* Haryana's state family-ID database and city-level e-government: how eligibility data are produced and corrected, and how residents and officials work with them.  
*Caveat.* Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.

**H3. Gurugram and Haryana in platform, gig-work and digital-mobility research** (C15 C9 C2)  
*Evidence.* Works naming any Haryana place (Gurugram included), 2010–26, adjusted: urban gig work (C15) 0, digital mobility (C9) 0, platform urbanism (C2) 1, proptech (C10) 0; against Delhi/NCR-named C15 15 (core 6), C9 9 and C2 6.  
*Examples* (2 matching records): Nair (2026) [LM06336]; Pal & Kumar (2026) [LM07362].  
*Missing.* Gurugram and the Haryana NCR as sites of platform work, quick-commerce warehousing, app-based mobility and housing platforms, studied by name rather than folded into "Delhi".  
*Caveat.* Works about Gurugram that name only "Delhi" or "NCR" are not counted for Haryana. Coverage limit (Coverage limits table): OpenAlex holds EPW only from 2024, has no Seminar, and has Shodhganga theses only to 2021, almost all without abstracts and outside the count filters, so Indian writing is undercounted. Check EPW and Shodhganga by hand before relying on this.


## 8. Methodological gaps

Method is inferred from abstracts by keyword cues and is known for 5,721 of
8,949 theme records; shares below are among records with a known method, with
the n. No method claim is made where fewer than 50 records have a known method (one theme,
C18). Per-theme shares are in the Methods tab.

| Group | Records | Known method (n) | Qualitative | Quantitative | Mixed | Review | Conceptual | Computational |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Domain A (all records) | 3458 | 2067 | 31% | 13% | 13% | 4% | 35% | 4% |
| Domain B (all records) | 3052 | 1983 | 24% | 20% | 9% | 5% | 34% | 8% |
| Domain C (all records) | 2439 | 1671 | 24% | 19% | 12% | 7% | 25% | 14% |
| A, India-flagged | 1315 | 780 | 38% | 10% | 13% | 3% | 32% | 4% |
| A, Global North | 328 | 237 | 32% | 18% | 6% | 1% | 39% | 4% |
| B, India-flagged | 1067 | 725 | 27% | 18% | 10% | 4% | 35% | 6% |
| B, Global North | 233 | 180 | 27% | 26% | 10% | 3% | 29% | 6% |
| C, India-flagged | 758 | 559 | 26% | 23% | 15% | 4% | 20% | 12% |
| C, Global North | 325 | 256 | 33% | 17% | 8% | 4% | 25% | 13% |

The urban themes lean qualitative and conceptual; the C themes carry most computational work
(13.8% of known-method C records). India-flagged urban records are
less often quantitative than Global North ones (10.1% against
18.1%), while in the C themes the order reverses
(22.7% against 17.2%); these are
differences within the sample. Three gaps stand out:

**M1. Few qualitative studies of digital twins and city models in use** (C13)  
*Evidence.* Among the 126 C13 records with a known method, 7.9% are qualitative and 46.8% computational (the map's records; the method is inferred from abstracts).  
*Examples* (10 matching records): Nochta et al. (2020) [LM08702]; Peldon et al. (2024) [LM08732]; Saeidian et al. (2023) [LM08742].  
*Missing.* Ethnographic and interview studies of how digital twins and city models are built, bought and used in planning offices.  
*Caveat.* Method shares come from the map's records and are inferred from abstracts.

**M2. Few field studies of municipal and generative AI in use** (C7 B14)  
*Evidence.* Qualitative records: C7 15.3% of 111 with a known method, B14 10.6% of 142; reviews make up 14.4% and 12.7%.  
*Examples* (32 matching records): Tlili et al. (2023) [LM06745]; Cooper (2023) [LM06752]; Cugurullo (2020) [LM07848].  
*Missing.* Field studies (observation, interviews, documents) of AI and GenAI inside public organisations and cities, rather than reviews, frameworks and perception surveys.  
*Caveat.* Method shares come from the map's records and are inferred from abstracts; B14 is very young.

**M3. Digital payments studied mostly through adoption surveys** (B6 C11)  
*Evidence.* Qualitative records: B6 10.6% of 132 with a known method (quantitative 50.0%); C11 16.0% of 94 (quantitative and mixed 44.7% and 20.2%).  
*Examples* (54 matching records): Hughes & Lonie (2007) [LM04933]; Maurer (2012) [LM04955]; Leong et al. (2017) [LM04956].  
*Missing.* Ethnographies of payment practice among urban vendors, workers and households: how QR and UPI payments change credit, record-keeping, tax visibility and bargaining.  
*Caveat.* 


## 9. Shortlist leads (S1–S7)

The researcher's leads were searched separately so as not to bias the map. OpenAlex-wide counts
(same filters, precision-adjusted with a 40-work sample of each set's India hit set, which is
small for S3 and S4) and the map's records:

| Lead | OpenAlex-wide, adj. (all / core) | India-named, adj. (all / core) | Haryana-named, adj. (all / core) | Precision p | Map records | India-flagged | Haryana-flagged |
|---|---:|---:|---:|---:|---:|---:|---:|
| S1 Railway stations | 2,262 / 1,119 | 162 / 70 | 2 / 1 | 0.31 | 146 | 67 | 4 |
| S2 Waiting and waiting rooms | 195 / 130 | 8 / 4 | 0 / 0 | 0.02 | 35 | 12 | 1 |
| S3 Night-time transit and transit operating hours | 57 / 33 | 2 / 2 | 0 / 0 | 0.22 | 64 | 13 | 0 |
| S4 Fare integration and transit cards (incl. NCMC) | 303 / 207 | 11 / 5 | 0 / 0 | 0.46 | 53 | 13 | 0 |
| S5 Rail-led urbanism and transit-oriented development | 267 / 166 | 66 / 36 | 3 / 2 | 0.55 | 159 | 87 | 6 |
| S6 Elevated rail and infrastructure undersides | 127 / 53 | 15 / 7 | 0 / 0 | 0.16 | 55 | 27 | 1 |
| S7 Haryana secondary cities (excluding Gurugram and Faridabad) | 387 / 127 | (Haryana set) | 387 / 127 | 0.32 | 75 | 57 | 56 |

India-flagged records per lead (S7: Haryana-flagged), by method (inferred; known n) and venue
type. Method shares support no claim where fewer than 50 records have a known method (all leads
except S5):

| Lead | India-flagged records | Known method (n) | Qual. | Quant. | Mixed | Review | Concept. | Comput. | Journal (core) | Journal (non-core) | Book/chapter | Conference | Thesis | Repository/preprint | Other |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S1 Railway stations | 67 | 38 | 13 | 9 | 7 | 1 | 5 | 3 | 29 | 18 | 4 | 10 | 0 | 6 | 0 |
| S2 Waiting and waiting rooms | 12 | 9 | 5 | 1 | 0 | 0 | 3 | 0 | 6 | 3 | 0 | 2 | 1 | 0 | 0 |
| S3 Night-time transit and transit operating hours | 13 | 10 | 5 | 2 | 1 | 0 | 2 | 0 | 7 | 3 | 1 | 1 | 0 | 1 | 0 |
| S4 Fare integration and transit cards (incl. NCMC) | 13 | 8 | 2 | 1 | 2 | 1 | 2 | 0 | 0 | 8 | 0 | 1 | 0 | 4 | 0 |
| S5 Rail-led urbanism and transit-oriented development | 87 | 58 | 20 | 10 | 7 | 1 | 14 | 6 | 27 | 30 | 12 | 7 | 1 | 9 | 1 |
| S6 Elevated rail and infrastructure undersides | 27 | 15 | 3 | 4 | 4 | 0 | 1 | 3 | 7 | 8 | 3 | 4 | 0 | 5 | 0 |
| S7 Haryana secondary cities (excluding Gurugram and Faridabad) (Haryana-flagged) | 56 | 33 | 4 | 12 | 3 | 0 | 3 | 11 | 15 | 24 | 4 | 5 | 1 | 6 | 1 |

**Railway stations (S1).** India-named station research is mostly transport planning — transfer
facilities, willingness to pay, service quality — and engineering. The strongest qualitative work
treats stations as social spaces: Gupta (2021) [LM01805] on caste, waste and cleaning labour, and
Gupta (2023) [LM01864] on waiting. Haryana-named station work is almost absent
(2 adjusted works). Missing: stations as public and labour spaces, and
suburban and NCR stations.

**Waiting (S2).** The India work is on waiting for the state, not in transit:
Carswell et al. (2018) [LM03699], Raphael (2022) [LM04749] and Sharma (2024) [LM03734], alongside *Timepass*,
Jeffrey (2010) [LM03676]. The OpenAlex count is uncertain (estimated precision
0.02: most "waiting" hits are queueing models). Missing: waiting rooms, platforms and bus
stops as social and temporal experience.

**Night-time transit (S3).** Near-absent worldwide (57 adjusted works,
2 India-named). The India records are on night-time fear and the night
economy — Roy (2026) [LM03732], Sahoo & Bigith.V.B (2023) [LM03750] — not on night transport. Missing: night bus
services and operating hours, night-shift commuting, women's travel after dark.

**Fare integration and transit cards (S4).** 11 India-named adjusted works
(5 in core venues); the India-flagged records include no core-venue
journal article, and no record in the map names the National Common Mobility Card in its title
or abstract. The nearest are Petel (2021) [LM08272], a case study of fare integration in Ahmedabad, and
Rahman (2013) [LM08205], a thesis on integrating rickshaws with BRT in Dhaka. Missing: the social science of NCMC and fare integration — who
gains, fare policy, data.

**Rail-led urbanism and TOD (S5).** The best-covered lead: India accounts for
66 of 267 adjusted works worldwide. Most India work sets
planning criteria (influence zones, land value capture); the strongest qualitative and policy studies are Mittal & Shah (2021) [LM00360] on
metro-TOD policy, Rangwala et al. (2014) [LM00345] on Mumbai and Bon (2016) [LM00395] on East Delhi's metro.
Missing: TOD and value capture in Haryana (Gurugram, the RRTS corridor) and corridor
displacement.

**Elevated rail and undersides (S6).** India-named: 15 adjusted works, mostly
engineering. One strong qualitative work: Harris (2018) [LM01562] on Mumbai's flyovers and
skywalks. Missing: undersides as livelihood and shelter spaces, and elevated metros and street
life.

**Haryana secondary cities (S7).** 387 adjusted works name these cities with
urban content (127 in core venues). Most Haryana-flagged records in the
map are urban-growth mapping, air-quality and waste studies; the social-science works are few
and descriptive: Bhagwan (1974) [LM01448],
Munjal (2016) [LM01319], Satpal et al. (2024) [LM01336]. Missing: governance, economy, everyday life and
digital change in these cities (gap H1).

## 10. Limits

- **Precision.** Counts are adjusted by 40-work samples, and the blind check behind the domain
  factors used six records per theme; it predates the India page-2 records (about a fifth of the
  map), which went through the same rules and hand review. Least certain: C18 (estimated precision 0.10), C6
  (0.27), C11 (0.27), C15 (0.29), C3 (0.29) and lead S2.
- **Place signal.** Places come from titles and abstracts, not affiliations; works naming no
  place count for no region, which matters most for generative AI and conceptual themes.
- **Coverage.** Indian venues and theses are under-covered (Section 1); about a fifth of the
  records have no abstract, and their method and region tags are thin.
- **Vocabulary.** Exact-phrase queries miss work that uses other words; each gap names the
  likely blind spot.
