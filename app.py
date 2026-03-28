import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st

st.set_page_config(
    page_title="The Energy Pill",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,600;1,300&display=swap');
html, body, [class*="css"] { background-color: #0B0F1A; color: #E8E0D0; font-family: 'IBM Plex Sans', sans-serif; }
[data-testid="stSidebar"] { background: #080C15 !important; border-right: 1px solid #1E2A3A; }
h1, h2, h3 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 0.05em; }
.metric-card { background: #111827; border: 1px solid #1E2A3A; border-radius: 8px; padding: 20px 24px; position: relative; overflow: hidden; }
.metric-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #F59E0B, #EF4444); }
.metric-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: #6B7A90; margin-bottom: 8px; }
.metric-value { font-family: 'Bebas Neue', sans-serif; font-size: 2.6rem; color: #E8E0D0; line-height: 1; }
.metric-change-up { font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; color: #10B981; margin-top: 6px; }
.metric-change-down { font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; color: #EF4444; margin-top: 6px; }
.metric-unit { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #6B7A90; margin-top: 4px; }
.section-header { border-bottom: 1px solid #1E2A3A; padding-bottom: 12px; margin-bottom: 24px; }
.section-tag { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; color: #F59E0B; margin-bottom: 4px; }
.news-card { background: #111827; border: 1px solid #1E2A3A; border-radius: 6px; padding: 16px 20px; margin-bottom: 12px; }
.news-title { font-family: 'IBM Plex Sans', sans-serif; font-weight: 600; font-size: 0.95rem; color: #E8E0D0; margin-bottom: 6px; line-height: 1.4; }
.news-meta { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: #6B7A90; letter-spacing: 0.05em; }
.news-source { color: #F59E0B; }
.stButton > button { background: transparent; border: 1px solid #F59E0B; color: #F59E0B; font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; border-radius: 4px; }
.stButton > button:hover { background: #F59E0B; color: #0B0F1A; }
hr { border-color: #1E2A3A; }
.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid #1E2A3A; }
.stTabs [data-baseweb="tab"] { font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6B7A90; background: transparent; border: none; }
.stTabs [aria-selected="true"] { color: #F59E0B !important; border-bottom: 2px solid #F59E0B !important; background: transparent !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 24px 0;'>
        <div style='font-family: Bebas Neue, sans-serif; font-size: 1.8rem; color: #F59E0B; letter-spacing: 0.08em; line-height:1;'>⚡ THE ENERGY PILL</div>
        <div style='font-family: IBM Plex Mono, monospace; font-size: 0.6rem; color: #3D4F65; letter-spacing: 0.2em; text-transform: uppercase; margin-top: 4px;'>Real-time Energy Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    pages = {
        "🏠  Market Overview": "Home",
        "📰  News Feed": "News",
        "📊  Analytics": "Analytics",
        "📋  Monthly Issue": "Issue",
    }
    for label, page_id in pages.items():
        if st.button(label, key=f"nav_{page_id}", use_container_width=True):
            st.session_state.current_page = page_id
            st.rerun()

    st.markdown("<hr style='border-color:#1E2A3A;margin:24px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:IBM Plex Mono,monospace;font-size:0.6rem;color:#3D4F65;letter-spacing:0.1em;line-height:1.8;'>Data: Alpha Vantage / EIA<br>News: Google News RSS<br>Prices refresh: every 8h<br><br>v0.1 — beta</div>", unsafe_allow_html=True)

page = st.session_state.current_page

if page == "Home":
    from sections.home import render
    render()
elif page == "News":
    from sections.news import render
    render()
elif page == "Analytics":
    from sections.analytics import render
    render()
elif page == "Issue":
    from sections.issue import render
    render()
