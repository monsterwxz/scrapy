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

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
]
PROXY_POOLS = ['https://113.200.56.13:8010', 'https://114.91.164.97:9999', 'https://221.6.201.18:9999',
               'https://202.112.237.102:3128', 'https://140.143.96.216:80', 'https://122.227.62.66:55816']


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

    def process_item(self, item):
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


def get_proxy():
    return random.choice(PROXY_POOLS)


def get_agent():
    return random.choice(USER_AGENTS)


def start(url):
    """
    :param url:
    :return:
    """
    mongo_db = DBToMongodb('mongodb://192.168.110.51:27017', "xuqiang", "maimai_info")
    redis_db = StrictRedisCluster(startup_nodes=[{"host": "192.168.108.181", "port": "6379"}], decode_responses=True)
    redis_list_name = 'maimai_list'
    redis_db.lpush(redis_list_name, url)
    item = {}
    while True:
        # time.sleep(0.2)
        print(datetime.datetime.now(), '当前队列长度', redis_db.llen(redis_list_name))
        if redis_db.llen(redis_list_name) == 0:
            break
        url = redis_db.rpop(redis_list_name)
        proxy = {'https': get_proxy()}
        # 判断是否已经访问
        if redis_db.get(url) is None:
            try:
                response = requests.get(url,
                                        proxies=proxy,
                                        # proxies={'https': PROXY_POOLS[1]},
                                        headers={'User-Agent': get_agent()}, timeout=5)
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
                    if redis_db.get(_url) is None:
                        # 存放获取到的新的url
                        redis_db.lpush(redis_list_name, _url)
                    # 判断该条数据是否存入数据库
                    if redis_db.get(item["encode_mmid"]) is None:
                        mongo_db.process_item(item)
                        # 标记该条数据已经存入数据库
                        redis_db.set(item["encode_mmid"], 1)
                # 标记当前url已经访问
                redis_db.set(url, 1)
            except Exception as e:
                print(proxy)
                print(e, url)
                print('重新加入队列')
                redis_db.lpush(redis_list_name, url)

    mongo_db.close()


if __name__ == "__main__":
    start(
        'https://maimai.cn/contact/interest_contact/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1IjoxMTk4MjA4NDAsImxldmVsIjoyLCJ0IjoiY3R0In0.fnz6vNCb63n2j-Frr6H_vu1LuG1jgfoq2oPOITSAJdA')
