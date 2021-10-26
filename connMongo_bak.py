import json
import os
import time
from pymongo import MongoClient
from bson import json_util

class ConnMongo(object):
    def __init__(self):
        host = '81.68.113.218'
        self.client = MongoClient(host, 27017)
        db = self.client.admin
        db.authenticate("tohsaka888", "swy156132264")
        self.my_db = self.client.Music

    @staticmethod
    def Conn_Mongo_MusicByTags(self):
        col = self.my_db.MusicByTags
        dict_tags = {
            "tags": []
        }
        tags = []
        for sc_music in col.find():
            # print(sc_music)
            sc_music_str = json_util.dumps(sc_music, ensure_ascii=False)
            print(sc_music_str)
            tags.append(sc_music)
        dict_tags['tags'] = tags
        return dict_tags
        # 调用server_info查询服务器状态
        # self.db.server_info()
        # 指定数据库，表名

    @staticmethod
    def Conn_Mongo_MusicByArtists(self):
        col = self.my_db.MusicArtists
        dict_artists = {
            "ar": []
        }
        ar = []
        for sc_music in col.find():
            # print(sc_music)
            sc_music_str = json_util.dumps(sc_music, ensure_ascii=False)
            print(sc_music_str)
            ar.append(sc_music)
        dict_artists['ar'] = ar
        return dict_artists

    @staticmethod
    def save_file(filepath, Json):
        json_file_path = filepath
        json_file = open(json_file_path, mode='w', encoding='utf-8')
        #
        save_json_content = Json
        print("directory save")
        for item in save_json_content:
            line = json_util.dumps(item, ensure_ascii=False)
            json_file.write(line + '\n')

    def run(self):
        col_music_tags = self.Conn_Mongo_MusicByTags(self)
        print(os.getcwd())
        self.save_file(os.getcwd() + '/music_by_tags.txt', col_music_tags['tags'])
        col_music_artist = self.Conn_Mongo_MusicByArtists(self)
        self.save_file(os.getcwd() + '/music_by_artists.txt', col_music_tags['tags'])

if __name__ == '__main__':
    start_time = time.time()
    connMongo = ConnMongo()
    connMongo.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
