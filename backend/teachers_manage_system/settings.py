# Celery 配置
CELERY_BROKER_URL = 'sqla+sqlite:///celerydb.sqlite'
CELERY_RESULT_BACKEND = 'db+sqlite:///celery_results.sqlite'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'

# 在 INSTALLED_APPS 中添加
INSTALLED_APPS = [
    # ... 其他应用 ...
    'django_celery_beat',
    'django_celery_results',
] 