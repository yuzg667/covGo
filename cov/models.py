# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class project(models.Model):
    id = models.AutoField(primary_key = True)
    projectName = models.CharField('项目名称',max_length=255)
    gitURL = models.CharField('git地址：形如gitee.com/xxx/yyy.git',max_length=255)
    gitName = models.CharField('git登录名',max_length=255)
    gitPwd = models.CharField('git密码',max_length=255)
    deleted = models.IntegerField('是否删除',default='0')
    createTime = models.DateTimeField('创建时间',auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def __str__(self):
        return self.projectName
    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.deleted = '1'
        self.save()

from cov.func import getProjectChoices, getProjectName
class covTask(models.Model):
    id = models.AutoField('任务ID',primary_key=True)
    covTaskName = models.CharField('任务名称',blank=True, null=True,max_length=30)
    projectName = models.CharField('所属项目名称',blank=True, null=True,max_length=255)
    projectId = models.IntegerField('所属项目ID',blank=True, null=True, choices= getProjectChoices())
    branch = models.CharField('被测分支',blank=True,null=True, max_length=100)
    compareBranch = models.CharField('基准分支(对比分支)',blank=True,null=True,max_length=100)
    clientServerHostPort = models.TextField('''被测服务host和port，list结构。如：['http://192.168.56.101:46599','http://192.168.56.102:46599']''',blank=True,null=True)
    status = models.CharField('状态：0新建；1clone完成；2clone异常；3成功-待首次获取覆盖率；31成功-待再次获取覆盖率；4获取覆盖率失败',blank=True,null=True,max_length=30, default='0')
    deleted = models.IntegerField('是否删除',blank=True,default='0',null=True)
    startTime = models.DateTimeField('搜集覆盖率开始时间',blank=True,null=True)
    endTime = models.DateTimeField('搜集覆盖率结束时间',blank=True,null=True)
    lastCollectTime = models.DateTimeField('上次收集时间',blank=True,null=True)
    createTime = models.DateTimeField('创建时间',auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间',null=True)
    class Meta:
        verbose_name = '覆盖率任务'
        verbose_name_plural = '覆盖率任务'
    def __str__(self):
        return self.covTaskName
    def __init__(self, *args, **kargs):
        super(covTask, self).__init__(*args, **kargs)
        self._meta.get_field('projectId').choices = getProjectChoices()
    # 重写save方法：在下拉框projectId保存时，同时保存projectName入库
    def save(self, *args, **kwargs):
        self.projectName = getProjectName(self.projectId)
        super(covTask, self).save(*args, **kwargs)
    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.deleted = '1'
        self.save()



# 收集覆盖率文件cov历史
class covTaskHistory(models.Model):
    id = models.AutoField(primary_key=True)
    runId = models.CharField('runId',blank=True,null=True,max_length=50)
    covTaskId = models.CharField('covTask表的ID',blank=True,null=True,max_length=30)
    clientServerHostPort = models.CharField('covTask表的ID',blank=True,null=True,max_length=30)
    covFileName = models.CharField('覆盖率文件名',blank=True,null=True,max_length=50)
    status = models.CharField('状态：0初始化；1获取cov文件成功；2获取cov文件失败；3已被merge合并过',blank=True,null=True,max_length=30)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.runId

# 历史报告
class reports(models.Model):
    id = models.AutoField(primary_key=True)
    runId = models.CharField('runId',blank=True,null=True,max_length=50)
    covTaskId = models.CharField('covTask表的ID',blank=True,null=True,max_length=30)
    type = models.CharField('覆盖率类型：0增量覆盖率，1全量覆盖率', max_length=1, default='0')
    htmlFileName = models.CharField('覆盖率文件名',blank=True,null=True,max_length=50)
    diffLineTotal = models.CharField('总变动行数',blank=True,null=True,max_length=50)
    missLineTotal = models.CharField('未覆盖行数',blank=True,null=True,max_length=50)
    coverage = models.CharField('覆盖率',blank=True,null=True,max_length=50)
    isCrawled = models.IntegerField('是否已经爬取，0未爬取，1已爬取成功,2失败',blank=True,default='0',null=True)
    status = models.CharField('状态：1成功，2失败',blank=True,null=True,max_length=30)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.runId