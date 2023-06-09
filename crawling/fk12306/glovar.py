#!/usr/local/bin/python
# coding=utf-8 
"""
@author: HJK
@file: glovar.py
@time: 2019-02-11
"""

import sys
import datetime
from os import path
import time
from fake_useragent import UserAgent
import random

from . import fk_crawler

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
    "X-Requested-With": "XMLHttpRequest"
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
    """自定义请求头

    Returns:
        _type_: 请求头
    """    
    chrome_ua:list = UserAgent().data_browsers['chrome']
    ua = random.choice(chrome_ua)
    # 伪造ua
    FAKE_HEADERS['User-Agent'] = ua
    # 更新cookie
    return update_cookie(FAKE_HEADERS)

def update_cookie(FAKE_HEADERS:dict[str,str]):
    """更新cookie
    """ 
    # 当前时间戳
    now = int(time.time())
    glovar = Glovar()
    # 如果cookie字段为空 直接获取cookie 设置expire_date
    # 如果cookie字段不为空 根据expire_date判断是否过期 
        # 过期调用fk_selenium刷新token
        # 没过期 不操作
    if glovar.cookie != '' and glovar.cookie_expire_time>=now:
        # 没过期
        FAKE_HEADERS['Cookie'] = glovar.cookie
    else:
        # 手动刷新
        res:tuple = fk_crawler.refresh_cookie()
        expire_date = res[0]
        glovar.cookie_expire_time = expire_date

        FAKE_HEADERS['Cookie'] = res[1]
        glovar.cookie = res[1]
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
        # cookie
        self.cookie:str = ''
        # cookie过期时间
        self.cookie_expire_time = int(time.time())

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
