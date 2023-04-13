#!/bin/bash
nohup /usr/local/bin/python /root/code/fk12306/app.py 1>/var/log/fk12306.log 2>&1 &
