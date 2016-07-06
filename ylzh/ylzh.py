# -*- coding: utf-8 -*-
import json, md5, requests, datetime, clean
from conf import config
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
        try:
            response = requests.get(request_url, verify=False)
            all_data = json.loads(response.text)
            self.order_id = all_data.get('orderId', '')
            self.cert_no = '51152119902022322'
            self.bank_card_no = '621123812839123912'
            self.name = u'张三'
            self.now_time = datetime.now() 
            #self.save_info(all_data)
        except Exception, e:
            return e.message
        data = all_data.get('data')
        result = data.get('result', {})
        quota = result.get('quota', {})
        __import__("ipdb").set_trace()
        quota = clean.data
        if quota:
            self.format_str.clean_na(quota)
            self.save_base_statistic_info(quota)


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
            create_time = datetime.now(),
            update_time = datetime.now(),
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
            deal_grade_in_city = percent_to_float(quota.get('S0363', '')),
            work_consume_times_per = percent_to_float(quota.get('S0656', '')),
            create_time=self.now_time,
        )

        			
