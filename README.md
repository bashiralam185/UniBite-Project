# 🍽️ UniBite Mallorca – Business Analytics Dashboard

A professional Streamlit dashboard for the Business Analytics course project (11759, Group 1 Mallorca).

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run unibite_dashboard.py
```

The app will open automatically at http://localhost:8501

---

## Dashboard Sections

| Section | Content |
|---|---|
| 🏠 Overview | Business KPI summary cards, revenue chart, cost breakdown |
| 📊 Level 1 Financials | P&L waterfall, revenue breakdown, assumptions |
| 🎯 KPI Tracker | All 10 KPIs with progress bars, radar chart |
| 🚀 Hypotheses & Actions | Detailed view of all 10 initiatives with cost & ROI |
| 📋 Summary Table | Full colour-coded hypothesis impact matrix |
| 🗂️ Balanced Scorecard | 4-perspective scorecard + 12-month KPI simulation |

---

## Requirements
- Python 3.9+
- Internet connection (for Google Fonts)

## Tip for Presentation
Run `streamlit run unibite_dashboard.py --server.headless false` to open directly in your browser, then use browser fullscreen (F11) for the presentation.
