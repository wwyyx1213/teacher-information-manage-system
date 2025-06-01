from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .models import User, Teacher, Schedule, ResearchAchievement, Appointment
import json

# 认证相关视图
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not all([username, password, role]):
            return Response({
                'message': '请提供所有必需的字段'
            }, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({
                'message': '用户名已存在'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            password=password,
            role=role
        )

        # 根据角色设置用户组
        group = Group.objects.get(name=role)
        user.groups.add(group)

        return Response({
            'message': '注册成功',
            'user': {
                'id': user.id,
                'username': user.username,
                'role': role
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            group = user.groups.first()
            return Response({
                'message': '登录成功',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': group.name if group else None
                }
            })
        else:
            return Response({
                'message': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def logout_view(request):
    logout(request)
    response = Response({'message': '已注销'}, status=200)
    # 彻底删除sessionid和csrftoken等cookie
    response.delete_cookie('sessionid', path='/', domain=None)
    response.delete_cookie('csrftoken', path='/', domain=None)
    # 兼容部分浏览器的SameSite属性
    response.set_cookie('sessionid', '', expires=0, path='/', samesite='Lax')
    response.set_cookie('csrftoken', '', expires=0, path='/', samesite='Lax')
    request.session.flush()
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    group = user.groups.first()
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': group.name if group else None
    })

# 教师相关视图
@api_view(['GET'])
@permission_classes([AllowAny])
def teacher_list(request):
    # 获取筛选参数
    name = request.GET.get('name', '')
    department = request.GET.get('department', '')
    title = request.GET.get('title', '')
    research_areas = request.GET.get('research_areas', '')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 100))

    # 构建查询
    query = Teacher.objects.all()
    if name:
        query = query.filter(name__icontains=name)
    if department:
        query = query.filter(department__icontains=department)
    if title:
        query = query.filter(title__icontains=title)
    if research_areas:
        query = query.filter(research_areas__icontains=research_areas)

    total = query.count()
    start = (page - 1) * page_size
    end = start + page_size
    teachers = query[start:end]
    data = [{
        'id': t.id,
        'name': t.name,
        'department': t.department,
        'title': t.title,
        'research_areas': t.research_areas,
        'avatar_url': t.avatar_url
    } for t in teachers]
    return Response({'count': total, 'results': data})

@api_view(['GET'])
@permission_classes([AllowAny])
def teacher_detail(request, teacher_id):
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        data = {
            'id': teacher.id,
            'name': teacher.name,
            'department': teacher.department,
            'title': teacher.title,
            'research_areas': teacher.research_areas,
            'homepage_url': teacher.homepage_url,
            'avatar_url': teacher.avatar_url,
            'bio': teacher.bio
        }
        return Response(data)
    except Teacher.DoesNotExist:
        return Response({
            'message': '教师不存在'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def teacher_schedule(request, teacher_id):
    try:
        schedules = Schedule.objects.filter(teacher_id=teacher_id)
        data = [{
            'id': s.id,
            'start_time': s.start_time,
            'end_time': s.end_time,
            'is_available': s.is_available
        } for s in schedules]
        return Response(data)
    except Exception as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def teacher_research(request, teacher_id):
    try:
        achievements = ResearchAchievement.objects.filter(teacher_id=teacher_id)
        data = [{
            'id': a.id,
            'title': a.title,
            'type': a.type,
            'date': a.date,
            'description': a.description,
            'file_url': a.file_url
        } for a in achievements]
        return Response(data)
    except Exception as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 预约相关视图
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list(request):
    if request.method == 'GET':
        user = request.user
        group = user.groups.first()
        
        if group.name == 'student':
            appointments = Appointment.objects.filter(student=user)
        elif group.name == 'teacher':
            teacher = Teacher.objects.get(user=user)
            appointments = Appointment.objects.filter(teacher=teacher)
        else:
            return Response({
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)
            
        data = [{
            'id': a.id,
            'student': a.student.username,
            'teacher': a.teacher.name,
            'time_slot': a.time_slot,
            'status': a.status,
            'remarks': a.remarks
        } for a in appointments]
        return Response(data)
        
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            teacher_id = data.get('teacher_id')
            time_slot = data.get('time_slot')
            remarks = data.get('remarks', '')
            
            teacher = Teacher.objects.get(id=teacher_id)
            appointment = Appointment.objects.create(
                student=request.user,
                teacher=teacher,
                time_slot=time_slot,
                remarks=remarks
            )
            
            return Response({
                'message': '预约成功',
                'appointment': {
                    'id': appointment.id,
                    'teacher': teacher.name,
                    'time_slot': appointment.time_slot,
                    'status': appointment.status
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def appointment_detail(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        if request.method == 'GET':
            data = {
                'id': appointment.id,
                'student': appointment.student.username,
                'teacher': appointment.teacher.name,
                'time_slot': appointment.time_slot,
                'status': appointment.status,
                'remarks': appointment.remarks
            }
            return Response(data)
            
        elif request.method == 'PUT':
            data = json.loads(request.body)
            new_status = data.get('status')
            
            if new_status in ['accepted', 'rejected']:
                appointment.status = new_status
                appointment.save()
                return Response({
                    'message': '预约状态已更新',
                    'status': appointment.status
                })
            else:
                return Response({
                    'message': '无效的状态值'
                }, status=status.HTTP_400_BAD_REQUEST)
                
    except Appointment.DoesNotExist:
        return Response({
            'message': '预约不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 推荐系统视图
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    # 这里实现推荐算法
    # 示例：返回所有教师
    teachers = Teacher.objects.all()[:5]  # 限制返回5个推荐
    data = [{
        'id': t.id,
        'name': t.name,
        'department': t.department,
        'title': t.title,
        'research_areas': t.research_areas,
        'avatar_url': t.avatar_url
    } for t in teachers]
    return Response(data)

# 搜索视图
@api_view(['GET'])
@permission_classes([AllowAny])
def search_teachers(request):
    try:
        # 获取搜索参数
        name = request.GET.get('name', '')
        department = request.GET.get('department', '')
        title = request.GET.get('title', '')
        research_areas = request.GET.get('research_areas', '')

        # 构建查询
        query = Teacher.objects.all()
        
        if name:
            query = query.filter(name__icontains=name)
        if department:
            query = query.filter(department__icontains=department)
        if title:
            query = query.filter(title__icontains=title)
        if research_areas:
            query = query.filter(research_areas__icontains=research_areas)

        # 获取结果
        teachers = query.all()
        data = [{
            'id': t.id,
            'name': t.name,
            'department': t.department,
            'title': t.title,
            'research_areas': t.research_areas,
            'avatar_url': t.avatar_url,
            'homepage_url': t.homepage_url
        } for t in teachers]

        return Response({
            'count': len(data),
            'results': data
        })

    except Exception as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 