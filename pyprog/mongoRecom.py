import json
import os
import pandas as pd
import time
import jieba
import math
from gensim import corpora,models,similarities

import fileTouch
from connMongo import ConnMongo

class MongoRecom(objecct):
    def __init__(self):
        self.connection = ConnMongo().my_db.MusicByTags

    def search_user(self):
        pass

    def recommend_music():
        answer_dict = {
            "list": []
        }

        return answer_dict

    def run(self):
        fileTouch.open_file(fileTouch.path + 'user_message.json')


if __name__ == '__main__':
    start_time = time.time()
    recom = MongoRecom()
    recom.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))