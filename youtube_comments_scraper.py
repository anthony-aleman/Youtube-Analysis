# Importing libraries 
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from pytube import extract, YouTube
load_dotenv()
api_key = os.getenv('API_KEY')

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

from dotenv import load_dotenv
load_dotenv()


class YoutubeVideo:
    def __init__(self, link="https://www.youtube.com/watch?v=qT7S0BrFnRc&t=214s"):
        #initialize class object

        self.link = link
        self.link_id = extract.video_id(link)
    
    def get_link_id(self) -> str:
        #return the link id of the youtube video
        return self.link_id

    def download(self):
        youtube = YouTube(self.link)   
        youtube = youtube.streams.get_highest_resolution()
        try:
            youtube.download()
        except:
            print("An error has occurred")
        print("Download is completed successfully")

video=YoutubeVideo()




DEVELOPER_KEY = os.getenv('API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_video_comments(service, **kwargs):
    comments, dates, likes = [], [], []
    results = service.commentThreads().list(**kwargs).execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            date = item['snippet']['topLevelComment']['snippet']['publishedAt']
            like = item['snippet']['topLevelComment']['snippet']['likeCount']

            comments.append(comment)
            dates.append(date)
            likes.append(like)

        # check if there are more comments
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break

    return pd.DataFrame({'Comments': comments, 'Date': dates, 'Likes': likes})


comments_df = None

def main():
    global comments_df
    
    # Build the service
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    yt_vid = YoutubeVideo()

    # Get the comments
    video_id = yt_vid.get_link_id() 
    comments_df = get_video_comments(youtube, part='snippet', videoId=video_id, textFormat='plainText')

if __name__ == '__main__':
    main()


