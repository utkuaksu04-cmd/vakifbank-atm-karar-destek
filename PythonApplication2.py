
import math
import warnings
from datetime import date, timedelta
from textwrap import dedent

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# Plotly eski Mapbox katmanı yalnızca terminalde deprecation uyarısı üretir.
# Uygulama içi operasyon uyarıları etkilenmez.
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*scatter_mapbox.*deprecated.*",
)
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*scattermapbox.*deprecated.*",
)


# =========================================================
# SAYFA AYARLARI
# =========================================================

st.set_page_config(
    page_title="VakıfBank | Doğu Karadeniz ATM Karar Destek Sistemi",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# TASARIM
# =========================================================

st.markdown(
    dedent("""
    <style>
    :root {
        --bg:#06111b;
        --bg2:#081622;
        --panel:#0f1d2a;
        --panel2:#102230;
        --panel3:#132738;
        --line:#263b4d;
        --text:#f7f9fb;
        --muted:#8fa3b6;
        --yellow:#ffbf00;
        --yellow2:#ffd24a;
        --green:#45c86a;
        --red:#ff4e57;
        --orange:#ff9d31;
        --blue:#4d9cff;
        --purple:#8f75ff;
        --cyan:#32c5c7;
    }

    html, body, [class*="css"] {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                     BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* Streamlit chrome / blank top strip */
    html, body, #root,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main {
        background:#07131f !important;
    }

    header[data-testid="stHeader"] {
        height:0 !important;
        min-height:0 !important;
        display:none !important;
        visibility:hidden !important;
    }

    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    #MainMenu,
    footer {
        display:none !important;
        visibility:hidden !important;
    }

    [data-testid="stAppViewContainer"] {
        padding-top:0 !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding-top:0 !important;
        margin-top:0 !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 82% -12%,rgba(55,90,130,.18),transparent 30%),
            linear-gradient(180deg,#07131f 0%,#06111b 100%);
        color:var(--text);
    }

    .block-container {
        max-width:none !important;
        width:100% !important;
        padding-top:.75rem !important;
        padding-left:1.25rem !important;
        padding-right:1.25rem !important;
        padding-bottom:2rem !important;
    }

    /* Sidebar dimensions closer to the reference */
    section[data-testid="stSidebar"] {
        width:315px !important;
        min-width:315px !important;
        background:linear-gradient(180deg,#07131e 0%,#081622 58%,#091a27 100%) !important;
        border-right:1px solid #263b4d !important;
        box-shadow:10px 0 34px rgba(0,0,0,.16);
    }

    section[data-testid="stSidebar"] > div:first-child {
        width:315px !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top:.65rem !important;
    }

    section[data-testid="stSidebar"] * {
        color:#eef3f7;
    }

    [data-testid="stSidebarCollapseButton"] {
        display:none !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap:8px;
    }

    section[data-testid="stSidebar"] label[data-baseweb="radio"] {
        width:100%;
        min-height:50px;
        margin:0;
        padding:12px 13px;
        border-radius:11px;
        transition:.18s ease;
    }

    section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
        background:#102231;
    }

    section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) {
        background:linear-gradient(90deg,rgba(255,191,0,.20),rgba(255,191,0,.07));
        box-shadow:inset 3px 0 0 var(--yellow);
    }

    section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) p {
        color:#ffd548 !important;
        font-weight:850 !important;
    }

    section[data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child {
        display:none !important;
    }

    section[data-testid="stSidebar"] label[data-baseweb="radio"] p {
        white-space:nowrap !important;
        overflow:visible !important;
        text-overflow:clip !important;
        font-size:1.02rem !important;
        line-height:1.30 !important;
        font-weight:780 !important;
        letter-spacing:-.1px !important;
    }

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color:#aebfce !important;
        font-size:.80rem !important;
        line-height:1.45 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        font-size:.91rem !important;
        line-height:1.45 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stAlert"] p {
        font-size:.89rem !important;
        font-weight:760 !important;
    }

    /* Sidebar brand */
    .vb-brand {
        display:flex;
        align-items:center;
        gap:10px;
        padding:4px 2px 8px;
        margin-bottom:4px;
    }

    .vb-mark {
        width:42px;
        height:33px;
        display:inline-flex;
        align-items:center;
        justify-content:center;
        flex:0 0 42px;
        border-radius:10px 4px 10px 4px;
        background:var(--yellow);
        color:#111;
        font-size:.78rem;
        font-weight:1000;
        transform:skewX(-10deg);
        box-shadow:0 9px 24px rgba(255,191,0,.12);
    }

    .vb-mark span { transform:skewX(10deg); }

    .vb-brand-name {
        font-size:1.72rem;
        font-weight:900;
        color:#fff;
        letter-spacing:-.6px;
    }

    /* Main top bar */
    .app-header {
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:18px;
        padding:3px 0 13px;
        border-bottom:1px solid rgba(255,255,255,.045);
        margin-bottom:10px;
    }

    .app-header-left {
        display:flex;
        align-items:center;
        min-width:0;
        gap:13px;
    }

    .menu-square {
        width:42px;
        height:42px;
        flex:0 0 42px;
        border-radius:10px;
        display:flex;
        align-items:center;
        justify-content:center;
        background:#0d1d2b;
        border:1px solid #243a4c;
        color:#fff;
        font-size:1.1rem;
    }

    .app-title {
        color:#fff;
        font-size:clamp(1.45rem,2.1vw,2.12rem);
        line-height:1.06;
        font-weight:900;
        letter-spacing:-.7px;
        margin:0;
        white-space:normal;
    }

    .app-subtitle {
        color:var(--yellow);
        font-size:.76rem;
        font-weight:760;
        margin-top:5px;
    }

    .user-area {
        display:flex;
        align-items:center;
        gap:10px;
        flex:0 0 auto;
    }

    .bell-box {
        position:relative;
        width:39px;
        height:39px;
        display:flex;
        align-items:center;
        justify-content:center;
        border-radius:10px;
        border:1px solid #263b4d;
        background:#0d1c29;
        font-size:1rem;
    }

    .bell-count {
        position:absolute;
        right:-4px;
        top:-5px;
        width:18px;
        height:18px;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        background:var(--yellow);
        color:#111;
        font-size:.58rem;
        font-weight:950;
    }

    .user-avatar {
        width:39px;
        height:39px;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        background:linear-gradient(135deg,#6d8093,#2e4050);
        color:#fff;
        font-size:.7rem;
        font-weight:900;
    }

    .user-copy strong {
        display:block;
        color:#fff;
        font-size:.71rem;
    }

    .user-copy span {
        display:block;
        color:#8296a8;
        font-size:.58rem;
        margin-top:2px;
    }

    /* Inputs */
    label[data-testid="stWidgetLabel"] p {
        color:#e7eef5 !important;
        font-size:.73rem !important;
        font-weight:760 !important;
    }

    div[data-baseweb="select"] > div,
    div[data-testid="stDateInput"] input,
    div[data-testid="stTextInput"] input {
        background:#0d1c29 !important;
        color:#f7f9fb !important;
        border-color:#2a4053 !important;
        border-radius:9px !important;
        min-height:40px !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    div[data-testid="stDateInput"] input:focus,
    div[data-testid="stTextInput"] input:focus {
        border-color:#cfa81f !important;
        box-shadow:0 0 0 2px rgba(255,191,0,.08) !important;
    }

    /* Buttons */
    .stButton > button {
        min-height:40px;
        border-radius:9px;
        border:1px solid #30475a;
        background:#0d1c29;
        color:#d5e0e8;
        font-size:.70rem;
        font-weight:800;
    }

    .stButton > button:hover {
        border-color:#51687a;
        color:#fff;
    }

    .stButton > button[kind="primary"] {
        background:linear-gradient(135deg,var(--yellow),var(--yellow2));
        color:#111;
        border:none;
        font-weight:900;
    }

    /* Bordered Streamlit containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:linear-gradient(180deg,#0f1d2a 0%,#0b1824 100%);
        border:1px solid #263b4d !important;
        border-radius:14px !important;
        box-shadow:0 12px 28px rgba(0,0,0,.08);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        padding-top:.15rem;
    }

    /* Native metrics for sub-pages */
    div[data-testid="stMetric"] {
        background:linear-gradient(180deg,#102230 0%,#0e1b28 100%);
        border:1px solid #263b4d;
        border-radius:13px;
        padding:13px 14px;
        min-height:102px;
        overflow:hidden;
    }

    div[data-testid="stMetricLabel"] {
        color:#9eb0c0;
        font-size:.70rem;
    }

    div[data-testid="stMetricValue"] {
        color:#fff;
        font-weight:900;
        font-size:1.55rem;
    }

    /* Titles in panels */
    h1,h2,h3 {
        color:#fff;
        letter-spacing:-.35px;
    }

    h3 {
        font-size:1rem !important;
        margin-top:.1rem !important;
        margin-bottom:.35rem !important;
    }

    [data-testid="stCaptionContainer"] {
        color:#8296a8 !important;
        font-size:.66rem !important;
    }

    /* Custom KPI cards */
    .kpi-card {
        position:relative;
        min-height:116px;
        background:linear-gradient(180deg,#102230 0%,#0e1b28 100%);
        border:1px solid #263b4d;
        border-radius:14px;
        padding:15px 15px;
        overflow:hidden;
        box-shadow:0 12px 28px rgba(0,0,0,.08);
    }

    .kpi-top {
        display:flex;
        align-items:center;
        gap:11px;
    }

    .kpi-icon {
        width:48px;
        height:48px;
        flex:0 0 48px;
        display:flex;
        align-items:center;
        justify-content:center;
        border-radius:12px;
        font-size:.95rem;
        font-weight:950;
    }

    .kpi-icon.blue { color:#8ab5ff;background:rgba(77,156,255,.18); }
    .kpi-icon.green { color:#86e19a;background:rgba(69,200,106,.16); }
    .kpi-icon.red { color:#ff8b91;background:rgba(255,78,87,.16); }
    .kpi-icon.purple { color:#b7a9ff;background:rgba(143,117,255,.16); }
    .kpi-icon.cyan { color:#80edef;background:rgba(50,197,199,.16); }

    .kpi-label {
        color:#c6d1db;
        font-size:.72rem;
        margin-bottom:5px;
    }

    .kpi-value {
        color:#fff;
        font-size:1.72rem;
        font-weight:950;
        line-height:1;
        letter-spacing:-.55px;
        white-space:nowrap;
    }

    .kpi-note {
        color:#8194a6;
        font-size:.64rem;
        margin-top:7px;
    }

    .kpi-good { color:#62d47d; }
    .kpi-bad { color:#ff6d75; }

    /* Dashboard route cards */
    .route-card {
        background:#102130;
        border:1px solid #2a3e51;
        border-left:3px solid var(--route-color);
        border-radius:11px;
        padding:11px 12px;
        margin-bottom:9px;
        overflow:hidden;
        width:100%;
    }

    .route-head {
        display:grid;
        grid-template-columns:minmax(150px,1fr) 78px 88px 88px;
        gap:8px;
        align-items:start;
        width:100%;
    }

    .route-name {
        color:#fff;
        font-size:.78rem;
        font-weight:900;
    }

    .route-vehicle {
        display:inline-block;
        margin-top:5px;
        padding:3px 7px;
        border-radius:999px;
        background:#173249;
        color:#8ec3ff;
        font-size:.58rem;
        font-weight:850;
    }

    .route-metric {
        text-align:right;
        min-width:0;
    }

    .route-metric span {
        display:block;
        color:#8194a6;
        font-size:.50rem;
        margin-bottom:3px;
        text-transform:uppercase;
    }

    .route-metric strong {
        color:#fff;
        font-size:.72rem;
        white-space:nowrap;
    }

    .route-stops {
        border-top:1px solid rgba(255,255,255,.06);
        margin-top:7px;
        padding-top:6px;
        color:#a5b5c2;
        font-size:.57rem;
        line-height:1.4;
    }

    /* Data frames */
    div[data-testid="stDataFrame"] {
        border:1px solid #263b4d;
        border-radius:11px;
        overflow:hidden;
    }


    /* =====================================================
       ROTA / SENARYO - KOYU FORM TEMASI
       ===================================================== */

    div[data-testid="stExpander"] details {
        background:linear-gradient(180deg,#0f1d2a 0%,#0b1824 100%) !important;
        border:1px solid #263b4d !important;
        border-radius:13px !important;
        overflow:hidden !important;
    }

    div[data-testid="stExpander"] details > summary {
        background:#102230 !important;
        color:#ffffff !important;
        border-bottom:1px solid rgba(255,255,255,.05) !important;
    }

    div[data-testid="stExpander"] details > summary:hover {
        background:#142838 !important;
    }

    div[data-testid="stExpander"] details > summary p,
    div[data-testid="stExpander"] details > summary span,
    div[data-testid="stExpander"] details > summary svg {
        color:#ffffff !important;
        fill:#ffffff !important;
    }

    div[data-testid="stExpander"] details[open] > div {
        background:#0d1b28 !important;
        color:#f7f9fb !important;
    }

    div[data-testid="stNumberInput"] div[data-baseweb="input"],
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stTextInput"] input {
        background:#0d1c29 !important;
        color:#ffffff !important;
        border-color:#2a4053 !important;
    }

    div[data-testid="stNumberInput"] button {
        background:#102230 !important;
        color:#ffffff !important;
        border-color:#2a4053 !important;
    }

    div[data-testid="stNumberInput"] button svg {
        color:#ffffff !important;
        fill:#ffffff !important;
    }

    div[data-baseweb="select"] > div {
        background:#0d1c29 !important;
        color:#ffffff !important;
        border-color:#2a4053 !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input {
        color:#ffffff !important;
    }

    div[data-baseweb="popover"] ul,
    ul[data-testid="stSelectboxVirtualDropdown"],
    div[data-baseweb="menu"] {
        background:#0d1c29 !important;
        color:#ffffff !important;
        border:1px solid #2a4053 !important;
    }

    div[role="option"] {
        background:#0d1c29 !important;
        color:#ffffff !important;
    }

    div[role="option"]:hover,
    div[role="option"][aria-selected="true"] {
        background:#173249 !important;
        color:#ffffff !important;
    }

    div[data-testid="stToggle"] label p,
    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] label,
    div[data-testid="stExpander"] span {
        color:#dbe4ec !important;
    }

    /* =====================================================
       GENEL METİN KONTRASTI - KOYU TEMA
       ===================================================== */

    /* Ana içerikte kaybolan Streamlit metinlerini görünür tut */
    [data-testid="stMain"] .stMarkdown p,
    [data-testid="stMain"] .stMarkdown span,
    [data-testid="stMain"] .stText,
    [data-testid="stMain"] label p,
    [data-testid="stMain"] label span {
        color:#f4f7fa !important;
    }

    /* Açıklamalar beyazdan biraz daha yumuşak ama rahat okunur */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p,
    [data-testid="stCaptionContainer"] span {
        color:#aebdcc !important;
    }

    /* Tabs / segmented-control / BaseWeb tab yazıları */
    div[data-testid="stTabs"] button,
    div[data-testid="stTabs"] button p,
    div[data-testid="stTabs"] button span,
    div[data-testid="stSegmentedControl"] button,
    div[data-testid="stSegmentedControl"] button p,
    div[data-testid="stSegmentedControl"] button span,
    div[role="tablist"] button,
    div[role="tablist"] button p,
    div[role="tablist"] button span,
    button[data-baseweb="tab"],
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color:#ffffff !important;
        font-weight:760 !important;
    }

    /* Koyu temadaki normal buton yazıları */
    .stButton > button:not([kind="primary"]),
    .stButton > button:not([kind="primary"]) p,
    .stButton > button:not([kind="primary"]) span {
        color:#ffffff !important;
    }

    /* Sarı birincil butonda koyu yazı daha yüksek kontrast verir */
    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span {
        color:#111111 !important;
    }

    /* Checkbox / radio / toggle ve slider metinleri */
    div[data-testid="stCheckbox"] p,
    div[data-testid="stRadio"] p,
    div[data-testid="stToggle"] p,
    div[data-testid="stSlider"] p,
    div[data-testid="stSlider"] span {
        color:#f4f7fa !important;
    }

    /* Metric kartlarında etiketlerin fazla kararmasını önle */
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] p {
        color:#c5d2dd !important;
    }

    /* Expander başlığı ve içindeki form metinleri */
    div[data-testid="stExpander"] details > summary *,
    div[data-testid="stExpander"] details[open] label p,
    div[data-testid="stExpander"] details[open] label span {
        color:#ffffff !important;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius:10px;
        font-size:.72rem;
    }

    /* Progress */
    div[data-testid="stProgress"] > div > div {
        background:linear-gradient(90deg,var(--blue),var(--green)) !important;
    }

    @media (max-width:1100px) {
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div:first-child {
            width:245px !important;
            min-width:245px !important;
        }

        .user-copy { display:none; }

        .route-head {
            grid-template-columns:1fr 1fr;
        }
    }
    </style>
    """),
    unsafe_allow_html=True,
)


# =========================================================
# VERİ
# =========================================================

ATM = pd.DataFrame(
    [
        ["ATM-015", "Trabzon", "Ortahisar", 41.0027, 39.7168, 25200, 85600, "Yüksek", 0.96],
        ["ATM-018", "Trabzon", "Akçaabat", 41.0219, 39.5717, 46200, 41400, "Düşük", 0.78],
        ["ATM-021", "Trabzon", "Yomra", 40.9548, 39.8644, 32100, 49100, "Orta", 0.82],
        ["ATM-024", "Trabzon", "Vakfıkebir", 41.0453, 39.2767, 38400, 35600, "Düşük", 0.70],
        ["ATM-042", "Rize", "Merkez", 41.0255, 40.5177, 18500, 72300, "Yüksek", 0.92],
        ["ATM-044", "Rize", "Çayeli", 41.0897, 40.7301, 27400, 49800, "Orta", 0.80],
        ["ATM-047", "Rize", "Ardeşen", 41.1911, 40.9875, 19800, 52400, "Yüksek", 0.84],
        ["ATM-009", "Artvin", "Hopa", 41.3907, 41.4227, 14800, 48200, "Orta", 0.86],
        ["ATM-011", "Artvin", "Merkez", 41.1828, 41.8183, 35700, 32100, "Düşük", 0.74],
        ["ATM-031", "Giresun", "Merkez", 40.9128, 38.3895, 33000, 39700, "Orta", 0.81],
        ["ATM-028", "Giresun", "Bulancak", 40.9372, 38.2318, 48700, 28100, "Düşük", 0.68],
        ["ATM-034", "Giresun", "Tirebolu", 41.0064, 38.8135, 21300, 44200, "Orta", 0.76],
        ["ATM-022", "Ordu", "Altınordu", 40.9862, 37.8797, 41200, 28900, "Düşük", 0.83],
        ["ATM-025", "Ordu", "Fatsa", 41.0268, 37.5014, 18600, 55300, "Yüksek", 0.85],
        ["ATM-026", "Ordu", "Ünye", 41.1272, 37.2887, 30200, 40700, "Orta", 0.77],
    ],
    columns=[
        "ATM Kodu", "İl", "İlçe", "Lat", "Lon",
        "Mevcut Nakit", "24s Tahmin", "Kritiklik", "Operasyon Etkisi"
    ],
)

SUMMARY = {
    "Doğu Karadeniz": {"atm": 285, "refill": 42, "critical": 12, "demand": 68.4, "eff": 87},
    "Trabzon": {"atm": 68, "refill": 10, "critical": 4, "demand": 16.3, "eff": 89},
    "Rize": {"atm": 54, "refill": 11, "critical": 5, "demand": 13.0, "eff": 84},
    "Ordu": {"atm": 63, "refill": 8, "critical": 2, "demand": 15.1, "eff": 88},
    "Giresun": {"atm": 58, "refill": 7, "critical": 1, "demand": 13.9, "eff": 90},
    "Artvin": {"atm": 42, "refill": 6, "critical": 2, "demand": 10.1, "eff": 82},
}

CITY_ROUTE_BASE = {
    "Trabzon": {"km": 286, "cost": 6420, "vehicles": 6},
    "Rize": {"km": 224, "cost": 5210, "vehicles": 4},
    "Ordu": {"km": 278, "cost": 6150, "vehicles": 5},
    "Giresun": {"km": 312, "cost": 6980, "vehicles": 5},
    "Artvin": {"km": 198, "cost": 4860, "vehicles": 3},
}

SCENARIOS = pd.DataFrame(
    [
        ["Ekonomik", -1, 0.93, 0.90, 90, 28],
        ["Dengeli", 0, 1.00, 1.00, 95, 12],
        ["Yüksek Hizmet", 1, 1.08, 1.17, 98, 5],
        ["Yoğun Talep", 1, 1.18, 1.28, 97, 8],
    ],
    columns=[
        "Senaryo", "Araç Farkı", "Mesafe Çarpanı",
        "Maliyet Çarpanı", "Hizmet Seviyesi", "Risk"
    ],
)

RISK_SCORE = {"Yüksek": 3, "Orta": 2, "Düşük": 1}
RISK_COLOR = {"Yüksek": "#ff3b58", "Orta": "#ffb300", "Düşük": "#20d879"}

CITY_LABELS = pd.DataFrame(
    [
        ["Ordu", 40.9862, 37.8797],
        ["Giresun", 40.9128, 38.3895],
        ["Trabzon", 41.0027, 39.7168],
        ["Rize", 41.0255, 40.5177],
        ["Artvin", 41.1828, 41.8183],
    ],
    columns=["İl", "Lat", "Lon"],
)


# =========================================================
# OSM / OSRM ROTA VE MALİYET MODELİ
# =========================================================
#
# Rota planlamasında düz/temsili mesafe kullanılmaz; gerçek sürüş yolu kullanılır.
# Yol mesafesi ve sürüş süresi OpenStreetMap yol verisini kullanan
# OSRM yönlendirme servisinden alınır.
#
# Toplam rota maliyeti SADECE:
#   1) Yol / araç işletme maliyeti
#   2) Çalışan işçilik maliyeti
# kalemlerinden oluşur.
#
# İş kazası, seminer/konferans, konaklama/harcırah vb. maliyetler
# ayrı maliyet kategorileri olarak izlenebilir; rota toplamına
# otomatik olarak dahil edilmez.

OSRM_BASE_URL = "https://router.project-osrm.org"

CITY_DEPOT_CODE = {
    "Trabzon": "ATM-015",
    "Rize": "ATM-042",
    "Ordu": "ATM-022",
    "Giresun": "ATM-031",
    "Artvin": "ATM-011",
}

COST_CATEGORY_CATALOG = pd.DataFrame(
    [
        ["Yol / Araç İşletme", "TL / km", "Aktif", "Rota ve senaryo toplamına dahil"],
        ["İşçilik", "TL / saat / çalışan", "Aktif", "Rota ve senaryo toplamına dahil"],
        ["İş Kazası / İşgücü Kaybı", "Olay başına", "Ayrı izleme", "Rota toplamına dahil değil"],
        ["Seminer / Konferans / Eğitim", "Kişi / etkinlik", "Ayrı izleme", "Rota toplamına dahil değil"],
        ["Konaklama / Harcırah", "Kişi / gün", "Ayrı izleme", "Rota toplamına dahil değil"],
        ["Fazla Mesai", "Saat / çalışan", "Ayrı izleme", "İstenirse sonraki modelde eklenebilir"],
    ],
    columns=["Maliyet Kalemi", "Ölçü Birimi", "Durum", "Model Notu"],
)


# =========================================================
# YARDIMCI FONKSİYONLAR
# =========================================================

def compact_html(html_text):
    """Streamlit Markdown'ta HTML bloklarının kod bloğuna dönüşmesini engeller."""
    return "".join(line.strip() for line in html_text.splitlines() if line.strip())


def safe_plotly_chart(fig):
    """Plotly grafiğini tam genişlikte ve araç çubuğu kapalı render eder."""
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


def fmt_tl(x):
    return f"₺{x:,.0f}".replace(",", ".")


def fmt_m(x):
    return f"₺{x:.1f} M".replace(".", ",")


def region_df(region):
    if region == "Doğu Karadeniz":
        return ATM.copy()
    return ATM[ATM["İl"] == region].copy()


def scenario_factor(name):
    return {
        "Normal Talep": 1.00,
        "Yoğun Talep": 1.18,
        "Düşük Talep": 0.84,
        "Turizm Sezonu": 1.12,
    }[name]


@st.cache_data(ttl=3600, show_spinner=False)
def osrm_route(lat1, lon1, lat2, lon2):
    """
    İki koordinat arasındaki gerçek karayolu rotasını OSRM üzerinden alır.

    Çıktı:
      distance_km  : sürüş mesafesi (km)
      duration_min : sürüş süresi (dk)
      geometry     : haritada çizilecek [(lat, lon), ...] noktaları
    """
    coords = (
        f"{float(lon1):.6f},{float(lat1):.6f};"
        f"{float(lon2):.6f},{float(lat2):.6f}"
    )

    url = f"{OSRM_BASE_URL}/route/v1/driving/{coords}"

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=12,
            headers={
                "User-Agent": "KTU-VakifBank-ATM-DecisionSupport/1.0"
            },
        )
        response.raise_for_status()
        data = response.json()

        if data.get("code") != "Ok" or not data.get("routes"):
            return None

        route = data["routes"][0]
        coords_geojson = route.get("geometry", {}).get("coordinates", [])

        geometry = [
            (float(lat), float(lon))
            for lon, lat in coords_geojson
        ]

        return {
            "distance_km": float(route["distance"]) / 1000,
            "duration_min": float(route["duration"]) / 60,
            "geometry": geometry,
            "source": "OpenStreetMap / OSRM",
        }

    except (requests.RequestException, ValueError, KeyError, TypeError):
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def osrm_table(coords_tuple):
    """
    Birden fazla nokta için OSRM sürüş mesafesi ve süre matrisi üretir.

    coords_tuple formatı:
        ((lat, lon), (lat, lon), ...)
    """
    if not coords_tuple:
        return None

    coords_text = ";".join(
        f"{float(lon):.6f},{float(lat):.6f}"
        for lat, lon in coords_tuple
    )

    url = f"{OSRM_BASE_URL}/table/v1/driving/{coords_text}"

    try:
        response = requests.get(
            url,
            params={"annotations": "distance,duration"},
            timeout=15,
            headers={
                "User-Agent": "KTU-VakifBank-ATM-DecisionSupport/1.0"
            },
        )
        response.raise_for_status()
        data = response.json()

        if data.get("code") != "Ok":
            return None

        distances_raw = data.get("distances")
        durations_raw = data.get("durations")

        if distances_raw is None or durations_raw is None:
            return None

        distances_km = [
            [
                None if value is None else float(value) / 1000
                for value in row
            ]
            for row in distances_raw
        ]

        durations_min = [
            [
                None if value is None else float(value) / 60
                for value in row
            ]
            for row in durations_raw
        ]

        return {
            "distances_km": distances_km,
            "durations_min": durations_min,
            "source": "OpenStreetMap / OSRM",
        }

    except (requests.RequestException, ValueError, KeyError, TypeError):
        return None


