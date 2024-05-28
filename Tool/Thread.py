from threading import Thread
from queue import Queue

class Spider():
    def __init__(self,number=10):
        self.qurl = Queue()
        self.thread_num = number  # 多线程处理数量

    def produce_url(self,page):
        for url in page:#你要多线程处理的url列表:
            self.qurl.put(url) # 生成URL存入队列，等待其他线程提取

    def get_info(self):
        while not self.qurl.empty(): # 保证url遍历结束后能退出线程
            url = self.qurl.get() # 从队列中获取URL
            print(f'{url} ing')


            #具体多线程处理函数(url)  #这个就是你要多线程处理的主体了

    def run(self):
        self.produce_url()
        for _ in range(self.thread_num):
            th = Thread(target=self.get_info)
            th.start()
        print('finished.')


