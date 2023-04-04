import os
import json
import pickle
import requests

def download(url):
    r = requests.get(url, allow_redirects=True)
    r = requests.get(r.url, allow_redirects=True)
    file_name = url.split('/')[-1].split('.mp3')[0]
    with open('../data/audio/' + file_name + '.mp3', 'wb') as file:
        file.write(r.content)
    file.close()
    return file_name
    
def get_apple_cat(apple_cat):
    file = open(os.path.join('../data/static_category/', 'apple_cat.pkl'), 'rb')
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