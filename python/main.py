from fastapi import FastAPI
from pydantic import BaseModel

from s3 import S3
from att import Audio_To_Text
from predict_iab import Predict_IAB
from predict_apple import Predict_Apple

class Podcast(BaseModel):
    podcast_name: str
    episode_name: str
    description: str | None = ''
    keywords: list | None = []
    s3_bucket: str
    s3_file: str

s3 = S3()   
predict_apple = Predict_Apple()
att = Audio_To_Text()

app = FastAPI()

@app.post('/categorize/')
async def categorize_podcast(podcast: Podcast):
    s3.download_file(podcast['s3_file'], podcast['s3_bucket'], '../data/audio/')
    
    data = podcast['podcast_name'] + ' ' + podcast['episode_name'] + ' ' + podcast['description'] + ' ' + ' '.join(podcast['keywords'])
    apple_cat = predict_apple.predict(predict_apple.clean_data(data))
    
    text = att.transcribe(podcast['s3_file'])
    text_file = att.save_text(text, podcast['s3_file'].split('.')[0] + '.pkl')
    Predict_IAB(text_file)
