import time
import connMongo
import random
import pandas as pd

# from recomend import Recomend


class TakeEachCollect(object):
    def __init__(self):
        self.connection = connMongo.Conn_Mongo_CollectMusic()

    def time_stamp(self):
        # 生成13位得时间戳
        millis = int(round(time.time()*1000))
        return millis

    def stamp_to_time(self, millis):
        timeN = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(millis/1000))
        return timeN

    def get_item(self):
        data_spring = self.connection.find({})
        return data_spring

    def change_data(self, data_spring):
        for item in data_spring:
            T = random.randint(-99999, 99999)
            result_dict = {
                "userId": item['userId'],
                "musicId": item['musicId'],
                "tags": item['tags'],
                "timestamp": self.time_stamp() + T
            }
            self.connection.delete_many({"_id": item['_id']})
            self.connection.insert_one(result_dict)

    def run(self):
        self.change_data(self.get_item())
        # print(self.time_stamp())
        # print(self.stamp_to_time(self.time_stamp()))


if __name__ == '__main__':
    start_time = time.time()
    item = TakeEachCollect()
    item.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
