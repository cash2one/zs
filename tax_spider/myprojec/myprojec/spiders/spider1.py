#coding:utf-8
import scrapy
from myprojec.items import MyprojecItem
from myprojec.items import TaxqiItem
from myprojec.items import ChinataxItem
from myprojec.items import TempItem
import time
from . import dom_clean
import hashlib
import redis
import myprojec.Environmental_parameters as Environmental_parameters
import logging
import datetime
import random

# logger = logging.getLogger('zjds')
# logger.error('save_time_error:%s', e)

# RedisOpera = redis.StrictRedis(host='dev.tax.redis.zs', port=6379)

RedisOpera = redis.StrictRedis(host=Environmental_parameters.redis_host, port=Environmental_parameters.redis_port)


class ZjdsSpider(scrapy.Spider):
    name = "zjds"
    start_urls = ["http://zjds.zjol.com.cn/yw/"]
    allowed_domains = ["zjds.zjol.com.cn"]


    def parse(self, response):
        item = MyprojecItem()
        logger = logging.getLogger('zjds')
        logger.info('start parse')
        for href in response.xpath('//*[@id="list_left"]/ul/li/a/@href'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, meta={"item":item}, callback=self.parse_item)

        url = response.xpath('//*[@id="list_left"]/div[2]/a[last()]/@href').extract()
        parse_url = "".join(list(url))
        yield scrapy.Request(parse_url, callback=self.parse)



    def parse_item(self, response):
        logger = logging.getLogger('zjds')
        logger.info('start parse item')
        try:
            url_cont = RedisOpera.sismember("tax_taxqi", response.url)
            if url_cont != 0:
                logger.info('url already exist')
                return True
            else:
                logger.info('parse item')
                r_url = response.url
                if r_url.find("zjnew") == -1 and r_url.find("gov") == -1:
                    item = response.meta["item"]
                    item["url"] = response.url
                    item["type"] = "tax"
                    item["spider_name"] = "zjds"


                    a = response.xpath('//*[@id="data"]/span[1]/text()|//*[@id="wrap"]/div//span[4]/text()').extract()
                    b = "".join(list(a))
                    if b.find('时间') == -1 or b == "":
                        pass
                    else:
                        b = b[3:]

                    try:
                        time_get = datetime.datetime.strptime(b, "%Y-%m-%d %H:%M")
                    except Exception as e:
                        logger.error('save_time_error:%s', e)
                    item["time"] = time_get

                    e = response.xpath('//*[@id="list_left"]/h1/text()|//*[@id="list_left2"]/h1/text()|//*[@id="wrap"]/div/h2/text()').extract()
                    f = "".join(list(e))
                    item["title"] = f

                    y = response.xpath('//*[@id="textp"]/p|img').extract()
                    try:
                        y = list(y)
                        item["content"] = dom_clean.bs_parse(y, "zjds")
                    except Exception as e:
                        logger.error('content_dom_clean_error:%s', e)

                    g = response.xpath('//*[@id="data"]/span[2]/text()|//*[@class="data"]/span[1]/text()').extract()
                    h = "".join(list(g))
                    item["source"] = h

                    logger.info('yield item')
                    yield item
                else:
                    return True
        except Exception as e:
            logger.error('parse_webpage_error:%s', e)


class TaxqiSpider(scrapy.Spider):
    name = "taxqi"
    start_urls = ["http://www.taxqi.com/news/"]
    allowed_domains = ["taxqi.com"]


    def parse(self, response):
        item = TaxqiItem()
        logger = logging.getLogger('taxqi')
        logger.info('start parse')
        for href in response.xpath('//div[@class="news"]//li//a[last()]/@href').extract():
            get_href = 'http://www.taxqi.com' + href
            full_url = response.urljoin(get_href)
            yield scrapy.Request(full_url, meta={"item":item}, callback=self.parse_item)

        url = response.xpath('//div[@class="content"]//a[@class="Pager_NextBtn"]/@href').extract()
        get_url = "".join(list(url))
        parse_url = 'http://www.taxqi.com' + get_url
        yield scrapy.Request(parse_url, callback=self.parse)



    def parse_item(self, response):
        logger = logging.getLogger('taxqi')
        try:
            url_cont = RedisOpera.sismember("tax_taxqi", response.url)
            if url_cont != 0:
                logger.info('url already exist')
                return True
            else:
                logger.info('parse item')
                item = response.meta["item"]
                item["type"] = "tax"
                item["spider_name"] = "taxqi"
                item["url"] = response.url
                item["abstract"] = ""


                a = response.xpath('//div[@class="content"]//div[@class="Contents_date"]/text()').extract()
                b = "".join(list(a))
                if b == "":
                    pass
                else:
                    b = b[5:]
                b = b.strip()
                hour = random.randint(8, 18)
                minute = random.randint(10, 59)
                time_first = b + " " + str(hour) + ":" + str(minute)

                try:

                    time_get = datetime.datetime.strptime(time_first, "%Y-%m-%d %H:%M")
                    # time_get = time_temp.strftime('%Y-%m-%d')
                except Exception as e:
                    logger.error('save_time_error:%s', e)
                item["time"] = time_get

                e = response.xpath('//h1[@class="Contents_tittle"]/text()').extract()
                f = "".join(list(e))
                item["title"] = f.strip()

                y = response.xpath('//div[@class="Contents_word"]/p|img').extract()
                try:
                    y = list(y)
                    item["content"] = dom_clean.bs_parse(y, "taxqi")
                except Exception as e:
                    logger.error('content_dom_clean_error:%s', e)

                item["source"] = '期税网'

                logger.info('yield item')

                yield item
        except Exception as e:
            logger.error('parse_webpage_error:%s', e)


