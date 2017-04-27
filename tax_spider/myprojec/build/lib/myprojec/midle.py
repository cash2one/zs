#-*-coding:utf-8-*-
import random
import base64
import json
from . import settings
import requests

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

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
        url = 'http://182.254.215.182:5999/'
        proxy = requests.get(url, auth=('zs5scom', 'zs5scom')).text
        request.meta['proxy'] = "http://" + proxy
