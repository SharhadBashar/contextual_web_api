import os
import json
import pickle
import requests

from constants import *

def download(episode_id, url):
    r = requests.get(url, allow_redirects = True)
    r = requests.get(r.url, allow_redirects = True)
    with open(PATH_DATA_AUDIO + episode_id + MP3, 'wb') as file:
        file.write(r.content)
    file.close()
    return episode_id + MP3
    
def get_apple_cat(apple_cat):
    file = open(os.path.join(PATH_DATA_STATIC_CATEGORY, APPLE_CAT), 'rb')
    data = dict(pickle.load(file))
    return data[apple_cat]

def get_iab_cat(text_file):
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

def load_topics(text_file):
    file = open(os.path.join(PATH_DATA_CATEGORY, text_file), 'rb')
    data = pickle.load(file)
    return json.dumps(list(data.keys())), json.dumps(data) 

def del_files(file_name, text_file):
    if os.path.isfile(os.path.join(PATH_DATA_AUDIO, file_name)):
        os.remove(os.path.join(PATH_DATA_AUDIO, file_name))
    if os.path.isfile(os.path.join(PATH_DATA_TEXT, text_file)):
        os.remove(os.path.join(PATH_DATA_TEXT, text_file))
    if os.path.isfile(os.path.join(PATH_DATA_CATEGORY, text_file)):
        os.remove(os.path.join(PATH_DATA_CATEGORY, text_file))