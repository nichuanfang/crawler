from re import I
from flask import Flask, request, jsonify

import json


from fk12306.train import TrainTable
from fk12306.glovar import Glovar
from fk12306.glovar import SEAT_TYPES
from fk12306 import utils


import datetime

app = Flask(__name__)

# app.debug = True


@app.route(rule='/get', methods=['get'])
def get_http():
    """测试get调用

    Returns:
        _type_: url
    """    
    return request.base_url


@app.route(rule='/post', methods=['post'])
def post_http():
    """测试http调用

    Returns:
        _type_: json格式化数据
    """
    if not request.data:
        return 'Fail'
    params = request.data.decode('utf-8')
    # 获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据晶具体情况而定
    params = json.loads(params)
    print(params)
    return jsonify(params)

@app.route(rule='/ticket', methods=['get'])
def ticket():
    """查询余票

    Returns:
        _type_: 余票信息
    """    
    values = request.values
    if not request.values.__contains__('begin'):
        return 'begin参数必填!'
    else:
        begin = request.values['begin'].replace('\'','').replace('\"','')
    if not request.values.__contains__('end'):
        return 'end参数必填!'
    else:
        end = request.values['end'].replace('\'','').replace('\"','')
    if request.values.__contains__('offset'):
        try:
            offset = int(request.values['offset'])
            if offset < 0:
                return 'offset必须大于等于0'
        except Exception as e:
            offset = 0
    else:
        offset = 0
    if request.values.__contains__('seats'):
        seats = request.values['seats']
    else:
        seats = None
    if request.values.__contains__('train_no'):
        train_no = request.values['train_no']
    else:
        train_no = None
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
        return '起点{}不是市级地点!'.format(begin)
    glovar.fs = begin

    glovar.ts_code = utils.station_to_code(end)
    if glovar.ts_code is None or glovar.ts_code == '':
        return '终点{}不是市级地点!'.format(end)
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

if __name__ == '__main__':
    # 开启http服务
    # query_tickets('杭州','武汉')
    app.run('0.0.0.0', port=5000)
