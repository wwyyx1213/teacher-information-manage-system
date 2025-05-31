from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = '初始化用户组'

    def handle(self, *args, **options):
        # 创建学生组
        student_group, created = Group.objects.get_or_create(name='student')
        if created:
            self.stdout.write(self.style.SUCCESS('成功创建学生组'))
        else:
            self.stdout.write(self.style.SUCCESS('学生组已存在'))

        # 创建教师组
        teacher_group, created = Group.objects.get_or_create(name='teacher')
        if created:
            self.stdout.write(self.style.SUCCESS('成功创建教师组'))
        else:
            self.stdout.write(self.style.SUCCESS('教师组已存在')) 