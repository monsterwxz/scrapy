# coding:utf-8

import requests
import queue
import random
import json
import logging
import pymongo
import datetime
import time
from rediscluster import StrictRedisCluster
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
]
PROXY_POOLS = ['https://113.200.56.13:8010', 'https://114.116.10.21:3128', 'https://119.27.177.169:80',
               'https://140.143.96.216:80']


class Proxies(object):
    """docstring for Proxies"""

    def __init__(self, page=3):
        self.proxies = []
        self.verify_pro = []
        self.page = page
        self.headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }

        self.get_proxies_wn()
        self.verify_proxies()

    def get_proxy_list(self):
        return self.proxies

    def get_proxies_wn(self):
        page = 1
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/wn/%d' % page
            html = requests.get(url, headers={'User-Agent': random.choice(USER_AGENTS)}).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower() + '://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def verify_proxies(self):
        # 没验证的代理
        old_queue = Queue()
        # 验证后的代理
        new_queue = Queue()
        print('验证代理........')
        works = []
        for _ in range(15):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue, new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = []
        while 1:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print('验证代理结束!')

    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0: break
            # protocol = 'https' if 'https' in proxy else 'http'
            proxies = {'https': proxy}
            try:
                rc = requests.get(
                    'https://maimai.cn/contact/interest_contact/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1IjoxMTk4MjA4NDAsImxldmVsIjoyLCJ0IjoiY3R0In0.fnz6vNCb63n2j-Frr6H_vu1LuG1jgfoq2oPOITSAJdA',
                    proxies=proxies,
                    headers={'User-Agent': random.choice(USER_AGENTS)},
                    timeout=3)
                ss = json.loads(rc.text)
                if isinstance(ss, list):
                    # print('success %s' % proxy)
                    new_queue.put(proxy)
            except:
                pass
                # print('fail %s' % proxy)


class DBToMongodb(object):
    """
        将数据存入mongodb数据库
        """

    def __init__(self, mongo_uri, mongo_db, dbc):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        print('连接数据库')
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.con = self.db[dbc]
        self.start_time = datetime.datetime.now()
        self.end_time = None

    def insert_item(self, item):
        try:
            self.con.insert_one(dict(item))
        except Exception as e:
            print(e)
        return item

    def close(self):
        self.end_time = datetime.datetime.now()
        print('花费时间:{}s'.format((self.end_time - self.start_time).seconds))
        print('关闭数据库')
        print('结束标识！')
        self.client.close()


class Spider(object):
    def __init__(self, first_url):
        self.start_url = first_url
        self.mongo_db = DBToMongodb('mongodb://192.168.110.51:27017', "xuqiang", "maimai_info")
        self.redis_db = StrictRedisCluster(startup_nodes=[{"host": "192.168.108.181", "port": "6379"}],
                                           decode_responses=True)
        self.redis_url_list_name = 'maimai_list'
        self.proxy_list = []
        # 代理ip出错记录
        self.proxy_err = {}

    def get_proxy(self):
        if len(self.proxy_list) == 0:
            print('代理ip为空，重新获取代理ip')
            self.proxy_err = {}
            p = Proxies()
            self.proxy_list = p.get_proxy_list()
            print('得到{}个'.format(len(self.proxy_list)))
            print(self.proxy_list)
        return random.choice(self.proxy_list)

    def get_agent(self):
        return random.choice(USER_AGENTS)

    def judge_proxy(self, proxy):

        if self.proxy_err.get(proxy) is None:
            self.proxy_err[proxy] = 0
        self.proxy_err[proxy] += 1
        # 代理ip出错3次，删除
        if self.proxy_err.get(proxy) >= 3:
            print('删除代理：', proxy)
            self.proxy_list.remove(proxy)
        print('当前代理池剩余{}个'.format(len(self.proxy_list)))

    def start(self):
        """
        :param url:
        :return:
        """
        self.redis_db.lpush(self.redis_url_list_name, self.start_url)
        item = {}
        while True:
            # time.sleep(0.2)
            print(datetime.datetime.now(), '当前队列长度', self.redis_db.llen(self.redis_url_list_name))
            if self.redis_db.llen(self.redis_url_list_name) == 0:
                break
            url = self.redis_db.rpop(self.redis_url_list_name)
            proxy = self.get_proxy()
            # 判断是否已经访问
            if self.redis_db.get(url) is None:
                try:
                    response = requests.get(url,
                                            proxies={'https': proxy},
                                            # proxies={'https': PROXY_POOLS[1]},
                                            headers={'User-Agent': self.get_agent()}, timeout=5)
                    datalist = json.loads(response.text)
                    print('分析数组内数据')
                    for i in datalist:
                        info = i.get("card")
                        item["name"] = info.get("name")
                        item["avatar"] = info.get("avatar")
                        item["company"] = info.get("company")
                        item["career"] = info.get("career")
                        item["position"] = info.get("position")
                        item["encode_mmid"] = info.get("encode_mmid")
                        item["province"] = info.get("province")
                        item["city"] = info.get("city")
                        item["tag"] = info.get("line4")
                        _url = "https://maimai.cn/contact/interest_contact/" + item["encode_mmid"]
                        # 判断是否已经访问
                        if self.redis_db.get(_url) is None:
                            # 存放获取到的新的url
                            self.redis_db.lpush(self.redis_url_list_name, _url)
                        # 判断该条数据是否存入数据库
                        if self.redis_db.get(item["encode_mmid"]) is None:
                            self.mongo_db.insert_item(item)
                            # 标记该条数据已经存入数据库
                            self.redis_db.set(item["encode_mmid"], 1)
                    # 标记当前url已经访问
                    self.redis_db.set(url, 1)
                except Exception as e:
                    self.judge_proxy(proxy)
                    print(e, url)
                    print('重新加入队列')
                    self.redis_db.lpush(self.redis_url_list_name, url)

        self.mongo_db.close()


if __name__ == "__main__":
    s = Spider(
        'https://maimai.cn/contact/interest_contact/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1IjoxMTk4MjA4NDAsImxldmVsIjoyLCJ0IjoiY3R0In0.fnz6vNCb63n2j-Frr6H_vu1LuG1jgfoq2oPOITSAJdA')
    s.start()
