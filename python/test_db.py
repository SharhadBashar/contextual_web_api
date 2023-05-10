import os
import json
import pyodbc
from datetime import datetime

from constants import *

class DB:
    def __init__(self, env = 'prod'):
        with open(os.path.join(PATH_CONFIG, DB_CONFIG)) as file:
            database_info = json.load(file)
        self.conn_common = self._database_conn(database_info[env], 'common')
        self.conn_dmp = self._database_conn(database_info[env], 'dmp')

    def _database_conn(self, database_info, database):
        return 'DRIVER={};\
                    SERVER={};\
                    DATABASE={};\
                    UID={};\
                    PWD={};\
                    TrustServerCertificate=yes'.format(
            database_info['driver'], database_info['server'], 
            database_info['database'][database],
            database_info['username'], database_info['password']
        )
    
    def test_conn(self):
        conn = pyodbc.connect(self.conn_dmp)
        query = """SELECT * FROM
                       dbo.ContextualCategories
                """
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor:
            print('Connection successful')
        else:
            print('Connection UNsuccessful')
        cursor.close()

    def write(self):
        conn = pyodbc.connect(self.conn_dmp)
        query = """
        INSERT INTO 
                    dbo.ContextualCategories 
                    (ShowId, EpisodeId, PublisherId, AppleContentFormatId, IabV2ContentFormatId, 
                     Active, CreatedDate, UpdatedDate,
                     PodcastName, EpisodeName, Keywords,
                     ContentType, ContentUrl, TransLink,
                     Topics, TopicsMatch, Description)
                   VALUES 
                    ('3464539', '53745822', 68, 109, 546,
                    'True', '2023-05-10 01:53:57.827971', '2023-05-10 01:53:57.827978', 
                    'Test podcast name', 'test eposide name', '[]',
                    'audio', 'https://api.spreaker.com/download/episode/53772091/20230507wkpwp_intclassic.mp3', 'https://s3.console.aws.amazon.com/s3/buckets/ts-transcription?region=us-east-1&prefix=53745822.pkl', 
                    '["wrestling", "podcast", "vip", "wwe", "week"]', '{"wrestling": {"id": 546, "data": "wrestling", "table": "Wrestling", "score": 1.0000011920928955, "count": 104}, "podcast": {"id": 371, "data": "podcast", "table": "Talk Radio", "score": 0.6291747093200684, "count": 63}, "vip": {"id": 1025, "data": "vip", "table": "Interactive", "score": 0.419993132352829, "count": 62}, "wwe": {"id": 546, "data": "wwe", "table": "Wrestling", "score": 0.8116478323936462, "count": 45}, "week": {"id": 164, "data": "week", "table": "Anniversary", "score": 0.331742525100708, "count": 43}}', 'test description')
        """
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()

    def read(self):
        conn = pyodbc.connect(self.conn_dmp)
        query = """SELECT COUNT(*) FROM
                       dbo.ContextualCategories
                   WHERE PublisherId = 68
                """
        cursor = conn.cursor()
        cursor.execute(query)
        count = cursor.fetchone()
        if (count == 0):
            print('Successful Read and Write')
        else:
            print('UNsuccessful Read and Write')
        cursor.close()

if __name__ == '__main__':
    db = DB()
    db.test_conn()
    db.write()
    db.read()
