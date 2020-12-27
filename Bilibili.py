#!/home/cyalias/Pyenv/env_1/bin/python
# -*- coding: UTF-8 -*-
# @Time         :2020/12/24
# @Author       :Cyalias


import time
import threading
import Danmu
import os
import json


config = json.load(open('./Config.json', encoding='utf-8'))
path = config['path']


path1 = path + '/static/kongxian/'
path2 = path + '/static/lyric/'


def delete_files(path0):
    all_files = os.listdir(path0)
    #　删除元素中最后一个点后边的内容，即去掉后缀只留文件名字
    for i, v in enumerate(all_files): all_files[i] = v.rpartition('.')[0]
    #　去列表中的重复元素
    all_files = list(set(all_files))
    # 排序
    all_files.sort(reverse=True)
    try:
        if len(all_files) > 50:
            for item in all_files[50:]:
                os.remove(path0 + item)
    except:
        pass


def df():
    while True:
        delete_files(path1)
        delete_files(path2)
        time.sleep(1800)


def pr():
    import Push_rtmp
    while True:
        Push_rtmp.run()


def dm():
    import download_music
    while True:
        download_music.run()


t1 = threading.Thread(target=pr)
t4 = threading.Thread(target=df)
t5 = threading.Thread(target=dm)
t1.start()
t4.start()
t5.start()


while True:
    Danmu.get_danmu()
    time.sleep(3)
    # 每三秒钟调用一个bzhan实例的get_danmu方法
