import time
import math
import pandas as pd
import numpy as np
from pandas._config.config import reset_option
import pymongo

import tool_connMongo as connMongo
import tool_fileTouch as fileTouch

limits = 18


class Classify(object):
    def __init__(self):
        self.connection = connMongo.Conn_Mongo_MusicPlayList()

    @staticmethod
    def db_get(self, target_data):
        answer_list = self.get_play_list(target_data)
        index = int(target_data['page'])
        print(index)
        # page为-1时取出10页
        if index == -1:
            fileTouch.save_file(
                fileTouch.path + "music_playlist_data.txt",
                answer_list[0: limits * 10])
        # if index > math.ceil(len(answer_list)/limits):
        #     fileTouch.save_file(
        #         fileTouch.path + "music_palylist_data.txt",
        #         [{}])
        # # 将分割的数据存放
        # else:
        #     try:
        #         fileTouch.save_file(
        #             fileTouch.path + "music_playlist_data.txt",
        #             answer_list[
        #                 limits*(index-1):limits*index])
        #     except:
        #         fileTouch.save_file(
        #             fileTouch.path + "music_playlist_data.txt",
        #             answer_list[
        #                 limits*math.floor(len(answer_list)/limits):len(answer_list)])

    # 该方法处理问题： 我们需要避免给如果出翔某个数据得返回结果是0时的问题
    def db_rand_get(self):
        answer_dict = {
            "list": []
        }
        # 循环将数据转存为字典，并存放到list中
        answer_frame = pd.DataFrame(
            self.connection.aggregate([{'$sample': {'size': 200}}]))
        # print(answer_frame)
        answer_list = answer_frame.to_dict('records')
        answer_dict['list'] = answer_list
        return answer_dict

    @staticmethod
    def db_find(self, target_data):
        answer_list = self.get_play_list(target_data)
        # 假如生成的结果时空的，那么我们随机获取几首歌出现在歌曲list上，limits = 1000
        if len(answer_list) == 0:
            answer_list = self.db_rand_get()['list']
            # 存放所有的数据
        fileTouch.save_file(
            fileTouch.path + "music_playlist_all_data.txt", answer_list)
        index = int(target_data['page'])
        print(index)
        # page为-1时取出10页
        if index == -1:
            fileTouch.save_file(
                fileTouch.path + "music_playlist_data.txt",
                answer_list[0: limits * 10])
        # if index > math.ceil(len(answer_list)/limits):
        #     fileTouch.save_file(
        #         fileTouch.path + "music_playlist_data.txt",
        #         [{}])
        # else:
        #     # 将分割的数据存放
        #     try:
        #         fileTouch.save_file(
        #             fileTouch.path + "music_playlist_data.txt",
        #             answer_list[
        #                 limits*(index-1):limits*index])
        #     except:  # 出翔达到最后一组时，出现不满20个shi
        #         fileTouch.save_file(
        #             fileTouch.path + "music_playlist_data.txt",
        #             answer_list[
        #                 limits*math.floor(len(answer_list)/limits):len(answer_list)])

    def get_play_list(self, cat_data):
        data_spring = self.connection.find(
            {"tags": cat_data["tags"]}).sort("tags")
        data_frame = pd.DataFrame(data_spring)
        data_frame['index'] = 0
        # print(data_frame)
        for sym in range(data_frame.shape[0]):
            # print(data_frame.loc[sym]['tags'].index(cat_data['tags']))
            data_frame.loc[sym, 'index'] = data_frame.loc[sym]['tags'].index(
                cat_data['tags'])
        data_frame = data_frame.sort_values(by='index', ascending=True)
        return data_frame.to_dict('records')

    def run(self):
        cat_data = fileTouch.open_file(fileTouch.path + "music_cat.json")
        print(cat_data)
        if cat_data['tags'] != "":
            self.db_find(self, cat_data)
        else:
            self.db_get(self, cat_data)
        pass


if __name__ == '__main__':
    start_time = time.time()
    classify = Classify()
    classify.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
