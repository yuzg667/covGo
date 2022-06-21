import os
from datetime import datetime

import requests
from django.conf import settings
import time, re
# 获取被测机器列表
def getClientServerList():
    # res = requests.get("http://127.0.0.1:7777/v1/cover/list")
    res = requests.get("http://192.168.56.101:7777/v1/cover/list")
    print(res.json())
    clientServerList = res.json()['simple-go-server']
    print(clientServerList)
    return clientServerList

# 定义覆盖率文件存储位置
def covReportsPath(gitProjectName,covTaskId):
    covReportsPath = os.path.join(settings.BASE_DIR, '..', 'covFilesDir', 'covReports',str(gitProjectName).strip(), str(covTaskId).strip())
    return covReportsPath

# 生成runId
def generateRunId(covTaskId,originalHostPort):
    t = datetime.now().strftime('%Y%m%d%H%M%S%f')
    patternHostPort = re.compile(r'''\/\/(.*)''')
    if originalHostPort:
        hostPort = re.findall(patternHostPort,str(originalHostPort))[0]
        hostPort = hostPort.replace(':','_')
        res = f'''{t}-{covTaskId}-{hostPort}'''
    else:
        res = f'''{t}-{covTaskId}'''
    return res
# hostPort = 'http://192.168.56.101:46599'
# generateRunId(1,hostPort)