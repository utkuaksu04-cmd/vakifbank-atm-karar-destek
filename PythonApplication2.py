import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="VakıfBank | Doğu Karadeniz ATM Nakit Yönetimi",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)
def giris_kontrol():
    if st.session_state.get("giris_yapildi", False):
        return

    st.title("🔐 VakıfBank ATM Karar Destek Sistemi")
    st.caption("Devam etmek için giriş yapın.")

    kullanici = st.text_input("Kullanıcı adı")
    sifre = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        if (
            kullanici == st.secrets["login"]["username"]
            and sifre == st.secrets["login"]["password"]
        ):
            st.session_state["giris_yapildi"] = True
            st.rerun()
        else:
            st.error("Kullanıcı adı veya şifre hatalı.")

    st.stop()

giris_kontrol()

# Streamlit'in kendi üst/alt boşluklarını gizle.
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {display:none;}
    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    .stApp {
        background: #06111b;
    }
    iframe {
        display:block;
        border:0 !important;
    }
</style>
""", unsafe_allow_html=True)

APP = r"""
<div id="vb-app">
  <style>
    * { box-sizing: border-box; }
    html, body { margin:0; padding:0; }
    body {
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:#06111b;
      color:#f5f7fb;
    }

    #vb-app {
      --bg:#07131f;
      --bg2:#091825;
      --panel:#0e1d2b;
      --panel2:#112333;
      --panel3:#14283a;
      --line:#263b4d;
      --text:#f7f9fb;
      --muted:#8fa3b6;
      --yellow:#ffbf00;
      --yellow2:#ffd24a;
      --green:#45c86a;
      --red:#ff4e57;
      --orange:#ff9d31;
      --blue:#3f83f8;
      --purple:#7d5df6;
      --cyan:#32c5c7;
      min-height:1000px;
      background:
        radial-gradient(circle at 78% -15%, rgba(40,78,116,.22), transparent 32%),
        linear-gradient(180deg,#07131f 0%,#06111b 100%);
      color:var(--text);
    }

    .shell {
      display:grid;
      grid-template-columns:220px minmax(0,1fr);
      min-height:1000px;
    }

    /* SIDEBAR */
    .sidebar {
      background:linear-gradient(180deg,#07131e 0%,#081622 100%);
      border-right:1px solid rgba(255,255,255,.06);
      padding:16px 12px;
      display:flex;
      flex-direction:column;
      min-width:0;
    }

    .brand {
      display:flex;
      align-items:center;
      gap:10px;
      padding:4px 6px 18px 6px;
    }

    .logo-mark {
      width:38px;
      height:31px;
      border-radius:9px 4px 9px 4px;
      background:var(--yellow);
      display:grid;
      place-items:center;
      color:#111;
      font-weight:1000;
      letter-spacing:-1px;
      transform:skewX(-10deg);
      box-shadow:0 8px 24px rgba(255,191,0,.10);
      flex:0 0 auto;
    }

    .logo-mark span { transform:skewX(10deg); }

    .brand-name {
      font-size:24px;
      font-weight:850;
      letter-spacing:-.6px;
      white-space:nowrap;
    }

    .nav {
      display:flex;
      flex-direction:column;
      gap:6px;
      margin-top:8px;
    }

    .nav button {
      appearance:none;
      width:100%;
      border:0;
      background:transparent;
      color:#d3dce5;
      min-height:43px;
      padding:9px 11px;
      border-radius:10px;
      display:flex;
      align-items:center;
      gap:10px;
      font-weight:650;
      text-align:left;
      transition:.18s ease;
    }

    .nav button:hover {
      background:#102231;
      color:white;
    }

    .nav button.active {
      color:#ffd548;
      background:linear-gradient(90deg,rgba(255,191,0,.20),rgba(255,191,0,.08));
      box-shadow:inset 3px 0 0 var(--yellow);
    }

    .nav-ico {
      width:25px;
      height:25px;
      border-radius:7px;
      display:grid;
      place-items:center;
      background:rgba(255,255,255,.04);
      font-size:14px;
      flex:0 0 25px;
    }

    .sidebar-status {
      margin-top:auto;
      border:1px solid var(--line);
      background:#0c1a27;
      border-radius:13px;
      padding:12px;
      color:var(--muted);
      font-size:11px;
      line-height:1.55;
    }

    .sidebar-status strong {
      color:#ffd457;
      font-size:11px;
    }

    .sys {
      margin-top:8px;
      color:#c8d5df;
    }

    .sys i {
      display:inline-block;
      width:8px;
      height:8px;
      background:var(--green);
      border-radius:50%;
      margin-right:6px;
      box-shadow:0 0 10px rgba(69,200,106,.5);
    }

    /* MAIN */
    .main {
      min-width:0;
      padding:14px 16px 18px;
    }

    .shell.collapsed { grid-template-columns:78px minmax(0,1fr); }
    .shell.collapsed .brand-name,
    .shell.collapsed .nav .text,
    .shell.collapsed .sidebar-status { display:none; }
    .shell.collapsed .brand { justify-content:center; }
    .shell.collapsed .nav button { justify-content:center; padding:9px; }

    .header-left {
      min-width:0;
      display:flex;
      align-items:center;
      gap:13px;
    }

    .menu-btn {
      width:38px;
      height:38px;
      flex:0 0 38px;
      border-radius:9px;
      border:1px solid rgba(255,255,255,.07);
      background:#0d1c29;
      color:#f6f8fa;
      display:grid;
      place-items:center;
      font-size:18px;
      cursor:pointer;
    }

    .menu-btn:hover {
      border-color:#3a5065;
      background:#102333;
    }

    .topbar {
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:16px;
      margin-bottom:12px;
    }

    .title-wrap {
      min-width:0;
    }

    .title {
      font-size:26px;
      line-height:1.1;
      margin:0;
      font-weight:850;
      letter-spacing:-.6px;
      color:#fff;
    }

    .subtitle {
      margin-top:5px;
      color:var(--yellow);
      font-size:12px;
      font-weight:750;
    }

    .profile {
      display:flex;
      align-items:center;
      gap:9px;
      flex:0 0 auto;
    }

    .bell {
      position:relative;
      width:35px;
      height:35px;
      border-radius:10px;
      display:grid;
      place-items:center;
      border:1px solid rgba(255,255,255,.07);
      background:#0d1c29;
    }

    .bell b {
      position:absolute;
      right:-3px;
      top:-4px;
      background:var(--yellow);
      color:#111;
      width:17px;
      height:17px;
      border-radius:50%;
      display:grid;
      place-items:center;
      font-size:9px;
    }

    .avatar {
      width:34px;
      height:34px;
      border-radius:50%;
      background:linear-gradient(135deg,#677b90,#2a3b4b);
      display:grid;
      place-items:center;
      font-size:13px;
      font-weight:800;
    }

    .profile-text strong {
      display:block;
      font-size:11px;
      color:#f6f8fa;
    }

    .profile-text span {
      display:block;
      margin-top:2px;
      color:var(--muted);
      font-size:9px;
    }

    /* FILTERS */
    .filters {
      display:grid;
      grid-template-columns:1.12fr 1fr 1.18fr .92fr .92fr auto auto;
      gap:9px;
      background:#0b1926;
      border:1px solid var(--line);
      border-radius:13px;
      padding:10px;
      margin-bottom:10px;
    }

    .field label {
      display:block;
      color:#8ea2b4;
      font-size:9.5px;
      margin:0 0 5px 2px;
      font-weight:650;
    }

    .field select,
    .field input {
      width:100%;
      height:37px;
      color:#f4f7fa;
      background:#0e1e2d;
      border:1px solid #2a4053;
      border-radius:9px;
      padding:0 10px;
      outline:none;
      font-size:11px;
    }

    .field select:focus,
    .field input:focus {
      border-color:#dcae1c;
      box-shadow:0 0 0 2px rgba(255,191,0,.08);
    }

    .filter-btn {
      align-self:end;
      height:37px;
      border-radius:9px;
      padding:0 13px;
      border:1px solid #2c4155;
      background:#0d1c29;
      color:#cbd7e1;
      font-size:10px;
      font-weight:750;
      white-space:nowrap;
    }

    .apply {
      background:linear-gradient(135deg,var(--yellow),var(--yellow2));
      color:#111;
      border-color:transparent;
      min-width:82px;
      font-weight:900;
    }

    /* KPI */
    .kpis {
      display:grid;
      grid-template-columns:repeat(5,minmax(0,1fr));
      gap:9px;
      margin-bottom:10px;
    }

    .kpi {
      min-width:0;
      min-height:100px;
      background:linear-gradient(180deg,#102230 0%,#0e1b28 100%);
      border:1px solid var(--line);
      border-radius:13px;
      padding:12px;
      display:flex;
      align-items:center;
      gap:10px;
    }

    .kpi-icon {
      width:46px;
      height:46px;
      border-radius:12px;
      display:grid;
      place-items:center;
      font-size:20px;
      font-weight:900;
      flex:0 0 46px;
    }

    .blue { background:rgba(63,131,248,.17); color:#8ab5ff; }
    .green { background:rgba(69,200,106,.16); color:#88e29b; }
    .red { background:rgba(255,78,87,.16); color:#ff8b91; }
    .purple { background:rgba(125,93,246,.16); color:#b09aff; }
    .cyan { background:rgba(50,197,199,.16); color:#80edef; }

    .kpi-label {
      color:#c6d1db;
      font-size:11px;
      margin-bottom:4px;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    .kpi-value {
      font-size:23px;
      font-weight:900;
      line-height:1.0;
      color:white;
      letter-spacing:-.5px;
      white-space:nowrap;
    }

    .kpi-note {
      color:#8194a6;
      font-size:9px;
      margin-top:6px;
      white-space:nowrap;
    }

    .good { color:#62d47d; }
    .bad { color:#ff6d75; }

    /* PANELS */
    .grid-main {
      display:grid;
      grid-template-columns:minmax(0,1.55fr) minmax(360px,.95fr);
      gap:10px;
      margin-bottom:10px;
    }

    .grid-bottom {
      display:grid;
      grid-template-columns:.88fr 1.42fr 1.05fr;
      gap:10px;
    }

    .panel {
      min-width:0;
      background:linear-gradient(180deg,#0f1d2a 0%,#0b1824 100%);
      border:1px solid var(--line);
      border-radius:13px;
      overflow:hidden;
    }

    .panel-head {
      min-height:43px;
      padding:10px 12px 7px;
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:8px;
    }

    .panel-head h2 {
      margin:0;
      font-size:13px;
      line-height:1.2;
      font-weight:850;
      color:white;
    }

    .panel-head p {
      margin:3px 0 0;
      color:var(--muted);
      font-size:9px;
    }

    .ghost-btn {
      border:1px solid #31465a;
      background:#0c1926;
      color:#c8d3dc;
      border-radius:8px;
      height:27px;
      padding:0 9px;
      font-size:8.5px;
      font-weight:750;
      white-space:nowrap;
    }

    /* MAP */
    #map {
      width:100%;
      height:325px;
      background:#0a1621;
    }

    .leaflet-container {
      font-family:inherit;
      background:#0a1621;
    }

    .leaflet-control-zoom a {
      background:#0e1d2b !important;
      color:white !important;
      border-color:#31475a !important;
    }

    .leaflet-control-attribution {
      font-size:7px !important;
      background:rgba(8,18,28,.75) !important;
      color:#a9bac9 !important;
    }

    .leaflet-control-attribution a { color:#d1dce5 !important; }

    .leaflet-popup-content-wrapper,
    .leaflet-popup-tip {
      background:#0e1d2b;
      color:white;
      border:1px solid #30465a;
    }

    .map-legend {
      position:absolute;
      z-index:500;
      left:12px;
      top:55px;
      background:rgba(7,18,28,.9);
      border:1px solid #2c4155;
      border-radius:9px;
      padding:8px 9px;
      font-size:8px;
      color:#dce5ec;
      line-height:1.65;
      pointer-events:none;
    }

    .map-wrap { position:relative; }

    .map-legend strong {
      display:block;
      font-size:8.5px;
      margin-bottom:3px;
    }

    .legend-dot {
      display:inline-block;
      width:8px;
      height:8px;
      border-radius:50%;
      margin-right:5px;
    }

    /* ROUTES */
    .routes {
      padding:0 9px 9px;
      display:flex;
      flex-direction:column;
      gap:7px;
    }

    .route {
      border:1px solid #2a3e51;
      border-left:3px solid var(--route);
      background:#102130;
      border-radius:10px;
      padding:9px 10px;
    }

    .route-top {
      display:grid;
      grid-template-columns:minmax(0,1fr) 64px 70px 68px;
      gap:8px;
      align-items:start;
    }

    .route-title {
      font-weight:850;
      font-size:11px;
      color:#f6f8fa;
    }

    .car {
      display:inline-block;
      margin-top:4px;
      border-radius:999px;
      padding:3px 6px;
      background:color-mix(in srgb, var(--route) 18%, transparent);
      color:color-mix(in srgb, var(--route) 75%, white);
      font-size:8px;
      font-weight:800;
    }

    .rmetric {
      text-align:right;
      min-width:0;
    }

    .rmetric span {
      display:block;
      color:#8799aa;
      font-size:7.5px;
      margin-bottom:2px;
    }

    .rmetric b {
      display:block;
      color:#f3f6f9;
      font-size:10px;
      white-space:nowrap;
    }

    .stops {
      border-top:1px solid rgba(255,255,255,.055);
      margin-top:7px;
      padding-top:6px;
      color:#a6b5c2;
      font-size:8px;
      line-height:1.35;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    .routes-footer {
      text-align:right;
      color:#4da4ff;
      font-size:8.5px;
      padding-top:1px;
    }

    /* CHART */
    .chart-wrap {
      height:225px;
      padding:0 10px 9px;
    }

    /* TABLE */
    .table-scroll {
      overflow:auto;
      height:225px;
      border-top:1px solid rgba(255,255,255,.035);
    }

    table {
      width:100%;
      border-collapse:collapse;
      min-width:650px;
      font-size:8px;
    }

    th, td {
      padding:7px 7px;
      text-align:left;
      border-bottom:1px solid rgba(255,255,255,.05);
      white-space:nowrap;
    }

    th {
      position:sticky;
      top:0;
      background:#132535;
      color:#9eafbf;
      font-weight:750;
      z-index:1;
    }

    td { color:#e3e9ef; }

    .risk {
      display:inline-flex;
      align-items:center;
      gap:4px;
      padding:2px 5px;
      border-radius:999px;
      font-weight:850;
      font-size:7px;
    }

    .risk.high { background:rgba(255,78,87,.15); color:#ff8e94; }
    .risk.mid { background:rgba(255,157,49,.15); color:#ffc16c; }
    .risk.low { background:rgba(69,200,106,.14); color:#8ae19c; }

    /* ALERTS */
    .alerts {
      padding:0 9px 9px;
      display:flex;
      flex-direction:column;
      gap:6px;
    }

    .alert {
      display:grid;
      grid-template-columns:26px minmax(0,1fr) 33px 41px;
      gap:7px;
      align-items:center;
      min-height:40px;
      padding:6px 7px;
      border-radius:9px;
      border:1px solid #263b4d;
      background:#101f2d;
    }

    .alert-icon {
      width:26px;
      height:26px;
      display:grid;
      place-items:center;
      border-radius:8px;
      background:rgba(255,255,255,.04);
      font-size:12px;
    }

    .alert-text {
      min-width:0;
      color:#e5ebf1;
      font-size:8.5px;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    .alert-time {
      color:#8b9daf;
      font-size:7.5px;
      text-align:right;
    }

    .sev {
      font-size:7px;
      font-weight:850;
      text-align:center;
      padding:3px 4px;
      border-radius:6px;
    }

    .sev.critical { background:#cf343c; color:white; }
    .sev.high { background:#d7801b; color:white; }
    .sev.medium { background:#aa7a12; color:white; }
    .sev.info { background:#2369b8; color:white; }

    /* TOAST */
    .toast {
      position:fixed;
      right:18px;
      bottom:18px;
      z-index:5000;
      max-width:310px;
      padding:10px 12px;
      border-radius:10px;
      border:1px solid #324a5e;
      background:#132635;
      color:white;
      font-size:10px;
      box-shadow:0 18px 50px rgba(0,0,0,.35);
      opacity:0;
      pointer-events:none;
      transform:translateY(8px);
      transition:.18s ease;
    }

    .toast.show {
      opacity:1;
      transform:translateY(0);
    }

    @media (max-width:1100px) {
      .shell { grid-template-columns:78px minmax(0,1fr); }
      .brand-name, .nav .text, .sidebar-status { display:none; }
      .brand { justify-content:center; }
      .nav button { justify-content:center; padding:9px; }
      .filters { grid-template-columns:repeat(3,1fr); }
      .kpis { grid-template-columns:repeat(3,1fr); }
      .grid-main, .grid-bottom { grid-template-columns:1fr; }
      .profile-text { display:none; }
      #map { height:360px; }
    }
  </style>

  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="logo-mark"><span>VB</span></div>
        <div class="brand-name">VakıfBank</div>
      </div>

      <div class="nav">
        <button class="active" data-page="Dashboard"><span class="nav-ico">▦</span><span class="text">Dashboard</span></button>
        <button data-page="ATM İzleme"><span class="nav-ico">▤</span><span class="text">ATM İzleme</span></button>
        <button data-page="Talep Tahmini"><span class="nav-ico">⌁</span><span class="text">Talep Tahmini</span></button>
        <button data-page="Kritik Önceliklendirme"><span class="nav-ico">⚠</span><span class="text">Kritik Önceliklendirme</span></button>
        <button data-page="Nakit Optimizasyonu"><span class="nav-ico">₺</span><span class="text">Nakit Optimizasyonu</span></button>
        <button data-page="Rota Planlama"><span class="nav-ico">⌖</span><span class="text">Rota Planlama</span></button>
        <button data-page="Senaryolar"><span class="nav-ico">◫</span><span class="text">Senaryolar</span></button>
        <button data-page="Raporlar"><span class="nav-ico">▥</span><span class="text">Raporlar</span></button>
      </div>

      <div class="sidebar-status">
        <div>Son Güncelleme</div>
        <strong>15.05.2025 08:30</strong>
        <div class="sys"><i></i>Tüm sistemler normal</div>
      </div>
    </aside>

    <main class="main">
      <div class="topbar">
        <div class="header-left">
          <button type="button" class="menu-btn" id="menuBtn" aria-label="Menüyü daralt">☰</button>
          <div class="title-wrap">
            <h1 class="title">Doğu Karadeniz ATM Nakit Yönetimi Karar Destek Sistemi</h1>
            <div class="subtitle">VakıfBank – Bölgesel Operasyon Paneli</div>
          </div>
        </div>

        <div class="profile">
          <div class="bell">🔔<b>3</b></div>
          <div class="avatar">OY</div>
          <div class="profile-text">
            <strong>Operasyon Yöneticisi</strong>
            <span>Bölge Operasyon</span>
          </div>
        </div>
      </div>

      <form class="filters" id="filters">
        <div class="field">
          <label>Bölge</label>
          <select id="region">
            <option value="all">Doğu Karadeniz</option>
            <option value="Trabzon">Trabzon</option>
            <option value="Rize">Rize</option>
            <option value="Ordu">Ordu</option>
            <option value="Giresun">Giresun</option>
            <option value="Artvin">Artvin</option>
          </select>
        </div>

        <div class="field">
          <label>Tarih</label>
          <input id="date" type="date" value="2025-05-15">
        </div>

        <div class="field">
          <label>Senaryo</label>
          <select id="scenario">
            <option>Gerçekleşen Talep</option>
            <option>Yoğun Talep</option>
            <option>Düşük Talep</option>
            <option>Turizm Sezonu</option>
          </select>
        </div>

        <div class="field">
          <label>Araç Sayısı</label>
          <select id="vehicles">
            <option>4</option>
            <option>5</option>
            <option selected>6</option>
            <option>7</option>
            <option>8</option>
          </select>
        </div>

        <div class="field">
          <label>Hizmet Seviyesi</label>
          <select id="service">
            <option>90</option>
            <option selected>95</option>
            <option>98</option>
            <option>99</option>
          </select>
        </div>

        <button type="button" id="clearBtn" class="filter-btn">Filtreleri Temizle</button>
        <button type="submit" class="filter-btn apply">Uygula</button>
      </form>

      <section class="kpis">
        <article class="kpi">
          <div class="kpi-icon blue">ATM</div>
          <div>
            <div class="kpi-label">Toplam ATM</div>
            <div class="kpi-value" id="kpiTotal">285</div>
            <div class="kpi-note" id="kpiRegion">5 il genelinde</div>
          </div>
        </article>

        <article class="kpi">
          <div class="kpi-icon green">₺</div>
          <div>
            <div class="kpi-label">Bugün İkmal Gereken</div>
            <div class="kpi-value" id="kpiRefill">42</div>
            <div class="kpi-note good">↓ %14,7</div>
          </div>
        </article>

        <article class="kpi">
          <div class="kpi-icon red">!</div>
          <div>
            <div class="kpi-label">Kritik ATM</div>
            <div class="kpi-value" id="kpiCritical">12</div>
            <div class="kpi-note bad">↑ %4,2</div>
          </div>
        </article>

        <article class="kpi">
          <div class="kpi-icon purple">▥</div>
          <div>
            <div class="kpi-label">Tahmini Nakit Talebi</div>
            <div class="kpi-value" id="kpiDemand">₺68,4 M</div>
            <div class="kpi-note">Bugün</div>
          </div>
        </article>

        <article class="kpi">
          <div class="kpi-icon cyan">↗</div>
          <div>
            <div class="kpi-label">Rota Verimliliği</div>
            <div class="kpi-value" id="kpiEff">%87</div>
            <div class="kpi-note" id="effTarget">Hedef: %85+</div>
          </div>
        </article>
      </section>

      <section class="grid-main">
        <article class="panel">
          <div class="panel-head">
            <div>
              <h2>Doğu Karadeniz ATM Dağılımı ve Kritiklik</h2>
              <p>ATM noktaları kritiklik seviyesine göre renklendirilmiştir.</p>
            </div>
          </div>

          <div class="map-wrap">
            <div class="map-legend">
              <strong>Kritiklik Seviyesi</strong>
              <div><i class="legend-dot" style="background:#45c86a"></i>Düşük (0–30%)</div>
              <div><i class="legend-dot" style="background:#ffbf00"></i>Orta (30–70%)</div>
              <div><i class="legend-dot" style="background:#ff4e57"></i>Yüksek (70%+)</div>
            </div>
            <div id="map"></div>
          </div>
        </article>

        <article class="panel">
          <div class="panel-head">
            <div>
              <h2>Bugünkü Optimum Rotalar</h2>
              <p id="routeSubtitle">6 araçlık operasyon senaryosu</p>
            </div>
            <button type="button" class="ghost-btn" id="allRoutesBtn">Tüm Rotaları Gör</button>
          </div>
          <div class="routes" id="routes"></div>
        </article>
      </section>

      <section class="grid-bottom">
        <article class="panel">
          <div class="panel-head">
            <div>
              <h2>7 Günlük Nakit Talep Tahmini</h2>
              <p>Milyon TL</p>
            </div>
          </div>
          <div class="chart-wrap">
            <canvas id="demandChart"></canvas>
          </div>
        </article>

        <article class="panel">
          <div class="panel-head">
            <div>
              <h2>ATM Kritiklik ve Önerilen Nakit</h2>
              <p>En yüksek öncelikli ATM'ler</p>
            </div>
          </div>
          <div class="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>ATM Kodu</th>
                  <th>İl</th>
                  <th>Mevcut Nakit</th>
                  <th>24s Tahmin</th>
                  <th>Kritiklik</th>
                  <th>Önerilen Nakit</th>
                  <th>Risk</th>
                  <th>Sonraki İkmal</th>
                </tr>
              </thead>
              <tbody id="atmTable"></tbody>
            </table>
          </div>
        </article>

        <article class="panel">
          <div class="panel-head">
            <div>
              <h2>Operasyon Uyarıları</h2>
              <p>Otomatik karar destek bildirimleri</p>
            </div>
          </div>
          <div class="alerts" id="alerts"></div>
        </article>
      </section>
    </main>
  </div>

  <div class="toast" id="toast"></div>
</div>

<!-- Leaflet -->
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>

<script>
(function(){
  const ATM_DATA = [
    {code:"ATM-015",city:"Trabzon",district:"Ortahisar",lat:41.0027,lng:39.7168,cash:25200,forecast:85600,risk:"high"},
    {code:"ATM-018",city:"Trabzon",district:"Akçaabat",lat:41.0219,lng:39.5717,cash:46200,forecast:41400,risk:"low"},
    {code:"ATM-021",city:"Trabzon",district:"Yomra",lat:40.9548,lng:39.8644,cash:32100,forecast:49100,risk:"mid"},
    {code:"ATM-024",city:"Trabzon",district:"Vakfıkebir",lat:41.0453,lng:39.2767,cash:38400,forecast:35600,risk:"low"},
    {code:"ATM-042",city:"Rize",district:"Merkez",lat:41.0255,lng:40.5177,cash:18500,forecast:72300,risk:"high"},
    {code:"ATM-044",city:"Rize",district:"Çayeli",lat:41.0897,lng:40.7301,cash:27400,forecast:49800,risk:"mid"},
    {code:"ATM-047",city:"Rize",district:"Ardeşen",lat:41.1911,lng:40.9875,cash:19800,forecast:52400,risk:"high"},
    {code:"ATM-009",city:"Artvin",district:"Hopa",lat:41.3907,lng:41.4227,cash:14800,forecast:48200,risk:"mid"},
    {code:"ATM-011",city:"Artvin",district:"Merkez",lat:41.1828,lng:41.8183,cash:35700,forecast:32100,risk:"low"},
    {code:"ATM-031",city:"Giresun",district:"Merkez",lat:40.9128,lng:38.3895,cash:33000,forecast:39700,risk:"mid"},
    {code:"ATM-028",city:"Giresun",district:"Bulancak",lat:40.9372,lng:38.2318,cash:48700,forecast:28100,risk:"low"},
    {code:"ATM-034",city:"Giresun",district:"Tirebolu",lat:41.0064,lng:38.8135,cash:21300,forecast:44200,risk:"mid"},
    {code:"ATM-022",city:"Ordu",district:"Altınordu",lat:40.9862,lng:37.8797,cash:41200,forecast:28900,risk:"low"},
    {code:"ATM-025",city:"Ordu",district:"Fatsa",lat:41.0268,lng:37.5014,cash:18600,forecast:55300,risk:"high"},
    {code:"ATM-026",city:"Ordu",district:"Ünye",lat:41.1272,lng:37.2887,cash:30200,forecast:40700,risk:"mid"}
  ];

  const SUMMARY = {
    all:{atm:285,refill:42,critical:12,demand:68.4},
    Trabzon:{atm:68,refill:10,critical:4,demand:16.3},
    Rize:{atm:54,refill:11,critical:5,demand:13.0},
    Ordu:{atm:63,refill:8,critical:2,demand:15.1},
    Giresun:{atm:58,refill:7,critical:1,demand:13.9},
    Artvin:{atm:42,refill:6,critical:2,demand:10.1}
  };

  const ROUTES = [
    {id:"TRB-01",vehicle:"34 AAF 123",km:286,time:"6sa 45dk",cost:6420,color:"#3f83f8",stops:"Trabzon Merkez → Akçaabat → Vakfıkebir → Rize Merkez → Ardeşen",cities:["Trabzon","Rize"]},
    {id:"GRS-01",vehicle:"61 AAC 456",km:312,time:"7sa 10dk",cost:6980,color:"#45c86a",stops:"Giresun Merkez → Bulancak → Espiye → Tirebolu → Görele",cities:["Giresun"]},
    {id:"ORD-01",vehicle:"52 ABB 789",km:278,time:"6sa 20dk",cost:6150,color:"#ffbf00",stops:"Ordu Merkez → Ünye → Fatsa → Perşembe → Giresun Merkez",cities:["Ordu","Giresun"]},
    {id:"RZE-01",vehicle:"08 ABC 418",km:224,time:"5sa 35dk",cost:5210,color:"#9b7cff",stops:"Rize Merkez → Çayeli → Ardeşen → Hopa → Artvin",cities:["Rize","Artvin"]}
  ];

  const COLORS = {high:"#ff4e57",mid:"#ffbf00",low:"#45c86a"};
  const scenarioMultiplier = name =>
    name==="Yoğun Talep" ? 1.18 :
    name==="Düşük Talep" ? .84 :
    name==="Turizm Sezonu" ? 1.12 : 1;

  const fmtTL = n => "₺" + new Intl.NumberFormat("tr-TR").format(Math.round(n));
  const riskLabel = r => r==="high" ? "Yüksek" : r==="mid" ? "Orta" : "Düşük";
  const riskClass = r => r==="high" ? "high" : r==="mid" ? "mid" : "low";

  function toast(msg){
    const el = document.getElementById("toast");
    el.textContent = msg;
    el.classList.add("show");
    clearTimeout(toast.timer);
    toast.timer = setTimeout(()=>el.classList.remove("show"),1800);
  }

  document.querySelectorAll(".nav button").forEach(btn=>{
    btn.addEventListener("click",()=>{
      document.querySelectorAll(".nav button").forEach(b=>b.classList.remove("active"));
      btn.classList.add("active");
      if(btn.dataset.page!=="Dashboard"){
        toast(btn.dataset.page + " bu prototipte menü örneği olarak gösteriliyor.");
      }
    });
  });

  document.getElementById("menuBtn").addEventListener("click",()=>{
    document.querySelector(".shell").classList.toggle("collapsed");
    setTimeout(()=>{ if(map) map.invalidateSize(); },220);
  });

  let map, markerLayer;
  function markerIcon(risk){
    return L.divIcon({
      className:"",
      html:`<div style="width:14px;height:14px;border-radius:50%;background:${COLORS[risk]};border:2px solid #fff;box-shadow:0 0 0 3px ${COLORS[risk]}33,0 4px 12px rgba(0,0,0,.3)"></div>`,
      iconSize:[14,14],
      iconAnchor:[7,7]
    });
  }

  function initMap(){
    map = L.map("map",{zoomControl:true,attributionControl:true}).setView([41.04,39.65],7);

    // Uydu görüntüsü
    L.tileLayer(
      "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
      {maxZoom:18, attribution:"Tiles © Esri"}
    ).addTo(map);

    // Yer adları/etiket katmanı
    L.tileLayer(
      "https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}{r}.png",
      {subdomains:"abcd", maxZoom:19, opacity:.85, attribution:"© CARTO"}
    ).addTo(map);

    markerLayer = L.layerGroup().addTo(map);
    renderMarkers("all");
  }

  function renderMarkers(region){
    markerLayer.clearLayers();
    const list = ATM_DATA.filter(a=>region==="all" || a.city===region);
    const bounds = [];

    list.forEach(a=>{
      L.marker([a.lat,a.lng],{icon:markerIcon(a.risk)})
        .bindPopup(`
          <strong>${a.code}</strong><br>
          ${a.city} / ${a.district}<br><br>
          Mevcut Nakit: <b>${fmtTL(a.cash)}</b><br>
          24s Tahmin: <b>${fmtTL(a.forecast)}</b><br>
          Kritiklik: <b>${riskLabel(a.risk)}</b>
        `)
        .addTo(markerLayer);
      bounds.push([a.lat,a.lng]);
    });

    if(bounds.length){
      map.fitBounds(bounds,{padding:[18,18],maxZoom:9});
    }
  }

  let chart;
  const baseForecast=[68.4,71.2,65.8,60.3,67.9,72.6,69.1];

  function initChart(){
    const ctx=document.getElementById("demandChart");
    chart=new Chart(ctx,{
      type:"line",
      data:{
        labels:["15 May","16 May","17 May","18 May","19 May","20 May","21 May"],
        datasets:[{
          data:baseForecast,
          borderColor:"#4d9cff",
          backgroundColor:"rgba(77,156,255,.13)",
          fill:true,
          tension:.36,
          pointRadius:3,
          pointHoverRadius:5,
          pointBackgroundColor:"#d8ebff",
          pointBorderColor:"#4d9cff",
          borderWidth:2
        }]
      },
      options:{
        responsive:true,
        maintainAspectRatio:false,
        plugins:{
          legend:{display:false},
          tooltip:{
            callbacks:{label:c=>" "+c.parsed.y.toFixed(1).replace(".",",")+" M TL"}
          }
        },
        scales:{
          x:{
            ticks:{color:"#8da0b1",font:{size:8}},
            grid:{display:false}
          },
          y:{
            ticks:{color:"#8da0b1",font:{size:8}},
            grid:{color:"rgba(255,255,255,.055)"},
            suggestedMin:45,
            suggestedMax:85
          }
        }
      }
    });
  }

  function renderRoutes(region,vehicleCount){
    const box=document.getElementById("routes");
    const f=Math.max(.86,Math.min(1.18,6/Number(vehicleCount)));

    const relevant = region==="all"
      ? ROUTES.slice(0,3)
      : [...ROUTES.filter(r=>r.cities.includes(region)), ...ROUTES.filter(r=>!r.cities.includes(region))].slice(0,3);

    box.innerHTML = relevant.map((r,i)=>`
      <div class="route" style="--route:${r.color}">
        <div class="route-top">
          <div>
            <div class="route-title">🚚 Rota ${i+1} – ${r.id}</div>
            <span class="car">Araç ${r.vehicle}</span>
          </div>
          <div class="rmetric"><span>Toplam Km</span><b>${Math.round(r.km*f)} km</b></div>
          <div class="rmetric"><span>Toplam Süre</span><b>${r.time}</b></div>
          <div class="rmetric"><span>Maliyet</span><b>${fmtTL(r.cost*f)}</b></div>
        </div>
        <div class="stops">⌖ ${r.stops}</div>
      </div>
    `).join("") + `<div class="routes-footer">Tüm 6 rotayı listele ›</div>`;
  }

  function renderTable(region,mult){
    const list=ATM_DATA
      .filter(a=>region==="all" || a.city===region)
      .map(a=>({...a,adj:a.forecast*mult}))
      .sort((a,b)=>{
        const score=r=>r==="high"?3:r==="mid"?2:1;
        return score(b.risk)-score(a.risk) || b.adj-a.adj;
      })
      .slice(0,7);

    document.getElementById("atmTable").innerHTML=list.map(a=>{
      const rec=Math.max(0,(a.adj-a.cash)*1.15);
      const next = a.risk==="high" ? "15.05.2025 12:00" : a.risk==="mid" ? "15.05.2025 16:00" : "16.05.2025 10:00";
      return `
        <tr>
          <td>${a.code}</td>
          <td>${a.city}</td>
          <td>${new Intl.NumberFormat("tr-TR").format(a.cash)}</td>
          <td>${new Intl.NumberFormat("tr-TR").format(Math.round(a.adj))}</td>
          <td><span class="risk ${riskClass(a.risk)}">● ${riskLabel(a.risk)}</span></td>
          <td>${new Intl.NumberFormat("tr-TR").format(Math.round(rec))}</td>
          <td>${riskLabel(a.risk)}</td>
          <td>${next}</td>
        </tr>
      `;
    }).join("");
  }

  function renderAlerts(region){
    const list=ATM_DATA
      .filter(a=>region==="all" || a.city===region)
      .filter(a=>a.risk!=="low")
      .slice(0,4);

    const rows=list.map((a,i)=>{
      const high=a.risk==="high";
      const text = high
        ? `${a.city} ${a.district} ${a.code}: kritik nakit seviyesine yaklaşıyor`
        : `${a.city} ${a.district} ${a.code}: ikmal planı gözden geçirilmeli`;
      return `
        <div class="alert">
          <div class="alert-icon">${high?"⚠":"!"}</div>
          <div class="alert-text">${text}</div>
          <div class="alert-time">${["08:15","07:45","07:30","06:50"][i] || "06:30"}</div>
          <div class="sev ${high?"critical":"medium"}">${high?"Kritik":"Orta"}</div>
        </div>
      `;
    });

    if(!rows.length){
      rows.push(`
        <div class="alert">
          <div class="alert-icon">i</div>
          <div class="alert-text">Seçili bölgede kritik operasyon uyarısı bulunmuyor.</div>
          <div class="alert-time">—</div>
          <div class="sev info">Bilgi</div>
        </div>
      `);
    }

    document.getElementById("alerts").innerHTML=rows.join("");
  }

  function updateDashboard(){
    const region=document.getElementById("region").value;
    const scenario=document.getElementById("scenario").value;
    const vehicles=Number(document.getElementById("vehicles").value);
    const service=Number(document.getElementById("service").value);
    const mult=scenarioMultiplier(scenario);
    const s=SUMMARY[region];

    const refill=Math.max(1,Math.round(s.refill*mult));
    const critical=Math.max(1,Math.round(s.critical*(1+Math.max(0,mult-1)*.8)));
    const demand=s.demand*mult;
    const efficiency=Math.max(78,Math.min(94,Math.round(84+(vehicles-4)*1.1+(service-90)*.18-Math.max(0,mult-1)*16)));

    document.getElementById("kpiTotal").textContent=s.atm;
    document.getElementById("kpiRegion").textContent=region==="all"?"5 il genelinde":region+" bölgesi";
    document.getElementById("kpiRefill").textContent=refill;
    document.getElementById("kpiCritical").textContent=critical;
    document.getElementById("kpiDemand").textContent="₺"+demand.toFixed(1).replace(".",",")+" M";
    document.getElementById("kpiEff").textContent="%"+efficiency;
    document.getElementById("effTarget").textContent="Hedef: %"+service+"+";
    document.getElementById("routeSubtitle").textContent=vehicles+" araçlık operasyon senaryosu";

    renderMarkers(region);
    renderRoutes(region,vehicles);
    renderTable(region,mult);
    renderAlerts(region);

    const regionFactor=s.demand/68.4;
    chart.data.datasets[0].data=baseForecast.map(v=>Number((v*regionFactor*mult).toFixed(1)));
    chart.update();
  }

  document.getElementById("filters").addEventListener("submit",e=>{
    e.preventDefault();
    updateDashboard();
    toast("Dashboard güncellendi.");
  });

  document.getElementById("clearBtn").addEventListener("click",()=>{
    document.getElementById("region").value="all";
    document.getElementById("date").value="2025-05-15";
    document.getElementById("scenario").value="Gerçekleşen Talep";
    document.getElementById("vehicles").value="6";
    document.getElementById("service").value="95";
    updateDashboard();
    toast("Filtreler temizlendi.");
  });

  document.getElementById("allRoutesBtn").addEventListener("click",()=>{
    toast("Bu prototipte üç optimum rota özet olarak gösteriliyor.");
  });

  initMap();
  initChart();
  renderRoutes("all",6);s
  renderTable("all",1);
  renderAlerts("all");
})();
</script>
"""

components.html(
    APP,
    height=1010,
    scrolling=True,
)
