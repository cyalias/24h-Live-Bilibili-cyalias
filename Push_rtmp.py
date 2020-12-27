#!/home/cyalias/Pyenv/env_1/bin/python
# -*- coding: UTF-8 -*-
# @Time         :2020/12/24
# @Author       :Cyalias


import os
import json
import random
import time
import shutil
from mutagen.mp3 import MP3


config = json.load(open('./Config.json', encoding='utf-8'))
path = config['path']
rtmp_url = config['rtmp']['url']
code = config['rtmp']['code']
rtmpurl = '\"' + rtmp_url + code + '\"'
p_list = []
push_lock = False


oldbg = path + "/static/img/bg.jpg"
ass_path = path + "/static/lyric/"


def push_kongxian_rtmp():
    global push_lock
    song_files = []
    mp3_path = path + '/static/kongxian/'
    all_files = os.listdir(path + '/static/kongxian/')  # 获取所有缓存文件
    try:
        for item in all_files:
            if os.path.splitext(item)[1] == '.mp3':
                song_files.append(item)
        if len(song_files) > 0:
            if len(song_files) == 1 and os.path.exists(ass_path + song_files[0].replace('.mp3', '.ass')):
                print("空闲b")
                song_name = song_files[0]
                audio = MP3(mp3_path + song_name)  # 获取mp3文件信息
                seconds = audio.info.length  # 获取时长
                add_info = play_info()
                shutil.copy(ass_path + song_name.replace('.mp3', '.ass'), mp3_path)
                with open(mp3_path + song_name.replace('.mp3', '.ass'), 'a') as f:
                    f.write(add_info)
                push_lock = True
                cm = "ffmpeg -threads 0 -re -loop 1 -r 25 -t " + str(int(seconds)) + " -thread_queue_size 512 -f image2 -i " + oldbg + " -thread_queue_size 512 -i " + mp3_path + song_name + " -vf ass=" + mp3_path + song_name.replace('.mp3', ".ass") + " -s 1280*720 -pix_fmt yuv420p -preset ultrafast -crf 22 -tune zerolatency -acodec copy -vcodec libx264 -maxrate 3000k -b:a 128k -flvflags no_duration_filesize -f flv -g 5 -b 700000 " + rtmpurl
                print(cm)
                os.system(cm)
                os.remove(mp3_path + song_name.replace('.mp3', ".ass"))
                push_lock = False
            elif os.path.exists(ass_path + song_files[0].replace('.mp3', '.ass')):
                print("空闲a")
                song_files.sort()  # 排序文件
                song_ran = random.randint(0, len(song_files) - 1)
                song_name = song_files[song_ran]
                audio = MP3(mp3_path + song_name)  # 获取mp3文件信息
                seconds = audio.info.length  # 获取时长
                add_info = play_info()
                shutil.copy(ass_path + song_name.replace('.mp3', '.ass'), mp3_path)
                with open(mp3_path + song_name.replace('.mp3', '.ass'), 'a') as f:
                    f.write(add_info)
                push_lock = True
                # cm = "ffmpeg -re -loop 1 -r 30 -t " + str(int(seconds)) + " -f image2 -i " + oldbg + " -i " + video_path1 + song_name + " -vf ass=" + ass_path1 + "lunbo.ass" + " -s 1280*720 -pix_fmt yuv420p -preset ultrafast -maxrate 3000k -acodec copy -vcodec libx264 -f flv " + rtmp_url
                # cm = "ffmpeg -re  -r 25 -i " + video_path1 + song_name + " -vf ass=" + ass_path1 + "lunbo.ass" + " -pix_fmt yuv420p -preset ultrafast -maxrate 1000k -acodec aac -vcodec libx264 -f flv " + rtmpurl
                # cm = "ffmpeg -threads 0 -re -loop 1 -r 25 -t " + str(int(seconds)) + " -thread_queue_size 512 -f image2 -i " + oldbg + " -thread_queue_size 512 -i " + mp3_path + song_name + " -vf ass=" + mp3_path + song_name.replace('.mp3', ".ass") + " -s 1280*720 -pix_fmt yuv420p -preset ultrafast -crf 22 -tune zerolatency -acodec copy -vcodec libx264 -maxrate 3000k -b:a 128k -flvflags no_duration_filesize -f flv -g 5 -b 700000 " + rtmpurl
                #cm = "ffmpeg -threads 0 -re -loop 1 -r 25 -t " + str(int(seconds)) + " -thread_queue_size 512 -f image2 -i " + oldbg + " -thread_queue_size 512 -i " + mp3_path + song_name + " -vf ass=" + mp3_path + song_name.replace('.mp3', ".ass") + " -s 1280*720 -pix_fmt yuv420p -acodec copy -vcodec libx264 -maxrate 3200k -bufsize 300k -flvflags no_duration_filesize -f flv -g 5 -b 700000 " + rtmpurl
                cm = "ffmpeg -threads 0 -re -loop 1 -r 15 -t " + str(int(seconds)) + " -thread_queue_size 128 -f image2 -i " + oldbg + " -thread_queue_size 4096 -i " + mp3_path + song_name + " -vf ass=" + mp3_path + song_name.replace('.mp3', ".ass") + " -s 1280*720 -pix_fmt yuv420p -preset ultrafast -crf 25 -acodec aac -vcodec libx264 -maxrate 3200k -flvflags no_duration_filesize -f flv -g 5 -b 700000 " + rtmpurl
                print(cm)
                os.system(cm)
                os.remove(mp3_path + song_name.replace('.mp3', ".ass"))
                push_lock = False
            else:
                print('没有ass歌词')
        else:
            print('检查kongxian目录和lyric是否有文件')
    except IOError:
        pass


