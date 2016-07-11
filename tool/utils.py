#!/usr/bin/env python
# coding: utf-8


import json, md5, requests, datetime, re
from conf import config
from pony.orm import *
from model.models import *
from datetime import *


def try_int(data):
    try:
        data = int(data)
    except Exception, e:
        return None
    return data

def try_float(data):
    try:
        data = round(float(data), 2)
    except Exception, e:
        return None
    return data

def percent_to_float(data):
    try:
        data = round(float(data.strip('%'))/100, 3)
    except Exception, e:
        return None
    return data

def exact_to_day(time_str):
    try:
        new_time = datetime.strptime(time_str, "%Y%m%d")
    except Exception, e:
        return None
    return new_time
    
def exact_to_month(time_str):
    try:
        new_time = datetime.strptime(time_str, "%Y%m")
    except Exception, e:
        return None
    return new_time

def get_db():
    db.bind('mysql', host=config.MYSQL_HOST, user=config.MYSQL_USER, 
            passwd=config.MYSQL_PASSWORD, db=config.DB_NAME
        )
    return db

def parse_to_dict(data, null=True):
    ret = {}
    try:
        data_list = data.split(';')
    except Exception, e:
        return {}
    for em in data_list:
        result = re.search(r'([\D\d]+)_([\D\d]*)', em)
        if result:
            key = result.group(1)
            value = result.group(2)
            if not value and null is True:
                value = None
            ret[key] = value
    return ret


class Request_Model(object):
    def request_params(self, param_dict):
        sign = self._parce_param(param_dict)
        param_dict['sign'] = sign
        return param_dict

    def _parce_param(self, param_dict):
        shabby_str = ''
        for key in sorted(param_dict.keys()):
            shabby_str += key.encode('utf8') + param_dict[key]
        shabby_str += config.PRIVATE_KEY
        return self._md5_encrypt(shabby_str)

    def _md5_encrypt(self, shabby_str):
        shabby_str=shabby_str.encode('utf8')
        md5_str = md5.new()
        md5_str.update(shabby_str)
        md5_str = md5_str.hexdigest()
        return md5_str.upper()

    def request_get(self, url, params):
        try:
            re = requests.get(url, params=params, verify=False)
        except Exception, e:
            raise e
        return re
    
    def request_post(self, url, data):
        r= requests.post(url, data=data)
        return r.url


class Format_Str(object):

    def clean_na(self, data):
        for key in data.keys():
            if data[key] == 'NA':
                data[key] = ''
                continue
            ems = data[key].split(';')
            for index in xrange(len(ems)):
                if ems[index] == 'NA':
                    ems[index] = ''
                ems[index] = ems[index].replace('_NA', '_')
            data[key] = ';'.join(ems)

