import time
from django.conf import settings
from utils.execCmd import execCmd
from utils.gitHandle import cloneCode, pullCode, checkOutBranch, downloadPath
from cov.models import project as projectModel
from cov.models import covTask as covTaskModel
from cov.models import covTaskHistory as covTaskHistoryModel
from cov.models import reports as reportsModel
from utils.logs import MyLog
from django.db import connection
from utils.covUtils import *


# 初次创建覆盖率任务后，任务状态=0，需要对0状态的进行clone代码到指定的任务目录
# todo 这个任务期望每1分钟检查一次
def cloneToTaskDir():
    MyLog.info(f"-----cloneToTaskDir任务开始执行-----")
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
    i = i + 1

# 获取覆盖率
def getCov():
    MyLog.info(f"-----getCov任务开始执行-----")
    # 1、获取被测试分支
    # 查出库里有哪些是1和3状态的数据待pull、获取覆盖率
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
                                        WHERE c.deleted = 0 AND c.status IN(1,3,31) AND p.deleted = 0 
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
        MyLog.info(f"开始搜集覆盖率--覆盖率任务名称:{covTaskName}--clientServerList:{clientServerHostPort}")
        try:
            # 拉取代码
            pullCode(gitProjectName, covTaskId)
            # 切换分支
            checkOutBranch(gitProjectName, covTaskId, branch)
            # 获取被测机器列表 todo 与填写的进行对比
            clientServerList = eval(clientServerHostPort)
            # 拉取覆盖率
            t = datetime.now().strftime('%Y%m%d%H%M%S%f')
            for clientServer in clientServerList:
                covPath = covReportsPath(gitProjectName, covTaskId)
                runId = generateRunId(t, covTaskId, None)
                covFileName = generateRunId(t, covTaskId, originalHostPort=clientServer)
                print(covPath)
                print(runId)
                # 拉取正常的入库status=1
                try:
                    # getCovcmd = f'''{settings.BASE_DIR}/cmdTools/goc profile --center={clientServer} -o {covPath}/{covFileName}.cov'''
                    getCovcmd = f'''goc profile --center={clientServer} -o {covPath}/{covFileName}.cov'''
                    MyLog.info(f'getCovcmd:{getCovcmd}')
                    execCmd(getCovcmd)
                    p = covTaskHistoryModel(runId = runId,
                                            covTaskId = covTaskId,
                                            clientServerHostPort = clientServer,
                                            covFileName = covFileName + ".cov",
                                            status = 3,
                                           )
                    p.save()
                    covTaskModel.objects.filter(id=covTaskId).update(
                        status = 31,
                        updateTime=time.strftime("%Y-%m-%d %H:%M:%S")
                    )
                    MyLog.info(f"收集覆盖率完毕--覆盖率任务名称:{covTaskName}--服务器:{clientServer}")
                # 拉取非正常的入库status=2
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
            MyLog.error(f"获取覆盖率cov文件异常--覆盖率任务名称:{covTaskName}--仓库地址:{gitUrl}，报错如下: {str(e)}")
            covTaskModel.objects.filter(id=covTaskId).update(
                                                             updateTime=time.strftime("%Y-%m-%d %H:%M:%S")
                                                             )
    i = i + 1

