#!/usr/local/bin/python
# coding=utf-8 
from api.base_api import get_required
from api.base_api import get_not_required
from flask import request
from crawling.fk12306.train import TrainTable
from crawling.fk12306.glovar import Glovar
from crawling.fk12306.glovar import SEAT_TYPES
from crawling.fk12306 import utils



import datetime

def ticket():
    """查询余票

    Returns:
        _type_: 余票信息
    """    
    values = request.values
    begin = get_required('begin')
    end = get_required('end')
    if request.values.__contains__('offset'):
        try:
            offset = int(request.values['offset'])
            if offset < 0:
                return 'offset必须大于等于0'
        except Exception as e:
            offset = 0
    else:
        offset = 0
    seats = get_not_required('seats')
    train_no = get_not_required('train_no')
    zmode = handle_bool(request,'zmode')
    zzmode = handle_bool(request,'zzmode')
    gcd = handle_bool(request,'gcd')
    ktz = handle_bool(request,'ktz')
    remaining = handle_bool(request,'remaining')
    # 根据查询参数调用对应的接口
    return query_tickets(begin,end,offset,seats,train_no,zmode,zzmode,gcd,ktz,remaining)


def query_tickets(begin: str, end: str, offset:int, seats:str|None, train_no:str|None
                  ,zmode:bool,zzmode:bool,gcd:bool,ktz:bool,remaining:bool):
    """查询余票(默认当天 普通模式 有票 高铁动车)
    
    Args:
        begin (str):出发地

        end (str):目的地

        offset (int):偏移量 距离今天的偏移量 默认为0 例如  1: 明天 -1:昨天

        seats (str):座位类型  一等座 二等座 无座  格式: 空格分隔

        train_no(str):默认不限制 限制车次  格式: 空格分隔

        zmode (bool):模式 是否开启高级模式 默认False

        zzmode(bool):模式 是否开启终极模式 默认False

        gcd(bool): 只看高铁

        ktz(bool): 只看火车

        remaining(bool): 只看有票
    """

    glovar = Glovar()

    glovar.fs_code = utils.station_to_code(begin)
    if glovar.fs_code is None or glovar.fs_code == '':
        return '起点{}不是市级地点或者不包含该地点!'.format(begin)
    glovar.fs = begin

    glovar.ts_code = utils.station_to_code(end)
    if glovar.ts_code is None or glovar.ts_code == '':
        return '终点{}不是市级地点或者不包含该地点!'.format(end)
    glovar.ts = end

    if offset:
        glovar.date = (datetime.datetime.now() +
                    datetime.timedelta(days=offset)).strftime('%Y-%m-%d')
    else:
        glovar.date = (datetime.datetime.now()).strftime('%Y-%m-%d')
    glovar.seats_list = []
    glovar.seats_idx_list = []
    if seats:
        handle_seats(seats,glovar)
    else:
        handle_seats('一等座 二等座 无座',glovar)
    if train_no:
        glovar.no_list = train_no.split()
    else:
        glovar.no_list = []
    glovar.zmode = zmode
    glovar.zzmode = zzmode
    glovar.gcd = gcd
    glovar.ktz = ktz
    glovar.remaining = remaining
    # if proxies_file:
    #     opts.proxies_file = proxies_file
    # if stations_file:
    #     opts.stations_file = stations_file
    # if cdn_file:
    #     opts.cdn_file = cdn_file
    tt = TrainTable()
    try:
        tt.update_trains()   # type: ignore
    except Exception as e:
        return e.__str__()
    return tt.output()


def handle_seats(seats,gloval):
    # 处理座位选择   seats（格式：一等座 二等座 无座） 
    for seat in seats.split():
        if seat not in SEAT_TYPES:
            continue
        gloval.seats_list.append(seat)
        gloval.seats_idx_list.append(SEAT_TYPES[seat])


def handle_bool(request,var:str):
    """处理请求bool默认值

    Args:
        request (_type_): 请求
        var (str): 字段

    Returns:
        _type_: 处理后的bool值
    """    
    res = False
    if request.values.__contains__(var):
        if request.values[var].lower() == 'true':
            res = True
        else:
            try:
                res = bool(int(request.values[var]))
            except Exception as e:
                return res
    return res
