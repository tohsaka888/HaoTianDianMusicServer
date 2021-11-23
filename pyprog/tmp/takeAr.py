import numpy as np
import time
import connMongo
from connMongo import Conn_Mongo_CollectMusic


class TakceAr(object):
    def __init__(self):
        self.connection_music_ar = connMongo.Conn_Mongo_MusicByArtists()
        self.connection_ar = connMongo.my_db.MusicArtists

    def take_frommusicAr(self):
        data_spring = self.connection_ar.find({})
        return data_spring

    def check_data(self, data_dict):
        data_ar = self.connection_music_ar.find(
            {"ar_name": data_dict['ar_name']})
        result_dict = {}
        for item in data_ar:
            result_dict = item
            print(result_dict)
            # result_dict 中是我们原有得数据
            # data_dict是新的数据，我们需要首先判断是否存在有同意名字的歌手
            # 我们将这个相同歌手的list进行一次合并
            for elem in data_dict['tracks']:
                result_dict['tracks'].append(elem)
            result_dict = self.check_list(result_dict)
            answer_dict = {
                "ar_name": result_dict['ar_name'],
                "tracks": result_dict['tracks']
            }
        self.connection_music_ar.delete_one(
            {"ar_name": ['ar_name']})
        self.connection_music_ar.insert_one(answer_dict)

    def check_list(self, result_dict):
        tmp_list = []
        check_list = result_dict['tracks']
        result_tracks_list = []

        for item in check_list:
            if item['id'] not in tmp_list:
                tmp_list.append(item['id'])
                result_tracks_list.append(item)
            else:
                pass
        result_dict['tracks'] = result_tracks_list
        return result_dict

    def run(self):
        data_spring = self.take_frommusicAr()
        for item in data_spring:
            self.check_data(item)
            # break


if __name__ == '__main__':
    start = time.time()
    TA = TakceAr()
    TA.run()
    end = time.time()
    print("执行时间:%.2f" % (end-start))
