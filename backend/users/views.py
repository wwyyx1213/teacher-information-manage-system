from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    用户注册接口，允许学生和教师注册
    允许任何用户访问
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(TokenObtainPairView):
    """
    JWT登录接口，继承SimpleJWT自带实现，无需重写
    """

class LogoutView(APIView):
    """
    用户注销接口，传入refresh token进行注销（加入黑名单）
    需要用户登录权限
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "注销成功"})
        except Exception:
            return Response({"detail": "注销失败"}, status=400)

class CurrentUserView(APIView):
    """
    获取当前登录用户信息
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
