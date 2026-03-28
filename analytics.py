"""
pages/analytics.py  — Analytics (Beta / Demo)
"""

import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random


# ── Color palette ─────────────────────────────────────────────────────────────
AMBER = "#F59E0B"
RED = "#EF4444"
GREEN = "#10B981"
BLUE = "#3B82F6"
NAVY = "#111827"
GRID = "#1E2A3A"
TEXT = "#8A9BB0"

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=NAVY,
    font=dict(family="IBM Plex Mono", color=TEXT, size=11),
    xaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(size=10)),
    yaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(size=10)),
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID),
)


# ── Simulated data generators ─────────────────────────────────────────────────
def _gen_price_series(start: float, n: int, seed: int, vol: float = 1.5) -> list:
    rng = np.random.default_rng(seed)
    prices = [start]
    for _ in range(n - 1):
        prices.append(max(0.1, prices[-1] + rng.normal(0, vol)))
    return prices


def _gen_dates(n: int, freq: str = "M") -> list:
    end = datetime(2024, 12, 1)
    return pd.date_range(end=end, periods=n, freq=freq).tolist()


# ── Charts ────────────────────────────────────────────────────────────────────
def chart_price_history() -> go.Figure:
    n = 36
    dates = _gen_dates(n)
    wti = _gen_price_series(75, n, seed=1, vol=2.5)
    brent = [w + random.uniform(1.5, 4.5) for w in wti]
    gas = _gen_price_series(3.2, n, seed=7, vol=0.25)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=wti, name="WTI", line=dict(color=AMBER, width=2), mode="lines"))
    fig.add_trace(go.Scatter(
        x=dates, y=brent, name="Brent", line=dict(color=BLUE, width=2), mode="lines"))

    fig.update_layout(**CHART_LAYOUT, title=dict(
        text="WTI vs Brent — 36 Month Simulated History",
        font=dict(family="Bebas Neue", size=16, color="#E8E0D0"), x=0))
    fig.update_yaxes(title_text="USD / barrel")
    return fig


def chart_natural_gas() -> go.Figure:
    n = 36
    dates = _gen_dates(n)
    gas = _gen_price_series(3.0, n, seed=99, vol=0.3)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=gas, name="Henry Hub",
        fill="tozeroy",
        fillcolor=f"rgba(239,68,68,0.08)",
        line=dict(color=RED, width=2),
        mode="lines"))
    fig.update_layout(**CHART_LAYOUT, title=dict(
        text="Henry Hub Natural Gas — Demo Price Series",
        font=dict(family="Bebas Neue", size=16, color="#E8E0D0"), x=0))
    fig.update_yaxes(title_text="USD / MMBtu")
    return fig


def chart_spread() -> go.Figure:
    n = 36
    dates = _gen_dates(n)
    wti = _gen_price_series(75, n, seed=1, vol=2.5)
    spread = [random.uniform(1.0, 6.0) for _ in range(n)]
    colors = [GREEN if s > 3 else RED for s in spread]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dates, y=spread,
        name="Brent-WTI Spread",
        marker_color=colors,
        opacity=0.85))
    fig.add_hline(y=3, line_dash="dot", line_color=AMBER,
                  annotation_text="avg 3.0", annotation_font_color=AMBER)
    fig.update_layout(**CHART_LAYOUT, title=dict(
        text="Brent–WTI Spread ($/bbl) — Demo Data",
        font=dict(family="Bebas Neue", size=16, color="#E8E0D0"), x=0))
    return fig


def chart_energy_mix() -> go.Figure:
    labels = ["Oil", "Natural Gas", "Coal", "Nuclear", "Renewables", "Other"]
    values = [31, 27, 22, 10, 8, 2]
    colors_pie = [AMBER, RED, "#6B7A90", BLUE, GREEN, "#3D4F65"]

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55,
        marker=dict(colors=colors_pie, line=dict(color=NAVY, width=2)),
        textfont=dict(family="IBM Plex Mono", size=11),
        insidetextorientation="radial",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Mono", color=TEXT),
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="v"),
        margin=dict(l=0, r=0, t=30, b=0),
        title=dict(
            text="Global Energy Mix — Illustrative",
            font=dict(family="Bebas Neue", size=16, color="#E8E0D0"), x=0),
    )
    return fig


