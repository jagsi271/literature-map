"""Place names used to tag 'Places studied', 'Region' and the India / Delhi-NCR / Haryana flags.

Matching is on title + abstract text only (never on author affiliations). Region buckets follow
BRIEF.md §4; two judgement calls are documented in the spreadsheet's Read me: North Africa is
counted as Africa, and Central Asia / Caucasus as Middle East. Pacific island states are
counted as Southeast Asia (rare in this corpus).
"""
import re

GN, EA, SA, SEA, AF, LA, ME = (
    "Global North", "China & East Asia", "South Asia", "Southeast Asia", "Africa",
    "Latin America", "Middle East",
)

# country -> region ; aliases map to the canonical country name
COUNTRIES = {
    # Global North
    "United States": GN, "Canada": GN, "United Kingdom": GN, "Ireland": GN, "France": GN,
    "Germany": GN, "Netherlands": GN, "Belgium": GN, "Luxembourg": GN, "Switzerland": GN,
    "Austria": GN, "Italy": GN, "Spain": GN, "Portugal": GN, "Greece": GN, "Denmark": GN,
    "Sweden": GN, "Norway": GN, "Finland": GN, "Iceland": GN, "Poland": GN, "Czechia": GN,
    "Slovakia": GN, "Hungary": GN, "Romania": GN, "Bulgaria": GN, "Croatia": GN, "Slovenia": GN,
    "Serbia": GN, "Bosnia and Herzegovina": GN, "Albania": GN, "North Macedonia": GN,
    "Estonia": GN, "Latvia": GN, "Lithuania": GN, "Ukraine": GN, "Belarus": GN, "Russia": GN,
    "Malta": GN, "Cyprus": GN, "Australia": GN, "New Zealand": GN,
    # China & East Asia
    "China": EA, "Hong Kong": EA, "Taiwan": EA, "Japan": EA, "South Korea": EA,
    "North Korea": EA, "Mongolia": EA, "Macau": EA,
    # South Asia
    "India": SA, "Pakistan": SA, "Bangladesh": SA, "Nepal": SA, "Sri Lanka": SA, "Bhutan": SA,
    "Maldives": SA, "Afghanistan": SA,
    # Southeast Asia (+ Pacific)
    "Indonesia": SEA, "Malaysia": SEA, "Singapore": SEA, "Thailand": SEA, "Vietnam": SEA,
    "Philippines": SEA, "Myanmar": SEA, "Cambodia": SEA, "Laos": SEA, "Timor-Leste": SEA,
    "Brunei": SEA, "Papua New Guinea": SEA, "Fiji": SEA,
    # Africa (incl. North Africa)
    "South Africa": AF, "Nigeria": AF, "Kenya": AF, "Ghana": AF, "Ethiopia": AF, "Tanzania": AF,
    "Uganda": AF, "Rwanda": AF, "Zambia": AF, "Zimbabwe": AF, "Malawi": AF, "Mozambique": AF,
    "Angola": AF, "Namibia": AF, "Botswana": AF, "Senegal": AF, "Mali": AF, "Burkina Faso": AF,
    "Niger": AF, "Cameroon": AF, "Ivory Coast": AF, "Benin": AF, "Togo": AF, "Sierra Leone": AF,
    "Liberia": AF, "Guinea": AF, "Democratic Republic of the Congo": AF, "Congo": AF,
    "Sudan": AF, "South Sudan": AF, "Somalia": AF, "Madagascar": AF, "Egypt": AF, "Morocco": AF,
    "Algeria": AF, "Tunisia": AF, "Libya": AF, "Gambia": AF, "Lesotho": AF, "Eswatini": AF,
    "Mauritius": AF, "Burundi": AF, "Eritrea": AF,
    # Latin America & Caribbean
    "Brazil": LA, "Mexico": LA, "Argentina": LA, "Chile": LA, "Colombia": LA, "Peru": LA,
    "Ecuador": LA, "Bolivia": LA, "Venezuela": LA, "Uruguay": LA, "Paraguay": LA, "Cuba": LA,
    "Haiti": LA, "Dominican Republic": LA, "Puerto Rico": LA, "Jamaica": LA, "Guatemala": LA,
    "Honduras": LA, "El Salvador": LA, "Nicaragua": LA, "Costa Rica": LA, "Panama": LA,
    "Trinidad and Tobago": LA,
    # Middle East (+ Central Asia, Caucasus)
    "Turkey": ME, "Iran": ME, "Iraq": ME, "Syria": ME, "Lebanon": ME, "Israel": ME,
    "Palestine": ME, "Saudi Arabia": ME, "United Arab Emirates": ME, "Qatar": ME, "Kuwait": ME,
    "Bahrain": ME, "Oman": ME, "Yemen": ME, "Kazakhstan": ME, "Uzbekistan": ME,
    "Kyrgyzstan": ME, "Tajikistan": ME, "Turkmenistan": ME, "Azerbaijan": ME, "Armenia": ME,
}

