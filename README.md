# The Energy Pill — Setup Guide

Real-time energy market intelligence dashboard built with Streamlit.

---

## Project Structure

```
the_energy_pill/
│
├── app.py                  ← Entry point (run this)
│
├── pages/
│   ├── home.py             ← Market Overview (commodity prices)
│   ├── news.py             ← Energy News Feed (RSS)
│   ├── analytics.py        ← Analytics (beta/demo)
│   └── issue.py            ← Monthly Issue
│
├── utils/
│   ├── commodity_api.py    ← Alpha Vantage API wrapper (8h cache)
│   └── news_feed.py        ← Google News RSS fetcher (30min cache)
│
├── requirements.txt
└── README.md
```

---

## Prerequisites

- **Python 3.10+** recommended
- An internet connection (for live API calls and RSS)

---

## Installation

### 1. Clone / download the project

Place the `the_energy_pill/` folder wherever you like.

### 2. Create a virtual environment (recommended)

```bash
cd the_energy_pill
python -m venv venv

# Activate:
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the App

```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

---

## API Key & Caching

The Alpha Vantage API key is already embedded in `utils/commodity_api.py`:

```python
API_KEY = "HC5JO3UM4O7IP3GV"
```

**Caching rules:**
| Data | Cache TTL | Calls/day |
|------|-----------|-----------|
| WTI price | 8 hours | 3 (one per commodity) |
| Brent price | 8 hours | — |
| Henry Hub gas | 8 hours | — |
| News RSS | 30 minutes | Unlimited (Google) |

With 3 commodities × 3 refreshes/day = **9 calls/day** (well under the 25/day free limit).

To force a refresh manually, use the **↻ Force Refresh** button on the Market Overview page.

---

## Customising Keywords (News)

Edit `utils/news_feed.py` — the `KEYWORD_GROUPS` dictionary:

```python
KEYWORD_GROUPS = {
    "Oil & Gas": [
        "crude oil price",
        "OPEC oil production",
        ...
    ],
    "My New Category": [
        "my keyword 1",
        "my keyword 2",
    ],
}
```

---

## Deploying to Streamlit Cloud (Free)

1. Push this folder to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set the main file to `app.py`
4. Click **Deploy**

For Streamlit Cloud, you can optionally move `API_KEY` to **Secrets**:
- In the Streamlit Cloud dashboard → App settings → Secrets
- Add: `ALPHA_VANTAGE_KEY = "HC5JO3UM4O7IP3GV"`
- Then in `commodity_api.py`: `API_KEY = st.secrets["ALPHA_VANTAGE_KEY"]`

---

## Next Steps / Roadmap

- [ ] Add daily interval prices (higher resolution, more API calls)
- [ ] Build price history chart on Home page using last 12 months of data
- [ ] Add email notification system for Monthly Issue
- [ ] Integrate real analytical models in Analytics section
- [ ] Add electricity price feeds (ENTSO-E, AEMO for Australia)
- [ ] Publish Issue 01: "Crisis Unplugged: The Hidden Flaws in Australia's Energy System"
