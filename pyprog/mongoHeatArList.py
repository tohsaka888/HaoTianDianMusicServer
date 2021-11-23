import time
import pandas as pd
import numpy as np

import tool_fileTouch as fileTouch
import tool_connMongo as connMongo

class SetHeatAr(object):
    def __init__(self):
        self.connection_ar = connMongo.Conn_Mongo_MusicByArtists()
        
    # firstly,we need touch the databsee named MusicByArtusts, 
    # we should sum the heat 
    def get_heat(self):
        answer_frame = pd.DataFrame(
            self.connection_ar.find({}).sort("heat", -1).limit(50)).drop('_id', axis=1)
        # print(answer_frame)
        return answer_frame.to_dict('records')

    def run(self):
        answer_list = []
        answer_list = self.get_heat()
        fileTouch.save_file(
            fileTouch.path + "music_ar_heat_list.txt", answer_list)
        pass

if __name__ == '__main__':
    start = time.time()
    SHA = SetHeatAr()
    SHA.run()
    end = time.time()
    print("执行时间:%.2f" % (end-start))
