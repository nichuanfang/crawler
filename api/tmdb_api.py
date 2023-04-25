#!/usr/local/bin/python
# coding=utf-8

# tmdb api
from environment import *
import datetime
from email import header
from time import sleep
from api.base_api import get_required
from api.base_api import get_not_required
from flask import request
from urllib.parse import parse_qs, urlparse
from urllib import request, parse
from crawling.tmdb import tmdb_crawler
from aliyundrive import ali_drive
from aligo.types.BaseFile import BaseFile
import json
import requests
from requests import Response
from api.cron_api import add_job
from cron.job.tmm_movie_check import tmm_movie_check
import subprocess
from my_selenium.my_selenium import logging

env = Env()

def rename():
    """文件/文件夹重命名
    Returns:
        _type_: _description_
    """    
    file_id = get_required('file_id')
    new_name = get_required('new_name')
    ali_drive.rename(file_id,new_name)
    return '文件重命名成功！'

def tmm_movies():
    """获取tmm文件夹下电影信息 层级展示 .mkv文件父级文件夹才是电影名文件夹 需要重命名
    """ 
    tmm_movies_folder = ali_drive.get_folder_by_path('tmm/tmm-movies')
    assert tmm_movies_folder is not None
    res = []
    file_id_list = []
    def callback(path:str,file:BaseFile):
        if file.file_extension.lower() in ['mkv','mov','wmv','flv','avi','avchd','webm','mp4']:
            # 父文件夹的id
            file_id = file.parent_file_id
            origin = parse.quote(ali_drive.get_file(file.parent_file_id).name)
            if file_id not in file_id_list:
                res.append({
                    'name': file.name,
                    'parent_name': parse.unquote(origin),
                    'parent_file_id': file_id,
                    'rename_url': f'{env.crawler_base_url}/ali_drive/rename?file_id={file_id}',
                    'tmdb_movie_url': f'{env.crawler_base_url}/tmdb/movie?file_id={file_id}&origin={origin}'
                })
                file_id_list.append(file_id)
        
    ali_drive.aligo.walk_files(callback,tmm_movies_folder.file_id)
    wrapper_res = {}
    wrapper_res['data'] = res
    wrapper_res['tmm_scrape_url'] = f'{env.crawler_base_url}/tmm/movie/scrape'
    return wrapper_res


def tmdb_movie():
    origin = get_required('origin')
    file_id = get_required('file_id')
    return tmdb_crawler.tmdb_movie(origin,file_id)


def tmdb_scrape_movie():
    file_id = get_required('file_id')
    name = get_required('name')
    # 将阿里云盘的tmm文件夹下面名为origin的文件夹重命名为name
    origin_folder = ali_drive.get_file(file_id)
    if origin_folder is not None:
        ali_drive.rename(file_id,name)
    return '电影名更新成功！'


def tmm_movie_scrape():
    # 1. 使用tinymediamanager进行刮削 (tmm需要开启http远程控制)  api_key
    # 2. 定期查看tmm文件夹 是否有生成nfo的文件夹 最长检查2h
    # 3. 生成.nfo的文件夹移至movies中 

    # todo tmm启动失败
    tmm_url = f'{env.tmm_base_url}/api/movie'
    # post请求体样例

    # 1. action: The name of the action to trigger - you will find all implemented actions below
    # 2. scope: The scope for the action. This defines on which entries the action should be applied. The optional parameter args can be used to fine-tune the scope (not available on all scope values). Valid scope values depend on the action you trigger (details see below).
    # 3. args: Any extra arguments you may pass to the actions (optional - used by some actions)

    # {
    #     "action": <action name>,    update/scrape/downloadTrailer/downloadSubtitle/rename/export
    #     "scope": {
    #         "name": <scope name>,  
    #         "args": [
    #         <value>  
    #         ]
    #     },
    #     "args": {
    #         <key>: <value>  
    #     }
    # }
    # 执行宿主机命令 启动tinymediamanager
    print(subprocess.call('nsenter -m -u -i -n -p -t 1 sh -c "docker start tinymediamanager"',shell=True))
    logging.info('启动tinymediamanager中...')
    # 更新数据源+刮削电影信息
    payload = [
        {
            'action': 'update',
            'scope': {
                'name': 'all'    
            }
        },
        {
            'action': 'scrape',
            'scope': {
                'name': 'all'
            }
        }
    ]
    headers = {
        'api-key': f'{env.tmm_api_key}'
    }
    max_wait_sec = 60
    curr_sec = 0
    while(True):
        if curr_sec > max_wait_sec:
            return 'tmm启动失败!'
        res = Response()
        try:
            res:Response = requests.post(tmm_url,json.dumps(payload),headers=headers)
        except Exception as e:
            sleep(5)
            curr_sec+=8
            continue
        if res.ok:
            # 开启定时任务 
            # 一个小时后执行tmm_movie_check job
            logging.info('tinymediamanager启动成功!')
            add_job(tmm_movie_check,'date',run_date=datetime.datetime.now() + datetime.timedelta(minutes=60))
            return '已发送刮削指令!'
        sleep(5)
        curr_sec+=8
