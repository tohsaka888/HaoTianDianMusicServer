import time
import tool_fileTouch as fileTouch

import tool_connMongo as connMongo

import pandas as pd

from tool_recomend import Recomend

limits = 20  # ..


class MongoRecomend(object):
    def __init__(self):
        self.connection_music = connMongo.Conn_Mongo_MusicByTags()

    def music_new_user(self, limits):
        new_frame = pd.DataFrame(
            self.connection_music.aggregate([{'$sample': {'size': limits}}]))
        return new_frame.drop('_id', axis=1)

    def recommend_music(self, src_user_music_frame, user_tags_rate, limits):
        tags_list = user_tags_rate['tag'].values.tolist()
        result_frame = pd.DataFrame()
        # 按tags查询结果
        for item in tags_list:
            dest_frame = pd.DataFrame(self.connection_music.find(
                {"tags": {"$all": [item]}}
            ))
            result_frame = result_frame.append(
                dest_frame, ignore_index=True).drop_duplicates('id').drop('_id', axis=1)
        # 删除重复项
        all_frame = result_frame[~result_frame['id'].isin(
            src_user_music_frame['musicId'])].reset_index().drop('index', axis=1)
        new_frame = all_frame.sample(
            n=limits, axis=0).reset_index().drop('index', axis=1)
        return new_frame

    def run(self):
        recomend = Recomend()
        answer_list = []
        target_userId = fileTouch.open_file(
            fileTouch.path + "music_recomend.json")['userId']
        print(target_userId)
        if recomend.check_user(target_userId):
            # 插入新用户
            recomend.inser_user(target_userId)
        # 获得标签list
        user_frame = recomend.search_user_music(target_userId)
        if (len(user_frame) == 0):
            answer_list = self.music_new_user(20).to_dict('records')
        else:
            user_frame = user_frame.drop('_id', axis=1)
            user_tags_list = recomend.twodim_to_onedim(
                user_frame['tags'].values.tolist())
            # 计算每个出现的tag的概率，同时保留高于平均频率以上的值
            user_tags_rate_frame = recomend.catch_tags_rate(
                pd.DataFrame(user_tags_list))
            # 根据频率和源数据，生成结果表，并生成list写到文件中
            answer_list = self.recommend_music(
                user_frame, user_tags_rate_frame, 20).to_dict('records')
        # 写道文件中
        fileTouch.save_file(
            fileTouch.path + "music_recomendM.txt", answer_list)


if __name__ == '__main__':
    start_time = time.time()
    recom = MongoRecomend()
    recom.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
