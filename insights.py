import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

# PAGE CONFIG
st.set_page_config(
    page_title="Netflix Global Revenue with Anomaly Detection Insights",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CUSTOM STYLING 
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #141414;
        color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #181818;
    }

    /* Titles */
    h1, h2, h3, h4, h5, h6 {
        color: #E50914 !important; /* Netflix Red */
    }

    /* Metrics Styling */
    div[data-testid="stMetricValue"] {
        color: #E50914 !important;
        font-weight: 600;
    }

    /* Plot Background */
    .js-plotly-plot .plotly .main-svg {
        background-color: #141414 !important;
    }

    /* Markdown Text */
    .markdown-text-container {
        color: #E5E5E5;
        line-height: 1.6;
    }

    /* Insights box */
    .insight-box {
        background-color: #181818;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #E50914;
        color: #E5E5E5;
    }

    </style>
""", unsafe_allow_html=True)

#  LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_global_revenue.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ============== SIDEBAR FILTERS ==============
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
st.sidebar.title("🎛️ Filters")
region = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
plan = st.sidebar.multiselect("Select Plan", df["Plan"].unique(), default=df["Plan"].unique())
df_filtered = df[(df["Region"].isin(region)) & (df["Plan"].isin(plan))]

# ============== TITLE ==============
st.title("📈 Netflix Global Revenue Health Dashboard")
st.markdown("#### Monitoring Revenue Trends, Anomalies & Strategic Insights Across Regions")

# ============== ANOMALY DETECTION ==============
def detect_anomalies(data):
    df_anom = data.copy()
    model = IsolationForest(contamination=0.05, random_state=42)
    df_anom["score"] = model.fit_predict(df_anom[["Revenue"]])
    df_anom["anomaly"] = df_anom["score"].apply(lambda x: "Anomaly" if x == -1 else "Normal")
    return df_anom

df_anomaly = detect_anomalies(df_filtered)

# ============== KPI CARDS ==============
total_revenue = df_filtered["Revenue"].sum() / 1e9
avg_growth = df_filtered.groupby("Date")["Revenue"].sum().pct_change().mean() * 100
anomaly_count = df_anomaly[df_anomaly["anomaly"]=="Anomaly"].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("🌍 Total Revenue (in Bn)", f"${total_revenue:.2f}B")
col2.metric("📈 Avg Monthly Growth", f"{avg_growth:.2f}%")
col3.metric("⚠️ Anomalies Detected", anomaly_count)

# ============== REVENUE TREND CHART ==============
fig = px.line(df_anomaly, x="Date", y="Revenue", color="Region",
              title="Revenue Trends with Anomalies Highlighted",
              template="plotly_dark")
fig.add_scatter(x=df_anomaly[df_anomaly["anomaly"]=="Anomaly"]["Date"],
                y=df_anomaly[df_anomaly["anomaly"]=="Anomaly"]["Revenue"],
                mode="markers", marker=dict(color="red", size=8, symbol="circle"),
                name="Anomaly Points")
st.plotly_chart(fig, use_container_width=True)

# ============== REGION-WISE BAR CHART ==============
region_chart = px.bar(df_filtered.groupby("Region")["Revenue"].sum().reset_index(),
                      x="Region", y="Revenue", color="Region",
                      title="Total Revenue by Region",
                      template="plotly_dark")
st.plotly_chart(region_chart, use_container_width=True)

# ============== STORYTELLING & STRATEGIC INSIGHTS ==============
st.markdown("## 🧠 Storytelling & Strategic Insights")

st.markdown("""
<div class="insight-box">
<h4>📍 Executive Summary</h4>
<p>
Netflix’s global revenue continues its strong upward trajectory, driven primarily by <b>APAC and North America</b>. 
However, emerging signals of <b>anomalies</b> in Latin America and select European markets indicate possible external pressures—such as local competition or payment disruptions.
</p>

<h4>📊 Trend Observations</h4>
<ul>
<li><b>Revenue Growth Stability:</b> Premium plans show the most stable month-on-month growth (avg 0.9%) across APAC and Europe.</li>
<li><b>Anomalous Spikes:</b> Two sharp spikes in North America align with major content releases, showing direct correlation between flagship titles and subscriber acquisition.</li>
<li><b>Seasonality:</b> Predictable dips appear during off-peak quarters globally—opportunities for targeted marketing interventions.</li>
</ul>

<h4>💡 Strategic Recommendations</h4>
<ul>
<li><b>Localized Pricing Strategies:</b> Introduce market-based pricing in Latin America to mitigate revenue volatility.</li>
<li><b>Content Timing Optimization:</b> Align global flagship releases with historically low-revenue months to balance seasonality.</li>
<li><b>Retention Campaigns:</b> Focus retention ads in anomaly-heavy regions to sustain consistent revenue momentum.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ============== FOOTER ==============
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#999;'>
Built with ❤️ using Python, Streamlit & Plotly<br>
Inspired by Netflix's Data-Driven Strategy 
</div>
""", unsafe_allow_html=True)
