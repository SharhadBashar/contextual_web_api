import os
import json
import pickle
import requests
from fastapi.responses import JSONResponse

from constants import *

def json_response_message(code, message):
    header = 'error' if 'Error ->' in message else 'info'
    return JSONResponse(
            status_code = code,
            content = {header: message},
        )

def download(episode_id, url):
    try:
        r = requests.get(url, allow_redirects = True)
        r = requests.get(r.url, allow_redirects = True)
        with open(PATH_DATA_AUDIO + episode_id + MP3, 'wb') as file:
            file.write(r.content)
        file.close()
        return episode_id + MP3
    except:
        return json_response_message(422, ERROR_DOWNLOAD)
    
def get_apple_cat(apple_cat):
    try:
        file = open(os.path.join(PATH_DATA_STATIC_CATEGORY, APPLE_CAT), 'rb')
        data = dict(pickle.load(file))
        return data[apple_cat]
    except:
        return json_response_message(422, ERROR_GET_APPLE_CAT)

def get_iab_cat(text_file):
    try:
        iab_cat = -1 
        highest_score = 0
        file = open(os.path.join(PATH_DATA_CATEGORY, text_file), 'rb')
        data = dict(pickle.load(file))
        for key, val in data.items():
            if (val['score'] < 0.5):
                continue
            score = val['score'] * val['count']
            if (score > highest_score):
                iab_cat = val['id']
                highest_score = score
        return iab_cat
    except:
        return json_response_message(422, ERROR_GET_IAB_CAT)

def load_topics(text_file):
    try:
        file = open(os.path.join(PATH_DATA_CATEGORY, text_file), 'rb')
        data = pickle.load(file)
        return json.dumps(list(data.keys())), json.dumps(data) 
    except:
        return json_response_message(422, ERROR_TOPICS)

def del_files(file_name, text_file):
    try:
        if os.path.isfile(os.path.join(PATH_DATA_AUDIO, file_name)):
            os.remove(os.path.join(PATH_DATA_AUDIO, file_name))
        if os.path.isfile(os.path.join(PATH_DATA_TEXT, text_file)):
            os.remove(os.path.join(PATH_DATA_TEXT, text_file))
        if os.path.isfile(os.path.join(PATH_DATA_CATEGORY, text_file)):
            os.remove(os.path.join(PATH_DATA_CATEGORY, text_file))
    except:
        return json_response_message(422, ERROR_DELETE_FILES)
