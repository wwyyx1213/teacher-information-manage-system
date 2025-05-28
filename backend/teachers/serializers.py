from rest_framework import serializers
from .models import Teacher, Schedule, ResearchProject, Publication, Appointment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    ''' 用户 '''
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class TeacherSerializer(serializers.ModelSerializer):
    ''' 教师 '''
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Teacher
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    ''' 日程 '''
    class Meta:
        model = Schedule
        fields = '__all__'

class ResearchProjectSerializer(serializers.ModelSerializer):
    ''' 研究项目 '''
    class Meta:
        model = ResearchProject
        fields = '__all__'

class PublicationSerializer(serializers.ModelSerializer):
    ''' 发表论文 '''
    class Meta:
        model = Publication
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    ''' 预约 '''
    class Meta:
        model = Appointment
        fields = '__all__'