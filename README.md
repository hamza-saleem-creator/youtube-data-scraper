# YouTube Data Scraper

A Python-based data scraper that uses the **YouTube Data API v3** to automatically collect channel statistics, video metadata, and full video descriptions from any YouTube channel — with no manual video ID entry required.

---

## What It Does

- Fetches channel-level statistics: subscriber count, total views, video count
- Automatically retrieves all video IDs from a channel's uploads playlist using the PlaylistItems endpoint (no manual ID entry)
- Collects per-video metadata: title, publish date, duration, view count, like count, comment count
- Fetches full video descriptions via a dedicated snippet-only API call
- Exports results to CSV files for downstream analysis

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| YouTube Data API v3 | Data source |
| google-api-python-client | YouTube API wrapper |
| pandas | Data manipulation and CSV export |
| Jupyter Notebook | Interactive development environment |

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/youtube-data-scraper.git
cd youtube-data-scraper
```

### 2. Create and Activate a Virtual Environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Your API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project and enable the **YouTube Data API v3**
3. Generate an **API Key** under Credentials
4. Open `youtube scrapping.ipynb` and replace the placeholder in cell 2:

```python
api_key = 'YOUR_API_KEY_HERE'
channel_id = 'TARGET_CHANNEL_ID'
```

> **Never commit your API key.** Use a `.env` file or environment variable in production.

---

## Usage

Open the notebook and run all cells in order:

```bash
jupyter notebook "youtube scrapping.ipynb"
```

Or in VS Code, open the `.ipynb` file and click **Run All**.

The notebook will:

1. Fetch channel statistics → saved to `channel_stats.csv`
2. Automatically pull all video IDs from the uploads playlist
3. Collect video statistics in batches of 50
4. Fetch full descriptions via a separate API call
5. Save everything to `video_stats_2.csv`

### Example Output — `channel_stats.csv`

| id_channel | title_channel | subscriber_count | view_count | video_count |
|---|---|---|---|---|
| UCTedH... | Channel Name | 500000 | 12000000 | 1692 |

### Example Output — `video_stats_2.csv`

| id_video | title_video | publish_date | duration | view_count | like_count | comment_count | description_video |
|---|---|---|---|---|---|---|---|
| 2VxH6h... | Video Title | 2023-01-01 | PT10M30S | 45000 | 1200 | 340 | Full description... |

---

## Future Enhancements

- **FastAPI integration** — wrap the scraper in a REST API so channel stats and video data can be retrieved via HTTP endpoints, enabling integration with dashboards or frontend applications
- **Scheduled scraping** — automate periodic data collection using cron or a task scheduler
- **Sentiment analysis** — run NLP on video descriptions and comments
- **Data visualization** — add a dashboard layer using Plotly or Streamlit
- **Multi-channel support** — accept a list of channel IDs and aggregate results

---

## Dashboard

An interactive Streamlit dashboard for exploring and comparing channel and video data stored in `youtube.db`.

### Run the dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

The dashboard reads from the existing SQLite database. Run the scraper notebook first to populate it.

### Features

- **Sidebar filters** — channel multi-select, publish date range, primary metric (Views / Likes / Comments / Engagement rate), Top N slider
- **KPI cards** — channels selected, videos in range, total views, avg engagement rate
- **Channel comparison** — metric and subscriber bar charts (shown when 2+ channels selected)
- **Time series** — upload cadence and cumulative metric over time
- **Top videos table** — sortable, filtered by Top N
- **Engagement deep-dive** — views vs engagement rate scatter, duration vs views scatter
- **Distribution** — view count box plot by channel

### Screenshot

_Add a screenshot here after first run._

---

## Author

**Muhammad Hamza Saleem**
