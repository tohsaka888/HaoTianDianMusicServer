import time
import os
import pandas as pd
from pymongo import database
import tool_connMongo as connMongo
import tool_fileTouch as fileTouch


class MongoRandomPlayList(object):
    def __init__(self):
        # 生成一个连接
        self.connection = connMongo.Conn_Mongo_MusicPlayList()

    def random_music(self):
        dest_frame = pd.DataFrame(
            self.connection.aggregate([{'$sample': {'size': 15}}]))
        answer_list = dest_frame.drop('_id', axis=1).to_dict('records')
        return answer_list

    def run(self):
        fileTouch.save_file(
            fileTouch.path + 'random_playlist.txt', self.random_music())


if __name__ == '__main__':
    start_time = time.time()
    find = MongoRandomPlayList()
    find.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
