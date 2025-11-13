import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Netflix Revenue & Strategy Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================== CUSTOM STYLING ==================
st.markdown("""
<style>
.stApp { background-color: #141414; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
[data-testid="stSidebar"] { background-color: #181818; }
h1, h2, h3, h4, h5, h6 { color: #E50914 !important; }
div[data-testid="stMetricValue"] { color: #E50914 !important; font-weight: 600; }
.js-plotly-plot .plotly .main-svg { background-color: #141414 !important; }
.markdown-text-container { color: #E5E5E5; line-height: 1.6; }
.insight-box { background-color: #181818; padding: 20px; border-radius: 10px; border: 1px solid #E50914; color: #E5E5E5; }
</style>
""", unsafe_allow_html=True)

# ================== LOAD DATA ==================
@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_global_revenue.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ================== SIDEBAR FILTERS ==================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
st.sidebar.title("🎛️ Filters")

region = st.sidebar.multiselect("Select Region", df["region"].unique(), default=df["region"].unique())
plan = st.sidebar.multiselect("Select Plan", df["subscription_plan"].unique(), default=df["subscription_plan"].unique())
content_launch = st.sidebar.multiselect("Content Launch", df["content_launch"].unique(), default=df["content_launch"].unique())
marketing_min = int(df["marketing_spend_usd_mn"].min())
marketing_max = int(df["marketing_spend_usd_mn"].max())
marketing_range = st.sidebar.slider("Marketing Spend (USD Mn)", marketing_min, marketing_max, (marketing_min, marketing_max))

# Apply filters
df_filtered = df[
    (df["region"].isin(region)) &
    (df["subscription_plan"].isin(plan)) &
    (df["content_launch"].isin(content_launch)) &
    (df["marketing_spend_usd_mn"].between(marketing_range[0], marketing_range[1]))
]

# ================== TITLE ==================
st.title("📊 Netflix Global Revenue & Strategy Dashboard")
st.markdown("#### Monitor Revenue, Subscribers, Marketing, Adoption & Retention Trends Across Regions")

# ================== ANOMALY DETECTION ==================
def detect_anomalies(data):
    df_anom = data.copy()
    if "anomalies" not in df_anom.columns:
        model = IsolationForest(contamination=0.05, random_state=42)
        df_anom["score"] = model.fit_predict(df_anom[["revenue_usd_mn"]])
        df_anom["anomalies"] = df_anom["score"].apply(lambda x: "Anomaly" if x == -1 else "Normal")
    return df_anom

df_anomaly = detect_anomalies(df_filtered)

# ================== KPI CARDS ==================
total_revenue = df_filtered["revenue_usd_mn"].sum() / 1e3  # Bn USD
total_subscribers = df_filtered["subscribers_mn"].sum()
avg_growth = df_filtered["growth_rate"].mean()
anomaly_count = df_anomaly[df_anomaly["anomalies"]=="Anomaly"].shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("🌍 Total Revenue (Bn USD)", f"${total_revenue:.2f}B")
col2.metric("👥 Total Subscribers (Mn)", f"{total_subscribers:.2f}M")
col3.metric("📈 Avg Monthly Growth", f"{avg_growth:.2f}%")
col4.metric("⚠️ Anomalies Detected", anomaly_count)

# ================== REVENUE TREND ==================
fig_revenue = px.line(df_anomaly, x="date", y="revenue_usd_mn", color="region",
                      title="Revenue Trends with Anomalies",
                      template="plotly_dark")
fig_revenue.add_scatter(x=df_anomaly[df_anomaly["anomalies"]=="Anomaly"]["date"],
                        y=df_anomaly[df_anomaly["anomalies"]=="Anomaly"]["revenue_usd_mn"],
                        mode="markers", marker=dict(color="red", size=8, symbol="circle"),
                        name="Anomaly Points")
st.plotly_chart(fig_revenue, use_container_width=True)

# ================== SUBSCRIBERS TREND ==================
fig_subs = px.line(df_filtered, x="date", y="subscribers_mn", color="region",
                   title="Subscribers Trend",
                   template="plotly_dark")
st.plotly_chart(fig_subs, use_container_width=True)

# ================== MARKETING SPEND vs REVENUE ==================
fig_marketing = px.scatter(df_filtered, x="marketing_spend_usd_mn", y="revenue_usd_mn",
                           color="region", size="subscribers_mn",
                           hover_data=["subscription_plan", "adoption_rate", "retention_index"],
                           title="Marketing Spend vs Revenue",
                           template="plotly_dark")
st.plotly_chart(fig_marketing, use_container_width=True)

# ================== ADOPTION & RETENTION TRENDS ==================
fig_adoption = px.line(df_filtered, x="date", y=["adoption_rate", "retention_index"],
                       title="Adoption Rate & Retention Index Over Time",
                       template="plotly_dark")
st.plotly_chart(fig_adoption, use_container_width=True)

# ================== STORYTELLING & STRATEGIC INSIGHTS ==================
st.markdown("## 🧠 Storytelling & Strategic Insights")
st.markdown(f"""
<div class="insight-box">
<h4>📍 Executive Summary</h4>
<p>
Netflix’s global revenue continues its strong trajectory. APAC and North America are leading in both revenue and subscriber growth.
</p>

<h4>📊 Trend Observations</h4>
<ul>
<li><b>Revenue Growth Stability:</b> Premium plans remain stable.</li>
<li><b>Anomalies Detected:</b> Red flags appear in certain regions—could be due to local competition or marketing gaps.</li>
<li><b>Marketing Efficiency:</b> High marketing spend generally correlates with spikes in adoption and revenue.</li>
<li><b>Content Launch Impact:</b> Launches drive both revenue and adoption peaks.</li>
</ul>

<h4>💡 Strategic Recommendations</h4>
<ul>
<li>Adjust pricing or campaigns in regions with anomalies.</li>
<li>Plan content launches to optimize adoption & retention trends.</li>
<li>Focus marketing spend where ROI in revenue/subscribers is highest.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ================== FOOTER ==================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#999;'>
Built with ❤️ using Python, Streamlit & Plotly<br>
Portfolio Project: Netflix Revenue & Strategy Analytics
</div>
""", unsafe_allow_html=True)
