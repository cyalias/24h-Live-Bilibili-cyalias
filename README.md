# 24h-Live-on-Bilibili_cyalias
Python写的一个bilibili弹幕点歌



树莓派驱动的b站直播点播台 [Demo](https://live.bilibili.com/7164303)


## 本项目是参考了下面两个大佬的部分代码完成的
### chenxuuu的项目
GitHub: https://github.com/chenxuuu/24h-raspberry-live-on-bilibili
### Crashiers的项目
GitHub: https://github.com/crashiers/Music-Live-on-Bilibili



## 歌曲下载部分参考
使用的是Am0xil的代码
地址：https://blog.csdn.net/zgbzbl/article/details/107773755

### 本项目的功能：
+ 弹幕点歌
+ 歌词滚动显示
+ 闲时随机播放预留歌曲
+ 已点播歌曲、视频自动进入缓存，无人点播时随机播放
+ 歌曲缓存只保留５０个，定时清理多余的缓存，防止存储爆满
+ 实时显示歌曲/视频长度

已知问题，待解决：
弹幕点歌，可能会失灵
自动换歌的时候，中间有段时间不显示画面

## 使用方法：
+ 确保是python3.6以上版本(建议使用python虚拟环境)
+ 安装ffmpeg，screen
+ 安装依赖包
+ pip install -r requirements.txt
+ 修改Config.json　配置文件
+ ./start.sh开启
