#!/usr/local/bin/python
# coding=utf-8 
import time
import sys
sys.path.append('../../')
from my_selenium.my_selenium import driver,BeautifulSoup,ActionChains,By,logging
from my_selenium.my_selenium import get_soup


def refresh_cookie() -> tuple[int,str]:
    logging.info('=========开始获取cookie==========')
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
            print(e.__str__())
            break
    Cookie:str = ''
    expire_time:int = 0
    cookies:list = driver.get_cookies()
    for cookie in cookies:
        Cookie+=cookie['name'] + '=' + cookie['value']+';'
        if cookie.__contains__('expiry'):
            expiry = cookie['expiry']
            if expiry is not None and expiry != '' and expire_time < expiry:
                expire_time = expiry
    logging.info('=========已获取cookie:{}=========='.format(Cookie[:-1]))
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
if __name__ == '__main__':
    # soup = get_soup('https://www.baidu.com')
    # print(soup.prettify())
    refresh_cookie()
    pass