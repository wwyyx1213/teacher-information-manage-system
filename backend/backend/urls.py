"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teachers.views import (
    TeacherViewSet, ScheduleViewSet, ResearchProjectViewSet,
    PublicationViewSet, AppointmentViewSet
) 

router = DefaultRouter() # 路由器
router.register(r'teachers', TeacherViewSet) # 注册教师
router.register(r'schedules', ScheduleViewSet) # 注册日程
router.register(r'projects', ResearchProjectViewSet) # 注册研究项目
router.register(r'publications', PublicationViewSet) # 注册发表论文
router.register(r'appointments', AppointmentViewSet) # 注册预约

# 路由  
urlpatterns = [
    path('admin/', admin.site.urls), # 管理员
    path('api/', include(router.urls)), # 路由
    path('api-auth/', include('rest_framework.urls')), # 认证
]
