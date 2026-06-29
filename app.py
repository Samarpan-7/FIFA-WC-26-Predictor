"""
FIFA Oracle 2026 — Main Streamlit Application
==============================================
Run with:  streamlit run app.py
Requires:  python src/train.py  (once, to generate models/match_model.pkl)
"""

import time
import streamlit as st
import pandas as pd

from src.data import WC2026_GROUPS, get_team_info, get_all_teams, flag_img
from src.bracket import (
    simulate_group_stage,
    get_qualified_32,
    simulate_knockout_round,
    simulate_match_detail,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FIFA WC'26 Predictor",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — Light/White Theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── FONTS & BASE ──────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Georgia', 'Times New Roman', Times, serif;
    letter-spacing: 0.01em;
}

/* ── APP BACKGROUND — WHITE ────────────────────── */
.stApp {
    background: #f8fafc !important;
    min-height: 100vh;
}
.block-container { padding: 1.5rem 2rem 4rem !important; max-width: 1400px; }

/* Force all text to dark */
.stApp, .stApp p, .stApp span, .stApp div,
.stApp label, .stApp li, .stApp h1, .stApp h2,
.stApp h3, .stApp h4, .stApp h5, .stApp h6 {
    color: #0f172a !important;
}

/* ── SIDEBAR — LIGHT GREY ───────────────────────── */
[data-testid="stSidebar"] {
    background: #f1f5f9 !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] * { color: #1e293b !important; }
[data-testid="stSidebar"] .stButton > button {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    color: #334155 !important;
    border-radius: 10px !important;
    width: 100% !important;
    text-align: left !important;
    padding: 0.55rem 1rem !important;
    margin-bottom: 4px !important;
    transition: all 0.2s ease !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #0057b8 !important;
    background: #eff6ff !important;
    color: #0057b8 !important;
}

/* ── GLOBAL BUTTONS ────────────────────────────── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    color: #1e293b !important;
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
}
.stButton > button[kind="primary"] {
    background: #0057b8 !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 2px 6px rgba(0,87,184,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #003f8a !important;
    box-shadow: 0 3px 10px rgba(0,87,184,0.4) !important;
}

/* ── HERO ──────────────────────────────────────── */
.hero-wrap {
    background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 50%, #2563eb 100%);
    border: none;
    border-radius: 22px;
    padding: 3rem 2rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(29,78,216,0.25);
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.4);
    color: #ffffff;
    font-size: 0.7rem; font-weight: 700;
    padding: 4px 14px; border-radius: 20px;
    letter-spacing: 2.5px; text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 900; line-height: 1.05;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    margin: 0 0 0.4rem;
}
.hero-sub  { font-size: 1.05rem; color: rgba(255,255,255,0.85) !important; font-weight: 400; margin: 0; }
.hero-host { font-size: 0.82rem; color: rgba(255,255,255,0.65) !important; margin-top: 0.6rem; }

