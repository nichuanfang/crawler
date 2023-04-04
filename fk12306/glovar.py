#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: glovar.py
@time: 2019-02-11
"""

import sys
import datetime
from os import path
from fake_useragent import UserAgent
import random

from .config import Options

# 大写配置无特殊情况不建议修改
FAKE_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "kyfw.12306.cn",
    "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/72.0.3626.96 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "JSESSIONID=806459121FBEEB715068BFA8B2BF9188; tk=TfHY4SqBDKxI6GdcdR3UaUxl9LwqvnsFrGuhznvcLAYnxr1r0; BIGipServerotn=3738632458.64545.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; BIGipServerpassport=837288202.50215.0000; RAIL_EXPIRATION=1680907851121; RAIL_DEVICEID=XvCkXzcmjtuvmF8vcJTfLYlg3tQrQ55SzoQlMwodBbsF29Mjddt9DcGvq7OaiD72zMutxhrmj38b-Y9RiWcc51qwqCWMKyf3M_Znkf1oL8gLNM7qXNOUePyQ8rlP3TGLnASQog_Ebe0yBR3BQmbG4JabR7hSx_yf; route=6f50b51faa11b987e576cdb301e545c4; uKey=09cf71a13b132a028c0fb799f5559d31706aa2797b1db4db2b40eb52412ae114; fo=q05lmopjl8fmylsux9byxSjTLENgKV-4ipMdDQp-SLTAGxXwYZobroRBHD1KFioLJQ_m4i4bzDX8j0BJpGXLBz2wIJmVGXHI1TQ9GnwO2zwfYM57P1y_9x63JedWiTCtmMTS_2oq6gQjHLy80XK-HTRvB73qiPBt2lLMIwltjGVZvDTBfHWhHckWUW4",
}

SEAT_TYPES = {
    "特等座": 25,
    "商务座": 32,
    "一等座": 31,
    "二等座": 30,
    "高级软卧": 21,
    "软卧": 23,
    "动卧": 33,
    "硬卧": 28,
    "软座": 24,
    "硬座": 29,
    "无座": 26,
    "其他": 22,
}

def generate_header():
    chrome_ua:list = UserAgent().data_browsers['chrome']
    ua = random.choice(chrome_ua)
    FAKE_HEADERS['User-Agent'] = ua
    return FAKE_HEADERS

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Glovar(metaclass=Singleton):
    """
    全局共享变量
    """

    def __init__(self):
        opts = Options()

        if not path.isfile(opts.stations_file):
            # 如果stations文件不存在则终止程序
            print(opts.stations_file)
            print("Stations file is not exsits.")
            sys.exit(-1)

        self.zmode = opts.zmode
        self.zzmode = opts.zzmode
        self.total_stations = []
        self.total_proxies = []
        self.seats_list = []
        self.seats_idx_list = []
        self.fs = opts.fs
        self.ts = opts.ts
        self.fs_code = ""
        self.ts_code = ""
        self.date = opts.date or datetime.date.today().strftime("%Y-%m-%d")
        self.no_list = opts.train_no.split()
        self.gcd = opts.gcd
        self.ktz = opts.ktz
        self.remaining = opts.remaining

        # 获得所有站点编码的名称对应信息
        stations = open(opts.stations_file, "r", encoding="utf-8").read()
        for station in stations.split("@"):
            if not station:
                continue
            t = station.split("|")
            # (编码, 站名）如（VAP，北京）
            self.total_stations.append((t[2], t[1]))

        # 获得所有代理信息
        if path.isfile(opts.proxies_file):
            # 如果代理列表文件存在
            self.total_proxies = open(
                opts.proxies_file, "r", encoding="utf-8"
            ).readlines()

        # 处理座位选择
        for seat in opts.seats.split():
            if seat not in SEAT_TYPES:
                continue
            self.seats_list.append(seat)
            self.seats_idx_list.append(SEAT_TYPES[seat])

        # 处理站名编码
        for station in self.total_stations:
            if self.fs == station[1]:
                self.fs_code = station[0]
            if self.ts == station[1]:
                self.ts_code = station[0]
            if self.fs_code and self.ts_code:
                break
        # self.fs_code = station_to_code(self.fs)
        # print("-----glovar init")
        # print(self.fs_code, self.ts_code)
