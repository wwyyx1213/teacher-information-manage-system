import os
from celery import Celery

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
        'schedule': 3600.0,  # 每小时执行一次
    },
}

# 使用 SQLite 作为后端
app.conf.update(
    broker_url='sqla+sqlite:///celerydb.sqlite',
    result_backend='db+sqlite:///celery_results.sqlite',
) 