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
    
    # 教师个人中心的日程管理
    path('teacher/schedules/', views.teacher_schedule_management, name='teacher_schedule_management'),
    path('teacher/schedules/<int:schedule_id>/', views.teacher_schedule_detail, name='teacher_schedule_detail'),
    
    # 教师个人中心的成果管理
    path('teacher/achievements/', views.teacher_achievement_management, name='teacher_achievement_management'),
    path('teacher/achievements/<int:achievement_id>/', views.teacher_achievement_detail, name='teacher_achievement_detail'),
    
    # 推荐系统
    path('recommendations/', views.get_recommendations, name='recommendations'),
    
    # 搜索
    path('search/teachers/', views.search_teachers, name='search_teachers'),
    
    # 教师个人中心
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('clear-session/', views.clear_session, name='clear-session'),
    path('admin/users/', views.admin_user_management, name='admin_user_management'),
    path('admin/users/<int:user_id>/', views.admin_user_management, name='admin_user_management_detail'),
    path('admin/update-database/', views.update_database, name='update_database'),
    path('change-password/', views.change_password, name='change_password'),
] 