def nearest_neighbor_order(distance_matrix, start_index=0, return_to_start=False):
    """
    OSRM sürüş mesafesi matrisi üzerinde basit en yakın komşu sezgiseli.

    Sonuç:
        order = ziyaret sırası indeksleri
        legs  = [(from_index, to_index, km), ...]
    """
    n = len(distance_matrix)

    if n == 0:
        return [], []

    start_index = max(0, min(start_index, n - 1))

    remaining = set(range(n))
    remaining.remove(start_index)

    order = [start_index]
    legs = []
    current = start_index

    while remaining:
        candidates = []

        for candidate in remaining:
            distance = distance_matrix[current][candidate]

            if distance is not None:
                candidates.append((distance, candidate))

        if not candidates:
            break

        distance, nxt = min(candidates, key=lambda x: x[0])

        legs.append((current, nxt, float(distance)))
        order.append(nxt)

        current = nxt
        remaining.remove(nxt)

    if return_to_start and len(order) > 1:
        return_distance = distance_matrix[current][start_index]

        if return_distance is not None:
            legs.append((current, start_index, float(return_distance)))

    return order, legs


def route_cost_breakdown(
    road_distance_km,
    driving_minutes,
    road_cost_per_km=0.0,
    hourly_worker_cost=0.0,
    crew_size=1,
    service_minutes=0.0,
    fixed_stop_cost=0.0,
    service_stop_count=0,
    include_road=True,
    include_labor=True,
    include_fixed_stop=False,
):
    """
    Gerçek OSM/OSRM sürüş rotası için seçili maliyet kalemlerini hesaplar.

    Kalemler:
      - Yol / araç işletme maliyeti (TL/km)
      - İşçilik maliyeti (TL/saat/çalışan)
      - ATM ikmal / durak sabit maliyeti (TL/durak)

    service_minutes toplam hizmet süresidir; sürüş süresine eklenerek
    işçilik maliyetine yansıtılır.
    """
    road_distance_km = float(road_distance_km)
    driving_minutes = float(driving_minutes)
    service_minutes = float(service_minutes)

    road_cost = (
        road_distance_km * float(road_cost_per_km)
        if include_road
        else 0.0
    )

    operation_minutes = driving_minutes + service_minutes
    labor_hours = operation_minutes / 60

    labor_cost = (
        labor_hours
        * int(crew_size)
        * float(hourly_worker_cost)
        if include_labor
        else 0.0
    )

    fixed_service_cost = (
        float(fixed_stop_cost) * int(service_stop_count)
        if include_fixed_stop
        else 0.0
    )

    return {
        "road_cost": road_cost,
        "labor_cost": labor_cost,
        "fixed_service_cost": fixed_service_cost,
        "total_cost": road_cost + labor_cost + fixed_service_cost,
        "operation_minutes": operation_minutes,
        "labor_hours": labor_hours,
    }


@st.cache_data(ttl=3600, show_spinner=False)
def city_osrm_baseline(city):
    """
    Her il için temsili ATM örneklemi üzerinde OSM/OSRM sürüş matrisi kurar
    ve il operasyon merkezi kabul edilen ATM'den başlayan/dönen bir tur
    üretir.

    OSRM erişilemezse None döner. Senaryo ekranı bu durumda mevcut
    temsili karayolu baz değerlerini yedek olarak kullanır.
    """
    city_df = ATM[ATM["İl"] == city].copy().reset_index(drop=True)

    if city_df.empty:
        return None

    coords_tuple = tuple(
        (float(row["Lat"]), float(row["Lon"]))
        for _, row in city_df.iterrows()
    )

    table = osrm_table(coords_tuple)

    if table is None:
        return None

    depot_code = CITY_DEPOT_CODE.get(city)

    depot_matches = city_df.index[
        city_df["ATM Kodu"] == depot_code
    ].tolist()

    start_index = depot_matches[0] if depot_matches else 0

    order, legs = nearest_neighbor_order(
        table["distances_km"],
        start_index=start_index,
        return_to_start=True,
    )

    total_km = 0.0
    total_minutes = 0.0

    for from_idx, to_idx, leg_km in legs:
        total_km += float(leg_km)

        duration = table["durations_min"][from_idx][to_idx]

        if duration is not None:
            total_minutes += float(duration)

    return {
        "city": city,
        "distance_km": total_km,
        "duration_min": total_minutes,
        "stop_count": len(city_df),
        "order": order,
        "codes": city_df["ATM Kodu"].tolist(),
        "source": table["source"],
    }


def map_fig(df, height=430, selected_codes=None, line_points=None, show_city_labels=True):
    """
    Açık renkli, şehir ve yol isimleri görünür OpenStreetMap operasyon haritası.
    Rota geometrisi OSRM'den gelir; harita tabanı API anahtarı gerektirmez.
    """
    selected_codes = selected_codes or []

    tmp = df.copy()
    tmp["Marker Boyutu"] = tmp["ATM Kodu"].apply(
        lambda x: 18 if x in selected_codes else 11
    )

    # Yeni Plotly MapLibre katmanı: API anahtarı istemeyen OpenStreetMap.
    fig = px.scatter_map(
        tmp,
        lat="Lat",
        lon="Lon",
        color="Kritiklik",
        size="Marker Boyutu",
        size_max=18,
        hover_name="ATM Kodu",
        custom_data=["ATM Kodu"],
        hover_data={
            "İl": True,
            "İlçe": True,
            "Mevcut Nakit": ":,.0f",
            "24s Tahmin": ":,.0f",
            "Lat": False,
            "Lon": False,
            "Marker Boyutu": False,
        },
        color_discrete_map=RISK_COLOR,
        zoom=6.25 if len(tmp) > 6 else 8.15,
        height=height,
        opacity=.94,
        map_style="open-street-map",
    )

    # Seçili ATM'leri altın renkli halka/halo ile ayırt et.
    if selected_codes:
        selected_df = tmp[tmp["ATM Kodu"].isin(selected_codes)].copy()
        if not selected_df.empty:
            fig.add_trace(
                go.Scattermap(
                    lat=selected_df["Lat"],
                    lon=selected_df["Lon"],
                    mode="markers",
                    marker=dict(
                        size=27,
                        color="rgba(255,191,0,.28)",
                        opacity=.82,
                    ),
                    hoverinfo="skip",
                    showlegend=False,
                    name="Seçili ATM vurgusu",
                )
            )

    # Gerçek OSRM sürüş rotası: altta gölge, üstte VakıfBank sarısı.
    if line_points:
        route_lat = [p[0] for p in line_points]
        route_lon = [p[1] for p in line_points]

        fig.add_trace(
            go.Scattermap(
                lat=route_lat,
                lon=route_lon,
                mode="lines",
                line=dict(width=9, color="rgba(31,41,55,.30)"),
                hoverinfo="skip",
                showlegend=False,
                name="Rota gölgesi",
            )
        )
        fig.add_trace(
            go.Scattermap(
                lat=route_lat,
                lon=route_lon,
                mode="lines",
                line=dict(width=4.5, color="#ffbf00"),
                hoverinfo="skip",
                name="Gerçek sürüş rotası",
            )
        )

    # Şehir adlarını taban haritasına ek olarak belirgin biçimde göster.
    if show_city_labels:
        labels = CITY_LABELS.copy()

        if len(tmp) <= 6 and len(tmp) > 0:
            cities = tmp["İl"].unique().tolist()
            labels = labels[labels["İl"].isin(cities)]

        # Yazıları ATM işaretlerinden biraz yukarı taşı.
        labels["LabelLat"] = labels["Lat"] + 0.105

        # Hafif beyaz halo etkisi için önce daha büyük açık renk yazı.
        fig.add_trace(
            go.Scattermap(
                lat=labels["LabelLat"],
                lon=labels["Lon"],
                mode="text",
                text=labels["İl"],
                textfont=dict(
                    color="rgba(255,255,255,.96)",
                    size=18,
                    family="Arial Black",
                ),
                hoverinfo="skip",
                showlegend=False,
                name="Şehir etiketi zemini",
            )
        )
        fig.add_trace(
            go.Scattermap(
                lat=labels["LabelLat"],
                lon=labels["Lon"],
                mode="text",
                text=labels["İl"],
                textfont=dict(
                    color="#17324d",
                    size=14,
                    family="Arial Black",
                ),
                hoverinfo="skip",
                showlegend=False,
                name="Şehir etiketleri",
            )
        )

    # Harita merkezini görünür ATM örneklemi üzerinde tut.
    center_lat = float(tmp["Lat"].mean()) if not tmp.empty else 41.0
    center_lon = float(tmp["Lon"].mean()) if not tmp.empty else 39.7
    map_zoom = 6.25 if len(tmp) > 6 else 8.15

    fig.update_layout(
        map=dict(
            style="open-street-map",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=map_zoom,
            bearing=0,
            pitch=0,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#07131f",
        plot_bgcolor="#07131f",
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#d6dee7",
            font=dict(color="#102230", size=12),
        ),
        legend=dict(
            orientation="h",
            y=1.015,
            x=.01,
            bgcolor="rgba(255,255,255,.94)",
            bordercolor="rgba(23,50,77,.22)",
            borderwidth=1,
            font=dict(color="#17324d", size=11),
            title=None,
        ),
    )

    return fig

def demand_line_chart(values, labels, height=330, y_title="Milyon TL"):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=labels,
            y=values,
            mode="lines+markers",
            line=dict(color="#4d9cff", width=3),
            marker=dict(
                size=7,
                color="#dceeff",
                line=dict(color="#4d9cff", width=2),
            ),
            fill="tozeroy",
            fillcolor="rgba(77,156,255,.12)",
        )
    )

    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#0f1d2a",
        plot_bgcolor="#0f1d2a",
        font=dict(color="#dbe4ec"),
        showlegend=False,
        xaxis=dict(showgrid=False, type="category"),
        yaxis=dict(
            title=y_title,
            gridcolor="rgba(255,255,255,.06)",
        ),
    )

    return fig


