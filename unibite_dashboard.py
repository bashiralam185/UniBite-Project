import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UniBite Mallorca · Business Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
}
[data-testid="stSidebar"] * { color: #e8d5b7 !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.95rem; padding: 6px 0; }

.main { background-color: #f9f6f0; }

.hero-banner {
    background: linear-gradient(135deg, #c84b31 0%, #e8773a 40%, #f4a261 100%);
    border-radius: 18px;
    padding: 36px 40px 28px;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(200,75,49,0.25);
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: #fff;
    margin: 0;
    line-height: 1.1;
}
.hero-sub { color: rgba(255,255,255,0.85); font-size: 1.05rem; margin-top: 8px; font-weight: 300; }
.hero-tag {
    display:inline-block;
    background:rgba(255,255,255,0.2);
    border-radius:20px;
    padding:4px 14px;
    font-size:0.8rem;
    color:#fff;
    margin-top:14px;
    font-weight:500;
    letter-spacing:.5px;
}

.kpi-card {
    background: #fff;
    border-radius: 14px;
    padding: 22px 20px 18px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    border-left: 5px solid #c84b31;
    height: 100%;
}
.kpi-label { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1.2px; color: #888; font-weight: 600; margin-bottom: 6px; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: #1a1a2e; line-height: 1; }
.kpi-delta { font-size: 0.85rem; color: #2ecc71; margin-top: 6px; font-weight: 600; }

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #1a1a2e;
    margin: 32px 0 16px;
    border-bottom: 3px solid #c84b31;
    padding-bottom: 8px;
}

.insight-box {
    background: #fff;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-left: 4px solid #e8773a;
    margin-bottom: 12px;
    font-size: 0.9rem;
    line-height: 1.6;
}
.insight-box b { color: #c84b31; }

.footer { color: #aaa; font-size:0.78rem; text-align:center; margin-top:40px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SHARED DATA
# ══════════════════════════════════════════════════════════════
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

revenue_current  = [22000,21000,24000,25500,27000,29000,31000,32500,28000,25000,23000,21000]
revenue_target   = [24000,23500,26500,28000,30000,32500,35000,37000,33000,29500,27000,25000]
expenses_current = [18500,18000,19500,20000,21000,22500,24000,25000,22000,20500,19500,18500]

kpis_df = pd.DataFrame({
    "KPI": [
        "Daily Customers","Avg Ticket (€)","Retention Rate","App Adoption",
        "Cust. Acq. Cost (€)","Food Cost Ratio","Order Prep Time (min)",
        "Satisfaction Score","Loyalty Participation","Daily Revenue (€)"
    ],
    "Current": [150, 7.0, 40, 20, 5.0, 35, 10, 3.5, 10, 1050],
    "Target":  [200, 8.5, 60, 60,  3.0, 30,  6, 4.5, 50, 1700],
    "Unit":    ["pax","€","%","%","€","%","min","/ 5","%","€"],
    "L1 Impact":["Income ↑","Income ↑","Income Protection","Income ↑",
                 "Cost ↓","Cost ↓ / Margin ↑","Income ↑","Retention ↑",
                 "Income ↑","Income ↑"],
    "Frequency":["Daily","Weekly","Monthly","Monthly","Monthly","Monthly",
                 "Weekly","Monthly","Monthly","Daily"],
})

hypotheses_df = pd.DataFrame({
    "Hypothesis": [
        "H1 – Mobile App Dev","H2 – Student Campaign","H3 – Loyalty Program",
        "H4 – Menu Optimization","H5 – Supplier Negotiation","H6 – Fast Service",
        "H7 – Healthy Branding","H8 – Influencer Campaign","H9 – Bundle Offers",
        "H10 – Pre-Order System",
    ],
    "KPIs Impacted": [
        "KPI4, KPI3, KPI9","KPI1, KPI5","KPI3, KPI9","KPI6",
        "KPI6","KPI7, KPI1","KPI8, KPI1","KPI1, KPI5",
        "KPI2","KPI7, KPI1",
    ],
    "Impact Type": [
        "Positive","Positive","Positive","Positive","Positive",
        "Positive","Positive","Positive","Positive (+/-)","Positive",
    ],
    "CAPEX (€)": [15000,0,0,0,0,4000,0,0,0,0],
    "OPEX/yr (€)": [12000,3000,5000,2000,1000,0,3000,2500,1000,0],
    "L1 Impact": [
        "Income ↑","Income ↑ / Cost ↓","Income ↑","Cost ↓",
        "Cost ↓","Income ↑","Income ↑","Income ↑ / Cost ↓",
        "Income ↑","Income ↑",
    ],
    "Est. ROI": ["High","Medium","High","High","Very High","High","Medium","Medium","High","High"],
})

# Hypothesis → KPI matrix  (1=positive, -1=negative, 0=none)
# Rows = H1..H10,  Cols = KPI1..KPI10
h_kpi_matrix = np.array([
    # K1  K2  K3  K4  K5  K6  K7  K8  K9  K10
    [  0,  0,  1,  1,  0,  0,  0,  0,  1,  0 ],  # H1  Mobile App
    [  1,  0,  0,  0, -1,  0,  0,  0,  0,  1 ],  # H2  Campaign
    [  0,  0,  1,  0,  0,  0,  0,  0,  1,  0 ],  # H3  Loyalty
    [  0,  0,  0,  0,  0,  1,  0,  0,  0,  0 ],  # H4  Menu Opt
    [  0,  0,  0,  0,  0,  1,  0,  0,  0,  0 ],  # H5  Supplier
    [  1,  0,  0,  0,  0,  0,  1,  0,  0,  1 ],  # H6  Fast Svc
    [  1,  0,  0,  0,  0,  0,  0,  1,  0,  1 ],  # H7  Healthy
    [  1,  0,  0,  0, -1,  0,  0,  0,  0,  1 ],  # H8  Influencer
    [  0,  1,  0,  0,  0, -1,  0,  0,  0,  0 ],  # H9  Bundles
    [  1,  0,  0,  0,  0,  0,  1,  0,  0,  1 ],  # H10 PreOrder
])

# KPI → KPI causal influence  (1 = row-KPI improvement drives col-KPI improvement)
kpi_kpi_matrix = np.array([
    # K1  K2  K3  K4  K5  K6  K7  K8  K9  K10
    [  0,  1,  0,  0,  0,  0,  0,  0,  0,  1 ],  # K1  Customers
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  1 ],  # K2  Avg Ticket
    [  1,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],  # K3  Retention
    [  0,  0,  1,  0,  0,  0,  0,  0,  1,  0 ],  # K4  App Adoption
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],  # K5  CAC
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],  # K6  Food Cost
    [  1,  0,  0,  0,  0,  0,  0,  1,  0,  1 ],  # K7  Prep Time
    [  0,  0,  1,  0,  0,  0,  0,  0,  1,  0 ],  # K8  Satisfaction
    [  1,  0,  0,  0,  0,  0,  0,  0,  0,  1 ],  # K9  Loyalty
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],  # K10 Revenue (outcome)
])

hypothesis_details = [
    {"title":"H1 – Mobile App Development",
     "objective":"Increase retention, app usage and loyalty through digital channel",
     "actions":["Develop iOS & Android app","Student ID verification module",
                "Loyalty points engine","Push notifications for promotions","Pre-order and pickup scheduling"],
     "capex":15000,"opex":12000,
     "kpis":"KPI4 (App 20%→50%), KPI3 (Retention 40%→50%), KPI9 (Loyalty 10%→40%)",
     "l1":"Income ↑","roi":"High","duration":"6 months dev + ongoing"},
    {"title":"H2 – Student Discount Campaign",
     "objective":"Grow customer base through university partnerships",
     "actions":["Partner with UIB and CESAG","Targeted flyers on campus",
                "Instagram/TikTok paid ads","Student card verification for discount"],
     "capex":0,"opex":3000,
     "kpis":"KPI1 (Customers 150→180), KPI5 (CAC €5→€4)",
     "l1":"Income ↑ / Cost ↓","roi":"Medium","duration":"Ongoing, first push Month 1"},
    {"title":"H3 – Loyalty Program",
     "objective":"Drive repeat visits and customer frequency",
     "actions":["Points per purchase system","Free meal after 10 visits",
                "App-integrated reward tracking","Birthday offers"],
     "capex":0,"opex":5000,
     "kpis":"KPI3 (Retention 40%→60%), KPI9 (Loyalty 10%→50%)",
     "l1":"Income ↑","roi":"High","duration":"Month 2 launch"},
    {"title":"H4 – Menu Optimization",
     "objective":"Reduce food costs by streamlining the menu",
     "actions":["Sales data analysis per dish","Remove low-margin items",
                "Standardize ingredient shopping list","Seasonal menu cycles"],
     "capex":0,"opex":2000,
     "kpis":"KPI6 (Food Cost 35%→32%)",
     "l1":"Cost ↓","roi":"High","duration":"Month 1-2"},
    {"title":"H5 – Supplier Negotiation",
     "objective":"Lower ingredient costs through bulk and local sourcing",
     "actions":["Tender process with 5+ suppliers","Bulk purchase contracts",
                "Priority to local Mallorcan producers","Monthly cost review"],
     "capex":0,"opex":1000,
     "kpis":"KPI6 (Food Cost 35%→30%)",
     "l1":"Cost ↓","roi":"Very High","duration":"Month 1"},
    {"title":"H6 – Fast Service System",
     "objective":"Increase throughput and serve more customers per day",
     "actions":["Pre-prepared meal components","Kitchen workflow redesign",
                "Staff cross-training","Service time targets per station"],
     "capex":4000,"opex":0,
     "kpis":"KPI7 (Prep 10→6 min), KPI1 (Customers 150→190)",
     "l1":"Income ↑","roi":"High","duration":"Month 1-3"},
    {"title":"H7 – Healthy Menu Branding",
     "objective":"Improve perception and attract health-conscious students",
     "actions":["Introduce 5 healthy meal options","Nutritional labeling on all dishes",
                "'Eat Well, Spend Less' marketing angle","Partnership with campus sports clubs"],
     "capex":0,"opex":3000,
     "kpis":"KPI8 (Satisfaction 3.5→4.2), KPI1 (Customers ↑)",
     "l1":"Income ↑","roi":"Medium","duration":"Month 2"},
    {"title":"H8 – Influencer & Social Media",
     "objective":"Build brand awareness at low cost",
     "actions":["Identify 5-10 student micro-influencers","TikTok meal challenge campaigns",
                "Instagram story ads","Weekly 'Deal of the Day' posts"],
     "capex":0,"opex":2500,
     "kpis":"KPI1 (Customers ↑), KPI5 (CAC ↓)",
     "l1":"Income ↑ / Cost ↓","roi":"Medium","duration":"Month 1 onwards"},
    {"title":"H9 – Bundle Meal Offers",
     "objective":"Increase average spend per customer",
     "actions":["Main + drink + dessert combo at €9.50","Weekly bundle specials",
                "Upsell prompts in app","Student vs tourist bundle pricing"],
     "capex":0,"opex":1000,
     "kpis":"KPI2 (Ticket €7→€8.50) ⚠️ slight food cost increase",
     "l1":"Income ↑","roi":"High","duration":"Month 1"},
    {"title":"H10 – Online Pre-Order System",
     "objective":"Reduce wait times and increase operational efficiency",
     "actions":["In-app meal scheduling","Pickup time slots",
                "Kitchen prep alert system","Queue management display"],
     "capex":0,"opex":0,
     "kpis":"KPI7 (Prep Time ↓), KPI1 (Customers ↑)",
     "l1":"Income ↑","roi":"High","duration":"Month 6 (part of app)"},
]

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍽️ UniBite Mallorca")
    st.markdown("**Business Analytics Dashboard**")
    st.markdown("---")
    section = st.radio("Navigate to", [
        "🏠 Overview",
        "📊 Level 1 Financials",
        "🎯 KPI Tracker",
        "🚀 Hypotheses & Actions",
        "📋 Summary Table",
        "🗂️ Balanced Scorecard",
    ])
    st.markdown("---")
    st.markdown("**Year 1 Scenario**")
    st.markdown("📍 1 Location · Palma de Mallorca")
    st.markdown("🎓 Primary target: students")
    st.markdown("📅 300 operating days/year")
    st.markdown("---")
    st.caption("Business Analytics · Group 1 (Mallorca)\nCourse: 11759")

# ── Hero ───────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">UniBite Mallorca</div>
  <div class="hero-sub">Student-Focused Food Chain · Palma de Mallorca · Business Analytics Project</div>
  <span class="hero-tag">🎓 Student Cafeteria Chain</span>
  <span class="hero-tag" style="margin-left:8px">📱 App-Powered</span>
  <span class="hero-tag" style="margin-left:8px">🥗 Healthy &amp; Affordable</span>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SECTION 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
if "Overview" in section:
    st.markdown('<div class="section-title">Business at a Glance</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    for col,(label,val,delta) in zip([c1,c2,c3,c4],[
        ("Annual Revenue","€320,000","↑ Target: €410,000"),
        ("Operating Margin","€20,000","6.25% of revenue"),
        ("Daily Customers","150","↑ Target: 200 / day"),
        ("Avg Ticket","€7.00","↑ Target: €8.50"),
    ]):
        col.markdown(f"""<div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{val}</div>
          <div class="kpi-delta">{delta}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    col_l, col_r = st.columns([3,2])
    with col_l:
        st.markdown('<div class="section-title">Revenue vs Target – Monthly Projection</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=months, y=revenue_current, name="Current Revenue",
                             marker_color="#c84b31", opacity=0.85))
        fig.add_trace(go.Scatter(x=months, y=revenue_target, name="Target Revenue",
                                 line=dict(color="#1a1a2e", width=2.5, dash="dash"),
                                 mode="lines+markers", marker=dict(size=7)))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_family="DM Sans", height=320,
                          margin=dict(l=10,r=10,t=10,b=10),
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                          yaxis=dict(tickprefix="€", gridcolor="#ece9e2"),
                          xaxis=dict(gridcolor="#ece9e2"))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">Cost Structure</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Pie(
            labels=["Fixed Costs\n(Rent, Salaries, Utilities)",
                    "Variable Costs\n(Ingredients)","Marketing & Digital"],
            values=[168000,112000,20000], hole=0.55,
            marker=dict(colors=["#1a1a2e","#c84b31","#f4a261"],
                        line=dict(color="#f9f6f0",width=3)),
            textinfo="percent+label", textfont_size=11,
        ))
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300,
                           margin=dict(l=10,r=10,t=10,b=10), showlegend=False,
                           annotations=[dict(text="€300K<br>Total",x=0.5,y=0.5,
                                            font_size=14,font_family="Playfair Display",
                                            showarrow=False)])
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-title">Strategic Focus Areas</div>', unsafe_allow_html=True)
    ca,cb,cc = st.columns(3)
    ca.info("**📈 Increase Income**\nMore customers, higher ticket, better retention through loyalty & app")
    cb.warning("**💸 Reduce Expenses**\nMenu optimization, supplier negotiation, food cost ratio improvement")
    cc.success("**🛡️ Income Protection**\nStudent loyalty, satisfaction, repeat-purchase programmes")


# ══════════════════════════════════════════════════════════════
# SECTION 2 — LEVEL 1 FINANCIALS
# ══════════════════════════════════════════════════════════════
elif "Financials" in section:
    st.markdown('<div class="section-title">Level 1 – Financial Performance (Year 1)</div>', unsafe_allow_html=True)
    st.caption("Period: Year 1 · 1 location · ~150 customers/day · €7 avg ticket · 300 operating days")

    c1,c2,c3 = st.columns(3)
    for col,(label,val,delta) in zip([c1,c2,c3],[
        ("💰 Annual Revenue","€320,000","↑ +28% potential with actions"),
        ("💸 Total Expenses","€300,000","Fixed €168K + Variable €112K + Marketing €20K"),
        ("📈 Operating Margin","€20,000","6.25% — target: >12% after actions"),
    ]):
        col.markdown(f"""<div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{val}</div>
          <div class="kpi-delta">{delta}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="section-title">P&L Waterfall – Year 1</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute","relative","relative","relative","total"],
        x=["Revenue","Fixed Costs","Variable Costs","Marketing","Operating Margin"],
        y=[320000,-168000,-112000,-20000,0],
        text=["€320K","-€168K","-€112K","-€20K","€20K"],
        textposition="outside",
        connector={"line":{"color":"#ccc"}},
        increasing={"marker":{"color":"#c84b31"}},
        decreasing={"marker":{"color":"#1a1a2e"}},
        totals={"marker":{"color":"#f4a261"}},
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      height=400, font_family="DM Sans",
                      yaxis=dict(tickprefix="€", gridcolor="#ece9e2"),
                      margin=dict(l=10,r=10,t=20,b=10))
    st.plotly_chart(fig, use_container_width=True)

    col_l2,col_r2 = st.columns(2)
    with col_l2:
        st.markdown('<div class="section-title">Revenue Breakdown</div>', unsafe_allow_html=True)
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name="Student Revenue (discount price)",
                              x=["Revenue"], y=[192000], marker_color="#c84b31"))
        fig3.add_trace(go.Bar(name="Non-Student Revenue (std price)",
                              x=["Revenue"], y=[128000], marker_color="#f4a261"))
        fig3.update_layout(barmode="stack", height=300,
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_family="DM Sans",
                           yaxis=dict(tickprefix="€", gridcolor="#ece9e2"),
                           margin=dict(l=10,r=10,t=10,b=10),
                           legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig3, use_container_width=True)

    with col_r2:
        st.markdown('<div class="section-title">Assumptions</div>', unsafe_allow_html=True)
        for k,v in {
            "Customers / day":"150","Average ticket (blended)":"€7.00",
            "Operating days / year":"300","Student share":"~60%",
            "Student price":"€6.00","Non-student price":"€8.50",
            "Food cost % of revenue":"35%","Employees":"3–4 FTEs","Rent / month":"€3,000",
        }.items():
            ck,cv = st.columns([2,1]); ck.write(k); cv.markdown(f"**{v}**")


