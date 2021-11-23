from os import PRIO_PGRP

from pymongo.common import HEARTBEAT_FREQUENCY
import tool_fileTouch as fileTouch
import random
import time
import pandas as pd
import tool_connMongo as connMongo


class DaData(object):
    def __init__(self):
        self.connection_music = connMongo.Conn_Mongo_MusicByTags()
        self.connection_artist = connMongo.Conn_Mongo_MusicByArtists()
        self.connection_playlist = connMongo.Conn_Mongo_MusicPlayList()

        self.data = fileTouch.open_file(
            "/home/aliceMargetroid/express_server/HaoTianDianMusicServer/pyprog/tmp/list.json")
        self.dict_tags = {
            "music": []
        }

    def addTracks(self, json_data):
        # 检查当前使用的playlist内容
        print(json_data['name'])
        time.sleep(3)
        for item in json_data['tracks']:
            print(item ,item['ar'])
            result = {
                "tags": json_data['tags'],
                "name": item['name'],
                "id": item['id'],
                "picUrl": item['picUrl'],
                "ar": item['ar'],
                "heat": random.randint(1000, 4000)
            }
            # 将之前存在的数据进行删除
            # 将结果写道数据库中
            self.connection_music.delete_many({"id": item['id']})
            self.connection_music.insert(result)

    def createAr(self, json_data):
        dict_ar = []
        ar_list = []
        # for curTagDict in json_data:
        #     for curPlayList in curTagDict['playListAll']:
        for curPlayList in json_data:
            print(curPlayList['name'])
            for song in curPlayList['tracks']:
                result_track_json = {
                    "name": song['name'],
                    "id": song['id'],
                    "tags": curPlayList['tags'],
                    "picUrl": song['picUrl']
                }
            # print(result_track_json)
                for i in range(len(song['ar'])):
                    if song['ar'][i]['name'] not in ar_list:
                        ar_list.append(song['ar'][i]['name'])
                        result_json = {
                            "ar_id": song['ar'][i]['id'],
                            "ar_name": song['ar'][i]['name'],
                            "tracks": [],
                            "heat": 0
                        }
                        dict_ar.append(result_json)
                    dict_ar[ar_list.index(song['ar'][i]['name'])]['tracks']\
                        .append(result_track_json)
                    heat = self.connection_music.find_one(
                        {"id": result_track_json['id']})
                    heat = heat['heat']
                    print(type(heat), heat)
                    dict_ar[ar_list.index(
                        song['ar'][i]['name'])]['heat'] += heat
        for track in dict_ar:
            print(track)
            break
            self.connection_artist.delete_many(track['ar_name'])
            self.connection_artist.insert(track)

            # print(
            #     len(pd.DataFrame(self.connection_artist.find({"name": track["ar_name"]}))))

            # if :
            #     self.connection_artist.insert(track)
            # else:

    def createAr(self, data_frame):
        dict_ar = []
        ar_list = []
        i = 0
        for song in data_frame:
            print(i)
            i += 1
            print(song)
            result_track_json = {
                "name": song['name'],
                "id": song['id'],
                "tags": song['tags'],
                "picUrl": song['picUrl']
            }
            # print(result_track_json)
            for i in range(len(song['ar'])):
                if song['ar'][i]['name'] not in ar_list:
                    ar_list.append(song['ar'][i]['name'])
                    result_json = {
                        "ar_id": song['ar'][i]['id'],
                        "ar_name": song['ar'][i]['name'],
                        "tracks": [],
                        "heat": 0
                    }
                    dict_ar.append(result_json)
                dict_ar[ar_list.index(song['ar'][i]['name'])]['tracks']\
                    .append(result_track_json)
                heat = self.connection_music.find_one(
                    {"id": result_track_json['id']})
                heat = heat['heat']
                print(type(heat), heat)
                dict_ar[ar_list.index(
                    song['ar'][i]['name'])]['heat'] += heat
        # self.connection_artist.

    def drop_item(self, data_frame):
        data_frame.drop_duplicates('id')
        result_dict_list = data_frame.to_dict('records')
        i = 0
        for item in result_dict_list:
            print(i)
            i += 1
            print(item)
            self.connection_music.delete_many({"id": item['id']})
            self.connection_music.insert_one(item)
        # return data_drame

    def run(self):
        data_spring = self.connection_playlist.find({})
        # 根据一致的list内容分割出所有的歌曲
        # data_spring = self.connection_music.find({})
        # self.createAr(data_spring)
        for item in data_spring:
            self.addTracks(item)

        # 获取所有的歌曲信息，并且将这些信息进行去重
        data_frame = pd.DataFrame(self.connection_music.find({}))
        self.drop_item(data_frame)
        # print(self.data)
        # print(data)


if __name__ == '__main__':
    start = time.time()
    prog = DaData()
    prog.run()
    end = time.time()
    print("执行时间:%.2f" % (end-start))