def kpi_html(icon_class, icon, label, value, note, note_class=""):
    return compact_html(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-icon {icon_class}">{icon}</div>
                <div>
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-note {note_class}">{note}</div>
                </div>
            </div>
        </div>
        """
    )


def route_card_html(name, vehicle, km, duration, cost, stops, color):
    return compact_html(
        f"""
        <div class="route-card" style="--route-color:{color}">
            <div class="route-head">
                <div>
                    <div class="route-name">🚚 {name}</div>
                    <span class="route-vehicle">Araç {vehicle}</span>
                </div>
                <div class="route-metric"><span>TOPLAM KM</span><strong>{km} km</strong></div>
                <div class="route-metric"><span>TOPLAM SÜRE</span><strong>{duration}</strong></div>
                <div class="route-metric"><span>MALİYET</span><strong>{fmt_tl(cost)}</strong></div>
            </div>
            <div class="route-stops">⌖ {stops}</div>
        </div>
        """
    )



def reset_dashboard_filters():
    st.session_state["dash_region"] = "Doğu Karadeniz"
    st.session_state["dash_date"] = date(2026, 8, 28)
    st.session_state["dash_scenario"] = "Normal Talep"
    st.session_state["dash_vehicle"] = 6
    st.session_state["dash_service"] = 95


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        compact_html(
            """
            <div class="vb-brand">
                <div class="vb-mark"><span>VB</span></div>
                <div class="vb-brand-name">VakıfBank</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.caption("Doğu Karadeniz ATM Karar Destek Sistemi")

    MENU_ICONS = {
        "Dashboard": "▦",
        "ATM İzleme": "▤",
        "Talep Tahmini": "⌁",
        "Kritik Önceliklendirme": "⚠",
        "Nakit & İkmal Optimizasyonu": "₺",
        "Rota Planlama": "⌖",
        "Senaryolar": "◫",
        "Raporlar": "▥",
    }

    page = st.radio(
        "Menü",
        list(MENU_ICONS.keys()),
        format_func=lambda item: f"{MENU_ICONS[item]}   {item}",
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("Son Güncelleme")
    st.markdown("**28.08.2026 10:15**")
    st.success("● Tüm sistemler normal")

# =========================================================
# BAŞLIK
# =========================================================

PAGE_TITLES = {
    "Dashboard": (
        "Doğu Karadeniz ATM Nakit Yönetimi Karar Destek Sistemi",
        "VakıfBank – Bölgesel Operasyon Paneli",
    ),
    "ATM İzleme": (
        "ATM İzleme ve Operasyon Takibi",
        "ATM bazlı nakit seviyesi, durum ve ikmal görünümü",
    ),
    "Talep Tahmini": (
        "Nakit Talep Tahmini",
        "Bölge ve ATM bazlı kısa dönem talep öngörüsü",
    ),
    "Kritik Önceliklendirme": (
        "Kritik ATM Önceliklendirme",
        "Çok kriterli risk skoru ile müdahale sıralaması",
    ),
    "Nakit & İkmal Optimizasyonu": (
        "Nakit & İkmal Optimizasyonu",
        "Hedef nakit, R-Q ikmal politikası ve maliyet dengesi",
    ),
    "Rota Planlama": (
        "Rota Planlama",
        "İki nokta arasında mesafe, süre ve operasyon maliyeti",
    ),
    "Senaryolar": (
        "Senaryo Analizi",
        "Her il ekibi için maliyet, mesafe ve hizmet seviyesi karşılaştırması",
    ),
    "Raporlar": (
        "Raporlar",
        "Operasyon sonuçlarını özetle ve dışa aktar",
    ),
}

st.markdown(
    compact_html(
        f"""
        <div class="app-header">
            <div class="app-header-left">
                <div class="menu-square">☰</div>
                <div>
                    <div class="app-title">{PAGE_TITLES[page][0]}</div>
                    <div class="app-subtitle">{PAGE_TITLES[page][1]}</div>
                </div>
            </div>
            <div class="user-area">
                <div class="bell-box">🔔<span class="bell-count">3</span></div>
                <div class="user-avatar">OY</div>
                <div class="user-copy">
                    <strong>Operasyon Yöneticisi</strong>
                    <span>Bölge Operasyon</span>
                </div>
            </div>
        </div>
        """
    ),
    unsafe_allow_html=True,
)


# =========================================================
# 1. DASHBOARD
# =========================================================

if page == "Dashboard":
    with st.container(border=True):
        f1, f2, f3, f4, f5, f6, f7 = st.columns(
            [1.08, 1.00, 1.18, .82, .88, .72, .55]
        )

        with f1:
            region = st.selectbox(
                "Bölge",
                list(SUMMARY.keys()),
                key="dash_region",
            )

        with f2:
            selected_date = st.date_input(
                "Tarih",
                value=date(2026, 8, 28),
                key="dash_date",
            )

        with f3:
            scenario = st.selectbox(
                "Senaryo",
                ["Normal Talep", "Yoğun Talep", "Düşük Talep", "Turizm Sezonu"],
                key="dash_scenario",
            )

        with f4:
            vehicle_count = st.selectbox(
                "Araç Sayısı",
                [4, 5, 6, 7, 8],
                index=2,
                key="dash_vehicle",
            )

        with f5:
            service_level = st.selectbox(
                "Hizmet Seviyesi",
                [90, 95, 98, 99],
                index=1,
                key="dash_service",
            )

        with f6:
            st.write("")
            st.button(
                "Filtreleri Temizle",
                key="dash_reset",
                on_click=reset_dashboard_filters,
            )

        with f7:
            st.write("")
            st.button(
                "Uygula",
                key="dash_apply",
                type="primary",
                width="stretch",
            )

    factor = scenario_factor(scenario)
    base = SUMMARY[region]
    filtered = region_df(region)

    total_atm = base["atm"]
    refill_count = max(1, round(base["refill"] * factor))
    critical_count = max(
        1,
        round(
            base["critical"]
            * (1 + max(0, factor - 1) * .8)
        ),
    )
    demand = base["demand"] * factor

    route_eff = round(
        base["eff"]
        + (vehicle_count - 6) * 1.1
        + (service_level - 95) * .18
        - max(0, factor - 1) * 16
    )
    route_eff = max(75, min(95, route_eff))

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(
            kpi_html(
                "blue",
                "ATM",
                "Toplam ATM",
                f"{total_atm}",
                "5 il genelinde" if region == "Doğu Karadeniz" else f"{region} bölgesi",
            ),
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            kpi_html(
                "green",
                "₺",
                "Bugün İkmal Gereken",
                f"{refill_count}",
                "↓ %14,7 önceki güne göre",
                "kpi-good",
            ),
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            kpi_html(
                "red",
                "!",
                "Kritik ATM",
                f"{critical_count}",
                "↑ %4,2 risk artışı",
                "kpi-bad",
            ),
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            kpi_html(
                "purple",
                "▥",
                "Tahmini Nakit Talebi",
                fmt_m(demand),
                "24 saatlik tahmin",
            ),
            unsafe_allow_html=True,
        )

    with k5:
        st.markdown(
            kpi_html(
                "cyan",
                "↗",
                "Rota Verimliliği",
                f"%{route_eff}",
                f"Hedef: %{service_level}",
            ),
            unsafe_allow_html=True,
        )

    st.write("")

    left, right = st.columns([1.62, 1])

    with left:
        with st.container(border=True):
            st.subheader("Doğu Karadeniz ATM Dağılımı ve Kritiklik")
            st.caption("🔴 Yüksek · 🟠 Orta · 🟢 Düşük")

            safe_plotly_chart(
                map_fig(filtered, height=455)
            )

    with right:
        with st.container(border=True):
            st.subheader("Bugünkü Optimum Rotalar")
            st.caption(f"{vehicle_count} araçlı operasyon senaryosu")

            route_factor = max(.85, min(1.18, 6 / vehicle_count))

            route_cards = [
                (
                    "Rota 1 – TRB-01",
                    "34 AAF 123",
                    round(286 * route_factor),
                    f"{round(286 * route_factor / 48, 1)} sa",
                    6420 * route_factor,
                    "Trabzon Merkez → Akçaabat → Vakfıkebir → Rize Merkez → Ardeşen",
                    "#4d9cff",
                ),
                (
                    "Rota 2 – GRS-01",
                    "61 AAC 456",
                    round(312 * route_factor),
                    f"{round(312 * route_factor / 48, 1)} sa",
                    6980 * route_factor,
                    "Giresun Merkez → Bulancak → Espiye → Tirebolu → Görele",
                    "#45c86a",
                ),
                (
                    "Rota 3 – ORD-01",
                    "52 ABB 789",
                    round(278 * route_factor),
                    f"{round(278 * route_factor / 48, 1)} sa",
                    6150 * route_factor,
                    "Ordu Merkez → Perşembe → Fatsa → Ünye",
                    "#ffbf00",
                ),
            ]

            for item in route_cards:
                st.markdown(
                    route_card_html(*item),
                    unsafe_allow_html=True,
                )

    st.write("")

    c1, c2, c3 = st.columns([1, 1.45, 1])

    with c1:
        with st.container(border=True):
            st.subheader("7 Günlük Nakit Talep Tahmini")

            curve = np.array([1.00, 1.045, .965, .938, .994, 1.065, 1.00])
            vals = demand * curve

            labels = [
                (selected_date + timedelta(days=i)).strftime("%d.%m")
                for i in range(7)
            ]

            safe_plotly_chart(
                demand_line_chart(vals, labels, height=310)
            )

    with c2:
        with st.container(border=True):
            st.subheader("ATM Kritiklik ve Önerilen Nakit")

            table = filtered.copy()
            table["Ayarlı Tahmin"] = table["24s Tahmin"] * factor
            table["Önerilen İkmal"] = (
                (table["Ayarlı Tahmin"] - table["Mevcut Nakit"])
                .clip(lower=0)
                * 1.15
            ).round()

            table["_risk"] = table["Kritiklik"].map(RISK_SCORE)
            table = table.sort_values(
                ["_risk", "Ayarlı Tahmin"],
                ascending=[False, False],
            )

            show = table[
                [
                    "ATM Kodu",
                    "İl",
                    "İlçe",
                    "Mevcut Nakit",
                    "Ayarlı Tahmin",
                    "Kritiklik",
                    "Önerilen İkmal",
                ]
            ].rename(columns={"Ayarlı Tahmin": "24s Tahmin"})

            st.dataframe(
                show,
                hide_index=True,
                height=310,
            )

    with c3:
        with st.container(border=True):
            st.subheader("Operasyon Uyarıları")

            risky = filtered[filtered["Kritiklik"] != "Düşük"]

            if risky.empty:
                st.success("Aktif kritik uyarı yok.")
            else:
                for _, row in risky.head(4).iterrows():
                    if row["Kritiklik"] == "Yüksek":
                        st.error(
                            f"**{row['İl']} / {row['İlçe']} — {row['ATM Kodu']}**\n\n"
                            "Kritik nakit seviyesine yaklaşıyor."
                        )
                    else:
                        st.warning(
                            f"**{row['İl']} / {row['İlçe']} — {row['ATM Kodu']}**\n\n"
                            "İkmal planı gözden geçirilmeli."
                        )


    # -----------------------------------------------------
    # DASHBOARD - İL PERFORMANS KARŞILAŞTIRMASI
    # -----------------------------------------------------

    st.write("")

    with st.container(border=True):
        st.subheader("İl Bazlı Operasyon Performansı")
        st.caption(
            "Her il ayrı operasyon ekibi olarak değerlendirilmiştir. Aşağıdaki değerler prototip amaçlıdır."
        )

        city_rows = []
        for city_name in ["Trabzon", "Rize", "Ordu", "Giresun", "Artvin"]:
            s = SUMMARY[city_name]
            base_route = CITY_ROUTE_BASE[city_name]
            city_rows.append(
                {
                    "İl": city_name,
                    "ATM": s["atm"],
                    "İkmal Gereken": s["refill"],
                    "Kritik ATM": s["critical"],
                    "Talep (M TL)": s["demand"],
                    "Rota km": base_route["km"],
                    "Rota Maliyeti": base_route["cost"],
                    "Verimlilik %": s["eff"],
                }
            )

        city_perf = pd.DataFrame(city_rows)

        perf_left, perf_right = st.columns([1.4, 1])

        with perf_left:
            st.dataframe(
                city_perf,
                hide_index=True,
                width="stretch",
                height=245,
                column_config={
                    "Talep (M TL)": st.column_config.NumberColumn(format="%.1f"),
                    "Rota Maliyeti": st.column_config.NumberColumn(format="₺ %.0f"),
                },
            )

        with perf_right:
            health = city_perf.copy()
            health["Sağlık Skoru"] = (
                health["Verimlilik %"] * .50
                + (100 - health["Kritik ATM"] / health["ATM"] * 100) * .30
                + (100 - health["İkmal Gereken"] / health["ATM"] * 100) * .20
            ).round(1)

            health_fig = go.Figure(
                go.Bar(
                    x=health["İl"],
                    y=health["Sağlık Skoru"],
                    marker=dict(
                        color=health["Sağlık Skoru"],
                        colorscale=[
                            [0, "#ff9d31"],
                            [1, "#45c86a"],
                        ],
                    ),
                    text=health["Sağlık Skoru"],
                    textposition="outside",
                )
            )
            health_fig.update_layout(
                height=245,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                xaxis=dict(showgrid=False, type="category"),
                yaxis=dict(
                    title="Operasyon Sağlık Skoru",
                    range=[0, 100],
                    gridcolor="rgba(255,255,255,.05)",
                ),
                coloraxis_showscale=False,
            )
            safe_plotly_chart(
                health_fig
            )

    with st.container(border=True):
        st.subheader("Bölgesel Risk ve Talep Profili")

        risk_demand_left, risk_demand_right = st.columns(2)

        with risk_demand_left:
            total_risk = (
                ATM["Kritiklik"]
                .value_counts()
                .reindex(["Yüksek", "Orta", "Düşük"], fill_value=0)
                .reset_index()
            )
            total_risk.columns = ["Kritiklik", "ATM Sayısı"]

            risk_pie = px.pie(
                total_risk,
                names="Kritiklik",
                values="ATM Sayısı",
                hole=.58,
                color="Kritiklik",
                color_discrete_map=RISK_COLOR,
            )
            risk_pie.update_layout(
                height=285,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                legend=dict(orientation="h", y=-.05),
            )
            safe_plotly_chart(
                risk_pie
            )

        with risk_demand_right:
            demand_by_city = pd.DataFrame(
                {
                    "İl": ["Trabzon", "Rize", "Ordu", "Giresun", "Artvin"],
                    "Talep": [
                        SUMMARY["Trabzon"]["demand"],
                        SUMMARY["Rize"]["demand"],
                        SUMMARY["Ordu"]["demand"],
                        SUMMARY["Giresun"]["demand"],
                        SUMMARY["Artvin"]["demand"],
                    ],
                }
            )

            demand_city_fig = go.Figure(
                go.Bar(
                    x=demand_by_city["İl"],
                    y=demand_by_city["Talep"],
                    marker_color="#4d9cff",
                    text=np.round(demand_by_city["Talep"], 1),
                    textposition="outside",
                )
            )
            demand_city_fig.update_layout(
                height=285,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                xaxis=dict(showgrid=False, type="category"),
                yaxis=dict(
                    title="Milyon TL",
                    gridcolor="rgba(255,255,255,.05)",
                ),
            )
            safe_plotly_chart(
                demand_city_fig
            )


# =========================================================
# 2. ATM İZLEME
# =========================================================

elif page == "ATM İzleme":
    f1, f2, f3 = st.columns([1, 1, 1.5])

    with f1:
        city = st.selectbox(
            "İl",
            ["Tüm İller", "Trabzon", "Rize", "Ordu", "Giresun", "Artvin"],
            key="monitor_city",
        )

    with f2:
        risk = st.selectbox(
            "Durum",
            ["Tümü", "Yüksek", "Orta", "Düşük"],
            key="monitor_risk",
        )

    with f3:
        search = st.text_input(
            "ATM Ara",
            placeholder="ATM kodu veya ilçe",
            key="monitor_search",
        )

    monitor_df = ATM.copy()

    if city != "Tüm İller":
        monitor_df = monitor_df[monitor_df["İl"] == city]

    if risk != "Tümü":
        monitor_df = monitor_df[monitor_df["Kritiklik"] == risk]

    if search.strip():
        q = search.lower()
        monitor_df = monitor_df[
            monitor_df.apply(
                lambda r: q in (
                    str(r["ATM Kodu"]) + " " + str(r["İlçe"])
                ).lower(),
                axis=1,
            )
        ]

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("İzlenen ATM", len(monitor_df))
    m2.metric(
        "Kritik Durum",
        len(monitor_df[monitor_df["Kritiklik"] == "Yüksek"]),
    )

    if len(monitor_df) > 0:
        avg_fill = (
            monitor_df["Mevcut Nakit"]
            / monitor_df["24s Tahmin"]
            * 100
        ).clip(upper=100).mean()
    else:
        avg_fill = 0

    m3.metric("Ortalama Doluluk", f"%{avg_fill:.0f}")

    refill_today = len(
        monitor_df[
            monitor_df["Mevcut Nakit"]
            < monitor_df["24s Tahmin"] * .70
        ]
    )
    m4.metric("Bugün İkmal", refill_today)

    st.write("")

    left, right = st.columns([1.5, 1])

    with left:
        with st.container(border=True):
            st.subheader("ATM Durum Haritası")

            if len(monitor_df) > 0:
                safe_plotly_chart(
                    map_fig(monitor_df, height=480)
                )
            else:
                st.warning("Filtreye uygun ATM bulunamadı.")

    with right:
        with st.container(border=True):
            st.subheader("ATM Detayı")

            if len(monitor_df) > 0:
                selected_atm = st.selectbox(
                    "ATM Seç",
                    monitor_df["ATM Kodu"].tolist(),
                    key="monitor_selected",
                )

                row = monitor_df[
                    monitor_df["ATM Kodu"] == selected_atm
                ].iloc[0]

                util = min(
                    100,
                    row["Mevcut Nakit"]
                    / row["24s Tahmin"]
                    * 100,
                )

                recommended = max(
                    0,
                    (row["24s Tahmin"] - row["Mevcut Nakit"])
                    * 1.15,
                )

                a, b = st.columns(2)

                a.metric("Mevcut Nakit", fmt_tl(row["Mevcut Nakit"]))
                b.metric("24s Tahmin", fmt_tl(row["24s Tahmin"]))

                a.metric("Doluluk Oranı", f"%{util:.0f}")
                b.metric("Kritiklik", row["Kritiklik"])

                a.metric("Önerilen İkmal", fmt_tl(recommended))
                b.metric(
                    "Sonraki Kontrol",
                    "12:00" if row["Kritiklik"] == "Yüksek" else "16:00",
                )

                hours = ["06", "07", "08", "09", "10", "11"]
                trend = np.linspace(min(100, util + 18), util, 6)

                safe_plotly_chart(
                    demand_line_chart(
                        trend,
                        hours,
                        height=230,
                        y_title="% Doluluk",
                    )
                )

    with st.container(border=True):
        st.subheader("ATM Operasyon Listesi")

        show = monitor_df.copy()

        show["Doluluk %"] = (
            show["Mevcut Nakit"]
            / show["24s Tahmin"]
            * 100
        ).clip(upper=100).round()

        show["Önerilen İkmal"] = (
            (show["24s Tahmin"] - show["Mevcut Nakit"])
            .clip(lower=0)
            * 1.15
        ).round()

        st.dataframe(
            show[
                [
                    "ATM Kodu",
                    "İl",
                    "İlçe",
                    "Mevcut Nakit",
                    "24s Tahmin",
                    "Doluluk %",
                    "Kritiklik",
                    "Önerilen İkmal",
                ]
            ],
            hide_index=True,
            height=360,
        )


    # -----------------------------------------------------
    # ATM İZLEME - EK ANALİTİKLER
    # -----------------------------------------------------

    st.write("")

    trend_col, risk_col = st.columns([1.35, 1])

    with trend_col:
        with st.container(border=True):
            st.subheader("Seçili ATM İçin 24 Saatlik Nakit Seyri")

            if len(monitor_df) > 0:
                selected_for_trend = st.selectbox(
                    "Trend ATM",
                    monitor_df["ATM Kodu"].tolist(),
                    key="monitor_trend_atm",
                )

                trend_row = monitor_df[
                    monitor_df["ATM Kodu"] == selected_for_trend
                ].iloc[0]

                hours_24 = [f"{h:02d}:00" for h in range(24)]
                start_cash = float(trend_row["Mevcut Nakit"] * 1.42)
                end_cash = float(trend_row["Mevcut Nakit"])

                base_curve = np.linspace(start_cash, end_cash, 24)
                intraday_wave = (
                    np.sin(np.linspace(0, 3 * np.pi, 24))
                    * trend_row["24s Tahmin"]
                    * 0.018
                )

                cash_curve = np.maximum(0, base_curve - intraday_wave)

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=hours_24,
                        y=cash_curve,
                        mode="lines",
                        name="Tahmini Kalan Nakit",
                        line=dict(color="#4d9cff", width=3),
                        fill="tozeroy",
                        fillcolor="rgba(77,156,255,.10)",
                    )
                )

                threshold = trend_row["24s Tahmin"] * 0.30
                fig.add_hline(
                    y=threshold,
                    line_dash="dash",
                    line_color="#ff4e57",
                    annotation_text="Kritik eşik",
                    annotation_font_color="#ff8b91",
                )

                fig.update_layout(
                    height=310,
                    margin=dict(l=10, r=10, t=15, b=10),
                    paper_bgcolor="#0f1d2a",
                    plot_bgcolor="#0f1d2a",
                    font=dict(color="#dbe4ec"),
                    xaxis=dict(showgrid=False, type="category"),
                    yaxis=dict(
                        title="TL",
                        gridcolor="rgba(255,255,255,.06)",
                    ),
                    showlegend=False,
                )

                safe_plotly_chart(
                    fig
                )

    with risk_col:
        with st.container(border=True):
            st.subheader("İl Bazlı Risk Dağılımı")

            risk_summary = (
                ATM.groupby(["İl", "Kritiklik"])
                .size()
                .reset_index(name="ATM Sayısı")
            )

            risk_fig = px.bar(
                risk_summary,
                x="İl",
                y="ATM Sayısı",
                color="Kritiklik",
                color_discrete_map=RISK_COLOR,
                barmode="stack",
            )

            risk_fig.update_layout(
                height=310,
                margin=dict(l=10, r=10, t=15, b=10),
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                xaxis=dict(showgrid=False, type="category"),
                yaxis=dict(gridcolor="rgba(255,255,255,.06)"),
                legend=dict(orientation="h", y=1.08, x=0),
            )

            safe_plotly_chart(
                risk_fig
            )

    with st.container(border=True):
        st.subheader("Önerilen İkmal Kuyruğu")

        queue = ATM.copy()
        queue["Nakit Açığı"] = (
            queue["24s Tahmin"] - queue["Mevcut Nakit"]
        ).clip(lower=0)
        queue["Risk Puanı"] = queue["Kritiklik"].map(RISK_SCORE)
        queue["İkmal Önceliği"] = (
            queue["Risk Puanı"] * 100000 + queue["Nakit Açığı"]
        )
        queue = queue.sort_values("İkmal Önceliği", ascending=False)
        queue["Önerilen İkmal"] = (queue["Nakit Açığı"] * 1.15).round()
        queue["Planlama"] = queue["Kritiklik"].map(
            {
                "Yüksek": "İlk rota",
                "Orta": "Bugün",
                "Düşük": "İzle",
            }
        )

        st.dataframe(
            queue[
                [
                    "ATM Kodu",
                    "İl",
                    "İlçe",
                    "Kritiklik",
                    "Nakit Açığı",
                    "Önerilen İkmal",
                    "Planlama",
                ]
            ].head(10),
            hide_index=True,
            height=325,
        )


