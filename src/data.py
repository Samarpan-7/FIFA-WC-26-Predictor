"""
FIFA World Cup 2026 – Complete Team Data
Real group draw data as per official FIFA World Cup 2026 draw.
Groups A–H: exact teams from official draw images.
Groups I–L: remaining qualified teams.
"""

# ─────────────────────────────────────────────────────────────────────────────
# REAL GROUP ASSIGNMENTS — FIFA World Cup 2026 Official Draw
# Groups A–H from official images provided
# Groups I–L: remaining 16 qualified nations
# ─────────────────────────────────────────────────────────────────────────────
WC2026_GROUPS: dict[str, list[str]] = {
    # ── From official draw images ──────────────────────────────────────────
    "Group A": ["Mexico",        "South Africa",      "South Korea",   "Czechia"],
    "Group B": ["Switzerland",   "Canada",            "Bosnia & Herz", "Qatar"],
    "Group C": ["Brazil",        "Morocco",           "Scotland",      "Haiti"],
    "Group D": ["United States", "Australia",         "Paraguay",      "Türkiye"],
    "Group E": ["Germany",       "Côte d'Ivoire",     "Ecuador",       "Curaçao"],
    "Group F": ["Netherlands",   "Japan",             "Sweden",        "Tunisia"],
    "Group G": ["Belgium",       "Egypt",             "Iran",          "New Zealand"],
    "Group H": ["Spain",         "Cabo Verde",        "Uruguay",       "Saudi Arabia"],
    # ── Groups I–L: real official draw ─────────────────────────────────────
    "Group I": ["France",        "Norway",            "Senegal",       "Iraq"],
    "Group J": ["Argentina",     "Austria",           "Algeria",       "Jordan"],
    "Group K": ["Colombia",      "Portugal",          "DR Congo",      "Uzbekistan"],
    "Group L": ["England",       "Croatia",           "Ghana",         "Panama"],
}

