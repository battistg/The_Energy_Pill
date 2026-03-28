import sys
import os
import time
import urllib.parse
from datetime import datetime

import streamlit as st
import requests
import feedparser
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Energy Pill",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS  — written as a plain string variable, no heredoc
# ─────────────────────────────────────────────────────────────────────────────
CSS = (
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue"
    "&family=IBM+Plex+Mono:wght@400;600"
    "&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,600;1,300&display=swap');"
    "html,body,[class*='css']{background-color:#0B0F1A;color:#E8E0D0;font-family:'IBM Plex Sans',sans-serif;}"
    "[data-testid='stSidebar']{background:#080C15 !important;border-right:1px solid #1E2A3A;}"
    "h1,h2,h3{font-family:'Bebas Neue',sans-serif;letter-spacing:0.05em;}"
    ".metric-card{background:#111827;border:1px solid #1E2A3A;border-radius:8px;"
    "padding:20px 24px;position:relative;overflow:hidden;margin-bottom:4px;}"
    ".metric-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;"
    "background:linear-gradient(90deg,#F59E0B,#EF4444);}"
    ".metric-label{font-family:'IBM Plex Mono',monospace;font-size:0.7rem;"
    "letter-spacing:0.15em;text-transform:uppercase;color:#6B7A90;margin-bottom:8px;}"
    ".metric-value{font-family:'Bebas Neue',sans-serif;font-size:2.6rem;color:#E8E0D0;line-height:1;}"
    ".metric-change-up{font-family:'IBM Plex Mono',monospace;font-size:0.8rem;color:#10B981;margin-top:6px;}"
    ".metric-change-down{font-family:'IBM Plex Mono',monospace;font-size:0.8rem;color:#EF4444;margin-top:6px;}"
    ".metric-unit{font-family:'IBM Plex Mono',monospace;font-size:0.7rem;color:#6B7A90;margin-top:4px;}"
    ".section-header{border-bottom:1px solid #1E2A3A;padding-bottom:12px;margin-bottom:24px;}"
    ".section-tag{font-family:'IBM Plex Mono',monospace;font-size:0.65rem;"
    "letter-spacing:0.2em;text-transform:uppercase;color:#F59E0B;margin-bottom:4px;}"
    ".news-card{background:#111827;border:1px solid #1E2A3A;border-radius:6px;"
    "padding:16px 20px;margin-bottom:12px;}"
    ".news-title{font-family:'IBM Plex Sans',sans-serif;font-weight:600;font-size:0.95rem;"
    "color:#E8E0D0;margin-bottom:6px;line-height:1.4;}"
    ".news-meta{font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:#6B7A90;letter-spacing:0.05em;}"
    ".news-source{color:#F59E0B;}"
    ".stButton>button{background:transparent;border:1px solid #F59E0B;color:#F59E0B;"
    "font-family:'IBM Plex Mono',monospace;font-size:0.75rem;letter-spacing:0.1em;"
    "text-transform:uppercase;border-radius:4px;}"
    ".stButton>button:hover{background:#F59E0B;color:#0B0F1A;}"
    "hr{border-color:#1E2A3A;}"
    ".stTabs [data-baseweb='tab-list']{background:transparent;border-bottom:1px solid #1E2A3A;}"
    ".stTabs [data-baseweb='tab']{font-family:'IBM Plex Mono',monospace;font-size:0.75rem;"
    "letter-spacing:0.1em;text-transform:uppercase;color:#6B7A90;background:transparent;border:none;}"
    ".stTabs [aria-selected='true']{color:#F59E0B !important;"
    "border-bottom:2px solid #F59E0B !important;background:transparent !important;}"
    "</style>"
)
st.markdown(CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# COMMODITY API  (Alpha Vantage, cached 8 h)
# ─────────────────────────────────────────────────────────────────────────────
API_KEY = "HC5JO3UM4O7IP3GV"
BASE_URL = "https://www.alphavantage.co/query"

COMMODITIES = {
    "WTI":         {"function": "WTI",         "label": "WTI Crude",     "unit": "USD / barrel", "emoji": "🛢️"},
    "BRENT":       {"function": "BRENT",        "label": "Brent Crude",   "unit": "USD / barrel", "emoji": "🛢️"},
    "NATURAL_GAS": {"function": "NATURAL_GAS",  "label": "Henry Hub Gas", "unit": "USD / MMBtu",  "emoji": "🔥"},
}


@st.cache_data(ttl=28800, show_spinner=False)
@st.cache_data(ttl=1800, show_spinner=False)  # 30 min cache (più "real-time")
def fetch_all_prices():

    TICKERS = {
        "WTI": "CL=F",
        "BRENT": "BZ=F",
        "NATURAL_GAS": "NG=F",
    }

    results = {}

    for key, ticker in TICKERS.items():
        meta = COMMODITIES[key]

        try:
            data = yf.download(
                ticker,
                period="2d",       # ultimi 2 giorni
                interval="1d",     # daily close
                progress=False,
            )

            if data.empty or len(data) < 1:
                raise ValueError("No data")

            latest = float(data["Close"].iloc[-1])
            previous = float(data["Close"].iloc[-2]) if len(data) > 1 else None
            date = data.index[-1].strftime("%d %b %Y")

        except Exception:
            latest = previous = None
            date = ""

        change = (latest - previous) if (latest and previous) else None
        change_pct = (change / previous * 100) if (change and previous) else None

        results[key] = {
            **meta,
            "price": latest,
            "previous": previous,
            "change": change,
            "change_pct": change_pct,
            "date": date,
        }

    return results


# ─────────────────────────────────────────────────────────────────────────────
# NEWS FEED  (Google News RSS, cached 30 min)
# ─────────────────────────────────────────────────────────────────────────────
KEYWORD_GROUPS = {
    "Oil & Gas":      ["crude oil price", "WTI Brent oil", "OPEC oil production", "natural gas LNG"],
    "Energy Markets": ["energy market prices", "electricity prices", "energy crisis", "energy transition"],
    "Renewables":     ["solar energy investment", "wind power offshore", "renewable energy policy"],
    "Geopolitics":    ["energy geopolitics", "Russia gas pipeline", "Middle East oil", "energy sanctions"],
}


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_news_by_category():
    result = {}
    for cat, queries in KEYWORD_GROUPS.items():
        seen, articles = set(), []
        for q in queries:
            url = (
                "https://news.google.com/rss/search?q="
                + urllib.parse.quote(q)
                + "&hl=en-US&gl=US&ceid=US:en"
            )
            try:
                feed = feedparser.parse(url)
                for e in feed.entries[:5]:
                    title = e.get("title", "").strip()
                    src   = e.get("source", {}).get("title", "Google News")
                    if " - " in title:
                        title, src = title.rsplit(" - ", 1)
                        title = title.strip()
                        src   = src.strip()
                    k = title.lower()[:80]
                    if k in seen:
                        continue
                    seen.add(k)
                    try:
                        t = e.get("published_parsed") or e.get("updated_parsed")
                        date_str = datetime(*t[:6]).strftime("%d %b %Y") if t else "—"
                    except Exception:
                        date_str = "—"
                    articles.append({
                        "title": title, "link": e.get("link", "#"),
                        "source": src,  "date": date_str,
                    })
            except Exception:
                pass
            time.sleep(0.05)
        result[cat] = articles
    return result


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='padding:8px 0 24px 0;'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;"
        "color:#F59E0B;letter-spacing:0.08em;line-height:1;'>⚡ THE ENERGY PILL</div>"
        "<div style='font-family:IBM Plex Mono,monospace;font-size:0.6rem;"
        "color:#3D4F65;letter-spacing:0.2em;text-transform:uppercase;margin-top:4px;'>"
        "Real-time Energy Intelligence</div></div>",
        unsafe_allow_html=True,
    )

    if "page" not in st.session_state:
        st.session_state.page = "Home"

    nav_items = [
        ("🏠  Market Overview", "Home"),
        ("📰  News Feed",       "News"),
        ("📊  Analytics",       "Analytics"),
        ("📋  Monthly Issue",   "Issue"),
    ]
    for label, pid in nav_items:
        if st.button(label, key="nav_" + pid, use_container_width=True):
            st.session_state.page = pid
            st.rerun()

    st.markdown("<hr style='border-color:#1E2A3A;margin:24px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-family:IBM Plex Mono,monospace;font-size:0.6rem;"
        "color:#3D4F65;line-height:1.8;'>"
        "Data: Alpha Vantage / EIA<br>News: Google News RSS<br>"
        "Prices refresh: every 8h<br><br>v0.1 — beta</div>",
        unsafe_allow_html=True,
    )

