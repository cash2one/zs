# -*- coding: utf-8 -*-
from . import es
import logging
import codecs
import redis
import arbitration_spider.Environmental_parameters as Environmental_parameters


RedisOpera = redis.StrictRedis(host=Environmental_parameters.redis_host, port=Environmental_parameters.redis_port)


class JsonWithEncodingCnblogsPipeline(object):
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
            RedisOpera.sadd("arbitration_{}".format(spider.name), item["url"])
            self.count += 1
            print("es_save")
        except Exception as e:
            logger.error('es_save_error:', e)


    def close_spider(self, spider):
        logger = logging.getLogger(spider.name)
        logger.info('get_webpage_count:%d', self.count)
