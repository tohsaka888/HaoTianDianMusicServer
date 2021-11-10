import numpy as np
import time
import connMongo

class WriteUserId(object):
    def __init__(self):
        self.connection_user = connMongo.Conn_Mongo_CollectMusic()
        self.connection_music = connMongo.Conn_Mongo_MusicByTags()
        self.connection_u = connMongo.my_db.user

    def setRandomUserId(self):
        randomUser = np.random.randint(low=1000000, high=19999999, size=(100))
        return randomUser

    def connect_music(self):
        result_dict = {}
        for item in self.connection_music.aggregate([{'$sample': {'size': 1}}]):
            result_dict = dict(item)
        return result_dict
        

    @staticmethod    
    def set_pseudo_data(self, user_list):
        answer_dict = {
            "list1": [],
            "list2": []
        }
        for user in user_list:
            print(user)
            user_str = int(user)
            result_dict1 = {
                    "userId": user_str
            }
            answer_dict['list1'].append(result_dict1)    
            for turn in range(20):
                item_dict = self.connect_music()
                reslut_dict2 = {
                    "userId": user_str,
                    "musicId": item_dict['id'],
                    "tags": item_dict['tags']
                }
                answer_dict['list2'].append(reslut_dict2)
        return answer_dict

    def run(self):
        user_list = self.setRandomUserId()
        reslut_dict = self.set_pseudo_data(self, user_list)
        self.connection_user.delete_many({})
        for item in reslut_dict['list2']:
            self.connection_user.insert_one(item)
        self.connection_u.delete_many({})
        for item in reslut_dict['list1']:
            self.connection_u.insert_one(item)


if __name__=='__main__':
    start_time = time.time()
    writeUser = WriteUserId()
    writeUser.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))#   