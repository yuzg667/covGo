from django.urls import path
from cov import views as covViews  # 导入views

urlpatterns = [
    path('covHtml/', covViews.covHtml),
    path('covTaskList/', covViews.covTaskList),
    path('', covViews.covTaskList),
    path('covHtmlList/', covViews.covHtmlList),
              ]