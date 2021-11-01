import time
import os 
import connMongo 
import fileTouch


class MongoRandom(object):
    def __init__(self):
        # 生成连接
        self.connection = connMongo.Conn_Mongo_MusicByTags()
   
    def random_music(self):
        answer_dict = {
            "list": []
        }
        # 随机获得一个音乐数据
        for item in self.connection.aggregate([{'$sample': {'size': 1}}]):
            result_dict = dict(item)
            answer_dict['list'].append(result_dict)
        return answer_dict
     
    def run(self):
        fileTouch.save_file(fileTouch.path + 'random_music.txt', self.random_music()['list'])    


if __name__=='__main__':
    start_time = time.time()
    find = MongoRandom()
    find.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