# =========================================================
# 3. TALEP TAHMİNİ
# =========================================================

elif page == "Talep Tahmini":
    f1, f2, f3, f4 = st.columns([1, 1.5, .8, 1])

    with f1:
        city = st.selectbox(
            "İl",
            list(SUMMARY.keys()),
            key="forecast_city",
        )

    fc_df = region_df(city)

    with f2:
        atm_choice = st.selectbox(
            "ATM / Bölge",
            ["Bölge Toplamı"] + fc_df["ATM Kodu"].tolist(),
            key="forecast_atm",
        )

    with f3:
        horizon = st.selectbox(
            "Tahmin Ufku",
            [7, 14, 30],
            format_func=lambda x: f"{x} Gün",
            key="forecast_horizon",
        )

    with f4:
        fc_scenario = st.selectbox(
            "Senaryo",
            ["Normal Talep", "Yoğun Talep", "Düşük Talep", "Turizm Sezonu"],
            key="forecast_scenario",
        )

    factor = scenario_factor(fc_scenario)

    if atm_choice == "Bölge Toplamı":
        base_daily = SUMMARY[city]["demand"]
    else:
        atm_row = fc_df[fc_df["ATM Kodu"] == atm_choice].iloc[0]
        base_daily = atm_row["24s Tahmin"] / 1_000_000

    labels, values, upper, lower = [], [], [], []

    for i in range(horizon):
        dt = date(2026, 8, 28) + timedelta(days=i)
        labels.append(dt.strftime("%d.%m"))

        wave = 1 + .055 * math.sin(i * .85) + .025 * math.cos(i * .33)
        value = base_daily * factor * wave

        values.append(value)
        upper.append(value * 1.10)
        lower.append(value * .90)

    total_forecast = sum(values)
    avg_forecast = total_forecast / horizon
    peak_value = max(values)
    peak_index = values.index(peak_value)
    std = np.std(values)
    cv = std / avg_forecast * 100 if avg_forecast else 0

    a, b, c, d = st.columns(4)

    a.metric("Toplam Tahmin", fmt_m(total_forecast))
    b.metric("Günlük Ortalama", fmt_m(avg_forecast))
    c.metric("Pik Gün", labels[peak_index], fmt_m(peak_value))
    d.metric(
        "Tahmin Değişkenliği",
        f"%{cv:.1f}".replace(".", ","),
    )

    st.write("")

    left, right = st.columns([1.55, 1])

    with left:
        with st.container(border=True):
            st.subheader("Nakit Talep Tahmini ve Güven Aralığı")

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=labels,
                    y=upper,
                    mode="lines",
                    line=dict(width=0),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=labels,
                    y=lower,
                    mode="lines",
                    line=dict(width=0),
                    fill="tonexty",
                    fillcolor="rgba(77,156,255,.12)",
                    name="Güven Aralığı",
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=labels,
                    y=values,
                    mode="lines+markers",
                    line=dict(color="#4d9cff", width=3),
                    marker=dict(size=6),
                    name="Tahmin",
                )
            )

            fig.update_layout(
                height=430,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                xaxis=dict(showgrid=False, type="category"),
                yaxis=dict(
                    title="Milyon TL",
                    gridcolor="rgba(255,255,255,.06)",
                ),
            )

            safe_plotly_chart(
                fig
            )

    with right:
        with st.container(border=True):
            st.subheader("Tahmin Özeti")

            st.info(
                f"**{horizon} günlük tahmin hazırlandı.**\n\n"
                f"Pik talep **{labels[peak_index]}** tarihinde yaklaşık "
                f"**{fmt_m(peak_value)}** seviyesinde bekleniyor."
            )

            if cv > 10:
                st.warning(
                    "Talep değişkenliği yüksek. Güvenlik stoğu artırılabilir."
                )
            else:
                st.success(
                    "Talep değişkenliği kontrol altında. Standart güvenlik stoğu yeterli."
                )

            st.metric("Senaryo", fc_scenario)
            st.metric("Tahmin Alt Bandı", fmt_m(min(lower)))
            st.metric("Tahmin Üst Bandı", fmt_m(max(upper)))


    # -----------------------------------------------------
    # TALEP TAHMİNİ - MODEL KARŞILAŞTIRMA / DESEN ANALİZİ
    # -----------------------------------------------------

    st.write("")

    model_col, pattern_col = st.columns([1.15, 1])

    with model_col:
        with st.container(border=True):
            st.subheader("Tahmin Modeli Karşılaştırması")
            st.caption(
                "Aşağıdaki hata metrikleri prototip amaçlı temsili model performans değerleridir."
            )

            model_metrics = pd.DataFrame(
                [
                    ["Hareketli Ortalama", 9.8, 12.4, 0.8],
                    ["Holt-Winters", 7.1, 9.2, -0.4],
                    ["SARIMA", 6.4, 8.5, 0.2],
                ],
                columns=["Model", "MAPE %", "RMSE", "Bias %"],
            )

            model_metrics["Öneri"] = model_metrics["MAPE %"].apply(
                lambda x: "Tercih" if x == model_metrics["MAPE %"].min() else "Alternatif"
            )

            st.dataframe(
                model_metrics,
                hide_index=True,
                height=185,
            )

            best_model = model_metrics.sort_values("MAPE %").iloc[0]
            st.success(
                f"Prototip model seçimine göre **{best_model['Model']}** "
                f"en düşük MAPE değerine (%{best_model['MAPE %']}) sahip."
            )

    with pattern_col:
        with st.container(border=True):
            st.subheader("Haftalık Talep Deseni")

            day_names = [
                "Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"
            ]
            day_factors = np.array([0.94, 0.97, 1.00, 1.03, 1.10, 1.07, 0.89])
            profile = base_daily * factor * day_factors

            day_fig = go.Figure(
                go.Bar(
                    x=day_names,
                    y=profile,
                    marker_color="#4d9cff",
                )
            )
            day_fig.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                xaxis=dict(showgrid=False, type="category"),
                yaxis=dict(
                    title="Milyon TL",
                    gridcolor="rgba(255,255,255,.06)",
                ),
            )
            safe_plotly_chart(
                day_fig
            )

    with st.container(border=True):
        st.subheader("Tahmin → Operasyon Dönüşümü")

        conversion = pd.DataFrame(
            {
                "Tarih": labels,
                "Tahmin": np.round(values, 2),
                "Güvenli Üst Seviye": np.round(upper, 2),
            }
        )
        conversion["Planlama Kararı"] = conversion["Tahmin"].apply(
            lambda x: (
                "Ek araç / ek nakit değerlendir"
                if x >= avg_forecast * 1.05
                else "Standart operasyon"
                if x >= avg_forecast * 0.95
                else "Düşük yoğunluk"
            )
        )

        st.dataframe(
            conversion,
            hide_index=True,
            height=280,
        )


# =========================================================
# 4. KRİTİK ÖNCELİKLENDİRME
# =========================================================

elif page == "Kritik Önceliklendirme":
    st.caption(
        "Ağırlıkları değiştirerek ATM öncelik sıralamasını yeniden hesaplayabilirsin."
    )

    w1, w2, w3 = st.columns(3)

    with w1:
        cash_weight = st.slider(
            "Nakit Tükenme Riski",
            min_value=0,
            max_value=100,
            value=50,
        )

    with w2:
        demand_weight = st.slider(
            "Talep Yoğunluğu",
            min_value=0,
            max_value=100,
            value=30,
        )

    with w3:
        impact_weight = st.slider(
            "Operasyonel Etki",
            min_value=0,
            max_value=100,
            value=20,
        )

    total_weight = max(1, cash_weight + demand_weight + impact_weight)

    critical_df = ATM.copy()
    max_forecast = critical_df["24s Tahmin"].max()

    critical_df["Nakit Açığı"] = (
        (
            critical_df["24s Tahmin"]
            - critical_df["Mevcut Nakit"]
        )
        / critical_df["24s Tahmin"]
    ).clip(lower=0)

    critical_df["Talep Yoğunluğu"] = (
        critical_df["24s Tahmin"]
        / max_forecast
    )

    critical_df["Risk Skoru"] = (
        100
        * (
            cash_weight * critical_df["Nakit Açığı"]
            + demand_weight * critical_df["Talep Yoğunluğu"]
            + impact_weight * critical_df["Operasyon Etkisi"]
        )
        / total_weight
    ).round(1)

    critical_df = critical_df.sort_values(
        "Risk Skoru",
        ascending=False,
    ).reset_index(drop=True)

    top = critical_df.iloc[0]

    urgent = len(
        critical_df[
            critical_df["Risk Skoru"] >= 70
        ]
    )

    watch = len(
        critical_df[
            (critical_df["Risk Skoru"] >= 40)
            & (critical_df["Risk Skoru"] < 70)
        ]
    )

    avg_score = critical_df["Risk Skoru"].mean()

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "1. Öncelik",
        top["ATM Kodu"],
        f"{top['İl']} / {top['İlçe']}",
    )
    k2.metric("Acil İkmal", urgent)
    k3.metric("Ortalama Risk Skoru", f"{avg_score:.0f}")
    k4.metric("İzleme Gereken", watch)

    critical_df["Önerilen Aksiyon"] = critical_df["Risk Skoru"].apply(
        lambda x: (
            "Acil İkmal"
            if x >= 70
            else "Bugün Planla"
            if x >= 40
            else "İzle"
        )
    )

    critical_df["Nakit Açığı %"] = (
        critical_df["Nakit Açığı"] * 100
    ).round()

    critical_df["Talep Yoğunluğu %"] = (
        critical_df["Talep Yoğunluğu"] * 100
    ).round()

    critical_df["Operasyon Etkisi %"] = (
        critical_df["Operasyon Etkisi"] * 100
    ).round()

    st.dataframe(
        critical_df[
            [
                "ATM Kodu",
                "İl",
                "İlçe",
                "Risk Skoru",
                "Nakit Açığı %",
                "Talep Yoğunluğu %",
                "Operasyon Etkisi %",
                "Önerilen Aksiyon",
            ]
        ],
        hide_index=True,
        width="stretch",
        height=510,
    )


    # -----------------------------------------------------
    # KRİTİKLİK - GÖRSEL SIRALAMA VE DUYARLILIK
    # -----------------------------------------------------

    st.write("")

    rank_col, sens_col = st.columns([1.25, 1])

    with rank_col:
        with st.container(border=True):
            st.subheader("En Kritik 10 ATM")

            top10 = critical_df.head(10).sort_values("Risk Skoru")
            rank_fig = go.Figure(
                go.Bar(
                    x=top10["Risk Skoru"],
                    y=top10["ATM Kodu"],
                    orientation="h",
                    marker=dict(
                        color=top10["Risk Skoru"],
                        colorscale=[
                            [0, "#ffbf00"],
                            [1, "#ff4e57"],
                        ],
                    ),
                )
            )
            rank_fig.update_layout(
                height=390,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                xaxis=dict(
                    title="Risk Skoru",
                    gridcolor="rgba(255,255,255,.06)",
                    range=[0, 100],
                ),
                yaxis=dict(showgrid=False),
                coloraxis_showscale=False,
            )
            safe_plotly_chart(
                rank_fig
            )

    with sens_col:
        with st.container(border=True):
            st.subheader("Ağırlık Duyarlılık Analizi")
            st.caption(
                "Nakit tükenme ağırlığı değiştiğinde ilk sıradaki ATM'nin skor hareketi."
            )

            sensitivity_rows = []
            for cw in [20, 30, 40, 50, 60, 70, 80]:
                remaining = 100 - cw
                dw = remaining * 0.60
                iw = remaining * 0.40

                temp = ATM.copy()
                temp_gap = (
                    (temp["24s Tahmin"] - temp["Mevcut Nakit"])
                    / temp["24s Tahmin"]
                ).clip(lower=0)
                temp_demand = temp["24s Tahmin"] / max_forecast

                temp["Skor"] = 100 * (
                    cw * temp_gap
                    + dw * temp_demand
                    + iw * temp["Operasyon Etkisi"]
                ) / 100

                winner = temp.sort_values("Skor", ascending=False).iloc[0]
                sensitivity_rows.append(
                    [cw, winner["ATM Kodu"], winner["Skor"]]
                )

            sensitivity = pd.DataFrame(
                sensitivity_rows,
                columns=["Nakit Ağırlığı %", "1. Öncelik", "Skor"],
            )

            sens_fig = go.Figure(
                go.Scatter(
                    x=sensitivity["Nakit Ağırlığı %"],
                    y=sensitivity["Skor"],
                    mode="lines+markers+text",
                    text=sensitivity["1. Öncelik"],
                    textposition="top center",
                    line=dict(color="#ffbf00", width=3),
                    marker=dict(size=8),
                )
            )
            sens_fig.update_layout(
                height=330,
                margin=dict(l=10, r=10, t=20, b=10),
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                xaxis=dict(showgrid=False, type="category"),
                yaxis=dict(
                    title="En Yüksek Skor",
                    gridcolor="rgba(255,255,255,.06)",
                    range=[0, 100],
                ),
            )
            safe_plotly_chart(
                sens_fig
            )


# =========================================================
# 5. NAKİT & İKMAL OPTİMİZASYONU
# =========================================================

