# 默认打开的文件是当工作路径下的文件/src_target.txt
# 注：文件默认每一次打开读取后将其中内容清空
import json
import os

import pandas as pd
import time
import jieba
import math

from gensim import corpora, models, similarities

import tool_fileTouch as fileTouch
import tool_connMongo as connMongo

limits = 18


class MongoPLCat(object):
    def __init__(self):
        self.connection = connMongo.Conn_Mongo_MusicPlayList()

    def get_PL(self, tag, page):
        if page > 0:
            PL_frame = pd.DataFrame(self.connection.aggregate(
                [
                    {"$match": {"tags": {"$all": tag}}},
                    {"$skip": (page-1)*limits},
                    {"$limit": limits}
                ]
            ))
            if len(PL_frame) == 0:
                return []
            return PL_frame.drop('_id', axis=1).to_dict('records')
        else:
            return []
        pass

    def run(self):
        target_cat = fileTouch.open_file(fileTouch.path+'music_cat.json')
        answer_list = self.get_PL(
            [target_cat['tags']], int(target_cat['page']))
        fileTouch.save_file(fileTouch.path + "music_pl.txt", answer_list)


if __name__ == '__main__':
    start_time = time.time()
    pLCat = MongoPLCat()
    pLCat.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
