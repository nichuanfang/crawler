#!/usr/local/bin/python
# coding=utf-8

# 调度器
from my_selenium.my_selenium import logging
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
# 调试调度器
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler(timezone='Asia/Shanghai')

scheduler.start()