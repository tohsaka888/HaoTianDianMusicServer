import pandas as pd
import pymongo as py

import time


import tool_connMongo as connMongo
import tool_fileTouch as fileTouch


limits = 25
name = "ArtistCountNL"


class MongoDataCCAr(object):
    def __init__(self):
        self.connection = connMongo.Conn_Mongo_MusicByArtists()
        self.connection_an = connMongo.Conn_Mongo_DataAnalyse()
        pass

    def get_data_one(self):
        data_frame = pd.DataFrame(self.connection.aggregate(
            [
                {"$project": {
                    "name": "$ar_name",
                    "value": {"$size": "$tracks"}}
                 },
                {"$sort": {"value": -1}}
            ]
        ))
        return data_frame.head(limits).drop('_id', axis=1).to_dict('records')

    def run(self):
        self.connection_an.delete_many({"name": name})
        self.connection_an.insert_one(
            {"name": name, "result": self.get_data_one()})


if __name__ == '__main__':
    start_time = time.time()
    DCCAr = MongoDataCCAr()
    DCCAr.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
