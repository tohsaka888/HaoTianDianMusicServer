
import json
import os
# from typing_extensions import ParamSpec

import requests
import time
import random

import fileTouch
# from requests.sessions import _Data

# from Cloud.utils.fileTou import FileTou
from tmp.ua_info import ua_list  # 自定义的ua池


class CloudPlayListSpider(object):
    def __init__(self):
        # self.login = login()
        # self.playlist = playlist()
        self.url = "http://cloud-music.pl-fe.cn/playlist/detail?id=24381616"
        self.songurl = "http://cloud-music.pl-fe.cn/song/detail?ids={}"
        # pass
        # 定义常用变量,比如url或计数变量等
        # self.url = 'http://cloud-music.pl-fe.cn/top/playlist?cat={}'

    def get_json(self, url):
        # 获取响应内容函数,使用随机User-Agent
        req = requests.post(url,
                            headers={'User-Agent': random.choice(ua_list)})
        Json = req.json()
        return Json
    #     # pass

    def parse_json(self, Json):
        # 获得json数据是字典模式的，且需要的数据在all - sub 内
        # 使用正则表达式来解析页面，提取数据
        # print(Json)
        result = {
            "list": [
                {
                    "name": Json['name'],
                    "id": Json['id'],
                    "coverImgUrl": Json['coverImgUrl'],
                    "tags": Json['tags'],
                    "tracks":[]
                }
            ]
        }
        list = []
        for item in Json['trackIds']:
            result_dict = {
                "id": item['id']
            }
            # print(result_dict)
            result['list'][0]['tracks'].append(result_dict)
        return result
        pass

    def parse_song(self, data):
        result = {
            "name": data['al']['name'],
            "picUrl": data['al']['picUrl'],
            "id": data['al']['id'],
            "ar": []
        }
        for item in data['ar']:
            result_dict = {
                "name": item['name']
            }
            result["ar"].append(result_dict)
        print(result)
        return result

    def run(self):
        data = self.get_json(self.url)
        # print(data['playlist']['id'])
        answer_dict = self.parse_json(data['playlist'])
        for sym in range(len(answer_dict['list'][0]["tracks"])):
            url = self.songurl.format(
                answer_dict['list'][0]["tracks"][sym]['id'])
            data = self.get_json(url)
            result_dict = self.parse_song(data['songs'][0])
            answer_dict['list'][0]["tracks"][sym] = result_dict
        fileTouch.save_file(
            "/home/aliceMargetroid/express_server/HaoTianDianMusicServer/pyprog/tmp/list.json", answer_dict['list'])


if __name__ == '__main__':
    # 程序开始运行时间
    # cookie = "MUSIC_A_T=1514153612071; __remember_me=true; MUSIC_R_T=1514153650217; MUSIC_U=60eda557f75356a9bcb4c7680ab45f46ffdf534d9230cf97c7799a0b962ee003993166e004087dd3d78b6050a17a35e705925a4e6992f61d07c385928f88e8de; __csrf=37a1f3094514f2f6a4a7bfcb5f8ec721; NMTID=00O-MDuTXaAP5Pfu0VGjF7FEJtzUwAAAAF89Md5vA"
    # trans = TransCookie(cookie)
    # trans_ = trans.StringToDict()
    start = time.time()
    spider = CloudPlayListSpider()
    spider.run()
    end = time.time()
    print("执行时间:%.2f" % (end-start))
