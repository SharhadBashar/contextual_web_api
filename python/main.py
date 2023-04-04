import os
import json
import pickle
import requests
from pydantic import BaseModel
from fastapi import FastAPI, status, Response

from s3 import S3
from database import Database
from att import Audio_To_Text
from predict_iab import Predict_IAB
from predict_apple import Predict_Apple

class Podcast(BaseModel):
    show_id: int
    episode_id: int
    publisher_id: int
    podcast_name: str
    episode_name: str
    description: str 
    keywords: list 
    url: str


s3 = S3() 
db = Database()
att = Audio_To_Text()  
predict_apple = Predict_Apple()

app = FastAPI()

def download(url):
    r = requests.get(url, allow_redirects=True)
    r = requests.get(r.url, allow_redirects=True)
    file_name = url.split('/')[-1].split('.mp3')[0]
    with open('../data/audio/' + file_name + '.mp3', 'wb') as file:
        file.write(r.content)
    file.close()
    return file_name
    
def get_apple_cat(apple_cat):
    file = open(os.path.join('../data/', 'apple_cat.pkl'), 'rb')
    data = dict(pickle.load(file))
    return data[apple_cat]

def get_iab_cat(text_file): 
    file = open(os.path.join('../data/category/', text_file), 'rb')
    data = dict(pickle.load(file))
    return 404

def load_topics(text_file):
    file = open(os.path.join('../data/category/', text_file), 'rb')
    data = pickle.load(file)
    return json.dumps(list(data.keys())), json.dumps(data) 

@app.get('/', status_code=status.HTTP_200_OK)
async def intro():
    welcome = '''Welcome to Contextual web API.\n
                 Please go to home_url/categorize/ with the following body to get started:
                 show_id: int
                 episode_id: int
                 publisher_id: int
                 podcast_name: str
                 episode_name: str
                 description: str or ''
                 keywords: list or ''
                 url: str
                 Please go to home_url/docs/ to see all the different API calls and information
                 Please go to home_url/status/ to see API status
              '''
    return (welcome)

@app.post('/categorize/', status_code=status.HTTP_201_CREATED)
async def categorize_podcast(podcast: Podcast):
    # s3.download_file(podcast.s3_file, podcast.s3_bucket, '../data/audio/')
    file_name = download(podcast.url)
    
    data = podcast.podcast_name + ' ' + \
            podcast.episode_name + ' ' + \
            podcast.description + ' ' + \
            ' '.join(podcast.keywords)
    apple_cat = predict_apple.predict(predict_apple.clean_data(data))

    text = att.transcribe(file_name)
    text_file = att.save_text(text, file_name.split('.')[0] + '.pkl')

    # s3.upload_file(os.path.join('../data/text/', text_file), 'ts-transcribe')

    Predict_IAB(text_file)

    db_data = {} 
    db_data['ShowId'] = podcast.show_id
    db_data['EpisodeId'] = podcast.episode_id 
    db_data['PublisherId'] = podcast.publisher_id
    db_data['AppleContentFormatId'] = get_apple_cat(apple_cat)
    db_data['IabV2ContentFormatId'] = get_iab_cat(text_file)
    db_data['PodcastName'] = podcast.podcast_name
    db_data['EpisodeName'] = podcast.episode_name
    db_data['Keywords'] = podcast.keywords
    db_data['ContentType'] = 'audio'
    db_data['ContentUrl'] = 'https://s3.console.aws.amazon.com/s3/object/ts-whisper?region=us-east-1&prefix=' + podcast.s3_file
    db_data['TransLink'] = 'https://s3.console.aws.amazon.com/s3/buckets/ts-transcription?region=us-east-1&prefix=' + text_file
    topics, topics_match = load_topics(text_file)
    db_data['Topics'] = topics
    db_data['TopicsMatch'] = topics_match
    db_data['Description'] = podcast.description

    db.write_category(db_data)

# To do
# 1. function to download audio from link
# 2. get list of apple categories and their id
# 3. get list of iab categories and their id