elif page == "Nakit & İkmal Optimizasyonu":
    f1, f2, f3, f4 = st.columns(4)

    with f1:
        cash_city = st.selectbox(
            "İl",
            ["Trabzon", "Rize", "Ordu", "Giresun", "Artvin"],
            key="cash_city",
        )

    cash_df = ATM[ATM["İl"] == cash_city].copy()

    with f2:
        cash_atm = st.selectbox(
            "ATM",
            cash_df["ATM Kodu"].tolist(),
            key="cash_atm",
        )

    with f3:
        cash_service = st.selectbox(
            "Hizmet Seviyesi",
            [90, 95, 98, 99],
            index=1,
            key="cash_service",
        )

    with f4:
        cash_days = st.selectbox(
            "Planlama Ufku",
            [1, 2, 3],
            format_func=lambda x: f"{x} Gün",
            key="cash_days",
        )

    row = cash_df[cash_df["ATM Kodu"] == cash_atm].iloc[0]

    st.write("")

    # -----------------------------------------------------
    # TÜM ALT SEKME HESAPLARINDA ORTAK PARAMETRELER
    # -----------------------------------------------------
    with st.expander("⚙️ Ortak Nakit ve Maliyet Parametreleri", expanded=False):
        st.caption(
            "Bu parametreler hedef nakit, R-Q politikası ve maliyet analizinde ortak kullanılır. "
            "Değerler prototip amaçlıdır ve gerçek banka verisiyle değiştirilebilir."
        )

        cp1, cp2, cp3, cp4 = st.columns(4)

        with cp1:
            uncertainty = st.slider(
                "Talep Belirsizliği (%)",
                5,
                30,
                12,
                key="cash_uncertainty",
                help="Güvenlik nakdi ve R yeniden sipariş noktası hesabında kullanılır.",
            )

        with cp2:
            holding_rate = st.number_input(
                "Günlük taşıma maliyeti (%)",
                min_value=0.01,
                max_value=2.00,
                value=0.08,
                step=0.01,
                key="cash_holding_rate",
                help="ATM'de tutulan nakdin günlük fırsat/taşıma maliyeti oranı.",
            )

        with cp3:
            fixed_refill_cost = st.number_input(
                "İkmal başına sabit maliyet (TL)",
                min_value=1.0,
                max_value=50000.0,
                value=900.0,
                step=100.0,
                key="cash_fixed_refill_cost",
                help="Q hesabındaki sipariş/ikmal maliyetini temsil eder.",
            )

        with cp4:
            stock_penalty = st.number_input(
                "Nakitsiz kalma ceza maliyeti (TL)",
                min_value=0.0,
                max_value=100000.0,
                value=5000.0,
                step=500.0,
                key="cash_stock_penalty",
            )

    z_value = {
        90: 1.28,
        95: 1.645,
        98: 2.05,
        99: 2.33,
    }[cash_service]

    daily_demand = float(row["24s Tahmin"])
    demand_needed = daily_demand * cash_days
    safety_stock = demand_needed * (uncertainty / 100) * z_value
    service_target_cash = demand_needed + safety_stock
    refill_amount = max(0.0, service_target_cash - float(row["Mevcut Nakit"]))

    risk_before = min(
        99,
        max(
            1,
            100 * (1 - float(row["Mevcut Nakit"]) / max(1, demand_needed)),
        ),
    )
    risk_after = 100 - cash_service

    tab_target, tab_rq, tab_cost, tab_monte = st.tabs(
        ["💵 Hedef Nakit", "🔁 R-Q İkmal Politikası", "📊 Maliyet Analizi", "🎲 Monte Carlo Risk Analizi"]
    )

    # -----------------------------------------------------
    # SEKME 1 - HEDEF NAKİT
    # -----------------------------------------------------
    with tab_target:
        st.caption(
            "Talep tahmini, hizmet seviyesi ve belirsizlik dikkate alınarak ATM için hedef nakit seviyesi hesaplanır."
        )

        left, right = st.columns([1.25, 1])

        with left:
            with st.container(border=True):
                st.subheader("Önerilen Nakit Seviyesi")

                st.metric(
                    "Hizmet Seviyesine Göre Hedef Nakit",
                    fmt_tl(service_target_cash),
                )

                a, b = st.columns(2)
                a.metric("Mevcut Nakit", fmt_tl(row["Mevcut Nakit"]))
                b.metric("Önerilen İkmal", fmt_tl(refill_amount))
                a.metric("İkmal Öncesi Risk", f"%{risk_before:.0f}")
                b.metric("İkmal Sonrası Risk", f"%{risk_after:.0f}")

                st.progress(cash_service / 100)

                st.caption(
                    f"{cash_atm} için {cash_days} günlük talep, "
                    f"%{cash_service} hizmet seviyesi ve "
                    f"%{uncertainty} talep belirsizliği dikkate alınmıştır."
                )

        with right:
            with st.container(border=True):
                st.subheader("Nakit Yapısı")

                st.metric("Planlama Ufku Talebi", fmt_tl(demand_needed))
                st.metric("Güvenlik Nakdi", fmt_tl(safety_stock))
                st.metric("24 Saatlik Tahmin", fmt_tl(daily_demand))
                st.metric("ATM Kritiklik Sınıfı", str(row["Kritiklik"]))

                coverage_hours = (
                    float(row["Mevcut Nakit"]) / max(1.0, daily_demand / 24.0)
                )
                st.metric("Tahmini Nakit Yeterlilik Süresi", f"{coverage_hours:.1f} saat")

    # -----------------------------------------------------
    # SEKME 2 - R-Q İKMAL POLİTİKASI
    # -----------------------------------------------------
    with tab_rq:
        st.caption(
            "R, ikmal emrinin ne zaman tetikleneceğini; Q ise tetikleme olduğunda önerilen sabit ikmal miktarını gösterir."
        )

        rq_p1, rq_p2, rq_p3 = st.columns(3)

        with rq_p1:
            lead_time_hours = st.number_input(
                "İkmal Lead Time (saat)",
                min_value=1.0,
                max_value=48.0,
                value=8.0,
                step=1.0,
                key="rq_lead_time_hours",
                help="İkmal kararından nakdin ATM'ye ulaşıp kullanılabilir olmasına kadar geçen süre.",
            )

        with rq_p2:
            default_capacity = max(
                150000.0,
                float(row["Mevcut Nakit"]) * 2.0,
                service_target_cash * 1.20,
            )
            atm_capacity = st.number_input(
                "ATM Maksimum Nakit Kapasitesi (TL)",
                min_value=50000.0,
                max_value=1000000.0,
                value=float(round(default_capacity / 1000) * 1000),
                step=10000.0,
                key="rq_atm_capacity",
            )

        with rq_p3:
            operating_days = st.selectbox(
                "Yıllık Planlama Günü",
                [300, 330, 365],
                index=2,
                key="rq_operating_days",
                help="EOQ tipi Q hesabında yıllık talebi ölçeklemek için kullanılır.",
            )

        lead_days = float(lead_time_hours) / 24.0
        lead_demand = daily_demand * lead_days

        # Günlük talep standart sapması için prototip yaklaşımı:
        # tahminin belirsizlik yüzdesi * günlük talep.
        sigma_daily = daily_demand * (uncertainty / 100.0)
        lead_sigma = sigma_daily * math.sqrt(max(lead_days, 1 / 24))
        rq_safety_stock = z_value * lead_sigma

        reorder_point = lead_demand + rq_safety_stock

        annual_demand = daily_demand * operating_days
        annual_holding_cost_per_tl = max(
            0.000001,
            (holding_rate / 100.0) * operating_days,
        )

        raw_q = math.sqrt(
            (2.0 * annual_demand * fixed_refill_cost)
            / annual_holding_cost_per_tl
        )

        # Sipariş geldiğinde ortalama elde güvenlik stoğu kaldığı varsayılır;
        # Q, fiziksel ATM kapasitesini aşmayacak şekilde sınırlandırılır.
        capacity_limited_q = max(0.0, atm_capacity - rq_safety_stock)
        order_quantity = min(raw_q, capacity_limited_q)

        current_cash = float(row["Mevcut Nakit"])
        trigger_order = current_cash <= reorder_point

        hourly_demand = daily_demand / 24.0
        if current_cash > reorder_point:
            hours_to_r = (current_cash - reorder_point) / max(hourly_demand, 1.0)
        else:
            hours_to_r = 0.0

        hours_to_empty = current_cash / max(hourly_demand, 1.0)
        expected_cycle_days = order_quantity / max(daily_demand, 1.0)
        expected_orders_month = (
            (30.0 * daily_demand) / max(order_quantity, 1.0)
            if order_quantity > 0
            else 0.0
        )

        rq1, rq2, rq3, rq4 = st.columns(4)
        rq1.metric("R · Yeniden Sipariş Noktası", fmt_tl(reorder_point))
        rq2.metric("Q · Önerilen İkmal Miktarı", fmt_tl(order_quantity))
        rq3.metric("Mevcut Nakit", fmt_tl(current_cash))
        rq4.metric("Lead Time Talebi", fmt_tl(lead_demand))

        st.write("")

        rq_left, rq_right = st.columns([1.35, 1])

        with rq_left:
            with st.container(border=True):
                st.subheader("R-Q Nakit Seviyesi Görünümü")

                gauge_max = max(atm_capacity, reorder_point * 1.15, current_cash * 1.15)

                rq_fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=current_cash,
                        number={"prefix": "₺", "valueformat": ",.0f"},
                        title={"text": f"{cash_atm} Mevcut Nakit"},
                        gauge={
                            "axis": {"range": [0, gauge_max], "tickcolor": "#dbe4ec"},
                            "bar": {"color": "#4d9cff", "thickness": 0.28},
                            "bgcolor": "#0f1d2a",
                            "borderwidth": 1,
                            "bordercolor": "#263b4d",
                            "steps": [
                                {"range": [0, min(reorder_point, gauge_max)], "color": "rgba(255,78,87,.25)"},
                                {"range": [min(reorder_point, gauge_max), gauge_max], "color": "rgba(69,200,106,.16)"},
                            ],
                            "threshold": {
                                "line": {"color": "#ffbf00", "width": 5},
                                "thickness": 0.8,
                                "value": min(reorder_point, gauge_max),
                            },
                        },
                    )
                )
                rq_fig.update_layout(
                    height=330,
                    margin=dict(l=25, r=25, t=55, b=10),
                    paper_bgcolor="#0f1d2a",
                    font=dict(color="#f7f9fb"),
                )
                safe_plotly_chart(rq_fig)

                st.caption(
                    "Sarı eşik R seviyesidir. Mevcut nakit bu seviyeye indiğinde Q kadar ikmal emri tetiklenir."
                )

        with rq_right:
            with st.container(border=True):
                st.subheader("Politika Kararı")

                st.metric("R İçindeki Güvenlik Stoğu", fmt_tl(rq_safety_stock))
                st.metric("Tahmini Nakit Tükenme Süresi", f"{hours_to_empty:.1f} saat")
                st.metric(
                    "R Seviyesine Kalan Süre",
                    "Eşik aşıldı" if trigger_order else f"{hours_to_r:.1f} saat",
                )
                st.metric("Tahmini Sipariş Döngüsü", f"{expected_cycle_days:.1f} gün")
                st.metric("Tahmini İkmal / Ay", f"{expected_orders_month:.1f}")

                if trigger_order:
                    if current_cash <= reorder_point * 0.75:
                        st.error(
                            f"**Acil ikmal:** Mevcut nakit R seviyesinin belirgin biçimde altında. "
                            f"Yaklaşık **{fmt_tl(order_quantity)}** ikmal öneriliyor."
                        )
                    else:
                        st.warning(
                            f"**İkmal emri oluştur:** Mevcut nakit R = **{fmt_tl(reorder_point)}** "
                            f"seviyesine ulaştı. Q = **{fmt_tl(order_quantity)}** öneriliyor."
                        )
                else:
                    st.success(
                        f"Şu anda ikmal tetiklenmiyor. Mevcut nakit R seviyesinin üzerinde; "
                        f"yaklaşık **{hours_to_r:.1f} saat** sonra yeniden sipariş eşiğine ulaşması bekleniyor."
                    )

        with st.expander("R ve Q nasıl hesaplandı?", expanded=False):
            st.markdown(
                f"""
### R · Yeniden Sipariş Noktası

**Kullanılan formül:**  
**R = d × L + z × σd × √L**

Burada ilk terim **lead time boyunca beklenen talebi**, ikinci terim ise **güvenlik stoğunu** temsil eder.

- Günlük ortalama talep, **d**: **{fmt_tl(daily_demand)} / gün**
- Lead time, **L**: **{lead_time_hours:.0f} saat = {lead_days:.3f} gün**
- Lead time talebi, **d × L**: **{fmt_tl(lead_demand)}**
- Seçilen hizmet seviyesi: **%{cash_service}**
- Hizmet seviyesine karşılık gelen **z**: **{z_value:.3f}**
- Günlük talep standart sapması, **σd**: **{fmt_tl(sigma_daily)}**
- Güvenlik stoğu, **z × σd × √L**: **{fmt_tl(rq_safety_stock)}**
- **Sonuç R = {fmt_tl(reorder_point)}**

> Prototipte σd, geçmiş gerçek ATM verisi olmadığı için günlük talebin seçilen **%{uncertainty} talep belirsizliği** ile yaklaşık olarak hesaplanmaktadır. Gerçek banka verisi geldiğinde σd doğrudan geçmiş talebin standart sapmasından hesaplanabilir.

---

### Q · Önerilen İkmal Miktarı

**Önce ekonomik ikmal miktarı hesaplanır:**  
**Q* = √(2 × D × S / H)**

- Yıllıklaştırılmış talep, **D**: **{fmt_tl(annual_demand)} / yıl**
- İkmal başına sabit operasyon maliyeti, **S**: **{fmt_tl(fixed_refill_cost)}**
- Yıllık elde tutma maliyeti, **H**: **{annual_holding_cost_per_tl:.4f} TL / TL-yıl**
- Ekonomik miktar, **Q***: **{fmt_tl(raw_q)}**

ATM'nin fiziksel nakit kapasitesi nedeniyle Q* doğrudan uygulanmayabilir. Bu nedenle:

**Q = min(Q*, ATM kapasitesi − güvenlik stoğu)**

- ATM maksimum kapasitesi: **{fmt_tl(atm_capacity)}**
- Güvenlik stoğu için ayrılan kapasite: **{fmt_tl(rq_safety_stock)}**
- Kullanılabilir ikmal kapasitesi: **{fmt_tl(capacity_limited_q)}**
- **Sonuç Q = {fmt_tl(order_quantity)}**
                """
            )
            st.caption(
                "R, ikmal emrinin ne zaman tetikleneceğini; Q ise tetikleme olduğunda önerilen ikmal miktarını belirler. Model, klasik sürekli gözden geçirmeli (Q,R) stok politikasının ATM nakit ikmal problemine uyarlanmış prototipidir."
            )

    # -----------------------------------------------------
    # SEKME 3 - MALİYET ANALİZİ
    # -----------------------------------------------------
    with tab_cost:
        st.caption(
            "Hangi maliyet kalemlerinin toplam karara dahil edileceğini seçerek hedef nakit seviyelerinin maliyet etkisini karşılaştırabilirsin."
        )

        with st.expander("💰 Maliyet Kalemlerini Seç", expanded=True):
            cost_c1, cost_c2, cost_c3 = st.columns(3)

            with cost_c1:
                include_holding = st.toggle(
                    "Nakit taşıma maliyeti",
                    value=True,
                    key="cash_include_holding",
                )
                st.caption(f"Günlük oran: %{holding_rate:.2f}")

            with cost_c2:
                include_stockout = st.toggle(
                    "Nakitsiz kalma ceza maliyeti",
                    value=True,
                    key="cash_include_stockout",
                )
                st.caption(f"Ceza katsayısı: {fmt_tl(stock_penalty)}")

            with cost_c3:
                include_refill = st.toggle(
                    "İkmal sabit operasyon maliyeti",
                    value=True,
                    key="cash_include_refill",
                )
                st.caption(f"İkmal başına: {fmt_tl(fixed_refill_cost)}")

        holding_cost = (
            max(0, service_target_cash - demand_needed)
            * holding_rate
            / 100
            * cash_days
            if include_holding
            else 0.0
        )

        stockout_cost = (
            stock_penalty * risk_after / 100
            if include_stockout
            else 0.0
        )

        operation_cost = (
            fixed_refill_cost
            if include_refill and refill_amount > 0
            else 0.0
        )

        total_cost = holding_cost + stockout_cost + operation_cost

        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric(
            "Nakit Taşıma Maliyeti",
            fmt_tl(holding_cost) if include_holding else "Dahil değil",
        )
        mc2.metric(
            "Nakitsiz Kalma Ceza Maliyeti",
            fmt_tl(stockout_cost) if include_stockout else "Dahil değil",
        )
        mc3.metric(
            "İkmal Sabit Maliyeti",
            fmt_tl(operation_cost) if include_refill else "Dahil değil",
        )
        mc4.metric("Toplam Tahmini Maliyet", fmt_tl(total_cost))

        active_cash_costs = []
        if include_holding:
            active_cash_costs.append("Nakit taşıma")
        if include_stockout:
            active_cash_costs.append("Nakitsiz kalma cezası")
        if include_refill:
            active_cash_costs.append("İkmal sabit operasyon")

        st.write("")
        curve_col, service_col = st.columns([1.35, 1])

        with curve_col:
            with st.container(border=True):
                st.subheader("Hedef Nakit Seviyesine Göre Toplam Maliyet")
                st.caption(
                    "Eğri yalnızca aktif ettiğin maliyet kalemlerinden oluşur."
                )

                low_candidate = max(
                    float(row["Mevcut Nakit"]) * 0.75,
                    demand_needed * 0.50,
                )
                high_candidate = max(
                    service_target_cash * 1.35,
                    demand_needed * 1.10,
                )
                candidates = np.linspace(low_candidate, high_candidate, 45)

                candidate_costs = []
                for candidate in candidates:
                    shortage_ratio = max(
                        0,
                        1 - candidate / max(1, demand_needed),
                    )

                    candidate_holding = (
                        max(0, candidate - demand_needed)
                        * holding_rate
                        / 100
                        * cash_days
                        if include_holding
                        else 0.0
                    )

                    candidate_shortage = (
                        stock_penalty * shortage_ratio
                        if include_stockout
                        else 0.0
                    )

                    candidate_refill = (
                        fixed_refill_cost
                        if include_refill and candidate > float(row["Mevcut Nakit"])
                        else 0.0
                    )

                    candidate_costs.append(
                        candidate_holding
                        + candidate_shortage
                        + candidate_refill
                    )

                best_idx = int(np.argmin(candidate_costs))
                best_candidate = float(candidates[best_idx])
                best_cost = float(candidate_costs[best_idx])

                cost_fig = go.Figure()
                cost_fig.add_trace(
                    go.Scatter(
                        x=candidates,
                        y=candidate_costs,
                        mode="lines",
                        line=dict(color="#4d9cff", width=3),
                        name="Seçili Toplam Maliyet",
                    )
                )
                cost_fig.add_trace(
                    go.Scatter(
                        x=[best_candidate],
                        y=[best_cost],
                        mode="markers+text",
                        text=["Minimum"],
                        textposition="top center",
                        marker=dict(size=11, color="#ffbf00"),
                        name="Minimum",
                    )
                )
                cost_fig.add_vline(
                    x=service_target_cash,
                    line_dash="dash",
                    line_color="#45c86a",
                    annotation_text="Hizmet hedefi",
                    annotation_position="top right",
                )
                cost_fig.update_layout(
                    height=360,
                    margin=dict(l=10, r=10, t=15, b=10),
                    paper_bgcolor="#0f1d2a",
                    plot_bgcolor="#0f1d2a",
                    font=dict(color="#dbe4ec"),
                    xaxis=dict(
                        title="Hedef Nakit (TL)",
                        gridcolor="rgba(255,255,255,.04)",
                    ),
                    yaxis=dict(
                        title="Tahmini Maliyet (TL)",
                        gridcolor="rgba(255,255,255,.06)",
                    ),
                    showlegend=False,
                )
                safe_plotly_chart(cost_fig)

                if active_cash_costs:
                    st.success(
                        f"Seçili maliyetlere göre en düşük maliyetli aday seviye yaklaşık "
                        f"**{fmt_tl(best_candidate)}** (maliyet: **{fmt_tl(best_cost)}**)."
                    )
                else:
                    st.info(
                        "Maliyet kalemi seçilmediği için tüm adayların maliyeti 0 TL'dir."
                    )

        with service_col:
            with st.container(border=True):
                st.subheader("Hizmet Seviyesi Karşılaştırması")

                comparison_rows = []
                for srv in [90, 95, 98, 99]:
                    z = {90: 1.28, 95: 1.645, 98: 2.05, 99: 2.33}[srv]
                    temp_target = demand_needed * (1 + (uncertainty / 100) * z)
                    temp_refill = max(
                        0,
                        temp_target - float(row["Mevcut Nakit"]),
                    )

                    temp_hold = (
                        max(0, temp_target - demand_needed)
                        * holding_rate
                        / 100
                        * cash_days
                        if include_holding
                        else 0.0
                    )
                    temp_stock = (
                        stock_penalty * ((100 - srv) / 100)
                        if include_stockout
                        else 0.0
                    )
                    temp_fixed = (
                        fixed_refill_cost
                        if include_refill and temp_refill > 0
                        else 0.0
                    )
                    temp_total = temp_hold + temp_stock + temp_fixed

                    comparison_rows.append(
                        [srv, round(temp_target), round(temp_refill), round(temp_total)]
                    )

                service_compare = pd.DataFrame(
                    comparison_rows,
                    columns=[
                        "Hizmet %",
                        "Hedef Nakit",
                        "İkmal",
                        "Seçili Toplam Maliyet",
                    ],
                )

                st.dataframe(
                    service_compare,
                    hide_index=True,
                    height=230,
                    column_config={
                        "Hedef Nakit": st.column_config.NumberColumn(format="₺ %.0f"),
                        "İkmal": st.column_config.NumberColumn(format="₺ %.0f"),
                        "Seçili Toplam Maliyet": st.column_config.NumberColumn(format="₺ %.0f"),
                    },
                )

                st.info(
                    "Hizmet seviyesi yükseldikçe güvenlik nakdi artar. "
                    "R-Q sekmesi ise bu hedefin yanında ikmalin ne zaman ve ne kadar yapılacağını belirler."
                )


    # -----------------------------------------------------
    # SEKME 4 - MONTE CARLO RİSK ANALİZİ
    # -----------------------------------------------------
    with tab_monte:
        st.caption(
            "R-Q politikasının talep ve lead time belirsizliği altında nasıl davrandığını simülasyonla test eder."
        )

        mc_ctrl1, mc_ctrl2, mc_ctrl3, mc_ctrl4 = st.columns(4)

        with mc_ctrl1:
            sim_count = st.selectbox(
                "Simülasyon Sayısı",
                [1000, 5000, 10000],
                index=1,
                format_func=lambda x: f"{x:,}".replace(",", "."),
                key="mc_sim_count",
            )

        with mc_ctrl2:
            lead_time_variability = st.slider(
                "Lead Time Belirsizliği (%)",
                0,
                40,
                20,
                key="mc_lead_time_variability",
            )

        with mc_ctrl3:
            demand_bias = st.slider(
                "Talep Şoku (%)",
                -20,
                20,
                0,
                key="mc_demand_bias",
                help="Ortalama talebi yukarı/aşağı kaydırarak yoğun gün veya düşük talep etkisini gösterir.",
            )

        with mc_ctrl4:
            seed_value = st.number_input(
                "Rastgelelik Tohumu",
                min_value=1,
                max_value=9999,
                value=42,
                step=1,
                key="mc_seed_value",
            )

        sim_button = st.button(
            "▶ Simülasyonu Çalıştır",
            key="mc_run_button",
            type="primary",
        )

        run_monte_carlo = sim_button or "mc_last_run" not in st.session_state
        if sim_button:
            st.session_state["mc_last_run"] = True

        if run_monte_carlo:
            rng = np.random.default_rng(int(seed_value))

            adjusted_daily_demand = daily_demand * (1 + demand_bias / 100.0)
            demand_std = max(1.0, adjusted_daily_demand * (uncertainty / 100.0))

            sim_lead_hours = np.maximum(
                rng.normal(
                    loc=float(lead_time_hours),
                    scale=max(0.01, float(lead_time_hours) * lead_time_variability / 100.0),
                    size=int(sim_count),
                ),
                0.5,
            )

            sim_daily_demand = np.maximum(
                rng.normal(
                    loc=adjusted_daily_demand,
                    scale=demand_std,
                    size=int(sim_count),
                ),
                0.0,
            )

            sim_lead_demand = sim_daily_demand * (sim_lead_hours / 24.0)
            stockout_before_arrival = sim_lead_demand > reorder_point

            remaining_before_arrival = np.maximum(0.0, reorder_point - sim_lead_demand)
            cash_after_replenishment = np.minimum(
                float(atm_capacity),
                remaining_before_arrival + float(order_quantity),
            )

            sim_post_arrival_demand = np.maximum(
                rng.normal(
                    loc=adjusted_daily_demand * float(cash_days),
                    scale=demand_std * math.sqrt(max(float(cash_days), 1.0)),
                    size=int(sim_count),
                ),
                0.0,
            )

            ending_cash = cash_after_replenishment - sim_post_arrival_demand
            total_stockout = stockout_before_arrival | (ending_cash < 0)

            holding_component = np.maximum(ending_cash, 0.0) * (holding_rate / 100.0) * float(cash_days)
            stockout_component = np.where(
                total_stockout,
                float(stock_penalty) * (1 + np.maximum(-ending_cash, 0.0) / max(adjusted_daily_demand, 1.0)),
                0.0,
            )
            refill_component = np.full(int(sim_count), float(fixed_refill_cost))
            total_costs = holding_component + stockout_component + refill_component

            stockout_prob = float(total_stockout.mean() * 100.0)
            avg_total_cost = float(total_costs.mean())
            safe_cash_need = float(np.quantile(cash_after_replenishment, cash_service / 100.0))
            avg_order_cycle = float(order_quantity / max(adjusted_daily_demand, 1.0))
            avg_order_per_month = float((30.0 * adjusted_daily_demand) / max(order_quantity, 1.0)) if order_quantity > 0 else 0.0

            k1, k2, k3, k4, k5 = st.columns(5)
            k1.metric("Nakitsiz Kalma Olasılığı", f"%{stockout_prob:.1f}")
            k2.metric("Ortalama Toplam Maliyet", fmt_tl(avg_total_cost))
            k3.metric(f"%{cash_service} Güvenli Nakit İhtiyacı", fmt_tl(safe_cash_need))
            k4.metric("Ortalama İkmal Sıklığı", f"{avg_order_per_month:.1f} / ay")
            k5.metric("Önerilen Q ile Çevrim Süresi", f"{avg_order_cycle:.1f} gün")

            st.write("")
            mc_left, mc_right = st.columns([1.2, 1])

            with mc_left:
                with st.container(border=True):
                    st.subheader("Gün Sonu Kalan Nakit Dağılımı")
                    st.caption("Simülasyonların planlama ufku sonundaki kalan nakit dağılımı")

                    hist_cash = go.Figure()
                    hist_cash.add_trace(
                        go.Histogram(
                            x=ending_cash,
                            nbinsx=28,
                            marker=dict(color="#4d9cff"),
                            name="Kalan nakit",
                        )
                    )
                    hist_cash.add_vline(
                        x=0,
                        line_dash="dash",
                        line_color="#ff4e57",
                        annotation_text="0 (Nakitsiz Kalma)",
                        annotation_position="top left",
                    )
                    hist_cash.update_layout(
                        height=360,
                        margin=dict(l=10, r=10, t=15, b=10),
                        paper_bgcolor="#0f1d2a",
                        plot_bgcolor="#0f1d2a",
                        font=dict(color="#dbe4ec"),
                        xaxis=dict(title="Kalan Nakit (TL)", gridcolor="rgba(255,255,255,.04)"),
                        yaxis=dict(title="Frekans", gridcolor="rgba(255,255,255,.06)"),
                        showlegend=False,
                    )
                    safe_plotly_chart(hist_cash)

            with mc_right:
                with st.container(border=True):
                    st.subheader("Toplam Maliyet Dağılımı")
                    st.caption("Simülasyonlarda oluşan toplam maliyet dağılımı")

                    hist_cost = go.Figure()
                    hist_cost.add_trace(
                        go.Histogram(
                            x=total_costs,
                            nbinsx=28,
                            marker=dict(color="#8f75ff"),
                            name="Toplam maliyet",
                        )
                    )
                    hist_cost.add_vline(
                        x=avg_total_cost,
                        line_dash="dash",
                        line_color="#ffbf00",
                        annotation_text=f"Ortalama: {fmt_tl(avg_total_cost)}",
                        annotation_position="top right",
                    )
                    hist_cost.update_layout(
                        height=360,
                        margin=dict(l=10, r=10, t=15, b=10),
                        paper_bgcolor="#0f1d2a",
                        plot_bgcolor="#0f1d2a",
                        font=dict(color="#dbe4ec"),
                        xaxis=dict(title="Toplam Maliyet (TL)", gridcolor="rgba(255,255,255,.04)"),
                        yaxis=dict(title="Frekans", gridcolor="rgba(255,255,255,.06)"),
                        showlegend=False,
                    )
                    safe_plotly_chart(hist_cost)

            st.write("")
            line_col, table_col = st.columns([1.15, 1])

            with line_col:
                with st.container(border=True):
                    st.subheader("R Değeri Senaryo Analizi")
                    st.caption("Farklı R seviyeleri için stokout olasılığı ve maliyet karşılaştırması")

                    r_candidates = [
                        float(reorder_point),
                        float(reorder_point) * 1.05,
                        float(reorder_point) * 1.10,
                        float(reorder_point) * 1.20,
                        float(reorder_point) * 1.30,
                    ]

                    scenario_rows = []
                    for r_value in r_candidates:
                        sim_stockout = sim_lead_demand > r_value
                        sim_remaining = np.maximum(0.0, r_value - sim_lead_demand)
                        sim_cash_after = np.minimum(float(atm_capacity), sim_remaining + float(order_quantity))
                        sim_end = sim_cash_after - sim_post_arrival_demand
                        sim_total_stockout = sim_stockout | (sim_end < 0)

                        sim_holding = np.maximum(sim_end, 0.0) * (holding_rate / 100.0) * float(cash_days)
                        sim_penalty = np.where(
                            sim_total_stockout,
                            float(stock_penalty) * (1 + np.maximum(-sim_end, 0.0) / max(adjusted_daily_demand, 1.0)),
                            0.0,
                        )
                        sim_total_cost = sim_holding + sim_penalty + refill_component

                        scenario_rows.append(
                            [
                                round(r_value),
                                round(float(sim_total_stockout.mean() * 100.0), 1),
                                round(float(sim_total_cost.mean()), 0),
                                round(float(np.quantile(sim_cash_after, cash_service / 100.0)), 0),
                            ]
                        )

                    scenario_df = pd.DataFrame(
                        scenario_rows,
                        columns=[
                            "R Değeri",
                            "Stockout Olasılığı %",
                            "Ortalama Toplam Maliyet",
                            f"%{cash_service} Güvenli Nakit",
                        ],
                    )

                    scenario_fig = go.Figure()
                    scenario_fig.add_trace(
                        go.Scatter(
                            x=scenario_df["R Değeri"],
                            y=scenario_df["Stockout Olasılığı %"],
                            mode="lines+markers",
                            line=dict(color="#ff7a59", width=3),
                            marker=dict(size=8),
                            name="Stockout Olasılığı",
                        )
                    )
                    scenario_fig.update_layout(
                        height=320,
                        margin=dict(l=10, r=10, t=15, b=10),
                        paper_bgcolor="#0f1d2a",
                        plot_bgcolor="#0f1d2a",
                        font=dict(color="#dbe4ec"),
                        xaxis=dict(title="R Değeri (TL)", gridcolor="rgba(255,255,255,.04)"),
                        yaxis=dict(title="Stockout Olasılığı (%)", gridcolor="rgba(255,255,255,.06)"),
                        showlegend=False,
                    )
                    safe_plotly_chart(scenario_fig)

            with table_col:
                with st.container(border=True):
                    st.subheader("R Önerisi")

                    st.dataframe(
                        scenario_df,
                        hide_index=True,
                        height=250,
                        column_config={
                            "R Değeri": st.column_config.NumberColumn(format="₺ %.0f"),
                            "Ortalama Toplam Maliyet": st.column_config.NumberColumn(format="₺ %.0f"),
                            f"%{cash_service} Güvenli Nakit": st.column_config.NumberColumn(format="₺ %.0f"),
                        },
                    )

                    target_stockout_limit = max(1.0, 100.0 - float(cash_service))
                    feasible_rows = scenario_df[scenario_df["Stockout Olasılığı %"] <= target_stockout_limit]

                    if not feasible_rows.empty:
                        recommended_r = float(feasible_rows.iloc[0]["R Değeri"])
                        improvement = max(0.0, stockout_prob - float(feasible_rows.iloc[0]["Stockout Olasılığı %"]))
                        st.success(
                            f"Öneri: Stockout olasılığını **%{target_stockout_limit:.0f}** altına indirmek için "
                            f"R değerinin en az **{fmt_tl(recommended_r)}** olması önerilir. "
                            f"Tahmini iyileşme: **%{improvement:.1f} puan**."
                        )
                    else:
                        st.warning(
                            "Seçilen senaryolarda hedef hizmet seviyesini sağlayan bir R değeri oluşmadı. "
                            "Belirsizliği azaltmak, Q'yu artırmak veya hizmet seviyesini yeniden değerlendirmek gerekebilir."
                        )

                    st.info(
                        f"Bu analizde talep ortalaması **{fmt_tl(adjusted_daily_demand)}**, lead time ortalaması **{lead_time_hours:.1f} saat**, "
                        f"talep belirsizliği **%{uncertainty}**, lead time belirsizliği ise **%{lead_time_variability}** kabul edilmiştir."
                    )

            with st.container(border=True):
                st.subheader("Simülasyon Varsayımları")
                s1, s2, s3, s4 = st.columns(4)
                s1.metric("Talep Dağılımı", "Normal (μ, σ)")
                s2.metric("Lead Time", f"{lead_time_hours:.1f} saat")
                s3.metric("Hedef Hizmet", f"%{cash_service} (z={z_value})")
                s4.metric("Politika", "(Q, R)")

                st.caption(
                    "Not: Bu Monte Carlo bölümü prototip amaçlıdır. Gerçek banka verisi gelirse talep ve lead time dağılımları "
                    "geçmiş operasyon verisinden fit edilerek çok daha gerçekçi sonuçlar üretilebilir."
                )


