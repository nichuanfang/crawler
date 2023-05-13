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
    root_path = '/assets/img/bg'
    soup = get_soup('https://wallhaven.cc/search?categories=111&purity=100&resolutions=3440x1440%2C1600x900%2C1920x1080%2C2560x1440%2C3840x2160&sorting=hot&order=desc&ai_art_filter=0')

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
            with open(root_path+'/'+f'bg{index}.jpg','wb') as f:
                f.write(r.content)
            logging.info(f'已刮削图片:{url}')
            img_names.append(f'bg{index}.jpg')
        index+=1

    # 随机一张图片保存到vscode中
    with open(root_path+'/'+random.choice(img_names),'rb') as f:
        with open(f'{root_path}/vscode'+ '/'+'vscode-bg.jpg','wb') as vscf:
            vscf.write(f.read())
    logging.info('壁纸已更新')
    # 执行宿主机命令 重启nginx
    print(subprocess.call('nsenter -m -u -i -n -p -t 1 sh -c "docker restart nginx"',shell=True))
    logging.info('已重启nginx')

def craw_random_wallpaper():
    # 随机挑一页数据(总数200)
    soup = get_soup(f'https://wallhaven.cc/search?categories=110&purity=100&atleast=1200x900&sorting=date_added&order=desc&ai_art_filter=1&page={random.randint(1, 200)}')

    #拖动到页面最底部，=0为拖动到页面最顶部  分多少页就滚动几次
    # 获取图片链接并保存
    figures = soup.findAll('figure')
    # 随机获取一个figure
    if len(figures) == 0:
        return craw_random_wallpaper()
    figure = figures[random.randint(0, len(figures))]
    # 解析对应的url 
    link_soup = get_soup(figure.contents[1]['href'])
    img_ele = link_soup.find(id='wallpaper')
    if img_ele is None:
        # 直到有数据
        return craw_random_wallpaper()
    else:
        url = img_ele['src']
        r = requests.get(url)
        logging.info(f'已刮削图片:{url}')
        return r.content

if __name__ == '__main__':
    craw_wallpaper()
    pass