import os
import re
import execjs
from Tool.RequestUrl import RequestUrl

class DanMu(object):
    def __init__(self,url,cookie):
        self.url = url
        self.origin = 'https://www.bilibili.com/'
        self.cookie = cookie
        self.infor = RequestUrl(url, 'https://www.bilibili.com/', self.origin, self.cookie)
        self.current_dir = os.path.dirname(__file__)
    def api(self):
        if self.infor is None:
            raise ValueError("请求体为空")
        cidMap = re.findall('"cidMap":{.*?}', self.infor.text, re.S)[0]
        aid_cid = re.search(r'"aid":(?P<aid>.*?),.*,"cids":{"1":(?P<cids>.*?)}', cidMap)
        oid = aid_cid.group('cids')
        pid = aid_cid.group('aid')
        file_path = os.path.join(self.current_dir, 'w_rid.js')
        compile_code = execjs.compile(open(file_path, 'r', encoding='utf-8').read())
        wts = compile_code.call('wts')
        key = f'oid={oid}&pe=120000&pid={pid}&ps=0&pull_mode=1&segment_index=1&type=1&web_location=1315873&wts={wts}'
        w_rid = compile_code.call('w_rid', key)

        Dm_api = f"https://api.bilibili.com/x/v2/dm/wbi/web/seg.so?type=1&oid={oid}&pid={pid}&segment_index=1&pull_mode=1&ps=0&pe=120000&web_location=1315873&w_rid={w_rid}&wts={wts}"
        print('目前暂不提供弹幕文件的逆向解析，只提供静态api')
        return Dm_api







