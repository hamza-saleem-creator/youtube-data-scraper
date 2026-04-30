import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()


def _build_youtube():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY is not set — add it to your .env file")
    return build("youtube", "v3", developerKey=api_key)


def get_channel_stats(channel_id: str) -> dict:
    youtube = _build_youtube()
    try:
        response = (
            youtube.channels()
            .list(part="snippet,contentDetails,statistics", id=channel_id)
            .execute()
        )
        item = response["items"][0]
        return {
            "id_channel": item["id"],
            "title_channel": item["snippet"]["title"],
            "description_channel": item["snippet"]["description"],
            "publish_date": item["snippet"]["publishedAt"],
            "subscriber_count": item["statistics"]["subscriberCount"],
            "view_count": item["statistics"]["viewCount"],
            "video_count": item["statistics"]["videoCount"],
            "uploads_playlist_id": item["contentDetails"]["relatedPlaylists"]["uploads"],
        }
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        raise


def get_video_ids(channel_id: str) -> list[str]:
    playlist_id = get_channel_stats(channel_id)["uploads_playlist_id"]
    youtube = _build_youtube()
    video_ids = []
    next_page_token = None

    while True:
        try:
            response = (
                youtube.playlistItems()
                .list(
                    part="contentDetails",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token,
                )
                .execute()
            )
            for item in response["items"]:
                video_ids.append(item["contentDetails"]["videoId"])

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            break

    return video_ids


def get_video_details(video_ids: list[str]) -> list[dict]:
    youtube = _build_youtube()
    all_data = []

    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i : i + 50]
        try:
            response = (
                youtube.videos()
                .list(part="snippet,contentDetails,statistics", id=",".join(chunk))
                .execute()
            )
            for item in response["items"]:
                stats = item["statistics"]
                all_data.append(
                    {
                        "id_video": item["id"],
                        "title_video": item["snippet"]["title"],
                        "description_video": item["snippet"]["description"],
                        "publish_date": item["snippet"]["publishedAt"],
                        "duration": item["contentDetails"]["duration"],
                        "view_count": stats.get("viewCount"),
                        "like_count": stats.get("likeCount"),
                        "comment_count": stats.get("commentCount"),
                    }
                )
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")

    return all_data
