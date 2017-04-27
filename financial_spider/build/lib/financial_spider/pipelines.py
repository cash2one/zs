# -*- coding: utf-8 -*-
import logging
from . import es
import redis
import financial_spider.Environmental_parameters as Environmental_parameters
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

RedisOpera = redis.StrictRedis(host=Environmental_parameters.redis_host, port=Environmental_parameters.redis_port)

class FinancialSpiderPipeline(object):
    def __init__(self):
        self.count = 0
        self.num = 0

    def process_item(self, item, spider):
        logger = logging.getLogger(spider.name)
        try:
            i = dict(item)
            if self.num == 0:
                es.add_mapping()
                self.num += 1
            es.es_save([i])
            RedisOpera.sadd("financial_{}".format(spider.name), item["url"])
            self.count += 1
            print("es_save")
        except Exception as e:
            logger.error('es_save_error:', e)


    def close_spider(self, spider):
        logger = logging.getLogger(spider.name)
        logger.info('get_webpage_count:%d', self.count)


