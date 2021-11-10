from pandas.core.indexes.timedeltas import timedelta_range
import connMongo
import pandas as pd


class UserLove(object):
    def __init__(self):
        # 连接到收藏表中
        self.connection_user = connMongo.Conn_Mongo_CollectMusic()
        # 连接到用户表中
        self.connection_u = connMongo.Conn_Mongo_User()
        # 连接到音乐表中
        self.connection_music = connMongo.Conn_Mongo_MusicByTags()

    # get spring message from collectMusic table by the name of userId
    # at the same time ,we will list the message by the time
    # retuen the message like the pandas
    def get_music_mine(self, target_userId):
        data_frame = pd.DataFrame(self.connection_user.find(
            {"userId": target_userId}).sort({"timestamp": -1}))
        return data_frame

    def get_music_thing(self, data_frame):
        pass

# if __name__ == '__main__':
#     start = time.time()
#     SHA = SetHeatAr()
#     SHA.run()
#     end = time.time()
#     print("执行时间:%.2f" % (end-start))
