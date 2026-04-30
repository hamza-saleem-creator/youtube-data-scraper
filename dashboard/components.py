import pandas as pd
import plotly.express as px
import streamlit as st

METRIC_COL = {
    "Views": "view_count",
    "Likes": "like_count",
    "Comments": "comment_count",
    "Engagement rate": "engagement_rate",
}

METRIC_AGG = {
    "Views": "sum",
    "Likes": "sum",
    "Comments": "sum",
    "Engagement rate": "mean",
}


def kpi_cards(channels_df: pd.DataFrame, videos_df: pd.DataFrame, metric: str) -> None:
    c1, c2, c3, c4 = st.columns(4)
    n_channels = len(channels_df)
    n_videos = len(videos_df)
    total_views = int(videos_df["view_count"].sum()) if not videos_df.empty else 0
    avg_eng = videos_df["engagement_rate"].mean() if not videos_df.empty else float("nan")

    c1.metric("Channels selected", n_channels)
    c2.metric("Videos in range", f"{n_videos:,}")
    c3.metric("Total views", f"{total_views:,}")
    c4.metric("Avg engagement rate", f"{avg_eng:.2%}" if pd.notna(avg_eng) else "N/A")


def channel_comparison(channels_df: pd.DataFrame, videos_df: pd.DataFrame, metric: str) -> None:
    col = METRIC_COL[metric]
    agg = METRIC_AGG[metric]
    title_metric = "Avg engagement rate by channel" if metric == "Engagement rate" else f"Total {metric} by channel"

    st.subheader("Channel Comparison")
    left, right = st.columns(2)

    with left:
        if not videos_df.empty and "title_channel" in videos_df.columns:
            grouped = (
                videos_df.groupby("title_channel")[col]
                .agg(agg)
                .reset_index()
                .sort_values(col, ascending=True)
            )
            fig = px.bar(
                grouped, x=col, y="title_channel", orientation="h", title=title_metric
            )
            st.plotly_chart(fig, use_container_width=True)

    with right:
        if not channels_df.empty:
            sub = (
                channels_df[["title_channel", "subscriber_count"]]
                .sort_values("subscriber_count", ascending=True)
            )
            fig = px.bar(
                sub, x="subscriber_count", y="title_channel",
                orientation="h", title="Subscribers by channel",
            )
            st.plotly_chart(fig, use_container_width=True)


def time_series(videos_df: pd.DataFrame, metric: str) -> None:
    col = METRIC_COL[metric]
    label = "Avg engagement rate" if metric == "Engagement rate" else metric

    cadence = (
        videos_df.assign(month=videos_df["publish_date"].dt.to_period("M").dt.to_timestamp())
        .groupby(["month", "title_channel"])
        .size()
        .reset_index(name="uploads")
    )
    fig_a = px.line(
        cadence, x="month", y="uploads", color="title_channel",
        title="Upload cadence (videos per month)",
    )
    st.plotly_chart(fig_a, use_container_width=True)

    cumulative = (
        videos_df.sort_values("publish_date")
        .groupby(["title_channel", "publish_date"])[col]
        .sum()
        .groupby(level=0)
        .cumsum()
        .reset_index()
    )
    fig_b = px.line(
        cumulative, x="publish_date", y=col, color="title_channel",
        title=f"Cumulative {label} over time",
    )
    st.plotly_chart(fig_b, use_container_width=True)


def top_videos_table(videos_df: pd.DataFrame, metric: str, top_n: int) -> None:
    col = METRIC_COL[metric]
    st.subheader(f"Top {top_n} Videos by {metric}")

    display_cols = ["title_video", "title_channel", "publish_date",
                    "view_count", "like_count", "comment_count", "engagement_rate"]
    available = [c for c in display_cols if c in videos_df.columns]
    df = videos_df[available].sort_values(col, ascending=False).head(top_n).copy()
    df["publish_date"] = df["publish_date"].dt.date

    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "title_video": "Video",
            "title_channel": "Channel",
            "publish_date": st.column_config.DateColumn("Published"),
            "view_count": st.column_config.NumberColumn("Views", format="%d"),
            "like_count": st.column_config.NumberColumn("Likes", format="%d"),
            "comment_count": st.column_config.NumberColumn("Comments", format="%d"),
            "engagement_rate": st.column_config.NumberColumn("Engagement Rate", format=".2%"),
        },
    )


def engagement_scatter(videos_df: pd.DataFrame) -> None:
    hover = [c for c in ["title_video", "publish_date"] if c in videos_df.columns]
    fig = px.scatter(
        videos_df,
        x="view_count",
        y="engagement_rate",
        color="title_channel" if "title_channel" in videos_df.columns else None,
        hover_data=hover,
        log_x=True,
        title="Views vs engagement rate (each dot is a video)",
    )
    st.plotly_chart(fig, use_container_width=True)


def duration_scatter(videos_df: pd.DataFrame) -> None:
    hover = [c for c in ["title_video"] if c in videos_df.columns]
    fig = px.scatter(
        videos_df,
        x="duration_minutes",
        y="view_count",
        color="title_channel" if "title_channel" in videos_df.columns else None,
        hover_data=hover,
        log_y=True,
        title="Duration vs views",
    )
    st.plotly_chart(fig, use_container_width=True)


def distribution_box(videos_df: pd.DataFrame) -> None:
    fig = px.box(
        videos_df,
        x="title_channel" if "title_channel" in videos_df.columns else None,
        y="view_count",
        log_y=True,
        title="View count distribution by channel",
    )
    st.plotly_chart(fig, use_container_width=True)
