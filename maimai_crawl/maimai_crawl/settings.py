# -*- coding: utf-8 -*-

# Scrapy settings for maimai_crawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'maimai_crawl'

SPIDER_MODULES = ['maimai_crawl.spiders']
NEWSPIDER_MODULE = 'maimai_crawl.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 2

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'maimai_crawl.middlewares.MaimaiCrawlSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'maimai_crawl.middlewares.RandomUserAgent': 901,
    # 'maimai_crawl.middlewares.RandomProxy': 902,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'maimai_crawl.pipelines.DBToMongodb': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
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

import logging

# 日志打印开关
LOG_ENABLED = True
LOG_LEVEL = logging.INFO
LOG_FILE = 'spider.log'
# LOG_STDOUT = True

# mongodb数据库配置
MONGO_URI = 'mongodb://192.168.110.51:27017'
MONGO_DB = "xuqiang"
MONGO_CONNECTION = "maimai_info"

# redis配置
