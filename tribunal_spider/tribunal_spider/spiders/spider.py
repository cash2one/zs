#coding:utf-8
import scrapy
from tribunal_spider.items import ZhejiangItem
from tribunal_spider.items import GuangdongItem
from tribunal_spider.items import ShanghaiItem
from tribunal_spider.items import JiangsuItem
from tribunal_spider.items import HeilongjiangItem
from selenium import webdriver
from lxml import etree
import redis
import tribunal_spider.Environmental_parameters as Environmental_parameters
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
            list_last = q.split(":", 1)
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


class TribunalZhejiang(scrapy.Spider):
    name = "zhejiang"
    start_urls = ["http://ldzc.zjhrss.gov.cn/ldzc/onlinelearn/cms/bb3flist?jsoncallback=jQuery111309199566876902545_1490168372426&count=15&num=1&aab301=&type=&abb703=&abb704=&keyword=&_=1490168372427"]
    allowed_domains = ["ldzc.zjhrss.gov.cn"]

    def parse(self, response):
        for i in range(1,20000):
            parse_url = "http://ldzc.zjhrss.gov.cn/ldzc/onlinelearn/cms/bb3flist?jsoncallback=jQuery111309199566876902545_1490168372426&count=15&num=" + str(i) + "&aab301=&type=&abb703=&abb704=&keyword=&_=1490168372427"
            yield scrapy.Request(parse_url, callback=self.parse2)

    def parse2(self, response):
        item = ZhejiangItem()
        logger = logging.getLogger('zhejiang')
        try:
            url_cont = RedisOpera.sismember("tribunal_zhejiang", response.url)
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
                    item["tribunal_title"] = i.get("abb016")
                    item["tribunal_units"] = i.get("abb704")
                    item["tribunal_commission_name"] = i.get("abe124")

                    str_time = i.get("abb780")
                    try:
                        time_get = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M')
                    except Exception as e:
                        logger.error('save_time_error:%s', e)
                    item["tribunal_time"] = time_get

                    item["tribunal_applicant"] = i.get("abb703")
                    item["tribunal_place"] = i.get("abb779")
                    item["source_city"] = i.get("aab301name")
                    item["source_province"] = "浙江"

                    yield item
        except Exception as e:
            print(e)


class TribunalGuangdong(scrapy.Spider):
    name = "guangdong"
    start_urls = ["http://www.gdhrss.gov.cn/publicfiles/business/htmlfiles/tjzcw/ktgg/list.html#"]


    def parse(self, response):
        print("start parse")
        item = GuangdongItem()
        for href in response.xpath('//td[@class="time"]/a/@href').extract():
            # get_href = "http://www.gdhrss.gov.cn/publicfiles" + href[11:]
            # print(get_href)
            full_url = response.urljoin(href)
            print(full_url)
            yield scrapy.Request(full_url, meta={"item":item}, callback=self.parse_item)


    def parse_item(self, response):
        logger = logging.getLogger('guangdong')
        try:
            url_cont = RedisOpera.sismember("tribunal_guangdong", response.url)
            if url_cont != 0:
                return True
            else:
                item = response.meta["item"]
                item["url"] = response.url

                title = response.xpath('//tr[2]/td[2]/p[@class="MsoNormal"]/b//text()').extract()
                temp = "".join(title)
                item["tribunal_title"] = temp.strip()

                applicant = response.xpath('//tr[3]/td[2]/p[@class="MsoNormal"]/b//text()').extract()
                temp = "".join(applicant)
                item["tribunal_applicant"] = temp.strip()

                units = response.xpath('//tr[4]/td[2]/p[@class="MsoNormal"]/b//text()').extract()
                temp = "".join(units)
                item["tribunal_units"] = temp.strip()

                reason = response.xpath('//tr[5]/td[2]/p[@class="MsoNormal"]/b//text()').extract()
                temp = "".join(reason)
                item["tribunal_reason"] = temp.strip()

                arbitrator = response.xpath('//tr[6]/td[2]/p[@class="MsoNormal"]/b//text()').extract()
                temp = "".join(arbitrator)
                item["tribunal_arbitrator"] = temp.strip()

                clerk = response.xpath('//tr[7]/td[2]/p[@class="MsoNormal"]/b//text()').extract()
                temp = "".join(clerk)
                item["tribunal_clerk"] = temp.strip()

                place = response.xpath('//tr[8]/td[2]/p[@class="MsoNormal"]/b//text()').extract()
                temp = "".join(place)
                item["tribunal_place"] = temp.strip()

                str_time = response.xpath('//tr[1]/td[2]/p[@class="MsoNormal"]//text() | //tr[@style="HEIGHT: 29.75pt"]/td[2]/p[1]//text()').extract()
                temp = "".join(str_time)
                year_num = temp.find("20")
                day_num = temp.find("日")
                year = temp[year_num:day_num + 1]
                hours_num = temp.rfind("午")
                hours = temp[hours_num + 1:hours_num + 6]
                if hours.find("：") != -1:
                    hours = hours.replace("：", ":")
                format_time = year + " " + hours
                try:
                    time_get = datetime.datetime.strptime(format_time, '%Y年%m月%d日 %H:%M')
                except Exception as e:
                    print("error_url", response.url)
                    logger.error('save_time_error:%s', e)
                item["tribunal_time"] = time_get

                item["source_province"] = "广东"

                yield item
        except Exception as e:
            logger.error('parse_webpage_error:%s', e)


