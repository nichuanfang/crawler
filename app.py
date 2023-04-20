#!/usr/local/bin/python
# coding=utf-8 
from flask import Flask
from api import fk12306_api

app = Flask(__name__)

# app.debug = True

@app.route(rule='/fk12306/ticket', methods=['get'])
def ticket():
    """查询余票

    Returns:
        _type_: 余票信息
    """    
    return fk12306_api.ticket()



if __name__ == '__main__':
    # 开启http服务
    # query_tickets('杭州','武汉')
    app.run('0.0.0.0', port=5000)
