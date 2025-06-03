## 提示词

请根据项目文档README.md（其中数据库和url不能变）优化项目中【学生预约页面设计http://localhost:5173/teachers/id 的预约部分】，要求要满足文档内要求，界面要美观，符合人类审美，然后同时请连通前后端间（告诉含API的请求体和响应体），且给出测试步骤，前后端均在当前目录下，backend为后端django，frontend为前端vue（使用element ui）







请根据项目文档README.md（其中数据库不能变）内要求完成教师个人中心页面设计，url为：http://localhost:5173/profile，要求在老师注册后自动跳转到个人中心界面（不同老师的个人中心界面内容不一样），其界面内要能够让老师编辑个人信息，在老师提交后将其同步到对应的数据库（数据库表在文档内给出），要求连通前后端间（告诉我含API的请求体和响应体），且给出测试步骤，前后端均在当前目录下，backend为后端django，frontend为前端vue（使用element ui），你可调试运行





导航栏仍然没有显示头像，请调整App.vue中导航栏右侧部分（使其直接显示头像），导航栏左侧部分已实现功能不变，当点击头像时，弹出预约管理、个人中心（学生无），退出等选项，其他部分实现的功能不动，要求头像内显示白色文字（文字内容为登录时username，显示在头像内），确保一次性实现



导航栏仍然没有显示头像，导航栏左侧部分已实现的功能不变，请调整App.vue中导航栏右侧部分（使其直接显示头像，不再依赖折叠菜单），要求头像内显示白色文字（文字内容为username首字母，背景色，显示在头像内），当点击头像时，弹出预约管理、个人中心（学生无），退出等选项，其他部分实现的功能不动，确保一次性实现





  项目文档为README.md（数据库表在文档内），请根据项目文档继续完成项目中学生预约功能，学生预约教师界面（http://localhost:5173/teachers/id界面的预约部分），要求预约时间以下拉菜单展示（预约时间分为：9:00-10:00;10:00-11:00;15:00-16:00;16:00-17:00;19:00-20:00;20:00-21:00），预约状态分为（pending，rejected，accepted）学生提交预约后status变为pending，同步到数据库并以列表显示展现在相应教师的预约管理界面（/appointments，已有代码文件，需完善功能），教师可进行接受和拒绝操作，然后更新数据库表appointment的status字段，如果拒绝就删除数据库中相应记录，将结果分为同意和等待两块展示在学生的我的预约界面（/my-appointments，已有代码文件，需完善功能），被拒绝的不用展示，要求连通前后端间，能够将数据同步到数据库，数据库中过期的预约记录直接自动删除，前后端均在当前目录下，backend为后端django，frontend为前端vue（使用element ui）




要求学生用户登录后在点击导航栏的我的预约后显示出学生的具体预约详情









管理员个人中心界面添加功能（更新数据库，删除账号）





## 同步

配置：

```python
配置celery文件后
pip install celery redis django-celery-beat django-celery-results
winget install Redis-x64
	pip install memurai
pip install sqlalchemy
pip install pytz
```



改数据库

```python
# 创建迁移文件
python manage.py makemigrations

# 应用迁移，创建 SQLite 数据库
python manage.py migrate
```





run：

```shell
 .\venv\Scripts\activate
cd backend
python manage.py runserver       
cd frontend
npm run dev

redis-server

# 启动 Celery beat（用于定时任务）
celery -A teachers_manage_system beat -l info
# 启动 Celery worker（用于清理过期预约）
celery -A teachers_manage_system worker -l info
```







## 注册接口：

     POST http://localhost:8000/api/register/
     请求体：
     {
       "username": "用户名",
       "password": "密码",
       "email": "邮箱",
       "role": "student/teacher"
     }
      {
       "username": "ouu",
       "password": "666666",
       "email": "2689877@qq.com",
       "role": "student"
     }


​     
​     响应体：
​         {
​           "message": "注册成功",
​           "user": {
​             "id": 用户ID,
​             "username": "用户名",
​             "email": "邮箱",
​             "role": "角色"
​           }
​         }
​         
​     {
​        "message": "注册成功",
​        "user": {
​            "id": 15,
​            "username": "ouu",
​            "role": "student"
​        }
​    }




登录接口：

     POST http://localhost:8000/api/login/
     请求体：
     {
       "username": "用户名",
       "password": "密码"
     }
     响应体：
     {
       "message": "登录成功",
       "user": {
         "id": 用户ID,
         "username": "用户名",
         "email": "邮箱",
         "role": "角色"
       }
     }
登出接口：

     POST http://localhost:8000/api/logout/
     响应体：
     {
       "message": "已成功退出登录"
     }



## 后端API实现：

- 搜索教师API：GET /api/search/teachers/

- 请求参数：

     {
       "name": "教师姓名",
       "department": "院系",
       "title": "职称",
       "research_areas": "研究方向"
     }
响应格式：

     {
       "count": 数量,
       "results": [
         {
           "id": "教师ID",
           "name": "教师姓名",
           "department": "院系",
           "title": "职称",
           "research_areas": "研究方向",
           "avatar_url": "头像URL",
           "homepage_url": "主页URL"
         }
       ]
     }





## 一、后端API

### 1. 获取教师个人信息

- 接口：GET /api/profile/

- 请求头：Authorization: Bearer <token>

- 响应体（示例）：

```json
  {
    "id": 1,
    "name": "张三",
    "department": "计算机学院",
    "title": "教授",
    "research_areas": "人工智能,大数据",
    "homepage_url": "http://xxx",
    "avatar_url": "http://xxx",
    "bio": "人工智能领域专家，我热爱运动、健身、阅读，感兴趣就加入我的课题组"
  }

```

### 更新教师个人信息

- 接口：PUT /api/profile/

- 请求头：Authorization: Bearer <token>

- 请求体（可选字段，均为字符串）：

```json
  {
    "name": "张三",
    "department": "计算机学院",
    "title": "教授",
    "research_areas": "人工智能,大数据",
    "homepage_url": "http://xxx",
    "avatar_url": "http://xxx",
    "bio": "个人简介"
  }
```

响应体：

```json
  {
    "message": "个人信息已更新",
    "teacher": { ...同上... }
  }
```

