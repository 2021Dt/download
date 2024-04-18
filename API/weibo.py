import json
import os
import re
from datetime import datetime
from tqdm import tqdm
from Tool.RequestUrl import RequestUrl
from pprint import pprint
from lxml import etree
from threading import Thread
from queue import Queue


class Weibo(object):
    def __init__(self, url, number=10, cookie=''):
        self.referer = 'https://weibo.com/'
        self.cookie = cookie
        self.url = url
        self.qurl = Queue()
        self.thread_num = number  # 多线程处理数量

    def get_info(self,page=''):
        """获取主页面内容"""
        global url
        if page!='':
            url = self.url + f'&page={page}'
        html = etree.HTML(RequestUrl(url, referer=self.referer, cookie=self.cookie).text)
        part = html.xpath('//*[@id="pl_feedlist_index"]/div[4]//div[@class="card-wrap"]')
        data = []

        for i in part:
            nick_name = i.xpath('./div/div[1]/div[2]/div[1]/div[2]/a/@nick-name')
            id_link = i.xpath('./div/div[1]/div[2]/div[1]/div[2]/a/@href')
            time = i.xpath('./div/div[1]/div[2]/div[2]/a[1]/text()')
            content = i.xpath('./div/div[1]/div[2]//p/text()')
            mid = i.xpath('@mid')

            infor = {
                'nick_name': nick_name[0].strip(),
                'time': time[0].strip(),
                'nick_name_id_link': 'https:' + id_link[0].strip(),
                'content': [i.strip().replace('【', '').replace('\u200b', '').replace('】', '') for i in content[1:] if
                            i.strip() != ''],
                'mid': mid[0].strip(),
                'user_id': re.search(r'/(?P<id>\d+)', id_link[0], re.S).group('id'),
                'reply': []
            }

            data.append(infor)
            # print(etree.tostring(i,encoding = "utf-8").decode('utf-8'))
        return data

    def clear_info(self, info: dict):
        """从页面数据清洗提取"""

        data = []
        for i in info['data']:
            user = {
                'rootid': i['rootid'],
                'source': i['source'],
                'text_raw': i['text_raw'],
                'screen_name': i['user']['screen_name'],
                # 'total_number': i['total_number'],
                'created_at': datetime.strptime(i['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime(
                    "%Y-%m-%d %H:%M:%S")

            }
            data.append(user)
        return data

    def getBuildComments(self,page=''):
        """构建json文件"""

        data = self.get_info(page)
        threads = []

        for i in data:
            self.qurl.put(i)

        for _ in range(self.thread_num):
            th = Thread(target=self.produce)
            th.start()
            threads.append(th)

        # Join all threads
        for th in threads:
            th.join()

        #pprint(data)
        return {'data': data}

    def produce(self):
        while not self.qurl.empty():  # 保证url遍历结束后能退出线程
            i = self.qurl.get()  # 从队列中获取URL
            result = self.quick(i)
            self.write_to_file(result)

    def quick(self, i):
        resp = RequestUrl(self.buildApi(i['mid'], i['user_id']), referer=self.url, cookie=self.cookie).json()
        i['total_number'] = resp['total_number']
        reply = self.clear_info(resp)

        for j in tqdm(reply, desc=f"Processing {i['nick_name']}"):
            next_resp = RequestUrl(self.buildApi(j['rootid'], i['user_id'], max_id='0'), referer=self.url,
                                   cookie=self.cookie).json()
            j['total_number'] = next_resp['total_number']
            j['reply'] = self.clear_info(next_resp)
            max_id = next_resp['max_id']

            for k in range(20, int(j['total_number']), 20):
                next_resp2 = RequestUrl(self.buildApi(j['rootid'], i['user_id'], max_id=max_id, is_mix=1),
                                        referer=self.url,
                                        cookie=self.cookie).json()
                max_id = next_resp2['max_id']
                if len(self.clear_info(next_resp2)) > 0:
                    j['reply'].append(self.clear_info(next_resp2))

        i['reply'] = reply
        return i

    def buildApi(self, mid, user_id, is_mix=0, count=20, max_id=''):
        api = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count={count}&uid={user_id}&fetch_level=0&locale=zh-CN'

        next_api = f'https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&max_id={max_id}&count={count}&uid={user_id}&fetch_level=0&locale=zh-CN'

        reply_next_api = f'https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={mid}&is_show_bulletin=2&is_mix={is_mix}&fetch_level=1&max_id={max_id}&count=20&uid={user_id}&locale=zh-CN'

        reply_api = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={mid}&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id={max_id}&count=20&uid={user_id}&locale=zh-CN'

        if max_id == '0':
            return reply_api
        elif max_id != '' and is_mix == 0:
            return next_api
        elif max_id != '' and is_mix == 1:
            return reply_next_api
        elif max_id == '':
            return api

    def write_to_file(self, data):
        if not os.path.exists('.\\Comment'):
            os.mkdir('.\\Comment')
        with open(f'.\\Comment\\WeiBoComment_{data["mid"]}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f'为 {data["nick_name"]} 生成了评论区文件(◍˃̶ᗜ˂̶◍)✩')
