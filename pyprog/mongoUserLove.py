from pandas.core.indexes.timedeltas import timedelta_range
import tool_connMongo
import pandas as pd
import tool_fileTouch as fileTouch
import time


class UserLove(object):
    def __init__(self):
        # 连接到收藏表中
        self.connection_user = tool_connMongo.Conn_Mongo_CollectMusic()
        # 连接到用户表中
        self.connection_u = tool_connMongo.Conn_Mongo_User()
        # 连接到音乐表中
        self.connection_music = tool_connMongo.Conn_Mongo_MusicByTags()

    # get spring message from collectMusic table by the name of userId
    # at the same time ,we will list the message by the time
    # retuen the message like the pandas
    def get_music_mine(self, target_userId):
        data_frame = pd.DataFrame(self.connection_user.find(
            {"userId": target_userId}).sort([("timestamp", -1)]))
        return data_frame.drop(['_id', 'userId', 'timestamp'], axis=1)

    def get_music_thing(self, tmp_list, userId):
        music = pd.DataFrame(self.connection_music.find(
            {"id": tmp_list[0]['musicId']}))
        result_dict = {
            "name": "我喜欢的音乐",
            "id": userId,
            "coverImgUrl": music['picUrl'].values[0],
            "tracks": []
        }
        for item in tmp_list:
            music_frame = pd.DataFrame(
                self.connection_music.find({"id": item['musicId']}))
            result_item_dict = music_frame.drop(
                ['_id', 'heat'], axis=1).to_dict('records')
            result_dict['tracks'].append(result_item_dict[0])

        return result_dict

    def run(self):
        # 获取查询对象
        target_userId = fileTouch.open_file(
            fileTouch.path + "music_recomend.json")['userId']
        tmp_0_list = self.get_music_mine(int(target_userId)).to_dict('records')
        # 处理对象
        answer_list = [self.get_music_thing(tmp_0_list, target_userId)]
        fileTouch.save_file(
            fileTouch.path + "music_user_love.txt", answer_list)


if __name__ == '__main__':
    start = time.time()
    UL = UserLove()
    UL.run()
    end = time.time()
    print("执行时间:%.2f" % (end-start))
