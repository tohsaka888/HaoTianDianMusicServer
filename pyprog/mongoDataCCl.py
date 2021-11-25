from calendar import day_abbr
import time
import random
import pandas as pd
import pymongo as pymg
import numpy as np
import tool_connMongo as connMongo
import tool_fileTouch as fileTouch


class MongoDataCCl(object):
    def __init__(self):
        self.connection = connMongo.Conn_Mongo_MusicByTags()
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
        df_answer_tags = data_frame_tags.head(10)
        # .append(
        #     pd.Series({
        #         'name': '其他',
        #         'value': data_frame_tags.tail(len(data_frame_tags)-9)['value'].sum()
        #     }), ignore_index=True)

        # data_frame_tags = data_frame_tags.drop_duplicates('tags')
        answer_dict = df_answer_tags.to_dict('records')
        return answer_dict

    def run(self):
        # 获取每种标签所关联的歌曲，并记录数据量
        fileTouch.save_file(fileTouch.path + "music_table.txt",
                            self.get_data_one())


if __name__ == '__main__':
    start_time = time.time()
    DCCl = MongoDataCCl()
    DCCl.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
