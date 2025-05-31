from rest_framework import serializers
from django.contrib.auth import get_user_model

# 获取当前项目使用的用户模型（自定义或默认）
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """
    用于用户注册的序列化器
    处理注册时的密码加密和用户创建逻辑
    """
    # 密码字段只写（写入时有效，序列化时不返回）
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # 注册时需要的字段
        fields = ['username', 'password', 'email', 'role']

    def create(self, validated_data):
        """
        create 方法，确保密码正确加密存储
        """
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'student')  # 默认角色为学生
        )
        # 使用 Django 内置方法加密密码
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    用于用户信息序列化（例如当前登录用户信息展示）
    所有字段只读，防止前端修改
    """
    class Meta:
        model = User
        # 需要序列化返回的字段
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = fields  # 所有字段均只读
