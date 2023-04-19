import os

RECURRING_N = 5

# Path
PATH_DATA = '../data/'
PATH_MODEL = '../model/'
PATH_CONFIG = '../config/'
PATH_LOG = '../log/'

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
LOG_FILENAME = 'logging.log'

# File formats
MP3 = '.mp3'
WAV = '.wav'
PKL = '.pkl'
TXT = '.txt'
LOG = '.log'

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

LOG_SETUP_MESSAGE = 'Contextual web API log file \n'

S3_TRANSCRIBE = {
    'name': 'ts-transcription',
    'link': 'https://s3.console.aws.amazon.com/s3/buckets/ts-transcription?region=us-east-1&prefix='
}
S3_CONTEXTUAL_WEB_API = {
    'name': 'ts-contextual-web-api',
    'link': 'https://s3.console.aws.amazon.com/s3/buckets/ts-contextual-web-api?region=us-east-1'
}
SETUP = {
    'directory': [
        PATH_DATA,
        PATH_MODEL,
        PATH_CONFIG,
        PATH_DATA_AUDIO,
        PATH_DATA_CATEGORY,
        PATH_DATA_STATIC_CATEGORY,
        PATH_DATA_TEXT,
        PATH_LOG 
    ],
    'download': [
        [STOP_WORDS, './'],
        [DB_CONFIG, PATH_CONFIG],
        [APPLE_CAT, PATH_DATA_STATIC_CATEGORY],
        [IAB_CAT, PATH_DATA_STATIC_CATEGORY],
        [APPLE_CAT_MAP_EN, PATH_DATA_STATIC_CATEGORY],
        [IAB_CAT_EMB, PATH_DATA_STATIC_CATEGORY],
        [RYAN_CAT, PATH_DATA_STATIC_CATEGORY],
        [MODEL, PATH_MODEL],
    ]
}

# Error Codes:
API_RUNNING = 'API is up and running. WOOHOO!!!'
API_SUCCESS = 'Podcast categorized successfully'
ERROR_PODCAST_NAME = 'Error -> Podcast name missing'
ERROR_EPISODE_NAME = 'Error -> Episode name missing'
ERROR_CLEAN_DATA = 'Error -> class: predict_apple; function: clean_data'
ERROR_PREDICT = 'Error -> class: predict_apple; function: predict'
ERROR_DOWNLOAD = 'Error -> unable to download podcast'
ERROR_TRANSCRIBE = 'Error -> class: att; function: transcribe'
ERROR_SAVE_TEXT = 'Error -> class: att; function: save_text'
ERROR_S3_SAVE = 'Error -> unable to upload transcribed test to S3 bucket'
ERROR_IAB_PREDICT = 'Error -> class: predict_iab'
ERROR_GET_APPLE_CAT = 'Error -> class: helper; function: get_apple_cat'
ERROR_GET_IAB_CAT = 'Error -> class: helper; function: get_iab_cat'
ERROR_TOPICS = 'Error -> class: helper; function: load_topics'
ERROR_DELETE_FILES = 'Error -> class: helper; function: del_files'
ERROR_DB_WRITE = 'Error -> unable to write to database'
