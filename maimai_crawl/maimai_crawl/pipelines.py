# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import datetime
from .settings import MONGO_CONNECTION

logger = logging.getLogger(__name__)


class MaimaiCrawlPipeline(object):
    def process_item(self, item, spider):
        return item


class DBToMongodb(object):
    """
        将数据存入mongodb数据库
        """

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        logger.info('连接数据库')
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.con = self.db[MONGO_CONNECTION]
        self.start_time = datetime.datetime.now()
        self.end_time = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        logger.warning('开始标识！')

    def close_spider(self, spider):
        self.end_time = datetime.datetime.now()
        logger.warning('花费时间:{}s'.format((self.end_time - self.start_time).seconds))
        logger.info('关闭数据库')
        logger.warning('结束标识！')
        self.client.close()

    def process_item(self, item, spider):
        try:
            self.con.insert_one(dict(item))
        except Exception as e:
            logger.error(e)
        return item
