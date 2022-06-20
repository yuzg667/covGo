# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class covTask(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    projectName = models.CharField('项目名称',blank=True,null=True,max_length=30)
    projectId = models.IntegerField('所属项目ID',blank=True,null=True,)
    covTaskName = models.CharField('任务名称',blank=True,null=True,max_length=30)
    branch = models.CharField('被测分支',blank=True,null=True,max_length=100)
    compareBranch = models.CharField('基准分支(对比分支)',blank=True,null=True,max_length=100)
    status = models.CharField('状态：0新建，1clone完成，2clone异常',blank=True,null=True,max_length=30)
    deleted = models.IntegerField('是否删除',blank=True,default='0',null=True)
    startTime = models.DateTimeField('搜集覆盖率开始时间',blank=True,null=True)
    endTime = models.DateTimeField('搜集覆盖率结束时间',blank=True,null=True)
    lastCollectTime = models.DateTimeField('上次收集时间',blank=True,null=True)
    createTime = models.DateTimeField('创建时间',auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间',null=True)

class project(models.Model):
    # id = models.IntegerField(primary_key = True,auto_created=True)
    projectName =  models.CharField('项目名称',max_length=20)
    gitURL = models.CharField('git地址：形如gitee.com/xxx/yyy.git',max_length=255)
    gitName = models.CharField('git登录名',max_length=255)
    gitPwd = models.CharField('git密码',max_length=255)
    deleted = models.IntegerField('是否删除',default='0')
    createTime = models.DateTimeField('创建时间',auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'