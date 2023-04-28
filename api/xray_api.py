#!/usr/local/bin/python
# coding=utf-8

# xray配置相关api

from api.base_api import get_required
from api.base_api import get_not_required
import json
from flask import request
import subprocess
import re
from my_selenium.my_selenium import logging



# 添加xray客户端路由规则
def add_client_route_rule():
    # 要添加的规则(域名/子域名) 逗号分隔
    rules = get_required('rules')
    # 是否是子域名 is_subdomain  匹配当前域名与所有子域名  反之就是完全匹配 默认是子域名
    is_subdomain = get_not_required('is_subdomain',True)
    # 处理后的规则集
    handled_rules = []
    # 处理前的规则集
    unhandled_rules = rules.split(',')

    # 策略 支持direct proxy block
    strategy = get_required('strategy')
    # 定位 标识该规则放在 header body 还是 footer
    position = get_required('position')

    domain_regex = r'^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*$'

    def format(unhandled_rule:str):
        # 判断当前参数是否符合域名规则(正则匹配)
        match = re.match(domain_regex,unhandled_rule.strip())
        if match is None:
            raise RuntimeError(f'规则列表中有非域名规则: {unhandled_rule.strip()}!')
        if is_subdomain:
            # 当前域名和所有的子域名 可以自定义规则
            return unhandled_rule.strip()
        else:
            # 完全匹配
            return f'full:{unhandled_rule.strip()}'

    def choose(handled_rules,unhandled_rules,special_rules):
        for unhandled_rule in unhandled_rules:
            unhandled_rule = format(unhandled_rule)
            # 判断该规则是否最终添加
            flag = True
            for special_rule in special_rules:
                domains:list = special_rule['domain']
                if domains.__contains__(unhandled_rule):
                    flag = False
                    # 一旦碰到有相同的规则 直接退出循环
                    break
            if flag:
                handled_rules.append(unhandled_rule)
    

    # 若xray-parser不存在则clone
    print(subprocess.call('nsenter -m -u -i -n -p -t 1 sh -c "[ ! -d /root/code/xray-parser ] && cd /root/code && git clone https://github.com/nichuanfang/xray-parser.git"',shell=True))
    # 若xray-parser存在则pull
    print(subprocess.call('nsenter -m -u -i -n -p -t 1 sh -c "[ -d /root/code/xray-parser ] && cd /root/code/xray-parser && git checkout . && git checkout client && git pull"',shell=True))
    # 获取routing/routing_header.json routing/routing_body.json routing/routing_footer.json
    with open('/code/xray-parser/routing/routing_header.json') as header_file:
        header = json.load(header_file)

    with open('/code/xray-parser/routing/routing_body.json') as body_file:
        body = json.load(body_file)

    with open('/code/xray-parser/routing/routing_footer.json') as footer_file:
        footer = json.load(footer_file)

    

    match position:
        case 'header':
            header_rules:list = header['rules']
            # 判断当前域名是否已添加规则

            # 最终要添加的规则集
            handled_rules = []
            choose(handled_rules,unhandled_rules,header_rules)
            header_rules.append({
                'type': 'field',
                'outboundTag': strategy,
                'domain': handled_rules
            })
            with open('/code/xray-parser/routing/routing_header.json','w+') as w_header_file:
                json.dump(header,w_header_file)
        case 'body':
            body_rules:list = body['rules']
            handled_rules = []
            choose(handled_rules,unhandled_rules,body_rules)
            body_rules.append({
                'type': 'field',
                'outboundTag': strategy,
                'domain': handled_rules
            })
            with open('/code/xray-parser/routing/routing_body.json','w+') as w_body_file:
                json.dump(body,w_body_file)
        case 'footer':
            footer_rules:list = footer['rules']
            handled_rules = []
            choose(handled_rules,unhandled_rules,footer_rules)
            footer_rules.append({
                'type': 'field',
                'outboundTag': strategy,
                'domain': handled_rules
            })
            with open('/code/xray-parser/routing/routing_footer.json','w+') as w_footer_file:
                json.dump(footer,w_footer_file)
        case _:
            pass
    if len(handled_rules) == 0:
        return f'无需更新路由规则!'    
    user_name = 'github-actions[bot]'
    email = 'github-actions[bot]@users.noreply.github.com'
    # 指定用户和邮箱  git config user.name git config user.email
    print(subprocess.call(f'nsenter -m -u -i -n -p -t 1 sh -c "cd /root/code/xray-parser && git config user.name {user_name}"',shell=True))
    print(subprocess.call(f'nsenter -m -u -i -n -p -t 1 sh -c "cd /root/code/xray-parser && git config user.email {email}"',shell=True))
    # 提交信息
    commit_msg = 'chore:更新xray客户端路由规则'
    # git提交
    print(subprocess.call(f'nsenter -m -u -i -n -p -t 1 sh -c "cd /root/code/xray-parser && git add /root/code/xray-parser/routing/*.json && git commit /root/code/xray-parser/routing/*.json -m {commit_msg} && git push"',shell=True))
    logging.info(f'==================================xray客户端已更新{len(handled_rules)}条路由规则===============================================')
    return f'xray客户端已更新{len(handled_rules)}条路由规则!'


if __name__ == '__main__':
    add_client_route_rule()
    