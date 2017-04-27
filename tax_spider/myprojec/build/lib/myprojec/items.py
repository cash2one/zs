# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyprojecItem(scrapy.Item):
    # define the fields for your item here like:
    type = scrapy.Field()
    spider_name = scrapy.Field()
    abstract = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    # pass

class TaxqiItem(scrapy.Item):
    # define the fields for your item here like:
    type = scrapy.Field()
    spider_name = scrapy.Field()
    abstract = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()


class ChinataxItem(scrapy.Item):
    # define the fields for your item here like:
    type = scrapy.Field()
    spider_name = scrapy.Field()
    abstract = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()

class TempItem(scrapy.Item):
    # define the fields for your item here like:
    type = scrapy.Field()
    spider_name = scrapy.Field()
    abstract = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()