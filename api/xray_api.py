#!/usr/local/bin/python
# coding=utf-8

# xray配置相关api

from api.base_api import get_required
from api.base_api import get_not_required
import json
import random
from flask import request
import subprocess
import re
from my_selenium.my_selenium import logging
# 判断该站点是域名
domain_regex = r'^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*$'

# 判断域名前缀是否符合规则 
prefix_regex = r''


# 生成uuid
def generate_uuid():
    return random.sample('0123456789abcdefghijklmnopqrstuvwxyz',16)

# 校验规则(基于域名)
def verify_rule(rule:str):
    split_res = rule.strip().split(':')
    if len(split_res) == 1:
        # 不包含：  直接校验域名
        match = re.match(domain_regex,split_res[0])
        if match is None:
            raise RuntimeError(f'规则{split_res[0]}不是一个合法的域名!')
        pass


    return ''

# 若xray-parser不存在则clone
print(subprocess.call('nsenter -m -u -i -n -p -t 1 sh -c "[ ! -d /root/code/xray-parser ] && cd /root/code && git clone https://github.com/nichuanfang/xray-parser.git"',shell=True))
# 若xray-parser存在则pull
print(subprocess.call('nsenter -m -u -i -n -p -t 1 sh -c "[ -d /root/code/xray-parser ] && cd /root/code/xray-parser && git checkout . && git checkout client && git pull"',shell=True))
# 获取routing/routing_header.json routing/routing_body.json routing/routing_footer.json
with open('/code/xray-parser/routing/routing_header.json') as header_file:
    header:dict = json.load(header_file)
    # 头部规则集
    header_rules:list[str] = []
    for rule_entity in header['rules']:
        try:
            header_rules.__add__(rule_entity['domain'])
        except:
            continue

with open('/code/xray-parser/routing/routing_body.json') as body_file:
    body:dict = json.load(body_file)
    # body规则集
    body_rules:list[str] = []
    for rule_entity in body['rules']:
        try:
            body_rules.__add__(rule_entity['domain'])
        except:
            continue

with open('/code/xray-parser/routing/routing_footer.json') as footer_file:
    footer:dict = json.load(footer_file)
    # 尾部规则集
    footer_rules:list[str] = []
    for rule_entity in footer['rules']:
        try:
            footer_rules.__add__(rule_entity['domain'])
        except:
            continue



def format(unhandled_rule:str):
        judged_rule = unhandled_rule.strip()
        # 判断当前参数是否符合域名规则(正则匹配)
        domain_match = re.match(domain_regex,judged_rule)
        prefix_match = re.match(prefix_regex,judged_rule)
        if domain_match is None:
            raise RuntimeError(f'规则列表中有非域名规则: {judged_rule}!')
            # 当前域名和所有的子域名 可以自定义规则
        return judged_rule


# 添加一条xray客户端路由规则  get请求添加
def add_client_route_rule():
    # 要添加的规则(域名/子域名) 域名前缀需要正则校验!
    rule = get_required('rule')
    # 校验该规则是否合规 （基于domain的规则）
    rule = verify_rule(rule)
    # 规则id 非必填 如果存在 表示该条记录添加到当前规则下 如果不存在 新增一个规则体 
    rule_id = get_not_required('rule_id','')
    # 策略 支持direct proxy block
    strategy = get_required('strategy')
    # 定位 标识该规则放在 header body 还是 footer
    position = get_required('position')

    # 当前规则所属的规则集 header | body | footer
    position_data = {}
    # 当前位置及之前的所有规则组成的超集
    pre_rules = []
    match position:
        case 'header':
            position_data:dict = header
            pre_rules:list = header_rules
        case 'body':
            position_data:dict = body
            pre_rules:list = header_rules.__add__(body_rules)
        case 'footer':
            position_data:dict = footer
            pre_rules:list = header_rules.__add__(body_rules).__add__(footer_rules)
    pass
    position_rules:list = position_data['rules']

    # 如果之前有配置过相同的规则 就会让这条规则失效! 所以应该不予添加 并返回友好提示
    if pre_rules.__contains__(rule):
            raise RuntimeError('已配置该规则!')
    
    if rule_id == '':
        # 新增规则体
        position_rules.append({
            'id': generate_uuid(),
            'type': 'field',
            'outboundTag': strategy,
            'domain': ''
        })
    else:
        # 修改规则体 往已存在的规则中添加域名/ip 仍需要判断之前没配置过

        pass
    # 最终要添加的规则集
    # choose(handled_rules,unhandled_rules,position_rules)
    # position_rules.append({
    #     'type': 'field',
    #     'outboundTag': strategy,
    #     'domain': handled_rules
    # })
    with open(f'/code/xray-parser/routing/routing_{position}.json','w+') as w_file:
        json.dump(position_data,w_file)
    pass

    
    handled_rules = []
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



# 添加多条路由规则 post请求
def batch_add_client_route_rule():
    pass

# 删除xray客户端路由规则  
def del_client_route_rule():
    # 要删除的规则(域名/子域名) 逗号分隔
    pass

# 查看xray客户端路由配置
def client_route_rule_preview():
    # 要删除的规则(域名/子域名) 逗号分隔
    rules = get_required('rules')
    # 是否是子域名 is_subdomain  匹配当前域名与所有子域名  反之就是完全匹配 默认是子域名
    is_subdomain = get_not_required('is_subdomain',True)

    pass


if __name__ == '__main__':
    add_client_route_rule()
    