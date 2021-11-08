from bson import json_util

path = "/home/aliceMargetroid/express_server/HaoTianDianMusicServer/"


def save_file(filepath, save_json_content):
    # print(save_json_content, type(save_json_content))
    json_file = open(filepath, mode='w', encoding='utf-8')
    length = len(save_json_content)-1
    for sym in range(length):
        line = json_util.dumps(save_json_content[sym], ensure_ascii=False)
        json_file.write(line + '\n')
    json_file.write(json_util.dumps(
        save_json_content[length], ensure_ascii=False))


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        line = json_util.loads(f.read())
    return line


def open_fileL(filepath):
    data_dict = {
        "list": []
    }
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            data_dict['list'].append(json_util.loads(line))
    return data_dict
