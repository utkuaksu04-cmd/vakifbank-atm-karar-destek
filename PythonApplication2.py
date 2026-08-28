
import math
from datetime import date, timedelta
from textwrap import dedent
from html import escape

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


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
        width:245px !important;
        min-width:245px !important;
        background:linear-gradient(180deg,#07131e 0%,#081622 100%) !important;
        border-right:1px solid #1d3041 !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        width:245px !important;
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
        gap:5px;
    }

    section[data-testid="stSidebar"] label[data-baseweb="radio"] {
        width:100%;
        min-height:44px;
        margin:0;
        padding:10px 11px;
        border-radius:10px;
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
        font-size:1.55rem;
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
        color:#8fa4b7 !important;
        font-size:.68rem !important;
        font-weight:700 !important;
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
        color:#ffffff !important;
    }

    /* TÜM SAYFALARDA METRIC KÜÇÜK BAŞLIKLARI */
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] > div,
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricLabel"] span,
    div[data-testid="stMetricLabel"] label,
    div[data-testid="stMetricLabel"] * {
        color:#FFD54A !important;
        -webkit-text-fill-color:#FFD54A !important;
        opacity:1 !important;
        visibility:visible !important;
        font-size:.72rem !important;
        font-weight:850 !important;
        filter:none !important;
    }

    /* METRIC ANA DEĞERLERİ */
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricValue"] p,
    div[data-testid="stMetricValue"] span,
    div[data-testid="stMetricValue"] * {
        color:#FFFFFF !important;
        -webkit-text-fill-color:#FFFFFF !important;
        opacity:1 !important;
        visibility:visible !important;
        font-weight:900 !important;
        font-size:1.55rem;
        filter:none !important;
    }

    div[data-testid="stMetricDelta"],
    div[data-testid="stMetricDelta"] * {
        opacity:1 !important;
        visibility:visible !important;
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
        color:#FFD54A !important;
        -webkit-text-fill-color:#FFD54A !important;
        opacity:1 !important;
        font-size:.72rem;
        font-weight:800;
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
            width:205px !important;
            min-width:205px !important;
        }

        .user-copy { display:none; }

        .route-head {
            grid-template-columns:1fr 1fr;
        }
    }

    /* =====================================================
       FINAL METRIC COLOR OVERRIDE
       ATM İzleme / Talep Tahmini / Kritik Önceliklendirme /
       Nakit Optimizasyonu / Raporlar ve diğer st.metric alanları
       ===================================================== */
    [data-testid="stMetric"] [data-testid="stMetricLabel"],
    [data-testid="stMetric"] [data-testid="stMetricLabel"] *,
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color:#FFD54A !important;
        -webkit-text-fill-color:#FFD54A !important;
        opacity:1 !important;
        visibility:visible !important;
        font-weight:850 !important;
        filter:none !important;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"],
    [data-testid="stMetric"] [data-testid="stMetricValue"] *,
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color:#FFFFFF !important;
        -webkit-text-fill-color:#FFFFFF !important;
        opacity:1 !important;
        visibility:visible !important;
        filter:none !important;
    }


    /* =====================================================
       ÖZEL METRIC KARTLARI — RENK GARANTİLİ
       Küçük başlık: sarı | Değer: beyaz
       ===================================================== */
    .vb-metric-card {
        background:linear-gradient(180deg,#102230 0%,#0e1b28 100%);
        border:1px solid #263b4d;
        border-radius:13px;
        padding:13px 14px;
        min-height:102px;
        margin-bottom:12px;
        overflow:hidden;
        box-sizing:border-box;
    }

    .vb-metric-label {
        color:#FFD54A !important;
        -webkit-text-fill-color:#FFD54A !important;
        opacity:1 !important;
        font-size:.72rem;
        font-weight:850;
        line-height:1.25;
        margin-bottom:7px;
    }

    .vb-metric-value {
        color:#FFFFFF !important;
        -webkit-text-fill-color:#FFFFFF !important;
        opacity:1 !important;
        font-size:1.55rem;
        font-weight:900;
        line-height:1.05;
        letter-spacing:-.35px;
        overflow-wrap:anywhere;
    }

    .vb-metric-delta {
        color:#AFC0CF !important;
        -webkit-text-fill-color:#AFC0CF !important;
        opacity:1 !important;
        font-size:.68rem;
        font-weight:700;
        margin-top:7px;
        line-height:1.25;
        overflow-wrap:anywhere;
    }

    </style>
    """),
    unsafe_allow_html=True,
)




# =========================================================
# ÖZEL METRIC KARTI
# Streamlit'in tema/DOM değişikliklerinden etkilenmez.
# =========================================================

def metric_card(container, label, value, delta=None, *args, **kwargs):
    label_text = escape(str(label))
    value_text = escape(str(value))

    delta_html = ""
    if delta is not None and str(delta) != "":
        delta_html = (
            f'<div class="vb-metric-delta">{escape(str(delta))}</div>'
        )

    container.markdown(
        f"""
        <div class="vb-metric-card">
            <div class="vb-metric-label">{label_text}</div>
            <div class="vb-metric-value">{value_text}</div>
            {delta_html}
        </div>
        """,
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
RISK_COLOR = {"Yüksek": "#ff4e57", "Orta": "#ffbf00", "Düşük": "#45c86a"}

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
# YARDIMCI FONKSİYONLAR
# =========================================================

def compact_html(html_text):
    """Streamlit Markdown'ta HTML bloklarının kod bloğuna dönüşmesini engeller."""
    return "".join(line.strip() for line in html_text.splitlines() if line.strip())


def safe_plotly_chart(fig):
    """Plotly'yi yalnızca config üzerinden render eder; deprecated kwargs uyarısını önler."""
    st.plotly_chart(
        fig,
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


def haversine(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1)
        * math.cos(p2)
        * math.sin(dl / 2) ** 2
    )

    return 2 * r * math.asin(math.sqrt(a))


def map_fig(df, height=430, selected_codes=None, line_points=None, show_city_labels=True):
    """
    API KEY istemeyen uydu tabanı.
    Plotly white-bg üzerine Esri World Imagery raster katmanı bindirilir.
    """
    selected_codes = selected_codes or []

    tmp = df.copy()
    tmp["Marker Boyutu"] = tmp["ATM Kodu"].apply(
        lambda x: 18 if x in selected_codes else 11
    )

    fig = px.scatter_mapbox(
        tmp,
        lat="Lat",
        lon="Lon",
        color="Kritiklik",
        size="Marker Boyutu",
        size_max=18,
        hover_name="ATM Kodu",
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
        zoom=6.2 if len(tmp) > 6 else 8,
        height=height,
    )

    if line_points:
        fig.add_trace(
            go.Scattermapbox(
                lat=[p[0] for p in line_points],
                lon=[p[1] for p in line_points],
                mode="lines",
                line=dict(width=4, color="#ffbf00"),
                hoverinfo="skip",
                name="Seçili rota",
            )
        )

    if show_city_labels:
        labels = CITY_LABELS.copy()

        if len(tmp) <= 6 and len(tmp) > 0:
            cities = tmp["İl"].unique().tolist()
            labels = labels[labels["İl"].isin(cities)]

        fig.add_trace(
            go.Scattermapbox(
                lat=labels["Lat"],
                lon=labels["Lon"],
                mode="text",
                text=labels["İl"],
                textfont=dict(
                    color="white",
                    size=12,
                ),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    fig.update_layout(
        mapbox=dict(
            style="white-bg",
            layers=[
                dict(
                    below="traces",
                    sourcetype="raster",
                    source=[
                        "https://server.arcgisonline.com/ArcGIS/rest/services/"
                        "World_Imagery/MapServer/tile/{z}/{y}/{x}"
                    ],
                )
            ],
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#0f1d2a",
        plot_bgcolor="#0f1d2a",
        legend=dict(
            orientation="h",
            y=1.01,
            x=0,
            font=dict(color="white", size=10),
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
        "Nakit Optimizasyonu": "₺",
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
    "Nakit Optimizasyonu": (
        "Nakit Optimizasyonu",
        "Hizmet seviyesi ve maliyet dengesine göre hedef nakit",
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

    metric_card(m1, "İzlenen ATM", len(monitor_df))
    metric_card(m2, 
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

    metric_card(m3, "Ortalama Doluluk", f"%{avg_fill:.0f}")

    refill_today = len(
        monitor_df[
            monitor_df["Mevcut Nakit"]
            < monitor_df["24s Tahmin"] * .70
        ]
    )
    metric_card(m4, "Bugün İkmal", refill_today)

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

                metric_card(a, "Mevcut Nakit", fmt_tl(row["Mevcut Nakit"]))
                metric_card(b, "24s Tahmin", fmt_tl(row["24s Tahmin"]))

                metric_card(a, "Doluluk Oranı", f"%{util:.0f}")
                metric_card(b, "Kritiklik", row["Kritiklik"])

                metric_card(a, "Önerilen İkmal", fmt_tl(recommended))
                metric_card(b, 
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

    metric_card(a, "Toplam Tahmin", fmt_m(total_forecast))
    metric_card(b, "Günlük Ortalama", fmt_m(avg_forecast))
    metric_card(c, "Pik Gün", labels[peak_index], fmt_m(peak_value))
    metric_card(d, 
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

            metric_card(st, "Senaryo", fc_scenario)
            metric_card(st, "Tahmin Alt Bandı", fmt_m(min(lower)))
            metric_card(st, "Tahmin Üst Bandı", fmt_m(max(upper)))


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

    metric_card(k1, 
        "1. Öncelik",
        top["ATM Kodu"],
        f"{top['İl']} / {top['İlçe']}",
    )
    metric_card(k2, "Acil İkmal", urgent)
    metric_card(k3, "Ortalama Risk Skoru", f"{avg_score:.0f}")
    metric_card(k4, "İzleme Gereken", watch)

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
# 5. NAKİT OPTİMİZASYONU
# =========================================================

elif page == "Nakit Optimizasyonu":
    f1, f2, f3, f4 = st.columns(4)

    with f1:
        cash_city = st.selectbox(
            "İl",
            ["Trabzon", "Rize", "Ordu", "Giresun", "Artvin"],
        )

    cash_df = ATM[ATM["İl"] == cash_city].copy()

    with f2:
        cash_atm = st.selectbox(
            "ATM",
            cash_df["ATM Kodu"].tolist(),
        )

    with f3:
        cash_service = st.selectbox(
            "Hizmet Seviyesi",
            [90, 95, 98, 99],
            index=1,
        )

    with f4:
        cash_days = st.selectbox(
            "Planlama Ufku",
            [1, 2, 3],
            format_func=lambda x: f"{x} Gün",
        )

    row = cash_df[cash_df["ATM Kodu"] == cash_atm].iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        holding_rate = st.slider(
            "Günlük Taşıma Maliyeti (%)",
            0.02,
            0.20,
            0.08,
            0.01,
        )

    with c2:
        stock_penalty = st.slider(
            "Stokout Ceza Maliyeti",
            1000,
            10000,
            5000,
            500,
        )

    with c3:
        fixed_refill_cost = st.slider(
            "İkmal Sabit Maliyeti",
            300,
            2500,
            900,
            100,
        )

    with c4:
        uncertainty = st.slider(
            "Talep Belirsizliği (%)",
            5,
            30,
            12,
        )

    z_value = {
        90: 1.28,
        95: 1.645,
        98: 2.05,
        99: 2.33,
    }[cash_service]

    demand_needed = row["24s Tahmin"] * cash_days

    safety_stock = (
        demand_needed
        * (uncertainty / 100)
        * z_value
    )

    target_cash = demand_needed + safety_stock

    refill_amount = max(
        0,
        target_cash - row["Mevcut Nakit"],
    )

    risk_before = min(
        99,
        max(
            1,
            100
            * (
                1
                - row["Mevcut Nakit"]
                / max(1, demand_needed)
            ),
        ),
    )

    risk_after = 100 - cash_service

    holding_cost = (
        max(0, target_cash - demand_needed)
        * holding_rate
        / 100
        * cash_days
    )

    stockout_cost = (
        stock_penalty
        * risk_after
        / 100
    )

    operation_cost = (
        fixed_refill_cost
        if refill_amount > 0
        else 0
    )

    total_cost = (
        holding_cost
        + stockout_cost
        + operation_cost
    )

    left, right = st.columns([1.2, 1])

    with left:
        with st.container(border=True):
            st.subheader("Önerilen Nakit Seviyesi")

            metric_card(st, 
                "Optimum Hedef Nakit",
                fmt_tl(target_cash),
            )

            a, b = st.columns(2)

            metric_card(a, 
                "Mevcut Nakit",
                fmt_tl(row["Mevcut Nakit"]),
            )
            metric_card(b, 
                "Önerilen İkmal",
                fmt_tl(refill_amount),
            )

            metric_card(a, 
                "İkmal Öncesi Risk",
                f"%{risk_before:.0f}",
            )
            metric_card(b, 
                "İkmal Sonrası Risk",
                f"%{risk_after:.0f}",
            )

            st.progress(cash_service / 100)

            st.caption(
                f"{cash_atm} için {cash_days} günlük talep, "
                f"%{cash_service} hizmet seviyesi ve "
                f"%{uncertainty} talep belirsizliği dikkate alınmıştır."
            )

    with right:
        with st.container(border=True):
            st.subheader("Maliyet Dengesi")

            metric_card(st, 
                "Beklenen Taşıma Maliyeti",
                fmt_tl(holding_cost),
            )

            metric_card(st, 
                "Beklenen Stokout Maliyeti",
                fmt_tl(stockout_cost),
            )

            metric_card(st, 
                "İkmal Operasyon Maliyeti",
                fmt_tl(operation_cost),
            )

            metric_card(st, 
                "Toplam Tahmini Maliyet",
                fmt_tl(total_cost),
            )


    # -----------------------------------------------------
    # NAKİT OPTİMİZASYONU - MALİYET EĞRİSİ
    # -----------------------------------------------------

    st.write("")

    curve_col, service_col = st.columns([1.35, 1])

    with curve_col:
        with st.container(border=True):
            st.subheader("Hedef Nakit Seviyesine Göre Toplam Maliyet")
            st.caption(
                "Fazla nakit taşıma maliyeti ile stokout cezası arasındaki denge."
            )

            low_candidate = max(
                row["Mevcut Nakit"],
                demand_needed * 0.60,
            )
            high_candidate = target_cash * 1.30
            candidates = np.linspace(low_candidate, high_candidate, 35)

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
                )
                candidate_shortage = stock_penalty * shortage_ratio
                candidate_refill = (
                    fixed_refill_cost
                    if candidate > row["Mevcut Nakit"]
                    else 0
                )
                candidate_costs.append(
                    candidate_holding
                    + candidate_shortage
                    + candidate_refill
                )

            best_idx = int(np.argmin(candidate_costs))
            best_candidate = candidates[best_idx]

            cost_fig = go.Figure()
            cost_fig.add_trace(
                go.Scatter(
                    x=candidates,
                    y=candidate_costs,
                    mode="lines",
                    line=dict(color="#4d9cff", width=3),
                    name="Toplam Maliyet",
                )
            )
            cost_fig.add_trace(
                go.Scatter(
                    x=[best_candidate],
                    y=[candidate_costs[best_idx]],
                    mode="markers+text",
                    text=["Minimum"],
                    textposition="top center",
                    marker=dict(size=11, color="#ffbf00"),
                    name="Minimum",
                )
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

            safe_plotly_chart(
                cost_fig
            )

            st.success(
                f"Maliyet eğrisine göre aday minimum seviye yaklaşık "
                f"**{fmt_tl(best_candidate)}**."
            )

    with service_col:
        with st.container(border=True):
            st.subheader("Hizmet Seviyesi Karşılaştırması")

            comparison_rows = []
            for srv in [90, 95, 98, 99]:
                z = {90: 1.28, 95: 1.645, 98: 2.05, 99: 2.33}[srv]
                temp_target = demand_needed * (
                    1 + (uncertainty / 100) * z
                )
                temp_refill = max(
                    0,
                    temp_target - row["Mevcut Nakit"],
                )
                temp_hold = (
                    max(0, temp_target - demand_needed)
                    * holding_rate
                    / 100
                    * cash_days
                )
                temp_stock = stock_penalty * ((100 - srv) / 100)
                temp_total = (
                    temp_hold
                    + temp_stock
                    + (fixed_refill_cost if temp_refill > 0 else 0)
                )
                comparison_rows.append(
                    [
                        srv,
                        round(temp_target),
                        round(temp_refill),
                        round(temp_total),
                    ]
                )

            service_compare = pd.DataFrame(
                comparison_rows,
                columns=[
                    "Hizmet %",
                    "Hedef Nakit",
                    "İkmal",
                    "Toplam Maliyet",
                ],
            )

            st.dataframe(
                service_compare,
                hide_index=True,
                height=230,
                column_config={
                    "Hedef Nakit": st.column_config.NumberColumn(format="₺ %.0f"),
                    "İkmal": st.column_config.NumberColumn(format="₺ %.0f"),
                    "Toplam Maliyet": st.column_config.NumberColumn(format="₺ %.0f"),
                },
            )

            st.info(
                "Yüksek hizmet seviyesi stokout riskini düşürür; ancak hedef nakit ve taşıma maliyetini artırır."
            )


# =========================================================
# 6. ROTA PLANLAMA
# =========================================================

elif page == "Rota Planlama":
    st.info(
        "İki ATM seçerek aralarındaki mesafe, tahmini karayolu mesafesi, süre ve operasyon maliyetini karşılaştır."
    )

    f1, f2, f3 = st.columns([.8, 1.4, 1.4])

    with f1:
        route_city = st.selectbox(
            "Ekip / İl",
            ["Tüm Bölge", "Trabzon", "Rize", "Ordu", "Giresun", "Artvin"],
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

    with f2:
        from_label = st.selectbox(
            "Başlangıç Noktası",
            atm_labels,
            index=0,
        )

    with f3:
        to_label = st.selectbox(
            "Varış Noktası",
            atm_labels,
            index=1 if len(atm_labels) > 1 else 0,
        )

    from_code = atm_codes[atm_labels.index(from_label)]
    to_code = atm_codes[atm_labels.index(to_label)]

    from_row = route_df[
        route_df["ATM Kodu"] == from_code
    ].iloc[0]

    to_row = route_df[
        route_df["ATM Kodu"] == to_code
    ].iloc[0]

    if from_code == to_code:
        st.warning(
            "Başlangıç ve varış için farklı iki ATM seç."
        )
    else:
        air_distance = haversine(
            from_row["Lat"],
            from_row["Lon"],
            to_row["Lat"],
            to_row["Lon"],
        )

        road_factor = (
            1.22
            if from_row["İl"] == to_row["İl"]
            else 1.28
        )

        road_distance = air_distance * road_factor

        travel_minutes = (
            road_distance / 52 * 60 + 24
        )

        route_cost = (
            road_distance * 32 + 850
        )

        left, right = st.columns([1.55, 1])

        with left:
            with st.container(border=True):
                st.subheader("Seçili Rota")

                fig = map_fig(
                    route_df,
                    height=500,
                    selected_codes=[from_code, to_code],
                    line_points=[
                        (from_row["Lat"], from_row["Lon"]),
                        (to_row["Lat"], to_row["Lon"]),
                    ],
                )

                safe_plotly_chart(
                    fig
                )

        with right:
            with st.container(border=True):
                st.subheader("Rota Özeti")

                st.markdown(
                    f"**{from_code} → {to_code}**\n\n"
                    f"{from_row['İl']} / {from_row['İlçe']} → "
                    f"{to_row['İl']} / {to_row['İlçe']}"
                )

                a, b = st.columns(2)

                metric_card(a, 
                    "Kuş Uçuşu",
                    f"{air_distance:.1f} km".replace(".", ","),
                )

                metric_card(b, 
                    "Tahmini Yol",
                    f"{road_distance:.1f} km".replace(".", ","),
                )

                metric_card(a, 
                    "Tahmini Süre",
                    f"{travel_minutes:.0f} dk",
                )

                metric_card(b, 
                    "Tahmini Maliyet",
                    fmt_tl(route_cost),
                )

                if from_row["İl"] == to_row["İl"]:
                    st.success(
                        "İki nokta aynı il ekibinde. Tek araçla ardışık ikmal planı uygulanabilir."
                    )
                else:
                    st.warning(
                        "İller arası rota seçildi. Ekip sınırı nedeniyle ortak araç veya devir noktası değerlendirilmeli."
                    )

                st.caption(
                    "Tahmini yol mesafesi gerçek navigasyon servisi değildir. "
                    "Kuş uçuşu mesafesine bölgesel karayolu katsayısı uygulanmıştır."
                )


        # -------------------------------------------------
        # ROTA PLANLAMA - MESAFE MATRİSİ / YAKIN KOMŞULAR
        # -------------------------------------------------

        st.write("")

        matrix_col, nearest_col = st.columns([1.35, 1])

        with matrix_col:
            with st.container(border=True):
                st.subheader("Seçili Ekip İçin ATM Mesafe Matrisi")
                st.caption(
                    "Kuş uçuşu mesafeleridir; karayolu planında ayrıca yol katsayısı uygulanır."
                )

                matrix_source = route_df.head(8).copy()
                codes = matrix_source["ATM Kodu"].tolist()
                matrix = pd.DataFrame(index=codes, columns=codes, dtype=float)

                for _, ra in matrix_source.iterrows():
                    for _, rb in matrix_source.iterrows():
                        matrix.loc[ra["ATM Kodu"], rb["ATM Kodu"]] = round(
                            haversine(
                                ra["Lat"],
                                ra["Lon"],
                                rb["Lat"],
                                rb["Lon"],
                            ),
                            1,
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
                    )
                )
                matrix_fig.update_layout(
                    height=390,
                    margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor="#0f1d2a",
                    plot_bgcolor="#0f1d2a",
                    font=dict(color="#dbe4ec", size=9),
                )
                safe_plotly_chart(
                    matrix_fig
                )

        with nearest_col:
            with st.container(border=True):
                st.subheader("Başlangıç ATM'sine En Yakın Noktalar")

                nearest_rows = []
                for _, candidate in route_df.iterrows():
                    if candidate["ATM Kodu"] == from_code:
                        continue

                    direct = haversine(
                        from_row["Lat"],
                        from_row["Lon"],
                        candidate["Lat"],
                        candidate["Lon"],
                    )
                    factor_local = (
                        1.22
                        if from_row["İl"] == candidate["İl"]
                        else 1.28
                    )
                    road_est = direct * factor_local
                    nearest_rows.append(
                        [
                            candidate["ATM Kodu"],
                            candidate["İlçe"],
                            round(road_est, 1),
                            round(road_est / 52 * 60 + 12),
                        ]
                    )

                nearest_df = pd.DataFrame(
                    nearest_rows,
                    columns=["ATM", "İlçe", "Tahmini Yol km", "Süre dk"],
                ).sort_values("Tahmini Yol km").head(6)

                st.dataframe(
                    nearest_df,
                    hide_index=True,
                    height=265,
                )

                if len(nearest_df) > 0:
                    nearest = nearest_df.iloc[0]
                    st.success(
                        f"{from_code} için en yakın sonraki durak "
                        f"**{nearest['ATM']}** (~{nearest['Tahmini Yol km']} km)."
                    )


        st.write("")

        with st.container(border=True):
            st.subheader("Önerilen Ardışık İkmal Sırası")
            st.caption(
                "Seçili ekipte başlangıç ATM'sinden en yakın komşu mantığıyla üretilmiş basit rota önerisi."
            )

            sequence_source = route_df.copy().reset_index(drop=True)
            if len(sequence_source) >= 2:
                start_code = from_code
                remaining = sequence_source[
                    sequence_source["ATM Kodu"] != start_code
                ].copy()
                current = sequence_source[
                    sequence_source["ATM Kodu"] == start_code
                ].iloc[0]

                sequence = [start_code]
                cumulative_km = 0.0
                sequence_rows = []

                while len(remaining) > 0:
                    options = []
                    for idx, candidate in remaining.iterrows():
                        direct = haversine(
                            current["Lat"],
                            current["Lon"],
                            candidate["Lat"],
                            candidate["Lon"],
                        )
                        factor_local = (
                            1.22
                            if current["İl"] == candidate["İl"]
                            else 1.28
                        )
                        road_est = direct * factor_local
                        options.append((road_est, idx, candidate))

                    options.sort(key=lambda x: x[0])
                    road_est, idx, nxt = options[0]
                    cumulative_km += road_est

                    sequence_rows.append(
                        {
                            "Sıra": len(sequence) + 1,
                            "ATM": nxt["ATM Kodu"],
                            "İl": nxt["İl"],
                            "İlçe": nxt["İlçe"],
                            "Bir Önceki Duraktan km": round(road_est, 1),
                            "Kümülatif km": round(cumulative_km, 1),
                            "Kritiklik": nxt["Kritiklik"],
                        }
                    )

                    sequence.append(nxt["ATM Kodu"])
                    current = nxt
                    remaining = remaining.drop(index=idx)

                sequence_df = pd.DataFrame(sequence_rows)

                route_seq_cols = st.columns([1.5, 1])

                with route_seq_cols[0]:
                    st.dataframe(
                        sequence_df,
                        hide_index=True,
                        width="stretch",
                        height=275,
                    )

                with route_seq_cols[1]:
                    metric_card(st, 
                        "Önerilen Tur Uzunluğu",
                        f"{cumulative_km:.1f} km".replace(".", ","),
                    )
                    metric_card(st, 
                        "Yaklaşık Tur Süresi",
                        f"{(cumulative_km / 48 * 60 + 12 * len(sequence_df)):.0f} dk",
                    )
                    metric_card(st, 
                        "Yaklaşık Tur Maliyeti",
                        fmt_tl(cumulative_km * 32 + 850),
                    )
                    st.caption(
                        "Bu bölüm optimizasyonun ilk prototipidir; en yakın komşu sezgiseli kullanılmıştır."
                    )


# =========================================================
# 7. SENARYOLAR
# =========================================================

elif page == "Senaryolar":
    f1, f2 = st.columns(2)

    with f1:
        scenario_city = st.selectbox(
            "İl / Ekip",
            ["Tüm İller", "Trabzon", "Rize", "Ordu", "Giresun", "Artvin"],
        )

    with f2:
        objective = st.selectbox(
            "Optimizasyon Hedefi",
            ["Maliyet Minimum", "Mesafe Minimum", "Dengeli"],
        )

    cities = (
        list(CITY_ROUTE_BASE.keys())
        if scenario_city == "Tüm İller"
        else [scenario_city]
    )

    rows = []

    for city in cities:
        base = CITY_ROUTE_BASE[city]

        for _, sc in SCENARIOS.iterrows():
            distance = base["km"] * sc["Mesafe Çarpanı"]
            cost = base["cost"] * sc["Maliyet Çarpanı"]

            vehicles = max(
                1,
                int(base["vehicles"] + sc["Araç Farkı"]),
            )

            if objective == "Maliyet Minimum":
                score = cost
            elif objective == "Mesafe Minimum":
                score = distance
            else:
                score = (
                    (cost / base["cost"]) * .50
                    + (distance / base["km"]) * .30
                    + (sc["Risk"] / 100) * .20
                )

            rows.append(
                {
                    "İl": city,
                    "Senaryo": sc["Senaryo"],
                    "Araç": vehicles,
                    "Toplam Mesafe": round(distance),
                    "Toplam Maliyet": round(cost),
                    "Hizmet Seviyesi": int(sc["Hizmet Seviyesi"]),
                    "Risk": int(sc["Risk"]),
                    "_score": score,
                }
            )

    scenario_result = pd.DataFrame(rows)

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
                    f"{row['Toplam Mesafe']} km · "
                    f"{fmt_tl(row['Toplam Maliyet'])}\n\n"
                    f"{row['Araç']} araç · "
                    f"%{row['Hizmet Seviyesi']} hizmet"
                )

    st.write("")

    left, right = st.columns([1.45, 1])

    with left:
        with st.container(border=True):
            st.subheader("Senaryo Karşılaştırması")

            table_show = scenario_result.copy()
            table_show["Karar"] = ""

            for row in best_rows:
                mask = (
                    (table_show["İl"] == row["İl"])
                    & (table_show["Senaryo"] == row["Senaryo"])
                )
                table_show.loc[mask, "Karar"] = "Önerilen"

            table_show["Maliyet"] = (
                table_show["Toplam Maliyet"].apply(fmt_tl)
            )

            table_show["Mesafe"] = (
                table_show["Toplam Mesafe"].astype(str)
                + " km"
            )

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
                        "Araç",
                        "Mesafe",
                        "Maliyet",
                        "Hizmet",
                        "Risk %",
                        "Karar",
                    ]
                ],
                hide_index=True,
                width="stretch",
                height=440,
            )

    with right:
        with st.container(border=True):
            chart_city = st.selectbox(
                "Grafikte gösterilecek il",
                cities,
            )

            chart_df = scenario_result[
                scenario_result["İl"] == chart_city
            ].copy()

            chart_df["Maliyet (Bin TL)"] = (
                chart_df["Toplam Maliyet"] / 1000
            )

            chart_df["Mesafe (100 km)"] = (
                chart_df["Toplam Mesafe"] / 100
            )

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=chart_df["Senaryo"],
                    y=chart_df["Maliyet (Bin TL)"],
                    name="Maliyet (Bin TL)",
                    marker_color="#4d9cff",
                )
            )

            fig.add_trace(
                go.Bar(
                    x=chart_df["Senaryo"],
                    y=chart_df["Mesafe (100 km)"],
                    name="Mesafe (100 km)",
                    marker_color="#ffbf00",
                )
            )

            fig.update_layout(
                barmode="group",
                height=400,
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="white"),
                xaxis=dict(showgrid=False, type="category"),
                yaxis=dict(
                    gridcolor="rgba(255,255,255,.06)"
                ),
            )

            safe_plotly_chart(
                fig
            )


    # -----------------------------------------------------
    # SENARYO - İL BAZLI TOPLAM PORTFÖY ÖZETİ
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
                    "Mesafe km": int(best["Toplam Mesafe"]),
                    "Maliyet": int(best["Toplam Maliyet"]),
                    "Hizmet %": int(best["Hizmet Seviyesi"]),
                    "Risk %": int(best["Risk"]),
                }
            )

        portfolio = pd.DataFrame(portfolio_rows)

        p1, p2, p3, p4 = st.columns(4)
        metric_card(p1, 
            "Toplam Araç",
            int(portfolio["Araç"].sum()),
        )
        metric_card(p2, 
            "Toplam Mesafe",
            f"{int(portfolio['Mesafe km'].sum())} km",
        )
        metric_card(p3, 
            "Toplam Maliyet",
            fmt_tl(portfolio["Maliyet"].sum()),
        )
        metric_card(p4, 
            "Ortalama Hizmet",
            f"%{portfolio['Hizmet %'].mean():.1f}".replace(".", ","),
        )

        portfolio["Maliyet / km"] = (
            portfolio["Maliyet"]
            / portfolio["Mesafe km"]
        ).round(1)

        st.dataframe(
            portfolio,
            hide_index=True,
            height=245,
        )

    st.write("")

    with st.container(border=True):
        st.subheader("Pareto Görünümü: Maliyet – Mesafe")

        pareto_fig = px.scatter(
            scenario_result,
            x="Toplam Mesafe",
            y="Toplam Maliyet",
            color="İl",
            symbol="Senaryo",
            hover_data=[
                "Araç",
                "Hizmet Seviyesi",
                "Risk",
            ],
        )
        pareto_fig.update_traces(marker=dict(size=11))
        pareto_fig.update_layout(
            height=390,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#0f1d2a",
            plot_bgcolor="#0f1d2a",
            font=dict(color="#dbe4ec"),
            xaxis=dict(
                title="Toplam Mesafe (km)",
                gridcolor="rgba(255,255,255,.05)",
            ),
            yaxis=dict(
                title="Toplam Maliyet (TL)",
                gridcolor="rgba(255,255,255,.05)",
            ),
        )
        safe_plotly_chart(
            pareto_fig
        )


    st.write("")

    with st.container(border=True):
        st.subheader("Araç Sayısı Duyarlılık Analizi")

        sensitivity_city = st.selectbox(
            "Duyarlılık için il",
            cities,
            key="scenario_sensitivity_city",
        )
        base = CITY_ROUTE_BASE[sensitivity_city]

        vehicle_rows = []
        for vehicle in range(2, 9):
            congestion_factor = max(0.78, 1.18 - vehicle * 0.055)
            distance = base["km"] * congestion_factor
            variable_cost = distance * 19.5
            fixed_vehicle_cost = vehicle * 620
            service = min(99, 78 + vehicle * 3.1)
            shortage_penalty = max(0, 95 - service) * 150
            total = variable_cost + fixed_vehicle_cost + shortage_penalty

            vehicle_rows.append(
                {
                    "Araç": vehicle,
                    "Mesafe": round(distance),
                    "Hizmet %": round(service, 1),
                    "Toplam Maliyet": round(total),
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
                    line=dict(color="#4d9cff", width=3),
                )
            )
            fleet_fig.add_trace(
                go.Scatter(
                    x=[min_cost_row["Araç"]],
                    y=[min_cost_row["Toplam Maliyet"]],
                    mode="markers+text",
                    text=["Minimum"],
                    textposition="top center",
                    marker=dict(color="#ffbf00", size=12),
                    name="Minimum",
                )
            )
            fleet_fig.update_layout(
                height=340,
                margin=dict(l=10, r=10, t=20, b=10),
                paper_bgcolor="#0f1d2a",
                plot_bgcolor="#0f1d2a",
                font=dict(color="#dbe4ec"),
                xaxis=dict(title="Araç Sayısı", showgrid=False),
                yaxis=dict(
                    title="Toplam Maliyet (TL)",
                    gridcolor="rgba(255,255,255,.05)",
                ),
                showlegend=False,
            )
            safe_plotly_chart(
                fleet_fig
            )

        with sens_right:
            metric_card(st, 
                "Minimum Maliyetli Araç Sayısı",
                int(min_cost_row["Araç"]),
            )
            metric_card(st, 
                "Minimum Tahmini Maliyet",
                fmt_tl(min_cost_row["Toplam Maliyet"]),
            )
            metric_card(st, 
                "Bu Noktadaki Hizmet Seviyesi",
                f"%{min_cost_row['Hizmet %']:.1f}".replace(".", ","),
            )

            st.dataframe(
                vehicle_sensitivity,
                hide_index=True,
                height=205,
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

    metric_card(r1, "ATM Sayısı", report_summary["atm"])
    metric_card(r2, "Kritik ATM", report_summary["critical"])
    metric_card(r3, "Tahmini Talep", fmt_m(report_summary["demand"]))
    metric_card(r4, "Rota Verimliliği", f"%{report_summary['eff']}")

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
    "ATM, nakit, maliyet, rota ve talep verileri temsilidir; "
    "gerçek VakıfBank operasyon verisi kullanılmamaktadır."
)