# =========================================================
# 6. ROTA PLANLAMA
# =========================================================

elif page == "Rota Planlama":
    st.info(
        "Başlangıç ve varış ATM'sini listeden veya haritadaki ATM noktalarından seç. "
        "Mesafe artık kuş uçuşu değildir: OSRM, OpenStreetMap yol ağı üzerinde otomobilin "
        "izleyeceği sürüş rotasını döndürür; km ve süre doğrudan bu rotadan hesaplanır."
    )

    f1, f2, f3 = st.columns([.8, 1.4, 1.4])

    with f1:
        route_city = st.selectbox(
            "Ekip / İl",
            ["Tüm Bölge", "Trabzon", "Rize", "Ordu", "Giresun", "Artvin"],
            key="route_city_osm",
        )

    if route_city == "Tüm Bölge":
        route_df = ATM.copy()
    else:
        route_df = ATM[ATM["İl"] == route_city].copy()

    atm_labels = [
        f"{row['ATM Kodu']} · {row['İl']} / {row['İlçe']}"
        for _, row in route_df.iterrows()
    ]

    atm_codes = route_df["ATM Kodu"].tolist()
    label_by_code = dict(zip(atm_codes, atm_labels))

    if (
        "route_from_osm" not in st.session_state
        or st.session_state["route_from_osm"] not in atm_labels
    ):
        st.session_state["route_from_osm"] = atm_labels[0]

    if (
        "route_to_osm" not in st.session_state
        or st.session_state["route_to_osm"] not in atm_labels
    ):
        st.session_state["route_to_osm"] = (
            atm_labels[1] if len(atm_labels) > 1 else atm_labels[0]
        )

    with f2:
        from_label = st.selectbox(
            "Başlangıç Noktası",
            atm_labels,
            key="route_from_osm",
        )

    with f3:
        to_label = st.selectbox(
            "Varış Noktası",
            atm_labels,
            key="route_to_osm",
        )

    with st.expander("💰 Rota Maliyet Kalemlerini Seç", expanded=True):
        st.caption(
            "Toplam rota maliyeti yalnızca açık olan kalemlerden oluşur. "
            "Böylece yol, işçilik ve ATM ikmal/durak maliyetlerini ayrı ayrı test edebilirsin."
        )

        rc1, rc2, rc3 = st.columns(3)

        with rc1:
            include_route_road = st.toggle(
                "Yol / araç işletme maliyeti",
                value=True,
                key="route_include_road",
            )
            road_cost_per_km = st.number_input(
                "Yol / araç işletme (TL/km)",
                min_value=0.0,
                max_value=250.0,
                value=22.0,
                step=1.0,
                key="route_road_cost_per_km",
                disabled=not include_route_road,
                help="Yakıt, bakım, amortisman ve araç kullanımına bağlı km bazlı temsili gider.",
            )

        with rc2:
            include_route_labor = st.toggle(
                "İşçilik maliyeti",
                value=True,
                key="route_include_labor",
            )
            hourly_worker_cost = st.number_input(
                "İşçilik (TL/saat/çalışan)",
                min_value=0.0,
                max_value=5000.0,
                value=350.0,
                step=25.0,
                key="route_hourly_worker_cost",
                disabled=not include_route_labor,
            )
            crew_size = st.number_input(
                "Araçtaki ekip büyüklüğü",
                min_value=1,
                max_value=8,
                value=2,
                step=1,
                key="route_crew_size",
                disabled=not include_route_labor,
            )

        with rc3:
            include_route_fixed = st.toggle(
                "ATM ikmal / durak sabit maliyeti",
                value=True,
                key="route_include_fixed",
            )
            fixed_stop_cost = st.number_input(
                "ATM başına sabit maliyet (TL)",
                min_value=0.0,
                max_value=25000.0,
                value=450.0,
                step=50.0,
                key="route_fixed_stop_cost",
                disabled=not include_route_fixed,
            )
            service_minutes_per_stop = st.number_input(
                "ATM başına işlem süresi (dk)",
                min_value=0,
                max_value=180,
                value=20,
                step=5,
                key="route_service_minutes",
                help="İşçilik seçiliyse, ATM'deki ikmal/servis süresi toplam çalışma süresine eklenir.",
            )

        active_route_costs = []
        if include_route_road:
            active_route_costs.append("Yol / araç")
        if include_route_labor:
            active_route_costs.append("İşçilik")
        if include_route_fixed:
            active_route_costs.append("ATM sabit işlem")

        if active_route_costs:
            st.success("Toplama dahil: " + " · ".join(active_route_costs))
        else:
            st.warning("Hiçbir maliyet kalemi seçili değil; rota ve süre hesaplanır ancak maliyet 0 TL olur.")

    from_code = atm_codes[atm_labels.index(from_label)]
    to_code = atm_codes[atm_labels.index(to_label)]

    from_row = route_df[route_df["ATM Kodu"] == from_code].iloc[0]
    to_row = route_df[route_df["ATM Kodu"] == to_code].iloc[0]

    if from_code == to_code:
        st.warning("Başlangıç ve varış için farklı iki ATM seç.")
    else:
        with st.spinner("OpenStreetMap / OSRM üzerinden gerçek sürüş rotası hesaplanıyor..."):
            road_route = osrm_route(
                from_row["Lat"],
                from_row["Lon"],
                to_row["Lat"],
                to_row["Lon"],
            )

        if road_route is None:
            st.error(
                "OpenStreetMap / OSRM rota servisine şu anda ulaşılamadı. "
                "İnternet bağlantısını kontrol edip tekrar deneyebilirsin."
            )
        else:
            road_distance = road_route["distance_km"]
            driving_minutes = road_route["duration_min"]

            point_costs = route_cost_breakdown(
                road_distance_km=road_distance,
                driving_minutes=driving_minutes,
                road_cost_per_km=road_cost_per_km,
                hourly_worker_cost=hourly_worker_cost,
                crew_size=crew_size,
                service_minutes=service_minutes_per_stop,
                fixed_stop_cost=fixed_stop_cost,
                service_stop_count=1,
                include_road=include_route_road,
                include_labor=include_route_labor,
                include_fixed_stop=include_route_fixed,
            )

            left, right = st.columns([1.55, 1])

            with left:
                with st.container(border=True):
                    st.subheader("Gerçek OSM Karayolu Rotası")
                    st.caption(
                        "Sarı çizgi, OSRM'nin OpenStreetMap yol ağı üzerinde döndürdüğü "
                        "otomobil sürüş geometrisidir; düz çizgi/kuş uçuşu kullanılmaz."
                    )

                    fig = map_fig(
                        route_df,
                        height=500,
                        selected_codes=[from_code, to_code],
                        line_points=road_route["geometry"],
                    )

                    map_event = st.plotly_chart(
                        fig,
                        use_container_width=True,
                        key="route_interactive_osm_map",
                        on_select="rerun",
                        selection_mode="points",
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                            "scrollZoom": True,
                        },
                    )

                    st.caption(
                        "Kaynak: OpenStreetMap yol verisi + OSRM yönlendirme. "
                        "Bu prototip anlık trafik ve canlı yol kapanmalarını içermez."
                    )

                    selected_map_code = None

                    try:
                        selection = map_event.get("selection", {})
                        selected_points = selection.get("points", [])
                    except Exception:
                        try:
                            selected_points = map_event.selection.points
                        except Exception:
                            selected_points = []

                    if selected_points:
                        last_point = selected_points[-1]

                        try:
                            customdata = last_point.get("customdata", [])
                        except Exception:
                            customdata = getattr(last_point, "customdata", [])

                        if customdata:
                            selected_map_code = customdata[0]

                    if selected_map_code is not None and selected_map_code in label_by_code:
                        st.markdown(f"**Haritada seçilen ATM:** `{selected_map_code}`")

                        map_pick_left, map_pick_right = st.columns(2)

                        with map_pick_left:
                            if st.button(
                                "📍 Başlangıç yap",
                                key="route_map_set_start",
                                width="stretch",
                            ):
                                st.session_state["route_from_osm"] = label_by_code[selected_map_code]
                                st.rerun()

                        with map_pick_right:
                            if st.button(
                                "🏁 Varış yap",
                                key="route_map_set_end",
                                width="stretch",
                            ):
                                st.session_state["route_to_osm"] = label_by_code[selected_map_code]
                                st.rerun()

            with right:
                with st.container(border=True):
                    st.subheader("Rota Özeti")

                    st.markdown(
                        f"**{from_code} → {to_code}**\n\n"
                        f"{from_row['İl']} / {from_row['İlçe']} → "
                        f"{to_row['İl']} / {to_row['İlçe']}"
                    )

                    a, b = st.columns(2)
                    a.metric(
                        "Karayolu Mesafesi",
                        f"{road_distance:.1f} km".replace(".", ","),
                    )
                    b.metric("Sürüş Süresi", f"{driving_minutes:.0f} dk")

                    st.metric(
                        "Operasyon Süresi",
                        f"{point_costs['operation_minutes']:.0f} dk",
                        help="Sürüş + ATM işlem süresi",
                    )

                    st.divider()
                    st.metric("Seçili Toplam Rota Maliyeti", fmt_tl(point_costs["total_cost"]))

                    if from_row["İl"] == to_row["İl"]:
                        st.success(
                            "İki nokta aynı il ekibinde. Tek ekipli ardışık ikmal planı uygundur."
                        )
                    else:
                        st.warning(
                            "İller arası rota seçildi. Ekip sınırı ve görev devri ayrıca değerlendirilmelidir."
                        )

            st.write("")

            # -------------------------------------------------
            # SEÇİLİ ROTA MALİYETLERİ
            # -------------------------------------------------

            with st.container(border=True):
                st.subheader("Seçili Rota Maliyetleri")
                st.caption(
                    "Grafik ve toplam yalnızca üst bölümde aktif ettiğin maliyet kalemlerinden oluşur."
                )

                cost_rows = []
                if include_route_road:
                    cost_rows.append(["Yol / Araç İşletme", point_costs["road_cost"]])
                if include_route_labor:
                    cost_rows.append(["İşçilik", point_costs["labor_cost"]])
                if include_route_fixed:
                    cost_rows.append(["ATM Sabit İşlem", point_costs["fixed_service_cost"]])

                if cost_rows:
                    route_cost_df = pd.DataFrame(cost_rows, columns=["Kalem", "Tutar"])

                    cost_fig = px.bar(
                        route_cost_df,
                        x="Kalem",
                        y="Tutar",
                        text_auto=".0f",
                    )
                    cost_fig.update_layout(
                        height=300,
                        margin=dict(l=10, r=10, t=10, b=10),
                        paper_bgcolor="#0f1d2a",
                        plot_bgcolor="#0f1d2a",
                        font=dict(color="#dbe4ec"),
                        xaxis=dict(showgrid=False, type="category"),
                        yaxis=dict(title="TL", gridcolor="rgba(255,255,255,.06)"),
                        showlegend=False,
                    )
                    safe_plotly_chart(cost_fig)

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Yol", fmt_tl(point_costs["road_cost"]) if include_route_road else "—")
                    m2.metric("İşçilik", fmt_tl(point_costs["labor_cost"]) if include_route_labor else "—")
                    m3.metric("ATM İşlem", fmt_tl(point_costs["fixed_service_cost"]) if include_route_fixed else "—")
                    m4.metric("Toplam", fmt_tl(point_costs["total_cost"]))
                else:
                    st.info("Maliyet kalemi seçilmedi.")

            # -------------------------------------------------
            # OSM SÜRÜŞ MESAFESİ MATRİSİ / YAKIN NOKTALAR
            # -------------------------------------------------

            st.write("")
            matrix_col, nearest_col = st.columns([1.35, 1])
            matrix_source = route_df.head(8).copy().reset_index(drop=True)

            coords_tuple = tuple(
                (float(row["Lat"]), float(row["Lon"]))
                for _, row in matrix_source.iterrows()
            )

            with st.spinner("OSM sürüş mesafesi matrisi hazırlanıyor..."):
                road_table = osrm_table(coords_tuple)

            with matrix_col:
                with st.container(border=True):
                    st.subheader("Karayolu Sürüş Mesafesi Matrisi")
                    st.caption(
                        "Matristeki değerler iki koordinat arasındaki düz mesafe değil; "
                        "OSRM'nin en hızlı otomobil rotalarının yol uzunluklarıdır."
                    )

                    if road_table is None:
                        st.warning("OSM/OSRM mesafe matrisi şu anda alınamadı.")
                    else:
                        codes = matrix_source["ATM Kodu"].tolist()
                        matrix = pd.DataFrame(
                            road_table["distances_km"],
                            index=codes,
                            columns=codes,
                            dtype=float,
                        )

                        matrix_fig = go.Figure(
                            data=go.Heatmap(
                                z=matrix.values,
                                x=matrix.columns,
                                y=matrix.index,
                                colorscale=[
                                    [0, "#102130"],
                                    [0.5, "#4d9cff"],
                                    [1, "#ffbf00"],
                                ],
                                colorbar=dict(title="km"),
                                hovertemplate="%{y} → %{x}<br>%{z:.1f} km<extra></extra>",
                            )
                        )
                        matrix_fig.update_layout(
                            height=390,
                            margin=dict(l=10, r=10, t=10, b=10),
                            paper_bgcolor="#0f1d2a",
                            plot_bgcolor="#0f1d2a",
                            font=dict(color="#dbe4ec", size=9),
                        )
                        safe_plotly_chart(matrix_fig)

            with nearest_col:
                with st.container(border=True):
                    st.subheader("Başlangıç ATM'sine En Yakın Noktalar")
                    st.caption("OSM otomobil sürüş mesafesine göre sıralanır.")

                    if road_table is None:
                        st.warning("Mesafe matrisi alınamadığı için yakın nokta sıralaması oluşturulamadı.")
                    else:
                        codes = matrix_source["ATM Kodu"].tolist()
                        from_index = codes.index(from_code) if from_code in codes else 0
                        nearest_rows = []

                        for candidate_index, candidate in matrix_source.iterrows():
                            if candidate_index == from_index:
                                continue

                            km = road_table["distances_km"][from_index][candidate_index]
                            duration = road_table["durations_min"][from_index][candidate_index]

                            if km is None:
                                continue

                            nearest_rows.append(
                                {
                                    "ATM": candidate["ATM Kodu"],
                                    "İl": candidate["İl"],
                                    "İlçe": candidate["İlçe"],
                                    "OSM Yol km": round(km, 1),
                                    "Sürüş dk": None if duration is None else round(duration),
                                }
                            )

                        nearest_df = pd.DataFrame(nearest_rows)

                        if not nearest_df.empty:
                            nearest_df = nearest_df.sort_values("OSM Yol km").head(6)
                            st.dataframe(nearest_df, hide_index=True, height=265)
                            nearest = nearest_df.iloc[0]
                            st.success(
                                f"{from_code} için OSM yol ağına göre en yakın sonraki durak "
                                f"**{nearest['ATM']}** (~{nearest['OSM Yol km']} km)."
                            )
                        else:
                            st.info("Karşılaştırılabilecek başka ATM bulunamadı.")

            # -------------------------------------------------
            # OSM MATRİSİYLE ARDIŞIK İKMAL SIRASI
            # -------------------------------------------------

            st.write("")

            with st.container(border=True):
                st.subheader("Önerilen Ardışık İkmal Sırası")
                st.caption(
                    "Seçili ekipteki ATM'ler, OSM sürüş mesafesi matrisi üzerinde "
                    "en yakın komşu sezgiseliyle sıralanır. Tur maliyeti de seçili maliyet "
                    "kalemleriyle yeniden hesaplanır."
                )

                return_to_start = st.toggle(
                    "Tur sonunda başlangıç ATM'sine dön",
                    value=True,
                    key="route_return_to_start",
                )

                if road_table is None:
                    st.warning("OSM sürüş matrisi alınamadığı için tur sırası hesaplanamadı.")
                elif len(matrix_source) < 2:
                    st.info("Tur oluşturmak için en az iki ATM gerekir.")
                else:
                    codes = matrix_source["ATM Kodu"].tolist()
                    start_index = codes.index(from_code) if from_code in codes else 0

                    order, legs = nearest_neighbor_order(
                        road_table["distances_km"],
                        start_index=start_index,
                        return_to_start=return_to_start,
                    )

                    sequence_rows = []
                    cumulative_km = 0.0
                    cumulative_drive_min = 0.0

                    for leg_no, (i, j, leg_km) in enumerate(legs, start=1):
                        leg_duration = road_table["durations_min"][i][j]
                        cumulative_km += float(leg_km)
                        if leg_duration is not None:
                            cumulative_drive_min += float(leg_duration)

                        sequence_rows.append(
                            {
                                "Etap": leg_no,
                                "Başlangıç": codes[i],
                                "Varış": codes[j],
                                "OSM Yol km": round(float(leg_km), 1),
                                "Sürüş dk": None if leg_duration is None else round(float(leg_duration)),
                                "Kümülatif km": round(cumulative_km, 1),
                            }
                        )

                    sequence_df = pd.DataFrame(sequence_rows)

                    # Başlangıç noktası depo/ilk ATM kabul edilir; dönüş bacağı hizmet durağı sayılmaz.
                    service_stop_count = max(0, len(order) - 1)
                    total_service_minutes = service_stop_count * service_minutes_per_stop

                    tour_costs = route_cost_breakdown(
                        road_distance_km=cumulative_km,
                        driving_minutes=cumulative_drive_min,
                        road_cost_per_km=road_cost_per_km,
                        hourly_worker_cost=hourly_worker_cost,
                        crew_size=crew_size,
                        service_minutes=total_service_minutes,
                        fixed_stop_cost=fixed_stop_cost,
                        service_stop_count=service_stop_count,
                        include_road=include_route_road,
                        include_labor=include_route_labor,
                        include_fixed_stop=include_route_fixed,
                    )

                    route_seq_cols = st.columns([1.5, 1])

                    with route_seq_cols[0]:
                        st.dataframe(
                            sequence_df,
                            hide_index=True,
                            width="stretch",
                            height=295,
                        )

                    with route_seq_cols[1]:
                        st.metric(
                            "OSM Tur Uzunluğu",
                            f"{cumulative_km:.1f} km".replace(".", ","),
                        )
                        st.metric("Toplam Sürüş Süresi", f"{cumulative_drive_min:.0f} dk")
                        st.metric("Hizmet Durağı", f"{service_stop_count} ATM")
                        st.metric(
                            "Toplam Operasyon Süresi",
                            f"{tour_costs['operation_minutes']:.0f} dk",
                        )
                        st.metric("Seçili Tur Maliyeti", fmt_tl(tour_costs["total_cost"]))

                        st.caption(
                            "Tur maliyeti: seçili yol/araç + işçilik + ATM sabit işlem kalemlerinin toplamıdır."
                        )


