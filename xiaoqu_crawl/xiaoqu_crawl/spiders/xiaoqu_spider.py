# -*- coding: utf-8 -*-
import scrapy

import re
import logging
from ..items import XiaoquCrawlItem
from ..settings import MYCookie, city_url

logger = logging.getLogger(__name__)


class AuthorSpider(scrapy.Spider):
    name = 'xiaoqu'
    headers = dict()
    headers['User-Agent'] = "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) " \
                            "AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4"
    headers['cookie'] = MYCookie
    start_urls = [i['url'] for i in city_url]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    # '//div[@class="cl-c-list"][3]/ul/li[@class="cl-c-l-li"]'

    def parse(self, response):
        print('#' * 20)
        # print(len(response.xpath('//div[@class="list_filter"]/div/a')))
        href = ''
        for q in response.xpath('//div[@class="list_filter"]/div/a')[1:]:
            try:
                href = q.xpath("./@href").extract_first()
                name = q.xpath("./text()").extract_first()
                # print(name, href)
            except Exception as e:
                logger.error(e)
                logger.error('parse error url:{}'.format(response.url))
            request = scrapy.Request(href, headers=self.headers, callback=self.parse_next_1)
            yield request

    def parse_next_1(self, response):
        mobile_href = ''
        for q in response.xpath('//div[@class="itemsCont"]/div/a'):
            try:
                mobile_href = q.xpath("./@href").extract_first()
                xiaoqu_id = re.findall(r'\d+', q.xpath("./@href").extract_first())[0]
                pc_herf = "https://chongqing.anjuke.com/community/view/{}".format(xiaoqu_id)
                # print(mobile_href)
            except Exception as e:
                logger.error(e)
                logger.error('parse error url:{}'.format(response.url))
            request = scrapy.Request(mobile_href, headers=self.headers, callback=self.pares_xiaoqu_mobile)
            yield request
        next_page = response.xpath('//span[@class="nextPage"]/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, headers=self.headers, callback=self.parse_next_1)

    def pares_xiaoqu_mobile(self, response):
        # print("pares_xiaoqu_pc")
        item = XiaoquCrawlItem()

        xiaoqu_name = re.sub(r'\s', '', response.xpath('//div[@class="comm-tit"]/h1/text()').extract_first())
        xiaoqu_addr = re.sub(r'\s', '', response.xpath('//div[@class="comm-ad"]/p/text()').extract_first()).replace(
            "地址：", "")
        _temp = re.findall(r'\d+\.\d+', response.xpath('//div[@class="comm-ad"]/p/a/@href').extract_first())
        lat = ''
        lng = ''
        if len(_temp) == 2:
            lat = _temp[0]  # 维度
            lng = _temp[1]  # 经度

        property_type = response.xpath('//div[@class="header-field"]/span[1]/text()').extract_first()  # 物业类型
        property_cost = response.xpath('//div[@class="header-field"]/span[2]/text()').extract_first()  # 物业费
        complete_time = response.xpath('//div[@class="header-field"]/span[3]/text()').extract_first()  # 竣工时间
        greening_rate = response.xpath('//div[@class="header-field"]/span[4]/text()').extract_first()  # 绿化率
        total_houses = response.xpath('//div[@class="header-field"]/span[5]/text()').extract_first()  # 总户数
        volume_rate = response.xpath('//div[@class="header-field"]/span[6]/text()').extract_first()  # 容积率
        developers = response.xpath('//dl[@class="comm-other-field"]/dd[1]/text()').extract_first()  # 开发商
        management_company = response.xpath('//dl[@class="comm-other-field"]/dd[2]/text()').extract_first()  # 物业公司
        xiaoqu_text = response.xpath('//div[@class="comm-survey-field"]/p/text()').extract_first()
        city = response.xpath('//div[@class="h-search"]/a/span/text()').extract_first()
        item['xiaoqu_name'] = xiaoqu_name
        item['city'] = city
        item['xiaoqu_addr'] = xiaoqu_addr
        item['lat'] = lat
        item['lng'] = lng
        item['property_type'] = property_type
        item['property_cost'] = property_cost
        item['complete_time'] = complete_time
        item['greening_rate'] = greening_rate
        item['total_houses'] = total_houses
        item['volume_rate'] = volume_rate
        item['developers'] = developers
        item['management_company'] = management_company
        item['xiaoqu_text'] = xiaoqu_text

        yield item
    # def pares_xiaoqu_pc(self, response):
    #     print("pares_xiaoqu_pc")
    #     item = XiaoquCrawlItem()
    #     xiaoqu_name = re.sub(r'\s', '', response.xpath('//div[@class="comm-title"]/h1/text()').extract_first())
    #     xiaoqu_addr = re.sub(r'\s', '', response.xpath('//div[@class="comm-title"]/h1/span/text()').extract_first())
    #     lat = re.findall(r'\d+\.\d+', response.xpath('//div[@class="comm-title"]/a/@href').extract_first())[0]  # 维度
    #     lng = re.findall(r'\d+\.\d+', response.xpath('//div[@class="comm-title"]/a/@href').extract_first())[1]  # 经度
    #     item['xiaoqu_name'] = xiaoqu_name
    #     item['xiaoqu_addr'] = xiaoqu_addr
    #     item['lat'] = lat
    #     item['lng'] = lng
    #     yield item
