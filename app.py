from flask import Flask,request,jsonify

import json


from fk12306.glovar import Glovar
from fk12306.train import TrainTable


import datetime

app = Flask(__name__)

app.debug = True

@app.route(rule='/get',methods=['get'])
def get_http():
    return request.base_url


@app.route(rule='/post',methods=['post'])
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


def query_tickets(begin:str,end:str,offset:int,mode:int,type:int,seats:int,train_no:str):
    """查询余票(默认当天 普通模式 有票 高铁动车)

    Args:
        begin (str):出发地

        end (str):目的地

        offset (int):偏移量 距离今天的偏移量 默认为0 例如  1: 明天 -1:昨天

        mode (int):模式 0:普通模式(默认) 1:(高级模式) 2:(终极模式)

        type (int):车次类型 0:不过滤类型(默认) 1: 只看高铁动车城际  2: 只看普快特快直达等

        seats (int):座位类型 0:不过滤类型(默认) 1: 一等座  2: 二等座 3: 无座

        train_no(str):默认不限制 限制车次
    """ 
    # opts.fs = from_station
    # opts.ts = to_station
    # if date:
    #     opts.date = date
    # if seats:
    #     opts.seats = seats
    # if train_no:
    #     opts.train_no = train_no
    # opts.zmode = zmode
    # opts.zzmode = zzmode
    # opts.gcd = gcd
    # opts.ktz = ktz
    # opts.remaining = remaining
    # if proxies_file:
    #     opts.proxies_file = proxies_file
    # if stations_file:
    #     opts.stations_file = stations_file
    # if cdn_file:
    #     opts.cdn_file = cdn_file    


    data = {}



    date = (datetime.datetime.now()+datetime.timedelta(days=offset)).strftime('%Y-%m-%d')
    

    tt = TrainTable()
    tt.update_trains(data)
    tt.echo()



if __name__=='__main__':
    # 开启http服务
    app.run('127.0.0.1',port=5000)
    