ALIASES = {
    "USA": "United States", "U.S.": "United States", "United States of America": "United States",
    "America": "United States", "American": "United States", "UK": "United Kingdom",
    "Britain": "United Kingdom", "British": "United Kingdom", "England": "United Kingdom",
    "Scotland": "United Kingdom", "Wales": "United Kingdom", "Chinese": "China",
    "Japanese": "Japan", "Korea": "South Korea", "Korean": "South Korea", "Indian": "India",
    "Pakistani": "Pakistan", "Bangladeshi": "Bangladesh", "Nepali": "Nepal", "Nepalese": "Nepal",
    "Sri Lankan": "Sri Lanka", "Indonesian": "Indonesia", "Vietnamese": "Vietnam",
    "Viet Nam": "Vietnam", "Filipino": "Philippines", "Thai": "Thailand",
    "Malaysian": "Malaysia", "Kenyan": "Kenya", "Nigerian": "Nigeria", "Ghanaian": "Ghana",
    "South African": "South Africa", "Ethiopian": "Ethiopia", "Brazilian": "Brazil",
    "Mexican": "Mexico", "Argentine": "Argentina", "Argentinian": "Argentina",
    "Chilean": "Chile", "Colombian": "Colombia", "Peruvian": "Peru", "Turkish": "Turkey",
    "Türkiye": "Turkey", "Iranian": "Iran", "Israeli": "Israel", "Palestinian": "Palestine",
    "Egyptian": "Egypt", "Canadian": "Canada", "Australian": "Australia", "German": "Germany",
    "French": "France", "Italian": "Italy", "Spanish": "Spain", "Dutch": "Netherlands",
    "Swedish": "Sweden", "Danish": "Denmark", "Norwegian": "Norway", "Finnish": "Finland",
    "Polish": "Poland", "Russian": "Russia", "Czech Republic": "Czechia", "Côte d'Ivoire": "Ivory Coast",
    "UAE": "United Arab Emirates", "Ugandan": "Uganda", "Rwandan": "Rwanda",
    "Tanzanian": "Tanzania", "Zimbabwean": "Zimbabwe", "Cameroonian": "Cameroon",
    "Singaporean": "Singapore", "Taiwanese": "Taiwan", "Burma": "Myanmar",
}

