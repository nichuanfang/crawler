#!/usr/local/bin/python
# coding=utf-8
from environment import *
import sys
sys.path.append('../../')
# tmdb电影/剧集
from my_selenium.my_selenium import driver, BeautifulSoup, ActionChains, By, logging
from my_selenium.my_selenium import get_soup
import re
from urllib import request, parse

env = Env()

def tmdb_movie(origin:str,file_id:str):
    url = f'https://www.themoviedb.org/search/movie?query={origin}'
    soup = get_soup(url)
    # 返回电影名集合
    
    # 电影    soup.findAll('div',id=re.compile(r'^card_movie_[A-Za-z0-9]+$'))
    # 电视剧  soup.findAll('div',id=re.compile(r'^card_tv_[A-Za-z0-9]+$'))
    res = []

    movies = soup.findAll('div',id=re.compile(r'^card_movie_[A-Za-z0-9]+$'))
    for movie in movies:
        href_suffix = movie.a['href']
        # 跳转到详情页面
        href = f'https://www.themoviedb.org{href_suffix}'
        href_soup = get_soup(href)
        # 获取真正的电影名
        name = href_soup.findAll('h2')[0].text.replace('\n',' ').strip()

        if movie.contents[1].img is not None:
            img_url = 'https://www.themoviedb.org' + movie.contents[1].img['srcset'].split(',')[1][1:-3]
        else:
            img_url = ''
        urlencoded_origin = parse.quote(origin)
        urlencoded_parsed_name = parse.quote(name)
        # 简述
        if movie.p is not None:
            sketch = movie.p.text
        else:
            sketch = ''
        data = {
            # 点击链接 直接刮削该电影 生产环境需要替换域名
            'name': name,
            'file_id': file_id,
            'scrape_url': f'{env.crawler_base_url}/tmdb/scrape_movie?file_id={file_id}&name={urlencoded_parsed_name}',
            'picture_url': img_url,
            'sketch': sketch
        }
        res.append(data)
        logging.info(f'{name}')
    return res


def scrape_tvshows():
    pass

if __name__ == '__main__':
    pass