class TribunalShanghai(scrapy.Spider):
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
        item = ShanghaiItem()
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
            url_cont = RedisOpera.sismember("tribunal_shanghai", response.url)
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


class TribunalJiangsu(scrapy.Spider):
    name = "jiangsu"
    start_urls = ["http://ggfw.jshrss.gov.cn/UnifiedPublicServicePlatform/business/ldjc/toArbitrationNoticeList.action?page.page=1"]
    allowed_domains = ["ggfw.jshrss.gov.cn"]

    def parse(self, response):
        for i in range(1, 900):
            full_url = "http://ggfw.jshrss.gov.cn/UnifiedPublicServicePlatform/business/ldjc/toArbitrationNoticeList.action?page.page=" + str(i)
            yield scrapy.Request(full_url, callback=self.parse2)


    def parse2(self, response):
        item = JiangsuItem()
        for href in response.xpath('//ul//li//a/@href').extract():
            full_url = response.urljoin(href)
            print("last_url:", full_url)
            yield scrapy.Request(full_url, meta={"item":item}, callback=self.parse_item)


    def parse_item(self, response):
        logger = logging.getLogger('jiangsu')
        try:
            print("enter_parse")
            url_cont = RedisOpera.sismember("tribunal_jiangsu", response.url)
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


class TribunalHeilongjiang(scrapy.Spider):
    name = "heilongjiang"
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        logger = logging.getLogger('heilongjiang')
        item = HeilongjiangItem()
        print("PhantomJS start...")
        driver = webdriver.PhantomJS()
        driver.get("http://hl.lss.gov.cn/hljszc/CtrlServlet?parm=search_Court")
        driver.implicitly_wait(3)
        time.sleep(3)

        num = 0
        true_page = driver.page_source
        origin_html = etree.HTML(true_page)

        number_pages = origin_html.xpath('//div[@class="page-inputleft3"]/span/text()')
        temp = "".join(number_pages)
        int_pages = int(temp)
        mainwin = driver.current_window_handle
        print("mainwin:", mainwin)
        print("int_pages:", int_pages)
        for i in range(0, int_pages):
            if num != 0:
                next_page = driver.find_element_by_xpath('//li[@class="page-txt"][3]')
                next_page.click()
                mainwin = driver.current_window_handle
                print("click get")

            hrefs = origin_html.xpath('//td[@width="200px"]')
            for i in range(0, len(hrefs)):
                links = driver.find_elements_by_xpath('//td[@width="200px"]/a')
                links[i].click()
                time.sleep(3)

                handles = driver.window_handles
                print(handles)
                for i in handles:
                    if mainwin == i:
                        continue
                    else:
                        driver.switch_to.window(i)

                page = driver.page_source
                print(page)
                response_body = etree.HTML(page)
                try:
                    print("enter_parse")
                    url_cont = RedisOpera.sismember("tribunal_heilongjiang", driver.current_url)
                    if url_cont != 0:
                        driver.close()
                        driver.switch_to.window(mainwin)
                        continue
                    else:
                        item["url"] = driver.current_url

                        title = response_body.xpath('//td[@align="center"]//tbody/tr[1]/td[1]/text()')
                        temp = "".join(title)
                        item["tribunal_title"] = temp.strip()

                        applicant = response_body.xpath('//td[@align="center"]//tbody/tr[2]/td[1]/text()')
                        temp = "".join(applicant)
                        item["tribunal_applicant"] = temp.strip()

                        units = response_body.xpath('//td[@align="center"]//tbody/tr[2]/td[2]/text()')
                        temp = "".join(units)
                        item["tribunal_units"] = temp.strip()

                        arbitrator = response_body.xpath('//td[@align="center"]//tbody/tr[4]/td[1]/text()')
                        temp = "".join(arbitrator)
                        item["tribunal_arbitrator"] = temp.strip()

                        place = response_body.xpath('//td[@align="center"]//tbody/tr[3]/td[2]/text()')
                        temp = "".join(place)
                        item["tribunal_place"] = temp.strip()

                        str_time = response_body.xpath('//td[@align="center"]//tbody/tr[1]/td[2]/text()')
                        temp = "".join(str_time)
                        format_time = temp.strip()
                        try:
                            time_get = datetime.datetime.strptime(format_time, '%Y年%m月%d日')
                        except Exception as e:
                            print("error_url", response.url)
                            logger.error('save_time_error:%s', e)
                        item["tribunal_time"] = time_get

                        item["source_province"] = "黑龙江"

                        yield item
                        driver.close()
                        driver.switch_to.window(mainwin)

                except Exception as e:
                    logger.error('parse_webpage_error:%s', e)
            num += 1
        print("quit driver")
        driver.quit()






