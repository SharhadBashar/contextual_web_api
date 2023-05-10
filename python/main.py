import os
import json
from pydantic import BaseModel
from fastapi import FastAPI, status

from s3 import S3
from constants import *
from logger import Logger
from att import Audio_To_Text_EN, Audio_To_Text_FR
from database import Database
from predict_iab import Predict_IAB
from predict_apple import Predict_Apple
from helper import download, get_apple_cat, get_iab_cat, load_topics, del_files, json_response_message

class Podcast(BaseModel):
    show_id: str
    episode_id: str
    publisher_id: int
    podcast_name: str
    episode_name: str
    apple_cat: str
    content_type: str
    description: str 
    keywords: list 
    content_url: str

s3 = S3() 
db = Database(env = 'prod')
att_en = Audio_To_Text_EN() 
att_fr = Audio_To_Text_FR()  
predict_apple = Predict_Apple()

app = FastAPI()

@app.get('/status', status_code = status.HTTP_200_OK)
async def status_check():
    return json_response_message(200, API_RUNNING)

@app.get('/welcome', status_code = status.HTTP_200_OK)
async def intro():
    return WELCOME

@app.get('/log', status_code = status.HTTP_200_OK)
async def get_log():
    json_list = []
    with open(os.path.join(PATH_LOG, LOG_FILENAME)) as file:
        for json_obj in file:
            if (json_obj is not None):
                json_list.append(json.loads(json_obj))
    return json_list

@app.post('/categorize/english', status_code = status.HTTP_201_CREATED)
async def categorize_podcast(podcast: Podcast):
    language = 'english'
    Logger(200, LOG_TYPE['i'], PODCAST_REQUEST.format(podcast.episode_id), podcast.show_id, podcast.episode_id, language)

    if (podcast.podcast_name is None or podcast.podcast_name == ''):
        return json_response_message(404, ERROR_PODCAST_NAME.format(podcast.episode_id), podcast.show_id, podcast.episode_id, language)
    if (podcast.episode_name is None or podcast.episode_name == ''):
        return json_response_message(404, ERROR_EPISODE_NAME.format(podcast.episode_id), podcast.show_id, podcast.episode_id, language)

    if (podcast.apple_cat and len(podcast.apple_cat) > 0):
        apple_cat = podcast.apple_cat
    else:                 
        podcast.description = '' if podcast.description is None else podcast.description
        podcast.keywords = [] if podcast.keywords is None else podcast.keywords
        data = podcast.podcast_name + ' ' + \
                podcast.episode_name + ' ' + \
                podcast.description + ' ' + \
                ' '.join(podcast.keywords)
        apple_cat_cleaned_data = predict_apple.clean_data(data, podcast.show_id, podcast.episode_id, language)
        apple_cat = predict_apple.predict(apple_cat_cleaned_data, podcast.show_id, podcast.episode_id, language)

    file_name = download(podcast.episode_id, podcast.content_url, podcast.show_id, language)

    text = att_en.transcribe(file_name, podcast.show_id, podcast.episode_id, language)
    text_file = att_en.save_text(text, file_name.split('.')[0] + PKL, podcast.show_id, podcast.episode_id, language)

    try:
        s3.upload_file(os.path.join(PATH_DATA_TEXT, text_file), S3_TRANSCRIBE['name'])
        Logger(201, LOG_TYPE['i'], S3_SAVE.format(podcast.episode_id, os.path.join(S3_URI + S3_TRANSCRIBE['name'], text_file)), podcast.show_id, podcast.episode_id, language)
    except Exception as error:
        return json_response_message(422, ERROR_S3_SAVE.format(podcast.episode_id, error), podcast.show_id, podcast.episode_id, language)

    try:
        Predict_IAB(text_file, podcast.episode_id, podcast.show_id, language)
    except Exception as error:
        return json_response_message(422, ERROR_IAB_PREDICT.format(podcast.episode_id, error), podcast.show_id, podcast.episode_id, language)

    db_data = {} 
    db_data['ShowId'] = podcast.show_id
    db_data['EpisodeId'] = podcast.episode_id 
    db_data['PublisherId'] = podcast.publisher_id
    db_data['AppleContentFormatId'] = get_apple_cat(apple_cat, podcast.show_id, podcast.episode_id, language)
    db_data['IabV2ContentFormatId'] = get_iab_cat(text_file, podcast.show_id, podcast.episode_id, language)
    db_data['PodcastName'] = podcast.podcast_name
    db_data['EpisodeName'] = podcast.episode_name
    db_data['Keywords'] = podcast.keywords
    db_data['ContentType'] = podcast.content_type
    db_data['ContentUrl'] = podcast.content_url
    db_data['TransLink'] = S3_TRANSCRIBE['link'] + text_file
    topics, topics_match = load_topics(text_file, podcast.show_id, podcast.episode_id, language)
    db_data['Topics'] = topics
    db_data['TopicsMatch'] = topics_match
    db_data['Description'] = podcast.description

    try:
        db.write_category(db_data)
        Logger(201, LOG_TYPE['i'], DATA_WRITE.format(podcast.episode_id), podcast.show_id, podcast.episode_id, language)
    except Exception as error:
        return json_response_message(422, ERROR_DB_WRITE.format(podcast.episode_id, error), podcast.show_id, podcast.episode_id, language)

    del_files(file_name, text_file, podcast.show_id, podcast.episode_id, language)

    return json_response_message(201, API_SUCCESS.format(podcast.episode_id), podcast.show_id, podcast.episode_id, language)

