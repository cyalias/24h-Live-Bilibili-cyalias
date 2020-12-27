#!/home/cyalias/Pyenv/env_1/bin/python
# -*- coding: UTF-8 -*-
# @Time         :2020/12/24
# @Author       :Cyalias


import re
import requests
import json
import base64
import binascii
import random
import string
from urllib import parse
from Crypto.Cipher import AES
import time
import datetime
import assmaker
import Danmu
import Push_rtmp


config = json.load(open('./Config.json', encoding='utf-8'))
path = config['path']
Accept = config['web_headers']['Accept']
Accept_Encoding = config['web_headers']['Accept-Encoding']
Accept_Language = config['web_headers']['Accept-Language']
Connection = config['web_headers']['Connection']
User_Agent = config['web_headers']['User-Agent']
content_type = config['web_headers']['content-type']
search_list = []

# 从a-z,A-Z,0-9中随机获取16位字符
def get_random():
    random_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    return random_str


# AES加密要求加密的文本长度必须是16的倍数，密钥的长度固定只能为16,24或32位，因此我们采取统一转换为16位的方法
def len_change(text):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    text = text.encode("utf-8")
    return text


# AES加密方法
def aes(text, key):
    # 首先对加密的内容进行位数补全，然后使用 CBC 模式进行加密
    iv = b'0102030405060708'
    text = len_change(text)
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(text)
    encrypt = base64.b64encode(encrypted).decode()
    return encrypt


# js中的 b 函数，调用两次 AES 加密
# text 为需要加密的文本， str 为生成的16位随机数
def b(text, str):
    first_data = aes(text, '0CoJUm6Qyw8W8jud')
    second_data = aes(first_data, str)
    return second_data


# 这就是那个巨坑的 c 函数
def c(text):
    e = '010001'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    text = text[::-1]
    result = pow(int(binascii.hexlify(text.encode()), 16), int(e, 16), int(f, 16))
    return format(result, 'x').zfill(131)


# 获取最终的参数 params 和 encSecKey 的方法
def get_final_param(text, str):
    params = b(text, str)
    encSecKey = c(str)
    return {'params': params, 'encSecKey': encSecKey}


