#!/home/cyalias/Pyenv/env_1/bin/python
# -*- coding: UTF-8 -*-
# @Time         :2020/12/24
# @Author       :Cyalias


import requests
import json
import time
import datetime
import re
import download_music


config = json.load(open('./Config.json', encoding='utf-8'))
header = config['web_headers']
roomid = config['danmu']['roomid']
cookie1 = config['danmu']['cookie']
token = config['danmu']['token']
header['Referer'] = 'https://live.bilibili.com/'
search_list = []
keys = ['song_name', 'ar_name', 'user']
# 创建一个old_list列表用于辅助后面的text_danmu方法提取新消息
old_list = []
# # 定义一个Danmu类
# class Danmu():
#     def __init__(self,):


url_path = "https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid="

data = {
        "roomid": roomid,
        "csrf_token": "",
        "csrf": token,
        "visit_id": ""
    }


# 创建一个text_danmu方法，用于提取弹幕信息
def text_danmu(html):
    # 设置变量作用域，使得该方法可以修改全局变量old_list的值
    global old_list

    # 创建一个temp_list列表用于作为临时列表辅助提取弹幕消息
    temp_list = []
    danmu_list = html["data"]["room"]
    #print(type(danmu_list))
    dm_num = len(danmu_list)
    #print(danmu_list)
    # 弹幕数量
    # for循环提取html字典中嵌套的子字典data中嵌套的子字典room的内容赋值给text变量
    # 这个html字典来自于get_danmu方法传递
    for text in danmu_list:
        temp_list.append(text["text"])
        #datetime.datetime.strptime('2015-03-05 17:41:20', '%Y-%m-%d %H:%M:%S')
        # int(time.strftime("%H%M%S", text["timeline"]))
        timeline = text["timeline"]
        user = text['nickname']
        timeline = datetime.datetime.strptime(timeline, '%Y-%m-%d %H:%M:%S')
        time_now = (datetime.datetime.now() + datetime.timedelta(minutes=-1)).strftime("%Y-%m-%d %H:%M:%S")
        time_now = datetime.datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
        #time_now = int(time.strftime(time_now, "%H%M%S"))
    # 检测temp_list临时列表的内容和old_list是否相同，如果相同则跳过
        if temp_list == old_list:
            pass
        else:
            # 创建for循环一次将1到10的数字赋给text_number
            for text_number in range(1, dm_num+1):
                if "".join(temp_list[:text_number]) in "".join(old_list):
                    pass
                # 使用join方法以""为分割符提取temp_list切割后的列表的内容
                # 使用join方法以""为分割符提取old_list列表的内容
                # 比较内容是否相同，如果相同则跳过
                else:
                    # print(temp_list[text_number-1])
                    # # 将temp_list的值赋给old_list，进行更新旧信息列表
                    if time_now < timeline:
                        pick_dm(temp_list[text_number - 1], user)
                        # if danmu_list[-1]['text'] not in old_list:
                        #     # print(temp_list[text_number - 1])
                        #     # print(user)
                        #     pick_dm(temp_list[text_number - 1], user)
                    old_list = temp_list[:]


def pick_dm(content, user):
    content = re.sub('\s+', ' ', content)
    sa_list = []
    if content.startswith("点歌,") | content.startswith("点歌，") | content.startswith("点歌 "):
        # 去掉多余空格，只保留一个空格
        dm_list = re.split("[,，\s]\s*", content)
        # re.sub(r"^(\s+)|(\s+)$", "", dm_list[0]) 去掉首尾空格
        if len(dm_list) <= 2:
            song_name = re.sub(r"^(\s+)|(\s+)$", "", dm_list[1])
            ar_name = "null"
            sa_list.append(song_name)
            sa_list.append(ar_name)
            sa_list.append(user)
        else:
            song_name = re.sub(r"^(\s+)|(\s+)$", "", dm_list[1])
            ar_name = re.sub(r"^(\s+)|(\s+)$", "", dm_list[2])
            sa_list.append(song_name)
            sa_list.append(ar_name)
            sa_list.append(user)
        # print(sa_list)
        #download_music.search_info(sa_list[0], sa_list[1], user)
        global search_list
        a_dict = dict(zip(keys, sa_list))
        download_music.transact(a_dict)


def get_danmu():
    url = url_path + roomid
    html = requests.post(url=url, headers=header, data=data)
    html.json()
    text_danmu(eval(html.text))
#定义get_danmu方法
#使用requests.post方法获取网页内容
#将网页返回值以json的信息加载
#调用之前定义的text_danmu方法，传递eval处理后的网页返回值的文本内容


#发送弹幕
def send_dm(message):
    send_message = message
    url = 'https://api.live.bilibili.com/msg/send'
    cookie = {'cookie': cookie1}

    data = {'fontsize': '25',
            'mode': '1',
            'color': '16777215',
            'rnd': str(time.time() * 1000000),  # 时间戳
            'msg': send_message,
            'roomid': roomid,
            'bubble': '0',
            'csrf_token': token,
            'csrf': token
            }

    # 构造请求
    response = requests.post(url, data=data, cookies=cookie)
