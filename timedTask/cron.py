import time

from utils.gitHandle import *
from cov.models import project as projectModel
from cov.models import covTask as covTaskModel
from utils.logs import MyLog
from django.db import connection


# 初次创建覆盖率任务后，任务状态=0，需要对0状态的进行clone代码到指定的任务目录
# todo 这个任务期望每1分钟检查一次
def cloneToTaskDir():
    # 查出库里有哪些是0状态的数据待clone
    cursor = connection.cursor()
    cursor.execute('''SELECT c.id AS cid, p.id AS pid, gitName,gitUrl,gitPwd,covTaskName FROM cov_covtask c
                                    LEFT JOIN cov_project p ON  c.projectId = p.id
                                    WHERE c.deleted = 0 AND c.status=0 AND p.deleted = 0 
                                        ''')
    resObj = cursor.fetchall()
    i = 0
    # 依次下载
    for res in resObj:
        res = resObj[i]
        username = res.gitName
        pwd = res.gitPwd
        gitUrl = res.gitURL
        gitProjectName = res.projectName
        covTaskId = res.cid
        covTaskName = res.covTaskName
        MyLog.info(f"首次下载--start git clone--覆盖率任务名称:{covTaskName}--仓库地址:{gitUrl}")
        # TODO 当clone异常的时候跳过执行下一个任务
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
# def getCov():
