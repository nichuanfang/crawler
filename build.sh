#!/bin/bash
# 重新构建镜像 (修改版本)
docker rm -vf crawler
docker build -t registry.cn-hangzhou.aliyuncs.com/jayzhou/crawler:latest --build-arg CRAWLER_VERSION=v1.0.0 .
# 推送到阿里云镜像仓库
docker push registry.cn-hangzhou.aliyuncs.com/jayzhou/crawler:latest
# 删除本地镜像
docker rmi -f $(docker images | grep crawler | awk '{print $3}')
docker rmi -f ubuntu:latest
# 执行docker-compose
docker-compose -f /root/docker/docker-compose/docker-compose.yml up -d
