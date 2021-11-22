import time
import os
import tool_connMongo as connMongo
import tool_fileTouch as fileTouch
import pandas as pd


class MongoRandom(object):
    def __init__(self):
        # 生成连接
        self.connection = connMongo.Conn_Mongo_MusicByTags()

    def random_music(self):
        dest_frame = pd.DataFrame(
            self.connection.aggregate([{'$sample': {'size': 1}}]))
        
        answer_list = dest_frame.drop('_id',axis=1).to_dict('records')
        return answer_list

    def run(self):
        fileTouch.save_file(fileTouch.path + 'random_music.txt',
                            self.random_music())


if __name__ == '__main__':
    start_time = time.time()
    find = MongoRandom()
    find.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
