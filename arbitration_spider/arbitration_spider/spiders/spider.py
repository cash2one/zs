#coding:utf-8
import scrapy
from arbitration_spider.items import ArbitrationZhejiangItem
from arbitration_spider.items import ArbitrationGuangdongItem
from arbitration_spider.items import ArbitrationShanghaiItem
from arbitration_spider.items import ArbitrationJiangsuItem
from arbitration_spider.items import ArbitrationHeilongjiangItem

import redis
import arbitration_spider.Environmental_parameters as Environmental_parameters
import logging
from bs4 import BeautifulSoup
import re
import time
import datetime
import heapq


RedisOpera = redis.StrictRedis(host=Environmental_parameters.redis_host, port=Environmental_parameters.redis_port)


def division(response_extract, direction):
    respons_str = "".join(response_extract)
    num1 = respons_str.rfind(":")
    num2 = respons_str.rfind("：")
    num3 = respons_str.rfind("，")
    num_list = []
    num_list.append(num1)
    num_list.append(num2)
    num_list.append(num3)
    num_get = heapq.nlargest(1, num_list)
    for num_max in num_get:
        if num_max == -1:
            return False
        elif direction == "left":
            respons_get = respons_str[:num_max]
        elif direction == "right":
            respons_get = respons_str[num_max + 1:]
        else:
            return "The wrong direction"
        response_last = respons_get.strip()
        return response_last


def str_to_list(a):
    b = a.split(",{")
    list = []
    for i in b:
        dict = {}
        i = i.replace("{", "", 2)
        i = i.replace("}", "", 2)
        list_content = i.split(",\"")
        for q in list_content:
            list_last = q.split(":")
            str = list_last[0]
            if str[0] == '"':
                str = str[1:]
            if str[-1] == '"':
                str = str[:-1]
            list_last[0] = str
            str1 = list_last[1]
            if str1[0] == '"':
                str1 = str1[1:]
            if str1[-1] == '"':
                str1 = str1[:-1]
            list_last[1] = str1
            dict[list_last[0]] = list_last[1]
        list.append(dict)
    return list


def bs_parse(dom):
    a = "".join(dom)
    soup = BeautifulSoup(a, "html5lib")
    tags = soup.find_all(re.compile("\w*"))
    for tag in tags:
        nms = tuple(tag.attrs.keys())
        for nm in nms:
            del tag[nm]
    try:
        b = list(soup.body.contents)
    except Exception as e:
        print(e)
    bs_result = ''
    for cc in b:
        bs_result += str(cc)
    return bs_result


class ArbitrationZhejiang(scrapy.Spider):
    name = "zhejiang"
    start_urls = ["http://ldzc.zjhrss.gov.cn/ldzc/onlinelearn/cms/bb5hlist?jsoncallback=jQuery111303864416212000952_1486374438418&count=15&num=1&aab301=&type=&abb703=&abb704=&_=1486374438420"]
    allowed_domains = ["ldzc.zjhrss.gov.cn"]

    def parse(self, response):
        for i in range(1,399):
            parse_url = "http://ldzc.zjhrss.gov.cn/ldzc/onlinelearn/cms/bb5hlist?jsoncallback=jQuery111303864416212000952_1486374438418&count=15&num=" + str(i) + "&aab301=&type=&abb703=&abb704=&_=1486374438420"
            yield scrapy.Request(parse_url, callback=self.parse2)

    def parse2(self, response):
        item = ArbitrationZhejiangItem()
        logger = logging.getLogger('zhejiang')
        try:
            url_cont = RedisOpera.sismember("arbitration_zhejiang", response.url)
            if url_cont != 0:
                return True
            else:
                item["url"] = response.url
                res_decode = response.body
                text_parse = res_decode.decode("utf-8")
                num = text_parse.find("[{")
                text_parse = text_parse[num+1:-2]
                text_list = str_to_list(text_parse)
                for i in text_list:
                    item["Arbitration_title"] = i.get("abb016")
                    item["Arbitration_units"] = i.get('abb704')
                    item["Arbitration_commission_name"] = i.get("fwjg")
                    str_time = i.get("abz354")
                    try:
                        time_get = datetime.datetime.strptime(str_time, '%Y-%m-%d')
                    except Exception as e:
                        logger.error('save_time_error:%s', e)
                    item["time"] = time_get

                    str = i.get("bfd195")
                    item["content"] = str.replace("\\n", "<br/>")
                    item["Arbitration_person"] = i.get("abb703")
                    item["source_city"] = i.get("aab301name")
                    item["source_province"] = "浙江"
                    item["divison_code"] = i.get("aab301id")
                    yield item
        except Exception as e:
            print(e)


