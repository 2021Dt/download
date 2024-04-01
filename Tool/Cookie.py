from pprint import pprint
from API.CommentAPI import CommentAPI
from API.BaiNianJi import BaiNianJi
from API.DanMuAPI import DanMu
from Tool.DowbLoad import DownLoad
import os
import time

def set_cookie(cookie, filename='cookie.txt'):

    try:
        with open(f'cookie/{filename}', 'w') as f:
            f.write(f'Cookie: {cookie}\n')
            f.write(f'Stored Time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
        print('Cookie 已成功存储。')
    except Exception as e:
        print(f'存储 Cookie 出错：{e}')

def out_cookie(filename='cookie.txt', expiration_days=10):
    try:
        cookie_file = f'cookie/{filename}'
        if not os.path.exists(cookie_file):
            print('尚未存储 Cookie，请先执行 set_cookie 函数。')
            return None

        with open(cookie_file, 'r') as f:
            stored_time = None
            for line in f:
                if line.startswith('Stored Time:'):
                    stored_time = line.strip().split(': ')[1]
                    break

            if stored_time:
                stored_time = time.mktime(time.strptime(stored_time, "%Y-%m-%d %H:%M:%S"))
                current_time = time.time()
                if current_time - stored_time > expiration_days * 24 * 3600:
                    print(f'Cookie 已存储超过 {expiration_days} 天，请更新。')
                else:
                    print('Cookie 检查正常。')
            else:
                print('无法读取存储时间。')

        with open(cookie_file, 'r') as f:
            cookie = f.readline().strip().split(': ')[1]
            return cookie
    except Exception as e:
        print(f'读取 Cookie 出错：{e}')
        return None


def user_show(filename='bilibili.txt',expiration_days=10):
    while True:
        cookie = input('请输入您的 Cookie：').strip()
        if cookie:
            set_cookie(cookie, filename)
            break
        else:
            print('Cookie 不能为空，请重新输入。')
    user_cookie = out_cookie(filename, expiration_days)
    if user_cookie:
        print('当前使用的 Cookie 为：', user_cookie)

if __name__ == '__main__':
    #user_show()
    print(out_cookie('bilibili.txt'))





