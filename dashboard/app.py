# ─── RFM Analysis Dashboard ────────────────────────────────
# Interactive Streamlit dashboard for RFM customer segmentation
# Run with: streamlit run dashboard/app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="RFM Customer Segmentation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border-left: 4px solid #2ECC71;
    }
    .stMetric label { font-size: 13px !important; }
    .block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────
@st.cache_data
def load_data():
    rfm = pd.read_csv('data/processed/rfm_clustered.csv')
    df  = pd.read_csv('data/processed/clean_retail.csv',
                      parse_dates=['InvoiceDate'])
    return rfm, df

rfm, df = load_data()

# ─── Sidebar Filters ───────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/combo-chart.png", width=80)
st.sidebar.title("RFM Dashboard")
st.sidebar.markdown("---")

# Segment filter
all_segments = sorted(rfm['Segment'].unique().tolist())
selected_segments = st.sidebar.multiselect(
    "Filter by Segment",
    options=all_segments,
    default=all_segments
)

# Cluster filter
all_clusters = sorted(rfm['Cluster_Label'].unique().tolist())
selected_clusters = st.sidebar.multiselect(
    "Filter by Cluster",
    options=all_clusters,
    default=all_clusters
)

# RFM Score range
min_score = float(rfm['RFM_Score'].min())
max_score = float(rfm['RFM_Score'].max())
score_range = st.sidebar.slider(
    "RFM Score Range",
    min_value=min_score,
    max_value=max_score,
    value=(min_score, max_score),
    step=0.1
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Info**")
st.sidebar.markdown(f"Total customers: **{len(rfm):,}**")
st.sidebar.markdown(f"Total segments: **{rfm['Segment'].nunique()}**")

# ─── Apply Filters ─────────────────────────────────────────
filtered = rfm[
    (rfm['Segment'].isin(selected_segments)) &
    (rfm['Cluster_Label'].isin(selected_clusters)) &
    (rfm['RFM_Score'] >= score_range[0]) &
    (rfm['RFM_Score'] <= score_range[1])
]

# ─── Header ────────────────────────────────────────────────
st.title("📊 RFM Customer Segmentation Dashboard")
st.markdown("Advanced customer segmentation using RFM scoring and K-Means clustering")
st.markdown("---")

# ─── KPI Cards ─────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Customers", f"{len(filtered):,}",
              delta=f"{len(filtered)/len(rfm)*100:.1f}% of total")
with col2:
    st.metric("Total Revenue", f"£{filtered['Monetary'].sum():,.0f}")
with col3:
    st.metric("Avg Recency", f"{filtered['Recency'].mean():.0f} days")
with col4:
    st.metric("Avg Frequency", f"{filtered['Frequency'].mean():.1f} orders")
with col5:
    st.metric("Avg Monetary", f"£{filtered['Monetary'].mean():,.0f}")

st.markdown("---")

# ─── Row 1: Segment Distribution + Revenue ─────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Count by Segment")
    seg_count = filtered['Segment'].value_counts().reset_index()
    seg_count.columns = ['Segment', 'Count']
    fig = px.bar(seg_count, x='Count', y='Segment', 
                 orientation='h',
                 color='Count',
                 color_continuous_scale='RdYlGn',
                 text='Count')
    fig.update_traces(textposition='outside')
    fig.update_layout(height=400, showlegend=False,
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Revenue by Segment")
    seg_rev = filtered.groupby('Segment')['Monetary'].sum().reset_index()
    seg_rev.columns = ['Segment', 'Revenue']
    seg_rev = seg_rev.sort_values('Revenue', ascending=True)
    fig = px.bar(seg_rev, x='Revenue', y='Segment',
                 orientation='h',
                 color='Revenue',
                 color_continuous_scale='Blues',
                 text=seg_rev['Revenue'].apply(lambda x: f'£{x/1000:.0f}K'))
    fig.update_traces(textposition='outside')
    fig.update_layout(height=400, showlegend=False,
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ─── Row 2: RFM Distributions ──────────────────────────────
st.markdown("---")
st.subheader("RFM Score Distributions by Segment")

col1, col2, col3 = st.columns(3)

for col, metric, color in zip(
    [col1, col2, col3],
    ['Recency', 'Frequency', 'Monetary'],
    ['#E74C3C', '#3498DB', '#2ECC71']
):
    with col:
        fig = px.box(filtered, x='Segment', y=metric,
                     color='Segment',
                     title=f'{metric} by Segment')
        fig.update_layout(height=400, showlegend=False,
                          xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

# ─── Row 3: Scatter Plot ────────────────────────────────────
st.markdown("---")
st.subheader("Customer Map — Recency vs Monetary Value")

fig = px.scatter(
    filtered,
    x='Recency',
    y='Monetary',
    color='Segment',
    size='Frequency',
    hover_data=['Customer ID', 'R_Score', 'F_Score', 'M_Score', 'RFM_Score'],
    title='Customer Segments — Recency vs Monetary (bubble size = frequency)',
    height=500
)
fig.update_layout(xaxis_title='Recency (days since last purchase)',
                  yaxis_title='Monetary Value (GBP)')
st.plotly_chart(fig, use_container_width=True)

# ─── Row 4: Cluster Analysis ────────────────────────────────
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("ML Cluster Distribution")
    cluster_count = filtered['Cluster_Label'].value_counts().reset_index()
    cluster_count.columns = ['Cluster', 'Count']
    fig = px.pie(cluster_count, values='Count', names='Cluster',
                 color_discrete_sequence=px.colors.qualitative.Set2,
                 hole=0.4)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("RFM Heatmap — R vs F Score")
    pivot = filtered.pivot_table(index='R_Score', columns='F_Score',
                                  values='Monetary', aggfunc='mean')
    fig = px.imshow(pivot, 
                    color_continuous_scale='RdYlGn',
                    title='Avg Monetary Value by R and F Score',
                    text_auto='.0f')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ─── Row 5: Customer Drill-Down Table ──────────────────────
st.markdown("---")
st.subheader("Customer Level Drill-Down")

col1, col2 = st.columns([1, 3])
with col1:
    search_segment = st.selectbox("Select Segment", 
                                   ['All'] + all_segments)
    top_n = st.slider("Show top N customers", 10, 100, 25)

table_data = filtered.copy()
if search_segment != 'All':
    table_data = table_data[table_data['Segment'] == search_segment]

table_display = (table_data[['Customer ID', 'Recency', 'Frequency', 
                               'Monetary', 'R_Score', 'F_Score', 
                               'M_Score', 'RFM_Score', 'Segment', 
                               'Cluster_Label']]
                 .sort_values('Monetary', ascending=False)
                 .head(top_n)
                 .reset_index(drop=True))

st.dataframe(table_display, use_container_width=True, height=400)

# ─── Footer ────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "Built with Python · Pandas · Scikit-learn · Plotly · Streamlit | "
    "Data: UCI Online Retail II Dataset"
)