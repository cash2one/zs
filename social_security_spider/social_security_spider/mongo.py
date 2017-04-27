from pymongo import MongoClient
from bson.objectid import ObjectId
Client = MongoClient()

db = Client.social_security

def lxml_obj_to_str(obj):
    info_list = []
    for i in obj:
        info_list.append(i.text)
    return info_list


def mongo_save(postitem):
    collection = db.basic_info
    print(type(postitem))
    basic_info = {
        # 名字
        "name": postitem.get("Name", ""),
        # 身份证号
        "id_number": postitem.get("Id_number", ""),
        # 社会保障号
        "social_security_num": postitem.get("Social_security_num", ""),
        # 当前所在公司
        "unit_latest": postitem.get("Unit_latest", ""),
        # 更新时间
        "date_time": postitem.get("Date_time", ""),
    }
    person_id = collection.update({"id_number": postitem.get("Id_number", "")}, basic_info, True)

    if person_id.get("upserted") is None:
        info = collection.find_one({"id_number": postitem.get("Id_number", "")})
        update_key = ObjectId(info.get("_id", ""))
    else:
        update_key = ObjectId(person_id.get("upserted", ""))

    # 基本养老保险 #######################################################################################################
    # 基本养老保险-在职参保人员基础信息
    collection = db.endowment_insurance
    endowment_insurance = {
        # 养老保险是否存在
        "endowment_insurance": postitem.get("Endowment_insurance", ""),
        # 养老保险参保状态
        "endowment_insurance_status": postitem.get("Endowment_insurance_status", ""),
        # 和basic_info建立联系
        "give_endowment_insurance_to_basic_info_id": update_key,
    }
    collection.update({"give_endowment_insurance_to_basic_info_id": update_key}, endowment_insurance, True)

    # 基本养老保险-在职年度个人账户
    collection = db.annual_individual_account
    Annual_individual_account_this_year_actual_payment_months_num = lxml_obj_to_str(postitem.get("Annual_individual_account_this_year_actual_payment_months", ""))
    for i in range(len(Annual_individual_account_this_year_actual_payment_months_num)):
        annual_individual_account = {
            # 年度
            "annual_individual_account_year": lxml_obj_to_str(postitem.get("Annual_individual_account_year", ""))[i],
            # 截至上年末个人账户累计储存额
            "annual_individual_account_last_year_stores_the_forehead": lxml_obj_to_str(postitem.get("Annual_individual_account_last_year_stores_the_forehead", ""))[i],
            # 本年实际缴费月数
            "annual_individual_account_actual_payment_months": lxml_obj_to_str(postitem.get("Annual_individual_account_actual_payment_months", ""))[i],
            # 当年记账金额
            "annual_individual_account_amount_charge_account": lxml_obj_to_str(postitem.get("Annual_individual_account_amount_charge_account", ""))[i],
            # 当年记账利息
            "annual_individual_account_interest_charge_account": lxml_obj_to_str(postitem.get("Annual_individual_account_interest_charge_account", ""))[i],
            # 至本年末账户累计储存额
            "annual_individual_account_this_year_stores_the_forehead": lxml_obj_to_str(postitem.get("Annual_individual_account_this_year_stores_the_forehead", ""))[i],
            # 至本年末实际缴费月数
            "annual_individual_account_this_year_actual_payment_months": lxml_obj_to_str(postitem.get("Annual_individual_account_this_year_actual_payment_months", ""))[i],
            # 和basic_info建立联系
            "give_annual_individual_account_to_basic_info_id": update_key,
        }
        collection.update({"give_annual_individual_account_to_basic_info_id": update_key, "annual_individual_account_year": lxml_obj_to_str(postitem.get("Annual_individual_account_year", ""))[i]}, annual_individual_account, True)

    # 基本养老保险-个人缴费信息（近2年）
    collection = db.individual_pay_info
    endowment_individual_pay_to_account_num = lxml_obj_to_str(postitem.get("Endowment_individual_pay_to_account", ""))
    for i in range(len(endowment_individual_pay_to_account_num)):
        endowment_individual_pay_info = {
            # 基本养老保险缴费年月
            "endowment_individual_pay_years": lxml_obj_to_str(postitem.get("Endowment_individual_pay_years", ""))[i],
            # 基本养老保险月缴费基数
            "endowment_individual_pay_base": lxml_obj_to_str(postitem.get("Endowment_individual_pay_base", ""))[i],
            # 基本养老保险个人缴费金额
            "endowment_individual_pay_amount": lxml_obj_to_str(postitem.get("Endowment_individual_pay_amount", ""))[i],
            # 基本养老保险到账情况
            "endowment_individual_pay_to_account": lxml_obj_to_str(postitem.get("Endowment_individual_pay_to_account", ""))[i],
            # 基本养老保险和basic_info建立联系
            "give_endowment_individual_pay_info_to_basic_info_id": update_key,
        }
        collection.update({"give_endowment_individual_pay_info_to_basic_info_id": update_key, "endowment_individual_pay_years": lxml_obj_to_str(postitem.get("Endowment_individual_pay_years", ""))[i]}, endowment_individual_pay_info, True)


    # 城乡居民养老保险 ###################################################################################################
    collection = db.urban_rural_endowment_insurance
    urban_rural_endowment_insurance = {
        # 城市居民养老保险是否存在
        "urban_rural_endowment_insurance": postitem.get("Urban_rural_endowment_insurance", ""),
        # 和basic_info建立联系
        "give_urban_rural_endowment_to_basic_info_id": update_key,
    }
    collection.update({"give_urban_rural_endowment_to_basic_info_id": update_key}, urban_rural_endowment_insurance, True)


    # 基本医疗保险 #######################################################################################################
    collection = db.basic_medical_insurance
    basic_medical_insurance = {
        # 基本医疗保险是否存在
        "basic_medical_insurance": postitem.get("Basic_medical_insurance", ""),
        # 基本医疗保险参保状态
        "basic_medical_insurance_status": postitem.get("Basic_medical_insurance_status", ""),
        # 人员性质(是否在职)
        "nature_personnel": postitem.get("Nature_personnel", ""),
        # 和basic_info建立联系
        "give_basic_medical_insurance_to_basic_info_id": update_key,
    }
    collection.update({"give_basic_medical_insurance_to_basic_info_id": update_key}, basic_medical_insurance, True)


    # 基本医疗保险个人缴费信息
    collection = db.basic_medical_individual_pay_info
    basic_medical_individual_pay_amount_num = lxml_obj_to_str(postitem.get("Basic_medical_individual_pay_amount", ""))
    for i in range(len(basic_medical_individual_pay_amount_num)):
        basic_medical_individual_pay_info = {
            # 个人缴费信息(近两年)
            # 缴费年月
            "basic_medical_individual_pay_years": lxml_obj_to_str(postitem.get("Basic_medical_individual_pay_years", ""))[i],
            # 月缴费基数
            "basic_medical_individual_pay_base": lxml_obj_to_str(postitem.get("Basic_medical_individual_pay_base", ""))[i],
            # 个人缴费金额
            "basic_medical_individual_pay_amount": lxml_obj_to_str(postitem.get("Basic_medical_individual_pay_amount", ""))[i],
            # 基本医疗保险和basic_info建立联系
            "give_basic_medical_individual_pay_info_to_basic_info_id": update_key,
        }
        collection.update({"give_basic_medical_individual_pay_info_to_basic_info_id": update_key, "basic_medical_individual_pay_years":lxml_obj_to_str(postitem.get("Basic_medical_individual_pay_years", ""))[i]}, basic_medical_individual_pay_info, True)

    # 年度个人医保账户
    collection = db.basic_medical_annual_personal_medical
    basic_medical_annual_personal_medical = {
        # 当年账户总额
        "basic_medical_annual_personal_medical_all": postitem.get("Basic_medical_annual_personal_medical_all", ""),
        # 历年账户总额
        "basic_medical_over_year_personal_medical_all": postitem.get("Basic_medical_over_year_personal_medical_all", ""),
        # 当年账户支付累计
        "basic_medical_annual_personal_medical_total_pay": postitem.get("Basic_medical_annual_personal_medical_total_pay", ""),
        # 历年账户支付累计
        "basic_medical_over_year_personal_medical_total_pay": postitem.get("Basic_medical_over_year_personal_medical_total_pay", ""),
        # 和basic_info建立联系
        "give_basic_medical_annual_personal_medical_to_basic_info_id": update_key,
    }
    collection.update({"give_basic_medical_annual_personal_medical_to_basic_info_id": update_key}, basic_medical_annual_personal_medical, True)

    # 个人就诊信息
    collection = db.basic_medical_personal_medical_information
    basic_medical_cash_pay_num = lxml_obj_to_str(postitem.get("basic_medical_cash_pay", ""))
    for i in range(len(basic_medical_cash_pay_num)):
        basic_medical_personal_medical_information = {
            # 结算日期
            "basic_medical_settlement_date": lxml_obj_to_str(postitem.get("Basic_medical_settlement_date", ""))[i],
            # 医疗类别
            "basic_medical_category": lxml_obj_to_str(postitem.get("Basic_medical_category", ""))[i],
            # 医疗机构名称
            "basic_medical_institutions_name": lxml_obj_to_str(postitem.get("Basic_medical_institutions_name", ""))[i],
            # 总费用
            "basic_medical_total_cost": lxml_obj_to_str(postitem.get("Basic_medical_total_cost", ""))[i],
            # 医保基（资）金支付
            "basic_medical_medicare_pay": lxml_obj_to_str(postitem.get("Basic_medical_medicare_pay", ""))[i],
            # 现金支付
            "basic_medical_cash_pay": lxml_obj_to_str(postitem.get("Basic_medical_cash_pay", ""))[i],
            # 个人就诊信息和basic_info建立联系
            "give_basic_medical_personal_medical_information_to_basic_info_id": update_key,
        }
        collection.update({"give_basic_medical_personal_medical_information_to_basic_info_id": update_key, "basic_medical_settlement_date":lxml_obj_to_str(postitem.get("Basic_medical_settlement_date", ""))[i]}, basic_medical_personal_medical_information, True)




    # 城乡居民医疗保险 #######################################################################################################
    collection = db.urban_rural_medical_insurance
    urban_rural_medical_insurance = {
        # 城乡医疗保险是否存在
        "urban_rural_medical_insurance": postitem.get("Urban_rural_medical_insurance", ""),
        # 和basic_info建立联系
        "give_urban_rural_medical_to_basic_info_id": update_key,
    }
    collection.update({"give_urban_rural_medical_to_basic_info_id": update_key}, urban_rural_medical_insurance, True)


    # 工商保险 #######################################################################################################
    collection = db.inductrial_injury_insurance
    inductrial_injury_insurance = {
        # 工商保险是否存在
        "inductrial_injury_insurance": postitem.get("Inductrial_injury_insurance", ""),
        # 参保缴费单位列表
        "inductrial_injury_units": postitem.get("Inductrial_injury_units", ""),
        # 工商保险参保状态
        "inductrial_injury_state": postitem.get("Inductrial_injury_state", ""),
        # 和basic_info建立联系
        "give_inductrial_injury_to_basic_info_id": update_key,
    }
    collection.update({"give_inductrial_injury_to_basic_info_id": update_key}, inductrial_injury_insurance, True)


    # 生育保险 #######################################################################################################
    collection = db.birth_insurance
    birth_insurance = {
        # 生育保险是否存在
        "birth_insurance": postitem.get("Birth_insurance", ""),
        # 生育保险参保状态
        "birth_insurance_state": postitem.get("Birth_insurance_state", ""),
        # 和basic_info建立联系
        "give_birth_insurance_to_basic_info_id": update_key,
    }
    collection.update({"give_birth_insurance_to_basic_info_id": update_key}, birth_insurance, True)


    # 失业保险 #######################################################################################################
    collection = db.unemployment_insurance
    unemployment_insurance = {
        # 失业保险是否存在
        "unemployment_insurance": postitem.get("Unemployment_insurance", ""),
        # 失业保险参保状态
        "unemployment_insurance_state": postitem.get("Unemployment_insurance_state", ""),
        # 和basic_info建立联系
        "give_unemployment_insurance_to_basic_info_id": update_key,
    }
    collection.update({"give_unemployment_insurance_to_basic_info_id": update_key}, unemployment_insurance, True)


    # 机关事业养老保险 ####################################################################################################
    collection = db.office_facilities_endowment_insurance
    office_facilities_endowment_insurance = {
        # 失业保险是否存在
        "office_facilities_endowment_insurance": postitem.get("Office_facilities_endowment_insurance", ""),
        # 和basic_info建立联系
        "give_office_facilities_endowment_to_basic_info_id": update_key,
    }
    collection.update({"give_office_facilities_endowment_to_basic_info_id": update_key}, office_facilities_endowment_insurance, True)
