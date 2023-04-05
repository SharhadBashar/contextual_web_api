import os
import json
import pickle
import requests

def download(episode_id, url):
    r = requests.get(url, allow_redirects=True)
    r = requests.get(r.url, allow_redirects=True)
    with open('../data/audio/' + episode_id + '.mp3', 'wb') as file:
        file.write(r.content)
    file.close()
    return episode_id + '.mp3'
    
def get_apple_cat(apple_cat):
    file = open(os.path.join('../data/static_category/', 'apple_cat.pkl'), 'rb')
    data = dict(pickle.load(file))
    return data[apple_cat]

def get_iab_cat(text_file):
    iab_cat = -1 
    highest_score = 0
    file = open(os.path.join('../data/category/', text_file), 'rb')
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
    file = open(os.path.join('../data/category/', text_file), 'rb')
    data = pickle.load(file)
    return json.dumps(list(data.keys())), json.dumps(data) 