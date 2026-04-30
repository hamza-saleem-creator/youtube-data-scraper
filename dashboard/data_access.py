import datetime
import os
import re
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.db import get_engine

_engine = get_engine()


def _parse_duration_minutes(s) -> float:
    if not s:
        return 0.0
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", str(s))
    if not m:
        return 0.0
    return int(m.group(1) or 0) * 60 + int(m.group(2) or 0) + int(m.group(3) or 0) / 60


@st.cache_data(ttl=600)
def get_channels() -> pd.DataFrame:
    try:
        df = pd.read_sql("SELECT * FROM channels", _engine)
    except Exception:
        return pd.DataFrame(
            columns=[
                "id_channel", "title_channel", "description_channel",
                "publish_date", "subscriber_count", "view_count",
                "video_count", "uploads_playlist_id",
            ]
        )
    for col in ("subscriber_count", "view_count", "video_count"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


@st.cache_data(ttl=600)
def get_videos() -> pd.DataFrame:
    try:
        df = pd.read_sql("SELECT * FROM videos", _engine)
    except Exception:
        return pd.DataFrame(
            columns=[
                "id_video", "channel_id", "title_video", "description_video",
                "publish_date", "duration", "view_count", "like_count", "comment_count",
            ]
        )
    for col in ("view_count", "like_count", "comment_count"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["publish_date"] = pd.to_datetime(df["publish_date"], utc=True).dt.tz_localize(None)
    df["engagement_rate"] = (df["like_count"] + df["comment_count"]) / df["view_count"].replace(0, float("nan"))
    df["duration_minutes"] = df["duration"].apply(_parse_duration_minutes)
    return df


def get_db_mtime() -> str:
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "youtube.db")
    if os.path.exists(db_path):
        mtime = os.path.getmtime(db_path)
        return datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
    return "N/A"
