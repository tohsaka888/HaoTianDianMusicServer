import json
import os
import time
import math
import pandas as pd

from gensim import corpora,models,similarities

import fileTouch
import connMongo

# 如何修改相似算法，需要data_list 处理的对象之后会和srclist进行比对
# tmp_list必须和前面data_list顺序一致，用于之后结果生成时，使用data_list的顺序依次将tmp_list的内容排序
# src_list用于比对data_list
def sort_similarity(data_list, tmp_list, src_list):
    # 制作语料库
    # 获取词袋
    answer_list = []
    dictionary = corpora.Dictionary(data_list)
    dictionary.keys()
    dictionary.token2id
    # print(dictionary.token2id)
    # 语料库如下。语料库是一组向量，向
    # 量中的元素是一个二元组（编号、频次数），对应分词后的文档中的每一个词。
    corpus = [dictionary.doc2bow(data) for data in data_list]
    # print(corpora)
    test_str_vec = dictionary.doc2bow(src_list)
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


class MongoSimi(object):
    def __init__(self):
        self.connection_music = connMongo.Conn_Mongo_MusicByTags()
        self.connection_user = connMongo.Conn_Mongo_CollectMusic()
    
    def music_user_set(self,target_musicId):
        # 获得包含该音乐的用户，并返回用户id list
        target_music_user_frame = pd.DataFrame(self.connection_user.find({"musicId": target_musicId}))
        result_list = target_music_user_frame['userId'].values.tolist()
        return result_list

    def get_music_tags(self, musicId):
        # 获得单个对象，返回这个对象中的tags
        answer_dict = dict(self.connection_music.find_one({"id": musicId}))
        return answer_dict['tags']


    def by_tags_get(self ,tags):
        result_frame = pd.DataFrame()
        # 按tags查询结果
        for item in tags:
            dest_frame = pd.DataFrame(self.connection_music.find(
                {"tags": {"$all": [item]}}
            ))
            result_frame = result_frame.append(dest_frame, ignore_index=True)
        # 删除重复项
        result_frame = result_frame.drop_duplicates('id').drop('_id',axis=1)
        # 转换全部结果为list
        result_list = result_frame.to_dict('records')
        # 转换tags数据为list
        tags_list = result_frame['tags'].values.tolist()
        # 根据tags的相似度，对所有格去进行一个排序
        answer_list = sort_similarity(tags_list, result_list, tags)
        return answer_list[:10] 

    def all_user_music_set(self, users):
        # 临时变量
        result_frame = pd.DataFrame()
        # 根据用户查询
        for user in users:
            tmp_frame = pd.DataFrame(self.connection_user.find({"userId":user}))
            result_frame = result_frame.append(tmp_frame, ignore_index=True)
        # 获得结果
        # 统计这些歌同时被几个人收藏。。。 1. 计算每一个元素重复的次数 2.将生成的data_frame的index改为新额一列，并对这些列重命名
        vc_frame = pd.DataFrame((result_frame['musicId'].value_counts())).reset_index()
        vc_frame.columns=['musicId','count']
        vc_frame = vc_frame[vc_frame['count']>1]
        # 生成结果表，这里存放了收藏同一首歌的人还收藏了。。。1. 删除无用列 2. 删除一列中的重复数据 3. 重新生成index
        result_frame = result_frame.drop('_id',axis=1).drop_duplicates(subset=['musicId']).reset_index(drop=True)
        # 将两张表相连接，冰降序拍啊徐
        result_frame = pd.merge(vc_frame,result_frame , on='musicId',how='inner')
        # 删除重复次数小于3的数据
        # reset_frame = reset_frame.drop_duplicates
        return result_frame

    def run(self):
        target_musicId = fileTouch.open_file(fileTouch.path + "music_similarity.json")['musicId']
        result = self.connection_music.find_one({"id": target_musicId})
        
        # by tags
        # answer_list = self.by_tags_get(self.get_music_tags(target_musicId))
        # 以下原则上适合的大量用户各自按照喜好选择的歌曲，通过之间的交集进行计算得到的数据，
        # 如果这个查询的对象生成时是随机的，那么选择使用tags方法会更加高效
        if result is None: 
            answer_list = [{}]
        else: 
            src_user_list = self.music_user_set(target_musicId)
            if len(src_user_list) == 1:
                # print(len(src_frame['music']), src_frame['tags'])
                answer_list = self.by_tags_get(list(self.get_music_tags(target_musicId))) 
            else:
                # print(list(src_frame['userId']))
                # 在这里根据用户将所有的music获取
                tmp_frame = self.all_user_music_set(src_user_list)
                # 删除查询源数据
                frame = tmp_frame.drop(tmp_frame[tmp_frame['musicId'] == target_musicId].index)
            if len(frame) < 10:
                answer_list = self.by_tags_get(list(self.get_music_tags(target_musicId)))
            else:
                answer_list = frame.to_dict('records')         
        fileTouch.save_file(fileTouch.path + "music_similarity.txt", answer_list)


if __name__ == '__main__':
    start_time = time.time()
    similarity = MongoSimi()
    similarity.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))