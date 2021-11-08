from os import PRIO_PGRP
import fileTouch
import time
import pandas as pd
import connMongo


class DaData(object):
    def __init__(self):
        self.connection_music = connMongo.Conn_Mongo_MusicByTags()
        self.connection_artist = connMongo.Conn_Mongo_MusicByArtists()
        self.data = fileTouch.open_file(
            "/home/aliceMargetroid/express_server/HaoTianDianMusicServer/pyprog/tmp/list.json")
        self.dict_tags = {
            "music": []
        }

    def addTracks(self, json_data):
        for item in json_data['tracks']:
            result = {
                "tags": json_data['tags'],
                "name": item['name'],
                "id": item['id'],
                "picUrl": item['picUrl'],
                "ar": item['ar']
            }
            self.connection_music.insert(result)
        # for curTagDict in json_data:
        #     for curPlayList in curTagDict['playListAll']:
        #         result_json = {
        #             "tags": curPlayList['tags'],
        #             "name": "none",
        #             "id": "none",
        #             "picUrl": "none",
        #             "ar": []
        #         }
        #         for element in curPlayList['tracks']:
        #             result_json = {
        #                 "tags": curPlayList['tags'],
        #                 "name": element['name'],
        #                 "id": element['id'],
        #                 "picUrl": element['picUrl'],
        #                 "ar": element['ar']
        #             }
        #             dict_temp = result_json
        #             dict_tags['music'].append(dict_temp)
        # return dict_tags

    def createAr(self, json_data):
        dict_arN = {
            "ar": []
        }
        dict_ar = []
        ar_list = []
        # for curTagDict in json_data:
        #     for curPlayList in curTagDict['playListAll']:
        curPlayList = json_data
        for song in curPlayList['tracks']:
            result_track_json = {
                "name": song['name'],
                "id": song['id'],
                "tags": curPlayList['tags'],
                "picUrl": song['picUrl']
            }
            # print(result_track_json)
            for i in range(len(song['ar'])):
                if song['ar'][i]['name'] not in ar_list:
                    ar_list.append(song['ar'][i]['name'])
                    result_json = {
                        "ar_name": song['ar'][i]['name'],
                        "tracks": []
                    }
                    dict_ar.append(result_json)
                dict_ar[ar_list.index(song['ar'][i]['name'])]['tracks']\
                    .append(result_track_json)
        for track in dict_ar:
            self.connection_artist.insert(track)

            # print(
            #     len(pd.DataFrame(self.connection_artist.find({"name": track["ar_name"]}))))

            # if :
            #     self.connection_artist.insert(track)
            # else:

    def run(self):
        # print(self.data)
        self.addTracks(self.data)
        # self.createAr(self.data)
        # print(data)


if __name__ == '__main__':
    start = time.time()
    prog = DaData()
    prog.run()
    end = time.time()
    print("执行时间:%.2f" % (end-start))
