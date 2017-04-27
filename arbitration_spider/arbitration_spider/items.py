# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArbitrationZhejiangItem(scrapy.Item):
    url = scrapy.Field()
    Arbitration_title = scrapy.Field()
    Arbitration_units = scrapy.Field()
    Arbitration_commission_name = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    Arbitration_person = scrapy.Field()
    source_city = scrapy.Field()
    source_province = scrapy.Field()
    divison_code = scrapy.Field()

class ArbitrationGuangdongItem(scrapy.Item):
    url = scrapy.Field()
    Arbitration_title = scrapy.Field()
    Arbitration_units = scrapy.Field()
    Arbitration_commission_name = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    Arbitration_person = scrapy.Field()
    source_city = scrapy.Field()
    source_province = scrapy.Field()
    divison_code = scrapy.Field()

class ArbitrationShanghaiItem(scrapy.Item):
    url = scrapy.Field()
    Arbitration_title = scrapy.Field()
    Arbitration_units = scrapy.Field()
    Arbitration_commission_name = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    Arbitration_person = scrapy.Field()
    source_city = scrapy.Field()
    source_province = scrapy.Field()
    divison_code = scrapy.Field()


class ArbitrationJiangsuItem(scrapy.Item):
    url = scrapy.Field()
    Arbitration_title = scrapy.Field()
    Arbitration_units = scrapy.Field()
    Arbitration_commission_name = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    Arbitration_person = scrapy.Field()
    source_city = scrapy.Field()
    source_province = scrapy.Field()
    divison_code = scrapy.Field()


class ArbitrationHeilongjiangItem(scrapy.Item):
    url = scrapy.Field()
    Arbitration_title = scrapy.Field()
    Arbitration_units = scrapy.Field()
    Arbitration_commission_name = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    Arbitration_person = scrapy.Field()
    source_city = scrapy.Field()
    source_province = scrapy.Field()
    divison_code = scrapy.Field()