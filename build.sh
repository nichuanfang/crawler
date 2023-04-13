#!/bin/bash
/usr/local/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ./requirements.txt
/usr/local/bin/python setup.py install
/usr/local/bin/python app.py
bash stop.sh
bash start.sh
docker restart nginx
