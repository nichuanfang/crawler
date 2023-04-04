from flask import Flask, request, jsonify

import json


from fk12306.glovar import Glovar
from fk12306.train import TrainTable


import datetime

app = Flask(__name__)

app.debug = True


@app.route(rule='/get', methods=['get'])
def get_http():
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


def query_tickets(begin: str, end: str, **kwargs):
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
    data = {}
    data['fs'] = begin
    data['ts'] = end
    data['date'] = (datetime.datetime.now() +
                    datetime.timedelta(days=offset)).strftime('%Y-%m-%d')
    if kwargs['seats']:
        match kwargs['seats']:
            case 1:
                data['seats'] = '一等座'
            case 2:
                data['seats'] = '二等座'
            case 3:
                data['seats'] = '无座'
            case other:
                pass
    if kwargs['train_no']:
        data['train_no'] = kwargs['train_no']
    if kwargs['mode']:
        match kwargs['mode']:
            case 1:
                data['zmode'] = True
                data['zzmode'] = False
            case 2:
                data['zmode'] = False
                data['zzmode'] = True
            case other:
                data['zmode'] = False
                data['zzmode'] = False
        pass
    if kwargs['type']:
        match kwargs['type']:
            case 1:
                data['gcd'] = True
                data['ktz'] = False
            case 2:
                data['gcd'] = False
                data['ktz'] = True
            case other:
                data['gcd'] = False
                data['ktz'] = False
    data['remaining'] = True
    # todo 加载代理文件和cdn
    # if proxies_file:
    #     opts.proxies_file = proxies_file
    # if stations_file:
    #     opts.stations_file = stations_file
    # if cdn_file:
    #     opts.cdn_file = cdn_file

    tt = TrainTable()
    tt.update_trains(data)  # type: ignore
    tt.echo()


if __name__ == '__main__':
    # 开启http服务
    # query_tickets('杭州','武汉')
    # app.run('127.0.0.1', port=5000)
    query_tickets('杭州','五哈尼')
    pass
