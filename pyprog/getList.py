import json
import time
import random
from numpy import int64, result_type, string_

import tool_connMongo as connMongo
import pandas as pd
import pymongo
import requests

from ua_info import ua_list


class GL(object):
    def __init__(self):
        self.connection_playlist = connMongo.Conn_Mongo_MusicPlayList()
        self.url = 'http://cloud-music.pl-fe.cn/playlist/detail?id={}'
        self.urlM = 'http://cloud-music.pl-fe.cn/song/detail?ids={}'

    def get_play_list_id(self):
        data_frame = pd.DataFrame(
            self.connection_playlist.find({}, {'id': 1, "_id": 0}))
        return data_frame

    def get_one_list(self, data_frame, sym):
        play_list_id = data_frame['id'].values[sym]
        return play_list_id
    # 爬虫的模板

    def get_json(self, url):
        req = requests.post(
            url, headers={'User-Agent': random.choice(ua_list)})
        Json = req.json()
        return Json

    def get_track(self, item):
        result_dict = {}
        url = self.urlM.format(item['id'])
        json_data = self.get_json(url)
        if json_data['code'] == 200 and len(json_data['songs']) == 1:
            data_J = json_data['songs'][0]
            result_dict = {
                "name": data_J['al']['name'],
                "picUrl": data_J['al']['picUrl'],
                "id": data_J['al']['id'],
                "ar": []
            }
            result_dict['ar'] = self.get_ar(data_J['ar'])
            return result_dict
        else:
            return {}

    def get_ar(self, item):
        ar_list = []
        for it in item:
            result_dict = {
                "id": it['id'],
                "name": it['name']
            }
            ar_list.append(result_dict)
        return ar_list

    def parse_json(self, Json):
        result_dict = {
            "name": Json['name'],
            "id": Json['id'],
            "coverImgUrl": Json['coverImgUrl'],
            "tags": Json['tags'],
            "tracks": []
        }
        for item in Json['trackIds']:
            json_list = self.get_track(item)
            if json_list is not None:
                result_dict['tracks'].append(json_list)
            else:
                pass
        print(Json['id'])
        print(result_dict['coverImgUrl'])
        return result_dict

    def run(self):
        # 将错误的字段名更正
        # self.connection_playlist.update_many(
        #     {}, {"$rename": {"coverImgId": "coverImgUrl"}}, False)
        data_frame = self.get_play_list_id()
        # data_frame = data_frame.drop([0])
        # data_frame = data_frame.loc[:1]
        # print(data_frame.loc[0])
        length = len(data_frame)
        for sym in range(length):
            print(sym)
            # item = self.connection_playlist.find(
            #     {"id": int(self.get_one_list(data_frame, sym))})
            # # print(item['coverImgUrl'])
            # length = item.count()

            # if length != 1:
            #     print({"id": int(self.get_one_list(data_frame, sym))})
            #     # print(self.connection_playlist.find_one(
            #     #     {"id": int(self.get_one_list(data_frame, sym))})['coverImgUrl'])
            #     self.connection_playlist.delete_one(
            #         {"id": int(self.get_one_list(data_frame, sym))})
            # break

            #     # 生成一个新的uel
            url = self.url.format(self.get_one_list(data_frame, sym))
            # 获取json，并进行处理
            json_data = self.get_json(url)
            # if json_data['code'] != 200:
            # continue
            # 生成我们的新的list
            # else:
            # 只换url
            json_data = json_data['playlist']
            # print(sym, '\n', json_data['name'], '\n', json_data['coverImgUrl'])
            # self.connection_playlist.update_one({"id": int(self.get_one_list(data_frame, sym))}, {
            #     "$set": {"coverImgUrl": json_data['coverImgUrl']}})
            tmp_dict = self.parse_json(json_data)
        # # print(json_data, '\n', type(json_data['id']), json_data['name'])
            self.connection_playlist.delete_many({"id": json_data['id']})
        # # # print(data)
            self.connection_playlist.insert_one(tmp_dict)
        # break
        # 我们需要将新的list存放到我们数据库
        # 但是我们list应该将数据库中的信息删除


if __name__ == '__main__':
    start = time.time()
    GL = GL()
    GL.run()
    end = time.time()
    print("执行时间:%.2f" % (end-start))
