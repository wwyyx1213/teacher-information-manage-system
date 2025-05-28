from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Teacher, Schedule, ResearchProject, Publication, Appointment
from .serializers import (
    TeacherSerializer, ScheduleSerializer, ResearchProjectSerializer,
    PublicationSerializer, AppointmentSerializer
)

class TeacherViewSet(viewsets.ModelViewSet):
    ''' 教师 '''
    queryset = Teacher.objects.all() # 查询集
    serializer_class = TeacherSerializer # 序列化器
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] # 过滤器
    filterset_fields = ['department', 'title'] # 过滤字段
    search_fields = ['user__username', 'research_direction', 'introduction'] # 搜索字段

class ScheduleViewSet(viewsets.ModelViewSet):
    ''' 日程 '''
    queryset = Schedule.objects.all() # 查询集
    serializer_class = ScheduleSerializer # 序列化器
    permission_classes = [IsAuthenticated] # 权限

class ResearchProjectViewSet(viewsets.ModelViewSet):
    ''' 研究项目 '''
    queryset = ResearchProject.objects.all() # 查询集
    serializer_class = ResearchProjectSerializer # 序列化器
    permission_classes = [IsAuthenticated] # 权限

class PublicationViewSet(viewsets.ModelViewSet):
    ''' 发表论文 '''
    queryset = Publication.objects.all() # 查询集
    serializer_class = PublicationSerializer # 序列化器
    permission_classes = [IsAuthenticated] # 权限

class AppointmentViewSet(viewsets.ModelViewSet):
    ''' 预约 '''
    queryset = Appointment.objects.all() # 查询集   
    serializer_class = AppointmentSerializer # 序列化器
    permission_classes = [IsAuthenticated] # 权限