# ─────────────────────────────────────────────────────────────────────────────
# COMPACT RAW DATA
# Tuple: (flag, fifa_rank, elo, coach, confederation, squad_value,
#         avg_age, form_last5, strength, attack, midfield, defense)
# ─────────────────────────────────────────────────────────────────────────────
_RAW: dict[str, tuple] = {
    # ── Group A ──────────────────────────────────────────────────────────────
    "Mexico":        ("🇲🇽", 15, 1935, "Javier Aguirre",          "CONCACAF", "€220M",  27.1, "WWDWL", 82, 80, 82, 81),
    "South Africa":  ("🇿🇦", 35, 1830, "Hugo Broos",              "CAF",      "€90M",   27.5, "WDWLW", 66, 64, 66, 67),
    "South Korea":   ("🇰🇷", 20, 1910, "Hong Myung-bo",           "AFC",      "€260M",  27.0, "WWDWW", 81, 80, 81, 79),
    "Czechia":       ("🇨🇿", 29, 1855, "Ivan Hasek",              "UEFA",     "€240M",  27.1, "WDWLW", 76, 74, 77, 76),

    # ── Group B ──────────────────────────────────────────────────────────────
    "Switzerland":   ("🇨🇭", 18, 1915, "Murat Yakin",             "UEFA",     "€320M",  27.3, "WDWWL", 82, 79, 83, 83),
    "Canada":        ("🇨🇦", 45, 1804, "Jesse Marsch",            "CONCACAF", "€190M",  25.4, "WDWWL", 71, 70, 71, 70),
    "Bosnia & Herz": ("🇧🇦", 52, 1785, "Sergej Barbarez",         "UEFA",     "€130M",  27.6, "WDWLW", 63, 62, 63, 62),
    "Qatar":         ("🇶🇦", 44, 1803, "Marquez Lopez",           "AFC",      "€55M",   27.1, "WDLWL", 62, 60, 62, 63),

    # ── Group C ──────────────────────────────────────────────────────────────
    "Brazil":        ("🇧🇷",  5, 2018, "Dorival Junior",          "CONMEBOL", "€1.1B",  26.8, "WWDWW", 93, 93, 92, 87),
    "Morocco":       ("🇲🇦", 13, 1950, "Walid Regragui",          "CAF",      "€340M",  26.7, "WWWWL", 85, 83, 84, 87),
    "Scotland":      ("🏴󠁧󠁢󠁳󠁣󠁴󠁿", 38, 1816, "Steve Clarke",            "UEFA",     "€200M",  27.2, "WWDLW", 72, 71, 73, 72),
    "Haiti":         ("🇭🇹", 72, 1692, "Jean-Jacques Pierre",     "CONCACAF", "€25M",   26.4, "WDLLL", 48, 47, 48, 49),

    # ── Group D ──────────────────────────────────────────────────────────────
    "United States": ("🇺🇸", 14, 1942, "Mauricio Pochettino",     "CONCACAF", "€380M",  25.6, "WWWDW", 83, 82, 81, 82),
    "Australia":     ("🇦🇺", 27, 1866, "Tony Popovic",            "AFC",      "€140M",  26.8, "WDWWL", 75, 73, 75, 75),
    "Paraguay":      ("🇵🇾", 33, 1840, "Gustavo Alfaro",          "CONMEBOL", "€140M",  27.3, "WDLWW", 70, 69, 70, 70),
    "Türkiye":       ("🇹🇷", 28, 1862, "Vincenzo Montella",       "UEFA",     "€280M",  27.4, "DWWLW", 78, 77, 78, 77),

    # ── Group E ──────────────────────────────────────────────────────────────
    "Germany":       ("🇩🇪",  8, 1963, "Julian Nagelsmann",       "UEFA",     "€820M",  26.5, "WWWWL", 90, 88, 90, 89),
    "Côte d'Ivoire": ("🇨🇮", 39, 1815, "Emerse Fae",              "CAF",      "€180M",  26.3, "WWDWL", 69, 69, 68, 67),
    "Ecuador":       ("🇪🇨", 22, 1895, "Sebastian Beccacece",     "CONMEBOL", "€180M",  25.8, "WDWWL", 78, 76, 77, 79),
    "Curaçao":       ("🇨🇼", 85, 1648, "Patrick Kluivert",        "CONCACAF", "€30M",   26.1, "WDLLW", 44, 43, 44, 45),

    # ── Group F ──────────────────────────────────────────────────────────────
    "Netherlands":   ("🇳🇱",  7, 1998, "Ronald Koeman",           "UEFA",     "€780M",  26.4, "WWDWL", 89, 87, 89, 88),
    "Japan":         ("🇯🇵", 19, 1914, "Hajime Moriyasu",         "AFC",      "€310M",  26.3, "WWWWL", 82, 80, 82, 82),
    "Sweden":        ("🇸🇪", 36, 1825, "Jon Dahl Tomasson",       "UEFA",     "€210M",  27.0, "LWWDW", 73, 71, 73, 74),
    "Tunisia":       ("🇹🇳", 34, 1838, "Jalel Kadri",             "CAF",      "€70M",   27.4, "WDWLL", 60, 59, 60, 62),

    # ── Group G ──────────────────────────────────────────────────────────────
    "Belgium":       ("🇧🇪",  9, 1980, "Domenico Tedesco",        "UEFA",     "€680M",  27.9, "WDWWW", 88, 86, 87, 86),
    "Egypt":         ("🇪🇬", 37, 1820, "Hossam Hassan",           "CAF",      "€140M",  26.4, "DWWWL", 71, 70, 71, 72),
    "Iran":          ("🇮🇷", 41, 1811, "Amir Ghalenoei",          "AFC",      "€80M",   27.6, "WDLWW", 66, 64, 66, 67),
    "New Zealand":   ("🇳🇿", 48, 1785, "Darren Bazeley",          "OFC",      "€40M",   26.6, "WDWDW", 60, 58, 60, 62),

    # ── Group H ──────────────────────────────────────────────────────────────
    "Spain":         ("🇪🇸",  3, 2042, "Luis de la Fuente",       "UEFA",     "€1.0B",  25.9, "WWWWW", 93, 91, 95, 88),
    "Cabo Verde":    ("🇨🇻", 65, 1728, "Bubista",                 "CAF",      "€45M",   27.3, "WDWDL", 52, 51, 52, 53),
    "Uruguay":       ("🇺🇾", 12, 1958, "Marcelo Bielsa",          "CONMEBOL", "€420M",  26.9, "WWWDW", 86, 85, 84, 85),
    "Saudi Arabia":  ("🇸🇦", 38, 1820, "Roberto Mancini",         "AFC",      "€80M",   27.3, "WLWDW", 67, 65, 67, 68),

    # ── Group I ──────────────────────────────────────────────────────────────
    "France":        ("🇫🇷",  2, 2058, "Didier Deschamps",        "UEFA",     "€1.3B",  27.1, "WWWDW", 94, 92, 93, 91),
    "Norway":        ("🇳🇴", 18, 1916, "Stale Solbakken",         "UEFA",     "€480M",  26.5, "WWWDW", 84, 86, 82, 81),
    "Senegal":       ("🇸🇳", 21, 1900, "Aliou Cisse",             "CAF",      "€260M",  26.5, "WWDWW", 81, 80, 80, 81),
    "Iraq":          ("🇮🇶", 63, 1732, "Jesus Casas",             "AFC",      "€40M",   27.2, "WDWLL", 50, 49, 50, 52),

    # ── Group J ──────────────────────────────────────────────────────────────
    "Argentina":     ("🇦🇷",  1, 2082, "Lionel Scaloni",          "CONMEBOL", "€950M",  27.4, "WWWWW", 95, 94, 91, 88),
    "Austria":       ("🇦🇹", 24, 1885, "Ralf Rangnick",           "UEFA",     "€360M",  26.8, "WWWDL", 80, 79, 81, 78),
    "Algeria":       ("🇩🇿", 31, 1847, "Vladimir Petkovic",       "CAF",      "€130M",  27.2, "WDWWL", 71, 70, 71, 72),
    "Jordan":        ("🇯🇴", 67, 1722, "Hussein Ammouta",         "AFC",      "€30M",   27.5, "WDWLL", 49, 48, 49, 51),

    # ── Group K ──────────────────────────────────────────────────────────────
    "Colombia":      ("🇨🇴", 16, 1930, "Nestor Lorenzo",          "CONMEBOL", "€380M",  26.3, "WWWWL", 84, 84, 82, 81),
    "Portugal":      ("🇵🇹",  6, 2010, "Roberto Martinez",        "UEFA",     "€850M",  27.8, "WWWLW", 90, 92, 87, 85),
    "DR Congo":      ("🇨🇩", 50, 1778, "Sebastien Desabre",       "CAF",      "€85M",   26.7, "WDWLW", 58, 57, 58, 58),
    "Uzbekistan":    ("🇺🇿", 69, 1718, "Srecko Katanec",          "AFC",      "€35M",   26.3, "WDLWL", 47, 46, 47, 48),

    # ── Group L ──────────────────────────────────────────────────────────────
    "England":       ("🏴󠁧󠁢󠁥󠁮󠁧󠁿",  4, 2017, "Gareth Southgate",        "UEFA",     "€1.1B",  26.2, "WWDWW", 91, 90, 88, 90),
    "Croatia":       ("🇭🇷", 11, 1961, "Zlatko Dalic",            "UEFA",     "€380M",  28.2, "WDWWL", 86, 83, 88, 84),
    "Ghana":         ("🇬🇭", 40, 1812, "Otto Addo",               "CAF",      "€120M",  26.8, "LWWDW", 68, 67, 68, 67),
    "Panama":        ("🇵🇦", 46, 1798, "Thomas Christiansen",     "CONCACAF", "€55M",   27.8, "LWWDW", 63, 61, 63, 65),

}

