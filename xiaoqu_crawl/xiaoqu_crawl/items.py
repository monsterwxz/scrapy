# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoquCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    xiaoqu_name = scrapy.Field()  # 名称
    city = scrapy.Field()  # 城市
    xiaoqu_addr = scrapy.Field()  # 地址
    lat = scrapy.Field()  # 维度
    lng = scrapy.Field()  # 经度
    property_type = scrapy.Field()  # 物业类型
    property_cost = scrapy.Field()  # 物业费
    complete_time = scrapy.Field()  # 竣工时间
    greening_rate = scrapy.Field()  # 绿化率
    total_houses = scrapy.Field()  # 总户数
    volume_rate = scrapy.Field()  # 容积率
    developers = scrapy.Field()  # 开发商
    management_company = scrapy.Field()  # 物业公司
    xiaoqu_text = scrapy.Field()  # 小区简介
