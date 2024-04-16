from lxml import etree
from pprint import pprint
from Tool.RequestUrl import RequestUrl

class HotWeibo(object):
    def __init__(self, cookie=''):
        self.referer = 'https://s.weibo.com/'
        self.cookie = cookie

    def get_hot_weibo(self,index):
        """
        index:
            0 : 热搜榜
            1 : 要闻榜
            2 : 文娱榜
            3 : 体育榜
            4 : 游戏榜
            5 : 好友榜
        """
        base_url = 'https://s.weibo.com/top/summary?cate='
        url = ['realtimehot','socialevent','entrank','sport','game','friends']
        html = etree.HTML(RequestUrl(base_url+url[index],cookie=self.cookie,referer=self.referer).text)
        hot_weibo_url = html.xpath('//*[@id="pl_top_realtimehot"]/table/tbody//tr/td[2]/a/@href')
        hot_weibo_title = html.xpath('//*[@id="pl_top_realtimehot"]/table/tbody//tr/td[2]/a/text()')
        data = []
        flag = 0
        for i, j in zip(hot_weibo_url, hot_weibo_title):
            data.append({
                j : 'https://s.weibo.com/' + i,
                'ranking' : flag,
            })
            flag += 1
        return data
