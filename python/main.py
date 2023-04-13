import os
from pydantic import BaseModel
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from s3 import S3
from constants import *
from database import Database
from att import Audio_To_Text
from predict_iab import Predict_IAB
from predict_apple import Predict_Apple
from helper import download, get_apple_cat, get_iab_cat, load_topics, del_files, json_response_message

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

@app.get('/status', status_code = status.HTTP_200_OK)
async def status_check():
    return json_response_message(200, API_RUNNING)

@app.get('/welcome/', status_code = status.HTTP_200_OK)
async def intro():
    return WELCOME

@app.post('/categorize/', status_code = status.HTTP_201_CREATED)
async def categorize_podcast(podcast: Podcast):
    print('Recieved request for podcast:', podcast.show_id)

    if (podcast.podcast_name is None or podcast.podcast_name == ''):
        return json_response_message(404, ERROR_PODCAST_NAME)

    if (podcast.episode_name is None or podcast.episode_name == ''):
        return json_response_message(404, ERROR_EPISODE_NAME)
                              
    podcast.description = '' if podcast.description is None else podcast.description
    podcast.keywords = [] if podcast.keywords is None else podcast.keywords

    data = podcast.podcast_name + ' ' + \
            podcast.episode_name + ' ' + \
            podcast.description + ' ' + \
            ' '.join(podcast.keywords)
    
    apple_cat_cleaned_data = predict_apple.clean_data(data)
    if (apple_cat_cleaned_data == ERROR_CLEAN_DATA):
        return json_response_message(422, ERROR_CLEAN_DATA)

    apple_cat = predict_apple.predict(apple_cat_cleaned_data)
    if (apple_cat == ERROR_PREDICT):
        return json_response_message(422, ERROR_PREDICT)


    file_name = download(podcast.episode_id, podcast.content_url)
    if (file_name == ERROR_DOWNLOAD):
        return json_response_message(422, ERROR_DOWNLOAD)


    text = att.transcribe(file_name)
    if (text == ERROR_TRANSCRIBE):
        return json_response_message(422, ERROR_DOWNLOAD)
    
    text_file = att.save_text(text, file_name.split('.')[0] + PKL)
    if (text_file == ERROR_SAVE_TEXT):
        return json_response_message(422, ERROR_SAVE_TEXT)

    try:
        s3.upload_file(os.path.join(PATH_DATA_TEXT, text_file), S3_TRANSCRIBE['name'])
    except:
        return json_response_message(422, ERROR_S3_SAVE)

    try:
        Predict_IAB(text_file)
    except:
        return json_response_message(422, ERROR_IAB_PREDICT)

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

    try:
        db.write_category(db_data)
    except:
        return json_response_message(422, ERROR_DB_WRITE)

    del_files(file_name, text_file)

    return json_response_message(201, API_SUCCESS)
