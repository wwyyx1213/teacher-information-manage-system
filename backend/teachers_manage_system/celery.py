import os
from celery import Celery
from celery.schedules import crontab

# 设置默认的 Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teachers_manage_system.settings')

app = Celery('teachers_manage_system')

# 使用 Django 的设置文件配置 Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从所有已注册的 Django app 配置中加载任务
app.autodiscover_tasks()

# 配置定时任务
app.conf.beat_schedule = {
    'clean-expired-appointments': {
        'task': 'teachers.tasks.clean_expired_appointments',
        'schedule': crontab(minute=0, hour='*'),  # 每小时执行一次
    },
}

# 使用 Redis 作为 broker 和 backend
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
) 