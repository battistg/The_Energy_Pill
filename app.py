import streamlit as st

st.set_page_config(
    page_title="The Energy Pill",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,600;1,300&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    background-color: #0B0F1A;
    color: #E8E0D0;
    font-family: 'IBM Plex Sans', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #080C15 !important;
    border-right: 1px solid #1E2A3A;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {
    color: #8A9BB0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ── Sidebar nav links ── */
.nav-link {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.15s;
    text-decoration: none;
    color: #8A9BB0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.nav-link:hover { background: #111827; color: #E8E0D0; }
.nav-link.active { background: #1E2A3A; color: #F59E0B; border-left: 2px solid #F59E0B; }

/* ── Headings ── */
h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 0.05em;
}

/* ── Metric cards ── */
.metric-card {
    background: #111827;
    border: 1px solid #1E2A3A;
    border-radius: 8px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #F59E0B, #EF4444);
}
.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6B7A90;
    margin-bottom: 8px;
}
.metric-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem;
    color: #E8E0D0;
    line-height: 1;
}
.metric-change-up {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: #10B981;
    margin-top: 6px;
}
.metric-change-down {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: #EF4444;
    margin-top: 6px;
}
.metric-unit {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #6B7A90;
    margin-top: 4px;
}

/* ── Section header ── */
.section-header {
    border-bottom: 1px solid #1E2A3A;
    padding-bottom: 12px;
    margin-bottom: 24px;
}
.section-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #F59E0B;
    margin-bottom: 4px;
}

/* ── News card ── */
.news-card {
    background: #111827;
    border: 1px solid #1E2A3A;
    border-radius: 6px;
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: border-color 0.15s;
}
.news-card:hover { border-color: #F59E0B44; }
.news-title {
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    color: #E8E0D0;
    margin-bottom: 6px;
    line-height: 1.4;
}
.news-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #6B7A90;
    letter-spacing: 0.05em;
}
.news-source {
    color: #F59E0B;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent;
    border: 1px solid #F59E0B;
    color: #F59E0B;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-radius: 4px;
    transition: all 0.15s;
}
.stButton > button:hover {
    background: #F59E0B;
    color: #0B0F1A;
}

/* ── Divider ── */
hr { border-color: #1E2A3A; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #1E2A3A;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6B7A90;
    background: transparent;
    border: none;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    color: #F59E0B !important;
    border-bottom: 2px solid #F59E0B !important;
    background: transparent !important;
}

/* ── Misc ── */
.stSpinner > div { border-top-color: #F59E0B !important; }
.stAlert { background: #111827; border-color: #1E2A3A; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 24px 0;'>
        <div style='font-family: Bebas Neue, sans-serif; font-size: 1.8rem;
                    color: #F59E0B; letter-spacing: 0.08em; line-height:1;'>
            ⚡ THE ENERGY PILL
        </div>
        <div style='font-family: IBM Plex Mono, monospace; font-size: 0.6rem;
                    color: #3D4F65; letter-spacing: 0.2em; text-transform: uppercase;
                    margin-top: 4px;'>
            Real-time Energy Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-family:IBM Plex Mono,monospace;font-size:0.65rem;color:#3D4F65;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:8px;'>Navigation</div>", unsafe_allow_html=True)

    pages = {
        "🏠  Market Overview": "Home",
        "📰  News Feed": "News",
        "📊  Analytics": "Analytics",
        "📋  Monthly Issue": "Issue",
    }

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    for label, page_id in pages.items():
        is_active = st.session_state.current_page == page_id
        btn_style = "primary" if is_active else "secondary"
        if st.button(label, key=f"nav_{page_id}", use_container_width=True):
            st.session_state.current_page = page_id
            st.rerun()

    st.markdown("<hr style='border-color:#1E2A3A;margin:24px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:IBM Plex Mono,monospace;font-size:0.6rem;color:#3D4F65;
                letter-spacing:0.1em;line-height:1.8;'>
        Data: Alpha Vantage / EIA<br>
        News: Google News RSS<br>
        Prices refresh: every 8h<br>
        <br>
        <span style='color:#1E2A3A;'>v0.1 — beta</span>
    </div>
    """, unsafe_allow_html=True)

# ── Page routing ─────────────────────────────────────────────────────────────
page = st.session_state.current_page

if page == "Home":
    from pages.home import render
    render()
elif page == "News":
    from pages.news import render
    render()
elif page == "Analytics":
    from pages.analytics import render
    render()
elif page == "Issue":
    from pages.issue import render
    render()
