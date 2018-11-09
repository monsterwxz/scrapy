# -*- coding: utf-8 -*-
import scrapy
from ..items import MaimaiCrawlItem
import json
import logging

logger = logging.getLogger(__name__)
from rediscluster import StrictRedisCluster

redis_db = StrictRedisCluster(startup_nodes=[{"host": "192.168.108.182", "port": "6379"}], decode_responses=True)


class MaiMaiSpider(scrapy.Spider):
    name = 'maimai'
    url = [
        'https://maimai.cn/contact/interest_contact/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1IjoxMTk4MjA4NDAsImxldmVsIjoyLCJ0IjoiY3R0In0.fnz6vNCb63n2j-Frr6H_vu1LuG1jgfoq2oPOITSAJdA']
    start_urls = url

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        try:
            datalist = json.loads(response.text)
            for i in datalist:
                item = MaimaiCrawlItem()
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

                if redis_db.get(item["encode_mmid"]) is None:
                    redis_db.set(item["encode_mmid"], 1)
                    yield item
                    url = "https://maimai.cn/contact/interest_contact/" + item["encode_mmid"]
                    logger.warning(url)
                    yield scrapy.Request(url, callback=self.parse)
        except Exception as e:
            logger.error(e, exc_info=1)
            logger.error(response.url)
            logger.error(response.text)
        # next_page = response.css('.dw_page ul li')[-1].css('a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
