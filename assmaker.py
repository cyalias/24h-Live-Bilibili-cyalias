#!/home/cyalias/Pyenv/env_1/bin/python
# -*- coding: UTF-8 -*-
# @Time         :2020/12/24
# @Author       :Cyalias


import os
import time
import re
from mutagen.mp3 import MP3


#生成字幕文件，传入参数：
#filename：文件名
#info：文件信息，用于左下角显示用的
#path：文件路径
#ass：最原始的歌词数据
def make_ass(filename, info, path, ass=''):
    ass = lrc_to_ass(ass)
    timer_get = timer_create(filename, path)
    file_content = '''[Script Info]
Title: Default ASS file
ScriptType: v4.00+
WrapStyle: 2
Collisions: Normal
PlayResX: 960
PlayResY: 720
ScaledBorderAndShadow: yes
Video Zoom Percent: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,2,10,10,5,1
Style: left_down,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,1,10,10,5,1
Style: right_down,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,3,10,10,5,1
Style: left_up,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,7,10,10,5,1
Style: right_up,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,9,10,10,5,1
Style: center_up,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,8,10,10,5,1
Style: center_up_big,微软雅黑,28,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,8,10,10,5,1
Style: center_down,微软雅黑,30,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,2,10,10,5,1
Style: center_down_big,微软雅黑,45,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,2,10,10,5,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 2,0:00:00.00,1:00:00.00,left_down,,0,0,0,,'''+info+'''
Dialogue: 2,0:00:00.00,1:00:00.00,right_down,,0,0,0,,基于树莓派3B+/Python\\N'''+'点播日期：'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'''
Dialogue: 2,0:00:00.00,1:00:00.00,left_up,,0,0,0,,明月免费点歌台~
Dialogue: 2,0:00:00.00,1:00:00.00,right_up,,0,0,0,,弹幕点播方法: \\N点歌,歌曲名字,歌手 
'''+ass+timer_get
    file = open(path+'/static/lyric/'+str(filename)+'.ass', 'w')    #保存ass字幕文件
    file.write(file_content)
    file.close()
    print(filename + "ass生成成功")
    try:
        os.remove(path + '/static/lyric/' + str(filename) + '.lrc')
    except:
        pass


# 生成info文件
def make_playlist(filename, info, path):
    file_content = filename + ',' + info
    file = open(path+'/static/playlist/' + str(filename) + '.info', 'w')
    file.write(file_content)
    file.close()


def s3t(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return ("%01d:%02d:%02d" % (h, m, s))


def timer_create(filename, path):
    result = '\r\n'
    filename = filename.replace('ok', '')
    if(os.path.isfile(path+'/static/playlist/'+str(filename)+'.mp3')):
        try:
            audio = MP3(path+'/static/playlist/'+str(filename)+'.mp3')   #获取mp3文件信息
            seconds = int(audio.info.length)   #获取时长
            for i in range(1, seconds):
                result += 'Dialogue: 2,' + s3t(i-1) + '.00,' + s3t(i) + '.00,right_down,,0,0,0,,歌曲时间:' + s3t(i) + '/' + s3t(seconds) + '\r\n'
        except Exception as e:
            print('shit(get song length)')
            print(e)
    return result


#滚动歌词生成
def lrc_to_ass(lrc):
    if os.path.exists(lrc):
        with open(lrc, 'r') as f:
            lryic = f.read()
        lrc = lryic.splitlines() #按行分割开来
        list1 = ['00', '00']
        list2 = ['00', '00']
        list3 = ['00', '00']
        list4 = [' ', ' ']
        result = '\r\n'
        for i in lrc:
            matchObj = re.match(r'.*\[(\d+):(\d+)\.(\d+)\]([^\[\]]*)', i)  #正则匹配获取每行的参数，看不懂的去自行学习正则表达式
            if matchObj:    #如果匹配到了东西
                list1.append(matchObj.group(1))
                list2.append(matchObj.group(2))
                list3.append(matchObj.group(3))
                list4.append(matchObj.group(4))
        list1.append('05')
        list1.append('05')
        list2.append('00')
        list2.append('00')
        list3.append('00')
        list3.append('00')
        list4.append(' ')
        list4.append(' ')
        for i in range(2, len(list1)-4):
            text = '　'+list4[i+1]+'　\\N　'+list4[i+2]+'　'
            result += 'Dialogue: 2,0:'+list1[i]+':'+list2[i]+'.'+list3[i][0:2]+',0:'+list1[i+1]+':'+list2[i+1]+'.'+list3[i+1][0:2]+',center_down,,0,0,0,,'+text+'\r\n'
            text = '　'+list4[i]+'　'
            result += 'Dialogue: 2,0:'+list1[i]+':'+list2[i]+'.'+list3[i][0:2]+',0:'+list1[i+1]+':'+list2[i+1]+'.'+list3[i+1][0:2]+',center_down_big,,0,0,0,,'+text+'\r\n'
            text = '　'+list4[i-2]+'　\\N　'+list4[i-1]+'　'
            result += 'Dialogue: 2,0:'+list1[i]+':'+list2[i]+'.'+list3[i][0:2]+',0:'+list1[i+1]+':'+list2[i+1]+'.'+list3[i+1][0:2]+',center_down,,0,0,0,,'+text+'\r\n'
        #修正倒数第二句句歌词消失的bug
        text = '　'+list4[len(list1)-3]+'　\\N　'+list4[len(list1)-2]+'　'
        result += 'Dialogue: 2,0:'+list1[len(list1)-4]+':'+list2[len(list1)-4]+'.'+list3[len(list1)-4][0:2]+',0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',center_down,,0,0,0,,'+text+'\r\n'
        text = '　'+list4[len(list1)-4]+'　'
        result += 'Dialogue: 2,0:'+list1[len(list1)-4]+':'+list2[len(list1)-4]+'.'+list3[len(list1)-4][0:2]+',0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',center_down_big,,0,0,0,,'+text+'\r\n'
        text = '　'+list4[len(list1)-6]+'　\\N　'+list4[len(list1)-5]+'　'
        result += 'Dialogue: 2,0:'+list1[len(list1)-4]+':'+list2[len(list1)-4]+'.'+list3[len(list1)-4][0:2]+',0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',center_down,,0,0,0,,'+text+'\r\n'
        #修正最后一句歌词消失的bug
        text = '　'+list4[len(list1)-2]+'　\\N　'+list4[len(list1)-1]+'　'
        result += 'Dialogue: 2,0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',0:10:00.00,center_down,,0,0,0,,'+text+'\r\n'
        text = '　'+list4[len(list1)-3]+'　'
        result += 'Dialogue: 2,0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',0:10:00.00,center_down_big,,0,0,0,,'+text+'\r\n'
        text = '　'+list4[len(list1)-5]+'　\\N　'+list4[len(list1)-4]+'　'
        result += 'Dialogue: 2,0:'+list1[len(list1)-3]+':'+list2[len(list1)-3]+'.'+list3[len(list1)-3][0:2]+',0:10:00.00,center_down,,0,0,0,,'+text+'\r\n'
        return result
    else:
        result = 'Dialogue: 2, 0: 00:00.00, 1: 00:00.00, center_down,, 0, 0, 0,, 无歌词'
    return result



