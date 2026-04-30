import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_access import get_channels, get_db_mtime, get_videos
from filters import render_filters
import components

st.set_page_config(
    page_title="YouTube Channel Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

channels_df = get_channels()
videos_df = get_videos()

if not channels_df.empty and not videos_df.empty:
    videos_df = videos_df.merge(
        channels_df[["id_channel", "title_channel"]],
        left_on="channel_id",
        right_on="id_channel",
        how="left",
    )

selected_ids, selected_titles, date_start, date_end, metric, top_n = render_filters(
    channels_df, videos_df
)

filtered_channels = (
    channels_df[channels_df["id_channel"].isin(selected_ids)]
    if not channels_df.empty
    else channels_df
)

if not videos_df.empty and "publish_date" in videos_df.columns:
    filtered_videos = videos_df[
        videos_df["channel_id"].isin(selected_ids)
        & (videos_df["publish_date"].dt.date >= date_start)
        & (videos_df["publish_date"].dt.date <= date_end)
    ]
else:
    filtered_videos = videos_df

st.sidebar.divider()
st.sidebar.caption(f"Data last refreshed: {get_db_mtime()}")

# ── Section 1: Header ──────────────────────────────────────────────────────────
st.title("YouTube Channel Analytics")
st.markdown("Compare performance across YouTube channels using data from the YouTube Data API v3.")
st.divider()

if channels_df.empty:
    st.info("No data yet. Run the scraper notebook to populate the database.")
    st.stop()

# ── Section 2: KPI cards ───────────────────────────────────────────────────────
components.kpi_cards(filtered_channels, filtered_videos, metric)
st.divider()

# ── Section 3: Channel comparison (2+ channels only) ──────────────────────────
if len(selected_titles) >= 2:
    components.channel_comparison(filtered_channels, filtered_videos, metric)
    st.divider()

# ── Section 4: Time series trends ─────────────────────────────────────────────
if not filtered_videos.empty:
    st.subheader("Time Series Trends")
    components.time_series(filtered_videos, metric)
st.divider()

# ── Section 5: Top videos table ────────────────────────────────────────────────
if not filtered_videos.empty:
    components.top_videos_table(filtered_videos, metric, top_n)
st.divider()

# ── Section 6: Engagement deep-dive ───────────────────────────────────────────
if not filtered_videos.empty:
    st.subheader("Engagement Deep-Dive")
    left, right = st.columns(2)
    with left:
        components.engagement_scatter(filtered_videos)
    with right:
        components.duration_scatter(filtered_videos)
st.divider()

# ── Section 7: Distribution ───────────────────────────────────────────────────
if not filtered_videos.empty:
    st.subheader("Distribution")
    components.distribution_box(filtered_videos)
