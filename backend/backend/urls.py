from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 导入teachers app的教师视图集
from teachers.views import TeacherViewSet

router = DefaultRouter()
# 注册教师信息视图集，自动生成 /api/teachers/ 及其子路由
router.register(r'teachers', TeacherViewSet, basename='teacher')

urlpatterns = [
    path('admin/', admin.site.urls),

    # 认证相关接口统一挂载到 /api/auth/，实际路径如 /api/auth/register/
    path('api/auth/', include('users.urls')),

    # 使用router注册的所有教师相关接口（包括 /api/teachers/ 及其子路由）
    path('api/', include(router.urls)),
]
