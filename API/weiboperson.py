from tqdm import tqdm
from Tool.RequestUrl import RequestUrl
from pprint import pprint
from lxml import etree
from threading import Thread
from queue import Queue
from datetime import datetime


class WeiboPerson(object):
    def __init__(self, url, number=10, cookie=''):

        '''纯随机抓取，非热榜页面'''

        self.referer = 'https://weibo.com/'
        self.cookie = cookie
        self.url = url
        self.qurl = Queue()
        self.thread_num = number  # 多线程处理数量

    def get_info(self):
        '''整合'''
        info = []
        list_data = self.allGroups_api()[0]

        list_api = RequestUrl(self.list_id_api(list_data['gid']), cookie=self.cookie, referer=self.referer).json()

        for a in tqdm(self.clear_list_api(list_api)):

            #print(a)
            first_comment = RequestUrl(self.comment_api(a['id'], a['user']['id']), cookie=self.cookie, referer=self.referer).json()
            first_data = self.clear_comment_api(first_comment)
            c = RequestUrl(self.next_comment_api(a['id'],first_data['max_id'],a['user']['id']), cookie=self.cookie, referer=self.referer).json()
            next_data = self.clear_comment_api(c)
            info.append({
                'main':a,
                'reply': first_data['comment'] + next_data['comment']
            })
        return info
        # pprint(list_api)

    def clear_list_api(self, info):
        data = []
        for i in info['statuses']:
            # pprint(i)
            data.append({
                'time': datetime.strptime(i['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime(
                    "%Y-%m-%d %H:%M:%S"),
                'user': {
                    'id': i['user']['id'],
                    'name': i['user']['screen_name'],

                },
                'id': i['id'],
                'text': i['text_raw'].replace('\n', '').replace('\u200b', '')
            })
        return data

    def clear_comment_api(self, info):
        data = {'max_id': info['max_id'], 'comment': []}

        for i in info['data']:
            for j in i['comments']:
                data['comment'].append({
                    'time': datetime.strptime(j['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime(
                        "%Y-%m-%d %H:%M:%S"),
                    'id': j['id'],
                    'gid': j['gid'],
                    'source': j['source'],
                    'reply_comment': {
                        'reply_text': j['reply_comment']['text'],
                        'reply_user': {
                            'id': j['reply_comment']['user']['id'],
                            'location': j['reply_comment']['user']['location'],
                            'name': j['reply_comment']['user']['screen_name']
                        }
                    },
                    'text': j['text_raw'].replace('\n', ''),
                    'user': {
                        'description': j['user']['description'],
                        'name': j['user']['screen_name']
                    }
                })
        #pprint(data)
        return data

    def allGroups_api(self):
        """
        获取list_id
        这个里面可以获取全部的类型的list_id
        可以单独运行查看
        """
        allGroups = 'https://weibo.com/ajax/feed/allGroups?is_new_segment=1&fetch_hot=1'
        list_id = RequestUrl(allGroups, referer=self.referer, cookie=self.cookie).json()
        data = []
        for i in list_id['groups']:
            for j in i['group']:
                data.append({
                    'gid': j['gid'],
                    'title': j['title'],
                    'uid': j['uid']
                })
        return data

    def list_id_api(self, list_id):
        '''获取id'''
        api = f'https://weibo.com/ajax/feed/unreadfriendstimeline?list_id={list_id}&refresh=4&since_id=0&count=15'
        return api

    def comment_api(self, comment_id, uid):
        api = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={comment_id}&is_show_bulletin=2&is_mix=0&count=20&type=feed&uid={uid}&fetch_level=0&locale=zh-CN'
        return api

    def next_comment_api(self, comment_id, max_id, uid):
        api = f'https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={comment_id}&is_show_bulletin=2&is_mix=0&max_id={max_id}&count=20&uid={uid}&fetch_level=0&locale=zh-CN'
        return api

