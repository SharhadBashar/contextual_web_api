import os
import json
import pickle
from fastapi import FastAPI
from pydantic import BaseModel

from s3 import S3
from database import Database
from att import Audio_To_Text
from predict_iab import Predict_IAB
from predict_apple import Predict_Apple

class Podcast(BaseModel):
    show_id: int
    episode_id: int
    publsher_id: int
    podcast_name: str
    episode_name: str
    description: str 
    keywords: list 
    s3_bucket: str
    s3_file: str


s3 = S3() 
db = Database()
att = Audio_To_Text()  
predict_apple = Predict_Apple()

app = FastAPI()

def get_apple_cat(apple_cat):
    file = open(os.path.join('../data/category/', 'apple_cat_pickle'), 'rb')
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

@app.post('/categorize/')
async def categorize_podcast(podcast: Podcast):
    s3.download_file(podcast.s3_file, podcast.s3_bucket, '../data/audio/')
    
    data = podcast.podcast_name + ' ' + \
           podcast.episode_name + ' ' + \
           podcast.description + ' ' + \
           ' '.join(podcast.keywords)
    apple_cat = predict_apple.predict(predict_apple.clean_data(data))

    text = att.transcribe(podcast.s3_file)
    text_file = att.save_text(text, podcast.s3_file.split('.')[0] + '.pkl')

    # s3.upload_file(os.path.join('../data/text/', text_file), 'ts-transcribe')

    Predict_IAB(text_file)

    db_data = {} 
    db_data['ShowId'] = podcast.show_id
    db_data['EpisodeId'] = podcast.episode_id 
    db_data['PublisherId'] = podcast.publsher_id
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
