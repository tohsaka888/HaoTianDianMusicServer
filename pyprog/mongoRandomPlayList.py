import time
import os 
import connMongo
import fileTouch


class MongoRandomPlayList(object):
    def __init__(self):
        # 生成一个连接
        self.connection = connMongo.Conn_Mongo_MusicPlayList()

    def random_music(self):
        answer_dict = {
            "list": []
        }
        # 循环将数据转存为字典，并存放到list中
        for item in self.connection.aggregate([{'$sample': {'size': 20}}]):
            result_dict = dict(item)
            answer_dict['list'].append(result_dict)
        return answer_dict
 
    def run(self):
        print("random_playlist")
        fileTouch.save_file(fileTouch.path + 'random_playlist.txt', self.random_music()['list'])    


if __name__=='__main__':
    start_time = time.time()
    find = MongoRandomPlayList()
    find.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))