# ══════════════════════════════════════════════════════════════
# SECTION 3 — KPI TRACKER
# ══════════════════════════════════════════════════════════════
elif "KPI" in section:
    st.markdown('<div class="section-title">KPI Dashboard – 10 Second-Level Indicators</div>',
                unsafe_allow_html=True)
    st.caption("Each KPI is directly linked to a first-level indicator (Income · Expenses · Operating Margin)")

    kpis_df["Progress %"] = (kpis_df["Current"] / kpis_df["Target"] * 100).round(1)

    for i, row in kpis_df.iterrows():
        pct = min(row["Progress %"], 100)
        bar_color = "#c84b31" if pct < 60 else "#f4a261" if pct < 80 else "#2ecc71"
        with st.expander(
            f"**KPI {i+1} – {row['KPI']}**   |   "
            f"{row['Current']} → {row['Target']} {row['Unit']}   |   {row['L1 Impact']}"
        ):
            st.markdown(f"""
            <div style="background:#f0ebe3;border-radius:8px;height:14px;margin:6px 0 10px;">
              <div style="background:{bar_color};width:{pct}%;height:14px;border-radius:8px;"></div>
            </div>""", unsafe_allow_html=True)
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Current",   f"{row['Current']} {row['Unit']}")
            c2.metric("Target",    f"{row['Target']} {row['Unit']}")
            c3.metric("Progress",  f"{pct}%")
            c4.metric("Frequency", row["Frequency"])

    st.markdown('<div class="section-title">KPI Progress Overview</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=kpis_df["KPI"], y=kpis_df["Current"],
                         name="Current", marker_color="#c84b31", opacity=0.9))
    fig.add_trace(go.Bar(x=kpis_df["KPI"], y=kpis_df["Target"],
                         name="Target",  marker_color="#1a1a2e", opacity=0.3))
    fig.update_layout(barmode="overlay", height=380,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_family="DM Sans", xaxis_tickangle=-30,
                      legend=dict(orientation="h", y=1.08),
                      margin=dict(l=10,r=10,t=30,b=80),
                      yaxis=dict(gridcolor="#ece9e2"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">KPI Radar – Normalised Performance</div>',
                unsafe_allow_html=True)
    norm_current = (kpis_df["Current"] / kpis_df["Target"] * 100).tolist()
    categories   = kpis_df["KPI"].tolist()
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=norm_current+[norm_current[0]], theta=categories+[categories[0]],
        fill="toself", name="Current",
        line_color="#c84b31", fillcolor="rgba(200,75,49,0.15)"))
    fig_radar.add_trace(go.Scatterpolar(
        r=[100]*len(categories)+[100], theta=categories+[categories[0]],
        fill="toself", name="Target",
        line_color="#1a1a2e", fillcolor="rgba(26,26,46,0.05)", line_dash="dash"))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,120])),
        paper_bgcolor="rgba(0,0,0,0)", height=420, font_family="DM Sans",
        margin=dict(l=40,r=40,t=20,b=20),
        legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_radar, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# SECTION 4 — HYPOTHESES & ACTIONS
