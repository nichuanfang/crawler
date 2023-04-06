#!/bin/bash
ps -ef | grep fk12306 | grep -v grep | awk '{print $2}' | xargs kill -9
