# -*- coding: utf-8 -*-
import json
import codecs
from . import es
import scrapy
import logging
import redis
import myprojec.Environmental_parameters as Environmental_parameters
import requests



from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import time
import os

runner = CrawlerRunner(get_project_settings())

# 'followall' is the name of one of the spiders of the project.

# logging.basicConfig(
#     format='%(levelname)s: %(levelname)s: %(message)s',
# )

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

RedisOpera = redis.StrictRedis(host=Environmental_parameters.redis_host, port=Environmental_parameters.redis_port)


class JsonWithEncodingCnblogsPipeline(object):
    def __init__(self):
        # self.line_list = []
        self.count = 0
        self.num = 0

    def process_item(self, item, spider):
        logger = logging.getLogger(spider.name)
        logger.info('in pipelines')
        try:
            i = dict(item)
            if self.num == 0:
                es.add_mapping()
                self.num += 1
            es.es_save([i])
            RedisOpera.sadd("tax_{}".format(spider.name), item["url"])
            logger.info('es_save')
            self.count += 1
        except Exception as e:
            logger.error('save_error:', e)


        # if spider.name == 'zjds':
        #     logger = logging.getLogger('zjds')
        #     try:
        #         i = dict(item)
        #         es.es_save([i])
        #         self.count += 1
        #     except Exception as e:
        #         print(e)
        #         logger.error('es_save_error:%s', e)
        # elif spider.name == 'taxqi':
        #     logger = logging.getLogger('taxqi')
        #     try:
        #         i = dict(item)
        #         es.es_save([i])
        #         self.count += 1
        #     except Exception as e:
        #         print(e)
        #         logger.error('es_save_error:%s', e)
        # elif spider.name == 'chinatax':
        #     try:
        #         i = dict(item)
        #         es.es_save([i])
        #         self.count += 1
        #     except Exception as e:
        #         print(e)
        #         logger.error('es_save_error:%s', e)

        # if spider.name == 'chinatax':
        #     self.line_list.append(dict(item))
        # elif spider.name == 'zjds':
        #     self.line_list.append(dict(item))
        # elif spider.name == 'taxqi':
        #     self.line_list.append(dict(item))

        # return dict(item)


    def close_spider(self, spider):
        logger = logging.getLogger(spider.name)
        logger.info('get_webpage_count:%d', self.count)
        logger.info('success')

        time.sleep(100)
        # print("already restart")
        # d = runner.crawl('zjds')
        # d.addBoth(lambda _: reactor.stop())
        # reactor.run()
        schedule_url = 'http://192.168.5.220:5888/update_spider'
        proxy = requests.get(schedule_url, auth=("zs5scom", "zs5scom")).text
        print(proxy)





        # if spider.name == 'zjds':
        #     log('created_file')
        #     opened_file = codecs.open('zj.json', 'w', encoding="utf-8")
        #     opened_file.write(str(self.line_list))
        #     opened_file.close()
        # elif spider.name == 'taxqi':
        #     log('created_file')
        #     opened_file = codecs.open('taxqi.json', 'w', encoding="utf-8")
        #     opened_file.write(str(self.line_list))
        #     opened_file.close()
        # elif spider.name == 'chinatax':
        #     log('created_file')
        #     opened_file = codecs.open('chinatax.json', 'w', encoding="utf-8")
        #     opened_file.write(str(self.line_list))
        #     opened_file.close()
        #     print('done')

