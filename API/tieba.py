from Tool.RequestUrl import RequestUrl
from pprint import pprint
import re
from lxml import etree
from datetime import datetime, timedelta



class Theme(object):
    def __init__(self, url):
        self.url = url
        self.referer = 'https://tieba.baidu.com/'
        self.info = RequestUrl(url, referer=self.referer)
        self.header_data = {}
        self.page_data = []
        self.get_html()

    def get_html(self):
        title = re.findall(r'<title>(.*?)</title>', self.info.text, re.S)[0]
        card_numLabel = re.findall(r'<span class="card_menNum">(.*?)</span>', self.info.text, re.S)[0]
        card_infoNum = re.findall(r'<span class="card_infoNum">(.*?)</span>', self.info.text, re.S)[0]
        content = re.findall(r'<meta name="description" content="(.*?)">', self.info.text, re.S)[0]
        red = re.findall(r'<span class="red_text">(\d+)</span>', self.info.text, re.S)

        self.header_data = {
            'title': title,
            'card_numLabel(关注)': card_numLabel,  # 关注数
            'card_infoNum(帖子)': card_infoNum,  # 帖子数
            'content': content,  # 本吧热帖
            'red_text': red[0],  # 主题帖子数
        }

    def get_page(self, url):
        """当前页面的所以文章"""

        info = RequestUrl(url, referer=self.referer)
        page_url = [self.referer + i for i in re.findall(r'a rel="noopener" href="/(p/\d+)"', info.text, re.S)]
        page_title = re.findall(r'a rel="noopener" href="/p/\d+" title="(.*?)"', info.text, re.S)
        return dict(zip(page_url, page_title))

    def pn(self):
        """获取本吧内所有主页面"""
        pn = int(self.header_data['red_text'])
        url = []
        if pn % 50 != 0:
            pn = pn - pn % 50 + 50

        for i in range(50, pn, 50):
            url.append(self.url + f'&ie=utf-8&pn={i}')

        return url

    def get_info(self, url,part=1):
        """处理文章页面：
            -- 获取页面全部楼主评论
                -- 包含楼主评论，IP，时间
            -- 楼主回复
                -- 包含时间，姓名，内容，id
        """

        info = RequestUrl(url, referer=self.url)
        html = etree.HTML(info.text)

        max_pn = html.xpath('//*[@id="thread_theme_7"]/div[1]/ul/li[2]/span[2]/text()')[0]
        max_pn = int(max_pn)/2

        pn_data = []

        for pn in range(1,int((max_pn+0.5+1)*part)):

            pn_url = url + f'?pn={pn}'

            info = RequestUrl(pn_url, referer=self.url)
            html = etree.HTML(info.text)

            d_author = re.findall(r'<ul class="p_author">.*?</ul>', info.text, re.S)
            user_id_patten = re.compile('user_id&quot;:(?P<user_id>\d+)')
            user_name = re.compile('<a data-field.*>(?P<user_name>.*)</a>')
            d_post_content = re.findall(r'<div id="post_content_(\d+)', info.text, re.S)

            information = self.clear_info(html.xpath('//*[@id="j_p_postlist"]//div/div[2]//div/div[1]/div//span/text()'))

            data = []

            reply = self.content(info.text, pn).json()['data']['comment_list']

            reply_key = []

            if len(reply) != 0:
                reply_key = reply.keys()

            for i, j, k in zip(d_author, d_post_content, information):
                user_replay = []
                if j in reply_key:
                    for m in reply[j]['comment_info']:

                        tmp = {
                                'now_time':datetime.fromtimestamp(m['now_time']).strftime("%Y-%m-%d %H:%M:%S"),
                                'comment_id': m['comment_id'],
                                'content': re.sub(r'<.*?>','',m['content'],re.S),
                                'post_id': m['post_id'],
                                'show_nickname': m['show_nickname'],
                                'thread_id': m['thread_id'],
                                'user_id': m['user_id'],
                                'username': m['username']
                            }
                        user_replay.append(tmp)
                else:
                    user_replay = ['当前无评论']

                data.append({
                    'user_id': user_id_patten.search(i).group('user_id'),
                    'user_name': user_name.search(i).group('user_name').strip() if user_name.search(
                        i).group('user_name') else 'error: 用户名字含有图片等非法信息',
                    'main_content': [k.strip() for k in html.xpath(f'//*[@id="post_content_{j}"]/text()')],
                    'information': k,
                    'reply': user_replay
                })
            # pprint({
            #     'pn':pn,
            #     'data':data
            # })
            pn_data.append({
                'pn':pn,
                'data':data
            })


        return pn_data

    def clear_info(self, data: list):
        flag = 0
        tmp = {
            'ip': '',
            'time': '',
            'floor': ''
        }
        infor = []
        for i in data:
            if flag == 3:
                infor.append(tmp)
                tmp = {
                    'ip': '',
                    'time': '',
                    'floor': ''
                }
                flag = 0

            if 'IP' in i:
                tmp['ip'] = i
                flag += 1
            elif '楼' in i:
                tmp['floor'] = i
                flag += 1
            elif '-' in i and ':' in i:
                tmp['time'] = i
                flag += 1
        return infor

    def t(self):
        timestamp = int(datetime.now().timestamp()) * 1000
        current_time = datetime.now()

        # 计算时间差
        delta = timedelta(seconds=2592)  # 2592 秒 = 72 小时
        new_time = current_time - delta

        # 将结果转换为时间戳（秒级）
        timestamp = int(new_time.timestamp())

        return timestamp

    def content(self, info, pn):
        fid = re.search("fid:'(\d+)'", info).group(1)
        tid = re.search("tid:'(\d+)'", info).group(1)
        api = f'https://tieba.baidu.com/p/totalComment?t={self.t()}&tid={tid}&fid={fid}&pn={pn}&see_lz=0'
        return RequestUrl(api,self.url)
