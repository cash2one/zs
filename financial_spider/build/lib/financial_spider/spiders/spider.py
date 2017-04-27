#coding:utf-8
import scrapy
from financial_spider.items import FinancialSpiderItem
import time
from . import dom_clean
import hashlib
import redis
import financial_spider.Environmental_parameters as Environmental_parameters
import logging
import datetime

def log(*args):
    print(*args)
    # pass


# RedisOpera = redis.StrictRedis(host='dev.tax.redis.zs', port=6379)

RedisOpera = redis.StrictRedis(host=Environmental_parameters.redis_host, port=Environmental_parameters.redis_port)

class WdzjSpider(scrapy.Spider):
    name = "wdzj"
    start_urls = ["http://www.wdzj.com/news/yanjiu/"]
    allowed_domains = ["wdzj.com"]

    def handle_error(self, failure):
        logger = logging.getLogger('wdzj')
        logger.error("Error Handle: %s" % failure.request)
        logger.info("Sleeping 60 seconds")
        print("Sleeping 6 seconds")
        time.sleep(6)
        url = 'http://www.wdzj.com/news/yanjiu/'
        yield scrapy.Request(url, self.parse, errback=self.handle_error, dont_filter=True)

    def parse(self, response):
        item = FinancialSpiderItem()
        for href in response.xpath('//div[@class="text"]//h3//a/@href'):
            full_url = href.extract()
            log(full_url)
            yield scrapy.Request(full_url, meta={"item": item}, callback=self.parse_item)

        for href in response.xpath('//div[@class="pagebox"]//a[last()-1]/@href'):
            full_url = response.urljoin(href.extract())
            log(full_url)
            yield scrapy.Request(full_url, callback=self.parse)

    def parse_item(self, response):
        logger = logging.getLogger('wdzj')
        try:
            url_cont = RedisOpera.sismember("financial_wdzj", response.url)
            if url_cont != 0:
                return True
            else:
                log("parse_page")
                item = response.meta["item"]
                item["type"] = "financial"
                item["spider_name"] = "wdzj"
                item["url"] = response.url
                title = response.xpath('//h1[@class="s-title"]/text()').extract()
                item["title"] = "".join(title)

                temp_time = response.xpath('//div[@class="s-bq"]//span[1]/text()').extract()
                str_time = "".join(temp_time)
                try:
                    time_get = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    logger.error('save_time_error:%s', e)
                item["time"] = time_get



                source = response.xpath('//div[@class="s-bq"]//span[2]/text()').extract()
                item["source"] = "".join(source)

                abstract = response.xpath('//div[@class="s-zy"]//text()').extract()
                temp = "".join(abstract)
                item["abstract"] = temp.strip()


                dom = response.xpath('//div[@class="c-cen"]').extract()
                try:
                    dom_get = list(dom)
                    item["content"] = dom_clean.bs_parse(dom_get)
                except Exception as e:
                    logger.error('content_dom_clean_error:%s', e)
                yield item
        except Exception as e:
            logger.error('parse_webpage_error:%s', e)









