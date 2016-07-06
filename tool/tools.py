# -*- coding: utf-8 -*-

import json, md5, requests, datetime
from conf import config
from pony.orm import *

class Build_Url(object):
    def request_url(self, param_dict):
        url = config.DOMAIN + config.USER_DATA
        for key, val in param_dict.items():
            url += key + '=' + val + '&'
        sign = self.parce_param(param_dict)
        url += 'sign' + '=' + sign
        return url

    def parce_param(self, param_dict):
        shabby_str = ''
        for key in sorted(param_dict.keys()):
            shabby_str += key.encode('utf8') + param_dict[key]
        shabby_str += config.PRIVATE_KEY
        return self.md5_encrypt(shabby_str)

    def md5_encrypt(self, shabby_str):
        shabby_str=shabby_str.encode('utf8')
        md5_str = md5.new()
        md5_str.update(shabby_str)
        md5_str = md5_str.hexdigest()
        return md5_str.upper()

                            