def push_play_rtmp(filename):
    global p_list
    global push_lock
    mp3_path = path + "/static/playlist/"
    audio = MP3(path + '/static/playlist/' + filename + '.mp3')  # 获取mp3文件信息
    seconds = audio.info.length  # 获取时长
    add_info = play_info()
    try:
        shutil.copy(ass_path + filename + '.ass', mp3_path)
        with open(mp3_path + filename + '.ass', 'a') as f:
            f.write(add_info)
        print('开始推流', filename)
        push_lock = True
        #cm = "ffmpeg -re -loop 1 -r 30 -t " + str(int(seconds)) + " -f image2 -i " + oldbg + " -i " + mp3_path + mp3_name + ".mp3" + " -vf ass=" + ass_path + filename + ".ok.ass" + " -s 1280*720 -pix_fmt yuv420p -preset ultrafast -maxrate 3000k -acodec copy -vcodec libx264 -f flv " + rtmp_url
        #cm = "ffmpeg -re -r 25 -i " + video_path + filename + ".ok.mp4" + " -pix_fmt yuv420p -preset ultrafast -maxrate 1000k -acodec aac -vcodec libx264 -f flv " + rtmpurl
        cm = "ffmpeg -threads 0 -re -loop 1 -r 25 -t " + str(int(seconds)) + " -thread_queue_size 512 -f image2 -i " + oldbg + " -thread_queue_size 512 -i " + mp3_path + filename + ".mp3" + " -vf ass=" + mp3_path + filename + ".ass" + " -s 1280*720 -pix_fmt yuv420p -preset ultrafast -crf 22 -tune zerolatency -acodec copy -vcodec libx264 -maxrate 3000k -b:a 128k -flvflags no_duration_filesize -f flv -g 5 -b 700000 " + rtmpurl
        print(cm)
        os.system(cm)
        print('结束推流', filename)
        shutil.move(mp3_path + filename + ".mp3", path + "/static/kongxian/")
        shutil.move(mp3_path + filename + ".info", path + "/static/kongxian/")
        os.remove(mp3_path + filename + ".ass")
        push_lock = False
    except IOError:
        pass


def transact(filename):
    global p_list
    p_list.append(filename)
    print('gangchuanguolai>', p_list)


def play_info():
    global p_list
    result = '\r\n'
    nm = len(p_list)
    if nm-1 > 0:
        s2 = p_list[1]
        try:
            with open(path + '/static/playlist/' + s2 + '.info', 'r') as f:
                a_str = f.readline()
        except IOError:
            pass
        a_list = a_str.split(',')
        result += 'Dialogue: 2,0:00:00.00,1:00:00.00,left_up,,0,0,0,,{\pos(10,70)}歌单还有' + str(nm-1) + '首歌，下一首：' + str(a_list[2]) + '\r\n'

    elif nm-1 == 0:
        result += 'Dialogue: 2,0:00:00.00,1:00:00.00,left_up,,0,0,0,,{\pos(10,70)}歌单还有' + str(nm-1) + '首歌，下一首将播放缓存歌曲' + '\r\n'
    else:
        result += 'Dialogue: 2,0:00:00.00,1:00:00.00,left_up,,0,0,0,,{\pos(10,70)}无人点歌，播放缓存歌曲' + '\r\n'
    return result

def run():
    mp3_path = path + "/static/playlist/"
    global p_list
    global push_lock
    print('panduan>', p_list)
    if len(p_list) == 0:
        while push_lock:
            time.sleep(1)
        print("a")
        push_kongxian_rtmp()
    elif len(p_list) > 0:
        while len(p_list) > 0:
            print('待播放列表：' + str(p_list))
            while push_lock:
                time.sleep(1)
            filename = p_list[0]
            if os.path.exists(mp3_path + filename + ".mp3"):
                push_play_rtmp(filename)
                p_list.pop(0)
            else:
                print("b")
                push_kongxian_rtmp()
