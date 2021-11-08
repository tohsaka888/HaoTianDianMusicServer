import time
import os
import connMongo
import fileTouch
import pandas as pd


class MHL(object):
    def __init__(self):
        self.connection = connMongo.Conn_Mongo_MusicByTags()

    def get_heat(self):
        answer_frame = pd.DataFrame(
            self.connection.find({}).sort("heat", -1).limit(50)).drop('_id', axis=1)
        print(answer_frame)
        return answer_frame.to_dict('records')

    def run(self):
        answer_list = []
        answer_list = self.get_heat()
        fileTouch.save_file(
            fileTouch.path + "music_heat_list.txt", answer_list)
        pass


if __name__ == '__main__':
    start_time = time.time()
    mhl = MHL()
    mhl.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
