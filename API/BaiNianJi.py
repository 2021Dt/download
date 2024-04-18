import json
import os
import re
import subprocess
import time
import execjs
from tqdm import tqdm
from Tool.RequestUrl import RequestUrl

class BaiNianJi(object):
    def __init__(self,url,cookie):
        self.url = url
        self.origin = 'https://www.bilibili.com/'
        self.cookie = cookie
        respon =  RequestUrl(url,referer=url,origin=self.origin,cookie=self.cookie)
        information = re.findall(r'<script>window.__INITIAL_STATE__=(.*?)</script>', respon.text, re.S)[0]
        if information == '':
            print('拜年祭解析失败')
            raise ValueError("未找到视频信息")

        information = re.sub(r';\(.*\);', '', information)

        self.infor = json.loads(information)
        self.name = self.infor['videoData']['title']
        self.avid = self.infor['videoData']['aid']
        self.bvid = self.infor['videoData']['bvid']
        self.cid = self.infor['videoData']['cid']
        self.current_dir = os.path.dirname(__file__)

    def api(self):
        file_path = os.path.join(self.current_dir,'w_rid.js')
        compile_code = execjs.compile(open(file_path, 'r', encoding='utf-8').read())
        wts = compile_code.call('wts')
        key = f'avid={self.avid}&bvid={self.bvid}&cid={self.cid}&fnval=4048&fnver=0&fourk=1&from_client=BROWSER&gaia_source=&qn=80&session=&voice_balance=1&web_location=1315873&wts=' + wts
        w_rid = compile_code.call('w_rid', key)
        api = f'https://api.bilibili.com/x/player/wbi/playurl?avid={self.avid}&bvid={self.bvid}&cid={self.cid}&qn=80&fnver=0&fnval=4048&fourk=1&gaia_source=&from_client=BROWSER&session=&voice_balance=1&web_location=1315873&w_rid={w_rid}&wts={wts}'
        return api

    def Clear_down(self):
        os.remove('.\\拜年祭\\' + self.name + '.mp4')
        os.remove('.\\拜年祭\\' + self.name + '.mp3')


    def run(self):
        if not os.path.exists('.\\拜年祭'):
            os.makedirs('.\\拜年祭')
        alldata = RequestUrl(self.api(),referer=self.url,cookie=self.cookie).json()
        alldata = alldata['data']
        accept_description = alldata['accept_description']
        accept_quality = alldata['accept_quality']
        dash = alldata['dash']
        audio = dash['audio']
        video = dash['video']

        downinfor_video = dict(zip(accept_quality, [[] for i in range(len(accept_description))]))

        for i in video:
            downinfor_video[i['id']].append(i['backupUrl'])

        try:
            print('为你查询清晰度相关代码和数据量：')
            ban = []
            for i in range(len(accept_description)):
                if len(downinfor_video[accept_quality[i]]) == 0:
                    ban.append(accept_quality[i])
                print(
                    f'{accept_description[i]}代码: {accept_quality[i]} 数据量：{len(downinfor_video[accept_quality[i]])}')
            while (True):
                select = input('请输入你要下载的清晰度代码').strip(' ')
                if self.Exist(select, accept_quality) == 1 and self.Exist(select, ban) == 0:
                    select = int(select)
                    break
                elif self.Exist(select, ban) == 1:
                    print('数据量为0,请确认你的账号是否为会员账号')
                elif self.Exist(select, accept_quality) == 0:
                    print('请按照正确的清晰度代码进行下载查询')

            print('正在为你查询并下载：')
            for i in range(len(audio)):

                for j in range(len(audio[i]['backupUrl'])):
                    print(audio[i]['backupUrl'][j])
                    content_audio = RequestUrl(audio[i]['backupUrl'][j],referer=self.url,cookie=self.cookie,origin=self.origin)
                    if content_audio != 0:
                        print('查询成功')
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

            for i in range(len(downinfor_video[select])):
                for j in range(len(downinfor_video[select][i])):
                    print(downinfor_video[select][i][j])
                    content_video = RequestUrl(downinfor_video[select][i][j],referer=self.url,cookie=self.cookie,origin=self.origin)

                    if content_video is not  None:
                        print('查询成功')

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
            print('下载完成,正在为你合成文件')
            merge_command = f'ffmpeg -loglevel quiet -i .\\拜年祭\\{self.name}.mp4 -i .\\拜年祭\\{self.name}.mp3 -c:v copy -c:a aac -strict experimental .\\拜年祭\\{self.name}output.mp4'
            subprocess.run(merge_command, shell=True)
            print('音视频合并完成')
            time.sleep(2)
            self.Clear_down()
            print('垃圾清理完毕')
        except Exception as error:
            print(error)
            print('发生错误')

    def Exist(self,Number, flag):
        for i in flag:
            if Number == str(i).replace(' ', ''):
                return 1
        return 0