page = st.session_state.page


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — MARKET OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if page == "Home":

    st.markdown(
        "<div class='section-header' style='margin-bottom:32px;'>"
        "<div class='section-tag'>Market Overview</div>"
        "<h1 style='margin:0;font-size:3rem;color:#E8E0D0;'>Energy Prices</h1>"
        "<p style='font-family:IBM Plex Sans,sans-serif;color:#6B7A90;"
        "font-size:0.85rem;margin-top:8px;font-style:italic;'>"
        "Spot prices for key energy commodities — monthly data via EIA / Alpha Vantage"
        "</p></div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Fetching commodity prices..."):
        prices = fetch_all_prices()

    c1, c2, c3 = st.columns(3, gap="medium")
    for col, key in zip([c1, c2, c3], ["WTI", "BRENT", "NATURAL_GAS"]):
        d = prices[key]
        with col:
            if d["price"] is None:
                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-label'>" + d["emoji"] + " " + d["label"] + "</div>"
                    "<div class='metric-value' style='font-size:1.4rem;color:#3D4F65;'>N/A</div>"
                    "<div class='metric-unit'>" + d["unit"] + "</div></div>",
                    unsafe_allow_html=True,
                )
            else:
                pct = d["change_pct"]
                if pct is not None:
                    sign  = "+" if pct >= 0 else ""
                    arrow = "▲" if pct >= 0 else "▼"
                    cls   = "metric-change-up" if pct >= 0 else "metric-change-down"
                    chg   = (
                        "<div class='" + cls + "'>"
                        + arrow + " " + sign + "{:.2f}".format(pct)
                        + "% <span style='color:#3D4F65;'>vs prev month</span></div>"
                    )
                else:
                    chg = ""

                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-label'>" + d["emoji"] + " " + d["label"] + "</div>"
                    "<div class='metric-value'>${:,.2f}".format(d["price"]) + "</div>"
                    + chg
                    + "<div class='metric-unit'>" + d["unit"] + "</div>"
                    "<div class='metric-unit'>Latest: " + d["date"] + "</div>"
                    "</div>",
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)
    ic, bc = st.columns([4, 1])
    with ic:
        st.markdown(
            "<div style='font-family:IBM Plex Mono,monospace;font-size:0.65rem;"
            "color:#3D4F65;letter-spacing:0.1em;'>⏱ LOADED: "
            + datetime.now().strftime("%d %b %Y — %H:%M")
            + " · CACHE: 8H · SOURCE: EIA / ALPHA VANTAGE</div>",
            unsafe_allow_html=True,
        )
    with bc:
        if st.button("↻ Force Refresh"):
            fetch_all_prices.clear()
            st.rerun()

    st.markdown("<hr style='border-color:#1E2A3A;margin:32px 0;'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-tag' style='margin-bottom:8px;'>Key Differentials</div>",
        unsafe_allow_html=True,
    )

    wti_p   = prices["WTI"]["price"]
    brent_p = prices["BRENT"]["price"]
    gas_p   = prices["NATURAL_GAS"]["price"]

    if wti_p and brent_p and gas_p:
        spread = brent_p - wti_p
        ratio  = brent_p / gas_p
        equiv  = wti_p / 5.8 - gas_p
        d1, d2, d3 = st.columns(3, gap="medium")
        spread_str = ("+${:.2f}".format(spread) if spread >= 0 else "-${:.2f}".format(abs(spread)))
        for col, label, val, unit in [
            (d1, "📐 Brent / WTI Spread", spread_str,                "Brent premium over WTI"),
            (d2, "⚖️ Oil-to-Gas Ratio",  "{:.1f}x".format(ratio),   "Brent ($/bbl) / HH ($/MMBtu)"),
            (d3, "🔄 Oil vs Gas BTU",    "${:.2f}".format(equiv),    "WTI/btu equiv. premium vs HH"),
        ]:
            with col:
                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-label'>" + label + "</div>"
                    "<div class='metric-value' style='font-size:2rem;'>" + val + "</div>"
                    "<div class='metric-unit'>" + unit + "</div></div>",
                    unsafe_allow_html=True,
                )

    st.markdown("<hr style='border-color:#1E2A3A;margin:32px 0;'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='background:#080C15;border:1px solid #1E2A3A;border-radius:6px;padding:16px 20px;'>"
        "<div class='section-tag' style='margin-bottom:8px;'>Data notes</div>"
        "<div style='font-family:IBM Plex Sans,sans-serif;font-size:0.82rem;color:#6B7A90;line-height:1.7;'>"
        "WTI Crude: West Texas Intermediate, Cushing OK — US crude benchmark.<br>"
        "Brent Crude: North Sea benchmark — global reference for approx. 2/3 of world oil contracts.<br>"
        "Henry Hub: US natural gas spot price at the Henry Hub, Louisiana.<br>"
        "Prices are monthly averages from EIA via FRED API. Data refreshes every 8 hours."
        "</div></div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — NEWS FEED
# ─────────────────────────────────────────────────────────────────────────────
elif page == "News":

    st.markdown(
        "<div class='section-header' style='margin-bottom:32px;'>"
        "<div class='section-tag'>Live Feed</div>"
        "<h1 style='margin:0;font-size:3rem;color:#E8E0D0;'>Energy News</h1>"
        "<p style='font-family:IBM Plex Sans,sans-serif;color:#6B7A90;"
        "font-size:0.85rem;margin-top:8px;font-style:italic;'>"
        "Aggregated from Google News — keyword-filtered for energy market relevance"
        "</p></div>",
        unsafe_allow_html=True,
    )

    vc, rc = st.columns([5, 1])
    with vc:
        view_mode = st.radio("View", ["All News", "By Category"], horizontal=True, label_visibility="collapsed")
    with rc:
        if st.button("↻ Refresh", key="ref_news"):
            fetch_news_by_category.clear()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    with st.spinner("Loading news..."):
        by_cat = fetch_news_by_category()

    cat_icons = {
        "Oil & Gas": "🛢️", "Energy Markets": "📈",
        "Renewables": "🌱", "Geopolitics": "🌍",
    }

    def news_card_html(a):
        return (
            "<div class='news-card'>"
            "<div class='news-title'>"
            "<a href='" + a["link"] + "' target='_blank' "
            "style='color:#E8E0D0;text-decoration:none;'>"
            + a["title"] + "</a></div>"
            "<div class='news-meta'>"
            "<span class='news-source'>" + a["source"] + "</span>"
            " · " + a["date"] + "</div></div>"
        )

    if view_mode == "All News":
        seen, flat = set(), []
        for articles in by_cat.values():
            for a in articles:
                k = a["title"].lower()[:80]
                if k not in seen:
                    seen.add(k)
                    flat.append(a)

        st.markdown(
            "<div style='font-family:IBM Plex Mono,monospace;font-size:0.68rem;"
            "color:#3D4F65;letter-spacing:0.1em;margin-bottom:20px;'>"
            + str(len(flat)) + " ARTICLES — CACHE 30 MIN</div>",
            unsafe_allow_html=True,
        )
        search = st.text_input("Filter", placeholder="Type to filter...", label_visibility="collapsed")
        if search:
            flat = [
                a for a in flat
                if search.lower() in a["title"].lower() or search.lower() in a["source"].lower()
            ]
        for a in flat:
            st.markdown(news_card_html(a), unsafe_allow_html=True)

    else:
        for cat, articles in by_cat.items():
            header = cat_icons.get(cat, "📰") + "  " + cat + "  (" + str(len(articles)) + " articles)"
            with st.expander(header, expanded=True):
                for a in articles:
                    st.markdown(news_card_html(a), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Analytics":

    AMBER = "#F59E0B"
    RED   = "#EF4444"
    GREEN = "#10B981"
    BLUE  = "#3B82F6"
    NAVY  = "#111827"
    GRID  = "#1E2A3A"
    TTEXT = "#8A9BB0"

    CHART_LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=NAVY,
        font=dict(family="IBM Plex Mono", color=TTEXT, size=11),
        xaxis=dict(gridcolor=GRID, linecolor=GRID),
        yaxis=dict(gridcolor=GRID, linecolor=GRID),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID),
    )

    def chart_title(txt):
        return dict(text=txt, font=dict(family="Bebas Neue", size=16, color="#E8E0D0"), x=0)

    rng     = np.random.default_rng(42)
    dates36 = pd.date_range(end="2024-12-01", periods=36, freq="ME").tolist()

    def walk(start, n, vol, seed):
        r = np.random.default_rng(seed)
        p = [float(start)]
        for _ in range(n - 1):
            p.append(max(0.5, p[-1] + float(r.normal(0, vol))))
        return p

    wti_s    = walk(75, 36, 2.5, 1)
    brent_s  = [w + float(rng.uniform(1.5, 4.5)) for w in wti_s]
    gas_s    = walk(3.0, 36, 0.28, 7)
    spread_s = [b - w for b, w in zip(brent_s, wti_s)]
    vol_s    = [abs(float(rng.normal(14, 5))) for _ in range(36)]

    st.markdown(
        "<div class='section-header' style='margin-bottom:20px;'>"
        "<div class='section-tag'>Analytics</div>"
        "<h1 style='margin:0;font-size:3rem;color:#E8E0D0;'>Data Analytics</h1>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='background:linear-gradient(90deg,#1a1200,#0B0F1A);"
        "border:1px solid #F59E0B44;border-radius:8px;padding:14px 20px;margin-bottom:28px;'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:1.1rem;color:#F59E0B;'>"
        "BETA / DEMO — ILLUSTRATIVE DATA ONLY</div>"
        "<div style='font-family:IBM Plex Sans,sans-serif;font-size:0.78rem;color:#6B7A90;margin-top:3px;'>"
        "Simulated data for demonstration. Live analytical models are under development."
        "</div></div>",
        unsafe_allow_html=True,
    )

    t1, t2, t3 = st.tabs(["📈  Price History", "⚖️  Spreads & Volatility", "🌍  Market Structure"])

    with t1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates36, y=wti_s,   name="WTI",   line=dict(color=AMBER, width=2)))
        fig.add_trace(go.Scatter(x=dates36, y=brent_s, name="Brent", line=dict(color=BLUE,  width=2)))
        fig.update_layout(**CHART_LAYOUT, title=chart_title("WTI vs Brent — 36 Month Simulated History"))
        fig.update_yaxes(title_text="USD / barrel")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=dates36, y=gas_s, name="Henry Hub",
            fill="tozeroy", fillcolor="rgba(239,68,68,0.08)",
            line=dict(color=RED, width=2),
        ))
        fig2.update_layout(**CHART_LAYOUT, title=chart_title("Henry Hub Natural Gas — Demo Price Series"))
        fig2.update_yaxes(title_text="USD / MMBtu")
        st.plotly_chart(fig2, use_container_width=True)

    with t2:
        bar_colors = [GREEN if s > 3 else RED for s in spread_s]
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=dates36, y=spread_s, marker_color=bar_colors, opacity=0.85, name="Spread"))
        fig3.add_hline(y=3, line_dash="dot", line_color=AMBER,
                       annotation_text="avg 3.0", annotation_font_color=AMBER)
        fig3.update_layout(**CHART_LAYOUT, title=chart_title("Brent-WTI Spread ($/bbl) — Demo Data"))
        st.plotly_chart(fig3, use_container_width=True)

        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=dates36, y=vol_s, name="Volatility",
            fill="tozeroy", fillcolor="rgba(245,158,11,0.07)",
            line=dict(color=AMBER, width=1.5),
        ))
        fig4.update_layout(**CHART_LAYOUT, title=chart_title("Implied Volatility Index — Demo Model"))
        fig4.update_yaxes(title_text="Volatility (%)")
        st.plotly_chart(fig4, use_container_width=True)

    with t3:
        cl2, cr2 = st.columns([1, 1], gap="large")
        with cl2:
            pie_labels = ["Oil", "Natural Gas", "Coal", "Nuclear", "Renewables", "Other"]
            pie_values = [31, 27, 22, 10, 8, 2]
            pie_colors = [AMBER, RED, "#6B7A90", BLUE, GREEN, "#3D4F65"]
            fig5 = go.Figure(go.Pie(
                labels=pie_labels, values=pie_values, hole=0.55,
                marker=dict(colors=pie_colors, line=dict(color=NAVY, width=2)),
                textfont=dict(family="IBM Plex Mono", size=11),
            ))
            fig5.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="IBM Plex Mono", color=TTEXT),
                legend=dict(bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=0, r=0, t=40, b=0),
                title=chart_title("Global Energy Mix — Illustrative"),
            )
            st.plotly_chart(fig5, use_container_width=True)

        with cr2:
            st.markdown(
                "<div class='section-tag' style='margin-bottom:12px;'>Models in Development</div>",
                unsafe_allow_html=True,
            )
            roadmap = [
                ("Q1 2025", "Price forecasting model (ARIMA / XGBoost)", "🔄 In progress"),
                ("Q2 2025", "Supply-demand balance indicator",            "📌 Planned"),
                ("Q2 2025", "Geopolitical risk score overlay",            "📌 Planned"),
                ("Q3 2025", "Cross-commodity correlation matrix",         "📌 Planned"),
                ("Q3 2025", "Seasonal pattern decomposition",             "📌 Planned"),
            ]
            for period, model, status in roadmap:
                st.markdown(
                    "<div style='background:#111827;border:1px solid #1E2A3A;"
                    "border-radius:6px;padding:12px 16px;margin-bottom:8px;'>"
                    "<div style='font-family:IBM Plex Mono,monospace;font-size:0.65rem;color:#F59E0B;'>"
                    + period + "</div>"
                    "<div style='font-family:IBM Plex Sans,sans-serif;font-size:0.85rem;"
                    "color:#E8E0D0;margin:4px 0;'>" + model + "</div>"
                    "<div style='font-family:IBM Plex Mono,monospace;font-size:0.65rem;"
                    "color:#6B7A90;'>" + status + "</div></div>",
                    unsafe_allow_html=True,
                )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE — MONTHLY ISSUE
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Issue":

    st.markdown(
        "<div class='section-header' style='margin-bottom:32px;'>"
        "<div class='section-tag'>Monthly Issue</div>"
        "<h1 style='margin:0;font-size:3rem;color:#E8E0D0;'>The Energy Pill</h1>"
        "<p style='font-family:IBM Plex Sans,sans-serif;color:#6B7A90;"
        "font-size:0.85rem;margin-top:8px;font-style:italic;'>"
        "In-depth analysis — Published monthly</p></div>",
        unsafe_allow_html=True,
    )

    issue_tags = [
        "Australia", "NEM", "LNG", "Energy Policy",
        "Grid Stability", "Coal Transition", "Renewables", "Market Design",
    ]
    tags_html = " ".join([
        "<span style='background:#111827;border:1px solid #1E2A3A;color:#6B7A90;"
        "font-family:IBM Plex Mono,monospace;font-size:0.65rem;letter-spacing:0.1em;"
        "text-transform:uppercase;padding:4px 10px;border-radius:4px;'>"
        + t + "</span>"
        for t in issue_tags
    ])

    st.markdown(
        "<div style='position:relative;"
        "background:linear-gradient(135deg,#0D1520 0%,#111827 60%,#0D1a10 100%);"
        "border:1px solid #1E2A3A;border-radius:12px;"
        "padding:48px 40px;overflow:hidden;margin-bottom:32px;'>"
        "<div style='position:absolute;top:-20px;right:-10px;"
        "font-family:Bebas Neue,sans-serif;font-size:14rem;"
        "color:#0F1A25;line-height:1;pointer-events:none;user-select:none;'>01</div>"
        "<div style='display:inline-block;background:#F59E0B18;"
        "border:1px solid #F59E0B44;color:#F59E0B;"
        "font-family:IBM Plex Mono,monospace;font-size:0.65rem;letter-spacing:0.2em;"
        "text-transform:uppercase;padding:5px 12px;border-radius:4px;margin-bottom:20px;'>"
        "Issue 01 — Coming Soon</div>"
        "<h2 style='font-family:Bebas Neue,sans-serif;font-size:3.2rem;color:#E8E0D0;"
        "margin:0 0 8px 0;line-height:1.05;max-width:680px;position:relative;'>"
        "Crisis Unplugged:<br>"
        "<span style='color:#10B981;'>The Hidden Flaws</span><br>"
        "in Australia's Energy System</h2>"
        "<div style='width:60px;height:3px;"
        "background:linear-gradient(90deg,#F59E0B,#EF4444);margin:20px 0 24px 0;'></div>"
        "<p style='font-family:IBM Plex Sans,sans-serif;font-size:1.0rem;color:#8A9BB0;"
        "line-height:1.8;max-width:620px;position:relative;'>"
        "Australia presents itself as a clean energy leader — abundant sun, wind, and LNG exports "
        "that power much of Asia. Yet beneath the surface, its domestic energy market is riddled "
        "with structural tensions: aging coal infrastructure, a fractured grid, soaring household "
        "bills, and policy whiplash that has spooked investors for over a decade."
        "</p>"
        "<p style='font-family:IBM Plex Sans,sans-serif;font-size:0.9rem;color:#6B7A90;"
        "line-height:1.7;max-width:580px;margin-top:12px;font-style:italic;position:relative;'>"
        "In Issue 01, we unpack the design failures behind the National Electricity Market, "
        "the gas export paradox, and what the energy transition really looks like when the "
        "economics refuse to cooperate."
        "</p>"
        "<div style='margin-top:28px;display:flex;flex-wrap:wrap;gap:8px;position:relative;'>"
        + tags_html
        + "</div>"
        "<div style='margin-top:32px;font-family:IBM Plex Mono,monospace;font-size:0.7rem;"
        "color:#3D4F65;letter-spacing:0.12em;position:relative;'>"
        "ESTIMATED RELEASE: APRIL 2025 — ISSUE LENGTH: approx. 3,000 WORDS — DATA PACK INCLUDED"
        "</div></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-tag' style='margin-bottom:12px;'>Stay Updated</div>",
        unsafe_allow_html=True,
    )
    nc, _ = st.columns([2, 2])
    with nc:
        email = st.text_input("Notify me", placeholder="your@email.com", label_visibility="collapsed")
        if st.button("Notify me"):
            if "@" in email:
                st.success("We will notify " + email + " when Issue 01 is published.")
            else:
                st.warning("Please enter a valid email address.")

    st.markdown("<hr style='border-color:#1E2A3A;margin:40px 0 28px;'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-tag' style='margin-bottom:16px;'>Issue Archive</div>"
        "<div style='background:#080C15;border:1px dashed #1E2A3A;"
        "border-radius:8px;padding:32px;text-align:center;'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:1.5rem;"
        "color:#3D4F65;letter-spacing:0.1em;'>Archive builds as issues are published</div>"
        "<div style='font-family:IBM Plex Mono,monospace;font-size:0.7rem;"
        "color:#3D4F65;margin-top:8px;'>Issue 01 will appear here on publication</div>"
        "</div>",
        unsafe_allow_html=True,
    )
