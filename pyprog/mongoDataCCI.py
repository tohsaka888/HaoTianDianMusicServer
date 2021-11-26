from calendar import day_abbr
from os import set_blocking
import time
import random
import pandas as pd
import pymongo as py
import numpy as np
import tool_connMongo as connMongo
import tool_fileTouch as fileTouch

limits = 12
name = "CatCountNL"


class MongoDataCCI(object):
    def __init__(self):
        self.connection = connMongo.Conn_Mongo_MusicByTags()
        self.connection_an = connMongo.Conn_Mongo_DataAnalyse()
        pass

    # 桶排序
    def get_data_one(self):
        data_spring = self.connection.find({},  {"tags": 1})
        data_frame = pd.DataFrame(data_spring)
        # 拆分数据
        df = pd.DataFrame({'_id': data_frame._id.repeat(
            data_frame.tags.str.len()), 'tags': np.concatenate(data_frame.tags.values)})
        data_frame_tags = pd.DataFrame(
            df.tags.value_counts()).reset_index()
        data_frame_tags.columns = ['name', 'value']
        df_answer_tags = data_frame_tags.head(limits)
        answer_dict = df_answer_tags.to_dict('records')

        return answer_dict

    def run(self):
        # 获取每种标签所关联的歌曲，并记录数据量
        self.connection_an.delete_many({"name": name})
        self.connection_an.insert_one(
            {"name": name, "result": self.get_data_one()})


if __name__ == '__main__':
    start_time = time.time()
    DCCl = MongoDataCCI()
    DCCl.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
