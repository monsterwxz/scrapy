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
PROXY_POOLS = ['http://221.204.116.100:8090', 'http://115.46.65.32:8123', 'http://121.31.143.143:8123',
               'http://121.31.160.195:8123', 'http://171.38.199.70:8123', 'http://222.217.68.51:54355',
               'http://111.75.223.9:35918', 'http://58.49.134.202:59095', 'http://113.121.241.229:61234',
               'http://182.88.189.234:8123', 'http://124.193.135.242:54219', 'http://175.168.185.240:8118',
               'http://182.88.167.77:8123', 'http://171.38.38.173:8123', 'http://171.38.90.234:8123',
               'http://115.46.71.231:8123', 'http://117.85.86.146:53128', 'http://115.46.67.176:8123',
               'http://42.176.36.251:37000', 'http://171.37.154.100:8123', 'http://175.155.24.51:808',
               'http://113.59.59.73:35683', 'http://180.175.136.195:54584', 'http://111.72.155.86:53128',
               'http://116.30.221.18:53471', 'http://182.88.128.221:8123', 'http://171.37.155.78:8123',
               'http://175.148.68.185:1133', 'http://110.73.1.22:8123', 'http://115.46.70.204:8123',
               'http://121.31.137.232:8123', 'http://118.190.149.36:8080', 'http://182.88.191.114:8123',
               'http://171.37.154.157:8123', 'http://60.177.227.49:18118', 'http://180.76.136.77:9999',
               'http://111.200.71.129:8123', 'http://171.38.85.122:8123', 'http://171.38.79.186:8123',
               'http://218.79.86.236:54166', 'http://182.88.189.42:8123', 'https://61.189.242.243:55484',
               'http://121.31.153.26:8123', 'http://114.225.168.21:53128', 'http://114.99.8.6:808',
               'http://115.46.65.224:8123', 'http://114.225.171.19:53128', 'http://182.88.15.228:8123',
               'http://110.73.9.136:8123', 'http://115.46.71.246:8123', 'http://115.46.118.187:8123',
               'http://171.38.86.145:8123', 'http://110.73.0.237:8123', 'http://182.88.215.177:8123',
               'http://171.38.34.242:8123', 'http://182.88.213.153:8123', 'http://218.22.102.107:80',
               'http://121.23.225.56:8118', 'https://114.215.149.170:8118', 'http://182.88.164.180:8123',
               'http://171.38.64.9:8123', 'http://182.88.178.174:8123', 'http://115.46.79.161:8123',
               'http://115.46.67.68:8123', 'http://183.16.28.8:8123', 'http://110.179.64.12:8123',
               'http://58.48.168.166:51430', 'http://171.37.167.150:8123', 'http://115.46.76.44:8123']


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
        # 判断是否已经访问
        if redis_db.get(url) is None:
            try:
                response = requests.get(url,
                                        # proxies={'http': get_proxy()},
                                        proxies={'https': 'https://221.229.252.98:9797'},
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
                print(e, url)
                print('重新加入队列')
                redis_db.lpush(redis_list_name, url)

    mongo_db.close()


if __name__ == "__main__":
    start(
        'https://maimai.cn/contact/interest_contact/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1IjoxMTk4MjA4NDAsImxldmVsIjoyLCJ0IjoiY3R0In0.fnz6vNCb63n2j-Frr6H_vu1LuG1jgfoq2oPOITSAJdA')
