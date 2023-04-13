#!/bin/bash
/usr/local/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ./requirements.txt
bash stop.sh
bash start.sh
docker restart nginx
