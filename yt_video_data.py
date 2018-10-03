from html.parser import HTMLParser
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import pprint

def get_video_data(yt_id):
    # This builds a Google API service object
    with open('resources/wav/scratchlogs.txt', 'r') as myfile:
        DEVELOPER_KEY = myfile.read().replace('\n', '')

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    def get_metadata(yt_id):
        # This builds a Google API service object
        client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

        # The search() method carries out a youtube search
        video_data = client.videos().list(
        id = yt_id,
        part="snippet,statistics").execute()

        d = {'title' : video_data['items'][0]['snippet']['title'],
             'channelId' : video_data['items'][0]['snippet']['channelId'],
             'description' : video_data['items'][0]['snippet']['description'],
             'views' : video_data['items'][0]['statistics']['viewCount'],
             'likes' : video_data['items'][0]['statistics']['likeCount'],
             'dislikes': video_data['items'][0]['statistics']['dislikeCount'],
             'n_comments' : video_data['items'][0]['statistics']['commentCount']}

        print("YouTube metadata scanned")
        return d


    def get_comments(yt_id):
        """ Download all comments on youtube video """

        client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

        video_comments = client.commentThreads().list(
        videoId = yt_id,
        part="snippet,replies").execute()

        comment_items = video_comments['items']

        class MLStripper(HTMLParser):
            def __init__(self):
                self.reset()
                self.strict = False
                self.convert_charrefs= True
                self.fed = []
            def handle_data(self, d):
                self.fed.append(d)
            def get_data(self):
                return ''.join(self.fed)

        def strip_tags(html):
            s = MLStripper()
            s.feed(html)
            return s.get_data()

        comments = []
        for sub_block in comment_items:
            comments.append(strip_tags(sub_block['snippet']['topLevelComment']['snippet']['textDisplay']))

        comments_all = ' '.join(comments)

        print("YouTube comments scanned")
        return comments_all

    metadata = get_metadata(yt_id)
    comments = get_comments(yt_id)

    metadata['comments'] = comments

    return metadata
