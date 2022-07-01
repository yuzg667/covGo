#!/bin/bash
#修改go配置代理
export PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:/root/bin:/root/.go/bin
go env -w GOPROXY=https://goproxy.cn,direct

#安装相关包
go install github.com/axw/gocov/gocov@latest
go install github.com/AlekSi/gocov-xml@latest
go install github.com/matm/gocov-html@latest
source /root/.bashrc
source /etc/profile

chmod 777 /home/workspace/*
# /home/workspace/covGo/cmdTools/goc server > /home/workspace/goc.log
# python3 /home/workspace/covGo/manage.py runserver 0.0.0.0:8899 > /home/workspace/covgo.log
