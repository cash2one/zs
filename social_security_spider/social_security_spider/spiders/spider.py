#coding:utf-8
import scrapy
from social_security_spider.items import HangzhouItem
# from social_security_spider.items import GuangdongItem
# from social_security_spider.items import ShanghaiItem
# from social_security_spider.items import JiangsuItem
# from social_security_spider.items import HeilongjiangItem
from lxml import etree
import redis
import social_security_spider.Environmental_parameters as Environmental_parameters
import logging
from bs4 import BeautifulSoup
import re
import time
import datetime
import heapq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
from . import verifycode

# 强哥 370685197909121317 Zero1one@hz
# 13716055137 Xxd123456

def page_num_get(page):
    if page[1] != 0:
        page_num = page[0] + 1
    else:
        page_num = page[0]
    return page_num


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


class SocialSecurityHangzhou(scrapy.Spider):
    name = "hangzhou"
    start_urls = ['http://puser.zjzwfw.gov.cn/sso/usp.do?action=ssoLogin&servicecode=njdh']

    def parse(self, response):
        logger = logging.getLogger('hangzhou')
        item = HangzhouItem()
        print("PhantomJS start...")
        driver = webdriver.PhantomJS()
        driver.set_window_size(2560, 1600)
        driver.get("http://puser.zjzwfw.gov.cn/sso/usp.do?action=ssoLogin&servicecode=njdh")
        driver.save_screenshot('1.png')
        print("get 1.png")
        try:
            dr = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "submit"))
            )
        except Exception as e:
            logger.error('we cant open the login page:', e)

        elem_user = driver.find_element_by_name("loginname")
        elem_user.send_keys("370685197909121317")
        elem_pwd = driver.find_element_by_name("loginpwd")
        elem_pwd.send_keys("Zero1one@hz")


        next_page = driver.find_element_by_id('submit')
        next_page.click()

        time.sleep(5)

        page = driver.page_source
        response_body = etree.HTML(page)
        temp = response_body.xpath('//div[@id="tab1"]/div/text()')
        verify = "".join(temp)
        verify_num = verify.find("密码")
        if verify_num != -1:
            return "用户名或者密码错误"

        verifycode_num = verify.find("验证码")
        if verifycode_num != -1:
            img_first = response_body.xpath('//img[@id="captcha_img"]/@src')
            img = "".join(img_first)
            img_url = "http://puser.zjzwfw.gov.cn/sso/" + img

            local_filename = 'spiders/verifycode.png'
            r = requests.get(img_url, stream=True)  # here we need to set stream = True parameter
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                f.close()


            elem_verifycode = driver.find_element_by_name('verifycode')
            elem_verifycode.send_keys(verifycode.answer)

            next_page = driver.find_element_by_id('submit')
            next_page.click()
            time.sleep(5)





        # 查看是否找到社保查询按钮
        try:
            dr = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@style="width: 1230px; left: 0px;"]//div[2][@title]'))
            )
        except Exception as e:
            logger.error('we cant find the socoal_security:', e)

        # 身份证信息
        item["Id_number"] = "370685197909121317"
        item["Date_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["City"] = "杭州"


        # 社保页面截屏
        driver.save_screenshot('2.png')
        print("get 2.png")

        # 点击社保按钮
        try:
            next_page = driver.find_element_by_xpath('//div[@style="width: 1230px; left: 0px;"]//div[2][@title]')
            next_page.click()
        except Exception as e:
            print(e)
            next_page = driver.find_element_by_xpath('//div[@class="rdfw_btn_left"]')
            next_page.click()

            time.sleep(2)
            driver.save_screenshot('3.png')
            print("get 3.png")


            next = driver.find_element_by_xpath('//div[@style="width: 1230px; left: 0px;"]//div[2][@title]')
            next.click()

        # 换页面到社保主页面
        mainwin = driver.current_window_handle
        handles = driver.window_handles
        print(handles)
        for i in handles:
            if mainwin == i:
                continue
            else:
                driver.switch_to.window(i)

        time.sleep(5)

        # 社保页面截屏
        driver.save_screenshot('4.png')
        print("get 4.png")

        try:
            # 更改选择的城市

            js = "document.querySelector('#sbcx-area-start').options[2].selected = true"
            driver.execute_script(js)
            
            time.sleep(5)

            js2 = "document.querySelector('#sbcx-area-end').options[1].selected = true"
            driver.execute_script(js2)
            time.sleep(5)
        except Exception as e:
            print(e)
            driver.save_screenshot('7.png')
            # 更改选择的城市
            js = "document.querySelector('#sbcx-area-start').options[2].selected = true"
            driver.execute_script(js)
            time.sleep(5)

            js2 = "document.querySelector('#sbcx-area-end').options[1].selected = true"
            driver.execute_script(js2)
            time.sleep(5)



        # 更改完城市后的截屏
        driver.save_screenshot('5.png')
        print("get 5.png")

        # 打开基本养老保险 #############################################################
        next_page = driver.find_element_by_xpath('//li[@class="sbcx-biz-jbyanglao"]')
        next_page.click()

        try:
            dr = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="container"]/div[@style="display: none;"]'))
            )
        except Exception as e:
            logger.error('we cant open the YangLaoBaoXian:', e)



        # 查看是否有基本养老保险相应信息
        main_page = driver.page_source
        response_body = etree.HTML(main_page)
        temp = response_body.xpath('//div[@id="sbcx-result"]/div/center/h4/text()')
        yes_no = "".join(temp)
        num = yes_no.find("无该人员信息")
        if num != -1:
            item["Endowment_insurance"] = "no"
        else:
            # 开始获取基本养老保险信息
            try:
                print("enter_parse")
                item["Endowment_insurance"] = "yes"


                # 确定翻页信息,page_num_n为具体需要翻得页数
                temp = response_body.xpath('//span[@class="pagination-info"]/text()')
                temp_str = "".join(temp)
                temp_nums = re.findall("\d+", temp_str)
                nums = list(map(int, temp_nums))
                # 显示的每一页的数量
                num_1 = nums[1] - nums[0] + 1
                num_2 = nums[4] - nums[3] + 1
                num_3 = nums[7] - nums[6] + 1
                if num_1 == 0:
                    num_1 = 1
                if num_2 == 0:
                    num_2 = 1
                if num_3 == 0:
                    num_3 = 1
                page_1 = divmod(nums[2], num_1)
                page_2 = divmod(nums[5], num_2)
                page_3 = divmod(nums[8], num_3)
                # 获取需要翻页的次数
                page_num_1 = page_num_get(page_1)
                page_num_2 = page_num_get(page_2)
                page_num_3 = page_num_get(page_3)




                temp = response_body.xpath('//td[@data-value="aac003"]/text()')
                Name = "".join(temp)
                item["Name"] = Name.strip()

                temp = response_body.xpath('//td[@data-value="aab004"]/text()')
                Unit_latest = "".join(temp)
                item["Unit_latest"] = Unit_latest.strip()

                # 社会保障号
                temp = response_body.xpath('//td[@data-value="aac002"]/text()')
                Social_security_num = "".join(temp)
                item["Social_security_num"] = Social_security_num.strip()

                # 养老保险参保状态
                temp = response_body.xpath('//td[@data-value="aac008"]/text()')
                Endowment_insurance_status = "".join(temp)
                item["Endowment_insurance_status"] = Endowment_insurance_status.strip()



                # 年度
                item["Annual_individual_account_year"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[1]')

                # 截至上年末个人账户累计储存额
                item["Annual_individual_account_last_year_stores_the_forehead"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[2]')

                # 本年实际缴费月数
                item["Annual_individual_account_actual_payment_months"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[3]')

                # 当年记账金额
                item["Annual_individual_account_amount_charge_account"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[4]')

                # 当年记账利息
                item["Annual_individual_account_interest_charge_account"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[5]')

                # 至本年末账户累计储存额
                item["Annual_individual_account_this_year_stores_the_forehead"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[6]')

                # 至本年末实际缴费月数
                item["Annual_individual_account_this_year_actual_payment_months"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[7]')

                # 在职年度个人账户的翻页
                if page_num_1 > 1:
                    for i in range(page_num_1 - 1):
                        try:
                            # next_page = driver.find_element_by_xpath('？？？')
                            # next_page.click()
                            # page = driver.page_source
                            # response_body = etree.HTML(page)

                            # 年度
                            temp = response_body.xpath(
                                '//table[@id="sbcx-fieldset-2"]//td[1]')
                            item["Annual_individual_account_year"].extend(temp)

                            # 截至上年末个人账户累计储存额
                            temp = response_body.xpath(
                                '//table[@id="sbcx-fieldset-2"]//td[2]')
                            item["Annual_individual_account_last_year_stores_the_forehead"].extend(temp)

                            # 本年实际缴费月数
                            temp = response_body.xpath(
                                '//table[@id="sbcx-fieldset-2"]//td[3]')
                            item["Annual_individual_account_actual_payment_months"].extend(temp)

                            # 当年记账金额
                            temp = response_body.xpath(
                                '//table[@id="sbcx-fieldset-2"]//td[4]')
                            item["Annual_individual_account_amount_charge_account"].extend(temp)

                            # 当年记账利息
                            temp = response_body.xpath(
                                '//table[@id="sbcx-fieldset-2"]//td[5]')
                            item["Annual_individual_account_interest_charge_account"].extend(temp)

                            # 至本年末账户累计储存额
                            temp = response_body.xpath(
                                '//table[@id="sbcx-fieldset-2"]//td[6]')
                            item["Annual_individual_account_this_year_stores_the_forehead"].extend(temp)

                            # 至本年末实际缴费月数
                            temp = response_body.xpath(
                                '//table[@id="sbcx-fieldset-2"]//td[7]')
                            item["Annual_individual_account_this_year_actual_payment_months"].extend(temp)

                        except Exception as e:
                            print(e)


                # 缴费年月
                item["Endowment_individual_pay_years"] = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[1]')

                # 月缴费基数
                item["Endowment_individual_pay_base"] = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[2]')

                # 个人缴费金额
                item["Endowment_individual_pay_amount"] = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[3]')

                # 到账情况
                item["Endowment_individual_pay_to_account"] = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[4]')

                # 个人缴费信息翻页
                if page_num_2 > 1:
                    for i in range(page_num_2 - 1):
                        try:
                            next_page = driver.find_element_by_xpath('//li[@class="page-next"]')
                            next_page.click()
                            time.sleep(2)
                            page = driver.page_source
                            response_body = etree.HTML(page)

                            # 缴费年月
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[1]')
                            item["Endowment_individual_pay_years"].extend(temp)

                            # 月缴费基数
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[2]')
                            item["Endowment_individual_pay_base"].extend(temp)

                            # 个人缴费金额
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[3]')
                            item["Endowment_individual_pay_amount"].extend(temp)

                            # 到账情况
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[4]')
                            item["Endowment_individual_pay_to_account"].extend(temp)

                        except Exception as e:
                            print(e)



            except Exception as e:
                logger.error('we cant get the Endowment_insurance:', e)

        try:
            next_page = driver.find_element_by_xpath('//button[@id="btn-return"]')
            next_page.click()
            time.sleep(5)
        except Exception as e:
            print(e)




        # 打开城乡居民养老保险 #######################################################
        next_page = driver.find_element_by_xpath('//li[@class="sbcx-biz-cxjmyanglao"]')
        next_page.click()

        try:
            dr = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="container"]/div[@style="display: none;"]'))
            )
        except Exception as e:
            logger.error('we cant open the cxjmyanglao:', e)



        # 查看是否有城乡居民养老保险相应信息
        main_page = driver.page_source
        response_body = etree.HTML(main_page)
        temp = response_body.xpath('//div[@id="sbcx-result"]/div/center/h4/text()')
        yes_no = "".join(temp)
        num = yes_no.find("无该人员信息")
        if num != -1:
            item["Urban_rural_endowment_insurance"] = "no"
        else:
            # 开始获取城乡居民养老保险信息
            try:
                print("enter_parse")
                item["Urban_rural_Endowment_insurance"] = "yes"
                # # 确定翻页信息,page_num_n为具体需要翻得页数
                # temp = response_body.xpath('//span[@class="pagination-info"]/text()')
                # temp_str = "".join(temp)
                # temp_nums = re.findall("\d+", temp_str)
                # nums = list(map(int, temp_nums))
                # # 显示的每一页的数量
                # num_1 = nums[1] - nums[0] + 1
                # num_2 = nums[4] - nums[3] + 1
                # num_3 = nums[7] - nums[6] + 1
                # if num_1 == 0:
                #     num_1 = 1
                # elif num_2 == 0:
                #     num_2 = 1
                # elif num_3 == 0:
                #     num_3 = 1
                # page_1 = divmod(nums[2], num_1)
                # page_2 = divmod(nums[5], num_2)
                # page_3 = divmod(nums[8], num_3)
                # # 获取需要翻页的次数
                # page_num_1 = page_num_get(page_1)
                # page_num_2 = page_num_get(page_2)
                # page_num_3 = page_num_get(page_3)
                #
                # temp = response_body.xpath('//td[@data-value="aac003"]/text()')
                # Name = "".join(temp)
                # item["Name"] = Name.strip()
                #
                # temp = response_body.xpath('//td[@data-value="aab004"]/text()')
                # Unit_latest = "".join(temp)
                # item["Unit_latest"] = Unit_latest.strip()
                #
                # # 社会保障号
                # temp = response_body.xpath('//td[@data-value="aac002"]/text()')
                # Social_security_num = "".join(temp)
                # item["Social_security_num"] = Social_security_num.strip()
                #
                # # 养老保险参保状态
                # temp = response_body.xpath('//td[@data-value="aac008"]/text()')
                # Endowment_insurance_status = "".join(temp)
                # item["Endowment_insurance_status"] = Endowment_insurance_status.strip()
                #
                # # 年度
                # item["Annual_individual_account_year"] = response_body.xpath(
                #     '//table[@id="sbcx-fieldset-2"]//td[1]')
                #
                # # 截至上年末个人账户累计储存额
                # item["Annual_individual_account_last_year_stores_the_forehead"] = response_body.xpath(
                #     '//table[@id="sbcx-fieldset-2"]//td[2]')
                #
                # # 本年实际缴费月数
                # item["Annual_individual_account_actual_payment_months"] = response_body.xpath(
                #     '//table[@id="sbcx-fieldset-2"]//td[3]')
                #
                # # 当年记账金额
                # item["Annual_individual_account_amount_charge_account"] = response_body.xpath(
                #     '//table[@id="sbcx-fieldset-2"]//td[4]')
                #
                # # 当年记账利息
                # item["Annual_individual_account_interest_charge_account"] = response_body.xpath(
                #     '//table[@id="sbcx-fieldset-2"]//td[5]')
                #
                # # 至本年末账户累计储存额
                # item["Annual_individual_account_this_year_stores_the_forehead"] = response_body.xpath(
                #     '//table[@id="sbcx-fieldset-2"]//td[6]')
                #
                # # 至本年末实际缴费月数
                # item["Annual_individual_account_this_year_actual_payment_months"] = response_body.xpath(
                #     '//table[@id="sbcx-fieldset-2"]//td[7]')
                #
                # # 在职年度个人账户的翻页
                # if page_num_1 > 1:
                #     for i in range(page_num_1 - 1):
                #         try:
                #             # next_page = driver.find_element_by_xpath('？？？')
                #             # next_page.click()
                #             # page = driver.page_source
                #             # response_body = etree.HTML(page)
                #
                #             # 年度
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[1]')
                #             item["Annual_individual_account_year"].extend(temp)
                #
                #             # 截至上年末个人账户累计储存额
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[2]')
                #             item["Annual_individual_account_last_year_stores_the_forehead"].extend(temp)
                #
                #             # 本年实际缴费月数
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[3]')
                #             item["Annual_individual_account_actual_payment_months"].extend(temp)
                #
                #             # 当年记账金额
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[4]')
                #             item["Annual_individual_account_amount_charge_account"].extend(temp)
                #
                #             # 当年记账利息
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[5]')
                #             item["Annual_individual_account_interest_charge_account"].extend(temp)
                #
                #             # 至本年末账户累计储存额
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[6]')
                #             item["Annual_individual_account_this_year_stores_the_forehead"].extend(temp)
                #
                #             # 至本年末实际缴费月数
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[7]')
                #             item["Annual_individual_account_this_year_actual_payment_months"].extend(temp)
                #
                #         except Exception as e:
                #             print(e)
                #
                # # 缴费年月
                # item["Individual_pay_years"] = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[1]')
                #
                # # 月缴费基数
                # item["Individual_pay_base"] = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[2]')
                #
                # # 个人缴费金额
                # item["Individual_pay_amount"] = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[3]')
                #
                # # 到账情况
                # item["Individual_pay_to_account"] = response_body.xpath(
                #     '//table[@id="sbcx-fieldset-3"]//td[4]')
                #
                # # 个人缴费信息翻页
                # if page_num_2 > 1:
                #     for i in range(page_num_2 - 1):
                #         try:
                #             next_page = driver.find_element_by_xpath('//li[@class="page-next"]')
                #             next_page.click()
                #             time.sleep(2)
                #             page = driver.page_source
                #             response_body = etree.HTML(page)
                #
                #             # 缴费年月
                #             temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[1]')
                #             item["Individual_pay_years"].extend(temp)
                #
                #             # 月缴费基数
                #             temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[2]')
                #             item["Individual_pay_base"].extend(temp)
                #
                #             # 个人缴费金额
                #             temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[3]')
                #             item["Individual_pay_amount"].extend(temp)
                #
                #             # 到账情况
                #             temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[4]')
                #             item["Individual_pay_to_account"].extend(temp)
                #
                #         except Exception as e:
                #             print(e)
                #

            except Exception as e:
                print(e)

        try:
            next_page = driver.find_element_by_xpath('//button[@id="btn-return"]')
            next_page.click()
            time.sleep(5)
        except Exception as e:
            print(e)




        # 打开基本医疗保险 #############################################################################################
        next_page = driver.find_element_by_xpath('//li[@class="sbcx-biz-jbyiliao"]')
        next_page.click()

        try:
            dr = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="container"]/div[@style="display: none;"]'))
            )
        except Exception as e:
            logger.error('we cant open the YangLaoBaoXian:', e)



        # 查看是否有基本医疗保险相应信息
        main_page = driver.page_source
        response_body = etree.HTML(main_page)
        temp = response_body.xpath('//div[@id="sbcx-result"]/div/center/h4/text()')
        yes_no = "".join(temp)
        num = yes_no.find("无该人员信息")
        if num != -1:
            item["Basic_medical_insurance"] = "no"
        else:
            # 开始获取基本养老保险信息
            try:
                print("enter_parse")
                item["Basic_medical_insurance"] = "yes"


                # 确定翻页信息,page_num_n为具体需要翻得页数
                temp = response_body.xpath('//span[@class="pagination-info"]/text()')
                temp_str = "".join(temp)
                temp_nums = re.findall("\d+", temp_str)
                nums = list(map(int, temp_nums))
                # 显示的每一页的数量
                num_1 = nums[1] - nums[0] + 1
                num_2 = nums[4] - nums[3] + 1
                if num_1 == 0:
                    num_1 = 1
                elif num_2 == 0:
                    num_2 = 1
                page_1 = divmod(nums[2], num_1)
                page_2 = divmod(nums[5], num_2)
                # 获取需要翻页的次数
                page_num_1 = page_num_get(page_1)
                page_num_2 = page_num_get(page_2)
                #
                #
                #
                #
                #
                # 基本医疗保险参保状态
                temp = response_body.xpath('//td[@data-value="aac008"]/text()')
                Basic_medical_insurance_status = "".join(temp)
                item["Basic_medical_insurance_status"] = Basic_medical_insurance_status.strip()

                temp = response_body.xpath('//td[@data-value="aac084"]/text()')
                Nature_personnel = "".join(temp)
                item["Nature_personnel"] = Nature_personnel.strip()


                # 基本医疗缴费年月 ##############################
                item["Basic_medical_individual_pay_years"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[1]')

                # 基本医疗月缴费基数
                item["Basic_medical_individual_pay_base"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[2]')

                # 基本医疗个人缴费金额
                item["Basic_medical_individual_pay_amount"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[3]')


                # 基本医疗个人缴费信息翻页
                if page_num_1 > 1:
                    for i in range(page_num_1 - 1):
                        try:
                            next_page = driver.find_element_by_xpath('//li[@class="page-next"]')
                            next_page.click()
                            time.sleep(2)
                            page = driver.page_source
                            response_body = etree.HTML(page)

                            # 缴费年月
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[1]')
                            item["Basic_medical_individual_pay_years"].extend(temp)

                            # 月缴费基数
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[2]')
                            item["Basic_medical_individual_pay_base"].extend(temp)

                            # 个人缴费金额
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[3]')
                            item["Basic_medical_individual_pay_amount"].extend(temp)

                        except Exception as e:
                            print(e)

                # 年度个人医保账户 ##########################
                # 当年账户总额
                temp = response_body.xpath('//td[@data-value="dnzhze"]/text()')
                Basic_medical_annual_personal_medical_all = "".join(temp)
                item["Basic_medical_annual_personal_medical_all"] = Basic_medical_annual_personal_medical_all

                # 历年账户总额
                temp = response_body.xpath('//td[@data-value="lnzhze"]/text()')
                Basic_medical_over_year_personal_medical_all = "".join(temp)
                item["Basic_medical_over_year_personal_medical_all"] = Basic_medical_over_year_personal_medical_all

                # 当年账户支付累计
                temp = response_body.xpath('//td[@data-value="bkc101"]/text()')
                Basic_medical_annual_personal_medical_total_pay = "".join(temp)
                item["Basic_medical_annual_personal_medical_total_pay"] = Basic_medical_annual_personal_medical_total_pay

                # 历年账户支付累计
                temp = response_body.xpath('//td[@data-value="bkc321"]/text()')
                Basic_medical_over_year_personal_medical_total_pay = "".join(temp)
                item["Basic_medical_over_year_personal_medical_total_pay"] = Basic_medical_over_year_personal_medical_total_pay


                # 个人就诊信息 ##############################
                # 结算日期
                item["Basic_medical_settlement_date"] = response_body.xpath(
                    '//table[@id="sbcx-fieldset-4"]//td[1]')

                # 医疗类别
                item["Basic_medical_category"] = response_body.xpath(
                    '//table[@id="sbcx-fieldset-4"]//td[2]')

                # 医疗机构名称
                item["Basic_medical_institutions_name"] = response_body.xpath(
                    '//table[@id="sbcx-fieldset-4"]//td[3]')

                # 总费用
                item["Basic_medical_total_cost"] = response_body.xpath(
                    '//table[@id="sbcx-fieldset-4"]//td[4]')

                # 医保基（资）金支付
                item["Basic_medical_medicare_pay"] = response_body.xpath(
                    '//table[@id="sbcx-fieldset-4"]//td[5]')

                # 现金支付
                item["Basic_medical_cash_pay"] = response_body.xpath(
                    '//table[@id="sbcx-fieldset-4"]//td[6]')

                if page_num_2 > 1:
                    for i in range(page_num_1 - 1):
                        try:
                            next_page = driver.find_element_by_xpath('//li[@class="page-next"]')
                            next_page.click()
                            time.sleep(2)
                            page = driver.page_source
                            response_body = etree.HTML(page)

                            # 结算日期
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-4"]//td[1]')
                            item["Basic_medical_settlement_date"].extend(temp)

                            # 医疗类别
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-4"]//td[2]')
                            item["Basic_medical_category"].extend(temp)

                            # 医疗机构名称
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-4"]//td[3]')
                            item["Basic_medical_institutions_name"].extend(temp)

                            # 总费用
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-4"]//td[4]')
                            item["Basic_medical_total_cost"].extend(temp)

                            # 医保基（资）金支付
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-4"]//td[5]')
                            item["Basic_medical_medicare_pay"].extend(temp)

                            # 现金支付
                            temp = response_body.xpath('//table[@id="sbcx-fieldset-4"]//td[6]')
                            item["Basic_medical_cash_pay"].extend(temp)

                        except Exception as e:
                            print(e)

            except Exception as e:
                logger.error('we cant get the YangLaoBaoXian:', e)

        try:
            next_page = driver.find_element_by_xpath('//button[@id="btn-return"]')
            next_page.click()
            time.sleep(5)
        except Exception as e:
            print(e)


        # 打开城乡居民医疗保险 #############################################################################################
        next_page = driver.find_element_by_xpath('//li[@class="sbcx-biz-cxjmyiliao"]')
        next_page.click()

        try:
            dr = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="container"]/div[@style="display: none;"]'))
            )
        except Exception as e:
            logger.error('we cant open the cxjmyiliao:', e)



        # 查看是否有城乡居民医疗保险相应信息
        main_page = driver.page_source
        response_body = etree.HTML(main_page)
        temp = response_body.xpath('//div[@id="sbcx-result"]/div/center/h4/text()')
        yes_no = "".join(temp)
        num = yes_no.find("无该人员信息")
        if num != -1:
            item["Urban_rural_medical_insurance"] = "no"
        else:
            # 开始获取基本养老保险信息
            try:
                print("enter_parse")
                item["Urban_rural_medical_insurance"] = "yes"


                # # 确定翻页信息,page_num_n为具体需要翻得页数
                # temp = response_body.xpath('//span[@class="pagination-info"]/text()')
                # temp_str = "".join(temp)
                # temp_nums = re.findall("\d+", temp_str)
                # nums = list(map(int, temp_nums))
                # # 显示的每一页的数量
                # num_1 = nums[1] - nums[0] + 1
                # num_2 = nums[4] - nums[3] + 1
                # num_3 = nums[7] - nums[6] + 1
                # if num_1 == 0:
                #     num_1 = 1
                # elif num_2 == 0:
                #     num_2 = 1
                # elif num_3 == 0:
                #     num_3 = 1
                # page_1 = divmod(nums[2], num_1)
                # page_2 = divmod(nums[5], num_2)
                # page_3 = divmod(nums[8], num_3)
                # # 获取需要翻页的次数
                # page_num_1 = page_num_get(page_1)
                # page_num_2 = page_num_get(page_2)
                # page_num_3 = page_num_get(page_3)
                #
                #
                #
                #
                # temp = response_body.xpath('//td[@data-value="aac003"]/text()')
                # Name = "".join(temp)
                # item["Name"] = Name.strip()
                #
                # temp = response_body.xpath('//td[@data-value="aab004"]/text()')
                # Unit_latest = "".join(temp)
                # item["Unit_latest"] = Unit_latest.strip()
                #
                # # 社会保障号
                # temp = response_body.xpath('//td[@data-value="aac002"]/text()')
                # Social_security_num = "".join(temp)
                # item["Social_security_num"] = Social_security_num.strip()
                #
                # # 养老保险参保状态
                # temp = response_body.xpath('//td[@data-value="aac008"]/text()')
                # Endowment_insurance_status = "".join(temp)
                # item["Endowment_insurance_status"] = Endowment_insurance_status.strip()
                #
                #
                #
                # # 年度
                # item["Annual_individual_account_year"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[1]')
                #
                # # 截至上年末个人账户累计储存额
                # item["Annual_individual_account_last_year_stores_the_forehead"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[2]')
                #
                # # 本年实际缴费月数
                # item["Annual_individual_account_actual_payment_months"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[3]')
                #
                # # 当年记账金额
                # item["Annual_individual_account_amount_charge_account"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[4]')
                #
                # # 当年记账利息
                # item["Annual_individual_account_interest_charge_account"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[5]')
                #
                # # 至本年末账户累计储存额
                # item["Annual_individual_account_this_year_stores_the_forehead"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[6]')
                #
                # # 至本年末实际缴费月数
                # item["Annual_individual_account_this_year_actual_payment_months"] = response_body.xpath('//table[@id="sbcx-fieldset-2"]//td[7]')
                #
                # # 在职年度个人账户的翻页
                # if page_num_1 > 1:
                #     for i in range(page_num_1 - 1):
                #         try:
                #             # next_page = driver.find_element_by_xpath('？？？')
                #             # next_page.click()
                #             # page = driver.page_source
                #             # response_body = etree.HTML(page)
                #
                #             # 年度
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[1]')
                #             item["Annual_individual_account_year"].extend(temp)
                #
                #             # 截至上年末个人账户累计储存额
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[2]')
                #             item["Annual_individual_account_last_year_stores_the_forehead"].extend(temp)
                #
                #             # 本年实际缴费月数
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[3]')
                #             item["Annual_individual_account_actual_payment_months"].extend(temp)
                #
                #             # 当年记账金额
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[4]')
                #             item["Annual_individual_account_amount_charge_account"].extend(temp)
                #
                #             # 当年记账利息
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[5]')
                #             item["Annual_individual_account_interest_charge_account"].extend(temp)
                #
                #             # 至本年末账户累计储存额
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[6]')
                #             item["Annual_individual_account_this_year_stores_the_forehead"].extend(temp)
                #
                #             # 至本年末实际缴费月数
                #             temp = response_body.xpath(
                #                 '//table[@id="sbcx-fieldset-2"]//td[7]')
                #             item["Annual_individual_account_this_year_actual_payment_months"].extend(temp)
                #
                #         except Exception as e:
                #             print(e)
                #
                #
                # # 缴费年月
                # item["Individual_pay_years"] = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[1]')
                #
                # # 月缴费基数
                # item["Individual_pay_base"] = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[2]')
                #
                # # 个人缴费金额
                # item["Individual_pay_amount"] = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[3]')
                #
                # # 到账情况
                # item["Individual_pay_to_account"] = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[4]')
                #
                # # 个人缴费信息翻页
                # if page_num_2 > 1:
                #     for i in range(page_num_2 - 1):
                #         try:
                #             next_page = driver.find_element_by_xpath('//li[@class="page-next"]')
                #             next_page.click()
                #             time.sleep(2)
                #             page = driver.page_source
                #             response_body = etree.HTML(page)
                #
                #             # 缴费年月
                #             temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[1]')
                #             item["Individual_pay_years"].extend(temp)
                #
                #             # 月缴费基数
                #             temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[2]')
                #             item["Individual_pay_base"].extend(temp)
                #
                #             # 个人缴费金额
                #             temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[3]')
                #             item["Individual_pay_amount"].extend(temp)
                #
                #             # 到账情况
                #             temp = response_body.xpath('//table[@id="sbcx-fieldset-3"]//td[4]')
                #             item["Individual_pay_to_account"].extend(temp)
                #
                #         except Exception as e:
                #             print(e)
                #


            except Exception as e:
                logger.error('we cant get the YangLaoBaoXian:', e)

        try:
            next_page = driver.find_element_by_xpath('//button[@id="btn-return"]')
            next_page.click()
            time.sleep(5)
        except Exception as e:
            print(e)



        # 打开工伤保险 #############################################################################################
        next_page = driver.find_element_by_xpath('//li[@class="sbcx-biz-gongshang"]')
        next_page.click()

        try:
            dr = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="container"]/div[@style="display: none;"]'))
            )
        except Exception as e:
            logger.error('we cant open the gongshang:', e)



        # 查看是否有工伤保险相应信息
        main_page = driver.page_source
        response_body = etree.HTML(main_page)
        temp = response_body.xpath('//div[@id="sbcx-result"]/div/center/h4/text()')
        yes_no = "".join(temp)
        num = yes_no.find("无该人员信息")
        if num != -1:
            item["Inductrial_injury_insurance"] = "no"
        else:
            # 开始获取工伤保险信息
            try:
                print("enter_parse")
                item["Inductrial_injury_insurance"] = "yes"


                # 确定翻页信息,page_num_n为具体需要翻得页数
                temp = response_body.xpath('//span[@class="pagination-info"]/text()')
                temp_str = "".join(temp)
                temp_nums = re.findall("\d+", temp_str)
                nums = list(map(int, temp_nums))
                # 显示的每一页的数量
                num_1 = nums[1] - nums[0] + 1
                if num_1 == 0:
                    num_1 = 1
                page_1 = divmod(nums[2], num_1)
                # 获取需要翻页的次数
                page_num_1 = page_num_get(page_1)



                # 参保缴费单位列表
                temp = response_body.xpath('//tr[@data-index="0"]/td[1]/text()')
                Inductrial_injury_units = "".join(temp)
                item["Inductrial_injury_units"] = Inductrial_injury_units

                # 参保状态
                temp = response_body.xpath('//tr[@data-index="0"]/td[2]/text()')
                Inductrial_injury_state = "".join(temp)
                item["Inductrial_injury_state"] = Inductrial_injury_state


                # 参保缴费单位翻页
                if page_num_1 > 1:
                    for i in range(page_num_1 - 1):
                        try:
                            next_page = driver.find_element_by_xpath('//li[@class="page-next"]')
                            next_page.click()
                            time.sleep(2)
                            page = driver.page_source
                            response_body = etree.HTML(page)

                            # 参保缴费单位列表
                            temp = response_body.xpath('//tr[@data-index="0"]/td[1]/text()')
                            item["Inductrial_injury_units"].extend(temp)

                            # 参保缴费单位列表
                            temp = response_body.xpath('//tr[@data-index="0"]/td[2]/text()')
                            item["Inductrial_injury_state"].extend(temp)

                        except Exception as e:
                            print(e)



            except Exception as e:
                logger.error('we cant get the gong shang bao xian:', e)

        try:
            next_page = driver.find_element_by_xpath('//button[@id="btn-return"]')
            next_page.click()
            time.sleep(5)
        except Exception as e:
            print(e)



        # 打开生育保险 #############################################################################################
        next_page = driver.find_element_by_xpath('//li[@class="sbcx-biz-shengyu"]')
        next_page.click()

        try:
            dr = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="container"]/div[@style="display: none;"]'))
            )
        except Exception as e:
            logger.error('we cant open the gongshang:', e)

        # 查看是否有生育保险信息
        main_page = driver.page_source
        response_body = etree.HTML(main_page)
        temp = response_body.xpath('//div[@id="sbcx-result"]/div/center/h4/text()')
        yes_no = "".join(temp)
        num = yes_no.find("无该人员信息")
        if num != -1:
            item["Birth_insurance"] = "no"
        else:
            # 开始获取生育保险信息
            try:
                print("enter_parse")
                item["Birth_insurance"] = "yes"

                # 生育保险参保状态
                temp = response_body.xpath('//td[@data-value="aac008"]/text()')
                Birth_insurance_state = "".join(temp)
                item["Birth_insurance_state"] = Birth_insurance_state



            except Exception as e:
                logger.error('we cant get the gong shang bao xian:', e)

        try:
            next_page = driver.find_element_by_xpath('//button[@id="btn-return"]')
            next_page.click()
            time.sleep(5)
        except Exception as e:
            print(e)


        # 打开失业保险 #############################################################################################
        next_page = driver.find_element_by_xpath('//li[@class="sbcx-biz-shiye"]')
        next_page.click()

        try:
            dr = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="container"]/div[@style="display: none;"]'))
            )
        except Exception as e:
            logger.error('we cant open the unemployment insurance:', e)

        # 查看是否有失业保险信息
        main_page = driver.page_source
        response_body = etree.HTML(main_page)
        temp = response_body.xpath('//div[@id="sbcx-result"]/div/center/h4/text()')
        yes_no = "".join(temp)
        num = yes_no.find("无该人员信息")
        if num != -1:
            item["Unemployment_insurance"] = "no"
        else:
            # 开始获取失业保险信息
            try:
                print("enter_parse")
                item["Unemployment_insurance"] = "yes"

                # 失业保险参保状态
                temp = response_body.xpath('//td[@data-value="aac008"]/text()')
                Unemployment_insurance_state = "".join(temp)
                item["Unemployment_insurance_state"] = Unemployment_insurance_state



            except Exception as e:
                logger.error('we cant get the gong shang bao xian:', e)

        try:
            next_page = driver.find_element_by_xpath('//button[@id="btn-return"]')
            next_page.click()
            time.sleep(5)
        except Exception as e:
            print(e)



        # 打开机关事业养老保险 #############################################################################################
        next_page = driver.find_element_by_xpath('//li[@class="sbcx-biz-jgjbyanglao"]')
        next_page.click()

        try:
            dr = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="container"]/div[@style="display: none;"]'))
            )
        except Exception as e:
            logger.error('we cant open the Office_facilities_endowment_insurance:', e)

        # 查看是否有机关事业养老保险信息
        main_page = driver.page_source
        response_body = etree.HTML(main_page)
        temp = response_body.xpath('//div[@id="sbcx-result"]/div/center/h4/text()')
        yes_no = "".join(temp)
        num = yes_no.find("无该人员信息")
        if num != -1:
            item["Office_facilities_endowment_insurance"] = "no"
        else:
            # 开始获取机关事业养老保险信息
            try:
                print("enter_parse")
                item["Office_facilities_endowment_insurance"] = "yes"




            except Exception as e:
                logger.error('we cant get the gong shang bao xian:', e)


        try:
            next_page = driver.find_element_by_xpath('//button[@id="btn-return"]')
            next_page.click()
            time.sleep(5)
        except Exception as e:
            print(e)


        driver.quit()


        yield item








