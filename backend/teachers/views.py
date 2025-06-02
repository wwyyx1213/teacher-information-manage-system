from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .models import User, Teacher, Schedule, ResearchAchievement, Appointment
import json
from django.db.models import Count, Q

# 认证相关视图
@api_view(['POST'])
@permission_classes([AllowAny])
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

        # 如果是教师角色，创建对应的Teacher记录
        if role == 'teacher':
            Teacher.objects.create(
                user=user,
                name=username,  # 默认使用用户名作为教师姓名
                department='未设置',
                title='未设置',
                research_areas='未设置'
            )

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
            return Response({
                'message': '登录成功',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
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
def logout_view(request):
    # 清除所有会话数据
    request.session.flush()
    request.session.delete()
    
    # 执行登出
    logout(request)
    
    response = Response({'message': '已注销'}, status=200)
    
    # 清除所有相关的cookie
    cookies_to_clear = ['sessionid', 'csrftoken']
    for cookie in cookies_to_clear:
        # 删除cookie
        response.delete_cookie(
            cookie,
            path='/',
            domain=None,
            samesite='Lax'
        )
        # 设置过期时间为过去的时间
        response.set_cookie(
            cookie,
            '',
            expires='Thu, 01 Jan 1970 00:00:00 GMT',
            path='/',
            domain=None,
            samesite='Lax',
            secure=False,  # 开发环境设为False
            httponly=True if cookie == 'sessionid' else False
        )
    
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
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
        
        if user.role == 'student':
            appointments = Appointment.objects.filter(student=user)
        elif user.role == 'teacher':
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
@permission_classes([AllowAny])
def get_recommendations(request):
    user = request.user if request.user.is_authenticated else None
    recommended = []
    reason = ''
    # 游客或非学生，推荐科研成果最多的5位教师
    if not user or not hasattr(user, 'role') or user.role != 'student':
        teachers = Teacher.objects.annotate(ach_count=Count('researchachievement')).order_by('-ach_count')[:5]
        for t in teachers:
            recommended.append({
                'id': t.id,
                'name': t.name,
                'department': t.department,
                'title': t.title,
                'research_areas': t.research_areas,
                'avatar_url': t.avatar_url,
                'recommend_reason': f"该教师在{t.research_areas.split(',')[0] if t.research_areas else t.department}领域有丰富成果"
            })
        return Response({'results': recommended})
    # 学生，根据其院系/兴趣推荐
    student_major = getattr(user, 'major', None)
    student_interest = getattr(user, 'interest', None)
    # 先按院系推荐
    teachers = Teacher.objects.all()
    if student_major:
        teachers = teachers.filter(department__icontains=student_major)
        reason = f"与您的专业（{student_major}）相关"
    elif student_interest:
        teachers = teachers.filter(Q(research_areas__icontains=student_interest) | Q(department__icontains=student_interest))
        reason = f"与您的兴趣（{student_interest}）相关"
    # 若无偏好，退回科研成果最多
    if not teachers.exists():
        teachers = Teacher.objects.annotate(ach_count=Count('researchachievement')).order_by('-ach_count')[:5]
        reason = "科研成果丰富"
    else:
        teachers = teachers.annotate(ach_count=Count('researchachievement')).order_by('-ach_count')[:5]
    for t in teachers:
        recommended.append({
            'id': t.id,
            'name': t.name,
            'department': t.department,
            'title': t.title,
            'research_areas': t.research_areas,
            'avatar_url': t.avatar_url,
            'recommend_reason': reason or f"该教师在{t.research_areas.split(',')[0] if t.research_areas else t.department}领域有丰富成果"
        })
    return Response({'results': recommended})

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

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def teacher_profile(request):
    user = request.user
    if not hasattr(user, 'role') or user.role != 'teacher':
        return Response({'message': '仅教师可访问'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        return Response({'message': '教师信息不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
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
    elif request.method == 'PUT':
        data = request.data if hasattr(request, 'data') else json.loads(request.body)
        for field in ['name', 'department', 'title', 'research_areas', 'homepage_url', 'avatar_url', 'bio']:
            if field in data:
                setattr(teacher, field, data[field])
        teacher.save()
        return Response({
            'message': '个人信息已更新',
            'teacher': {
                'id': teacher.id,
                'name': teacher.name,
                'department': teacher.department,
                'title': teacher.title,
                'research_areas': teacher.research_areas,
                'homepage_url': teacher.homepage_url,
                'avatar_url': teacher.avatar_url,
                'bio': teacher.bio
            }
        }) 