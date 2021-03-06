from django.shortcuts import render
from cov.models import reports as reportsModel
from cov.models import covTask as covTaskModel
# Create your views here.

# 根据url中的id查询覆盖率报告文件 http://127.0.0.1:8899/covHtml/?reportId=164
def covHtml(request):
    reportId = request.GET.get("reportId")
    reportObj = reportsModel.objects.filter(id=reportId)
    if len(reportObj) > 0:
        covTaskId = reportObj[0].covTaskId
        htmlFileName = reportObj[0].htmlFileName
        covTaskObj = covTaskModel.objects.filter(id=covTaskId)
        projectName = covTaskObj[0].projectName

    return render(request, f'''{projectName}/{covTaskId}/{htmlFileName}''', {
                                                        })

def covHtmlList(request):
    covTaskId = request.GET.get("covTaskId")
    # 查询增量报告
    resObj = reportsModel.objects.raw(f'''SELECT r.id,
                                                r.runId,
                                                c.projectName,
                                                c.covTaskName,
                                                c.branch,
                                                c.compareBranch,
                                                r.createTime,
                                                r.diffLineTotal,
                                                r.missLineTotal,
                                                r.coverage,
                                                r.isCrawled
                                                 FROM `cov_reports` r
                                                LEFT JOIN cov_covtask c ON r.covTaskId = c.id
                                                WHERE r.covTaskId =  {covTaskId} AND r.type = 0 AND r.status = 1  AND  diffLineTotal != '-1' ORDER BY createTime DESC
                                        ''')
    projectName = None
    covTaskName = None
    if len(resObj) > 0:
        projectName = resObj[0].projectName
        covTaskName = resObj[0].covTaskName
    # 查询全量报告
    resFullCovHtmlObj = reportsModel.objects.raw(f'''SELECT r.id,
                                                r.runId,
                                                c.projectName,
                                                c.covTaskName,
                                                c.branch,
                                                c.compareBranch,
                                                r.createTime,
                                                r.diffLineTotal,
                                                r.missLineTotal,
                                                r.coverage,
                                                r.isCrawled
                                                 FROM `cov_reports` r
                                                LEFT JOIN cov_covtask c ON r.covTaskId = c.id
                                                WHERE r.covTaskId =  {covTaskId} AND r.type = 1 AND r.status = 1  AND  diffLineTotal != '-1' ORDER BY createTime DESC LIMIT 1
                                        ''')
    return render(request, 'covTaskReportsList.html', {'resObj':resObj,
                                                       "projectName": projectName,
                                                       "covTaskName": covTaskName,
                                                       'resFullCovHtmlObj': resFullCovHtmlObj,
                                                        })


def covTaskList(request):
    reportId = request.GET.get("reportId")
    covTaskListObj = covTaskModel.objects.filter(deleted=0).order_by('-createTime')
    return render(request, 'covTaskList.html', {'covTaskListObj':covTaskListObj
                                                 })


