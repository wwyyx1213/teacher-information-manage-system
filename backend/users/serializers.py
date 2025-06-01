from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 获取当前项目使用的用户模型
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """
    用于用户注册的序列化器
    处理注册时的密码加密和用户创建逻辑
    """

    class Meta:
        model = User
        # 注册时需要的字段
        fields = ['username', 'password', 'email', 'role','name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
        username=validated_data['username'],
        email=validated_data.get('email', ''),
        role=validated_data.get('role', 'student'),
        name=validated_data.get('name', '')
    )
        user.set_password(validated_data['password'])  # 密码加密
        user.save()  # 保存到数据库
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    用于用户信息序列化（例如当前登录用户信息展示）
    所有字段只读，防止前端修改
    """
    class Meta:
        model = User
        # 需要序列化返回的字段
        fields = ['id', 'username', 'email', 'role','name']
        read_only_fields = fields  # 所有字段均只读

# 自定义登录序列化器，返回 token 和 user 信息
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user_data = UserSerializer(self.user).data
        data['user'] = user_data

        return data