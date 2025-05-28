from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Teacher(models.Model):
    ''' 教师 '''
    user = models.OneToOneField(User, on_delete=models.CASCADE) # 关联用户
    title = models.CharField(max_length=50, verbose_name='职称') # 职称
    department = models.CharField(max_length=100, verbose_name='所属院系') # 所属院系
    research_direction = models.TextField(verbose_name='研究方向') # 研究方向
    introduction = models.TextField(verbose_name='个人简介') # 个人简介
    created_at = models.DateTimeField(auto_now_add=True) # 创建时间
    updated_at = models.DateTimeField(auto_now=True) # 更新时间 

    class Meta: 
        # 数据库表名
        verbose_name = '教师' # 别名
        verbose_name_plural = '教师' # 复数别名

    def __str__(self):
        # 返回字符串
        return f"{self.user.username} - {self.title}"

class Schedule(models.Model):
    ''' 日程 '''
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schedules') # 关联教师
    date = models.DateField(verbose_name='日期') # 日期
    start_time = models.TimeField(verbose_name='开始时间') # 开始时间
    end_time = models.TimeField(verbose_name='结束时间') # 结束时间
    is_available = models.BooleanField(default=True, verbose_name='是否可预约') # 是否可预约

    class Meta:
        # 数据库表名
        verbose_name = '日程' # 别名
        verbose_name_plural = '日程' # 复数别名

class ResearchProject(models.Model):
    ''' 研究项目 '''
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='projects') # 关联教师
    title = models.CharField(max_length=200, verbose_name='项目名称') # 项目名称
    funding_source = models.CharField(max_length=100, verbose_name='资金来源') # 资金来源
    start_date = models.DateField(verbose_name='开始日期') # 开始日期
    end_date = models.DateField(verbose_name='结束日期') # 结束日期
    description = models.TextField(verbose_name='项目描述') # 项目描述

    class Meta:
        # 数据库表名
        verbose_name = '研究项目' # 别名
        verbose_name_plural = '研究项目' # 复数别名

class Publication(models.Model):
    ''' 发表论文 '''
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='publications') # 关联教师
    title = models.CharField(max_length=200, verbose_name='论文标题') # 论文标题
    journal = models.CharField(max_length=200, verbose_name='期刊名称') # 期刊名称
    publication_date = models.DateField(verbose_name='发表日期') # 发表日期
    citation_count = models.IntegerField(default=0, verbose_name='引用次数') # 引用次数

    class Meta:
        # 数据库表名
        verbose_name = '发表论文' # 别名
        verbose_name_plural = '发表论文' # 复数别名

class Appointment(models.Model):
    ''' 预约 '''
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('accepted', '已接受'),
        ('rejected', '已拒绝'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_appointments') # 关联学生
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_appointments') # 关联教师
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE) # 关联日程
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') # 状态
    created_at = models.DateTimeField(auto_now_add=True) # 创建时间
    updated_at = models.DateTimeField(auto_now=True) # 更新时间

    class Meta:
        # 数据库表名
        verbose_name = '预约' # 别名
        verbose_name_plural = '预约' # 复数别名
