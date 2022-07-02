import os
from git.repo import Repo
from django.conf import settings

# https://blog.csdn.net/martinlinux/article/details/119874787

# 定义下载代码的路径：由项目名/覆盖率任务id组成
def downloadPath(gitProjectName,covTaskId):
    gitDownloadPath = os.path.join(settings.BASE_DIR, '..', 'covFilesDir', str(gitProjectName).strip(), str(covTaskId).strip())
    return gitDownloadPath

# 克隆仓库，不指定分支
def cloneCode(username,pwd,gitUrl,gitProjectName,covTaskId):
    # Repo.clone_from('https://yuzg667:22222@gitee.com/yuzg667/simple-go-server.git', to_path=download_path, branch='main')
    # Repo.clone_from('https://yuzg667:22222@gitee.com/yuzg667/simple-go-server.git', to_path=downloadPath("..","tttt"))
    codeDir = downloadPath(gitProjectName,covTaskId)
    Repo.clone_from(f'https://{username}:{pwd}@{gitUrl}', to_path=codeDir)

# 获取远程分支列表
def getRemoteBranchList(gitProjectName, covTaskId):
    codeDir = downloadPath(gitProjectName, covTaskId)
    repo = Repo(codeDir)
    git = repo.git
    # 获取远程所有分支
    remoteBranchsString = git.execute("git branch -r")
    remoteBranchs = remoteBranchsString.split('\n')
    remoteBranchsList = []
    # 去除空格分支名两端的空格
    for remoteBranch in remoteBranchs:
        remoteBranchsList.append(remoteBranch.strip())
    return remoteBranchsList

# 远程拉取代码
def pullCode(gitProjectName, covTaskId):
    codeDir = downloadPath(gitProjectName, covTaskId)
    repo = Repo(codeDir)
    repo.remote().pull()

# gitProjectName = ".."
# covTaskId = "gitTest22"
# codeDir = downloadPath(gitProjectName, covTaskId)
#
# cloneCode('yuzg667','xxx','gitee.com/yuzg667/web-app.git',gitProjectName,covTaskId)
#
# repo = Repo(codeDir)
# getRemoteBranchList(gitProjectName, covTaskId)
# pullCode(gitProjectName, covTaskId)