# =========================================================
# 7. SENARYOLAR
# =========================================================

elif page == "Senaryolar":
    st.info(
        "Her il ayrı operasyon ekibi olarak değerlendirilir. "
        "Mesafeler OpenStreetMap/OSRM otomobil sürüş yollarından gelir. "
        "Maliyet kalemleri aşağıda birbirinden bağımsız seçilip izlenebilir."
    )

    top1, top2 = st.columns(2)

    with top1:
        scenario_city = st.selectbox(
            "İl / Ekip",
            ["Tüm İller", "Trabzon", "Rize", "Ordu", "Giresun", "Artvin"],
            key="scenario_city_osm",
        )

    with top2:
        objective = st.selectbox(
            "Optimizasyon Hedefi",
            ["Maliyet Minimum", "Mesafe Minimum", "Dengeli"],
            key="scenario_objective_osm",
        )

    with st.expander("💰 Maliyet Türlerini Ayrı Yönet", expanded=True):
        st.caption(
            "Her maliyet kalemi ayrı tutulur. Yol / Araç İşletme her zaman aktiftir; "
            "diğer kalemleri butonlardan açıp kapatabilirsin."
        )

        top_cost_1, top_cost_2, top_cost_3 = st.columns(3)

        with top_cost_1:
            st.markdown("**Yol / Araç İşletme**")
            st.success("● Aktif")
            scenario_road_cost = st.number_input(
                "Yol / araç işletme (TL/km)",
                min_value=1.0,
                max_value=250.0,
                value=22.0,
                step=1.0,
                key="scenario_road_cost",
            )

            include_labor = st.toggle(
                "İşçilik maliyeti",
                value=True,
                key="scenario_include_labor",
            )
            scenario_hourly_worker = st.number_input(
                "İşçilik (TL/saat/çalışan)",
                min_value=0.0,
                max_value=5000.0,
                value=350.0,
                step=25.0,
                key="scenario_hourly_worker",
            )

        with top_cost_2:
            include_accident = st.toggle(
                "İş Kazası / İşgücü Kaybı",
                value=False,
                key="scenario_include_accident",
            )
            scenario_accident_cost = st.number_input(
                "İş kazası / işgücü kaybı (TL/olay)",
                min_value=0.0,
                max_value=1000000.0,
                value=0.0,
                step=1000.0,
                key="scenario_accident_cost",
            )

            include_training = st.toggle(
                "Seminer / Konferans / Eğitim",
                value=False,
                key="scenario_include_training",
            )
            scenario_training_cost = st.number_input(
                "Seminer / konferans / eğitim (TL/kişi)",
                min_value=0.0,
                max_value=100000.0,
                value=0.0,
                step=500.0,
                key="scenario_training_cost",
            )

        with top_cost_3:
            include_lodging = st.toggle(
                "Konaklama / Harcırah",
                value=False,
                key="scenario_include_lodging",
            )
            scenario_lodging_cost = st.number_input(
                "Konaklama / harcırah (TL/kişi-gün)",
                min_value=0.0,
                max_value=100000.0,
                value=0.0,
                step=500.0,
                key="scenario_lodging_cost",
            )

            include_overtime = st.toggle(
                "Fazla Mesai",
                value=False,
                key="scenario_include_overtime",
            )
            scenario_overtime_cost = st.number_input(
                "Fazla mesai (TL/saat/çalışan)",
                min_value=0.0,
                max_value=5000.0,
                value=0.0,
                step=25.0,
                key="scenario_overtime_cost",
            )

        st.divider()

        p1, p2 = st.columns(2)

        with p1:
            scenario_crew_size = st.number_input(
                "Araç başına çalışan",
                min_value=1,
                max_value=10,
                value=2,
                step=1,
                key="scenario_crew_size",
            )

        with p2:
            scenario_service_min = st.number_input(
                "ATM hizmet süresi (dk)",
                min_value=0,
                max_value=120,
                value=15,
                step=5,
                key="scenario_service_min",
            )

    with st.expander("📚 Maliyet Kategorileri", expanded=False):
        st.dataframe(
            COST_CATEGORY_CATALOG,
            hide_index=True,
            width="stretch",
            height=250,
        )

    cities = (
        list(CITY_ROUTE_BASE.keys())
        if scenario_city == "Tüm İller"
        else [scenario_city]
    )

    rows = []
    baseline_notes = []

    with st.spinner("İl ekipleri için OSM/OSRM sürüş bazları hazırlanıyor..."):
        for city in cities:
            osm_base = city_osrm_baseline(city)

            if osm_base is not None and osm_base["distance_km"] > 0:
                base_distance = osm_base["distance_km"]
                base_duration = osm_base["duration_min"]
                stop_count = osm_base["stop_count"]
                source = "OSM/OSRM"
            else:
                # OSRM geçici olarak erişilemezse daha önce tanımlı
                # temsili KARAYOLU operasyon değerleri kullanılır.
                fallback = CITY_ROUTE_BASE[city]
                base_distance = float(fallback["km"])
                base_duration = base_distance / 48 * 60
                stop_count = len(ATM[ATM["İl"] == city])
                source = "Temsili karayolu yedeği"

                baseline_notes.append(
                    f"{city}: OSM servisi alınamadığı için temsili karayolu baz değeri kullanıldı."
                )

            base_vehicle_count = CITY_ROUTE_BASE[city]["vehicles"]

            for _, sc in SCENARIOS.iterrows():
                scenario_name = sc["Senaryo"]

                # Senaryo çarpanı OSM sürüş baz mesafesi üzerinde uygulanır.
                # Bu çarpan daha sık/seyrek ikmal, ek ziyaret ve servis
                # yoğunluğunu temsil eden prototip varsayımıdır.
                distance_factor = float(sc["Mesafe Çarpanı"])

                distance = base_distance * distance_factor
                drive_minutes = base_duration * distance_factor

                vehicles = max(
                    1,
                    int(base_vehicle_count + sc["Araç Farkı"]),
                )

                # Hizmet süresi tüm temsili ATM durakları için eklenir.
                service_minutes = (
                    stop_count
                    * scenario_service_min
                )

                operation_hours = (
                    drive_minutes
                    + service_minutes
                ) / 60.0

                road_cost = (
                    distance
                    * scenario_road_cost
                )

                labor_cost = (
                    operation_hours
                    * scenario_crew_size
                    * scenario_hourly_worker
                    if include_labor
                    else 0.0
                )

                accident_cost = (
                    scenario_accident_cost
                    * (float(sc["Risk"]) / 100.0)
                    if include_accident
                    else 0.0
                )

                training_cost = (
                    scenario_training_cost
                    * scenario_crew_size
                    if include_training
                    else 0.0
                )

                lodging_cost = (
                    scenario_lodging_cost
                    * scenario_crew_size
                    if include_lodging
                    else 0.0
                )

                overtime_hours = max(
                    0.0,
                    operation_hours - 8.0,
                )

                overtime_cost = (
                    overtime_hours
                    * scenario_crew_size
                    * scenario_overtime_cost
                    if include_overtime
                    else 0.0
                )

                total_cost = (
                    road_cost
                    + labor_cost
                    + accident_cost
                    + training_cost
                    + lodging_cost
                    + overtime_cost
                )

                if objective == "Maliyet Minimum":
                    score = total_cost

                elif objective == "Mesafe Minimum":
                    score = distance

                else:
                    # Dengeli hedef:
                    # %50 normalize maliyet + %30 normalize mesafe
                    # + %20 operasyonel risk
                    normalized_cost = (
                        total_cost
                        / max(1, base_distance * scenario_road_cost)
                    )

                    normalized_distance = (
                        distance
                        / max(1, base_distance)
                    )

                    score = (
                        normalized_cost * .50
                        + normalized_distance * .30
                        + (float(sc["Risk"]) / 100) * .20
                    )

                rows.append(
                    {
                        "İl": city,
                        "Senaryo": scenario_name,
                        "Araç": vehicles,
                        "Baz Kaynak": source,
                        "OSM Baz km": round(base_distance, 1),
                        "Toplam Mesafe": round(distance, 1),
                        "Sürüş Süresi dk": round(drive_minutes),
                        "Yol Maliyeti": round(road_cost),
                        "İşçilik Maliyeti": round(labor_cost),
                        "İş Kazası / İşgücü Kaybı": round(accident_cost),
                        "Seminer / Konferans / Eğitim": round(training_cost),
                        "Konaklama / Harcırah": round(lodging_cost),
                        "Fazla Mesai": round(overtime_cost),
                        "Toplam Maliyet": round(total_cost),
                        "Hizmet Seviyesi": int(sc["Hizmet Seviyesi"]),
                        "Risk": int(sc["Risk"]),
                        "_score": float(score),
                    }
                )

    scenario_result = pd.DataFrame(rows)

    if baseline_notes:
        with st.expander("OSM bağlantı notları", expanded=False):
            for note in baseline_notes:
                st.warning(note)

    best_rows = []

    for city in cities:
        city_rows = scenario_result[
            scenario_result["İl"] == city
        ]

        best_index = city_rows["_score"].idxmin()
        best_rows.append(scenario_result.loc[best_index])

    st.subheader("Her İl İçin Önerilen Senaryo")

    best_cols = st.columns(len(best_rows))

    for col, row in zip(best_cols, best_rows):
        with col:
            with st.container(border=True):
                st.markdown(f"### {row['İl']}")
                st.markdown(f"**{row['Senaryo']}**")

                st.caption(
                    f"{row['Toplam Mesafe']:.1f} km OSM bazlı\n\n"
                    f"Yol: {fmt_tl(row['Yol Maliyeti'])}\n\n"
                    f"İşçilik: {fmt_tl(row['İşçilik Maliyeti'])}\n\n"
                    f"Toplam: {fmt_tl(row['Toplam Maliyet'])}"
                )

                st.caption(
                    f"{int(row['Araç'])} araç · "
                    f"%{int(row['Hizmet Seviyesi'])} hizmet"
                )

    st.write("")

    left, right = st.columns([1.5, 1])

    with left:
        with st.container(border=True):
            st.subheader("Senaryo Karşılaştırması")
            st.caption(
                "Toplam maliyet yol ve işçilik kalemlerine ayrılmıştır."
            )

            table_show = scenario_result.copy()
            table_show["Karar"] = ""

            for row in best_rows:
                mask = (
                    (table_show["İl"] == row["İl"])
                    & (table_show["Senaryo"] == row["Senaryo"])
                )

                table_show.loc[mask, "Karar"] = "Önerilen"

            table_show["Mesafe"] = (
                table_show["Toplam Mesafe"]
                .map(lambda x: f"{x:.1f} km".replace(".", ","))
            )

            table_show["Yol"] = table_show["Yol Maliyeti"].apply(fmt_tl)
            table_show["İşçilik"] = table_show["İşçilik Maliyeti"].apply(fmt_tl)
            table_show["İş Kazası"] = table_show["İş Kazası / İşgücü Kaybı"].apply(fmt_tl)
            table_show["Eğitim"] = table_show["Seminer / Konferans / Eğitim"].apply(fmt_tl)
            table_show["Konaklama"] = table_show["Konaklama / Harcırah"].apply(fmt_tl)
            table_show["Fazla Mesai"] = table_show["Fazla Mesai"].apply(fmt_tl)
            table_show["Toplam"] = table_show["Toplam Maliyet"].apply(fmt_tl)

            table_show["Hizmet"] = (
                "%"
                + table_show["Hizmet Seviyesi"].astype(str)
            )

            table_show["Risk %"] = (
                "%"
                + table_show["Risk"].astype(str)
            )

            st.dataframe(
                table_show[
                    [
                        "İl",
                        "Senaryo",
                        "Baz Kaynak",
                        "Araç",
                        "Mesafe",
                        "Yol",
                        "İşçilik",
                        "İş Kazası",
                        "Eğitim",
                        "Konaklama",
                        "Fazla Mesai",
                        "Toplam",
                        "Hizmet",
                        "Risk %",
                        "Karar",
                    ]
                ],
                hide_index=True,
                width="stretch",
                height=460,
            )

    with right:
        with st.container(border=True):
            chart_city = st.selectbox(
                "Grafikte gösterilecek il",
                cities,
                key="scenario_chart_city_osm",
            )

            chart_df = scenario_result[
                scenario_result["İl"] == chart_city
            ].copy()

            cost_fig = go.Figure()

            cost_fig.add_trace(
                go.Bar(
                    x=chart_df["Senaryo"],
                    y=chart_df["Yol Maliyeti"],
                    name="Yol Maliyeti",
                    marker_color="#4d9cff",
                )
            )

            cost_fig.add_trace(
                go.Bar(
                    x=chart_df["Senaryo"],
                    y=chart_df["İşçilik Maliyeti"],
                    name="İşçilik Maliyeti",
                    marker_color="#ffbf00",
                )
            )

            if include_accident:
                cost_fig.add_trace(
                    go.Bar(
                        x=chart_df["Senaryo"],
                        y=chart_df["İş Kazası / İşgücü Kaybı"],
                        name="İş Kazası / İşgücü Kaybı",
                        marker_color="#ff6b6b",
                    )
                )

            if include_training:
                cost_fig.add_trace(
                    go.Bar(
                        x=chart_df["Senaryo"],
                        y=chart_df["Seminer / Konferans / Eğitim"],
                        name="Seminer / Konferans / Eğitim",
                        marker_color="#7cdbb5",
                    )
                )

            if include_lodging:
                cost_fig.add_trace(
                    go.Bar(
                        x=chart_df["Senaryo"],
                        y=chart_df["Konaklama / Harcırah"],
                        name="Konaklama / Harcırah",
                        marker_color="#b29cff",
                    )
                )

            if include_overtime:
                cost_fig.add_trace(
                    go.Bar(
                        x=chart_df["Senaryo"],
                        y=chart_df["Fazla Mesai"],
                        name="Fazla Mesai",
                        marker_color="#f09a54",
                    )
                )

            cost_fig.update_layout(
                barmode="stack",
                height=405,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                xaxis=dict(
                    title="Senaryo",
                    showgrid=False,
                    type="category",
                ),
                yaxis=dict(
                    title="Maliyet (TL)",
                    gridcolor="rgba(255,255,255,.06)",
                ),
            )

            safe_plotly_chart(cost_fig)

    # -----------------------------------------------------
    # İL EKİPLERİ TOPLAM PORTFÖYÜ
    # -----------------------------------------------------

    st.write("")

    with st.container(border=True):
        st.subheader("İl Ekipleri İçin Önerilen Operasyon Portföyü")

        portfolio_rows = []

        for best in best_rows:
            portfolio_rows.append(
                {
                    "İl": best["İl"],
                    "Önerilen Senaryo": best["Senaryo"],
                    "Araç": int(best["Araç"]),
                    "OSM / Yol km": round(float(best["Toplam Mesafe"]), 1),
                    "Yol Maliyeti": int(best["Yol Maliyeti"]),
                    "İşçilik Maliyeti": int(best["İşçilik Maliyeti"]),
                    "İş Kazası / İşgücü Kaybı": int(best["İş Kazası / İşgücü Kaybı"]),
                    "Seminer / Konferans / Eğitim": int(best["Seminer / Konferans / Eğitim"]),
                    "Konaklama / Harcırah": int(best["Konaklama / Harcırah"]),
                    "Fazla Mesai": int(best["Fazla Mesai"]),
                    "Toplam Maliyet": int(best["Toplam Maliyet"]),
                    "Hizmet %": int(best["Hizmet Seviyesi"]),
                    "Risk %": int(best["Risk"]),
                }
            )

        portfolio = pd.DataFrame(portfolio_rows)

        p1, p2, p3, p4, p5 = st.columns(5)

        p1.metric(
            "Toplam Araç",
            int(portfolio["Araç"].sum()),
        )

        p2.metric(
            "Toplam OSM Yol",
            f"{portfolio['OSM / Yol km'].sum():.1f} km".replace(".", ","),
        )

        p3.metric(
            "Toplam Yol Maliyeti",
            fmt_tl(portfolio["Yol Maliyeti"].sum()),
        )

        p4.metric(
            "Toplam İşçilik",
            fmt_tl(portfolio["İşçilik Maliyeti"].sum()),
        )

        p5.metric(
            "Toplam Operasyon Maliyeti",
            fmt_tl(portfolio["Toplam Maliyet"].sum()),
        )

        portfolio["Maliyet / km"] = (
            portfolio["Toplam Maliyet"]
            / portfolio["OSM / Yol km"].replace(0, np.nan)
        ).round(1)

        st.dataframe(
            portfolio,
            hide_index=True,
            width="stretch",
            height=245,
        )

    # -----------------------------------------------------
    # PARETO: TOPLAM MALİYET - OSM MESAFE
    # -----------------------------------------------------

    st.write("")

    with st.container(border=True):
        st.subheader("Pareto Görünümü: Toplam Maliyet – OSM Yol Mesafesi")
        st.caption(
            "Sol-alt bölge daha iyidir: daha düşük sürüş mesafesi ve daha düşük toplam maliyet."
        )

        pareto_fig = px.scatter(
            scenario_result,
            x="Toplam Mesafe",
            y="Toplam Maliyet",
            color="İl",
            symbol="Senaryo",
            hover_data=[
                "Yol Maliyeti",
                "İşçilik Maliyeti",
                "Araç",
                "Hizmet Seviyesi",
                "Risk",
            ],
        )

        pareto_fig.update_traces(
            marker=dict(size=11)
        )

        pareto_fig.update_layout(
            height=390,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#0f1d2a",
            plot_bgcolor="#0f1d2a",
            font=dict(color="#dbe4ec"),
            xaxis=dict(
                title="OSM Bazlı Toplam Yol Mesafesi (km)",
                gridcolor="rgba(255,255,255,.05)",
            ),
            yaxis=dict(
                title="Toplam Maliyet (TL)",
                gridcolor="rgba(255,255,255,.05)",
            ),
        )

        safe_plotly_chart(pareto_fig)

    # -----------------------------------------------------
    # ARAÇ SAYISI DUYARLILIK ANALİZİ
    # -----------------------------------------------------

    st.write("")

    with st.container(border=True):
        st.subheader("Araç Sayısı Duyarlılık Analizi")
        st.caption(
            "Bu analizde toplam maliyet yine yalnızca yol ve işçilik kalemlerinden oluşur."
        )

        sensitivity_city = st.selectbox(
            "Duyarlılık için il",
            cities,
            key="scenario_sensitivity_city_osm",
        )

        osm_base = city_osrm_baseline(
            sensitivity_city
        )

        if osm_base is not None and osm_base["distance_km"] > 0:
            sensitivity_base_km = osm_base["distance_km"]
            sensitivity_base_min = osm_base["duration_min"]
            sensitivity_stops = osm_base["stop_count"]
            sensitivity_source = "OSM/OSRM"

        else:
            fallback = CITY_ROUTE_BASE[
                sensitivity_city
            ]

            sensitivity_base_km = float(
                fallback["km"]
            )

            sensitivity_base_min = (
                sensitivity_base_km
                / 48
                * 60
            )

            sensitivity_stops = len(
                ATM[
                    ATM["İl"]
                    == sensitivity_city
                ]
            )

            sensitivity_source = "Temsili karayolu yedeği"

        vehicle_rows = []

        for vehicle in range(2, 9):
            # Daha fazla araç paralel çalışma ile ekip başı çevrim süresini azaltabilir;
            # ancak toplam yol ağında tekrarlı hareket yaratabileceği için küçük bir
            # mesafe artış katsayısı kullanılır.
            distance_factor = (
                0.94
                + max(0, vehicle - 4) * 0.025
            )

            distance = (
                sensitivity_base_km
                * distance_factor
            )

            # Paralellik nedeniyle tamamlanma süresi azalır.
            parallel_factor = max(
                0.42,
                1.00 - (vehicle - 2) * 0.075,
            )

            drive_minutes = (
                sensitivity_base_min
                * parallel_factor
            )

            service_minutes = (
                sensitivity_stops
                * scenario_service_min
                * parallel_factor
            )

            sensitivity_hours = (
                drive_minutes
                + service_minutes
            ) / 60.0

            sensitivity_road_cost = (
                distance
                * scenario_road_cost
            )

            sensitivity_labor_cost = (
                sensitivity_hours
                * scenario_crew_size
                * scenario_hourly_worker
                if include_labor
                else 0.0
            )

            sensitivity_other_cost = (
                (
                    scenario_accident_cost * 0.10
                    if include_accident
                    else 0.0
                )
                + (
                    scenario_training_cost * scenario_crew_size
                    if include_training
                    else 0.0
                )
                + (
                    scenario_lodging_cost * scenario_crew_size
                    if include_lodging
                    else 0.0
                )
                + (
                    max(0.0, sensitivity_hours - 8.0)
                    * scenario_crew_size
                    * scenario_overtime_cost
                    if include_overtime
                    else 0.0
                )
            )

            sensitivity_total_cost = (
                sensitivity_road_cost
                + sensitivity_labor_cost
                + sensitivity_other_cost
            )

            service = min(
                99,
                80 + vehicle * 2.6,
            )

            vehicle_rows.append(
                {
                    "Araç": vehicle,
                    "Kaynak": sensitivity_source,
                    "OSM / Yol km": round(distance, 1),
                    "Hizmet %": round(service, 1),
                    "Yol Maliyeti": round(sensitivity_road_cost),
                    "İşçilik Maliyeti": round(sensitivity_labor_cost),
                    "Diğer Seçili Maliyetler": round(sensitivity_other_cost),
                    "Toplam Maliyet": round(sensitivity_total_cost),
                }
            )

        vehicle_sensitivity = pd.DataFrame(vehicle_rows)

        min_cost_row = vehicle_sensitivity.loc[
            vehicle_sensitivity["Toplam Maliyet"].idxmin()
        ]

        sens_left, sens_right = st.columns([1.35, 1])

        with sens_left:
            fleet_fig = go.Figure()

            fleet_fig.add_trace(
                go.Scatter(
                    x=vehicle_sensitivity["Araç"],
                    y=vehicle_sensitivity["Toplam Maliyet"],
                    mode="lines+markers",
                    name="Toplam Maliyet",
                    line=dict(
                        color="#4d9cff",
                        width=3,
                    ),
                )
            )

            fleet_fig.add_trace(
                go.Scatter(
                    x=[min_cost_row["Araç"]],
                    y=[min_cost_row["Toplam Maliyet"]],
                    mode="markers+text",
                    text=["Minimum"],
                    textposition="top center",
                    marker=dict(
                        color="#ffbf00",
                        size=13,
                    ),
                    name="Minimum",
                )
            )

            fleet_fig.update_layout(
                height=350,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                xaxis=dict(
                    title="Araç Sayısı",
                    dtick=1,
                    gridcolor="rgba(255,255,255,.05)",
                ),
                yaxis=dict(
                    title="Toplam Maliyet (TL)",
                    gridcolor="rgba(255,255,255,.05)",
                ),
            )

            safe_plotly_chart(fleet_fig)

        with sens_right:
            st.metric(
                "Minimum Maliyetli Araç Sayısı",
                int(min_cost_row["Araç"]),
            )

            st.metric(
                "Minimum Toplam Maliyet",
                fmt_tl(
                    min_cost_row[
                        "Toplam Maliyet"
                    ]
                ),
            )

            st.metric(
                "Bu Noktadaki Yol Maliyeti",
                fmt_tl(
                    min_cost_row[
                        "Yol Maliyeti"
                    ]
                ),
            )

            st.metric(
                "Bu Noktadaki İşçilik",
                fmt_tl(
                    min_cost_row[
                        "İşçilik Maliyeti"
                    ]
                ),
            )

            st.caption(
                f"Baz rota kaynağı: {sensitivity_source}. "
                "Araç sayısı arttıkça süre ve maliyet arasındaki denge karşılaştırılır."
            )

        st.dataframe(
            vehicle_sensitivity,
            hide_index=True,
            width="stretch",
            height=265,
        )


