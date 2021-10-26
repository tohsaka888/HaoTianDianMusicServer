# 默认打开的文件是当工作路径下的文件/src_target.txt
# 注：文件默认每一次打开读取后将其中内容清空
import json
import os

import pandas as pd
import time

from bson import json_util

from connMongo import ConnMongo

answer_dict = {
    "list": []
}


def split_target(target_str):
    target_list = []
    length = len(target_str)
    for step in range(length):
        for start in range(length - step):
            target_list.append(target_str[start:start + (step + 1)])
    return target_list


class MongoFind(object):
    def __init__(self):
        self.connection = ConnMongo().my_db

    @staticmethod
    def db_find(self, target_str):
        self.save_file(
            os.getcwd() + "/data_music.txt",
            self.find_music_tags(
                self.connection,
                split_target(target_str)
            )['list']
        )

    @staticmethod
    def find_music_tags(connection, target_list):
        print("tags")
        id_list = []

        data_spring = connection.MusicByTags.find({})
        data_tags_frame = pd.DataFrame(data_spring)

        index = len(data_tags_frame)
        set_target_list = set(target_list)
        for sym in range(index):
            set_single_spring = set(
                list(split_target(data_tags_frame.loc[sym]['name']))
            )
            answer_list = list(set_target_list.intersection(set_single_spring))
            if answer_list:
                result_dict = {
                    "element": data_tags_frame.loc[sym].astype('string'),
                    "frequency": len(answer_list)
                }
                if result_dict['element']['id'] not in id_list:
                    # print(result_dict)
                    id_list.append(result_dict['element']['id'])
                    answer_dict['list'].append(result_dict)
        data_answer_frame = pd.DataFrame(answer_dict['list'])
        del answer_dict['list'][:]
        data_answer_frame = data_answer_frame.sort_values(by='frequency')
        length = len(data_answer_frame)
        for sym in range(length):
            answer_dict['list'].append(data_answer_frame.loc[sym]['element'])
        return answer_dict

    @staticmethod
    def open_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            line = f.readlines()
        return line[0]
        pass

    @staticmethod
    def save_file(filepath, save_json_content):
        json_file = open(filepath, mode='w', encoding='utf-8')
        #
        length = len(save_json_content)-1
        for sym in range(length):
            line = json_util.dumps(save_json_content[sym], ensure_ascii=False)
            json_file.write(line + '\n')
        json_file.write(json_util.dumps(save_json_content[length], ensure_ascii=False))

    def run(self):
        target_data = self.open_file(os.getcwd() + '/music_name.txt')
        self.db_find(self, target_data)
        pass


if __name__ == '__main__':
    start_time = time.time()
    find = MongoFind()
    find.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
