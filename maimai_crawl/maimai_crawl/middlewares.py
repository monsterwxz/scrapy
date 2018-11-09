# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class MaimaiCrawlSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MaimaiCrawlDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


import random


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('cookie',
                                   '_buuid=0a43ac7a-a998-41fb-826a-c7a645c7d3dd; seid=s1541575813347; guid=GxgYBBgYHwQbGBIEGxkbVhgSHR8TEx9WHBkEHRkfBUNYS0xLeQoaGhsEHRMeGQQaBBMcBU9HRVhCaQoDRUFJT20KT0FDRgoGZmd+YmECChwZBB0ZHwVeQ2FIT31PRlpaawoDHhxSChEeHERDfQoRGgQaGwp+ZApZXUVOREN9AgoaBB8FS0ZGQ1BFZw==; token="juffd7CpFo97fItpdvn1FLInJneWPM9S706+Z0WzJMI8WdG+qAgYf10A1UKSIRAt8CKuzcDfAvoCmBm7+jVysA=="; uid="af1ewkBe5bJpU++2bbvlNvAirs3A3wL6ApgZu/o1crA="; session=eyJ1IjoiMjA2Mzg0NDgzIiwic2VjcmV0Ijoidm5jNC01MV9nVHRXaUFJLXZKcjNqZE9sIiwibWlkNDU2ODc2MCI6ZmFsc2UsIl9leHBpcmUiOjE1NDE2NjI2NDA1MjksIl9tYXhBZ2UiOjg2NDAwMDAwfQ==; session.sig=FH3KgmVpMXSoEwU2se5VT_KZcAo; OUTFOX_SEARCH_USER_ID_NCOO=2087174091.4867668; captcha=793fd949-a562-4d57-bbbb-73cdd4891ad7',
                                   )
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class RandomProxy(object):
    """随机代理ip"""

    def __init__(self, proxy_ip):
        self.proxy_ip = proxy_ip

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('PROXY_POOLS'))

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxy_ip)