# ─────────────────────────────────────────────────────────────────────────────
# Build TEAM_DATA from compact raw tuples
# ─────────────────────────────────────────────────────────────────────────────
TEAM_DATA: dict[str, dict] = {}
for _name, _r in _RAW.items():
    TEAM_DATA[_name] = {
        "flag":          _r[0],
        "fifa_rank":     _r[1],
        "elo":           _r[2],
        "coach":         _r[3],
        "confederation": _r[4],
        "squad_value":   _r[5],
        "avg_age":       _r[6],
        "form":          _r[7],
        "strength":      _r[8],
        "attack":        _r[9],
        "midfield":      _r[10],
        "defense":       _r[11],
    }

_DEFAULT: dict = {
    "flag": "🏳️", "fifa_rank": 99, "elo": 1700, "coach": "Unknown",
    "confederation": "Unknown", "squad_value": "€50M", "avg_age": 27.0,
    "form": "WDLWL", "strength": 60, "attack": 60, "midfield": 60, "defense": 60,
}

# ─────────────────────────────────────────────────────────────────────────────
# ISO 3166-1 alpha-2 country codes → flagcdn.com rectangular images
# flagcdn.com/w40/{code}.png  (40 px wide, proportional height ≈ 27 px)
# Subdivision codes for England (gb-eng) and Scotland (gb-sct)
# ─────────────────────────────────────────────────────────────────────────────
FLAG_ISO: dict[str, str] = {
    # Group A
    "Mexico":        "mx",
    "South Africa":  "za",
    "South Korea":   "kr",
    "Czechia":       "cz",
    # Group B
    "Switzerland":   "ch",
    "Canada":        "ca",
    "Bosnia & Herz": "ba",
    "Qatar":         "qa",
    # Group C
    "Brazil":        "br",
    "Morocco":       "ma",
    "Scotland":      "gb-sct",
    "Haiti":         "ht",
    # Group D
    "United States": "us",
    "Australia":     "au",
    "Paraguay":      "py",
    "Türkiye":       "tr",
    # Group E
    "Germany":       "de",
    "Côte d'Ivoire": "ci",
    "Ecuador":       "ec",
    "Curaçao":       "cw",
    # Group F
    "Netherlands":   "nl",
    "Japan":         "jp",
    "Sweden":        "se",
    "Tunisia":       "tn",
    # Group G
    "Belgium":       "be",
    "Egypt":         "eg",
    "Iran":          "ir",
    "New Zealand":   "nz",
    # Group H
    "Spain":         "es",
    "Cabo Verde":    "cv",
    "Uruguay":       "uy",
    "Saudi Arabia":  "sa",
    # Group I
    "France":        "fr",
    "Norway":        "no",
    "Senegal":       "sn",
    "Iraq":          "iq",
    # Group J
    "Argentina":     "ar",
    "Austria":       "at",
    "Algeria":       "dz",
    "Jordan":        "jo",
    # Group K
    "Colombia":      "co",
    "Portugal":      "pt",
    "DR Congo":      "cd",
    "Uzbekistan":    "uz",
    # Group L
    "England":       "gb-eng",
    "Croatia":       "hr",
    "Ghana":         "gh",
    "Panama":        "pa",
}

