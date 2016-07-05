# -*- coding: utf-8 -*-

from pony.orm import *
from pony import orm
from datetime import datetime
db = Database()


class REQUEST_INFO(db.Entity):
    orderId = PrimaryKey(str, 55)
    resCode = Optional(int)
    resMsg = Optional(str, 10)
    statCode = Optional(int)
    statMsg = Optional(str, 55)
    smartOrderId = Optional(str, 55)
    sign = Optional(str, 55)
    create_time = Optional(datetime)
    update_time = Optional(datetime)


class BN_BASE_STATISTIC_INFO(db.Entity):
    orderId = PrimaryKey(str, 55)
    cert_no = Optional(str, 20)
    bank_card_no = Optional(str, 20)
    name = Optional(str, 20)
    card_type = Optional(str, 10)
    card_grade = Optional(str, 10)
    line_consume_amt = Optional(float)
    line_consume_times = Optional(int)
    lastest_consume_date = Optional(datetime)
    dif_city_consume_1h = Optional(int)
    receive_to_transfer_per = Optional(float)
    receive_to_draw_per = Optional(float)
    fir_deal_date = Optional(datetime)
    deal_days = Optional(int)
    deal_grade_in_city = Optional(float)
    work_consume_times_per = Optional(float)
    create_time = Optional(datetime)
    update_time = Optional(datetime)

class BN_MONTH_CONSUME(db.Entity):
    orderId = PrimaryKey(str, 55)
    cert_no = Optional(str, 20)
    bank_card_no = Optional(str, 20)
    name = Optional(str, 20)
    month = Optional(datetime)
    work_consume_amt = Optional(float)
    deal_consume_amt = Optional(float)
    deal_consume_times = Optional(int)
    deal_bank_amt = Optional(float)
    deal_bank_times = Optional(int)
    create_time = Optional(datetime)
    update_time = Optional(datetime)


class BN_LIVE_CITY(db.Entity):
    orderId = PrimaryKey(str, 55)
    cert_no = Optional(str, 20)
    bank_card_no = Optional(str, 20)
    name = Optional(str, 20)
    province = Optional(str, 20)
    city1 = Optional(str, 20)
    city2 = Optional(str, 20)
    city3 = Optional(str, 20)
    city4 = Optional(str, 20)
    city5 = Optional(str, 20)
    create_time = Optional(datetime)
    update_time = Optional(datetime)


class BN_MCC_CONSUME(db.Entity):
    orderId = PrimaryKey(str, 55)
    cert_no = Optional(str, 20)
    bank_card_no = Optional(str, 20)
    name = Optional(str, 20)
    mcc_code = Optional(str, 10)
    night_consume_amt = Optional(float)
    night_consume_times = Optional(int)
    consume_amt = Optional(float)
    consume_times = Optional(int)
    create_time = Optional(datetime)
    update_time = Optional(datetime)


class BN_HIGH_FREQ_MAR(db.Entity):
    orderId = PrimaryKey(str, 55)
    cert_no = Optional(str, 20)
    bank_card_no = Optional(str, 20)
    name = Optional(str, 20)
    mar_name = Optional(str, 255)
    consume_per = Optional(float)
    create_time = Optional(datetime)
    update_time = Optional(datetime)


class BN_TOP_MONEY_MAR(db.Entity):
    orderId = PrimaryKey(str, 55)
    cert_no = Optional(str, 20)
    bank_card_no = Optional(str, 20)
    name = Optional(str, 20)
    top5_consume_amt_mar = Optional(str, 255)
    create_time = Optional(datetime)
    update_time = Optional(datetime)


class BN_CONSUME_CITY_TIMES(db.Entity):
    orderId = PrimaryKey(str, 55)
    cert_no = Optional(str, 20)
    bank_card_no = Optional(str, 20)
    name = Optional(str, 20)
    city_code = Optional(str, 10)
    consume_times = Optional(int)
    create_time = Optional(datetime)
    update_time = Optional(datetime)


