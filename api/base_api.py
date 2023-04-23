#!/usr/local/bin/python
# coding=utf-8
from flask import request
from urllib.parse import parse_qs, urlparse

# 校验和格式化flask get请求参数
def get_required(param):
    if not request.values.__contains__(param):
        raise RuntimeError(f'{param}参数必填!')
    else:
        return request.values[param].replace(
            '\'', '').replace('\"', '')

# 校验和格式化flask get请求参数 指定默认值
def get_not_required(param, default=None):
    if not request.values.__contains__(param):
        return default
    else:
        return request.values[param].replace(
            '\'', '').replace('\"', '')
