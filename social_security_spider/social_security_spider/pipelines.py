# -*- coding: utf-8 -*-
from . import mongo
import logging
import redis
import pymongo
import social_security_spider.Environmental_parameters as Environmental_parameters




import pymongo

from scrapy.exceptions import DropItem


class MongoDBPipeline(object):

    # def __init__(self):
        # self.client = pymongo.MongoClient(
        #     host=Environmental_parameters.mongodb_server,
        #     port=Environmental_parameters.mongodb_port
        # )
        # # 如果需要密码
        # # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        # self.db = self.client[Environmental_parameters.mongodb_db]  # 获得数据库的句柄

    def process_item(self, item, spider):
        logger = logging.getLogger(spider.name)
        try:
            postitem = dict(item)  # 把item转化成字典形式
            mongo.mongo_save(postitem)
        except Exception as e:
            logger.error('mongo_save_error:', e)

    def close_spider(self, spider):
        logger = logging.getLogger(spider.name)
        logger.info('we let it done:%s' %spider.name)