# 生成覆盖率报告
def generateHtmlReport():
    MyLog.info(f"-----generateHtmlReport任务开始执行-----")
    # 查出库里状态是1的covTaskId
    cursor = connection.cursor()
    cursor.execute('''SELECT c.id AS cid,
                                p.id AS pid, 
                                gitName,
                                gitUrl,
                                gitPwd,
                                compareBranch,
                                covTaskName,
                                p.projectName 
                                FROM cov_covtask c
                                    LEFT JOIN cov_project p ON  c.projectId = p.id
                                    WHERE c.deleted = 0 AND c.status in (31) AND p.deleted = 0 
                                        ''')
    resObj = cursor.fetchall()
    i = 0
    # 依次
    for res in resObj:
        res = resObj[i]
        compareBranch = res[5]
        covTaskName = res[6]
        gitProjectName = res[7]
        covTaskId = res[0]
        covPath = covReportsPath(gitProjectName, covTaskId)
        t = datetime.now().strftime('%Y%m%d%H%M%S%f')
        runId = generateRunId(t, covTaskId, None)
        mergeCovName = "merge" + str(runId)
        try:
            MyLog.info(f"开始生成html--覆盖率任务名称:{covTaskName}")
            # 合并全部覆盖率文件
            # mergeCmd = f'''{settings.BASE_DIR}/cmdTools/goc merge {covPath}/*.cov -o {covPath}/{mergeCovName}.cov'''
            mergeCmd = f'''goc merge {covPath}/*.cov -o {covPath}/{mergeCovName}.cov'''
            MyLog.info(f'mergeCmd:{mergeCmd}')
            execCmd(mergeCmd)
            # 把历史cov文件移到bak文件夹
            mvTobakCmd = f'''mkdir -p {covPath}/bak && mv {covPath}/*.cov {covPath}/bak'''
            MyLog.info(f'mvTobakCmd:{mvTobakCmd}')
            execCmd(mvTobakCmd)
            # 把最新的cov文件移出来，下次merge使用
            mvNewMergeOutCmd = f'''mv {covPath}/bak/{mergeCovName}.cov {covPath}'''
            MyLog.info(f'mvNewMergeOutCmd:{mvNewMergeOutCmd}')
            execCmd(mvNewMergeOutCmd)
            # 把cov转换成xml
            # covToXmlCmd = f'''cd {covPath} && gocov convert {covPath}/{mergeCovName}.cov | gocov-xml > {covPath}/{mergeCovName}.xml'''
            gitCodePath = downloadPath(gitProjectName, covTaskId)
            covToXmlCmd = f'''cd {gitCodePath} && {settings.BASE_DIR}/cmdTools/gocov convert {covPath}/{mergeCovName}.cov | {settings.BASE_DIR}/cmdTools/gocov-xml > {covPath}/{mergeCovName}.xml'''
            MyLog.info(f'covToXmlCmd:{covToXmlCmd}')
            execCmd(covToXmlCmd)
            # xml转换成后html文件
            xmlToHtmlCmd = f'''cd {gitCodePath} && diff-cover {covPath}/{mergeCovName}.xml --compare-branch={compareBranch} --html-report {covPath}/{mergeCovName}.html'''
            MyLog.info(f'xmlToHtmlCmd:{xmlToHtmlCmd}')
            execCmd(xmlToHtmlCmd)
            MyLog.info(f"生成html完毕--覆盖率任务名称:{covTaskName}--生成文件：{mergeCovName}.html")
            p = reportsModel(runId=runId,
                             covTaskId=covTaskId,
                             htmlFileName = mergeCovName + '.html',
                             status = 1,
                             )
            p.save()
        except Exception as e:
            p = reportsModel(runId=runId,
                             covTaskId=covTaskId,
                             htmlFileName = mergeCovName + '.html',
                             status = 2,
                             )
            p.save()
            MyLog.error(f"生成html失败--覆盖率任务名称:{covTaskName}--生成文件：{mergeCovName}.html，报错如下: {str(e)}")
    i = i + 1

# 从html报告中爬取覆盖率
def getCovFromHtml():
    MyLog.info(f"-----开始爬取覆盖率-----")
    # 查出库里状态是1的covTaskId
    cursor = connection.cursor()
    cursor.execute('''SELECT r.id,
                        r.runId,
                        c.projectName,
                        c.id,
                        c.covTaskName,
                        c.branch,
                        c.compareBranch,
                        r.createTime,
                        r.diffLineTotal,
                        r.missLineTotal,
                        r.coverage,
                        r.isCrawled,
                        r.htmlFileName
                         FROM `cov_reports` r
                        LEFT JOIN cov_covTask c ON r.covTaskId = c.id
                        WHERE  r.status = 1 AND r.isCrawled = 0 ORDER BY createTime ASC 
                                            ''')
    resObj = cursor.fetchall()
    i = 0
    # 依次
    for res in resObj:
        res = resObj[i]
        id = res[0]
        gitProjectName = res[2]
        covTaskId = res[3]
        htmlFileName = res[12]
        htmlPath = os.path.join(covReportsPath(gitProjectName,covTaskId), htmlFileName)
        try:
            covRes = crawlCovFromHtml(htmlPath)
            covRes['diffLineTotal']
            reportsModel.objects.filter(id=id).update(
                                                            isCrawled=1,
                                                            diffLineTotal=covRes['diffLineTotal'],
                                                            missLineTotal=covRes['missLineTotal'],
                                                            coverage=covRes['coverage'],
                                                            updateTime=time.strftime("%Y-%m-%d %H:%M:%S")
                                                             )
            MyLog.info(f"-----爬取covTask:{covTaskId}成功-----")
        except Exception as e:
            reportsModel.objects.filter(id=id).update(
                                                            isCrawled=2,
                                                            diffLineTotal="-1",
                                                            missLineTotal="-1",
                                                            coverage="-1",
                                                            updateTime=time.strftime("%Y-%m-%d %H:%M:%S")
                                                             )
            MyLog.error(f"-----爬取covTask:{covTaskId}失败-----，报错如下: {str(e)}")

        i = i + 1