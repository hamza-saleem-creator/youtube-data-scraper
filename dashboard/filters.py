import datetime

import pandas as pd
import streamlit as st


def render_filters(channels_df: pd.DataFrame, videos_df: pd.DataFrame):
    st.sidebar.header("Filters")

    all_titles = channels_df["title_channel"].tolist() if not channels_df.empty else []
    selected_titles = st.sidebar.multiselect("Channels", options=all_titles, default=all_titles)
    selected_ids = (
        channels_df[channels_df["title_channel"].isin(selected_titles)]["id_channel"].tolist()
        if not channels_df.empty
        else []
    )

    if not videos_df.empty and "publish_date" in videos_df.columns:
        min_date = videos_df["publish_date"].min().date()
        max_date = videos_df["publish_date"].max().date()
    else:
        min_date = max_date = datetime.date.today()

    date_range = st.sidebar.date_input(
        "Publish date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        date_start, date_end = date_range
    else:
        date_start = date_end = date_range[0] if date_range else min_date

    metric = st.sidebar.selectbox(
        "Primary metric", ["Views", "Likes", "Comments", "Engagement rate"]
    )

    top_n = st.sidebar.slider("Top N videos to show", min_value=5, max_value=50, value=10)

    return selected_ids, selected_titles, date_start, date_end, metric, top_n
