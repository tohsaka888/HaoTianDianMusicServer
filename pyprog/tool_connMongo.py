import json
import os
import time
from pymongo import MongoClient
from bson import json_util


host = '81.68.113.218'
client = MongoClient(host, 27017)
db = client.admin
db.authenticate("tohsaka888", "swy156132264")
my_db = client.Music

def Conn_Mongo_MusicByTags():
    return my_db.MusicByTags

def Conn_Mongo_MusicPlayList():
    return my_db.MusicPlayList

def Conn_Mongo_MusicByArtists():
    return my_db.MusicArtists

def Conn_Mongo_CollectMusic():
    return my_db.CollectMusic

def Conn_Mongo_User():
    return my_db.user