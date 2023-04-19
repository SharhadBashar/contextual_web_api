import os
import logging

from constants import *

class Logger:
    def __init__(self, code, message):
        logging.basicConfig(filename = os.path.join(PATH_LOG, LOG_FILENAME), 
                                 format = '%(asctime)s %(message)s', 
                                 filemode = 'a',
                                 level = logging.ERROR) 
        
        logger = logging.getLogger()
        
        logger.error('[{}] : {}'.format(str(code), message))

if __name__ == '__main__':
    Logger(201, API_SUCCESS)
    Logger(200, API_RUNNING)
    Logger(422, ERROR_DB_WRITE)