import time


import tool_connMongo as connMongo
import tool_fileTouch as fileTouch
from tool_recomend import Recomend


class CeckColle(object):
    def __init__(self):
        self.connection_coll = connMongo.Conn_Mongo_CollectMusic()
        self.connection_u = connMongo.Conn_Mongo_User()

    def judge_music_existence(self, check_data):
        recomend = Recomend()
        if recomend.check_user(check_data['userId']):
            recomend.inser_user(check_data['userId'])
        if self.connection_coll.find_one(check_data) is None:
            return [{"existence": False}]
        else:
            return [{"existence": True}]

    def run(self):
        fileTouch.save_file(
            fileTouch.path + "music_colle_existence.txt",
            self.judge_music_existence(
                fileTouch.open_file(fileTouch.path + "music_colle_existence.json")))


if __name__ == '__main__':
    start = time.time()
    ChC = CeckColle()
    ChC.run()
    end = time.time()
    print("执行时间:%.2f" % (end-start))
