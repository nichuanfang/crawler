#!/usr/local/bin/python
# coding=utf-8

# 定时任务api
import datetime
from flask import request
from urllib.parse import parse_qs, urlparse
from crawling.tmdb import tmdb_crawler


def tmdb_movie():
    if not request.values.__contains__('origin'):
        return 'origin参数必填!'
    else:
        origin = request.values['origin'].replace(
            '\'', '').replace('\"', '')
    return tmdb_crawler.tmdb_movie(origin)


def tmdb_scrape_movie():
    if not request.values.__contains__('origin'):
        return 'origin参数必填!'
    else:
        origin = request.values['origin'].replace(
            '\'', '').replace('\"', '')
    if not request.values.__contains__('name'):
        return 'name参数必填!'
    else:
        name = request.values['name'].replace(
            '\'', '').replace('\"', '')

    # 1. 将阿里云盘的tmm文件夹下面名为origin的文件夹重命名为name
    # 2. 使用tinymediamanager进行刮削
    # 3. 文件夹不再有变化 则将tmm下该电影文件夹移至movies中
    return origin+':'+name
