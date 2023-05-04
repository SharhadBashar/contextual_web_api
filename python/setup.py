import os
import json
from tqdm import tqdm

from s3 import S3
from constants import *

# print('Creating directories...')
# for directory in tqdm(SETUP['directory']):
#     try:
#         os.mkdir(directory)
#     except:
#         None
# print('Directories created')

f = open(os.path.join(PATH_LOG, LOG_FILENAME), 'w')
f.write(json.dumps(LOG_SETUP_MESSAGE))
f.write('\n')
f.close()

# print('Downloading required files...')
# s3 = S3()
# for file, download_path in tqdm(SETUP['download']):
#     s3.download_file(file, S3_CONTEXTUAL_WEB_API['name'], download_path)
# print('Files downloaded')

# print('SETUP COMLPETE')
