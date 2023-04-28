#!/usr/local/bin/python
# coding=utf-8 
from environment import *
from flask import Flask
from api import fk12306_api
from api import cron_api
from api import tmdb_api
from api import xray_api
from cron.job.wallpaper_crawling import craw_wallpaper
from cron.job.tmm_movie_check import tmm_movie_check
from my_selenium.my_selenium import logging
from aliyundrive import ali_drive
from swagger_ui import api_doc
import os

app = Flask(__name__)
# app.debug = True

# ====================================首页=========================================================

@app.route('/', methods = ['GET', 'POST'])
def index():
    return app.redirect('/api/doc')

#=====================================fk12306=====================================================
@app.route(rule='/fk12306/ticket', methods=['get'])
def ticket():
    """查询余票

    Returns:
        _type_: 余票信息
    """    
    try:
        return fk12306_api.ticket()
    except Exception as e:
        return e.__str__()
    
#=======================================xray=========================================================

@app.route(rule='/xray/add_rule', methods=['get'])
def add_rule():
    """xray添加路由规则

    Returns:
        _type_: 结果
    """    
    try:
        return xray_api.add_client_route_rule()
    except Exception as e:
        return e.__str__()

# =====================================定时任务======================================================
@app.route(rule='/job/list', methods=['get'])
def list_job():
    """查询当前所有任务

    Returns:
        _type_: 结果
    """    
    res = []
    for item in cron_api.list_job():
        res.append({'job_id': item.id,'data':item.__str__()})
    return res

@app.route(rule='/job/execute', methods=['get'])
def execute_job():
    """立即执行某个job

    Returns:
        _type_: 结果
    """ 
    try:
        return cron_api.execute_job()
    except Exception as e:
        return e.__str__()

@app.route(rule='/job/reschedule', methods=['get'])
def reschedule_job():
    """修改job

    Returns:
        _type_: 结果
    """    
    try:
        return cron_api.reschedule_job()
    except Exception as e:
        return e.__str__()


@app.route(rule='/job/remove', methods=['get'])
def remove_job():
    """移除job

    Returns:
        _type_: 结果
    """    
    try:
        return cron_api.remove_job()
    except Exception as e:
        return e.__str__()

@app.route(rule='/job/pause', methods=['get'])
def pause_job():
    """暂停job

    Returns:
        _type_: 结果
    """    
    try:
        return cron_api.pause_job()
    except Exception as e:
        return e.__str__()

@app.route(rule='/job/resume', methods=['get'])
def resume_job():
    """恢复job

    Returns:
        _type_: 结果
    """    
    try:
        return cron_api.resume_job()
    except Exception as e:
        return e.__str__()
    
# ==========================================阿里云盘=====================================================
@app.route(rule='/ali_drive/rename', methods=['get'])
def rename():
    """文件/文件夹重命名

    Returns:
        _type_: _description_
    """    
    try:
        return tmdb_api.rename()
    except Exception as e:
        return e.__str__()
    
# ==========================================tmdb刮削=====================================================
@app.route(rule='/tmm/movies', methods=['get'])
def tmm_movies():
    """获取tmm文件夹下电影信息 层级展示 .mkv文件父级文件夹才是电影名文件夹 需要重命名
    """ 
    try:
        return tmdb_api.tmm_movies()
    except Exception as e:
        return e.__str__()
    

@app.route(rule='/tmm/movie/scrape', methods=['get'])
def tmm_movie_scrape():
    """刮削修正好电影名字的tmm-movies文件夹
    """ 
    try:
        return tmdb_api.tmm_movie_scrape()
    except Exception as e:
        return e.__str__()
    


@app.route(rule='/tmdb/movie', methods=['get'])
def tmdb_movie():
    """获取电影修正信息

    Returns:
        _type_: 结果
    """    
    try:
        return tmdb_api.tmdb_movie()
    except Exception as e:
        return e.__str__()

@app.route(rule='/tmdb/scrape_movie', methods=['get'])
def tmdb_scrape_movie():
    """修正电影文件夹名称

    Returns:
        _type_: 结果
    """    
    try:
        return tmdb_api.tmdb_scrape_movie()
    except Exception as e:
        return e.__str__()




# ===========================================主程序======================================================
if __name__ == '__main__':
    # 加载环境
    env = Env()
    # 加载自定义的swagger文件
    api_doc(app,config_path=f'openapi/apidoc-{env.curr_env}.yml', url_prefix='/api/doc', title='API doc')

    # 添加若干定时任务
    # 壁纸刮削
    cron_api.add_job(craw_wallpaper,'cron',hour=13,minute=30,second=0,args=[])
    logging.info('壁纸刮削任务已启动...')

    # 启动爬虫主程序
    logging.info(f'===============已启动主程序,当前环境:{env.curr_env}===================================')
    app.run(env.listening_host, 5000)