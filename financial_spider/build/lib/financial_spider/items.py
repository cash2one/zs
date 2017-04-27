# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FinancialSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = scrapy.Field()
    spider_name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    abstract = scrapy.Field()
