from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class Teacher(models.Model):
    # 与User模型一对一绑定，便于教师扩展信息
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    research_areas = models.TextField()
    homepage_url = models.URLField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)  # 简介，包括科研成果

    def __str__(self):
        return self.name

# 教师日程模型
class Schedule(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='schedules', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='日期')
    time = models.TimeField(verbose_name='时间')
    content = models.TextField(verbose_name='日程内容')

    def __str__(self):
        return f"{self.teacher.name} - {self.date} {self.time}"