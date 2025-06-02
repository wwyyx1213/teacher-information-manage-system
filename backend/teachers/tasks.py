from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment

@shared_task
def clean_expired_appointments():
    """
    清理过期的预约记录
    1. 删除所有状态为rejected的预约
    2. 删除所有已过期的预约（预约时间在当前时间之前）
    """
    try:
        # 删除所有rejected状态的预约
        Appointment.objects.filter(status='rejected').delete()
        
        # 获取当前时间
        now = timezone.now()
        
        # 删除所有已过期的预约
        expired_appointments = Appointment.objects.filter(
            time_slot__lt=now
        ).exclude(
            status='rejected'  # 排除已经拒绝的预约
        )
        
        # 记录删除的预约数量
        count = expired_appointments.count()
        expired_appointments.delete()
        
        return f"成功清理 {count} 条过期预约记录"
    except Exception as e:
        return f"清理过期预约记录时出错: {str(e)}" 