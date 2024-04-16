import json
import os
import re
import execjs
import urllib
from urllib.parse import quote
from tqdm import tqdm
from Tool.RequestUrl import RequestUrl


class CommentAPI(object):
    def __init__(self, url, cookie,number=10):
        self.url = url
        self.origin = 'https://www.bilibili.com/'
        self.cookie = cookie
        self.infor = RequestUrl(url, 'https://www.bilibili.com/', self.origin, self.cookie)
        self.CommentAPI = {'data': []}
        oid_match = re.findall('"aid":(.*?),', self.infor.text, re.S)
        self.number = number
        if not oid_match:
            raise ValueError("未找到视频ID")
        self.oid = oid_match[0]
        self.current_dir = os.path.dirname(__file__)


    def request(self, session_id):
        file_path = os.path.join(self.current_dir, 'w_rid.js')
        compile_code = execjs.compile(open(file_path, 'r', encoding='utf-8').read())
        pagination_str = r'{"offset":"{\"type\":1,\"direction\":1,\"session_id\":\"' + str(
            session_id) + r'\",\"data\":{}}"}'
        pagination_str = urllib.parse.quote(pagination_str)
        wts = compile_code.call('wts')
        key = f'mode=3&oid={self.oid}&pagination_str={pagination_str}&plat=1&type=1&web_location=1315875&wts={wts}'
        w_rid = compile_code.call('w_rid', key)
        next_api = f'https://api.bilibili.com/x/v2/reply/wbi/main?oid={self.oid}&type=1&mode=3&pagination_str={pagination_str}&plat=1&web_location=1315875&w_rid={w_rid}&wts={wts}'
        return next_api

    def api(self, content_list):
        tmp = []

        for i in content_list:
            infor = {
                '用户昵称': i['member']['uname'],
                '发布时间': i['reply_control']['time_desc'],
                '内容': i['content']['message'],  # 第一层评论
                '回复': [],

            }

            for j in i['replies']:
                replies = {}
                replies['回复用户昵称'] = j['member']['uname']
                replies['回复发布时间'] = j['reply_control']['time_desc']
                replies['回复内容'] = j['content']['message']  # 回复
                infor['回复'].append(replies)
            tmp.append(infor)
        return tmp

    def get_content(self, next_api):
        response = RequestUrl(next_api, self.url, self.origin, self.cookie)
        if response is None:
            return []
        try:
            content_list = response.json()['data']['replies']
            return self.api(content_list)
        except (KeyError, ValueError) as e:
            print(f"获取评论内容失败: {e}")
            return []

    def get_comments(self):
        file_path = os.path.join(self.current_dir, 'w_rid.js')
        compile_code = execjs.compile(open(file_path, 'r', encoding='utf-8').read())
        wts = compile_code.call('wts')
        pagination_str = urllib.parse.quote('{"offset":""}')
        key = f'mode=3&oid={self.oid}&pagination_str={pagination_str}&plat=1&seek_rpid=&type=1&web_location=1315875&wts={wts}'  # '{"offset":""}'
        ans = compile_code.call('w_rid', key)
        api = f'https://api.bilibili.com/x/v2/reply/wbi/main?oid={self.oid}&type=1&mode=3&pagination_str={pagination_str}&plat=1&seek_rpid=&web_location=1315875&w_rid={ans}&wts={wts}'
        response = RequestUrl(api, self.url, self.origin, self.cookie)
        if response is None:
            return
        try:
            content_list = response.json()['data']['replies']
            session_id = response.json()['data']['cursor']['session_id']
            self.CommentAPI['data'].extend(self.api(content_list))
            next_api = [self.request(session_id) for _ in range(self.number)]
            for i in tqdm(next_api):
                self.CommentAPI['data'].extend(self.get_content(i))
        except (KeyError, ValueError) as e:
            print(f"获取评论失败: {e}")

    def run(self):
        self.get_comments()
        self.write_to_file()
        return self.CommentAPI

    def write_to_file(self):
        if not os.path.exists('.\\Comment'):
            os.mkdir('.\\Comment')
        with open('.\\Comment\\Bcomment.json', 'w', encoding='utf-8') as file:
            json.dump(self.CommentAPI, file, ensure_ascii=False, indent=4)
        print('为您生成了评论区文件(◍˃̶ᗜ˂̶◍)✩')



