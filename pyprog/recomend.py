import connMongo
import pandas as pd


class Recomend(object):
    def __init__(self):
        # 单独user表用于存放已存在的用户
        self.connection_u = connMongo.Conn_Mongo_User()
        # 存放user收藏的歌曲 ，通过user和music的id 唯一化
        self.connection_user = connMongo.Conn_Mongo_CollectMusic()

    # user Check
    def check_user(self, target_userId):
        data_spring = self.connection_u.find({"userId": target_userId})
        return (data_spring is None)

    def insert_user(self, target_userId):
        self.connection_u.insert_one({"musicId": int(target_userId)})

    # 使用target获得某用户的信息
    def search_user_music(self, target_userId):
        data_frame = pd.DataFrame(
            self.connection_user.find({"userId": target_userId}))
        return data_frame

    # 处理tags列表，二维转一维
    def twodim_to_onedim(self, src_list):
        user_tags_list = []
        user_tags_list.extend(item for elem in src_list for item in elem)
        return user_tags_list

    # 检查tags列表并将这个列表进行排序，排序的基准是tags出现的频率
    def catch_tags_rate(user, user_tags_frame):
        vc_frame = pd.DataFrame(
            (user_tags_frame[0].value_counts()).reset_index())
        vc_frame.columns = ['tag', 'frequency']
        vc_frame = vc_frame.head(3)
        return vc_frame
