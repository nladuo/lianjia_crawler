# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from .proxy_manager import ProxyManager


class UserAgentMiddleware(object):
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def insert_redirect_url(self):
        pass

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy = ProxyManager.get_instance().get_proxy()
        if proxy is not None:
            request.meta['proxy'] = "http://%s:%d" % (proxy["ip"], proxy["port"])
