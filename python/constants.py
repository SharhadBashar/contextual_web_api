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
PATH_STOP_WORDS = os.path.join(PATH_DATA, 'stop_words/')

# Files
STOP_WORDS_EN = 'stop_words_english.pkl'
STOP_WORDS_FR = 'stop_words_french.pkl'
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

LOG_SETUP_MESSAGE = {'title': 'Contextual web API log file'}
LOG_TYPE = {'i': 'info', 'e': 'error'}
LOG_FORMAT = {
    'timestamp': '',
    'status_code': '',
    'log_type': '',
    'show_id': '',
    'episode_id': '',
    'language': '',
    'message': ''
}

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
        PATH_LOG,
        PATH_STOP_WORDS
    ],
    'download': [
        [STOP_WORDS_EN, PATH_STOP_WORDS],
        # [STOP_WORDS_FR, PATH_STOP_WORDS],
        [DB_CONFIG, PATH_CONFIG],
        [APPLE_CAT, PATH_DATA_STATIC_CATEGORY],
        [IAB_CAT, PATH_DATA_STATIC_CATEGORY],
        [APPLE_CAT_MAP_EN, PATH_DATA_STATIC_CATEGORY],
        [IAB_CAT_EMB, PATH_DATA_STATIC_CATEGORY],
        [RYAN_CAT, PATH_DATA_STATIC_CATEGORY],
        [MODEL, PATH_MODEL],
    ]
}

# Error Messages:
API_RUNNING = 'API is up and running. WOOHOO!!!'
PODCAST_REQUEST = '[Podcast {}] Recieved request'
API_SUCCESS = '[Podcast {}] Categorized successfully'
ERROR_PODCAST_NAME = '[Podcast {}] Error -> Podcast name missing'
ERROR_EPISODE_NAME = '[Podcast {}] Error -> Episode name missing'
ERROR_CLEAN_DATA = '[Podcast {}] Error -> class: predict_apple; function: clean_data'
ERROR_PREDICT = '[Podcast {}] Error -> class: predict_apple; function: predict'
ERROR_DOWNLOAD = '[Podcast {}] Error -> unable to download podcast'
ERROR_TRANSCRIBE = '[Podcast {}] Error -> class: att; function: transcribe'
ERROR_SAVE_TEXT = '[Podcast {}] Error -> class: att; function: save_text'
ERROR_S3_SAVE = '[Podcast {}] Error -> unable to upload transcribed test to S3 bucket'
ERROR_IAB_PREDICT = '[Podcast {}] Error -> class: predict_iab'
ERROR_GET_APPLE_CAT = '[Podcast {}] Error -> class: helper; function: get_apple_cat'
ERROR_GET_IAB_CAT = '[Podcast {}] Error -> class: helper; function: get_iab_cat'
ERROR_TOPICS = '[Podcast {}] Error -> class: helper; function: load_topics'
ERROR_DELETE_FILES = '[Podcast {}] Error -> class: helper; function: del_files'
ERROR_DB_WRITE = '[Podcast {}] Error -> unable to write to database'