_CDN = "https://flagcdn.com/w40/{code}.png"


def flag_img(team: str, width: int = 36, height: int = 24) -> str:
    """Return an <img> tag for the team's rectangular flag from flagcdn.com."""
    code = FLAG_ISO.get(team, "")
    if not code:
        return ""
    url = _CDN.format(code=code)
    return (
        f'<img src="{url}" '
        f'style="width:{width}px;height:{height}px;object-fit:cover;'
        f'border:1px solid #d1d5db;border-radius:3px;'
        f'vertical-align:middle;display:inline-block;" '
        f'alt="{team}">'
    )


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def get_all_teams() -> list[str]:
    """Return flat list of all 48 WC 2026 participants in group order."""
    return [team for group in WC2026_GROUPS.values() for team in group]


def get_team_info(name: str) -> dict:
    """Return team metadata dict. Falls back to defaults for unknown teams."""
    return TEAM_DATA.get(name, {**_DEFAULT})


def get_groups() -> dict[str, list[str]]:
    """Return a copy of the group-assignment mapping."""
    return dict(WC2026_GROUPS)


def get_team_group(name: str) -> str:
    """Return which group a team belongs to, e.g. 'Group A'. Returns 'Unknown' if not found."""
    for grp, teams in WC2026_GROUPS.items():
        if name in teams:
            return grp
    return "Unknown"