# =========================================================
# 8. RAPORLAR
# =========================================================

elif page == "Raporlar":
    f1, f2, f3 = st.columns(3)

    with f1:
        report_type = st.selectbox(
            "Rapor Türü",
            [
                "Günlük Operasyon Özeti",
                "Kritik ATM Raporu",
                "Nakit Optimizasyon Raporu",
                "Rota Performans Raporu",
            ],
        )

    with f2:
        report_city = st.selectbox(
            "İl",
            list(SUMMARY.keys()),
            key="report_city",
        )

    with f3:
        report_date = st.date_input(
            "Tarih",
            value=date(2026, 8, 28),
            key="report_date",
        )

    report_df = region_df(report_city)
    report_summary = SUMMARY[report_city]

    r1, r2, r3, r4 = st.columns(4)

    r1.metric("ATM Sayısı", report_summary["atm"])
    r2.metric("Kritik ATM", report_summary["critical"])
    r3.metric("Tahmini Talep", fmt_m(report_summary["demand"]))
    r4.metric("Rota Verimliliği", f"%{report_summary['eff']}")

    st.write("")

    left, right = st.columns([1.4, 1])

    with left:
        with st.container(border=True):
            st.subheader(report_type)

            st.caption(
                f"{report_city} · "
                f"{report_date.strftime('%d.%m.%Y')} · "
                "Temsili Veri"
            )

            high = report_df[
                report_df["Kritiklik"] == "Yüksek"
            ]

            middle = report_df[
                report_df["Kritiklik"] == "Orta"
            ]

            st.info(
                f"Seçili kapsamda **{report_summary['atm']} ATM** bulunmaktadır.\n\n"
                f"Temsili ağ örneğinde **{len(high)} yüksek** ve "
                f"**{len(middle)} orta** riskli ATM bulunmaktadır.\n\n"
                f"24 saatlik bölgesel nakit talebi yaklaşık "
                f"**{fmt_m(report_summary['demand'])}** seviyesindedir.\n\n"
                "Operasyon önceliği kritik ATM ikmallerinin tamamlanması "
                "ve rota verimliliğinin korunmasıdır."
            )

    with right:
        with st.container(border=True):
            st.subheader("Öncelikli Aksiyonlar")

            if len(high) == 0:
                st.success("Yüksek riskli ATM bulunmuyor.")
            else:
                for _, row in high.head(4).iterrows():
                    st.warning(
                        f"**{row['ATM Kodu']} — "
                        f"{row['İl']} / {row['İlçe']}**\n\n"
                        "Öncelikli ikmal planlanmalı."
                    )

    report_table = report_df.copy()

    report_table["Önerilen İkmal"] = (
        (
            report_table["24s Tahmin"]
            - report_table["Mevcut Nakit"]
        )
        .clip(lower=0)
        * 1.15
    ).round()

    with st.container(border=True):
        st.subheader("Rapor Detayı")

        st.dataframe(
            report_table[
                [
                    "ATM Kodu",
                    "İl",
                    "İlçe",
                    "Mevcut Nakit",
                    "24s Tahmin",
                    "Kritiklik",
                    "Önerilen İkmal",
                ]
            ],
            hide_index=True,
            width="stretch",
            height=390,
        )

    csv_data = report_table[
        [
            "ATM Kodu",
            "İl",
            "İlçe",
            "Mevcut Nakit",
            "24s Tahmin",
            "Kritiklik",
            "Önerilen İkmal",
        ]
    ].to_csv(
        index=False,
        sep=";",
    ).encode("utf-8-sig")

    st.download_button(
        "📥 Raporu CSV Olarak İndir",
        data=csv_data,
        file_name="vakifbank_atm_raporu.csv",
        mime="text/csv",
    )


    # -----------------------------------------------------
    # RAPORLAR - RİSK / İL ÖZETİ VE METİN RAPORU
    # -----------------------------------------------------

    st.write("")

    report_chart_col, report_city_col = st.columns([1.1, 1])

    with report_chart_col:
        with st.container(border=True):
            st.subheader("Kritiklik Dağılımı")

            crit_counts = (
                report_df["Kritiklik"]
                .value_counts()
                .reindex(["Yüksek", "Orta", "Düşük"], fill_value=0)
                .reset_index()
            )
            crit_counts.columns = ["Kritiklik", "ATM Sayısı"]

            donut = px.pie(
                crit_counts,
                names="Kritiklik",
                values="ATM Sayısı",
                hole=.58,
                color="Kritiklik",
                color_discrete_map=RISK_COLOR,
            )
            donut.update_layout(
                height=310,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                legend=dict(orientation="h", y=-.05),
            )
            safe_plotly_chart(
                donut
            )

    with report_city_col:
        with st.container(border=True):
            st.subheader("İl Bazlı ATM Dağılımı")

            city_counts = ATM.groupby("İl").size().reset_index(name="ATM Sayısı")
            city_fig = go.Figure(
                go.Bar(
                    x=city_counts["İl"],
                    y=city_counts["ATM Sayısı"],
                    marker_color="#4d9cff",
                )
            )
            city_fig.update_layout(
                height=310,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                xaxis=dict(showgrid=False, type="category"),
                yaxis=dict(gridcolor="rgba(255,255,255,.06)"),
            )
            safe_plotly_chart(
                city_fig
            )

    report_text = f"""VAKIFBANK DOĞU KARADENİZ ATM KARAR DESTEK RAPORU

Rapor Türü: {report_type}
Kapsam: {report_city}
Tarih: {report_date.strftime('%d.%m.%Y')}

ATM Sayısı: {report_summary['atm']}
Kritik ATM: {report_summary['critical']}
Tahmini Nakit Talebi: {fmt_m(report_summary['demand'])}
Rota Verimliliği: %{report_summary['eff']}

Bu çıktı prototip amaçlı temsili veriler kullanılarak oluşturulmuştur.
"""

    st.download_button(
        "📝 Yönetici Özetini TXT Olarak İndir",
        data=report_text.encode("utf-8-sig"),
        file_name="vakifbank_yonetici_ozeti.txt",
        mime="text/plain",
    )


# =========================================================
# ALT NOT
# =========================================================

st.divider()

st.caption(
    "⚠️ Bu karar destek sistemi bitirme projesi prototipidir. "
    "ATM, nakit, maliyet ve talep verileri temsilidir; "
    "rota mesafe/süre hesaplarında OpenStreetMap/OSRM kullanılmaktadır. "
    "Gerçek VakıfBank operasyon verisi kullanılmamaktadır."
)
