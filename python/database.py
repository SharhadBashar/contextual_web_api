import os
import json
import pyodbc
from datetime import datetime

from constants import *

class Database:
    def __init__(self, env = 'staging'):
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
    
    def write_category(self, data):
        conn = pyodbc.connect(self.conn_dmp)
        query = """INSERT INTO 
                    dbo.ContextualCategories 
                    (ShowId, EpisodeId, PublisherId, AppleContentFormatId, IabV2ContentFormatId, 
                     Active, CreatedAt, UpdatedAt,
                     PodcastName, EpisodeName, Keywords,
                     ContentType, ContentUrl, TransLink,
                     Topics, TopicsMatch, Description)
                   VALUES 
                    ('{}', '{}', {}, {}, {},
                    'True', '{}', '{}', 
                    '{}', '{}', '{}',
                    '{}', '{}', '{}', 
                    '{}', '{}', '{}')
                """.format( 
                    data['ShowId'], 
                    data['EpisodeId'], 
                    data['PublisherId'], 
                    data['AppleContentFormatId'], 
                    data['IabV2ContentFormatId'], 
                    # data['Active'] -> Always True initially, 
                    datetime.now(), # CreatedAt
                    datetime.now(), # UpdatedAt
                    data['PodcastName'],
                    data['EpisodeName'],
                    data['Keywords'],
                    data['ContentType'],
                    data['ContentUrl'],
                    data['TransLink'],
                    data['Topics'],
                    data['TopicsMatch'],
                    data['Description']
                )
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