def chart_volatility() -> go.Figure:
    n = 36
    dates = _gen_dates(n)
    vol_wti = [abs(np.random.normal(12, 5)) for _ in range(n)]
    vol_gas = [abs(np.random.normal(20, 8)) for _ in range(n)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=vol_wti, name="WTI Volatility",
        line=dict(color=AMBER, width=1.5, dash="solid"), mode="lines"))
    fig.add_trace(go.Scatter(
        x=dates, y=vol_gas, name="Gas Volatility",
        line=dict(color=RED, width=1.5, dash="dot"), mode="lines"))
    fig.update_layout(**CHART_LAYOUT, title=dict(
        text="Implied Volatility Index — Demo Model",
        font=dict(family="Bebas Neue", size=16, color="#E8E0D0"), x=0))
    fig.update_yaxes(title_text="Volatility (%)")
    return fig


# ── Page render ───────────────────────────────────────────────────────────────
def render():
    st.markdown("""
    <div class="section-header" style="margin-bottom:20px;">
        <div class="section-tag">Analytics</div>
        <h1 style="margin:0;font-size:3rem;color:#E8E0D0;">Data Analytics</h1>
    </div>
    """, unsafe_allow_html=True)

    # Beta banner
    st.markdown("""
    <div style="background:linear-gradient(90deg,#1a1200,#0B0F1A);
                border:1px solid #F59E0B44;border-radius:8px;
                padding:14px 20px;margin-bottom:28px;
                display:flex;align-items:center;gap:12px;">
        <span style="font-size:1.4rem;">🧪</span>
        <div>
            <div style="font-family:Bebas Neue,sans-serif;font-size:1.1rem;
                        color:#F59E0B;letter-spacing:0.08em;">
                BETA / DEMO — ILLUSTRATIVE DATA ONLY
            </div>
            <div style="font-family:IBM Plex Sans,sans-serif;font-size:0.78rem;
                        color:#6B7A90;margin-top:3px;">
                This section uses simulated data for demonstration purposes.
                Live analytical models are under development and will be released in upcoming issues.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📈  Price History", "⚖️  Spreads & Ratios", "🌍  Market Structure"])

    with tab1:
        st.plotly_chart(chart_price_history(), use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(chart_natural_gas(), use_container_width=True)

    with tab2:
        st.plotly_chart(chart_spread(), use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(chart_volatility(), use_container_width=True)

    with tab3:
        col_left, col_right = st.columns([1, 1], gap="large")
        with col_left:
            st.plotly_chart(chart_energy_mix(), use_container_width=True)
        with col_right:
            st.markdown("""
            <div style="padding:16px 0;">
                <div class="section-tag" style="margin-bottom:12px;">Models in Development</div>
            </div>""", unsafe_allow_html=True)

            roadmap = [
                ("Q1 2025", "Price forecasting model (ARIMA / XGBoost)", "🔄 In progress"),
                ("Q2 2025", "Supply-demand balance indicator", "📌 Planned"),
                ("Q2 2025", "Geopolitical risk score overlay", "📌 Planned"),
                ("Q3 2025", "Cross-commodity correlation matrix", "📌 Planned"),
                ("Q3 2025", "Seasonal pattern decomposition", "📌 Planned"),
            ]
            for period, model, status in roadmap:
                st.markdown(f"""
                <div style="background:#111827;border:1px solid #1E2A3A;border-radius:6px;
                            padding:12px 16px;margin-bottom:8px;">
                    <div style="font-family:IBM Plex Mono,monospace;font-size:0.65rem;
                                color:#F59E0B;letter-spacing:0.12em;">{period}</div>
                    <div style="font-family:IBM Plex Sans,sans-serif;font-size:0.85rem;
                                color:#E8E0D0;margin:4px 0;">{model}</div>
                    <div style="font-family:IBM Plex Mono,monospace;font-size:0.65rem;
                                color:#6B7A90;">{status}</div>
                </div>""", unsafe_allow_html=True)
