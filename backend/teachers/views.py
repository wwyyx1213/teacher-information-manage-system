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
from datetime import datetime, timedelta
from django.utils import timezone
import pytz

# 设置时区为中国时区
china_tz = pytz.timezone('Asia/Shanghai')

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
            response_data = {
                'message': '登录成功',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
            }
            
            # 如果是教师，添加教师相关信息
            if user.role == 'teacher':
                try:
                    teacher = Teacher.objects.get(user=user)
                    response_data['user'].update({
                        'name': teacher.name,
                        'department': teacher.department,
                        'title': teacher.title,
                        'research_areas': teacher.research_areas,
                        'avatar_url': teacher.avatar_url
                    })
                except Teacher.DoesNotExist:
                    # 如果教师信息不存在，创建一个新的教师信息
                    teacher = Teacher.objects.create(
                        user=user,
                        name=username,  # 默认使用用户名作为教师姓名
                        department='未设置',
                        title='未设置',
                        research_areas='未设置'
                    )
                    response_data['user'].update({
                        'name': teacher.name,
                        'department': teacher.department,
                        'title': teacher.title,
                        'research_areas': teacher.research_areas,
                        'avatar_url': teacher.avatar_url
                    })
            
            print("Login response data:", response_data)  # 添加调试日志
            return Response(response_data)
        else:
            return Response({
                'message': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print("Login error:", str(e))  # 添加调试日志
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
    domains = [None, 'localhost']  # 尝试不同的domain
    
    for cookie in cookies_to_clear:
        for domain in domains:
            # 删除cookie
            response.delete_cookie(
                cookie,
                path='/',
                domain=domain,
                samesite='Lax'
            )
            # 设置过期时间为过去的时间
            response.set_cookie(
                cookie,
                '',
                expires='Thu, 01 Jan 1970 00:00:00 GMT',
                path='/',
                domain=domain,
                samesite='Lax',
                secure=False,
                httponly=True if cookie == 'sessionid' else False
            )
    
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def clear_session(request):
    """专门用于清除session的端点"""
    request.session.flush()
    request.session.delete()
    
    response = Response({'message': 'Session已清除'}, status=200)
    
    # 清除sessionid cookie
    response.delete_cookie(
        'sessionid',
        path='/',
        domain=None,
        samesite='Lax'
    )
    response.set_cookie(
        'sessionid',
        '',
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        path='/',
        domain=None,
        samesite='Lax',
        secure=False,
        httponly=True
    )
    
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    response_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }
    
    # 如果是教师，添加教师相关信息
    if user.role == 'teacher':
        try:
            teacher = Teacher.objects.get(user=user)
            response_data.update({
                'name': teacher.name,
                'department': teacher.department,
                'title': teacher.title,
                'research_areas': teacher.research_areas,
                'avatar_url': teacher.avatar_url
            })
        except Teacher.DoesNotExist:
            pass
    
    return Response(response_data)

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
        try:
            user = request.user
            print(f"获取预约列表，用户角色: {user.role}, 用户ID: {user.id}")
            
            if user.role == 'student':
                appointments = Appointment.objects.filter(student=user)
            elif user.role == 'teacher':
                try:
                    teacher = Teacher.objects.get(user=user)
                    print(f"找到教师信息: {teacher.id}, {teacher.name}")
                    appointments = Appointment.objects.filter(teacher=teacher)
                except Teacher.DoesNotExist:
                    print(f"未找到教师信息，用户ID: {user.id}")
                    return Response({
                        'message': '未找到教师信息'
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    'message': '权限不足'
                }, status=status.HTTP_403_FORBIDDEN)
                
            data = []
            for a in appointments:
                try:
                    # 确保时间在中国时区
                    time_slot = a.time_slot.astimezone(china_tz)
                    # 计算时间段
                    time_range = f"{time_slot.strftime('%H:%M')}-{(time_slot + timedelta(hours=1)).strftime('%H:%M')}"
                    
                    appointment_data = {
                        'id': a.id,
                        'student': {
                            'id': a.student.id,
                            'username': a.student.username
                        },
                        'teacher': {
                            'id': a.teacher.id,
                            'name': a.teacher.name
                        },
                        'time_slot': time_slot,
                        'time_range': time_range,
                        'status': a.status,
                        'remarks': a.remarks
                    }
                    data.append(appointment_data)
                except Exception as e:
                    print(f"处理预约数据错误: {str(e)}, 预约ID: {a.id}")
                    continue
            
            print(f"返回预约列表数据: {data}")
            return Response({
                'count': len(data),
                'results': data
            })
            
        except Exception as e:
            import traceback
            print(f"获取预约列表错误: {str(e)}")
            print(f"错误堆栈: {traceback.format_exc()}")
            return Response({
                'message': f'获取预约列表失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    elif request.method == 'POST':
        try:
            data = request.data
            teacher_id = data.get('teacher_id')
            time_slot = data.get('time_slot')
            remarks = data.get('remarks', '')
            
            if not all([teacher_id, time_slot]):
                return Response({
                    'message': '请提供所有必需的字段'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证时间段是否合法
            try:
                # 尝试解析 ISO 格式的时间
                time = datetime.fromisoformat(time_slot.replace('Z', '+00:00'))
                
                # 转换为中国时区
                local_time = time.astimezone(china_tz)
                hour = local_time.hour
                
                # 验证小时是否在允许的时间段内
                if hour not in [9, 10, 15, 16, 19, 20]:
                    return Response({
                        'message': f'无效的预约时间段：{hour}:00，请选择 9:00、10:00、15:00、16:00、19:00 或 20:00'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 验证分钟是否为 0
                if local_time.minute != 0:
                    return Response({
                        'message': '预约时间必须是整点'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            except ValueError as e:
                return Response({
                    'message': f'无效的时间格式：{str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 检查是否已经存在相同时间的预约
            existing_appointment = Appointment.objects.filter(
                teacher_id=teacher_id,
                time_slot=time,
                status__in=['pending', 'accepted']
            ).exists()
            
            if existing_appointment:
                return Response({
                    'message': '该时间段已被预约'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 检查是否已经预约过该教师
            student_existing = Appointment.objects.filter(
                student=request.user,
                teacher_id=teacher_id,
                status__in=['pending', 'accepted']
            ).exists()
            
            if student_existing:
                return Response({
                    'message': '您已经预约过该教师'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            teacher = Teacher.objects.get(id=teacher_id)
            appointment = Appointment.objects.create(
                student=request.user,
                teacher=teacher,
                time_slot=time,
                remarks=remarks,
                status='pending'
            )
            
            # 计算时间段
            time_slot_local = appointment.time_slot.astimezone(china_tz)
            end_time = time_slot_local + timedelta(hours=1)
            time_range = f"{time_slot_local.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"
            
            return Response({
                'message': '预约成功',
                'appointment': {
                    'id': appointment.id,
                    'teacher': teacher.name,
                    'time_slot': appointment.time_slot.astimezone(china_tz),
                    'time_range': time_range,
                    'status': appointment.status
                }
            }, status=status.HTTP_201_CREATED)
            
        except Teacher.DoesNotExist:
            return Response({
                'message': '教师不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"创建预约错误: {str(e)}")  # 添加调试日志
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def appointment_detail(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # 检查权限
        if request.user.role == 'student' and appointment.student != request.user:
            return Response({
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)
        elif request.user.role == 'teacher':
            teacher = Teacher.objects.get(user=request.user)
            if appointment.teacher != teacher:
                return Response({
                    'message': '权限不足'
                }, status=status.HTTP_403_FORBIDDEN)
        
        if request.method == 'GET':
            time_slot = appointment.time_slot.astimezone(china_tz)
            time_range = f"{time_slot.strftime('%H:%M')}-{(time_slot + timedelta(hours=1)).strftime('%H:%M')}"
            data = {
                'id': appointment.id,
                'student': appointment.student.username,
                'teacher': appointment.teacher.name,
                'time_slot': time_slot,
                'time_range': time_range,
                'status': appointment.status,
                'remarks': appointment.remarks
            }
            return Response(data)
        
        elif request.method in ['PUT', 'PATCH']:
            data = json.loads(request.body) if request.method == 'PUT' else request.data
            new_status = data.get('status')
            
            if new_status not in ['accepted', 'rejected']:
                return Response({
                    'message': '无效的状态值'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if request.user.role != 'teacher':
                return Response({
                    'message': '只有教师可以更改预约状态'
                }, status=status.HTTP_403_FORBIDDEN)
            
            if new_status == 'rejected':
                appointment.delete()
                return Response({
                    'message': '预约已拒绝并删除'
                })
            else:
                appointment.status = new_status
                appointment.save()
                return Response({
                    'message': '预约状态已更新',
                    'status': appointment.status
                })
        
        elif request.method == 'DELETE':
            # 只有学生本人可以删除
            if request.user.role == 'student' and appointment.student == request.user:
                appointment.delete()
                return Response({'message': '预约已取消'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': '只有预约学生本人可以取消预约'}, status=status.HTTP_403_FORBIDDEN)
    except Appointment.DoesNotExist:
        return Response({
            'message': '预约不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"处理预约详情错误: {str(e)}")  # 添加调试日志
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