@app.post('/categorize/french', status_code = status.HTTP_201_CREATED)
async def categorize_podcast(podcast: Podcast):
    language = 'french'
    Logger(200, LOG_TYPE['i'], PODCAST_REQUEST.format(podcast.episode_id), podcast.show_id, podcast.episode_id, language)

    if (podcast.podcast_name is None or podcast.podcast_name == ''):
        return json_response_message(404, ERROR_PODCAST_NAME.format(podcast.episode_id), podcast.show_id, podcast.episode_id, language)
    if (podcast.episode_name is None or podcast.episode_name == ''):
        return json_response_message(404, ERROR_EPISODE_NAME.format(podcast.episode_id), podcast.show_id, podcast.episode_id, language)

    if (podcast.apple_cat and len(podcast.apple_cat) > 0):
        apple_cat = podcast.apple_cat
    else:                 
        podcast.description = '' if podcast.description is None else podcast.description
        podcast.keywords = [] if podcast.keywords is None else podcast.keywords
        data = podcast.podcast_name + ' ' + \
                podcast.episode_name + ' ' + \
                podcast.description + ' ' + \
                ' '.join(podcast.keywords)
        apple_cat_cleaned_data = predict_apple.clean_data(data, podcast.show_id, podcast.episode_id, language)
        apple_cat = predict_apple.predict(apple_cat_cleaned_data, podcast.show_id, podcast.episode_id, language)

    file_name = download(podcast.episode_id, podcast.content_url, podcast.show_id, language)

    text = att_fr.transcribe(file_name, podcast.show_id, podcast.episode_id, language)
    text_file = att_fr.save_text(text, file_name.split('.')[0] + PKL, podcast.show_id, podcast.episode_id, language)

    try:
        s3.upload_file(os.path.join(PATH_DATA_TEXT, text_file), S3_TRANSCRIBE['name'])
        Logger(201, LOG_TYPE['i'], S3_SAVE.format(podcast.episode_id, os.path.join(S3_URI + S3_TRANSCRIBE['name'], text_file)), podcast.show_id, podcast.episode_id, language)
    except Exception as error:
        return json_response_message(422, ERROR_S3_SAVE.format(podcast.episode_id, error), podcast.show_id, podcast.episode_id, language)

    try:
        Predict_IAB(text_file, podcast.episode_id, podcast.show_id, language)
    except Exception as error:
        return json_response_message(422, ERROR_IAB_PREDICT.format(podcast.episode_id, error), podcast.show_id, podcast.episode_id, language)

    db_data = {} 
    db_data['ShowId'] = podcast.show_id
    db_data['EpisodeId'] = podcast.episode_id 
    db_data['PublisherId'] = podcast.publisher_id
    db_data['AppleContentFormatId'] = get_apple_cat(apple_cat, podcast.show_id, podcast.episode_id, language)
    db_data['IabV2ContentFormatId'] = get_iab_cat(text_file, podcast.show_id, podcast.episode_id, language)
    db_data['PodcastName'] = podcast.podcast_name
    db_data['EpisodeName'] = podcast.episode_name
    db_data['Keywords'] = podcast.keywords
    db_data['ContentType'] = podcast.content_type
    db_data['ContentUrl'] = podcast.content_url
    db_data['TransLink'] = S3_TRANSCRIBE['link'] + text_file
    topics, topics_match = load_topics(text_file, podcast.show_id, podcast.episode_id, language)
    db_data['Topics'] = topics
    db_data['TopicsMatch'] = topics_match
    db_data['Description'] = podcast.description

    try:
        db.write_category(db_data)
    except Exception as error:
        return json_response_message(422, ERROR_DB_WRITE.format(podcast.episode_id, error), podcast.show_id, podcast.episode_id, language)

    del_files(file_name, text_file, podcast.show_id, podcast.episode_id, language)

    return json_response_message(201, API_SUCCESS.format(podcast.episode_id), podcast.show_id, podcast.episode_id, language)
