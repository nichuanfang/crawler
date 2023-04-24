#!/bin/bash
# 重新构建镜像 (修改版本)
docker rm -vf crawler
docker rmi -f registry.cn-hangzhou.aliyuncs.com/jayzhou/crawler:latest
echo '开始构建镜像...'
docker build -t registry.cn-hangzhou.aliyuncs.com/jayzhou/crawler:latest /root/docker/dockerfile_work/crawler
echo '镜像构建完成!'
# 推送到阿里云镜像仓库
echo '推送镜像到阿里云镜像仓库...' 
docker push registry.cn-hangzhou.aliyuncs.com/jayzhou/crawler:latest
echo '推送镜像到阿里云镜像仓库完成!'
# 删除本地中间镜像
echo '开始清理本地中间镜像...'
docker rmi -f $(docker images | grep crawler | awk '{print $3}')
docker rmi -f ubuntu:latest
echo '本地残留镜像清理完成!'
# 执行docker-compose
echo 'docker-compose up...'
docker-compose -f /root/docker/docker-compose/docker-compose.yml up -d
echo 'docker-compose up completed!'
# 通过Bark发送推送消息
curl -L https://api.day.app/SxPmVcSCBLLRtuR9EVGt85/crawler已完成部署