class ArbitrationGuangdong(scrapy.Spider):
    name = "guangdong"
    start_urls = ["http://www.gdhrss.gov.cn/publicfiles/business/htmlfiles/tjzcw/sdgg/list.html"]


    def parse(self, response):
        print("start parse")
        item = ArbitrationGuangdongItem()
        for href in response.xpath('//td[@class="time"]/a/@href').extract():
            get_href = "http://www.gdhrss.gov.cn/publicfiles" + href[11:]
            print(get_href)
            full_url = response.urljoin(get_href)
            yield scrapy.Request(full_url, meta={"item":item}, callback=self.parse_item)


    def parse_item(self, response):
        logger = logging.getLogger('guangdong')
        try:
            url_cont = RedisOpera.sismember("arbitration_shanghai", response.url)
            if url_cont != 0:
                return True
            else:
                item = response.meta["item"]
                item["url"] = response.url

                title = response.xpath('//td[@class="font14"]/p[2]//text()').extract()
                temp = "".join(title)
                item["Arbitration_title"] = temp.strip()

                units = response.xpath('//td[@class="font14"]/p[3]//strong/text()').extract()
                units_name = "".join(units)
                num1 = units_name.find(":")
                if num1 != -1:
                    units_name = units_name[:num1]
                num2 = units_name.find("：")
                if num2 != -1:
                    units_name = units_name[:num2]
                num3 = units_name.find("，")
                if num3 != -1:
                    units_name = units_name[:num3]
                item["Arbitration_units"] = units_name.strip()

                commission_name = response.xpath('//td[@class="font14"]/p[1]//strong/text() | //td[@class="font14"]//p//strong/font/text() | //td[@class="font14"]//p[1]//strong/font[1]//text()').extract()
                commission_get = "".join(commission_name)
                num = commission_get.find("布")
                if num != -1:
                    commission_get = commission_get[: num - 1]
                item["Arbitration_commission_name"] = commission_get.strip()


                time = response.xpath('//td[@class="font14"]/text()').extract()
                time_parse = "".join(time)
                num = time_parse.find("20")
                time_get = time_parse[num : num + 10]
                str_time = time_get.strip()
                try:
                    time_get = datetime.datetime.strptime(str_time, '%Y年%m月%d日')
                except Exception as e:
                    logger.error('save_time_error:%s', e)
                item["time"] = time_get

                content = response.xpath('//td[@class="font14"]//p[position()>2] | //td[@class="font14"]//p[position()>2] | //td[@class="font14"]//font//p').extract()
                temp = "".join(content)
                content_get = bs_parse(temp)
                item["content"] = content_get

                item["source_province"] = "广东"
                yield item
        except Exception as e:
            logger.error('parse_webpage_error:%s', e)


class ArbitrationShanghai(scrapy.Spider):
    name = "shanghai"
    start_urls = ["http://www.12333sh.gov.cn/201412333/xxgk/zcgg/index.shtml"]
    allowed_domains = ["www.12333sh.gov.cn"]

    def parse(self, response):
        for i in range(0, 500):
            if i == 0:
                full_url = "http://www.12333sh.gov.cn/201412333/xxgk/zcgg/index.shtml"
                yield scrapy.Request(full_url, callback=self.parse2)
            else:
                full_url = "http://www.12333sh.gov.cn/201412333/xxgk/zcgg/index_" + str(i) + ".shtml"
                yield scrapy.Request(full_url, callback=self.parse2)


    def parse2(self, response):
        item = ArbitrationShanghaiItem()
        # print(response.meta["proxy"])

        for href in response.xpath('//div[@id="subcontent"]//table[last()-1]//tr//td//a/@href').extract():
            get_href = "http://www.12333sh.gov.cn/201412333/xxgk/zcgg" + href[1:]
            print(get_href)
            full_url = response.urljoin(get_href)
            yield scrapy.Request(full_url, meta={"item":item}, callback=self.parse_item)


    def parse_item(self, response):
        logger = logging.getLogger('shanghai')
        try:
            print("enter_parse")
            url_cont = RedisOpera.sismember("arbitration_shanghai", response.url)
            if url_cont != 0:
                return True
            else:

                item = response.meta["item"]
                item["url"] = response.url

                title = response.xpath('//table[@id="Table1"]//tbody//tr[2]//td/text()').extract()
                temp = "".join(title)
                item["Arbitration_title"] = temp.strip()

                units = response.xpath('//td[@id="fontzoom"]/p[1]/text()').extract()
                units_name = "".join(units)
                num1 = units_name.find(":")
                if num1 != -1:
                    units_name = units_name[:num1]
                num2 = units_name.find("：")
                if num2 != -1:
                    units_name = units_name[:num2]
                num3 = units_name.find("，")
                if num3 != -1:
                    units_name = units_name[:num3]
                item["Arbitration_units"] = units_name.strip()


                time_first = response.xpath('//tr/td[4]/span[@class="STYLE8"]/text()').extract()
                str_time = "".join(time_first)
                try:
                    time_get = datetime.datetime.strptime(str_time, '%Y年%m月%d日')
                except Exception as e:
                    logger.error('save_time_error:%s', e)
                item["time"] = time_get

                content = response.xpath('//td[@id="fontzoom"]//p').extract()
                temp = "".join(content)
                content_get = bs_parse(temp)
                item["content"] = content_get

                item["source_province"] = "上海"

                yield item
        except Exception as e:
            logger.error('parse_webpage_error:%s', e)


