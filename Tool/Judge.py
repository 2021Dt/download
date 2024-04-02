import difflib
from Tool.DowbLoad import DownLoad
from Tool.Cookie import out_cookie
from Tool.Cookie import user_show
from API.CommentAPI import CommentAPI
from API.BaiNianJi import BaiNianJi
from API.DanMuAPI import DanMu


def Judge(url, cookie):
    base_url = 'https://www.bilibili.com/'
    # select = ['video', 'festival', 'bnj', 'bangumi']
    similarity = difflib.SequenceMatcher(None, base_url, url[0:len(base_url)]).ratio()
    # 如果相似度超过阈值，则尝试进行纠正
    if 0.8 < similarity:
        print(f'网址与基础网址相似度为：{similarity:.2f}')
        if similarity != 1:
            print('输入网站貌似有误，，正在尝试修正...')
        corrected_url = url.replace(url[0:len(base_url)], base_url)
        tmp = corrected_url
        tag = tmp.replace(base_url, '').split('/')[0]
        if tag == 'video':
            DownLoad(corrected_url, cookie=cookie).run()
        elif tag == 'festival':
            BaiNianJi(corrected_url, cookie=cookie).run()
        elif tag == 'bangumi':
            print('暂时还没写')
    else:
        print('都说了是B站！૮₍ ˃ ⤙ ˂ ₎ა')
        print('重新开始吧')


def analyse(url, cookie):
    base_url = 'https://www.bilibili.com/'
    similarity = difflib.SequenceMatcher(None, base_url, url[0:len(base_url)]).ratio()
    # 如果相似度超过阈值，则尝试进行纠正
    if 0.8 < similarity:
        print(f'网址与基础网址相似度为：{similarity:.2f}')
        if similarity != 1:
            print('输入网站貌似有误，，正在尝试修正...')
        corrected_url = url.replace(url[0:len(base_url)], base_url)
        sel = input('弹幕爬取： 4\n评论爬取： 5 \n')
        if sel == '4':
            print('正在上成弹幕api')
            DanMu(corrected_url, cookie=cookie).api()
        elif sel == '5':
            print('评论爬取ing')
            a = CommentAPI(corrected_url, cookie=cookie).run()
            return a
    else:
        print("\033[H\033[J")
        print('都说了是B站！૮₍ ˃ ⤙ ˂ ₎ა')
        print('重新开始吧')


def Welcome():
    print('欢迎使用B站数据爬取，当前版本为1.0 ❛‿˂̵✧')
    print('按下任意键退出....')
    cookie = out_cookie('bilibili.txt')
    base_url = 'https://www.bilibili.com/'
    if cookie is None:
        user_show()
    url = input('请输入你要分析的网站\n')
    while True:
        if len(url) < len(base_url):
            print('都说了是B站！૮₍ ˃ ⤙ ˂ ₎ა')
            url = input('请重新输入你要分析的网站\n')
            continue
        sel = input('选择你要进行的数据爬取\n视音频下载： 1\n弹幕评论爬取： 2 \n回退至网站选择： 3 \n')
        if sel.strip() == '1':
            Judge(url, cookie)
        elif sel.strip() == '2':
            analyse(url, cookie)
        elif sel.strip() == '3':
            url = input('请重新输入你要分析的网站\n')
            while len(url) < len(base_url):
                print('都说了是B站！૮₍ ˃ ⤙ ˂ ₎ა')
                url = input('请重新输入你要分析的网站\n')
            continue
        else:
            exit(0)
