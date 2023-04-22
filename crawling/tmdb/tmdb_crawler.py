#!/usr/local/bin/python
# coding=utf-8
import sys
sys.path.append('../../')
# tmdb电影/剧集
from my_selenium.my_selenium import driver, BeautifulSoup, ActionChains, By, logging
from my_selenium.my_selenium import get_soup
import re
import random
import requests
import subprocess
from urllib import request, parse

def tmdb_movie(origin:str):
    url = 'https://www.themoviedb.org/search/movie?query={}'.format(origin)
    soup = get_soup(url)
    # 返回电影名集合
    
    # 电影    soup.findAll('div',id=re.compile(r'^card_movie_[A-Za-z0-9]+$'))
    # 电视剧  soup.findAll('div',id=re.compile(r'^card_tv_[A-Za-z0-9]+$'))
    res = []

    movies = soup.findAll('div',id=re.compile(r'^card_movie_[A-Za-z0-9]+$'))
    for movie in movies:
        year = movie.span.text[:4]
        movie_name = movie.contents[1].contents[3].contents[1].contents[1].a.text
        if movie.contents[1].img is not None:
            img_url = 'https://www.themoviedb.org' + movie.contents[1].img['srcset'].split(',')[1][1:-3]
        else:
            img_url = ''
        data = {
            # 点击链接 直接刮削该电影 生产环境需要替换域名
            'name': movie_name,
            'year': year,
            'scrape_url': 'http://127.0.0.1:5000/tmdb/scrape_movie?origin={}&name={}'.format(parse.quote(origin),parse.quote('{} ({})'.format(movie_name,year))),
            'picture_url': img_url,
            'sketch': movie.p.text
        }
        res.append(data)
    return res


def scrape_tvshows():
    pass

if __name__ == '__main__':
    res = tmdb_movie('教父')
    print(res)
    pass