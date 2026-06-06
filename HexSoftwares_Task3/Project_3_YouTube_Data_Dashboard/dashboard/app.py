import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="YouTube Analytics Dashboard - 2023",
    page_icon="📺",
    layout="wide"
)

# Dashboard Title
st.title("📺 YouTube Analytics Dashboard - 2023")
st.markdown("Analyze YouTube Channel Performance using Global YouTube Statistics Dataset")

# Load Dataset
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "Global YouTube Statistics.csv"
)

df = pd.read_csv(
    csv_path,
    encoding="latin1"
)

# Data Cleaning
df.columns = df.columns.str.strip()
df.fillna(0, inplace=True)

# Performance Score
df["Performance Score"] = (
    df["subscribers"] * 0.4 +
    df["video views"] * 0.4 +
    df["uploads"] * 0.2
)

# Sidebar Filters
st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["Country"].astype(str).unique().tolist())
)

category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df["category"].astype(str).unique().tolist())
)

# Apply Filters
filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[
        filtered_df["Country"] == country
    ]

if category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == category
    ]

# KPI Section
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Channels",
    f"{filtered_df.shape[0]:,}"
)

col2.metric(
    "Total Subscribers",
    f"{int(filtered_df['subscribers'].sum()):,}"
)

col3.metric(
    "Total Video Views",
    f"{int(filtered_df['video views'].sum()):,}"
)

col4.metric(
    "Total Uploads",
    f"{int(filtered_df['uploads'].sum()):,}"
)

# ==========================
# TOP CHANNELS
# ==========================

st.subheader("🏆 Top 10 Channels by Subscribers")

top_channels = (
    filtered_df
    .sort_values("subscribers", ascending=False)
    .head(10)
)

fig = px.bar(
    top_channels,
    x="subscribers",
    y="Youtuber",
    orientation="h",
    color="subscribers",
    title="Top 10 Most Subscribed Channels"
)

fig.update_layout(yaxis={'categoryorder':'total ascending'})

st.plotly_chart(fig, use_container_width=True)


# ==========================
# CONTENT CATEGORY ANALYSIS
# ==========================

st.subheader("🎬 Content Category Distribution")

category_chart = (
    filtered_df["category"]
    .value_counts()
    .head(10)
    .reset_index()
)

category_chart.columns = ["Category", "Count"]

fig = px.bar(
    category_chart,
    x="Category",
    y="Count",
    color="Count",
    title="Most Popular YouTube Categories"
)

st.plotly_chart(fig, use_container_width=True)


# ==========================
# CATEGORY SHARE
# ==========================

st.subheader("🥧 Category Market Share")

fig = px.pie(
    category_chart,
    names="Category",
    values="Count",
    hole=0.4,
    title="Category Share"
)

st.plotly_chart(fig, use_container_width=True)


# ==========================
# COUNTRY ANALYSIS
# ==========================

st.subheader("🌍 Top Countries by Number of Channels")

country_chart = (
    filtered_df["Country"]
    .value_counts()
    .head(10)
    .reset_index()
)

country_chart.columns = ["Country", "Channels"]

fig = px.bar(
    country_chart,
    x="Country",
    y="Channels",
    color="Channels",
    title="Countries with Most Popular YouTube Channels"
)

st.plotly_chart(fig, use_container_width=True)


# ==========================
# SUBSCRIBERS VS VIEWS
# ==========================

st.subheader("📈 Subscribers vs Video Views")

fig = px.scatter(
    filtered_df,
    x="subscribers",
    y="video views",
    size="uploads",
    color="category",
    hover_name="Youtuber",
    title="Subscribers vs Video Views vs Uploads"
)

st.plotly_chart(fig, use_container_width=True)


# ==========================
# EARNINGS ANALYSIS
# ==========================

st.subheader("💰 Top 10 Highest Earning Channels")

earnings_chart = (
    filtered_df
    .sort_values(
        "highest_yearly_earnings",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    earnings_chart,
    x="highest_yearly_earnings",
    y="Youtuber",
    orientation="h",
    color="highest_yearly_earnings",
    title="Top Earning YouTube Channels"
)

fig.update_layout(yaxis={'categoryorder':'total ascending'})

st.plotly_chart(fig, use_container_width=True)


# ==========================
# CHANNEL CREATION TREND
# ==========================

st.subheader("📅 Channel Creation Trend")

year_chart = (
    filtered_df["created_year"]
    .value_counts()
    .sort_index()
)

fig = px.line(
    x=year_chart.index,
    y=year_chart.values,
    markers=True,
    title="YouTube Channel Creation Trend"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Channels"
)

st.plotly_chart(fig, use_container_width=True)


# ==========================
# PERFORMANCE SCORE
# ==========================

st.subheader("⭐ Top Performance Channels")

top_score = (
    filtered_df
    .sort_values(
        "Performance Score",
        ascending=False
    )
    .head(10)
)

fig = px.treemap(
    top_score,
    path=["Youtuber"],
    values="Performance Score",
    title="Top Channels by Performance Score"
)

st.plotly_chart(fig, use_container_width=True)

# Download Dataset
st.subheader("📥 Download Dataset")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="youtube_filtered_data.csv",
    mime="text/csv"
)

# Key Insights
st.subheader("📌 Key Insights")

st.markdown("""
- T-Series is the most subscribed YouTube channel.
- Entertainment and Music dominate YouTube categories.
- Subscriber count strongly correlates with video views.
- United States and India have the highest number of popular channels.
- Channels with higher subscribers generally generate higher yearly earnings.
""")

# Dataset Preview
st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df.head(20))