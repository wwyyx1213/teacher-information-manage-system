from django.urls import path
from . import views

urlpatterns = [
    # 认证相关
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.get_user_info, name='user_info'),
    
    # 教师相关
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/<int:teacher_id>/schedule/', views.teacher_schedule, name='teacher_schedule'),
    path('teachers/<int:teacher_id>/research/', views.teacher_research, name='teacher_research'),
    
    # 预约相关
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    
    # 推荐系统
    path('recommendations/', views.get_recommendations, name='recommendations'),
    
    # 搜索
    path('search/teachers/', views.search_teachers, name='search_teachers'),
] 