# 通过参数获取搜索歌曲的列表
def get_music_list(params, encSecKey):
    url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
    payload = 'params=' + parse.quote(params) + '&encSecKey=' + parse.quote(encSecKey)
    headers = {
        'authority': 'music.163.com',
        'user-agent': User_Agent,
        'content-type': content_type,
        'accept': Accept,
        'origin': 'https://music.163.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://music.163.com/search/',
        'accept-language': Accept_Language,
        'Accept-Encoding': Accept_Encoding,
        'Connection': Connection
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


# 通过歌曲的id获取播放链接
def get_reply(params, encSecKey):
    url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
    payload = 'params=' + parse.quote(params) + '&encSecKey=' + parse.quote(encSecKey)
    headers = {
        'authority': 'music.163.com',
        'user-agent': User_Agent,
        'content-type': content_type,
        'accept': Accept,
        'origin': 'https://music.163.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://music.163.com/',
        'accept-language': Accept_Language,
        'Accept-Encoding': Accept_Encoding,
        'Connection': Connection
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


# 通过歌曲的id获取歌曲lyric
def get_song_lyric(song_id):
        lrc_url = 'http://music.163.com/api/song/lyric?id='+str(song_id)+'&lv=1&kv=1&tv=-1'
        headers = {
            'authority': 'music.163.com',
            'User-Agent': User_Agent,
            'content-type': content_type,
            'accept': Accept,
            'origin': 'https://music.163.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'Refer': 'http://music.163.com',
            'accept-language': Accept_Language,
            'Accept-Encoding': Accept_Encoding,
            'Connection': Connection
        }
        res = requests.get(lrc_url, headers=headers)
        lyric = res.text
        json_obj = json.loads(lyric)
        try:
            lyric = json_obj['lrc']['lyric']
        except KeyError:
            print("无歌词")
            lyric = "null"
            return lyric
        else:
            return lyric

def down_music(item, user):
    global a_name
    headers = {
        'authority': 'music.163.com',
        'user-agent': User_Agent,
        'content-type': content_type,
        'accept': Accept,
        'origin': 'https://music.163.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://music.163.com/',
        'accept-language': Accept_Language,
        'Accept-Encoding': Accept_Encoding,
        'Connection': Connection
    }
    # 获取时间戳，用来当作文件名,避免有特殊字符，导致ffmpeg推流失败和异常
    filename = str(time.mktime(datetime.datetime.now().timetuple()))
    song_id = json.loads(str(item))['id']
    song_ar = json.loads(str(item))['ar'][0]['name']
    song_lyric = get_song_lyric(song_id)
    song_name = ((json.loads(str(item))['name']).replace("/", "")).replace(" ", "")
    song_name = song_name.replace("（", "(").replace("）", ")")
    d = {"ids": "[" + str(json.loads(str(item))['id']) + "]", "level": "standard", "encodeType": "",
         "csrf_token": ""}
    d = json.dumps(d)
    random_param = get_random()
    param = get_final_param(d, random_param)
    song_info = get_reply(param['params'], param['encSecKey'])
    if len(song_info) > 0:
        song_info = json.loads(song_info)
        song_url = json.dumps(song_info['data'][0]['url'], ensure_ascii=False)
        song_url = re.sub('\"', '', song_url)
        song_url = song_url.encode()
        response = requests.get(song_url, headers=headers)
        content = response.content
        song_file_path = path + "/static/playlist/" + filename
        save_file(song_file_path + '.mp3', content, 'wb')
        print('歌曲（' + song_name + '）下载成功')
        lyric_file_path = path + "/static/lyric/" + filename
        #如果没有歌词，就不保存歌曲歌词动作
        if song_lyric != "null" and song_url != "None":
            save_file(lyric_file_path + '.lrc', song_lyric, 'w')
            print('歌曲（' + song_name + '）歌词下载成功')

        lyric = lyric_file_path + '.lrc'
        assmaker.make_ass(filename, '当前网易云id：' + str(song_id) + "\\N歌曲:" + song_name + "\\N歌手:" + song_ar + "\\N点播人:" + user, path, lyric)  # 生成字幕
        assmaker.make_playlist(filename, str(song_id) + "," + song_name + "," + song_ar + ',' + user, path)
        # print('等待渲染')
        print('已加入播队列')
        try:
            with open(path + '/static/playlist/' + filename + '.info', 'r') as f:
                a_str = f.readline()
        except:
            pass
        a_list = a_str.split(',')
        Danmu.send_dm(str("<<" + a_list[2]) + ">>已加入播队列")
        Push_rtmp.transact(filename)


    else:
        return "该首歌曲解析失败，可能是因为歌曲格式问题"


# 通过歌曲列表循环下载歌曲
def get_download_info(song_list, arname, user):
    """下载音乐"""
    if len(song_list) > 0:
        song_list = json.loads(song_list)['result']['songs']

        if arname == "null":
            item = json.dumps(song_list[0])
            down_music(item, user)

        else:
            a = 0
            for i, item in enumerate(song_list):
                item = json.dumps(item)
                song_ar = json.loads(str(item))['ar'][0]['name']
                if song_ar == arname:
                    a = 1
                    down_music(item, user)
                    break
            if a == 0:
                item = json.dumps(song_list[0])
                song_name = (json.loads(str(item))['name']).replace("/", "")
                print("没有找到有关歌手[" + arname + "]唱的<" + song_name + ">这首歌！")
                Danmu.send_dm("没找到[" + str(arname) + "]唱的<<" + str(song_name) + ">>这首歌！")
    else:
        print("没有搜到")


#　保存歌曲
def save_file(filename, content, mode):
    """保存音乐"""
    with open(file=filename, mode=mode) as f:
        f.write(content)
        f.flush()
        f.close()


# # 将下载下来的lrc文件转成srt字幕文件
# def lrc_srt(lrc_full_path, srt_full_path):
#     os.system('ffmpeg -i ' + lrc_full_path + ' ' + srt_full_path)


def search_info(songname, arname, user):
    d = {
        "hlpretag": "<span class=\"s-fc7\">",
         "hlposttag": "</span>",
         "s": songname,
        "type": "1",
         "offset": "0",
         "total": "true",
         "limit": "30",
         "csrf_token": ""
    }
    d = json.dumps(d)
    random_param = get_random()
    param = get_final_param(d, random_param)
    song_list = get_music_list(param['params'], param['encSecKey'])
    get_download_info(song_list, arname, user)


def transact(a_dict):
    global search_list
    search_list.append(a_dict)


def run():
    global search_list
    while len(search_list) > 0:
        print(search_list[0]['song_name'])
        search_info(search_list[0]['song_name'], search_list[0]['ar_name'], search_list[0]['user'])
        search_list.pop(0)


# songname = "辞九门回忆"
# arname = "null"
# search_info(songname, arname)
