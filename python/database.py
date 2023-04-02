import json
import pickle
# import pyodbc
import pandas as pd
from tqdm import tqdm
from datetime import datetime

class Database:
    def __init__(self, env = 'staging'):
        # with open('../config/database.json') as file:
        #     database_info = json.load(file)
        # self.conn_common = self._database_conn(database_info[env], 'common')
        # self.conn_dmp = self._database_conn(database_info[env], 'dmp')
        None
        
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
        # conn = pyodbc.connect(self.conn_dmp)
        query = """INSERT INTO 
                    dbo.ContextualCategories 
                    (ShowId, EpisodeId, PublisherId, AppleContentFormatId, IabV2ContentFormatId, 
                     Active, CreatedAt, UpdatedAt,
                     PodcastName, EpisodeName, Keywords,
                     ContentType, ContentUrl, TransLink,
                     Topics, TopicsMatch, Description)
                   VALUES 
                    ({}, {}, {}, {}, {},
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
        print(query)
        # cursor = conn.cursor()
        # cursor.execute(query)
        # conn.commit()
        # cursor.close()