"""
pages/home.py  — Market Overview
"""

import streamlit as st
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from utils.commodity_api import fetch_all_prices, get_cache_info


def _price_card(key: str, data: dict) -> str:
    price = data["price"]
    change = data["change"]
    change_pct = data["change_pct"]

    if price is None:
        return f"""
        <div class="metric-card">
            <div class="metric-label">{data['emoji']} {data['label']}</div>
            <div class="metric-value" style="font-size:1.4rem;color:#3D4F65;">N/A</div>
            <div class="metric-unit">{data['unit']}</div>
        </div>"""

    if change_pct is not None:
        sign = "+" if change_pct >= 0 else ""
        arrow = "▲" if change_pct >= 0 else "▼"
        css_cls = "metric-change-up" if change_pct >= 0 else "metric-change-down"
        change_html = f"""<div class="{css_cls}">{arrow} {sign}{change_pct:.2f}% &nbsp;
            <span style="color:#3D4F65;">vs prev month</span></div>"""
    else:
        change_html = ""

    date_label = f"<div class='metric-unit'>Latest: {data.get('date','—')}</div>"

    return f"""
    <div class="metric-card">
        <div class="metric-label">{data['emoji']} {data['label']}</div>
        <div class="metric-value">${price:,.2f}</div>
        {change_html}
        <div class="metric-unit">{data['unit']}</div>
        {date_label}
    </div>"""


def render():
    # ── Page header ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header" style="margin-bottom:32px;">
        <div class="section-tag">Market Overview</div>
        <h1 style="margin:0;font-size:3rem;color:#E8E0D0;">Energy Prices</h1>
        <p style="font-family:'IBM Plex Sans',sans-serif;color:#6B7A90;
                  font-size:0.85rem;margin-top:8px;font-style:italic;">
            Spot prices for key energy commodities — monthly data via EIA / Alpha Vantage
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Fetch data ────────────────────────────────────────────────────────────
    with st.spinner("Fetching commodity prices..."):
        prices = fetch_all_prices()

    # ── Ticker strip ─────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3, gap="medium")
    cols = [col1, col2, col3]
    keys = ["WTI", "BRENT", "NATURAL_GAS"]

    for col, key in zip(cols, keys):
        with col:
            st.markdown(_price_card(key, prices[key]), unsafe_allow_html=True)

    # ── Cache / refresh info ──────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    info_col, btn_col = st.columns([4, 1])
    with info_col:
        st.markdown(f"""
        <div style='font-family:IBM Plex Mono,monospace;font-size:0.65rem;
                    color:#3D4F65;letter-spacing:0.1em;'>
            ⏱ DATA LOADED: {get_cache_info()} &nbsp;·&nbsp;
            CACHE: 8H (25 API calls/day limit) &nbsp;·&nbsp;
            SOURCE: EIA VIA ALPHA VANTAGE
        </div>
        """, unsafe_allow_html=True)
    with btn_col:
        if st.button("↻ Force Refresh", key="refresh_prices"):
            fetch_all_prices.clear()
            st.rerun()

    # ── Spread section ────────────────────────────────────────────────────────
    st.markdown("<hr style='border-color:#1E2A3A;margin:32px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-tag" style="margin-bottom:8px;">Key Differentials</div>
    """, unsafe_allow_html=True)

    wti_price = prices["WTI"]["price"]
    brent_price = prices["BRENT"]["price"]
    gas_price = prices["NATURAL_GAS"]["price"]

    if wti_price and brent_price and gas_price:
        spread = brent_price - wti_price
        spread_sign = "+" if spread >= 0 else ""

        d1, d2, d3 = st.columns(3, gap="medium")
        with d1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📐 Brent / WTI Spread</div>
                <div class="metric-value" style="font-size:2rem;">
                    {spread_sign}${spread:.2f}
                </div>
                <div class="metric-unit">Brent premium over WTI</div>
            </div>""", unsafe_allow_html=True)
        with d2:
            ratio = brent_price / gas_price if gas_price else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⚖️ Oil-to-Gas Ratio</div>
                <div class="metric-value" style="font-size:2rem;">{ratio:.1f}x</div>
                <div class="metric-unit">Brent ($/bbl) ÷ HH ($/MMBtu)</div>
            </div>""", unsafe_allow_html=True)
        with d3:
            # Rough barrel equivalent: 1 bbl ≈ 5.8 MMBtu
            oil_btu_equiv = wti_price / 5.8 if wti_price else 0
            premium = oil_btu_equiv - gas_price
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🔄 Oil vs Gas (BTU basis)</div>
                <div class="metric-value" style="font-size:2rem;">${premium:.2f}</div>
                <div class="metric-unit">WTI/btu equiv. premium vs HH gas</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Spread data unavailable — prices could not be loaded.", icon="ℹ️")

    # ── Context note ──────────────────────────────────────────────────────────
    st.markdown("<hr style='border-color:#1E2A3A;margin:32px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#080C15;border:1px solid #1E2A3A;border-radius:6px;
                padding:16px 20px;'>
        <div class="section-tag" style="margin-bottom:8px;">ℹ️ Data notes</div>
        <div style='font-family:IBM Plex Sans,sans-serif;font-size:0.82rem;
                    color:#6B7A90;line-height:1.7;'>
            • <b style="color:#8A9BB0;">WTI Crude</b>: West Texas Intermediate, 
              Cushing OK — benchmark for US crude.<br>
            • <b style="color:#8A9BB0;">Brent Crude</b>: North Sea benchmark — 
              global reference price for ~2/3 of world oil contracts.<br>
            • <b style="color:#8A9BB0;">Henry Hub</b>: US natural gas spot price 
              at the Henry Hub, Louisiana pipeline interchange.<br>
            • Prices shown are <b style="color:#8A9BB0;">monthly averages</b> 
              from the EIA via the FRED API. Data refreshes every 8 hours.
        </div>
    </div>
    """, unsafe_allow_html=True)
