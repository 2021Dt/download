import difflib
from Tool.DowbLoad import DownLoad
from Tool.Cookie import out_cookie
from Tool.Cookie import user_show
from API.CommentAPI import CommentAPI
from API.BaiNianJi import BaiNianJi
from API.DanMuAPI import DanMu


def Judge(url):
    base_url = 'https://www.bilibili.com/'
    # select = ['video', 'festival', 'bnj', 'bangumi']
    similarity = difflib.SequenceMatcher(None, base_url, url).ratio()
    # 如果相似度超过阈值，则尝试进行纠正
    if 0.8 < similarity:
        print(f'网址与基础网址相似度为：{similarity:.2f}')
        if similarity!=1:print('输入网站貌似有误，，正在尝试修正...')
        corrected_url = url.replace(url[0:len(base_url)],base_url)
        tmp = corrected_url
        tag = tmp.replace(base_url,'').split('/')[0]
        cookie = out_cookie('bilibili.txt')
        if cookie is not None:
            if tag == 'video':
                DownLoad(corrected_url,cookie=cookie).run()
            elif tag == 'festival':
                BaiNianJi(corrected_url,cookie=cookie).run()
            elif tag == 'bangumi':
                print('暂时还没写')
        else:
            user_show()
    else:
        print('都说了是B站！૮₍ ˃ ⤙ ˂ ₎ა')
        print('重新开始吧')



def analyse(url):
    sel = input('弹幕爬取： 1\n评论爬取： 2')
    base_url = 'https://www.bilibili.com/'
    similarity = difflib.SequenceMatcher(None, base_url, url).ratio()
    # 如果相似度超过阈值，则尝试进行纠正
    if 0.8 < similarity:
        print(f'网址与基础网址相似度为：{similarity:.2f}')
        if similarity!=1:print('输入网站貌似有误，，正在尝试修正...')
        corrected_url = url.replace(url[0:len(base_url)], base_url)
        cookie = out_cookie('bilibili.txt')
        if cookie is not None:
            if sel == '1':
                DanMu(corrected_url,cookie=cookie).api()
            elif sel == '2':
                CommentAPI(corrected_url,cookie=cookie).run()
        else:
            user_show()
    else:
        print('都说了是B站！૮₍ ˃ ⤙ ˂ ₎ა')
        print('重新开始吧')

def Welcome():
    print('欢迎使用B站数据爬取，当前版本为1.0 ❛‿˂̵✧')
    while True:
        sel = input('选择你要进行的数据爬取\n视音频下载： 1\n弹幕评论爬取： 2 \n')
        if sel.strip() == '1':
            Judge(input('请输入你要分析的网站'))
        elif sel.strip() == '2':
            analyse(input('请输入你要分析的网站'))
        else:
            exit(0)