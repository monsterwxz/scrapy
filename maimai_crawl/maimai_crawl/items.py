# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaimaiCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    avatar = scrapy.Field()
    company = scrapy.Field()
    career = scrapy.Field()
    position = scrapy.Field()
    encode_mmid = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    tag = scrapy.Field()
