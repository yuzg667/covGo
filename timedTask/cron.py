import time

from utils.execCmd import execCmd
from utils.gitHandle import *
from cov.models import project as projectModel
from cov.models import covTask as covTaskModel
from cov.models import covTaskHistory as covTaskHistoryModel
from utils.logs import MyLog
from django.db import connection
from utils.covUtils import *


# 初次创建覆盖率任务后，任务状态=0，需要对0状态的进行clone代码到指定的任务目录
# todo 这个任务期望每1分钟检查一次
def cloneToTaskDir():
    # 查出库里有哪些是0状态的数据待clone
    cursor = connection.cursor()
    cursor.execute('''SELECT c.id AS cid,
                                p.id AS pid, 
                                gitName,
                                gitUrl,
                                gitPwd,
                                covTaskName,
                                p.projectName 
                                FROM cov_covtask c
                                    LEFT JOIN cov_project p ON  c.projectId = p.id
                                    WHERE c.deleted = 0 AND c.status=0 AND p.deleted = 0 
                                        ''')
    resObj = cursor.fetchall()
    i = 0
    # 依次下载
    for res in resObj:
        res = resObj[i]
        username = res[2]
        pwd = res[4]
        gitUrl = res[3]
        gitProjectName = res[6]
        covTaskId = res[0]
        covTaskName = res[5]
        MyLog.info(f"首次下载--start git clone--覆盖率任务名称:{covTaskName}--仓库地址:{gitUrl}")
        try:
            cloneCode(username, pwd, gitUrl, gitProjectName, covTaskId)
            MyLog.info(f"首次下载完毕--end git clone--覆盖率任务名称:{covTaskName}--仓库地址:{gitUrl}")
            covTaskModel.objects.filter(id=covTaskId).update(status=1,
                                                             updateTime=time.strftime("%Y-%m-%d %H:%M:%S")
                                                             )
        except Exception as e:
            MyLog.error(f"首次下载异常--end git clone--覆盖率任务名称:{covTaskName}--仓库地址:{gitUrl}，报错如下: {str(e)}")
            covTaskModel.objects.filter(id=covTaskId).update(status=2,
                                                             updateTime=time.strftime("%Y-%m-%d %H:%M:%S")
                                                             )

# 获取覆盖率
def getCov():
    # 1、获取被测试分支
    # 查出库里有哪些是0状态的数据待clone
    cursor = connection.cursor()
    cursor.execute('''SELECT c.id AS cid,
                                    p.id AS pid, 
                                    gitName,
                                    gitUrl,
                                    gitPwd,
                                    covTaskName,
                                    p.projectName ,
                                    c.branch,
                                    c.clientServerHostPort
                                    FROM cov_covtask c
                                        LEFT JOIN cov_project p ON  c.projectId = p.id
                                        WHERE c.deleted = 0 AND c.status IN(1,3) AND p.deleted = 0 
                                            ''')
    resObj = cursor.fetchall()
    i = 0
    # 依次下载
    for res in resObj:
        res = resObj[i]
        username = res[2]
        pwd = res[4]
        gitUrl = res[3]
        gitProjectName = res[6]
        covTaskId = res[0]
        covTaskName = res[5]
        branch = res[7]
        clientServerHostPort = res[8]
        MyLog.info(f"开始搜集覆盖率--start git clone--覆盖率任务名称:{covTaskName}--clientServer:{clientServerHostPort}")
        try:
            # 拉取代码
            pullCode(gitProjectName, covTaskId)
            # 切换分支
            checkOutBranch(gitProjectName, covTaskId, branch)
            # 获取被测机器列表 todo 与填写的进行对比
            clientServerList = eval(clientServerHostPort)
            # 拉取覆盖率
            for clientServer in clientServerList:
                # 拉取正常的入库status=1
                try:
                    covReportsPath = covReportsPath(gitProjectName,covTaskId)
                    runId = generateRunId(covTaskId, originalHostPort=clientServer)
                    execCmd(f'goc profile --center={clientServer} -o {covReportsPath}/{runId}.cov''')
                    p = covTaskHistoryModel(runId = runId,
                                            covTaskId = covTaskId,
                                            clientServerHostPort = clientServer,
                                            covFileName = runId + ".cov",
                                            status = 1,
                                           )
                    p.save()
                    MyLog.info(f"收集覆盖率完毕--覆盖率任务名称:{covTaskName}--服务器:{clientServer}")
                # 拉取正常的入库status=2
                except Exception as e:
                    p = covTaskHistoryModel(runId=runId,
                                            covTaskId=covTaskId,
                                            clientServerHostPort=clientServer,
                                            covFileName=runId + ".cov",
                                            status=2,
                                            )
                    p.save()
                    MyLog.info(f"收集覆盖率异常--覆盖率任务名称:{covTaskName}--服务器:{clientServer}，报错如下: {str(e)}")

        except Exception as e:
            MyLog.error(f"pull下载异常--end git pull--覆盖率任务名称:{covTaskName}--仓库地址:{gitUrl}，报错如下: {str(e)}")
            covTaskModel.objects.filter(id=covTaskId).update(status=4,
                                                             updateTime=time.strftime("%Y-%m-%d %H:%M:%S")
                                                             )



