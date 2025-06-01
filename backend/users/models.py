from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 用户角色，限定为 student、teacher、admin
    ROLE_CHOICES = (
        ('student', '学生'),
        ('teacher', '教师'),
        ('admin', '管理员'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
