from django.db import models
from django.contrib.auth.models import AbstractUser


# 自定义用户模型
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    # 重写 groups 和 user_permissions 字段，使用不同的 related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

# 教师信息表
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    research_areas = models.TextField()
    homepage_url = models.URLField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

# 教师日程表
class Schedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    external_source = models.CharField(max_length=50, blank=True, null=True)
    external_id = models.CharField(max_length=100, blank=True, null=True)
    synced_at = models.DateTimeField(blank=True, null=True)

# 科研成果
class ResearchAchievement(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=50)  # 论文、项目、基金等
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    file_url = models.URLField(blank=True, null=True)

# 预约记录
class Appointment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    time_slot = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
    remarks = models.TextField(blank=True, null=True)

# 通知
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)  # system, appointment, etc.
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 