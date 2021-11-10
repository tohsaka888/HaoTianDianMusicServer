import time
import fileTouch
import connMongo

import pandas as pd

from recomend import Recomend

limits = 20  # ..


class MyuLove(object):
    def __init__(self):
        self.connection_music = connMongo.Conn_Mongo_MusicByTags()

    # 抓取我们用户对应得两张表 （CollectMusic 、 user）
    # def music_new_user(self, limits):
    #     new_frame = pd.DataFrame(
    #         self.connection_music.aggregate([{'$sample': {'size': limits}}]))
    #     return new_frame.drop('_id', axis=1)

    # def recommend_music(self, src_user_music_frame, user_tags_rate, limits):
    #     pass

    # start
    def run(self):
        userId = fileTouch.open_file(fileTouch.path + "music_recomend.json")
        print(userId)
        data_frame = Recomend.search_user_music(Recomend(), userId['userId'])
        print(data_frame)


if __name__ == '__main__':
    start_time = time.time()
    loveL = MyuLove()
    loveL.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