class ArbitrationJiangsu(scrapy.Spider):
    name = "jiangsu"
    start_urls = ["http://ggfw.jshrss.gov.cn/UnifiedPublicServicePlatform/business/ldjc/toArbitrationNoticeList.action?page.page=1"]
    allowed_domains = ["ggfw.jshrss.gov.cn"]

    def parse(self, response):
        for i in range(1, 900):
            full_url = "http://ggfw.jshrss.gov.cn/UnifiedPublicServicePlatform/business/ldjc/toArbitrationNoticeList.action?page.page=" + str(i)
            yield scrapy.Request(full_url, callback=self.parse2)


    def parse2(self, response):
        item = ArbitrationJiangsuItem()
        for href in response.xpath('//ul//li//a/@href').extract():
            full_url = response.urljoin(href)
            print("last_url:", full_url)
            yield scrapy.Request(full_url, meta={"item":item}, callback=self.parse_item)


    def parse_item(self, response):
        logger = logging.getLogger('jiangsu')
        try:
            print("enter_parse")
            url_cont = RedisOpera.sismember("arbitration_jiangsu", response.url)
            if url_cont != 0:
                return True
            else:
                item = response.meta["item"]
                item["url"] = response.url

                item["Arbitration_title"] = ""

                units = response.xpath('//div/p[@class="Custom_UnionStyle"]//text()[1]').extract()
                item["Arbitration_units"] = division(units, "left")

                time_first = response.xpath('//div[@class="files_left_tit_span"]/span[2]/text()').extract()
                time_second = "".join(time_first)
                time_num = time_second.find("20")
                str_get = time_second[time_num:]
                str_time = str_get.strip()
                try:
                    time_get = datetime.datetime.strptime(str_time, '%Y-%m-%d')
                except Exception as e:
                    logger.error('save_time_error:%s', e)
                item["time"] = time_get

                content = response.xpath('//div/p[@class="Custom_UnionStyle"]//text()').extract()
                temp = "".join(content)
                content_get = bs_parse(temp)
                item["content"] = content_get

                item["source_province"] = "江苏"

                commission_get = response.xpath('//tbody//tr[last()]/td/text()').extract()
                item["Arbitration_commission_name"] = division(commission_get, "right")

                yield item
        except Exception as e:
            logger.error('parse_webpage_error:%s', e)


class ArbitrationHeilongjiang(scrapy.Spider):
    name = "heilongjiang"
    start_urls = ["http://hl.lss.gov.cn/hljszc/more.jsp?type=005.001&key1=&key2=&key3=&key4=&page=1"]

    def parse(self, response):
        print("start_parse")
        for i in range(1, 5):
            full_url = "http://hl.lss.gov.cn/hljszc/more.jsp?type=005.001&key1=&key2=&key3=&key4=&page=" + str(i)
            yield scrapy.Request(full_url, callback=self.parse2)


    def parse2(self, response):
        print("start_parse2")
        item = ArbitrationHeilongjiangItem()
        for href in response.xpath('//table[last()-1]//td[2]/a/@href').extract()[8:]:
            full_url = response.urljoin(href)
            print("last_url:", full_url)
            yield scrapy.Request(full_url, meta={"item":item}, callback=self.parse_item)


    def parse_item(self, response):
        print("parse_item")
        logger = logging.getLogger('heilongjiang')
        try:
            print("enter_parse")
            url_cont = RedisOpera.sismember("arbitration_heilongjiang", response.url)
            if url_cont != 0:
                return True
            else:
                item = response.meta["item"]
                item["url"] = response.url

                title_first = response.xpath('//td[@class="STYLE4"]/text()').extract()
                title_get = "".join(title_first)
                if title_get.find("开庭公告") != -1:
                    return True
                item["Arbitration_title"] = title_get.strip()

                # units = response.xpath('//td//p/b/span/text()').extract()
                # if division(units, "left") or units == []:
                #     units = response.xpath('//td//p[3]//span/text()').extract()
                #     if division(units, "left") or units == []:
                #         units = response.xpath('//td//p[1]//span/text()').extract()

                item["Arbitration_units"] = ""


                time_first = response.xpath('//tr[4]/td[@align="center"]/text()').extract()
                time_second = "".join(time_first)
                time_num = time_second.find("20")
                str_get = time_second[time_num:]
                str_time = str_get.strip()
                try:
                    time_get = datetime.datetime.strptime(str_time, '%Y-%m-%d')
                except Exception as e:
                    logger.error('save_time_error:%s', e)
                item["time"] = time_get

                content = response.xpath('//table[@align="center"]//tr[last()-1]//p//text()').extract()
                temp = "".join(content)
                content_get = bs_parse(temp)
                item["content"] = content_get

                item["source_province"] = "黑龙江"

                yield item
        except Exception as e:
            logger.error('parse_webpage_error:%s', e)

