#-*-coding:utf-8-*-
import random
import base64
import json
from . import settings
import redis
import requests
import logging
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import sys




class RotateUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua = random.choice(settings.USER_AGENT_LIST)
        if ua:
            print(ua)
            request.headers.setdefault('User-Agent', ua)



class ProxyMiddleware(object):
    def process_request(self, request, spider):
        url = 'http://45.63.123.116:5999'
        proxy = requests.get(url, auth=('zs5scom', 'zs5scom')).text
        request.meta['proxy'] = "http://" + proxy










