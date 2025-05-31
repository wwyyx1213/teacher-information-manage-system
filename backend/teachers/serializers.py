from rest_framework import serializers
from .models import Teacher, Schedule

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'name', 'department', 'title', 'research_areas', 'homepage_url', 'avatar_url', 'bio']
        read_only_fields = ['user']  # user字段只读，自动设置

# 教师日程序列化器
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'teacher', 'date', 'time', 'content']