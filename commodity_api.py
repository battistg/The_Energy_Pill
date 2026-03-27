"""
utils/commodity_api.py
Fetches WTI, Brent and Natural Gas prices from Alpha Vantage.
Results are cached for 8 hours to stay within the 25-calls/day limit.
"""

import requests
import streamlit as st
from datetime import datetime

API_KEY = "HC5JO3UM4O7IP3GV"
BASE_URL = "https://www.alphavantage.co/query"

COMMODITIES = {
    "WTI": {
        "function": "WTI",
        "label": "WTI Crude",
        "unit": "USD / barrel",
        "emoji": "🛢️",
    },
    "BRENT": {
        "function": "BRENT",
        "label": "Brent Crude",
        "unit": "USD / barrel",
        "emoji": "🛢️",
    },
    "NATURAL_GAS": {
        "function": "NATURAL_GAS",
        "label": "Henry Hub Gas",
        "unit": "USD / MMBtu",
        "emoji": "🔥",
    },
}


def _fetch_single(function: str) -> dict | None:
    """
    Call Alpha Vantage for one commodity.
    Returns the full JSON response or None on error.
    """
    params = {
        "function": function,
        "interval": "monthly",
        "apikey": API_KEY,
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.warning(f"API error for {function}: {e}")
        return None


def _parse_latest(data: dict) -> tuple[float | None, float | None, str | None]:
    """
    Extract the two most recent data points from the API response.
    Returns (latest_value, previous_value, latest_date_str).
    """
    if data is None:
        return None, None, None
    series = data.get("data", [])
    # Filter out entries with '.' as value (missing data)
    valid = [d for d in series if d.get("value") not in (".", "", None)]
    if len(valid) < 1:
        return None, None, None
    latest = float(valid[0]["value"])
    previous = float(valid[1]["value"]) if len(valid) >= 2 else None
    date_str = valid[0].get("date", "")
    return latest, previous, date_str


# Cache for 8 hours (28800 seconds)
@st.cache_data(ttl=28800, show_spinner=False)
def fetch_all_prices() -> dict:
    """
    Fetch prices for all three commodities.
    Cached for 8 hours.
    Returns a dict keyed by commodity ID with price info.
    """
    results = {}
    for key, meta in COMMODITIES.items():
        raw = _fetch_single(meta["function"])
        latest, previous, date = _parse_latest(raw)
        if latest is not None and previous is not None:
            change = latest - previous
            change_pct = (change / previous) * 100
        else:
            change = None
            change_pct = None

        results[key] = {
            "label": meta["label"],
            "unit": meta["unit"],
            "emoji": meta["emoji"],
            "price": latest,
            "previous": previous,
            "change": change,
            "change_pct": change_pct,
            "date": date,
        }
    return results


def get_cache_info() -> str:
    """Return a human-readable string about when data was last fetched."""
    now = datetime.now()
    return now.strftime("%d %b %Y — %H:%M UTC")
