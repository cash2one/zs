#-*-coding:utf-8-*-
import random
import base64
import json
from . import settings
import redis
import arbitration_spider.Environmental_parameters as Environmental_parameters
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


    # def process_request(self, request, spider):
    #     # self.cont += 1
    #     # if self.cont % 10 == 0:
    #     logger = logging.getLogger(spider.name)
    #     try:
    #         response = requests.get("http://ip.chinaz.com/getip.aspx")
    #         response.status_code = 0
    #         try:
    #             while response.status_code != 200:
    #                 try:
    #                     # num = RedisOpera.scard("ip_pool")
    #                     # if num == 0:
    #                     #     sys.exit()
    #                     ip_b = RedisOpera.srandmember("ip_pool", 1)[0]
    #                     ip = ip_b.decode("utf-8")
    #                     # ip = "113.135.227.80:9999"
    #                     proxy_host = "http://" + ip
    #                     proxyDict = {"http": proxy_host}
    #                     response = requests.get("http://ip.chinaz.com/getip.aspx", proxies=proxyDict, timeout=10)
    #                 except Exception as e:
    #                     print(e)
    #                     RedisOpera.srem("ip_pool", ip)
    #                     # num = RedisOpera.scard("ip_pool")
    #                     # if num == 0:
    #                     #     sys.exit()
    #             else:
    #                 request.meta['proxy'] = "http://" + ip
    #                 logger.info('get new proxy %s' % ip)
    #                 print(ip)
    #         except Exception as e:
    #             print(e)
    #     except Exception as e:
    #         print(e)
    #     # else:
    #     #     return True








