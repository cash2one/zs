# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhejiangItem(scrapy.Item):
    url = scrapy.Field()
    tribunal_title = scrapy.Field()
    tribunal_units = scrapy.Field()
    tribunal_commission_name = scrapy.Field()
    tribunal_time = scrapy.Field()
    tribunal_applicant = scrapy.Field()
    tribunal_place = scrapy.Field()
    source_city = scrapy.Field()
    source_province = scrapy.Field()
    tribunal_reason = scrapy.Field()
    tribunal_arbitrator = scrapy.Field()
    tribunal_clerk = scrapy.Field()

class GuangdongItem(scrapy.Item):
    url = scrapy.Field()
    tribunal_title = scrapy.Field()
    tribunal_units = scrapy.Field()
    tribunal_commission_name = scrapy.Field()
    tribunal_time = scrapy.Field()
    tribunal_applicant = scrapy.Field()
    tribunal_place = scrapy.Field()
    source_city = scrapy.Field()
    source_province = scrapy.Field()
    tribunal_reason = scrapy.Field()
    tribunal_arbitrator = scrapy.Field()
    tribunal_clerk = scrapy.Field()

class ShanghaiItem(scrapy.Item):
    url = scrapy.Field()
    tribunal_title = scrapy.Field()
    tribunal_units = scrapy.Field()
    tribunal_commission_name = scrapy.Field()
    tribunal_time = scrapy.Field()
    tribunal_applicant = scrapy.Field()
    tribunal_place = scrapy.Field()
    source_city = scrapy.Field()
    source_province = scrapy.Field()
    tribunal_reason = scrapy.Field()
    tribunal_arbitrator = scrapy.Field()
    tribunal_clerk = scrapy.Field()


class JiangsuItem(scrapy.Item):
    url = scrapy.Field()
    tribunal_title = scrapy.Field()
    tribunal_units = scrapy.Field()
    tribunal_commission_name = scrapy.Field()
    tribunal_time = scrapy.Field()
    tribunal_applicant = scrapy.Field()
    tribunal_place = scrapy.Field()
    source_city = scrapy.Field()
    source_province = scrapy.Field()
    tribunal_reason = scrapy.Field()
    tribunal_arbitrator = scrapy.Field()
    tribunal_clerk = scrapy.Field()


class HeilongjiangItem(scrapy.Item):
    url = scrapy.Field()
    tribunal_title = scrapy.Field()
    tribunal_units = scrapy.Field()
    tribunal_commission_name = scrapy.Field()
    tribunal_time = scrapy.Field()
    tribunal_applicant = scrapy.Field()
    tribunal_place = scrapy.Field()
    source_city = scrapy.Field()
    source_province = scrapy.Field()
    tribunal_reason = scrapy.Field()
    tribunal_arbitrator = scrapy.Field()
    tribunal_clerk = scrapy.Field()