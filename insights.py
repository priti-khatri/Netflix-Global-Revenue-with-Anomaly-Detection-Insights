import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

# config page
st.set_page_config(
    page_title="Netflix Global Revenue Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# theme and style of page - ui
st.markdown("""
<style>
body {
    background-color: #f5f5f5; 
    color: #111111; 
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3, h4, h5, h6 {
    color: #E50914 !important;
}
[data-testid="stSidebar"] {
    background-color: #ffffff; 
    color: #111111;
}
div[data-testid="stMetricValue"] {
    color: #E50914 !important;
    font-weight: 600;
}
.insight-box {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #E50914;
    color: #111111;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# data load
@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_global_revenue.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# filters for sidebars
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
st.sidebar.title("🎛️ Filters")
region = st.sidebar.multiselect("Select Region", df["region"].unique(), default=df["region"].unique())
plan = st.sidebar.multiselect("Select Plan", df["subscription_plan"].unique(), default=df["subscription_plan"].unique())
df_filtered = df[(df["region"].isin(region)) & (df["subscription_plan"].isin(plan))]

# title
st.title("📈 Netflix Global Revenue Insights Dashboard")
st.markdown("#### Track Revenue, Anomalies, and Strategic Insights Across Regions")

# detect anaomaly 
def detect_anomalies(data):
    df_anom = data.copy()
    model = IsolationForest(contamination=0.05, random_state=42)
    df_anom["score"] = model.fit_predict(df_anom[["revenue_usd_mn"]])
    df_anom["anomaly"] = df_anom["score"].apply(lambda x: "Anomaly" if x == -1 else "Normal")
    return df_anom

df_anomaly = detect_anomalies(df_filtered)

# kpi factors
total_revenue = df_filtered["revenue_usd_mn"].sum() / 1e3  # in Bn USD
avg_growth = df_filtered["growth_rate"].mean()
anomaly_count = df_anomaly[df_anomaly["anomaly"]=="Anomaly"].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("🌍 Total Revenue (Bn USD)", f"${total_revenue:.2f}B")
col2.metric("📈 Avg Growth Rate (%)", f"{avg_growth:.2f}%")
col3.metric("⚠️ Anomalies Detected", anomaly_count)

# tabs
tab1, tab2 = st.tabs(["Revenue & Anomalies", "Subscribers & Marketing"])

with tab1:
    # revenue chart
    fig_rev = px.line(df_anomaly, x="date", y="revenue_usd_mn", color="region",
                      title="Revenue Trends with Anomalies", template="plotly_white")
    fig_rev.add_scatter(
        x=df_anomaly[df_anomaly["anomaly"]=="Anomaly"]["date"],
        y=df_anomaly[df_anomaly["anomaly"]=="Anomaly"]["revenue_usd_mn"],
        mode="markers", marker=dict(color="red", size=8, symbol="circle"),
        name="Anomaly Points"
    )
    st.plotly_chart(fig_rev, use_container_width=True)

    # region wise chart
    region_chart = px.bar(df_filtered.groupby("region")["revenue_usd_mn"].sum().reset_index(),
                          x="region", y="revenue_usd_mn", color="region",
                          title="Total Revenue by Region", template="plotly_white")
    st.plotly_chart(region_chart, use_container_width=True)

with tab2:
    # subscribers insights
    subs_chart = px.line(df_filtered, x="date", y="subscribers_mn", color="region",
                         title="Subscriber Trends", template="plotly_white")
    st.plotly_chart(subs_chart, use_container_width=True)

    marketing_chart = px.bar(df_filtered, x="region", y="marketing_spend_usd_mn", color="region",
                             title="Marketing Spend by Region", template="plotly_white")
    st.plotly_chart(marketing_chart, use_container_width=True)

# insights and storytelling
with st.expander("📖 Strategic Insights"):
    st.markdown("""
    <div class="insight-box">
    <h4>📍 Executive Summary</h4>
    <p>
    Netflix’s global revenue remains strong, primarily driven by <b>APAC & North America</b>. 
    Anomalies in Latin America indicate possible competition or payment disruptions.
    </p>
    <h4>📊 Observations</h4>
    <ul>
        <li><b>Revenue Growth Stability:</b> Premium plans show steady growth across APAC & Europe.</li>
        <li><b>Anomalous Spikes:</b> North America spikes correlate with flagship content releases.</li>
        <li><b>Seasonality:</b> Predictable dips during off-peak quarters globally.</li>
    </ul>
    <h4>💡 Recommendations</h4>
    <ul>
        <li>Localized pricing strategies in Latin America.</li>
        <li>Content timing optimization for low-revenue months.</li>
        <li>Retention campaigns in anomaly-heavy regions.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#555;'>
Built with ❤️ using Python, Streamlit & Plotly<br>
Inspired by Netflix's Data-Driven Strategy 
</div>
""", unsafe_allow_html=True)
