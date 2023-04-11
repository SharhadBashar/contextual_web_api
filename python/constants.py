import os

RECURRING_N = 5

# Path
PATH_DATA = '../data/'
PATH_MODEL = '../model/'
PATH_CONFIG = '../config/'

PATH_DATA_AUDIO = os.path.join(PATH_DATA, 'audio/')
PATH_DATA_CATEGORY = os.path.join(PATH_DATA, 'category/')
PATH_DATA_STATIC_CATEGORY = os.path.join(PATH_DATA, 'static_category/')
PATH_DATA_TEXT = os.path.join(PATH_DATA, 'text/')

# Files
STOP_WORDS = 'stop_words.pkl'
APPLE_CAT = 'apple_cat.pkl'
IAB_CAT = 'iab_cat.pkl'
APPLE_CAT_MAP_EN = 'apple_cat_map_en.pkl'
IAB_CAT_EMB = 'iab_cat_embedding.t'
RYAN_CAT = 'ryan_category_id.pkl'
DB_CONFIG = 'database.json'
MODEL = 'model.pkl'

# File formats
MP3 = '.mp3'
WAV = '.wav'
PKL = '.pkl'
TXT = '.txt'

# Models
WHISPER_MODEL_TYPES = ['tiny.en', 'tiny', 'small', 'base', 'medium', 'large']
IAB_MODELS = ['all-mpnet-base-v2', 'bert-base-nli-mean-tokens', 'bert-large-uncased']
IAB_MODELS_PRAMS = {
    'all-mpnet-base-v2': 768, 
    'bert-base-nli-mean-tokens': 768,
    'bert-large-uncased': 1024
}

WELCOME = '''Welcome to Contextual web API.
             Please go to "home_url/categorize/" with the following body to get started:
             show_id: int
             episode_id: int
             publisher_id: int
                 podcast_name: str
                 episode_name: str
                 description: str or ''
                 keywords: list or ''
                 content_url: str
                 Please go to "home_url/docs/" to see all the different API calls and information
                 Please go to "home_url/status/" to see API status
              '''

S3_TRANSCRIBE = {'name': 'ts-transcription',
                 'link': 'https://s3.console.aws.amazon.com/s3/buckets/ts-transcription?region=us-east-1&prefix='}