# major cities -> country (only unambiguous names)
CITIES = {
    # India
    "Delhi": "India", "New Delhi": "India", "Mumbai": "India", "Bombay": "India",
    "Bangalore": "India", "Bengaluru": "India", "Chennai": "India", "Madras": "India",
    "Kolkata": "India", "Calcutta": "India", "Hyderabad": "India", "Pune": "India",
    "Ahmedabad": "India", "Surat": "India", "Jaipur": "India", "Lucknow": "India",
    "Kanpur": "India", "Nagpur": "India", "Indore": "India", "Bhopal": "India",
    "Patna": "India", "Bhubaneswar": "India", "Chandigarh": "India", "Kochi": "India",
    "Thiruvananthapuram": "India", "Varanasi": "India", "Guwahati": "India", "Ranchi": "India",
    "Raipur": "India", "Visakhapatnam": "India", "Coimbatore": "India", "Mysore": "India",
    "Mysuru": "India", "Gurgaon": "India", "Gurugram": "India", "Noida": "India",
    "Ghaziabad": "India", "Faridabad": "India", "Navi Mumbai": "India", "Thane": "India",
    "Srinagar": "India", "Amritsar": "India", "Ludhiana": "India", "Dehradun": "India",
    "Kerala": "India", "Tamil Nadu": "India", "Karnataka": "India", "Maharashtra": "India",
    "Gujarat": "India", "Rajasthan": "India", "Uttar Pradesh": "India", "Bihar": "India",
    "West Bengal": "India", "Odisha": "India", "Telangana": "India", "Andhra Pradesh": "India",
    "Punjab": "India", "Haryana": "India", "Assam": "India", "Jharkhand": "India",
    "Madhya Pradesh": "India", "Chhattisgarh": "India", "Uttarakhand": "India", "Goa": "India",
    # other South Asia
    "Dhaka": "Bangladesh", "Chittagong": "Bangladesh", "Khulna": "Bangladesh",
    "Karachi": "Pakistan", "Lahore": "Pakistan", "Islamabad": "Pakistan", "Rawalpindi": "Pakistan",
    "Peshawar": "Pakistan", "Kathmandu": "Nepal", "Colombo": "Sri Lanka", "Kabul": "Afghanistan",
    "Thimphu": "Bhutan",
    # East Asia
    "Beijing": "China", "Shanghai": "China", "Shenzhen": "China", "Guangzhou": "China",
    "Hangzhou": "China", "Wuhan": "China", "Chengdu": "China", "Chongqing": "China",
    "Nanjing": "China", "Tokyo": "Japan", "Osaka": "Japan", "Seoul": "South Korea",
    "Songdo": "South Korea", "Taipei": "Taiwan",
    # Southeast Asia
    "Jakarta": "Indonesia", "Surabaya": "Indonesia", "Bandung": "Indonesia",
    "Manila": "Philippines", "Bangkok": "Thailand", "Hanoi": "Vietnam",
    "Ho Chi Minh City": "Vietnam", "Kuala Lumpur": "Malaysia", "Yangon": "Myanmar",
    "Phnom Penh": "Cambodia",
    # Africa
    "Nairobi": "Kenya", "Mombasa": "Kenya", "Lagos": "Nigeria", "Abuja": "Nigeria",
    "Accra": "Ghana", "Kumasi": "Ghana", "Addis Ababa": "Ethiopia", "Kampala": "Uganda",
    "Kigali": "Rwanda", "Dar es Salaam": "Tanzania", "Johannesburg": "South Africa",
    "Cape Town": "South Africa", "Durban": "South Africa", "Harare": "Zimbabwe",
    "Lusaka": "Zambia", "Maputo": "Mozambique", "Luanda": "Angola", "Dakar": "Senegal",
    "Cairo": "Egypt", "Casablanca": "Morocco", "Kinshasa": "Democratic Republic of the Congo",
    "Ile-Ife": "Nigeria",
    # Latin America
    "São Paulo": "Brazil", "Sao Paulo": "Brazil", "Rio de Janeiro": "Brazil",
    "Mexico City": "Mexico", "Buenos Aires": "Argentina", "Santiago de Chile": "Chile",
    "Bogotá": "Colombia", "Bogota": "Colombia", "Medellín": "Colombia", "Medellin": "Colombia",
    "Lima": "Peru", "Quito": "Ecuador", "Montevideo": "Uruguay", "La Paz": "Bolivia",
    # Middle East
    "Istanbul": "Turkey", "Ankara": "Turkey", "Tehran": "Iran", "Beirut": "Lebanon",
    "Amman": "Jordan", "Dubai": "United Arab Emirates", "Abu Dhabi": "United Arab Emirates",
    "Doha": "Qatar", "Riyadh": "Saudi Arabia", "Tel Aviv": "Israel", "Jerusalem": "Israel",
    # Global North
    "New York": "United States", "Los Angeles": "United States", "Chicago": "United States",
    "San Francisco": "United States", "Seattle": "United States", "Boston": "United States",
    "New Orleans": "United States", "Detroit": "United States", "Philadelphia": "United States",
    "Toronto": "Canada", "Vancouver": "Canada", "Montreal": "Canada", "London": "United Kingdom",
    "Manchester": "United Kingdom", "Glasgow": "United Kingdom", "Edinburgh": "United Kingdom",
    "Milton Keynes": "United Kingdom", "Dublin": "Ireland", "Paris": "France", "Berlin": "Germany",
    "Hamburg": "Germany", "Munich": "Germany", "Amsterdam": "Netherlands",
    "Rotterdam": "Netherlands", "Brussels": "Belgium", "Barcelona": "Spain", "Madrid": "Spain",
    "Lisbon": "Portugal", "Rome": "Italy", "Milan": "Italy", "Turin": "Italy", "Vienna": "Austria",
    "Graz": "Austria", "Zurich": "Switzerland", "Copenhagen": "Denmark", "Stockholm": "Sweden",
    "Oslo": "Norway", "Helsinki": "Finland", "Reykjavík": "Iceland", "Reykjavik": "Iceland",
    "Warsaw": "Poland", "Athens": "Greece", "Zagreb": "Croatia", "Moscow": "Russia",
    "Sydney": "Australia", "Melbourne": "Australia", "Brisbane": "Australia", "Auckland": "New Zealand",
}
COUNTRIES.setdefault("Jordan", ME)  # only reached via Amman (bare "Jordan" is too ambiguous)

