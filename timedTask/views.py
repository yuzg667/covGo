from django.shortcuts import render

# Create your views here.

# 定时任务
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import configparser
from django.conf import settings
import sys, socket  # 解决uwsgi模式下apscheduler重复执行问题，http://www.h4ck.org.cn/2019/01/django-apscheduler-uwsgi-定时任务重复运行/
from timedTask.cron import *

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 47200))
except socket.error:
    print("!!!scheduler already started, DO NOTHING")
    #https://note.youdao.com/web/#/file/recent/note/wcp1566782277036579/  详解django-apscheduler的使用方法 - 掘金

try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # 设置定时任务，选择方式为interval，时间间隔为10s
    # 另一种方式为每天固定时间执行任务，对应代码为：
    # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
    @register_job(scheduler, "interval", seconds=30)  # minutes=10 seconds=5
    def my_job():
        cloneToTaskDir()
        getCov()
        generateHtmlReport()
    register_events(scheduler)
    scheduler.start()

except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()