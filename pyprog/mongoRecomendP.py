import json
import os
import time
import math
import fileTouch
import connMongo

import numpy as np
import pandas as pd

from sklearn.model_selection import KFold
from itertools import chain

limits = 9 #..


class MongoRecomend(object):
    def __init__(self):
        self.connection_user = connMongo.Conn_Mongo_CollectMusic()
        self.connection_musicPL = connMongo.Conn_Mongo_MusicPlayList()
        self.connection_u = connMongo.Conn_Mongo_User()

    def check_user(self, target_userId):
        data_spring = self.connection_u.find({"userId": target_userId})
        return (data_spring is None)

    def insert_user(self, target_userId):
        self.connection_u.insert_one({"musicId": int(target_userId)})
    # 使用target获得某用户的信息
    def search_user_music(self, target_userId):
        data_frame = pd.DataFrame(self.connection_user.find({"userId": target_userId}))
        return data_frame

    def twodim_to_one_dim(self, src_list):
        user_tags_list = []
        user_tags_list.extend(item for elem in src_list for item in elem)
        return user_tags_list
        
    def catch_tags_rate(user,user_tags_list, user_tags_frame):
        vc_frame = pd.DataFrame((user_tags_frame[0].value_counts()).reset_index())
        vc_frame.columns = ['tag','frequency']
        vc_frame = vc_frame.head(3)
        return vc_frame            

    def recommend_music(self, src_user_music_frame, user_tags_rate):
        tags_list = user_tags_rate['tag'].values.tolist()
        result_frame = pd.DataFrame()
        # 按tags查询结果
        for item in tags_list:
            dest_frame = pd.DataFrame(self.connection_musicPL.find(
                {"tags": {"$all": [item]}}
            ))
            result_frame = result_frame.append(dest_frame, ignore_index=True).drop_duplicates('id').drop('_id',axis=1)
        # 删除重复项
        all_frame = result_frame[~result_frame['id'].isin(src_user_music_frame['musicId'])].reset_index().drop('index',axis=1)
        new_frame = all_frame.sample(n=limits, axis=0).reset_index().drop('index',axis=1)
        return new_frame

    def recommend_music_new_user(self):
        new_frame = pd.DataFrame(self.connection_musicPL.aggregate([{'$sample': {'size': limits}}]))
        return new_frame.drop('_id',axis=1)

    def run(self):
        answer_list = []
        target_userId = fileTouch.open_file(fileTouch.path+ "music_recomend.json")['userId']
        print(target_userId)
        if self.check_user(target_userId):
            # 插入新用户
            self.inser_user(target_userId)
        # 获得标签list
        user_frame = self.search_user_music(target_userId)
        if (len(user_frame)==0):
            answer_list = self.recommend_music_new_user().to_dict('records')   
        else :
            user_frame = user_frame.drop('_id',axis=1)
            user_tags_list = self.twodim_to_one_dim(user_frame['tags'].values.tolist())
            # 计算每个出现的tag的概率，同时保留高于平均频率以上的值
            user_tags_rate_frame = self.catch_tags_rate(user_tags_list, pd.DataFrame(user_tags_list))
            # 根据频率和源数据，生成结果表，并生成list写到文件中
            print(user_tags_rate_frame)
            answer_list = self.recommend_music(user_frame, user_tags_rate_frame).to_dict('records')
        # 写道文件中
        fileTouch.save_file(fileTouch.path + "music_recomendP.txt", answer_list)


if __name__ == '__main__':
    start_time = time.time()
    recom = MongoRecomend()
    recom.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))