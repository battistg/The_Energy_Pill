"""
pages/news.py  — Energy News Feed
"""

import streamlit as st
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from utils.news_feed import fetch_news_by_category, fetch_all_news_flat


def _article_card(article: dict) -> str:
    return f"""
    <div class="news-card">
        <div class="news-title">
            <a href="{article['link']}" target="_blank"
               style="color:#E8E0D0;text-decoration:none;">
                {article['title']}
            </a>
        </div>
        <div class="news-meta">
            <span class="news-source">{article['source']}</span>
            &nbsp;·&nbsp;{article['date']}
        </div>
    </div>"""


def render():
    st.markdown("""
    <div class="section-header" style="margin-bottom:32px;">
        <div class="section-tag">Live Feed</div>
        <h1 style="margin:0;font-size:3rem;color:#E8E0D0;">Energy News</h1>
        <p style="font-family:'IBM Plex Sans',sans-serif;color:#6B7A90;
                  font-size:0.85rem;margin-top:8px;font-style:italic;">
            Aggregated from Google News · Keyword-filtered for energy market relevance
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Controls row ──────────────────────────────────────────────────────────
    ctrl_col, refresh_col = st.columns([5, 1])
    with ctrl_col:
        view_mode = st.radio(
            "View",
            ["All News", "By Category"],
            horizontal=True,
            label_visibility="collapsed",
        )
    with refresh_col:
        if st.button("↻ Refresh", key="refresh_news"):
            fetch_news_by_category.clear()
            fetch_all_news_flat.clear()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Fetch ─────────────────────────────────────────────────────────────────
    if view_mode == "All News":
        with st.spinner("Loading news..."):
            articles = fetch_all_news_flat()

        if not articles:
            st.warning("No articles found. Check your internet connection or try again.", icon="⚠️")
            return

        st.markdown(f"""
        <div style='font-family:IBM Plex Mono,monospace;font-size:0.68rem;
                    color:#3D4F65;letter-spacing:0.1em;margin-bottom:20px;'>
            {len(articles)} ARTICLES LOADED · REFRESHED EVERY 30 MIN
        </div>""", unsafe_allow_html=True)

        # Search filter
        search = st.text_input(
            "🔍 Filter articles",
            placeholder="Type to filter by keyword...",
            label_visibility="collapsed",
        )
        if search:
            articles = [a for a in articles if search.lower() in a["title"].lower()
                        or search.lower() in a["source"].lower()]
            st.markdown(f"""<div style='font-family:IBM Plex Mono,monospace;
                font-size:0.68rem;color:#F59E0B;margin-bottom:12px;'>
                ↳ {len(articles)} results for "{search}"</div>""",
                unsafe_allow_html=True)

        for article in articles:
            st.markdown(_article_card(article), unsafe_allow_html=True)

    else:
        # By Category
        with st.spinner("Loading news by category..."):
            by_cat = fetch_news_by_category()

        category_icons = {
            "Oil & Gas": "🛢️",
            "Energy Markets": "📈",
            "Renewables": "🌱",
            "Geopolitics": "🌍",
        }

        for category, articles in by_cat.items():
            icon = category_icons.get(category, "📰")
            with st.expander(f"{icon}  {category}  ({len(articles)} articles)", expanded=True):
                if not articles:
                    st.markdown("<div style='color:#3D4F65;font-size:0.8rem;padding:8px;'>"
                                "No articles found for this category.</div>",
                                unsafe_allow_html=True)
                else:
                    for article in articles:
                        st.markdown(_article_card(article), unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("<hr style='border-color:#1E2A3A;margin:32px 0 16px;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:IBM Plex Mono,monospace;font-size:0.62rem;color:#3D4F65;'>
        NEWS SOURCED VIA GOOGLE NEWS RSS · NOT FINANCIAL ADVICE ·
        ALL RIGHTS BELONG TO RESPECTIVE PUBLISHERS
    </div>""", unsafe_allow_html=True)
