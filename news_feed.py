"""
utils/news_feed.py
Fetches energy-related news from Google News RSS feeds using keyword queries.
Results are cached for 30 minutes.
"""

import feedparser
import streamlit as st
from datetime import datetime
import time
import urllib.parse

# ── Keyword query groups ─────────────────────────────────────────────────────
KEYWORD_GROUPS = {
    "Oil & Gas": [
        "crude oil price",
        "WTI Brent oil",
        "OPEC oil production",
        "natural gas LNG",
        "oil refinery",
    ],
    "Energy Markets": [
        "energy market prices",
        "electricity prices Europe",
        "energy crisis",
        "power grid",
        "energy transition",
    ],
    "Renewables": [
        "solar energy investment",
        "wind power offshore",
        "renewable energy policy",
        "battery storage energy",
    ],
    "Geopolitics": [
        "energy geopolitics",
        "Russia gas pipeline",
        "Middle East oil",
        "energy sanctions",
        "energy security",
    ],
}

MAX_ITEMS_PER_QUERY = 5  # articles per keyword
CACHE_TTL = 1800  # 30 minutes


def _build_rss_url(query: str) -> str:
    encoded = urllib.parse.quote(query)
    return f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"


def _parse_date(entry) -> str:
    """Return a formatted date string from an RSS entry."""
    try:
        t = entry.get("published_parsed") or entry.get("updated_parsed")
        if t:
            return datetime(*t[:6]).strftime("%d %b %Y")
    except Exception:
        pass
    return "—"


def _fetch_single_feed(query: str) -> list[dict]:
    """Fetch and parse one RSS feed query."""
    url = _build_rss_url(query)
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:MAX_ITEMS_PER_QUERY]:
            title = entry.get("title", "").strip()
            link = entry.get("link", "#")
            source_detail = entry.get("source", {})
            source = source_detail.get("title", "Google News")
            pub_date = _parse_date(entry)
            # Clean up Google News redirect titles (format: "Title - Source")
            if " - " in title:
                parts = title.rsplit(" - ", 1)
                title = parts[0].strip()
                if not source or source == "Google News":
                    source = parts[1].strip()
            items.append({
                "title": title,
                "link": link,
                "source": source,
                "date": pub_date,
                "query": query,
            })
        return items
    except Exception:
        return []


def _deduplicate(articles: list[dict]) -> list[dict]:
    """Remove duplicate titles (case-insensitive)."""
    seen = set()
    unique = []
    for a in articles:
        key = a["title"].lower()[:80]
        if key not in seen:
            seen.add(key)
            unique.append(a)
    return unique


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_news_by_category() -> dict[str, list[dict]]:
    """
    Fetch news for every category/keyword group.
    Returns dict: {category_name: [article, ...]}
    Cached for 30 minutes.
    """
    result = {}
    for category, queries in KEYWORD_GROUPS.items():
        all_articles = []
        for q in queries:
            all_articles.extend(_fetch_single_feed(q))
            time.sleep(0.1)  # be polite
        result[category] = _deduplicate(all_articles)
    return result


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_all_news_flat() -> list[dict]:
    """Return all articles as a flat deduplicated list."""
    by_cat = fetch_news_by_category()
    flat = []
    for articles in by_cat.values():
        flat.extend(articles)
    return _deduplicate(flat)
