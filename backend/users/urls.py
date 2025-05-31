from django.urls import path
from .views import RegisterView, LoginView, LogoutView, CurrentUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),    # 注册接口
    path('login/', LoginView.as_view(), name='login'),             # 登录接口
    path('logout/', LogoutView.as_view(), name='logout'),          # 注销接口
    path('user/', CurrentUserView.as_view(), name='current_user'), # 获取当前登录用户信息接口
]
