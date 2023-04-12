import os
import time
from pydantic import BaseModel
from fastapi import FastAPI, status

from s3 import S3
from constants import *
from database import Database
from att import Audio_To_Text
from predict_iab import Predict_IAB
from predict_apple import Predict_Apple
from helper import download, get_apple_cat, get_iab_cat, load_topics, del_files

class Podcast(BaseModel):
    show_id: str
    episode_id: str
    publisher_id: int
    podcast_name: str
    episode_name: str
    content_type: str
    description: str 
    keywords: list 
    content_url: str

s3 = S3() 
db = Database(env = 'prod')
att = Audio_To_Text()  
predict_apple = Predict_Apple()

app = FastAPI()

@app.get('/', status_code = status.HTTP_200_OK)
async def intro():
    return WELCOME

@app.post('/categorize/', status_code = status.HTTP_201_CREATED)
async def categorize_podcast(podcast: Podcast):
    start = time.time()
    data = podcast.podcast_name + ' ' + \
            podcast.episode_name + ' ' + \
            podcast.description + ' ' + \
            ' '.join(podcast.keywords)
    apple_cat = predict_apple.predict(predict_apple.clean_data(data))
    print('apple cat:', time.time() - start)

    temp = time.time()
    file_name = download(podcast.episode_id, podcast.content_url)
    print('download:', time.time() - temp)

    temp = time.time()
    text = att.transcribe(file_name)
    text_file = att.save_text(text, file_name.split('.')[0] + PKL)
    print('transcribe and saving:', time.time() - temp)

    s3.upload_file(os.path.join(PATH_DATA_TEXT, text_file), S3_TRANSCRIBE['name'])

    temp = time.time()
    Predict_IAB(text_file)
    print('iab cat:', time.time() - temp)

    db_data = {} 
    db_data['ShowId'] = podcast.show_id
    db_data['EpisodeId'] = podcast.episode_id 
    db_data['PublisherId'] = podcast.publisher_id
    db_data['AppleContentFormatId'] = get_apple_cat(apple_cat)
    db_data['IabV2ContentFormatId'] = get_iab_cat(text_file)
    db_data['PodcastName'] = podcast.podcast_name
    db_data['EpisodeName'] = podcast.episode_name
    db_data['Keywords'] = podcast.keywords
    db_data['ContentType'] = podcast.content_type
    db_data['ContentUrl'] = podcast.content_url
    db_data['TransLink'] = S3_TRANSCRIBE['link'] + text_file
    topics, topics_match = load_topics(text_file)
    db_data['Topics'] = topics
    db_data['TopicsMatch'] = topics_match
    db_data['Description'] = podcast.description

    db.write_category(db_data)

    del_files(file_name, text_file)

    print('total time taken:', time.time() - start)