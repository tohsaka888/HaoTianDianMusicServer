import time
import random
from typing import ClassVar
import pandas as pd
import numpy as np
import pymongo

import tool_connMongo as connMongo
import tool_fileTouch as fileTouch


class Classify(object):
    def __init__(self):
        self.connection = connMongo.Conn_Mongo_MusicByTags

    def run(self):
        pass


if __name__ == '__main__':
    start_time = time.time()
    classify = Classify()
    classify.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
