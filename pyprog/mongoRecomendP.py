import math
import time
import tool_fileTouch as fileTouch

import tool_connMongo as connMongo

import numpy as np
import pandas as pd

from tool_recomend import Recomend


class MongoRecomend(object):
    def __init__(self):
        self.connection_musicPL = connMongo.Conn_Mongo_MusicPlayList()

    # 为信用推荐歌曲
    def music_new_user(self, limits):
        new_frame = pd.DataFrame(self.connection_musicPL.aggregate(
            [{'$sample': {'size': limits}}]))
        return new_frame.drop('_id', axis=1)

    # 搜索挑选出的tags相关的歌曲
    def recommend_musicPL(self, src_user_music_frame, user_tags_rate, limits):
        # tags_list = user_tags_rate['tag'].values.tolist()
        result_frame = pd.DataFrame()
        length = len(user_tags_rate)
        # 按tags查询结果
        for it in range(length):
            limit = math.ceil(
                user_tags_rate.iloc[it, 1] * limits/user_tags_rate['frequency'].sum())
            dest_frame = pd.DataFrame(self.connection_musicPL.aggregate(
                [
                    {"$match": {
                        "tags": {"$all": [user_tags_rate.iloc[it, 0]]}}},
                    {'$sample': {'size': limit+2}}
                ]
            ))
            result_frame = result_frame.append(
                dest_frame, ignore_index=True).drop_duplicates('id')
        # 删除重复项
        all_frame = result_frame[~result_frame['id'].isin(
            src_user_music_frame['musicId'])].reset_index().drop('index', axis=1)
        new_frame = all_frame.sample(
            n=limits, axis=0).reset_index().drop('index', axis=1)
        return new_frame.drop('_id', axis=1)

    def run(self):
        recomend = Recomend()
        answer_list = []
        target_userId = fileTouch.open_file(
            fileTouch.path + "music_recomend.json")['userId']
        if recomend.check_user(target_userId):
            # 插入新用户
            recomend.inser_user(target_userId)
            answer_list = self.music_new_user(9).to_dict('records')
            fileTouch.save_file(
                fileTouch.path + "music_recomendP.txt", answer_list)
            return
        # 获得标签list
        answer_list = self.music_new_user(9).to_dict('records')
        user_frame = recomend.search_user_music(target_userId)
        # 此处信息不方便// 当出现意外的时候将会有一份信息输出
        try:
            user_tags_list = recomend.twodim_to_onedim(
                user_frame['tags'].values.tolist())
        except:
            answer_list = self.music_new_user(9).to_dict('records')
        # 计算每个出现的tag的概率，同时保留高于平均频率以上的值
        # 仅取出最高的三个标签
        user_tags_rate_frame = recomend.catch_tags_rate(
            pd.DataFrame(user_tags_list))
        # print(user_tags_rate_frame)
        # 根据频率和源数据，生成结果表，并生成list写到文件中
        answer_list = self.recommend_musicPL(
            user_frame, user_tags_rate_frame, 9).to_dict('records')
        # 写道文件中
        fileTouch.save_file(
            fileTouch.path + "music_recomendP.txt", answer_list)


if __name__ == '__main__':
    start_time = time.time()
    recom = MongoRecomend()
    recom.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