class ChinataxSpider(scrapy.Spider):
    name = "chinatax"
    start_urls = ["http://www.chinatax.gov.cn/n810341/n810780/index_831221_1.html"]
    allowed_domains = ["www.chinatax.gov.cn"]

    def parse(self, response):
        logger = logging.getLogger('chinatax')
        logger.info('start parse')
        for i in range(1,300):
            parse_url = "http://www.chinatax.gov.cn/n810341/n810780/index_831221_" + str(i) + ".html"
            yield scrapy.Request(parse_url, callback=self.parse2)


    def parse2(self, response):
        item = ChinataxItem()
        logger = logging.getLogger('chinatax')
        logger.info('start parse2')
        for href in response.xpath('//dl//a/@href').extract():
            get_href = 'http://www.chinatax.gov.cn' + href[5:]
            full_url = response.urljoin(get_href)
            yield scrapy.Request(full_url, meta={"item":item}, callback=self.parse_item)


    def parse_item(self, response):
        logger = logging.getLogger('chinatax')
        try:
            url_cont = RedisOpera.sismember("tax_chinatax", response.url)
            if url_cont != 0:
                logger.info('url already exist')
                return True
            else:
                logger.info('parse item')
                item = response.meta["item"]
                item["url"] = response.url
                item["type"] = "tax"
                item["spider_name"] = "chinatax"
                item["abstract"] = ""

                a = response.xpath('//div//li[@class="sv_texth2"]/text()').extract()
                b = "".join(list(a))
                if b.find("发布") != -1:
                    y = b.find("发布")
                    u = b[y+5:y+16]

                    u = u.strip()
                    hour = random.randint(8, 18)
                    minute = random.randint(10, 59)
                    time_first = u + " " + str(hour) + ":" + str(minute)

                    time_get = datetime.datetime.strptime(time_first, "%Y年%m月%d日 %H:%M")
                    item["time"] = time_get
                else:
                    item["time"] = 0

                if b.find("来源") != -1:
                    q = b.find("来源")
                    w = b[q:]
                    item["source"] = str.rstrip(w)
                else:
                    item["source"] = ""

                e = response.xpath('//div//li[@class="sv_texth1"]/text()').extract()
                temp = "".join(list(e))
                item["title"] = temp.strip()

                y = response.xpath('//div//li[@class="sv_texth3"]/p|img').extract()
                try:
                    y = list(y)
                    item["content"] = dom_clean.bs_parse(y, "chinatax")
                except Exception as e:
                    logger.error('content_dom_clean_error:%s', e)
                logger.info('yield item')
                yield item
        except Exception as e:
            logger.error('parse_webpage_error:%s', e)



class tempSpider(scrapy.Spider):
    name = "temp"
    start_urls = ["http://oil.cngold.com.cn/20170111d1970n115093439.html"]

    def parse(self, response):
        item = TempItem()
        try:
            url_cont = RedisOpera.sismember("tax_temp", response.url)
            if url_cont != 0:
                return True
            else:
                item["url"] = response.url
                item["type"] = "tax"
                item["spider_name"] = "temp"
                temp = response.xpath('//div[@class="left_body_two"]/p/text()').extract()
                item["abstract"] = "".join(temp)

                a = response.xpath('//div[@class="right_in2"]/text()').extract()
                b = "".join(list(a))
                try:
                    time_get = datetime.datetime.strptime(b, "%Y年%m月%d日 %H:%M")
                    item["time"] = time_get
                except Exception as e:
                    print(e)

                temp = response.xpath('//i[@style="margin-right: 0px;"]/text()').extract()
                item["source"] = "".join(temp)


                e = response.xpath('//div[@class="right_area2"]/h1/text()').extract()
                temp = "".join(list(e))
                item["title"] = temp.strip()

                y = response.xpath('//div[@class="left_body_center"]').extract()
                try:
                    y = list(y)
                    item["content"] = dom_clean.bs_parse(y, "temp")
                except Exception as e:
                    print(e)

                yield item
        except Exception as e:
            print(e)



