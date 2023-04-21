#!/usr/local/bin/python
# coding=utf-8 

# 定时任务api
import datetime
from cron.my_scheduler import scheduler
from flask import request
from urllib.parse import parse_qs, urlparse

# 添加job
def add_job(job,trigger,**kwargs):
    scheduler.add_job(job,trigger,**kwargs)
    return '任务已添加!'    


def execute_job():
    """立刻执行任务
    """    
    if not request.values.__contains__('job_id'):
        return 'job_id参数必填!'
    else:
        job_id = request.values['job_id'].replace('\'','').replace('\"','')
    if not request.values.__contains__('jobstore'):
        jobstore = None
    else:
        jobstore = request.values['jobstore'].replace('\'','').replace('\"','')
    job = scheduler._lookup_job(job_id, jobstore)
    # 新增一个立即执行的任务
    if job[0] is not None:
        scheduler.add_job(job[0].func,'date',run_date=datetime.datetime.now() + datetime.timedelta(seconds=3))
        return '任务已于{}触发!'.format(datetime.datetime.now() + datetime.timedelta(seconds=3))
    return '没有该任务!'
    

# 修改job
def reschedule_job():
    trigger_args = parse_qs(urlparse(request.url).query)
    if not request.values.__contains__('job_id'):
        return 'job_id参数必填!'
    else:
        trigger_args.pop('job_id')
        job_id = request.values['job_id'].replace('\'','').replace('\"','')

    if not request.values.__contains__('trigger'):
        return 'trigger参数必填!'
    else:
        trigger_args.pop('trigger')
        trigger = request.values['trigger'].replace('\'','').replace('\"','')

    if not request.values.__contains__('jobstore'):
        jobstore = None
    else:
        trigger_args.pop('jobstore')
        jobstore = request.values['jobstore'].replace('\'','').replace('\"','')
    new_trigger_args = {}
    for key in trigger_args:
        new_trigger_args[key] = trigger_args[key][0].replace('\'', '').replace('\"','')
    scheduler.reschedule_job(job_id=job_id,jobstore=jobstore,trigger=trigger,**new_trigger_args)
    return '任务触发器已修改!'    

# 删除job
def remove_job():
    if not request.values.__contains__('job_id'):
        return 'job_id参数必填!'
    else:
        job_id = request.values['job_id'].replace('\'','').replace('\"','')
    if not request.values.__contains__('jobstore'):
        jobstore = None
    else:
        jobstore = request.values['jobstore'].replace('\'','').replace('\"','')
    scheduler.remove_job(job_id=job_id,jobstore=jobstore)
    return '任务已移除!'    

# 暂停job
def pause_job():
    if not request.values.__contains__('job_id'):
        return 'job_id参数必填!'
    else:
        job_id = request.values['job_id'].replace('\'','').replace('\"','')
    if not request.values.__contains__('jobstore'):
        jobstore = None
    else:
        jobstore = request.values['jobstore'].replace('\'','').replace('\"','')
    scheduler.pause_job(job_id=job_id,jobstore=jobstore)
    return '任务已暂停!'

# 恢复job
def resume_job():
    if not request.values.__contains__('job_id'):
        return 'job_id参数必填!'
    else:
        job_id = request.values['job_id'].replace('\'','').replace('\"','')
    if not request.values.__contains__('jobstore'):
        jobstore = None
    else:
        jobstore = request.values['jobstore'].replace('\'','').replace('\"','')
    scheduler.resume_job(job_id=job_id,jobstore=jobstore)
    return '任务已恢复!'

# job列表
def list_job():
    # scheduler.print_jobs()
    return scheduler.get_jobs()

