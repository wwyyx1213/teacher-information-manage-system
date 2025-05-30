from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    research_areas = models.TextField()
    homepage_url = models.URLField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    external_source = models.CharField(max_length=50, blank=True, null=True)
    external_id = models.CharField(max_length=100, blank=True, null=True)
    synced_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.teacher.name}的日程: {self.start_time} - {self.end_time}"

class ResearchAchievement(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    file_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.teacher.name}的成果: {self.title}"

class Appointment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    time_slot = models.DateTimeField()
    status = models.CharField(max_length=20, default='pending')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username}预约{self.teacher.name}: {self.time_slot}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}的通知: {self.type}" 