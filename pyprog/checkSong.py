import json
import time
import random
from numpy import int64, result_type, string_
from pymongo.message import _batched_write_command_impl, delete

import tool_connMongo as connMongo
import pandas as pd
import pymongo
import requests

from ua_info import ua_list


class CSong(object):
    def __init__(self):
        self.url = "http://cloud-music.pl-fe.cn/check/music?id={}"
        self.connection_playlist = connMongo.Conn_Mongo_MusicPlayList()

    def get_json(self, url):
        req = requests.post(
            url, headers={'User-Agent': random.choice(ua_list)})
        Json = req.json()
        return Json

    def run(self):
        data_spring = self.connection_playlist.find({})
        print(data_spring.count())
        sym = 0
        for item in data_spring:
            new_tracks = []
            for elem in item['tracks']:
                if elem == {}:
                    continue
                url = self.url.format(elem['id'])
                Json = self.get_json(url)
                if Json['success'] != False:
                    new_tracks.append(elem)
                else:
                    continue
            print(sym, len(new_tracks))
            time.sleep(3)
            sym += 1
            if (new_tracks == []):
                self.connection_playlist.delete_many({"id": int(item['id'])})
                print("Success")
            else:
                item_dict = {
                    "name": item['name'],
                    "id": item['id'],
                    "tags": item['tags'],
                    "coverImgUrl": item['coverImgUrl'],
                    "tracks": new_tracks
                }
                self.connection_playlist.delete_many({"id": int(item['id'])})
                self.connection_playlist.insert_one(item_dict)
            # for elem in item['tracks']:
        #     print(elem)


if __name__ == '__main__':
    start = time.time()
    CS = CSong()
    CS.run()
    end = time.time()
    print("执行时间:%.2f" % (end-start))
