# -*- coding: utf-8 -*-

from tornado import (
        ioloop,
        web,
        httpserver
    )
import json, md5, requests, datetime, re
from conf import config
from pony.orm import *
from model.models import *
from ylzh.ylzh import Pylzh_Process
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import tornado.httpserver
from queryapi.urls import URLS as urls
from tool.utils import get_db

class MainHandler(web.RequestHandler):
    executor = ThreadPoolExecutor(30)

    def initialize(self):
        self.ylzh_process = Pylzh_Process()
    
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        #ram_data = {
        #    'account': config.ACCOUNT,
        #    'orderId': 'byjr_8ad22395309a120530c6e12a20260',
        #    'card': '6222629530002562008',
        #    'identityCard': '410422199003197012',
        #    'identityType': '001',
        #    'index': 'all',
        #    'mobile': '18625708694',
        #    'name': 'du培源'
        #}
        #json_data = json.dumps(ram_data)
        #self.ylzh_proc(json_data)
        for line in open('data.txt', 'r'):
            if line.strip():
                srt = re.match(r'"([\D\d]+)"\t"([\D\d]+)"\t"([\D\d]+)"\t"([\D\d]+)"\t"([\D\d]+)"\t', line.strip())
                try:
                    ram_data = {
                        'account': config.ACCOUNT,
                        'orderId': 'byjr_'+srt.group(1),
                        'card': srt.group(2),
                        'index': 'all',
                        'identityCard': srt.group(4),
                        'identityType': '001',
                        'mobile': srt.group(5),
                        'name': srt.group(3),
                    }
                except Exception, e:
                     continue
                json_data = json.dumps(ram_data)
                self.ylzh_proc(json_data)
    
    
    @run_on_executor
    def ylzh_proc(self, json_data):
        res = self.ylzh_process.request_data(json_data)

			
if __name__ == "__main__":
    settings = {
        'debug': True
    }
    # URLS is belong to queryapi
    urls.append((r"/", MainHandler))
    app = web.Application(urls,  **settings)
    db = get_db()
    db.generate_mapping(create_tables=True)
    app.listen(8888)
    ioloop.IOLoop.instance().start()
    server = httpserver.HTTPServer(app)
    server.bind(config.SERVER_PORT)
    server.start(config.SERVER_NUM)

