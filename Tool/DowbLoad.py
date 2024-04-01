import json
import os
import re
import subprocess
import time
from pprint import pprint

from lxml import etree
from tqdm import tqdm

from Tool.RequestUrl import RequestUrl


class DownLoad(object):
    def __init__(self, url, cookie):
        if not os.path.exists('.\\DownLoad'):
            os.makedirs('.\\DownLoad')
        self.url = url
        self.cookie = cookie
        self.origin = 'https://www.bilibili.com/'
        self.current_dir = os.path.dirname(__file__)
        try:
            # 发送请求并检查响应是否正常
            response = RequestUrl(self.url, referer=self.url, cookie=self.cookie, origin=self.origin)
            # 解析视频信息
            result = re.findall(r'<script>window.__playinfo__=(.*?)</script>', response.text)[0]
            self.data = json.loads(result)
            html = etree.HTML(response.text)
            video_title = html.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[1]/div/h1/text()')[0]
            video_title = video_title.replace(' ', '')
            self.video_title = re.sub(r'\W+', '', video_title).replace('_', '')
            #pprint(self.data['data'])
            self.quality = dict(zip(self.data['data']['accept_description'], self.data['data']['accept_quality']))
            # 获取音频和视频的URL
            self.audio_url = self.data['data']['dash']['audio']#[0]['baseUrl']
            self.video_url = self.data['data']['dash']['video']#[0]['baseUrl']
        except Exception as e:
            print(e)
    def download(self, down_data,sel):
        if sel=='.mp3':
            '''30280,30216,30232'''
            # print({'32112':'极高音质', '30280':'高音质', '30264':'中音质', '30232':'低音质', '30216':'极低音质'})
            # select = input('选择对应的id:')
            # 默认最高音质
            url = self.select_id(down_data, '30280')
        else:
            print(self.quality)
            select = input('选择对应的id:')
            url = self.select_id(down_data, select)

        if len(url) != 0:
            for i in url:
                content_video = RequestUrl(i, referer=self.url, cookie=self.cookie, origin=self.origin)

                if content_video is not None:
                    total_size = int(content_video.headers.get('content-length', 0))
                    block_size = 1024
                    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
                    with open('.\\DownLoad\\' + self.video_title + sel, 'wb') as f:
                        for data in content_video.iter_content(block_size):
                            progress_bar.update(len(data))
                            f.write(data)
                    progress_bar.close()
                    print('视频下载完成')
                    break
                else:
                    print(f'链接 {i[0]} 已失效')

        else:
            print('当前账号不支持清晰度下载')

    def select_id(self, data, select):
        '''backupUrl,backup_url,baseUrl,base_url'''
        return [i['baseUrl'] for i in data if str(i['id']).strip() == select]

    def Clear_down(self):
        os.remove('.\\DownLoad\\' + self.video_title + '.mp4')
        os.remove('.\\DownLoad\\' + self.video_title + '.mp3')

    def merge_video_and_audio(self):
        print("正在为您下载，请稍后")
        # 合并音频和视频
        merge_command = f'ffmpeg -loglevel quiet -i .\\DownLoad\\{self.video_title}.mp4 -i .\\DownLoad\\{self.video_title}.mp3 -c:v copy -c:a aac -strict experimental .\\DownLoad\\{self.video_title}output.mp4'
        subprocess.run(merge_command, shell=True)
        print('音视频合并完成')
        time.sleep(2)
        self.Clear_down()
        print('垃圾清理完毕')


    def run(self):
        print("请选择你要下载的方式")
        sel = input("1.仅下载音频\n2.仅下载视频（无声音）\n3.下载视频\n")
        if sel == '1':
            self.download(self.audio_url,'.mp3')
        elif sel == '2':
            self.download(self.video_url,'.mp4')
        elif sel == '3':
            self.download(self.audio_url, '.mp3')
            self.download(self.video_url, '.mp4')
            self.merge_video_and_audio()
