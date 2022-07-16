from django.contrib import admin

# Register your models here.
from django.db.models import QuerySet

from cov.models import project, covTask


class projectAdmin(admin.ModelAdmin):
    list_display = ('projectName', 'id', 'gitURL', 'gitName', 'gitPwd', 'deleted', 'createTime', 'updateTime')
    search_fields = ('projectName', 'id', 'gitURL', 'gitName', 'gitPwd', 'deleted',)
    exclude = ('deleted',)  # 编辑页面不显示这些字段

    # 设置只能新建不能修改的字段
    def get_readonly_fields(self, request, obj=None):
        if obj:
            readonly_fields = ('projectName', 'deleted')
        else:
            readonly_fields = ()
        return readonly_fields

    # 批量逻辑删除
    actions = ['delete_selected']
    def delete_selected(modeladmin, request, queryset):
        # Show confirmation page.
        for obj in queryset:
            obj.delete()


admin.site.register(project, projectAdmin)


class covTaskAdmin(admin.ModelAdmin):
    list_display = ('covTaskName', 'id', 'projectName', 'startTime', 'endTime', 'lastCollectTime', 'status', 'deleted', 'createTime')
    search_fields = ('covTaskName', 'projectName')
    exclude = ('projectName', 'deleted', 'status', 'lastCollectTime')  # 编辑页面不显示这些字段

    # 设置只能新建不能修改的字段
    def get_readonly_fields(self, request, obj=None):
        if obj:
            readonly_fields = ('covTaskName', 'projectName', 'projectId', 'lastCollectTime', 'deleted', 'status')
        else:
            readonly_fields = ()
        return readonly_fields
    # 批量逻辑删除
    actions = ['delete_selected']
    def delete_selected(modeladmin, request, queryset):
        # Show confirmation page.
        for obj in queryset:
            obj.delete()


admin.site.register(covTask, covTaskAdmin)

# 自定义管理后台名称
admin.site.site_title = "go服务覆盖率平台"
admin.site.site_header = "covGo覆盖率平台"
admin.site.index_title = "covGo"


# def delete_selected(modeladmin, request, QuerySet):
#     pass
#
#
#     for i in QuerySet:
#         i.delete()
# delete_selected.short_description = '删除已选项'
#
#
# class projectAdmin(admin.ModelAdmin):
#     actions = [delete_selected]
