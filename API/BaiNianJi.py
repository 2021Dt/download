import json
import os
import re
import subprocess
import time
from pprint import pprint

import execjs
from tqdm import tqdm
from Tool.RequestUrl import RequestUrl


class BaiNianJi(object):
    def __init__(self, url, cookie):

        self.url = url
        self.origin = 'https://www.bilibili.com/'
        self.cookie = cookie
        respon = RequestUrl(url, referer=url, origin=self.origin, cookie=self.cookie)
        information = re.findall(r'<script>window.__INITIAL_STATE__=(.*?)</script>', respon.text, re.S)[0]
        if information == '':
            print('拜年祭解析失败')
            raise ValueError("未找到视频信息")

        information = re.sub(r';\(.*\);', '', information)

        self.infor = json.loads(information)
        #pprint(self.infor)
        self.name = self.infor['sectionEpisodes'][0]['title']
        self.avid = self.infor['sectionEpisodes'][0]['aid']
        self.bvid = self.infor['sectionEpisodes'][0]['bvid']
        self.cid = self.infor['sectionEpisodes'][0]['cid']
        self.current_dir = os.path.dirname(__file__)

        if not os.path.exists('.\\拜年祭'):
            os.makedirs('.\\拜年祭')
        alldata = RequestUrl(self.api(), referer=self.url, cookie=self.cookie).json()
        alldata = alldata['data']
        self.dash = alldata['dash']
        self.accept_quality = alldata['accept_quality']
        self.accept_description = alldata['accept_description']
        self.audio = self.dash['audio']
        self.video = self.dash['video']
        self.quality = dict(zip(alldata['accept_description'], alldata['accept_quality']))
        #pprint(self.audio)
        #pprint(self.video)

    def api(self):
        file_path = os.path.join(self.current_dir, 'w_rid.js')
        compile_code = execjs.compile(open(file_path, 'r', encoding='utf-8').read())
        wts = compile_code.call('wts')
        key = f'avid={self.avid}&bvid={self.bvid}&cid={self.cid}&fnval=4048&fnver=0&fourk=1&from_client=BROWSER&gaia_source=&qn=80&session=&voice_balance=1&web_location=1315873&wts=' + wts
        w_rid = compile_code.call('w_rid', key)
        api = f'https://api.bilibili.com/x/player/wbi/playurl?avid={self.avid}&bvid={self.bvid}&cid={self.cid}&qn=80&fnver=0&fnval=4048&fourk=1&gaia_source=&from_client=BROWSER&session=&voice_balance=1&web_location=1315873&w_rid={w_rid}&wts={wts}'
        return api

    def Clear_down(self):
        os.remove('.\\拜年祭\\' + self.name + '.mp4')
        os.remove('.\\拜年祭\\' + self.name + '.mp3')

    def run_view(self, select):
        select = int(select)

        self.downinfor_video = dict(zip(self.accept_quality, [[] for i in range(len(self.accept_description))]))




        for i in self.video:
            self.downinfor_video[i['id']].append(i['backupUrl'])

        #pprint(self.downinfor_video.keys())

        try:
            for i in range(len(self.audio)):
                for j in range(len(self.audio[i]['backupUrl'])):
                    content_audio = RequestUrl(self.audio[i]['backupUrl'][j], referer=self.url, cookie=self.cookie,
                                               origin=self.origin)
                    if content_audio != 0:
                        total_size = int(content_audio.headers.get('content-length', 0))
                        block_size = 1024
                        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
                        with open('.\\拜年祭\\' + self.name + '.mp3', mode='wb') as f:
                            for data in content_audio.iter_content(block_size):
                                progress_bar.update(len(data))
                                f.write(data)
                        progress_bar.close()
                        break
                else:
                    continue
                break

            for i in range(len(self.downinfor_video[select])):
                for j in range(len(self.downinfor_video[select][i])):
                    #print(self.downinfor_video[select][i][j])
                    content_video = RequestUrl(self.downinfor_video[select][i][j], referer=self.url, cookie=self.cookie,
                                               origin=self.origin)

                    if content_video is not None:
                        total_size = int(content_video.headers.get('content-length', 0))
                        block_size = 1024
                        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
                        with open('.\\拜年祭\\' + self.name + '.mp4', mode='wb') as f:
                            for data in content_video.iter_content(block_size):
                                progress_bar.update(len(data))
                                f.write(data)

                        progress_bar.close()
                        break
                else:
                    continue
                break
            merge_command = f'ffmpeg -loglevel quiet -i .\\拜年祭\\{self.name}.mp4 -i .\\拜年祭\\{self.name}.mp3 -c:v copy -c:a aac -strict experimental .\\拜年祭\\{self.name}output.mp4'
            subprocess.run(merge_command, shell=True)
            time.sleep(2)
            self.Clear_down()
        except Exception as error:
            #print(error)
            print('发生错误')
            return -1

    def Exist(self, Number, flag):
        for i in flag:
            if Number == str(i).replace(' ', ''):
                return 1
        return 0
