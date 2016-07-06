# -*- coding: utf-8 -*-
import json, md5, requests, datetime
from conf import config
from pony.orm import *
from model.models import *
from tool import tools

class Pylzh_Process(object):
    def __init__(self):
        self.build_url = tools.Build_Url()

    def request_data(self, json_data):
        param_dict = json.loads(json_data)
        request_url = self.build_url.request_url(param_dict)
        try:
            response = requests.get(request_url, verify=False)
            self.save_info(response)
        except Exception, e:
            return 'e.message'
        return 'ylzh请求成功'

    @db_session
    def save_info(self, response):
        all_data = json.loads(response.text)
        __import__("ipdb").set_trace()
        if all_data.get('data'):
            try:
                self.save_data(all_data)
            except Exception, e:
                raise e
            Request_Info(
                orderId=all_data.get('orderId'), 
                resCode=all_data.get('resCode'),
                resMsg=all_data.get('resMsg'),
                statCode=all_data.get('statCode'),
                statMsg=all_data.get('statMsg'),
                smartOrderId=all_data.get('smartOrderId', ''),
                sign=all_data.get('sign', ''),
                create_time=datetime.now(),
                update_time=datetime.now(),
            )

    @db_session
    def save_data(self, all_data):
       # __import__("ipdb").set_trace()
        orderId = all_data.get('orderId')
        data = all_data.get('data')
        result = data.get('result', {})
        quota = result.get('quota', {})
        User_Data(
            orderId=orderId,
            validate=data.get('validate'),
            active=result.get('active'),
            S0479=quota.get('S0479'),
            S0478=quota.get('S0478'),
            sign=all_data.get('sign'),
            create_time=datetime.now(),
            update_time=datetime.now(),
        )

        			
