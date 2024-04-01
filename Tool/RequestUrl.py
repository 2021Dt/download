import time
import requests
import random
import os


LOG_DIR = '.\\log'
cookie = '''buvid3=FB0CB882-9D22-4B22-B84F-B34D5257A9C435692infoc; b_nut=1710053235; i-wanna-go-back=-1; b_ut=7; _uuid=CFE16EF10-A942-210A2-6577-C15985410B29736137infoc; enable_web_push=DISABLE; buvid4=B7B1128A-02A1-D449-AFC3-FE961957C71036241-024031006-lPdNycUBl7NKGeVq2YrRgQ%3D%3D; rpdid=|(u))uRJ|Jkk0J'u~u||lJkRk; DedeUserID=364386712; DedeUserID__ckMd5=91a731121ca04638; header_theme_version=CLOSE; PVID=1; CURRENT_QUALITY=80; fingerprint=09a311839a24769d1626c4e8f73eac9b; buvid_fp_plain=undefined; FEED_LIVE_VERSION=V_HEADER_LIVE_NO_POP; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTIwNjA4NDksImlhdCI6MTcxMTgwMTU4OSwicGx0IjotMX0.e8b8jECevC7J4e0qCDmX4MJ4964gkULTqNHKlu1BKOw; bili_ticket_expires=1712060789; home_feed_column=5; browser_resolution=1844-1059; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; bp_video_offset_364386712=914693820644327462; SESSDATA=3e5b1cf2%2C1727362996%2C3c944%2A31CjA7CV0DOedMGxZbA--wZVsocnFkLRFEMlKMl1MOB_KBwpnbGKh3UVs1IeHtbHa8qTcSVlNjb1E5dlZKMlFLYzRUZ1FNalR4YzhySmt6am5ETExqcmNNQ21xYnNuVVVDVGt2bzVIOG1fMTdsUDlJazZPMUV6UVk3VU5PNmdFTDJwbl9FYjhrcnFBIIEC; bili_jct=955033a1cdb68d777532c9c5c683a655; buvid_fp=09a311839a24769d1626c4e8f73eac9b; b_lsid=DF5D10BFC_18E92A1044E; sid=nlnadpez'''

def RequestUrl(url, referer='', origin='', cookie=''):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'Referer': referer,
        'Cookie': cookie,
        'Origin': origin
    }

    try:
        r = requests.get(url, headers=headers, timeout=2)
        time.sleep(random.uniform(1, 2))

        return r

    except requests.exceptions.Timeout:
        log_error("请求超时", url)
        return None

    except requests.exceptions.RequestException as error:
        log_error(f"请求错误: {error}", url)
        return None

def log_error(error_message, url):
    current_dir = os.path.dirname(__file__)
    log_file = os.path.join(current_dir, 'error.txt')
    with open(log_file, mode='a') as f:
        f.write(f"URL: {url}, 错误信息: {error_message}\n")