/* ── STAT STRIP ────────────────────────────────── */
.stat-strip { display: flex; gap: 1rem; margin: 1.6rem 0; flex-wrap: wrap; }
.stat-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 0.9rem 1.4rem;
    flex: 1; min-width: 110px; text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.stat-box .sv { font-size: 1.7rem; font-weight: 800; color: #1d4ed8 !important; line-height: 1; }
.stat-box .sl { font-size: 0.68rem; color: #64748b !important; text-transform: uppercase;
                letter-spacing: 1px; margin-top: 3px; }

/* ── NAV CARDS ─────────────────────────────────── */
.nav-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px; padding: 2.2rem 1.5rem;
    text-align: center; cursor: pointer;
    transition: all 0.3s ease;
    min-height: 190px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.nav-card:hover {
    border-color: #2563eb;
    box-shadow: 0 8px 28px rgba(37,99,235,0.15);
    transform: translateY(-4px);
}
.nc-icon  { font-size: 3.2rem; margin-bottom: 0.8rem; }
.nc-title { font-size: 1.25rem; font-weight: 800; color: #0f172a !important; margin: 0; }
.nc-desc  { font-size: 0.82rem; color: #64748b !important; margin-top: 0.4rem; line-height: 1.5; }

/* ── DIVIDER ───────────────────────────────────── */
.hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.8rem 0; }

/* ── GROUP TABLE ───────────────────────────────── */
.grp-label {
    font-size: 0.95rem; font-weight: 700; color: #1d4ed8 !important;
    border-left: 3px solid #2563eb; padding-left: 0.6rem;
    margin-bottom: 0.5rem; display: block;
}
.qual-pill {
    display: inline-flex; align-items: center; gap: 5px;
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 20px; padding: 4px 10px;
    margin: 3px; font-size: 0.74rem; color: #166534 !important; font-weight: 600;
}

/* ── TEAM SELECTION CARDS ───────────────────────── */
.tcard {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 0.7rem 0.3rem 0.55rem;
    text-align: center; min-height: 95px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.tcard:hover { border-color: #2563eb; transform: translateY(-2px);
               box-shadow: 0 4px 12px rgba(37,99,235,0.12); }
.tcard.sel {
    border: 2px solid #2563eb !important;
    background: #eff6ff !important;
    box-shadow: 0 0 18px rgba(37,99,235,0.18) !important;
}

/* ── MATCH CARDS ───────────────────────────────── */
.mc {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 13px 15px 9px;
    margin-bottom: 10px; transition: border-color 0.2s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.mc.fav-mc {
    border: 2px solid #2563eb !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.15) !important;
}
.mc-row { display: flex; align-items: center; justify-content: space-between; gap: 6px; }
.mc-team {
    display: flex; flex-direction: column; align-items: center;
    flex: 1; padding: 5px 3px; border-radius: 8px; min-width: 0;
}
.mc-team.won  { background: #f0fdf4; }
.mc-team.lost { opacity: 0.45; }
.mc-team.fav .mn { color: #1d4ed8 !important; font-weight: 800 !important; }
.mfl { font-size: 1.45rem; line-height: 1; }
.mn  { font-size: 0.72rem; font-weight: 700; color: #1e293b !important; margin-top: 3px;
       text-align: center; word-break: break-word; max-width: 80px; }
.mp  { font-size: 0.62rem; color: #64748b !important; margin-top: 2px; font-weight: 600; }
.sc-box { display: flex; flex-direction: column; align-items: center; padding: 0 10px; flex-shrink: 0; }
.scv { font-size: 1.25rem; font-weight: 900; color: #0f172a !important; letter-spacing: 4px; }
.sct { font-size: 0.52rem; color: #94a3b8 !important; text-transform: uppercase; letter-spacing: 1px; }
.mc-foot {
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 7px; padding-top: 5px;
    border-top: 1px solid #f1f5f9;
    flex-wrap: wrap; gap: 4px;
}
.wb  { font-size: 0.68rem; color: #16a34a !important; font-weight: 700; }
.cb  { font-size: 0.62rem; color: #334155 !important;
       background: #f1f5f9; padding: 3px 8px; border-radius: 5px; font-weight: 600; }
.xgb { font-size: 0.6rem; color: #64748b !important; font-weight: 500; }
.fact-row { margin-top: 6px; display: flex; flex-wrap: wrap; gap: 4px; }
.fact { font-size: 0.6rem; color: #1d4ed8 !important;
        background: #eff6ff; padding: 3px 7px; border-radius: 4px;
        font-weight: 600; border: 1px solid #bfdbfe; }

/* ── ROUND HEADER ──────────────────────────────── */
.rh {
    font-size: 1.08rem; font-weight: 800; color: #0f172a !important;
    background: linear-gradient(90deg, #eff6ff 0%, #f8fafc 100%);
    border-left: 4px solid #2563eb; padding: 0.6rem 1rem;
    border-radius: 4px; margin: 1.6rem 0 0.8rem; letter-spacing: 0.3px;
    border: 1px solid #e2e8f0; border-left: 4px solid #2563eb;
}

/* ── CHAMPION ──────────────────────────────────── */
.champ-card {
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    border: 2px solid #f59e0b; border-radius: 22px;
    padding: 2.5rem 2rem; text-align: center;
    box-shadow: 0 8px 32px rgba(245,158,11,0.2); margin: 0.8rem 0;
}
.ct  { font-size: 5rem; margin-bottom: 0.3rem; line-height: 1; }
.cl  { font-size: 0.82rem; font-weight: 700; color: #92400e !important;
       text-transform: uppercase; letter-spacing: 3px; }
.cf  { font-size: 4rem; line-height: 1; margin: 0.3rem 0; }
.cn  { font-size: 2.2rem; font-weight: 900; color: #0f172a !important; margin: 0.2rem 0; }
.cs  { font-size: 0.78rem; color: #78716c !important; margin-top: 0.3rem; }

/* ── FAV PATH (WHITE CARD) ──────────────────────── */
.path-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.4rem 1.6rem 1rem;
    margin-top: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}
.path-card-title {
    font-size: 1.05rem; font-weight: 800;
    color: #0f172a !important; margin-bottom: 0.9rem;
    border-bottom: 2px solid #e2e8f0; padding-bottom: 0.55rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.path-table { width: 100%; border-collapse: collapse; }
.path-table th {
    font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: #64748b;
    padding: 0 0.5rem 0.5rem; text-align: left;
    border-bottom: 1px solid #e2e8f0;
}
.path-table td {
    font-size: 0.82rem; color: #1e293b;
    padding: 0.55rem 0.5rem; border-bottom: 1px solid #f1f5f9;
    font-weight: 500; vertical-align: middle;
}
.path-table tr:last-child td { border-bottom: none; }
.path-table tr:hover td { background: #f8fafc; }
.pt-stage { font-size: 0.72rem; font-weight: 700; color: #475569;
            background: #f1f5f9; padding: 3px 8px; border-radius: 4px;
            white-space: nowrap; }
.pt-opp   { color: #1e293b; font-weight: 600; }
.pt-score { font-size: 0.82rem; font-weight: 800; color: #0f172a;
            background: #f1f5f9; padding: 2px 8px; border-radius: 5px;
            font-family: monospace; }
.pt-prob  { font-size: 0.76rem; color: #475569; font-weight: 600; }
.pt-ok  { font-size: 0.78rem; color: #16a34a; font-weight: 800; }
.pt-out { font-size: 0.78rem; color: #dc2626; font-weight: 800; }

/* ── SIDEBAR ACTIVE ────────────────────────────── */
.nav-active > button {
    background: rgba(0,212,255,0.1) !important;
    border-color: rgba(0,212,255,0.45) !important;
    color: #00d4ff !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    "page":           "home",
    "group_results":  None,   # {grp_name: (sorted_table, matches)}
    "qualified_32":   None,   # list[str] – 32 team names
    "favourite":      None,   # str – selected team
    "bracket":        None,   # full bracket dict
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


def _go(page: str) -> None:
    """Navigate to a page and rerun."""
    st.session_state.page = page
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1.2rem 0 0.6rem;">
        <div style="font-size:1rem; font-weight:700; color:#1d4ed8; letter-spacing:1px;">
            FIFA WC'26 PREDICTOR
        </div>
        <div style="font-size:0.58rem; color:#64748b; letter-spacing:3px; margin-top:3px; font-weight:400;">
            WORLD CUP 2026
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    _cur = st.session_state.page
    _nav = [
        ("Home",         "home"),
        ("Group Stage",  "group_stage"),
        ("Round of 32", "round_of_32"),
        ("About",        "about"),
    ]
    for _label, _key in _nav:
        _col = st.container()
        with _col:
            if st.button(_label, key=f"snav_{_key}",
                         use_container_width=True):
                _go(_key)

    st.divider()

    # Status panel
    if st.session_state.qualified_32:
        st.markdown("""
        <div style="text-align:center; font-size:0.73rem; background:#f0fdf4;
             border:1px solid #86efac; border-radius:8px; padding:0.6rem;">
            <span style="color:#16a34a; font-weight:700;">Group Stage Complete</span><br>
            <span style="color:#475569;">32 teams qualified</span>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.bracket and "Champion" in st.session_state.bracket:
        _ch = st.session_state.bracket["Champion"]
        st.html(f"""
        <div style="text-align:center; margin-top:0.7rem; padding:0.7rem 0.5rem;
             background:#fffbeb; border:1px solid #f59e0b;
             border-radius:9px;">
            <div style="font-size:0.6rem; color:#92400e; font-weight:700;
                 letter-spacing:2px; text-transform:uppercase;">
                Predicted Champion
            </div>
            <div style="margin-top:6px;">{flag_img(_ch, 48, 32)}</div>
            <div style="font-size:0.88rem; margin-top:5px; color:#0f172a; font-weight:700;">
                {_ch}
            </div>
        </div>
        """)

        if st.session_state.favourite:
            _fav = st.session_state.favourite
            st.html(f"""
            <div style="text-align:center; margin-top:0.5rem; font-size:0.68rem; color:#475569;
                 display:flex; align-items:center; justify-content:center; gap:6px;">
                {flag_img(_fav, 24, 16)}
                <span style="color:#1d4ed8; font-weight:700;">{_fav}</span>
            </div>
            """)


# ─────────────────────────────────────────────────────────────────────────────
# SHARED HTML BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

def _match_card_html(result: dict, favourite: str = "") -> str:
    """Render one match as HTML card string."""
    t1, t2   = result["team1"], result["team2"]
    winner   = result["winner"]
    score    = result["score"]
    i1, i2   = get_team_info(t1), get_team_info(t2)

    # Side classes
    if winner == "Draw":
        s1, s2 = "", ""
    else:
        s1 = "won" if winner == t1 else "lost"
        s2 = "won" if winner == t2 else "lost"

    f1 = "fav" if t1 == favourite else ""
    f2 = "fav" if t2 == favourite else ""
    card_fav = "fav-mc" if favourite in (t1, t2) else ""

    facts_html = "".join(
        f'<span class="fact">{f}</span>' for f in result["factors"]
    )

    conf_colour = {"High": "#16a34a", "Medium": "#d97706", "Low": "#dc2626"}.get(
        result["confidence"], "#94a3b8"
    )
    winner_text = (
        f"{winner} advances"
        if winner not in ("Draw", "Unknown", "")
        else "Draw"
    )

    fl1 = flag_img(t1, 36, 24)
    fl2 = flag_img(t2, 36, 24)

    return f"""
<div class="mc {card_fav}">
  <div class="mc-row">
    <div class="mc-team {s1} {f1}">
      <div class="mfl">{fl1}</div>
      <span class="mn">{t1}</span>
      <span class="mp">{result['prob_t1']}%</span>
    </div>
    <div class="sc-box">
      <span class="scv">{score}</span>
      <span class="sct">FT</span>
    </div>
    <div class="mc-team {s2} {f2}">
      <div class="mfl">{fl2}</div>
      <span class="mn">{t2}</span>
      <span class="mp">{result['prob_t2']}%</span>
    </div>
  </div>
  <div class="mc-foot">
    <span class="wb">{winner_text}</span>
    <span class="cb" style="color:{conf_colour};">Conf: {result['confidence']}</span>
    <span class="xgb">xG {result['xg1']} – {result['xg2']}</span>
  </div>
  <div class="fact-row">{facts_html}</div>
</div>
"""


def _render_round(matches: list[dict], round_name: str, favourite: str) -> None:
    """Display one bracket round (split into 2 columns for long rounds)."""
    rh_style = ("font-size:1.08rem;font-weight:800;color:#0f172a;"
                "background:linear-gradient(90deg,#eff6ff 0%,#f8fafc 100%);"
                "border-left:4px solid #2563eb;padding:0.6rem 1rem;"
                "border-radius:4px;margin:1.2rem 0 0.6rem;"
                "border:1px solid #e2e8f0;font-family:Georgia,serif;")
    st.html(f'<div style="{rh_style}">{round_name}</div>')

    if len(matches) == 1:
        _, mid_col, _ = st.columns([1, 2, 1])
        with mid_col:
            st.html(_match_card_html(matches[0], favourite))
    else:
        half = max(1, (len(matches) + 1) // 2)
        col_l, col_r = st.columns(2)
        with col_l:
            for m in matches[:half]:
                st.html(_match_card_html(m, favourite))
        with col_r:
            for m in matches[half:]:
                st.html(_match_card_html(m, favourite))


def _render_champion(champion: str) -> None:
    """Display the golden champion trophy card."""
    inf = get_team_info(champion)
    st.html(f"""
    <div style="background:linear-gradient(135deg,#fffbeb 0%,#fef3c7 100%);
         border:2px solid #f59e0b; border-radius:16px;
         padding:2rem 1.5rem; text-align:center;
         box-shadow:0 6px 24px rgba(245,158,11,0.2); margin:0.8rem 0;
         font-family:Georgia,serif;">
        <div style="font-size:0.7rem; font-weight:700; color:#92400e;
             text-transform:uppercase; letter-spacing:3px; margin-bottom:0.5rem;">
            FIFA World Cup 2026 &mdash; Predicted Champion
        </div>
        <div style="font-size:4rem; line-height:1; margin:0.4rem 0;">{inf['flag']}</div>
        <div style="font-size:1.8rem; font-weight:900; color:#0f172a; margin:0.3rem 0;">{champion}</div>
        <div style="font-size:0.72rem; color:#78716c; margin-top:0.4rem;">
            AI Predicted &nbsp;&middot;&nbsp; FIFA WC'26 Predictor &nbsp;&middot;&nbsp; XGBoost ML
        </div>
    </div>
    """)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — HOME
# ─────────────────────────────────────────────────────────────────────────────
def page_home() -> None:
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-badge">AI Powered Predictions</div>
        <h1 class="hero-title">FIFA WC'26 PREDICTOR</h1>
        <p class="hero-sub">Machine Learning Powered FIFA World Cup 2026 Prediction Platform</p>
        <p class="hero-host">🇺🇸 United States &nbsp;&middot;&nbsp; 🇨🇦 Canada &nbsp;&middot;&nbsp; 🇲🇽 Mexico &nbsp;&middot;&nbsp; June &ndash; July 2026</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-strip">
        <div class="stat-box"><div class="sv">48</div><div class="sl">Nations</div></div>
        <div class="stat-box"><div class="sv">12</div><div class="sl">Groups</div></div>
        <div class="stat-box"><div class="sv">32</div><div class="sl">Knockout Teams</div></div>
        <div class="stat-box"><div class="sv">104</div><div class="sl">Total Matches</div></div>
        <div class="stat-box"><div class="sv">XGBoost</div><div class="sl">ML Model</div></div>
        <div class="stat-box"><div class="sv">150+</div><div class="sl">Years of Data</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="hr">', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="nav-card">
            <div class="nc-title">Group Stage</div>
            <div class="nc-desc">Simulate all 12 groups &middot; Full table standings<br>
            Qualify 32 teams for the knockout stage</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Group Stage", key="h_gs",
                     use_container_width=True, type="primary"):
            _go("group_stage")

    with col2:
        st.markdown("""
        <div class="nav-card">
            <div class="nc-title">Round of 32</div>
            <div class="nc-desc">Choose your tournament favorite &middot; AI Bracket Generator<br>
            Follow the path to the championship</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Round of 32", key="h_r32",
                     use_container_width=True, type="primary"):
            _go("round_of_32")

    st.markdown('<hr class="hr">', unsafe_allow_html=True)
    st.markdown("""<div style="text-align:center; padding:0.5rem 0 1rem;">
        <p style="color:#475569; font-size:0.82rem; max-width:640px; margin:0 auto; line-height:1.7;">
            FIFA WC'26 Predictor uses an <strong style="color:#1d4ed8;">XGBoost classifier</strong> trained on over
            150 years of international football results. Winners are decided by the highest-probability
            class from the model &mdash; outcomes are <em>performance-driven</em>, not random.
        </p></div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — GROUP STAGE
# ─────────────────────────────────────────────────────────────────────────────
def page_group_stage() -> None:
    st.markdown("""
    <h2 style="font-size:1.75rem; font-weight:800; color:#0f172a; margin-bottom:0.15rem;">
        Group Stage
    </h2>
    <p style="color:#64748b; margin-bottom:1.4rem;">
        FIFA World Cup 2026 &nbsp;&middot;&nbsp; 12 Groups &nbsp;&middot;&nbsp; 48 Nations
    </p>
    """, unsafe_allow_html=True)

    run_col, info_col = st.columns([1, 3])
    with run_col:
        run_btn = st.button("Simulate All Groups",
                            type="primary", use_container_width=True)
    with info_col:
        if st.session_state.group_results:
            st.success("Group stage simulated — 32 teams qualified for Round of 32.")
        else:
            st.info("Press the button to simulate all 12 groups using the ML model.")

    if run_btn:
        with st.status("Simulating Group Stage...", expanded=True) as status:
            results: dict = {}
            for grp_name, teams in WC2026_GROUPS.items():
                st.write(f"Calculating {grp_name}...")
                table, matches = simulate_group_stage(teams)
                results[grp_name] = (table, matches)
            qualified = get_qualified_32(results)
            st.session_state.group_results = results
            st.session_state.qualified_32  = qualified
            st.session_state.bracket       = None
            status.update(label="Group Stage complete.", state="complete")
        st.rerun()

    if st.session_state.group_results:
        _show_all_groups(st.session_state.group_results)

        st.markdown('<hr class="hr">', unsafe_allow_html=True)
        st.markdown("""
        <h3 style="font-size:1.05rem; font-weight:700; color:#16a34a; margin-bottom:0.7rem;">
            32 Qualified Teams
        </h3>
        """, unsafe_allow_html=True)

        pills_html = "".join(
            f'<span class="qual-pill">{get_team_info(t)["flag"]} {t}</span>'
            for t in (st.session_state.qualified_32 or [])
        )
        st.markdown(f'<div style="line-height:2.6;">{pills_html}</div>',
                    unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Proceed to Round of 32", type="primary"):
            _go("round_of_32")


def _show_all_groups(group_results: dict) -> None:
    """Render all 12 groups as HTML tables with flag icons next to each team."""
    groups = list(group_results.items())
    for row_start in range(0, len(groups), 3):
        chunk = groups[row_start:row_start + 3]
        cols  = st.columns(len(chunk))
        for col, (grp_name, (table, matches)) in zip(cols, chunk):
            with col:
                # Build HTML table rows
                rows_html = ""
                for rank, (team, stats) in enumerate(table, 1):
                    fi = flag_img(team, 34, 22)
                    # Highlight top-2 qualifiers with green left border
                    row_style = (
                        'background:#f0fdf4; border-left:3px solid #16a34a;'
                        if rank <= 2 else
                        'background:#fff; border-left:3px solid transparent;'
                    )
                    qual_badge = (' <span style="font-size:0.55rem;color:#16a34a;font-weight:700;">Q</span>'
                                  if rank <= 2 else '')
                    rows_html += f"""
                    <tr style="{row_style}">
                        <td style="padding:5px 6px; font-size:0.78rem; white-space:nowrap;">
                            <span style="display:inline-block; vertical-align:middle; margin-right:6px;">{fi}</span>
                            <strong style="font-size:0.78rem; vertical-align:middle;">{team}</strong>{qual_badge}
                        </td>
                        <td style="text-align:center; padding:5px 4px; font-size:0.75rem; font-weight:700; color:#0057b8;">{stats['Pts']}</td>
                        <td style="text-align:center; padding:5px 4px; font-size:0.72rem; color:#475569;">{stats['W']}</td>
                        <td style="text-align:center; padding:5px 4px; font-size:0.72rem; color:#475569;">{stats['D']}</td>
                        <td style="text-align:center; padding:5px 4px; font-size:0.72rem; color:#475569;">{stats['L']}</td>
                        <td style="text-align:center; padding:5px 4px; font-size:0.72rem; color:#475569;">{stats['GD']:+d}</td>
                    </tr>
                    """

                grp_table_html = f"""
                <div style="margin-bottom:0.5rem;">
                    <div style="font-size:0.72rem; font-weight:700; color:#1d4ed8; letter-spacing:1px;
                                border-bottom:2px solid #1d4ed8; padding-bottom:3px; margin-bottom:4px;">
                        {grp_name}
                    </div>
                    <table style="width:100%; border-collapse:collapse; font-family:Georgia,serif;">
                        <thead>
                            <tr style="background:#f1f5f9;">
                                <th style="text-align:left; padding:4px 6px; font-size:0.65rem; color:#64748b; font-weight:600;">TEAM</th>
                                <th style="text-align:center; padding:4px 4px; font-size:0.65rem; color:#0057b8; font-weight:700;">PTS</th>
                                <th style="text-align:center; padding:4px 4px; font-size:0.65rem; color:#64748b;">W</th>
                                <th style="text-align:center; padding:4px 4px; font-size:0.65rem; color:#64748b;">D</th>
                                <th style="text-align:center; padding:4px 4px; font-size:0.65rem; color:#64748b;">L</th>
                                <th style="text-align:center; padding:4px 4px; font-size:0.65rem; color:#64748b;">GD</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>
                """
                st.html(grp_table_html)

                with st.expander(f"Match Results ({len(matches)} games)"):
                    for m in matches:
                        i1 = get_team_info(m["team1"])
                        i2 = get_team_info(m["team2"])
                        w1 = "font-weight:900;" if m["winner"] == m["team1"] else ""
                        w2 = "font-weight:900;" if m["winner"] == m["team2"] else ""
                        f1_img = flag_img(m["team1"], 26, 17)
                        f2_img = flag_img(m["team2"], 26, 17)
                        _div_s = "padding:4px 0;font-size:0.82rem;font-family:Georgia,serif;display:flex;align-items:center;gap:6px;"
                        st.html(
                            f'<div style="{_div_s}">'
                            f'{f1_img} '
                            f'<span style="{w1}">{m["team1"]}</span>'
                            f' <span style="font-weight:700;color:#0057b8;margin:0 6px;">{m["score"]}</span> '
                            f'<span style="{w2}">{m["team2"]}</span> '
                            f'{f2_img}'
                            f'</div>'
                        )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — ROUND OF 32
# ─────────────────────────────────────────────────────────────────────────────
def page_round_of_32() -> None:
    st.markdown("""
    <h2 style="font-size:1.75rem; font-weight:800; color:#0f172a; margin-bottom:0.15rem;">
        Round of 32 — Knockout Stage
    </h2>
    <p style="color:#64748b; margin-bottom:1.4rem;">
        Select your team and predict the full tournament bracket
    </p>
    """, unsafe_allow_html=True)

    # Auto-run group stage if needed
    if not st.session_state.group_results:
        st.info("Running Group Stage simulation first...")
        with st.status("Running Group Stage...", expanded=False) as status:
            results: dict = {}
            for grp_name, teams in WC2026_GROUPS.items():
                table, matches = simulate_group_stage(teams)
                results[grp_name] = (table, matches)
            qualified = get_qualified_32(results)
            st.session_state.group_results = results
            st.session_state.qualified_32  = qualified
            status.update(label="Group Stage complete.", state="complete")
        st.rerun()

    qualified: list = st.session_state.qualified_32 or []
    if not qualified:
        st.error("Could not determine qualified teams. Please run Group Stage manually.")
        if st.button("← Back to Group Stage"):
            _go("group_stage")
        return

    # ── Team Selection Grid ───────────────────────────────────────────────────
    fav = st.session_state.favourite

    st.markdown("""
    <h3 style="font-size:1.05rem; font-weight:700; color:#0f172a; margin-bottom:0.25rem;">
        🎯 Select Your Favourite Team
    </h3>
    <p style="font-size:0.8rem; color:#64748b; margin-bottom:1rem;">
        Choose the team you want to follow. Their matches will be highlighted throughout the bracket.
    </p>
    """, unsafe_allow_html=True)

    cols_per_row = 8
    for row_start in range(0, len(qualified), cols_per_row):
        row_teams = qualified[row_start:row_start + cols_per_row]
        cols = st.columns(len(row_teams))
        for col, team in zip(cols, row_teams):
            inf    = get_team_info(team)
            is_sel = (fav == team)
            sel_cls = "sel" if is_sel else ""
            sel_txt = ('<div style="font-size:0.52rem;color:#16a34a;font-weight:700;">&#10003; SELECTED</div>'
                       if is_sel else "")
            fi = flag_img(team, 40, 27)
            with col:
                st.html(f"""
                <div class="tcard {sel_cls}">
                    <div style="margin-bottom:4px;">{fi}</div>
                    <div style="font-size:0.62rem; font-weight:700;
                         color:{'#1d4ed8' if is_sel else '#334155'};
                         margin-top:2px; text-align:center; word-break:break-word;">
                        {team}
                    </div>
                    <div style="font-size:0.52rem; color:#64748b;">#{inf['fifa_rank']}</div>
                    {sel_txt}
                </div>
                """)
                if st.button("Select", key=f"pick_{team}", use_container_width=True):
                    st.session_state.favourite = team
                    st.session_state.bracket   = None
                    st.rerun()

    # ── Predict Button ────────────────────────────────────────────────────────
    st.html('<hr class="hr">')

    if fav:
        fav_inf = get_team_info(fav)
        st.html(f"""
        <div style="display:flex; align-items:center; gap:0.9rem; margin-bottom:1rem;
             background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px; padding:0.8rem 1rem;">
            <div>{flag_img(fav, 52, 35)}</div>
            <div>
                <div style="font-size:1rem; font-weight:700; color:#1d4ed8;">
                    Favourite: {fav}
                </div>
                <div style="font-size:0.73rem; color:#475569;">
                    FIFA #{fav_inf['fifa_rank']} &nbsp;&middot;&nbsp; {fav_inf['confederation']}
                    &nbsp;&middot;&nbsp; Elo {fav_inf['elo']} &nbsp;&middot;&nbsp; Form: {fav_inf['form']}
                </div>
            </div>
        </div>
        """)

        if st.button("🔮  Predict Tournament Journey", type="primary"):
            _run_full_prediction(qualified, fav)
    else:
        st.warning("👆 Select your favourite team above, then click **Predict Tournament Journey**.")

    # ── Display Bracket ───────────────────────────────────────────────────────
    if st.session_state.bracket:
        _show_bracket(st.session_state.bracket, st.session_state.favourite or "")


def _run_full_prediction(qualified: list, favourite: str) -> None:
    """Simulate the complete knockout tournament step-by-step with status updates."""
    bracket: dict = {}
    current = list(qualified[:32])

    with st.status("Predicting FIFA World Cup 2026 Tournament...", expanded=True) as status:

        st.write("Loading team data and form analysis...")
        time.sleep(0.5)

        st.write("Round of 32 — 16 matches...")
        time.sleep(0.9)
        r32, r16_teams = simulate_knockout_round(current)
        bracket["Round of 32"] = r32
        st.write("16 teams advance to Round of 16.")
        time.sleep(0.4)

        st.write("Round of 16 — 8 matches...")
        time.sleep(0.9)
        r16, qf_teams = simulate_knockout_round(r16_teams)
        bracket["Round of 16"] = r16
        st.write("8 teams advance to Quarter Finals.")
        time.sleep(0.4)

        st.write("Quarter Finals — 4 matches...")
        time.sleep(0.9)
        qf, sf_teams = simulate_knockout_round(qf_teams)
        bracket["Quarter Finals"] = qf
        st.write("4 teams advance to Semi Finals.")
        time.sleep(0.4)

        st.write("Semi Finals — 2 matches...")
        time.sleep(0.9)
        sf, finalists = simulate_knockout_round(sf_teams)
        bracket["Semi Finals"] = sf
        sf_losers = [r["loser"] for r in sf if r["loser"] not in (None, "Draw", "")]
        st.write("2 finalists and 2 third-place contenders determined.")
        time.sleep(0.4)

        if len(sf_losers) >= 2:
            st.write("3rd Place Match...")
            time.sleep(0.7)
            third = simulate_match_detail(sf_losers[0], sf_losers[1], is_knockout=True)
            bracket["3rd Place"] = [third]
            time.sleep(0.3)

        if len(finalists) >= 2:
            st.write("The Final...")
            time.sleep(1.1)
            final = simulate_match_detail(finalists[0], finalists[1], is_knockout=True)
            bracket["Final"] = [final]
            bracket["Champion"] = final["winner"]
            ci = get_team_info(final["winner"])
            st.write(f"World Cup Champion: {ci['flag']} {final['winner']}")
        elif finalists:
            bracket["Champion"] = finalists[0]

        status.update(label="Tournament Prediction Complete.", state="complete")

    st.session_state.bracket = bracket
    st.rerun()


def _show_bracket(bracket: dict, favourite: str) -> None:
    """Render the full bracket with favourite-team highlighting."""
    fav_inf = get_team_info(favourite) if favourite else {}

    if favourite:
        st.markdown(f"""
        <div style="background:#eff6ff; border:1px solid #bfdbfe;
             border-radius:10px; padding:0.75rem 1.2rem; margin:1rem 0;
             display:flex; align-items:center; gap:0.9rem;">
            <span style="font-size:1.6rem;">{fav_inf.get('flag','🏳️')}</span>
            <div>
                <div style="font-size:0.85rem; font-weight:700; color:#1d4ed8;">
                    Tracking: {favourite}
                </div>
                <div style="font-size:0.7rem; color:#64748b;">
                    Highlighted matches show their tournament journey
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    for round_name in ["Round of 32", "Round of 16", "Quarter Finals",
                        "Semi Finals", "3rd Place", "Final"]:
        if round_name in bracket:
            _render_round(bracket[round_name], round_name, favourite)

    if "Champion" in bracket:
        champ_style = ("font-size:1.08rem;font-weight:800;color:#0f172a;"
                       "background:linear-gradient(90deg,#fffbeb 0%,#fef3c7 100%);"
                       "border-left:4px solid #f59e0b;padding:0.6rem 1rem;"
                       "border-radius:4px;margin:1.2rem 0 0.6rem;"
                       "border:1px solid #fde68a;font-family:Georgia,serif;")
        st.html(f'<div style="{champ_style}">World Cup Champion</div>')
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            _render_champion(bracket["Champion"])

    if favourite:
        _show_fav_path(bracket, favourite)


def _show_fav_path(bracket: dict, favourite: str) -> None:
    """Show the favourite team's journey in a white card with black text."""
    st.markdown('<hr class="hr">', unsafe_allow_html=True)
    inf = get_team_info(favourite)

    _stages = ["Round of 32", "Round of 16", "Quarter Finals",
               "Semi Finals", "3rd Place", "Final"]

    # Collect all rows first
    rows_html = ""
    found_any = False
    eliminated_at = None
    is_champion = (bracket.get("Champion") == favourite)

    for stage in _stages:
        if stage not in bracket:
            continue
        for m in bracket[stage]:
            if favourite not in (m["team1"], m["team2"]):
                continue
            found_any = True
            advanced = (m["winner"] == favourite)
            opp      = m["team2"] if m["team1"] == favourite else m["team1"]
            opp_inf  = get_team_info(opp)
            own_prob = m["prob_t1"] if m["team1"] == favourite else m["prob_t2"]

            if advanced:
                result_html = f'<span class="pt-ok">Qualified</span>'
            else:
                result_html = f'<span class="pt-out">Eliminated</span>'
                eliminated_at = stage

            rows_html += f"""
            <tr>
                <td><span class="pt-stage">{stage}</span></td>
                <td class="pt-opp" style="display:flex; align-items:center; gap:6px;">
                    {flag_img(opp, 28, 18)} {opp}
                </td>
                <td><span class="pt-score">{m['score']}</span></td>
                <td class="pt-prob">{own_prob}% win prob</td>
                <td>{result_html}</td>
            </tr>
            """

    if not found_any:
        st.info(f"{favourite} was not found in the bracket records.")
        return

    # Champion / eliminated footer
    if is_champion:
        footer_html = f"""
        <div style="background: linear-gradient(135deg, #fef9c3, #fef08a);
             border: 2px solid #f59e0b; border-radius: 10px;
             padding: 1rem 1.2rem; margin-top: 1rem; text-align: center;">
            <div style="margin-bottom:6px;">{flag_img(favourite, 56, 38)}</div>
            <div style="font-size: 1rem; font-weight: 800; color: #92400e;">
                {favourite} &mdash; AI Predicted FIFA World Cup 2026 Champions
            </div>
        </div>
        """
    elif eliminated_at:
        footer_html = f"""
        <div style="background: #fff1f2; border: 1px solid #fecaca;
             border-radius: 10px; padding: 0.8rem 1.2rem; margin-top: 1rem; text-align:center;">
            <span style="font-size: 0.9rem; font-weight: 700; color: #dc2626;">
                {favourite} were eliminated at the {eliminated_at} stage.
            </span>
        </div>
        """
    else:
        footer_html = ""

    # Render the full white card
    st.html(f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px;
         padding:1.4rem 1.6rem 1rem; margin-top:1rem;
         box-shadow:0 4px 16px rgba(0,0,0,0.08); font-family:Georgia,serif;">
        <div style="font-size:1.05rem; font-weight:800; color:#0f172a;
             margin-bottom:0.9rem; border-bottom:2px solid #e2e8f0;
             padding-bottom:0.55rem; display:flex; align-items:center; gap:0.7rem;">
            {flag_img(favourite, 40, 27)}
            {favourite} &mdash; Tournament Journey
        </div>
        <table style="width:100%; border-collapse:collapse;">
            <thead>
                <tr>
                    <th style="font-size:0.68rem; font-weight:700; text-transform:uppercase;
                               letter-spacing:1px; color:#64748b; padding:0 0.5rem 0.5rem;
                               text-align:left; border-bottom:1px solid #e2e8f0;">Stage</th>
                    <th style="font-size:0.68rem; font-weight:700; text-transform:uppercase;
                               letter-spacing:1px; color:#64748b; padding:0 0.5rem 0.5rem;
                               text-align:left; border-bottom:1px solid #e2e8f0;">Opponent</th>
                    <th style="font-size:0.68rem; font-weight:700; text-transform:uppercase;
                               letter-spacing:1px; color:#64748b; padding:0 0.5rem 0.5rem;
                               text-align:left; border-bottom:1px solid #e2e8f0;">Score</th>
                    <th style="font-size:0.68rem; font-weight:700; text-transform:uppercase;
                               letter-spacing:1px; color:#64748b; padding:0 0.5rem 0.5rem;
                               text-align:left; border-bottom:1px solid #e2e8f0;">Win Prob</th>
                    <th style="font-size:0.68rem; font-weight:700; text-transform:uppercase;
                               letter-spacing:1px; color:#64748b; padding:0 0.5rem 0.5rem;
                               text-align:left; border-bottom:1px solid #e2e8f0;">Result</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        {footer_html}
    </div>
    """)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — ABOUT
# ─────────────────────────────────────────────────────────────────────────────
def page_about() -> None:
    st.markdown("""
    <h2 style="font-size:1.75rem; font-weight:800; color:#0f172a; margin-bottom:1.2rem;">
        About FIFA Oracle 2026
    </h2>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
        #### Machine Learning Model

        FIFA Oracle uses an **XGBoost classifier** trained on historical
        international football match results spanning over 150 years of data.

        **Features used:**
        - Home team identity (Label Encoded)
        - Away team identity (Label Encoded)
        - Historical win/draw/loss patterns

        **Model outputs:**
        - Home Win probability
        - Draw probability
        - Away Win probability

        **Model file:** `models/match_model.pkl`
        **Retrain:** `python src/train.py`
        """)

    with c2:
        st.markdown("""
        #### How It Works

        1. 48 teams split into 12 groups (4 each)
        2. Full round-robin within each group
        3. Top 2 per group (24) + 8 best 3rd-place = **32 qualified**
        4. ML model predicts every knockout match
        5. Draws in knockout resolved by highest win probability
        6. Bracket runs: R32 → R16 → QF → SF → 3rd Place → Final

        #### Data Sources
        - International results dataset (1872–2024)
        - FIFA ranking data
        - Squad strength estimates
        - Recent form data
        """)

    st.markdown('<hr class="hr">', unsafe_allow_html=True)
    st.info(
        "**Predictions are ML-driven, never random.** "
        "Score generation uses controlled randomness around the predicted winner only. "
        "Probabilities displayed are real model outputs from XGBoost's predict_proba()."
    )

    st.markdown("""
    #### Project Structure
    ```
    FIFA-WC-26/
    ├── app.py                <- Main Streamlit application
    ├── requirements.txt
    ├── data/
    │   └── matches.csv       <- Historical match data
    ├── models/
    │   └── match_model.pkl   <- Trained XGBoost model
    └── src/
        ├── train.py          <- Model training script
        ├── predictor.py      <- predict_match() - core ML interface
        ├── standings.py      <- Group simulation
        ├── knockout.py       <- Knockout logic
        ├── groups.py         <- Group creation
        ├── data.py           <- WC 2026 team data (48 nations)
        └── bracket.py        <- Bracket simulation engine
    ```
    """)


# ─────────────────────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────────────────────
_page = st.session_state.page

if _page == "home":
    page_home()
elif _page == "group_stage":
    page_group_stage()
elif _page == "round_of_32":
    page_round_of_32()
elif _page == "about":
    page_about()
else:
    page_home()