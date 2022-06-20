from django.contrib import admin

# Register your models here.
from cov.models import project,covTask

class projectAdmin(admin.ModelAdmin):
    list_display = ('projectName','id','gitURL','gitName', 'gitPwd', 'deleted','createTime','updateTime')
    search_fields = ('projectName','id','gitURL','gitName', 'gitPwd', 'deleted',)

admin.site.register(project,projectAdmin)

class covTaskAdmin(admin.ModelAdmin):
    list_display = ('covTaskName','projectName','id','startTime','endTime', 'lastCollectTime','createTime')
    search_fields = ('covTaskName','projectName')
admin.site.register(covTask,covTaskAdmin)