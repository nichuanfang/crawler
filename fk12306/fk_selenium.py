#!/usr/local/bin/python3
import time
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import random
import re

from selenium import webdriver
import io
import sys
from fake_useragent import UserAgent

# ip代理池 防止被屏蔽 很重要
proxy_arr = [
    '--proxy-server=http://183.237.47.54:9091'
]

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
  # 随机从代理池选一个代理  
proxy = random.choice(proxy_arr)
# 随机选取一个ua
chrome_ua:list = UserAgent().data_browsers['chrome']
ua = random.choice(chrome_ua)



# 谷歌驱动设置
options = webdriver.ChromeOptions()
# 设置User-Agent
options.add_argument(f'user-agent={ua}')
# 添加代理 代理还是有问题 todo待解决
# options.add_argument(proxy)
# 规避检测
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension',False)
options.add_argument('--disable-blink-features')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-extensions')
options.add_argument('--no-default-browser-check')
options.add_argument('--disable-dev-shm-usage')
# 不用打开界面 无头浏览器
options.add_argument('--headless')
# 避免某些网页出错
options.add_argument('--disable-gpu')
# 最大化
options.add_argument('--start-maximized')
# 无痕模式
options.add_argument('--incognito')
# 禁用缓存
options.add_argument("disable-cache")
options.add_argument('disable-infobars')
options.add_argument('--ignore-certificate-errors') 
# 日志级别 0:INFO  1:WARNING 2:LOG_ERROR 3:LOG_FATAL  default is 0
# options.add_argument('log-level=3')
# 禁止打印日志
options.add_experimental_option('excludeSwitches', ['enable-logging'])
executable_path = '/usr/local/bin/chromedriver'
def refresh_cookie() -> tuple[int,str]:
    driver = webdriver.Chrome(executable_path=executable_path,chrome_options=options)
    # 绕过检测
    with open('stealth.min.js', 'r') as f:
        js = f.read()
    # 调用函数在页面加载前执行脚本
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})
    driver.get("https://kyfw.12306.cn/otn/resources/login.html")
    user = driver.find_element(by=By.ID,value="J-userName")
    user.click()
    user.send_keys("rw15356123161")
    pswd = driver.find_element(by=By.ID,value="J-password")
    pswd.click()
    pswd.send_keys("0820nCf9270")
    butten = driver.find_element(by=By.ID,value="J-login")
    butten.click()
    time.sleep(1)

    while True:
        try:
            span = driver.find_element(by=By.ID,value="nc_1_n1z")
            actions = ActionChains(driver)  # 行为链实例化
            time.sleep(1)  # 等待2秒钟
            # 经截图测量，滑块需要滑过的距离为300像素
            actions.click_and_hold(span).move_by_offset(300, 0).perform()  # 滑动
            actions.release();
            time.sleep(1);
            a = driver.find_element(by=By.ID,value="nc_1_refresh1");# 查找刷新按钮，如果没有说明登录成功，执行except跳出循环
            a.click();# 如果刚刚滑动失败，则点击刷新，重新滑动
        except Exception as e:
            print(e);
            break;
    Cookie:str = ''
    expire_time:int = 0
    cookies:list = driver.get_cookies()
    for cookie in cookies:
        Cookie+=cookie['name'] + '=' + cookie['value']+';'
        expiry = cookies[0]['expiry']
        if expiry is not None and expiry != '' and expire_time < expiry:
            expire_time = expiry
    return (expire_time,Cookie[:-1])

# sure = driver.find_element_by_class_name("btn-primary");
# sure.click();

# link_for_ticket = driver.find_element_by_id("link_for_ticket");
# link_for_ticket.click();
# driver.find_element_by_id("fromStationText").click();
# driver.find_element_by_css_selector(u"[title=长沙]").click();
# driver.find_element_by_id("toStationText").click();
# driver.find_element_by_css_selector(u"[title=北京]").click();
# time.sleep(5);
# train_date = driver.find_element_by_id("train_date");
# train_date.clear();

# tomorrow = (date.today() + timedelta(days= 1)).strftime("%Y-%m-%d")
# train_date.send_keys(tomorrow);
# driver.find_element_by_css_selector("#_ul_station_train_code > li:nth-child(1) > label").click()

# while True:
#     try:
#         driver.find_element_by_id("query_ticket").click();
#         driver.find_element_by_xpath("/html/body/div[3]/div[7]/div[8]/table/tbody[1]/tr[1]/td[13]").click();
#         time.sleep(3);
#         driver.find_element_by_id("normalPassenger_0").click();
#         driver.find_element_by_id("submitOrder_id").click();
#         driver.find_element_by_link_text("确认").click();
#     except:
#         pass;