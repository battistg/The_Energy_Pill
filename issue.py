"""
pages/issue.py  — Monthly Issue
"""

import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st


def render():
    st.markdown("""
    <div class="section-header" style="margin-bottom:32px;">
        <div class="section-tag">Monthly Issue</div>
        <h1 style="margin:0;font-size:3rem;color:#E8E0D0;">The Energy Pill</h1>
        <p style="font-family:'IBM Plex Sans',sans-serif;color:#6B7A90;
                  font-size:0.85rem;margin-top:8px;font-style:italic;">
            In-depth analysis · Published monthly
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Issue 01 — Coming Soon ────────────────────────────────────────────────
    st.markdown("""
    <div style="
        position: relative;
        background: linear-gradient(135deg, #0D1520 0%, #111827 60%, #0D1a10 100%);
        border: 1px solid #1E2A3A;
        border-radius: 12px;
        padding: 48px 40px;
        overflow: hidden;
        margin-bottom: 32px;
    ">
        <!-- Decorative large issue number -->
        <div style="
            position: absolute;
            top: -20px; right: -10px;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 14rem;
            color: #0F1A25;
            line-height: 1;
            pointer-events: none;
            user-select: none;
        ">01</div>

        <!-- Badge -->
        <div style="
            display: inline-block;
            background: #F59E0B18;
            border: 1px solid #F59E0B44;
            color: #F59E0B;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.65rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            padding: 5px 12px;
            border-radius: 4px;
            margin-bottom: 20px;
        ">Issue 01 · Coming Soon</div>

        <!-- Title -->
        <h2 style="
            font-family: 'Bebas Neue', sans-serif;
            font-size: 3.2rem;
            color: #E8E0D0;
            margin: 0 0 8px 0;
            line-height: 1.05;
            max-width: 680px;
            position: relative;
        ">
            Crisis Unplugged:<br>
            <span style="color:#10B981;">The Hidden Flaws</span><br>
            in Australia's Energy System
        </h2>

        <!-- Subtitle line -->
        <div style="
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, #F59E0B, #EF4444);
            margin: 20px 0 24px 0;
        "></div>

        <!-- Teaser text -->
        <p style="
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 1.0rem;
            color: #8A9BB0;
            line-height: 1.8;
            max-width: 620px;
            position: relative;
        ">
            Australia presents itself as a clean energy leader — abundant sun, wind,
            and LNG exports that power much of Asia. Yet beneath the surface, 
            its domestic energy market is riddled with structural tensions: 
            aging coal infrastructure, a fractured grid, soaring household bills, 
            and policy whiplash that has spooked investors for over a decade.
        </p>
        <p style="
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 0.9rem;
            color:#6B7A90;
            line-height: 1.7;
            max-width: 580px;
            margin-top: 12px;
            font-style: italic;
            position: relative;
        ">
            In Issue 01, we unpack the design failures behind the National Electricity Market, 
            the gas export paradox, and what the energy transition really looks like 
            when the economics refuse to cooperate.
        </p>

        <!-- Tags -->
        <div style="margin-top:28px;display:flex;flex-wrap:wrap;gap:8px;position:relative;">
    """, unsafe_allow_html=True)

    tags = ["Australia", "NEM", "LNG", "Energy Policy", "Grid Stability",
            "Coal Transition", "Renewables", "Market Design"]
    tags_html = "".join([
        f"""<span style="background:#111827;border:1px solid #1E2A3A;
                         color:#6B7A90;font-family:'IBM Plex Mono',monospace;
                         font-size:0.65rem;letter-spacing:0.1em;text-transform:uppercase;
                         padding:4px 10px;border-radius:4px;">{t}</span>"""
        for t in tags
    ])

    st.markdown(f"""
        {tags_html}
        </div>

        <!-- Estimated release -->
        <div style="
            margin-top: 32px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem;
            color: #3D4F65;
            letter-spacing: 0.12em;
            position: relative;
        ">
            ✦ ESTIMATED RELEASE: APRIL 2025 &nbsp;·&nbsp; 
            ISSUE LENGTH: ~3,000 WORDS &nbsp;·&nbsp; 
            DATA PACK INCLUDED
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Notify me ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-tag" style="margin-bottom:12px;">Stay Updated</div>
    """, unsafe_allow_html=True)

    notify_col, _ = st.columns([2, 2])
    with notify_col:
        email = st.text_input(
            "Get notified when Issue 01 drops",
            placeholder="your@email.com",
            label_visibility="collapsed",
        )
        if st.button("Notify me →", key="notify_btn"):
            if "@" in email:
                st.success(f"✓ We'll notify {email} when Issue 01 is published.", icon="✅")
            else:
                st.warning("Please enter a valid email address.", icon="⚠️")

    # ── Archive placeholder ───────────────────────────────────────────────────
    st.markdown("<hr style='border-color:#1E2A3A;margin:40px 0 28px;'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-tag" style="margin-bottom:16px;">Issue Archive</div>
    <div style="background:#080C15;border:1px dashed #1E2A3A;border-radius:8px;
                padding:32px;text-align:center;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;
                    color:#3D4F65;letter-spacing:0.1em;">
            Archive builds as issues are published
        </div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;
                    color:#3D4F65;margin-top:8px;">
            Issue 01 will appear here on publication
        </div>
    </div>
    """, unsafe_allow_html=True)
