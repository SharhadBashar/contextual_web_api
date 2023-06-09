import os
import json
import pyodbc
from datetime import datetime

from constants import *

class Database:
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
    
    def get_podcast(self, publisher_id, show_id, episode_id):
        conn = pyodbc.connect(self.conn_dmp)
        query = """SELECT COUNT(Id)
                   FROM dbo.ContextualCategories
                   WHERE PublisherId = {} AND ShowId = '{}' AND EpisodeId = '{}'
                """.format(publisher_id, show_id, episode_id)
        cursor = conn.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        cursor.close()
        return count     

    def write_category(self, data):
        data['PodcastName'] = json.dumps(data['PodcastName']).replace("'", "''").strip('\"')
        data['EpisodeName'] = json.dumps(data['EpisodeName']).replace("'", "''").strip('\"')
        data['Description'] = json.dumps(data['Description']).replace("'", "''").strip('\"')

        conn = pyodbc.connect(self.conn_dmp)
        query = """INSERT INTO 
                    dbo.ContextualCategories 
                    (ShowId, EpisodeId, PublisherId, AppleContentFormatId, IabV2ContentFormatId, 
                     Active, CreatedDate, UpdatedDate,
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
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # CreatedDate
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # UpdatedDate
                    data['PodcastName'],
                    data['EpisodeName'],
                    data['Keywords'],
                    data['ContentType'],
                    data['ContentUrl'],
                    data['TransLink'],
                    str(data['Topics']),
                    str(data['TopicsMatch']),
                    data['Description']
                )
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
