# -*- coding: utf-8 -*-
import json, md5, requests, clean
from conf import config
from datetime import datetime
from pony.orm import *
from model.models import *
from tool import utils
from tool.utils import *

class Pylzh_Process(object):
    def __init__(self):
        self.build_url = utils.Build_Url()
        self.format_str = utils.Format_Str()

    def request_data(self, json_data):
        param_dict = json.loads(json_data)
        request_url = self.build_url.request_url(param_dict)
        self.request_time = None
        self.parse_time = None
        try:
            request_start = datetime.now()
            response = requests.get(request_url, verify=False)
            request_end = datetime.now()
            all_data = json.loads(response.text)
            self.order_id = all_data.get('orderId', '')
            self.order_id = param_dict.get('orderId', '')
            self.cert_no = '51152119902022322'
            self.bank_card_no = '621123812839123912'
            self.name = u'张三'
            self.time_now = datetime.now()
            self.request_time = request_end - request_start
            print '$$$$',self.request_time
        except Exception, e:
            raise e
        data = all_data.get('data')
        result = data.get('result', {})
        quota = result.get('quota', {})
        quota = clean.data
        if quota:
            try:
                parse_start = datetime.now()
                self.format_str.clean_na(quota)
                self.save_base_statistic_info(quota)
                self.save_month_consume(quota)
                self.save_live_city(quota)
                self.save_mcc_consume(quota)
                self.save_high_freq_mar(quota)
                self.save_top_money_mar(quota)
                self.save_consume_city_times(quota)
                parse_end = datetime.now()
                self.parse_time = parse_end - parse_start
                self.save_info(all_data)
                print self.parse_time
            except Exception, e:
                raise e
        return 'ylzh请求成功'

    @db_session
    def save_info(self, all_data):
        REQUEST_INFO(
            orderId = self.order_id, 
            resCode = all_data.get('resCode', ''),
            resMsg = all_data.get('resMsg', ''),
            statCode = all_data.get('statCode', ''),
            statMsg = all_data.get('statMsg', ''),
            smartOrderId = all_data.get('smartOrderId', ''),
            sign = all_data.get('sign', ''),
            request_time = self.request_time,
            parse_time = self.parse_time,
            create_time = self.time_now,
        )

    @db_session
    def save_base_statistic_info(self, quota):
        BN_BASE_STATISTIC_INFO(
            orderId = self.order_id,
            cert_no = self.cert_no,
            bank_card_no = self.bank_card_no,
            name = self.name,
            card_type = quota.get('S0466', ''),
            card_grade = quota.get('S0467', ''),
            line_consume_amt = try_float(quota.get('S0057')),
            line_consume_times = try_int(quota.get('S0060', '')),
            lastest_consume_date = exact_to_day(quota.get('S0135', '')),
            dif_city_consume_1h = try_int(quota.get('S0305', '')),
            receive_to_transfer_per = percent_to_float(quota.get('S0314', '')),
            receive_to_draw_per = percent_to_float(quota.get('S0317', '')),
            fir_deal_date = exact_to_day(quota.get('S0506', '')),
            deal_days = try_int(quota.get('S0513','')),
            deal_grade_in_city = percent_to_float(quota.get('S0563', '')),
            work_consume_times_per = percent_to_float(quota.get('S0656', '')),
            create_time=self.time_now,
        )

    @db_session
    def save_month_consume(self, quota):
        work_consume_amt_dict = parse_to_dict(quota.get('S0520', ''))
        deal_consume_amt_dict = parse_to_dict(quota.get('S0534', ''))
        deal_consume_times_dict = parse_to_dict(quota.get('S0537', ''))
        deal_bank_amt_dict = parse_to_dict(quota.get('S0535', ''))
        deal_bank_times_dict = parse_to_dict(quota.get('S0538', ''))
        keys = work_consume_amt_dict.keys()
        keys.sort(reverse=True)
        for key in keys:
            work_consume_amt = work_consume_amt_dict.get(key)
            deal_consume_amt = deal_consume_amt_dict.get(key)
            deal_consume_times = deal_consume_times_dict.get(key)
            deal_bank_amt = deal_bank_amt_dict.get(key)
            deal_bank_times = deal_bank_times_dict.get(key)
            BN_MONTH_CONSUME(
                orderId = self.order_id,
                cert_no = self.cert_no,
                bank_card_no = self.bank_card_no,
                name = self.name,
                month = exact_to_month('20'+key),
                work_consume_amt = work_consume_amt,
                deal_consume_amt = deal_consume_amt,
                deal_consume_times = deal_consume_times,
                deal_bank_amt = deal_bank_amt,
                deal_bank_times = deal_bank_times,
                create_time = self.time_now,
            )

    @db_session
    def save_live_city(self, quota):
        citys = quota.get('S0503', '').split(';')
        BN_LIVE_CITY(
            orderId = self.order_id,
            cert_no = self.cert_no,
            bank_card_no = self.bank_card_no,
            name = self.name,
            province = citys[0],
            city1 = citys[1],
            city2 = citys[2],
            city3 = citys[3],
            city4 = citys[4],
            city5 = citys[5],
            create_time = self.time_now,
        )

    @db_session
    def save_mcc_consume(self, quota):
        night_consume_amt_dict = parse_to_dict(quota.get('S0640', ''))
        night_consume_times_dict = parse_to_dict(quota.get('S0641', ''))
        consume_amt_dict = parse_to_dict(quota.get('S0647', ''))
        consume_times_dict = parse_to_dict(quota.get('S0649', ''))
        mccs = []
        mccs.extend(night_consume_times_dict)
        mccs.extend(night_consume_times_dict)
        mccs.extend(consume_amt_dict)
        mccs.extend(consume_times_dict)
        mccs = list(set(mccs))
        for mcc in mccs:
            BN_MCC_CONSUME(
                orderId = self.order_id,
                cert_no = self.cert_no,
                bank_card_no = self.bank_card_no,
                name = self.name,
                mcc_code = mcc,
                night_consume_amt = night_consume_amt_dict.get(mcc),
                night_consume_times = night_consume_times_dict.get(mcc),
                consume_amt = consume_amt_dict.get(mcc),
                consume_times = consume_times_dict.get(mcc),
                create_time = self.time_now,
            )

    @db_session
    def save_high_freq_mar(self, quota):
        data = quota.get('S0149', '')
        if data:
            company_list = data.split(';')
            for em in company_list:
                result = re.search(r'([\D\d]*)_(\d+%)', em)
                if result:
                    company = result.group(1)
                    percent = result.group(2)
                    BN_HIGH_FREQ_MAR(
                        orderId = self.order_id,
                        cert_no = self.cert_no,
                        bank_card_no = self.bank_card_no,
                        name = self.name,
                        mar_name = company,
                        consume_per = percent_to_float(percent),
                        create_time = self.time_now,
                    )
    @db_session
    def save_top_money_mar(self, quota):
        data = quota.get('S0613', '')
        mars = data.split(';')
        for mar in mars:
            if mar:
                BN_TOP_MONEY_MAR(
                    orderId = self.order_id,
                    cert_no = self.cert_no,
                    bank_card_no = self.bank_card_no,
                    name = self.name,
                    top5_consume_amt_mar = mar,
                    create_time = self.time_now,
                )

    @db_session
    def save_consume_city_times(self, quota):
        data = quota.get('S0581', '')
        data_list = data.split(';')
        for em in data_list:
            result = re.search(r'(\d+)_(\d+)', em)
            if result:
                city_code = result.group(1)
                consume_times = result.group(2)
                BN_CONSUME_CITY_TIMES(
                    orderId = self.order_id,
                    cert_no = self.cert_no,
                    bank_card_no = self.bank_card_no,
                    name = self.name,
                    city_code = city_code,
                    consume_times = consume_times,
                    create_time = self.time_now,
                )
