{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 68,
   "metadata": {},
   "outputs": [],
   "source": [
    "from googleapiclient.discovery import build # Used to interact with Google APIs\n",
    "from googleapiclient.errors import HttpError # For handling HTTP errors when working with Google APIs\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 69,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Sets up API key and channel ID\n",
    "api_key = 'AIzaSyAAsSPAqVzeWmJnGphYi236Oisr7OXg_Ao'\n",
    "channel_id = 'UCTedHfyVtctMgTWX2uZkEDQ'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 70,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_channel_stats(api_key,channel_id):\n",
    "    # Creates a YouTube API client\n",
    "    youtube = build('youtube','v3',developerKey=api_key)\n",
    "    \n",
    "    try:\n",
    "        # Makes an API request to get channel information\n",
    "        request = youtube.channels().list(part='snippet,contentDetails,statistics',id=channel_id)\n",
    "        response = request.execute()\n",
    "    \n",
    "        # Extracts relevant data from the API response\n",
    "        data = dict(id_channel = response['items'][0]['id'],\n",
    "                    title_channel = response['items'][0]['snippet']['title'],\n",
    "                    description_channel = response['items'][0]['snippet']['description'],\n",
    "                    publish_date = response['items'][0]['snippet']['publishedAt'],\n",
    "                    subscriber_count = response['items'][0]['statistics']['subscriberCount'],\n",
    "                    view_count = response['items'][0]['statistics']['viewCount'],\n",
    "                    video_count = response['items'][0]['statistics']['videoCount']\n",
    "                    )\n",
    "        \n",
    "    # Handle HTTP errors that may occur during the API request\n",
    "    except HttpError as e:\n",
    "        print(f'An HTTP error {e.resp.status} occurred: {e.content}')    \n",
    "    \n",
    "    # Return the extracted channel data\n",
    "    return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 71,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Gets channel statistics using the previously defined function\n",
    "channel_stats = get_channel_stats(api_key,channel_id)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 72,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Creates a single-row DataFrame from the channel statistics\n",
    "channel = pd.DataFrame(channel_stats, index=[0])\n",
    "# Saves the DataFrame to a CSV file without the index\n",
    "channel.to_csv('channel_stats.csv', index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 73,
   "metadata": {},
   "outputs": [],
   "source": [
    "video_ids = ['2VxH6h_crGk', 'waIu0n5SdGY', 'KI1YAIWW1mU', 'PnwwT5WCYD8', 'KFU9i98Ax5k', 'drwq7fO-t5Y', '2Oxd39-e8OI', 'BQm7qDIDNOw', 'SedqUIt0oiM', 'AaTPKewt7h4', '_Vu-KkAl_bQ', 'TbfR4ih0f-g', 'Ee6cPzcc8rQ', 'jsQgL1EEuYQ', 'gSgqENivJXE', 'IwxkiHlcwAk', 'uNm8G66-Vqs', 'yuG92CDa1ls', 'uaqxTKmZOog', 'Oj-UtFyeTrc', 'Nx4xXnU1D4k', 'VsjuBtUJQcw', 'yv2DKEMl-NE', 'Q0Zvh15w6O8', 'eq8SRzwHAiw', '38vtJ-Dtulo', 'Fu7a7E7T8b4', 'Bi3EYCclbGM', 'UVQvPwV9Xb8', 'ctoDRQVJjyo', 'pUKmXPhDuQs', '4nw0MEoa02k', 'C35MWffxxBU', 'gLrk9kBtm5s', 'dujHwidixxg', 'iK5FNqHdGfU', 'MR4woerlaqw', 'vs_5nLA2_Dg', 'LBvviB-Eg5Y', 'hmcNbztvTn8', 'UbBYDi4IHgw', 'k3SqDQjbnKM', 'wGe6M_zuIdk', 's1AHxrdL5O8', 'gDfZ0jNhid8', 'icEI_hccRaA', '0ewPyEDIr9o', 'iK2hAJaJeuw', 'rIxANsjdeCs', 'kohURvRdLWw', 'libkHaFbdv8', 'VDW-aWpFQ64', 'm9tmVI_ZhoE', 'x-rHg1NYBEw', 'U6V-J13M4x0', 'STr3vRHDIlE', '5ml1aAicGRU', '8cwedHvwxCY', 'OpohJ-e0eI8', '0ZawXbPm-yk', '2D1p6X-Pknw', 'hiwZXnmp53c', 'C3Mzh_hwLbE', 'detwhhs1S7c', 'FcdImRfd3jw', 'KM6xLSvx1Y8', '2JmpyzkLFJo', 'uwlHxkzbF50', '4NXmbT61eZI', 'YWNrX0qt1AQ', 'RlizU2ONMMc', '0xVKE0SxfZo', 'EUUJANPqFkU', 'VgMz5GJFQmQ', '2mVIFCSW_64', 'QZ9aexKIxrs', '0vqAxt5gjXk', 'FVamQFo1RJg', '9dPimgYVz38', 'rYBWzomkkKE', 'YhZ8nqvBHIc', 'FAbrH_3pAD4', 'P068iHLu_R4', '8YR1XZggVe0', 'nXgqCFUqzaI', 'c6ZT_9k0csc', '5UCTQ1vC6fI', '_KfRhGfAwng', 'MAAtM663dhE', 'LdN-1f-E99A']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 74,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_video_stats(api_key,video_ids):\n",
    "    all_data = []\n",
    "    # Creates YouTube API client\n",
    "    youtube = build('youtube','v3',developerKey=api_key)\n",
    "    \n",
    "    # YouTube API allows up to 50 video IDs per request\n",
    "    chunk_size = 50\n",
    "    for i in range(0, len(video_ids), chunk_size):\n",
    "        # Gets a chunk of video IDs\n",
    "        chunk = video_ids[i:i + chunk_size]\n",
    "        try:\n",
    "            # Makes API request for video details\n",
    "            request = youtube.videos().list(part='snippet,contentDetails,statistics',id=','.join(chunk)) # Joins video IDs into comma-separated string\n",
    "            response = request.execute()\n",
    "    \n",
    "            # Extracts data for each video in the response\n",
    "            for i in range(len(response['items'])):\n",
    "                data = dict(id_video = response['items'][i]['id'],\n",
    "                            title_video = response['items'][i]['snippet']['title'],\n",
    "                            description_video = response['items'][i]['snippet']['description'],\n",
    "                            publish_date = response['items'][i]['snippet']['publishedAt'],\n",
    "                            duration = response['items'][i]['contentDetails']['duration'],\n",
    "                            view_count = response['items'][i]['statistics']['viewCount'],\n",
    "                            like_count = response['items'][i]['statistics']['likeCount'],\n",
    "                            comment_count = response['items'][i]['statistics']['commentCount']\n",
    "                            )\n",
    "                all_data.append(data)\n",
    "        \n",
    "        # Handles HTTP errors\n",
    "        except HttpError as e:\n",
    "            print(f'An HTTP error {e.resp.status} occurred: {e.content}')\n",
    "    \n",
    "    # Returns list of all video data\n",
    "    return all_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 75,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Gets video statistics using the previously defined function\n",
    "video_stats = get_video_stats(api_key,video_ids)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 76,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Creates a DataFrame from the video statistics\n",
    "video = pd.DataFrame(video_stats)\n",
    "# Saves the DataFrame to a CSV file without the index\n",
    "video.to_csv('video_stats.csv', index=False)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
