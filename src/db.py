from sqlalchemy import Column, MetaData, String, Table, Text, create_engine
from sqlalchemy.dialects.sqlite import insert as sqlite_insert


def get_engine(db_path: str = "youtube.db"):
    return create_engine(f"sqlite:///{db_path}")


_metadata = MetaData()

channels_table = Table(
    "channels",
    _metadata,
    Column("id_channel", String, primary_key=True),
    Column("title_channel", String),
    Column("description_channel", Text),
    Column("publish_date", String),
    Column("subscriber_count", String),
    Column("view_count", String),
    Column("video_count", String),
    Column("uploads_playlist_id", String),
)

videos_table = Table(
    "videos",
    _metadata,
    Column("id_video", String, primary_key=True),
    Column("channel_id", String),
    Column("title_video", String),
    Column("description_video", Text),
    Column("publish_date", String),
    Column("duration", String),
    Column("view_count", String),
    Column("like_count", String),
    Column("comment_count", String),
)


def _upsert(engine, table: Table, records: list[dict]) -> None:
    if not records:
        return
    pk = next(iter(table.primary_key.columns)).key
    with engine.begin() as conn:
        stmt = sqlite_insert(table).values(records)
        stmt = stmt.on_conflict_do_update(
            index_elements=[pk],
            set_={k: stmt.excluded[k] for k in records[0] if k != pk},
        )
        conn.execute(stmt)


def save_channels(engine, records: list[dict]) -> None:
    _metadata.create_all(engine)
    _upsert(engine, channels_table, records)


def save_videos(engine, records: list[dict]) -> None:
    _metadata.create_all(engine)
    _upsert(engine, videos_table, records)