# ══════════════════════════════════════════════════════════════
elif "Hypotheses" in section:
    st.markdown('<div class="section-title">10 Strategic Hypotheses (Action Packs)</div>',
                unsafe_allow_html=True)
    st.caption("Each hypothesis = a pack of actions that impacts at least one KPI → Level 1 indicator")

    selected_h = st.selectbox("Select a hypothesis to inspect:",
                               [h["title"] for h in hypothesis_details])
    h = next(x for x in hypothesis_details if x["title"] == selected_h)

    col_l,col_r = st.columns([3,2])
    with col_l:
        st.markdown(f"#### {h['title']}")
        st.markdown(f"**Objective:** {h['objective']}")
        st.markdown("**Actions:**")
        for a in h["actions"]:
            st.markdown(f"&nbsp;&nbsp;&nbsp;• {a}")
        st.markdown(f"**KPIs Impacted:** `{h['kpis']}`")
        st.markdown(f"**Duration:** {h['duration']}")
    with col_r:
        st.markdown("**Cost Structure**")
        fig_cost = go.Figure(go.Bar(
            x=["CAPEX","OPEX/yr"], y=[h["capex"],h["opex"]],
            marker_color=["#1a1a2e","#c84b31"],
            text=[f"€{h['capex']:,}",f"€{h['opex']:,}/yr"],
            textposition="outside"))
        fig_cost.update_layout(height=220,
                                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                font_family="DM Sans",
                                yaxis=dict(tickprefix="€", gridcolor="#ece9e2"),
                                margin=dict(l=10,r=10,t=10,b=10), showlegend=False)
        st.plotly_chart(fig_cost, use_container_width=True)
        ca,cb = st.columns(2)
        ca.metric("L1 Impact", h["l1"])
        cb.metric("ROI", h["roi"])

    st.markdown("---")
    st.markdown('<div class="section-title">Total Investment Overview</div>', unsafe_allow_html=True)
    total_capex = sum(x["capex"] for x in hypothesis_details)
    total_opex  = sum(x["opex"]  for x in hypothesis_details)
    c1,c2,c3 = st.columns(3)
    c1.metric("Total CAPEX", f"€{total_capex:,}")
    c2.metric("Total OPEX / yr", f"€{total_opex:,}")
    c3.metric("Total Year-1 Investment", f"€{total_capex+total_opex:,}")

    fig_inv = go.Figure(go.Bar(
        x=[x["title"] for x in hypothesis_details],
        y=[x["capex"]+x["opex"] for x in hypothesis_details],
        marker_color="#c84b31", opacity=0.85,
        text=[f"€{x['capex']+x['opex']:,}" for x in hypothesis_details],
        textposition="outside"))
    fig_inv.update_layout(height=340,
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_family="DM Sans", xaxis_tickangle=-30,
                           yaxis=dict(tickprefix="€", gridcolor="#ece9e2"),
                           margin=dict(l=10,r=10,t=20,b=100))
    st.plotly_chart(fig_inv, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# SECTION 5 — SUMMARY TABLE  (bug-fixed + enriched)
# ══════════════════════════════════════════════════════════════
elif "Summary" in section:
    st.markdown('<div class="section-title">Summary Table – Hypotheses Impact Matrix</div>',
                unsafe_allow_html=True)
    st.caption("Each row = 1 hypothesis · Columns show KPI traceability → Cost → L1 Impact → ROI")

    # ── pandas-version-safe styling ──────────────────────────────
    def color_impact(val):
        s = str(val)
        if "+/-" in s:
            return "background-color:#fff3cd; color:#856404"
        if "↑" in s or s == "Positive":
            return "background-color:#d4edda; color:#155724"
        if "↓" in s:
            return "background-color:#cce5ff; color:#004085"
        return ""

    styled = hypotheses_df.style
    # map() is the modern API (pandas ≥ 2.1); fall back to applymap() for older versions
    try:
        styled = styled.map(color_impact, subset=["Impact Type","L1 Impact"])
    except AttributeError:
        styled = styled.applymap(color_impact, subset=["Impact Type","L1 Impact"])

    styled = (styled
              .format({"CAPEX (€)":"€{:,.0f}", "OPEX/yr (€)":"€{:,.0f}"})
              .set_properties(**{"font-size":"0.88rem"}))

    st.dataframe(styled, use_container_width=True, height=420)

    st.info("💡 **Trade-off note:** H9 (Bundle Offers) is the only hypothesis with a mixed impact "
            "— it raises Avg Ticket (positive) but slightly increases the Food Cost Ratio (negative)")

    # ══════════════════════════════════════════════════════════
    # ENRICHED ANALYSIS — 5 additional visualisations
    # ══════════════════════════════════════════════════════════

    # ── ① Hypothesis → KPI Heatmap ───────────────────────────
    st.markdown('<div class="section-title">① Hypothesis → KPI Impact Heatmap</div>',
                unsafe_allow_html=True)
    st.caption("Which hypothesis drives which KPI — green = positive effect, red = negative, white = no effect")

    h_short   = [f"H{i+1}" for i in range(10)]
    kpi_short = [f"KPI{i+1}: {kpis_df['KPI'].iloc[i][:13]}" for i in range(10)]

    cell_text = [["✔" if v==1 else ("✖" if v==-1 else "") for v in row]
                 for row in h_kpi_matrix]

    fig_heat = go.Figure(go.Heatmap(
        z=h_kpi_matrix,
        x=kpi_short, y=h_short,
        colorscale=[[0,"#e74c3c"],[0.5,"#f5f0ea"],[1,"#27ae60"]],
        zmid=0, zmin=-1, zmax=1,
        text=cell_text,
        texttemplate="%{text}",
        textfont={"size":15},
        showscale=True,
        colorbar=dict(title="Effect", tickvals=[-1,0,1],
                      ticktext=["Negative","None","Positive"]),
    ))
    fig_heat.update_layout(
        height=440, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans",
        xaxis=dict(side="top", tickfont=dict(size=10)),
        yaxis=dict(autorange="reversed", tickfont=dict(size=11)),
        margin=dict(l=20,r=20,t=70,b=20),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    ins_a, ins_b, ins_c = st.columns(3)
    ins_a.markdown("""<div class="insight-box">
        <b>Widest-reaching hypotheses</b><br>
        H1 (Mobile App) and H6 (Fast Service) each positively touch 3 KPIs —
        the broadest strategic reach in the portfolio.
    </div>""", unsafe_allow_html=True)
    ins_b.markdown("""<div class="insight-box">
        <b>Most contested KPI</b><br>
        KPI1 (Daily Customers) is targeted by 5 separate hypotheses, making it
        the most collectively invested-in metric.
    </div>""", unsafe_allow_html=True)
    ins_c.markdown("""<div class="insight-box">
        <b>Only negative effect</b><br>
        H9 (Bundle Offers) is the sole hypothesis with a deliberate negative side-effect
        on KPI6 (Food Cost Ratio) — worth monitoring monthly.
    </div>""", unsafe_allow_html=True)

    # ── ② KPI Coverage bar ───────────────────────────────────
    st.markdown('<div class="section-title">② How Many Hypotheses Target Each KPI</div>',
                unsafe_allow_html=True)
    st.caption("More bars = higher collective investment in that KPI — raises the probability of hitting its target")

    kpi_pos = (h_kpi_matrix == 1).sum(axis=0)
    kpi_neg = (h_kpi_matrix ==-1).sum(axis=0)
    kpi_full_labels = [f"KPI{i+1}: {kpis_df['KPI'].iloc[i]}" for i in range(10)]

    fig_cov = go.Figure()
    fig_cov.add_trace(go.Bar(x=kpi_full_labels, y=kpi_pos, name="Positive impacts",
                             marker_color="#27ae60", opacity=0.85,
                             text=kpi_pos, textposition="outside"))
    fig_cov.add_trace(go.Bar(x=kpi_full_labels, y=kpi_neg, name="Negative impacts",
                             marker_color="#e74c3c", opacity=0.85,
                             text=kpi_neg, textposition="outside"))
    fig_cov.update_layout(
        barmode="group", height=380,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans", xaxis_tickangle=-32,
        yaxis=dict(gridcolor="#ece9e2", title="# Hypotheses"),
        margin=dict(l=10,r=10,t=20,b=110),
        legend=dict(orientation="h", y=1.06))
    st.plotly_chart(fig_cov, use_container_width=True)

    # ── ③ KPI → KPI Causal Chain ─────────────────────────────
    st.markdown('<div class="section-title">③ KPI Causal Chain – How KPIs Cascade Into Each Other</div>',
                unsafe_allow_html=True)
    st.caption("An improvement in a row-KPI can ripple into the column-KPI — dark orange = causal link exists")

    chain_text = [["→" if v==1 else "" for v in row] for row in kpi_kpi_matrix]

    fig_chain = go.Figure(go.Heatmap(
        z=kpi_kpi_matrix,
        x=kpi_full_labels, y=kpi_full_labels,
        colorscale=[[0,"#f5f0ea"],[1,"#c84b31"]],
        zmin=0, zmax=1,
        text=chain_text,
        texttemplate="%{text}", textfont={"size":18},
        showscale=False,
    ))
    fig_chain.update_layout(
        height=440, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans",
        xaxis=dict(side="top", tickfont=dict(size=9), tickangle=-38,
                   title="… drives improvement in →"),
        yaxis=dict(autorange="reversed", tickfont=dict(size=9),
                   title="If this KPI improves …"),
        margin=dict(l=20,r=20,t=110,b=20),
    )
    st.plotly_chart(fig_chain, use_container_width=True)

    # Cascade written insights
    st.markdown('<div class="section-title">Key Cascade Insights</div>', unsafe_allow_html=True)
    ci1,ci2 = st.columns(2)
    cascades = [
        ("App Adoption (KPI4) unlocks the longest chain",
         "Improving app adoption directly drives Retention Rate (KPI3) and Loyalty Participation (KPI9). "
         "Both then flow into Daily Customers (KPI1) and Daily Revenue (KPI10). "
         "H1 (Mobile App) therefore has the deepest positive cascade in the entire portfolio."),
        ("Retention Rate (KPI3) is a multiplier KPI",
         "Higher retention simultaneously boosts Daily Customers, Loyalty Participation, and Daily Revenue. "
         "Three downstream KPIs from one improvement. Hypotheses H1 and H3 (Loyalty Program) both target it."),
        ("Order Prep Time (KPI7) has underrated reach",
         "Faster service improves Daily Customers (more throughput), Satisfaction Score, and Revenue directly. "
         "H6 (Fast Service) and H10 (Pre-Order) attack this KPI from different operational angles."),
        ("Bundle Offers (H9) creates a deliberate tension",
         "H9 raises Avg Ticket (KPI2) which feeds Daily Revenue, but also nudges Food Cost Ratio (KPI6) upward. "
         "Net effect is still positive — but this trade-off should be tracked monthly via the BI dashboard."),
    ]
    for i,(title,body) in enumerate(cascades):
        (ci1 if i%2==0 else ci2).markdown(
            f"""<div class="insight-box" style="margin-bottom:14px;">
            <b>{title}</b><br><br>{body}</div>""", unsafe_allow_html=True)

    # ── ④ Portfolio Bubble chart ──────────────────────────────
    st.markdown('<div class="section-title">④ Portfolio View – Investment vs ROI Rating</div>',
                unsafe_allow_html=True)
    st.caption("Bubble size = number of KPIs positively impacted · Top-left quadrant = best value initiatives")

    roi_map    = {"Very High":4,"High":3,"Medium":2,"Low":1}
    kpi_counts = [(h_kpi_matrix[i]==1).sum() for i in range(10)]
    h_costs    = [x["capex"]+x["opex"] for x in hypothesis_details]
    h_rois     = [roi_map[x["roi"]] for x in hypothesis_details]
    colors_p   = ["#c84b31","#e8773a","#f4a261","#2c7873","#27ae60",
                  "#1a1a2e","#3498db","#9b59b6","#e67e22","#16a085"]

    fig_port = go.Figure()
    for i in range(10):
        fig_port.add_trace(go.Scatter(
            x=[h_costs[i]], y=[h_rois[i]],
            mode="markers+text",
            marker=dict(size=max(int(kpi_counts[i])*18, 24),
                        color=colors_p[i], opacity=0.85,
                        line=dict(color="#fff",width=2)),
            text=[f"H{i+1}"], textposition="middle center",
            textfont=dict(color="#fff", size=11, family="DM Sans"),
            name=hypothesis_details[i]["title"],
            hovertemplate=(
                f"<b>{hypothesis_details[i]['title']}</b><br>"
                f"Cost: €{h_costs[i]:,}<br>"
                f"ROI: {hypothesis_details[i]['roi']}<br>"
                f"KPIs impacted: {kpi_counts[i]}<extra></extra>"),
        ))
    fig_port.update_layout(
        height=440, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans", showlegend=False,
        xaxis=dict(title="Total Investment (€)", tickprefix="€", gridcolor="#ece9e2"),
        yaxis=dict(title="ROI Rating", tickvals=[1,2,3,4],
                   ticktext=["Low","Medium","High","Very High"], gridcolor="#ece9e2"),
        margin=dict(l=20,r=20,t=20,b=30),
    )
    st.plotly_chart(fig_port, use_container_width=True)
    st.caption("💡 H5 (Supplier Negotiation) stands out: near-zero cost, Very High ROI — highest value-for-money initiative.")

    # ── ⑤ L1 First-Level Indicator Coverage ──────────────────
    st.markdown('<div class="section-title">⑤ First-Level Indicator Coverage Across Hypotheses</div>',
                unsafe_allow_html=True)
    st.caption("How the 10 hypotheses distribute across the three top-level financial objectives")

    l1_groups = {
        "Income ↑ only":          ["H1","H3","H6","H7","H9","H10"],
        "Income ↑ and Cost ↓":    ["H2","H8"],
        "Cost ↓ only":             ["H4","H5"],
    }
    l1_labels  = list(l1_groups.keys())
    l1_counts  = [len(v) for v in l1_groups.values()]
    l1_members = ["<br>".join(v) for v in l1_groups.values()]

    fig_l1 = go.Figure(go.Bar(
        x=l1_labels, y=l1_counts,
        marker_color=["#c84b31","#e8773a","#1a1a2e"],
        text=[f"{c} hypotheses" for c in l1_counts],
        textposition="outside",
        customdata=l1_members,
        hovertemplate="<b>%{x}</b><br>%{customdata}<extra></extra>",
    ))
    fig_l1.update_layout(
        height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans",
        yaxis=dict(gridcolor="#ece9e2", title="# Hypotheses"),
        margin=dict(l=10,r=10,t=20,b=40), showlegend=False,
    )
    st.plotly_chart(fig_l1, use_container_width=True)

    # ── ⑥ ROI distribution ───────────────────────────────────
    st.markdown('<div class="section-title">⑥ ROI Distribution Across the Portfolio</div>',
                unsafe_allow_html=True)
    roi_counts = hypotheses_df["Est. ROI"].value_counts().reset_index()
    roi_counts.columns = ["ROI","Count"]
    roi_order  = ["Very High","High","Medium","Low"]
    roi_counts["ROI"] = pd.Categorical(roi_counts["ROI"], categories=roi_order, ordered=True)
    roi_counts = roi_counts.sort_values("ROI")
    roi_color  = {"Very High":"#c84b31","High":"#e8773a","Medium":"#f4a261","Low":"#fcd5b4"}

    fig_roi = px.bar(roi_counts, x="ROI", y="Count", color="ROI",
                     color_discrete_map=roi_color, text="Count")
    fig_roi.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(0,0,0,0)", font_family="DM Sans",
                           showlegend=False, margin=dict(l=10,r=10,t=10,b=10),
                           yaxis=dict(gridcolor="#ece9e2"))
    st.plotly_chart(fig_roi, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# SECTION 6 — BALANCED SCORECARD
# ══════════════════════════════════════════════════════════════
elif "Scorecard" in section:
    st.markdown('<div class="section-title">Balanced Scorecard – Control Dashboard</div>',
                unsafe_allow_html=True)
    st.caption("Management monitoring view — KPIs grouped by strategic perspective")

    perspectives = {
        "💰 Financial": {"color":"#c84b31","kpis":[
            ("Annual Revenue","€320K","€410K","78%"),
            ("Operating Margin","€20K","€50K","40%"),
            ("Daily Revenue","€1,050","€1,700","62%"),
            ("Avg Ticket","€7.00","€8.50","82%"),
        ]},
        "👥 Customer": {"color":"#1a1a2e","kpis":[
            ("Daily Customers","150","200","75%"),
            ("Satisfaction Score","3.5 / 5","4.5 / 5","78%"),
            ("Retention Rate","40%","60%","67%"),
            ("Loyalty Participation","10%","50%","20%"),
        ]},
        "⚙️ Internal Process": {"color":"#e8773a","kpis":[
            ("Order Prep Time","10 min","6 min","60%"),
            ("Food Cost Ratio","35%","30%","86%"),
            ("App Adoption","20%","60%","33%"),
            ("Customer Acq. Cost","€5.00","€3.00","60%"),
        ]},
        "📱 Learning & Growth": {"color":"#2c7873","kpis":[
            ("App Users","20%","60%","33%"),
            ("Loyalty Members","10%","50%","20%"),
            ("Social Media Reach","—","10K followers","—"),
            ("Menu Healthy Options","0","5 dishes","—"),
        ]},
    }

    cols = st.columns(2)
    for i,(perspective,data) in enumerate(perspectives.items()):
        with cols[i%2]:
            st.markdown(f"""
            <div style="background:#fff;border-radius:14px;padding:20px;
                        border-top:5px solid {data['color']};
                        box-shadow:0 2px 16px rgba(0,0,0,0.07);margin-bottom:20px;">
              <div style="font-family:'Playfair Display',serif;font-size:1.1rem;
                          font-weight:700;color:{data['color']};margin-bottom:14px;">
                {perspective}
              </div>""", unsafe_allow_html=True)
            for (name,curr,tgt,pct) in data["kpis"]:
                try:
                    pct_val = float(pct.replace("%",""))
                    bar_c = "#2ecc71" if pct_val>=75 else "#f39c12" if pct_val>=50 else "#e74c3c"
                    st.markdown(f"""
                    <div style="margin:10px 0 6px;">
                      <div style="display:flex;justify-content:space-between;
                                  font-size:0.82rem;margin-bottom:3px;">
                        <span><b>{name}</b></span>
                        <span style="color:#888">{curr} → {tgt}</span>
                      </div>
                      <div style="background:#f0ebe3;border-radius:6px;height:8px;">
                        <div style="background:{bar_c};width:{pct_val}%;
                                    height:8px;border-radius:6px;"></div>
                      </div>
                      <div style="text-align:right;font-size:0.75rem;
                                  color:{bar_c};margin-top:2px;">{pct}</div>
                    </div>""", unsafe_allow_html=True)
                except Exception:
                    st.markdown(
                        f"<div style='margin:10px 0 6px;font-size:0.82rem;'>"
                        f"<b>{name}</b>: {curr} → {tgt}</div>",
                        unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">12-Month KPI Trend Simulation</div>',
                unsafe_allow_html=True)
    np.random.seed(42)
    kpi_selected = st.selectbox("Select KPI to simulate:", kpis_df["KPI"].tolist())
    row = kpis_df[kpis_df["KPI"]==kpi_selected].iloc[0]
    curr_v, tgt_v = row["Current"], row["Target"]
    trend = [
        curr_v + (tgt_v-curr_v)*(m/12)
        + np.random.uniform(-(tgt_v-curr_v)*0.05,(tgt_v-curr_v)*0.05)
        for m in range(1,13)
    ]
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=months, y=trend, mode="lines+markers", name="Projected",
        line=dict(color="#c84b31",width=2.5), marker=dict(size=8,color="#c84b31")))
    fig_trend.add_hline(y=tgt_v, line_dash="dash", line_color="#1a1a2e",
                         annotation_text=f"Target: {tgt_v} {row['Unit']}",
                         annotation_position="bottom right")
    fig_trend.add_hline(y=curr_v, line_dash="dot", line_color="#aaa",
                         annotation_text=f"Baseline: {curr_v} {row['Unit']}",
                         annotation_position="top left")
    fig_trend.update_layout(
        height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans", margin=dict(l=10,r=10,t=10,b=10),
        yaxis=dict(gridcolor="#ece9e2"),
        xaxis_title="Month", yaxis_title=f"{kpi_selected} ({row['Unit']})")
    st.plotly_chart(fig_trend, use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  UniBite Mallorca · Business Analytics Project · Course 11759 Group 1 (Mallorca)<br>
  Dashboard built with Streamlit &amp; Plotly · All figures based on Year 1 projections
</div>
""", unsafe_allow_html=True)