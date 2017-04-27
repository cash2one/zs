# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HangzhouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 基本信息
    # 姓名
    Name = scrapy.Field()
    # 身份证号
    Id_number = scrapy.Field()
    # 城市
    City = scrapy.Field()
    # 当前所在公司
    Unit_latest = scrapy.Field()
    # 社会保障号
    Social_security_num = scrapy.Field()
    # 更新时间
    Date_time = scrapy.Field()


    # 养老保险 ##########################################################################################################
    # 养老保险是否存在
    Endowment_insurance = scrapy.Field()
    # 养老保险参保状态
    Endowment_insurance_status = scrapy.Field()


    # 年度
    Annual_individual_account_year = scrapy.Field()
    # 截至上年末个人账户累计储存额
    Annual_individual_account_last_year_stores_the_forehead = scrapy.Field()
    # 本年实际缴费月数
    Annual_individual_account_actual_payment_months = scrapy.Field()
    # 当年记账金额
    Annual_individual_account_amount_charge_account = scrapy.Field()
    # 当年记账利息
    Annual_individual_account_interest_charge_account = scrapy.Field()
    # 至本年末账户累计储存额
    Annual_individual_account_this_year_stores_the_forehead = scrapy.Field()
    # 至本年末实际缴费月数
    Annual_individual_account_this_year_actual_payment_months = scrapy.Field()

    # 个人缴费信息
    # 缴费年月
    Endowment_individual_pay_years = scrapy.Field()
    # 月缴费基数
    Endowment_individual_pay_base = scrapy.Field()
    # 个人缴费金额
    Endowment_individual_pay_amount = scrapy.Field()
    # 到账情况
    Endowment_individual_pay_to_account = scrapy.Field()


    # 城乡居民养老保险 ##################################################################################################
    # 城乡居民养老保险是否存在
    Urban_rural_endowment_insurance = scrapy.Field()


    # 基本医疗保险 ######################################################################################################
    # 基本医疗保险是否存在
    Basic_medical_insurance = scrapy.Field()
    # 基本医疗保险参保状态
    Basic_medical_insurance_status = scrapy.Field()
    # 人员性质(是否在职)
    Nature_personnel = scrapy.Field()

    # 个人缴费信息(近两年) ##############################
    # 缴费年月
    Basic_medical_individual_pay_years = scrapy.Field()
    # 月缴费基数
    Basic_medical_individual_pay_base = scrapy.Field()
    # 个人缴费金额
    Basic_medical_individual_pay_amount = scrapy.Field()

    # 当年账户总额
    Basic_medical_annual_personal_medical_all = scrapy.Field()
    # 历年账户总额
    Basic_medical_over_year_personal_medical_all = scrapy.Field()
    # 当年账户支付累计
    Basic_medical_annual_personal_medical_total_pay = scrapy.Field()
    # 历年账户支付累计
    Basic_medical_over_year_personal_medical_total_pay = scrapy.Field()

    # 个人就诊信息 ##############################
    # 结算日期
    Basic_medical_settlement_date = scrapy.Field()
    # 医疗类别
    Basic_medical_category = scrapy.Field()
    # 医疗机构名称
    Basic_medical_institutions_name = scrapy.Field()
    # 总费用
    Basic_medical_total_cost = scrapy.Field()
    # 医保基（资）金支付
    Basic_medical_medicare_pay = scrapy.Field()
    # 现金支付
    Basic_medical_cash_pay = scrapy.Field()


    # 城乡居民医疗保险 ######################################################################################################
    # 城乡医疗保险是否存在
    Urban_rural_medical_insurance = scrapy.Field()

    # 工商保险 ############################################################################################################
    # 工商保险是否存在
    Inductrial_injury_insurance = scrapy.Field()
    # 参保缴费单位列表
    Inductrial_injury_units = scrapy.Field()
    # 工商保险参保状态
    Inductrial_injury_state = scrapy.Field()



    # 生育保险 ###########################################################################################################
    # 生育保险是否存在
    Birth_insurance = scrapy.Field()
    #生育保险参保状态
    Birth_insurance_state = scrapy.Field()

    # 失业保险 ###########################################################################################################
    # 失业保险是否存在
    Unemployment_insurance = scrapy.Field()
    # 失业保险参保状态
    Unemployment_insurance_state = scrapy.Field()


    # 机关事业养老保险 ###########################################################################################################
    # 机关事业养老保险是否存在
    Office_facilities_endowment_insurance = scrapy.Field()

