DELHI_NCR = [
    "Delhi", "New Delhi", "NCR", "National Capital Region", "Gurgaon", "Gurugram", "Noida",
    "Greater Noida", "Ghaziabad", "Faridabad", "Sonipat", "Sonepat", "Manesar", "Bahadurgarh",
    "Meerut", "Panipat", "Rohtak", "Palwal", "Rewari", "Jhajjar",
]
HARYANA = [
    "Haryana", "Gurgaon", "Gurugram", "Faridabad", "Sonipat", "Sonepat", "Panipat", "Rohtak",
    "Hisar", "Hissar", "Karnal", "Ambala", "Yamunanagar", "Yamuna Nagar", "Panchkula", "Bhiwani",
    "Sirsa", "Jind", "Kurukshetra", "Thanesar", "Rewari", "Palwal", "Bahadurgarh", "Manesar",
    "Kaithal", "Jhajjar", "Narnaul", "Fatehabad", "Hansi", "Charkhi Dadri", "Nuh", "Mewat",
]


def _rx(names):
    names = sorted(set(names), key=len, reverse=True)
    return re.compile(r"(?<![\w-])(" + "|".join(re.escape(n) for n in names) + r")(?![\w-])")


_PLACE_RX = _rx(list(COUNTRIES) + list(ALIASES) + list(CITIES))
_DELHI_RX = _rx(DELHI_NCR)
_HARYANA_RX = _rx(HARYANA)
# phrases where a place word does not mean the place
_FALSE = re.compile(
    r"(American|Native) Indians?|Indian Ocean|West Indi(es|an)|East India Company|"
    r"New England|New Mexico|Latin America(n)?|North America(n)?|South America(n)?|"
    r"Central America(n)?|African[- ]American|Asian[- ]American|Chinese[- ]American|"
    r"Mexican[- ]American|Korean[- ]American|British Columbia|Indian Institute|"
    r"Guinea-Bissau|Georgia"
)


# continent / world-region words -> region (they name no country, so add to regions only)
REGION_WORDS = [
    (r"\b(Europe|European|EU member states|Scandinavia\w*|Nordic|North America\w*)\b", GN),
    (r"\b(Latin America\w*|South America\w*|Central America\w*|Caribbean)\b", LA),
    (r"\b(East Asia\w*)\b", EA),
    (r"\b(Southeast Asia\w*|South-East Asia\w*)\b", SEA),
    (r"\b(South Asia\w*)\b", SA),
    (r"\b(Africa|African|sub-Saharan)\b", AF),
    (r"\b(Middle East\w*|MENA|Gulf states|Central Asia\w*)\b", ME),
]
REGION_WORDS = [(re.compile(rx), reg) for rx, reg in REGION_WORDS]
_REGION_FALSE = re.compile(r"African[- ]American|European Union law")


def places(text: str):
    """Return (sorted list of canonical places, set of regions, india, delhi_ncr, haryana)."""
    if not text:
        return [], set(), False, False, False
    clean = _FALSE.sub(" ", text)
    found = set()
    countries = set()
    for m in _PLACE_RX.finditer(clean):
        name = m.group(1)
        if name in ("NCR",):
            continue
        if name in CITIES:
            found.add(name if name not in ALIASES else ALIASES[name])
            countries.add(CITIES[name])
        else:
            c = ALIASES.get(name, name)
            if c in COUNTRIES:
                found.add(c)
                countries.add(c)
    # US/UK abbreviations are case-sensitive tokens; "America" alone is too loose → only via US forms
    regions = {COUNTRIES[c] for c in countries if c in COUNTRIES}
    rtext = _REGION_FALSE.sub(" ", text)
    for rx, reg in REGION_WORDS:
        for m in rx.finditer(rtext):
            regions.add(reg)
            found.add(m.group(1))
    india = "India" in countries
    dm = {m.group(1) for m in _DELHI_RX.finditer(text)}
    # NCR / Meerut / Panipat etc. only count when the text is about India
    delhi = bool(dm & {"Delhi", "New Delhi", "Gurgaon", "Gurugram", "Noida", "Greater Noida",
                       "Ghaziabad", "Faridabad", "Manesar"}) or (india and bool(dm))
    hm = {m.group(1) for m in _HARYANA_RX.finditer(text)}
    haryana = "Haryana" in hm or bool(hm & {"Gurgaon", "Gurugram", "Faridabad", "Manesar"}) or (
        india and bool(hm))
    if delhi or haryana:
        india = True
        regions.add(SA)
        found |= {n for n in dm | hm if n not in ("NCR", "National Capital Region")}
        found.add("India")
    return sorted(found), regions, india, delhi, haryana


def region_label(regions: set) -> str:
    if not regions:
        return "Not place-specific"
    if len(regions) == 1:
        return next(iter(regions))
    return "Multi-region"
