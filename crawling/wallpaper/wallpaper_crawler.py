#!/usr/local/bin/python 
# coding=utf-8
import sys
sys.path.append('../../')

from my_selenium.my_selenium import driver,BeautifulSoup,ActionChains,By,logging
from my_selenium.my_selenium import get_soup
import random
import requests
import subprocess

def craw_wallpaper():
    soup = get_soup('https://wallhaven.cc/search?categories=110&purity=100&atleast=1600x900&sorting=hot&order=desc&ai_art_filter=1')

    #拖动到页面最底部，=0为拖动到页面最顶部  分多少页就滚动几次
    # scroll_js="var q=document.documentElement.scrollTop=10000"
    # driver.execute_script(scroll_js)
    urls:list[str] = []
    # 获取图片链接并保存
    figures = soup.findAll('figure')
    img_names = []
    # 更新图片库
    index = 1
    for figure in figures:
        # 解析对应的url 
        link_soup = get_soup(figure.contents[1]['href'])
        img_ele = link_soup.find(id='wallpaper')
        if img_ele is None:
            pass
        else:
            url = img_ele['src']
            urls.append(url)
            r = requests.get(url)
            with open('/assets/img/bg'+'/'+'bg{}.jpg'.format(index),'wb') as f:
                f.write(r.content)
            logging.info('已刮削图片:{}'.format(url))
            img_names.append('bg{}.jpg'.format(index))
        index+=1

    # 随机一张图片保存到vscode中
    with open('/assets/img/bg'+'/'+random.choice(img_names),'rb') as f:
        with open('/assets/img/bg/vscode'+ '/'+'vscode-bg.jpg','wb') as vscf:
            vscf.write(f.read())
    logging.info('壁纸已更新')
    # 执行宿主机命令 重启nginx
    print(subprocess.call('nsenter -m -u -i -n -p -t 1 sh -c "docker restart nginx"',shell=True))
    logging.info('已重启nginx')

if __name__ == '__main__':
    craw_wallpaper()
    pass