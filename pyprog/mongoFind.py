# 默认打开的文件是当工作路径下的文件/src_target.txt
# 注：文件默认每一次打开读取后将其中内容清空
import json
import os

import pandas as pd
import time
import jieba
import math

from gensim import corpora,models,similarities

import fileTouch
import connMongo

answer_dict = {
    "list": []
}
limits = 20

# 判断字符类型
# 单词
def is_word(ch):
    if ch in range(65,91) or ch in range(97,123):
        return True
    return False

# 汉字
def is_character(ch):
    if '\u4e00' <= ch <= '\u9fff':
        return True
    return False

# 数字
def is_number(ch):
    if ch in range(48,58):
        return True
    return False

# 特殊字符
def is_special(ch):
    string = "~!@#$%^&*()_+-*/<>,.[]\/"
    if ch in string:
        return True
    return False
# 1. 从文件中获取-1这个时候，随机从文件获取歌曲信息,单独一个接口
# 2. 从数据库中获取信息，然后将这个信息交给文件中，并且将切片信息给到拎一个文件中
# 3. 
# 分割字符 以*
def split_target_str(target_str):
    answer_str = ""
    for ch in target_str:
        if target_str.index(ch) == 0 and is_word(ord(ch)):
            answer_str = answer_str + "*" + ch
        elif is_character(ch):
            answer_str = answer_str + '*' + ch
        elif is_word(ord(ch)):
            answer_str = answer_str + ch
        elif is_number(ord(ch)):
            answer_str = answer_str + '*' + ch
        elif is_special(ch):
            answer_str = answer_str + '*' + ch
        elif ch == " ":
            answer_str = answer_str + '*'
    return answer_str

# 相似度算法
def sort_similarity(name_list, tmp_list, str):
    all_name_list = []
    answer_list = []

    test_str_list = [word for word in jieba.cut(str)]
    for name in name_list:    
        name_ll = [word for word in jieba.cut(name)]
        all_name_list.append(name_ll)
    # 制作语料库
    # 获取词袋
    dictionary = corpora.Dictionary(all_name_list)
    dictionary.keys()
    dictionary.token2id
    # print(dictionary.token2id)
    # 语料库如下。语料库是一组向量，向
    # 量中的元素是一个二元组（编号、频次数），对应分词后的文档中的每一个词。
    corpus = [dictionary.doc2bow(name) for name in all_name_list]
    # print(corpora)
    test_str_vec = dictionary.doc2bow(test_str_list)
    # 相似度分析
    tfidf = models.TfidfModel(corpus)
    tfidf[test_str_vec]
    # print(tfidf[test_str_vec])
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
    sim = index[tfidf[test_str_vec]]
    # 获得按照相似的排序的结果
    sorted_name_lsit = sorted(enumerate(sim), key=lambda item: -item[1])
    # 根据结果重新排序
    for item in sorted_name_lsit:
        answer_list.append(tmp_list[item[0]])
    return answer_list


class MongoFind(object):
    def __init__(self):
        self.connection = connMongo.Conn_Mongo_MusicByTags()

    @staticmethod
    def db_get(self, target_data):
        answer_list = fileTouch.open_fileL(fileTouch.path + "music_name_all_data.txt")['list']
        index = int(target_data['page'])
        # 将分割的数据存放
        try:
            fileTouch.save_file(
                fileTouch.path + "music_name_data.txt",             
                answer_list[
                    limits*(index-1):limits*index])
        except:
            fileTouch.save_file(
                fileTouch.path + "music_name_data.txt",             
                answer_list[
                    limits*math.floor(len(answer_list)/limits):len(answer_list)])

    @staticmethod
    def db_find(self, target_data):
        answer_list = self.find_music_name(self.connection,target_data['musicName'],target_data['src_musicName'])['list']
        # 存放所有的数据
        fileTouch.save_file(fileTouch.path + "music_name_all_data.txt", answer_list)
        index = int(target_data['page'])
        # 将分割的数据存放
        try:
            fileTouch.save_file(
                fileTouch.path + "music_name_data.txt",             
                answer_list[
                    limits*(index-1):limits*index])
        except:
            fileTouch.save_file(
                fileTouch.path + "music_name_data.txt",             
                answer_list[
                    limits*math.floor(len(answer_list)/limits):len(answer_list)])

    @staticmethod
    def find_music_name(connection, str, target_str):
        id_list = []
        answer_dict = {
            "list": []
        }
        myquery = {"name": {"$regex": "/"+target_str+"/*"}}
        data_spring = connection.find(myquery)
        # 根据id进行去重
        name_Frame = pd.DataFrame(data_spring).drop_duplicates('id')
        # print(name_Frame)
        name_list = []
        tmp_list = []
        for row in name_Frame.itertuples():
            name_list.append(getattr(row,'name'))
            result_dict = {
                "id": getattr(row,'id'),
                "name":  getattr(row,'name'),
                "picUrl": getattr(row,'picUrl'),
                "tags": getattr(row,'tags'),
                "ar": getattr(row,'ar')
            }
            tmp_list.append(result_dict)
        answer_dict['list'] = sort_similarity(name_list, tmp_list, str)
        return answer_dict

    def run(self):
        target_data = fileTouch.open_file(fileTouch.path + 'music_name.json')
        if target_data['musicName'] != "":
            target_data['src_musicName'] = split_target_str(target_data['musicName'])
            self.db_find(self,target_data)
        else:
            self.db_get(self,target_data)


if __name__ == '__main__':
    start_time = time.time()
    find = MongoFind()
    find.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
