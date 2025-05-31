from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .models import Teacher, Schedule
from .serializers import TeacherSerializer, ScheduleSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'department', 'title', 'research_areas']

    def perform_create(self, serializer):
        # 创建时自动绑定当前登录用户
        serializer.save(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        # 只有教师本人或者管理员能访问/修改信息
        if obj.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("无权限访问该教师信息")
        return obj

    def update(self, request, *args, **kwargs):
        # 只允许教师本人修改
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_staff:
            raise PermissionDenied("无权限修改该教师信息")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # 只允许教师本人部分修改
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_staff:
            raise PermissionDenied("无权限修改该教师信息")
        return super().partial_update(request, *args, **kwargs)
    
    # 教师日程子路由
    @action(detail=True, methods=['get', 'post'], url_path='schedule')
    def schedule(self, request, pk=None):
        """
        GET: 查看指定教师的日程
        POST: 设置日程（仅教师本人）
        """
        teacher = self.get_object()

        if request.method == 'GET':
            schedules = Schedule.objects.filter(teacher=teacher)
            serializer = ScheduleSerializer(schedules, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = ScheduleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(teacher=teacher)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
