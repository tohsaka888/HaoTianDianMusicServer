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
        if data_ar is None:
            print("None")
        # for item in data_ar:
        #     print(item['ar_name'])

    def insert_data(self, data_src, data_dest):
        pass

    def run(self):
        data_spring = self.take_frommusicAr()
        for item in data_spring:
            self.check_data(item)


if __name__ == '__main__':
    start = time.time()
    TA = TakceAr()
    TA.run()
    end = time.time()
    print("执行时间:%.2f" % (end-start))
