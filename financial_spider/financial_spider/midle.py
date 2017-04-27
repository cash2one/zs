#-*-coding:utf-8-*-
import random
import base64
import json
from . import settings
import redis
import financial_spider.Environmental_parameters as Environmental_parameters
import requests
import logging
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import sys

RedisOpera = redis.StrictRedis(host=Environmental_parameters.redis_host, port=Environmental_parameters.redis_port)






class RotateUserAgentMiddleware(UserAgentMiddleware):
    # def __init__(self, user_agent=''):
    #     self.user_agent = user_agent
    def process_request(self, request, spider):
        ua = random.choice(settings.USER_AGENT_LIST)
        if ua:
            print(ua)
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        url = 'http://182.254.215.182:5999'
        proxy = requests.get(url, auth=('zs5scom', 'zs5scom')).text
        request.meta['proxy'] = "http://" + proxy







