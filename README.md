## 项目要求 初始化

项目要求使用**虚拟环境**，若不会可参考**附录 1**

激活当前虚拟环境：

```
 ...>Scripts> activate.bat
```



编程要求：函数有中文**注释**



项目要求**使用 git**，放在 GitHub 上，且**每次**开始写代码时记得**从仓库拉取最新代码**

GitHub 地址：

```shell
 # https://github.com/wwyyx1213/teacher-information-manage-system.git
 # 将远程仓库的 URL 添加到本地仓库的配置中，使其与本地仓库关联
 git remote add origin https://github.com/wwyyx1213/teacher-information-manage-system.git
```



代码开始编写时需要**pull**，

```shell
git pull
# 使用 --no-commit 选项可以拉取更改但不自动合并，允许用户检查更改后再手动合并：
```

然后安装依赖库：

```shell
pip install -r requirements.txt
```





当项目开发完后，建议使用 **pip freeze>requirements.txt** 命令将项目的库依赖导出

结束代码编写后需要检测是否有明显 bug，若无则**push**到 GitHub。

```shell
git add .	
# 或者  git add 文件名

git commit -m "提交提示信息"

# 将本地 main 分支的代码推送到远程仓库
git push -u origin main
```





数据库要求使用**MySQL**，需要：

```
import pymysql
pymysql.install_as_MySQLdb()
```

ip地址：

```
192.168.139.1
公网：10.68.69.19
```

```django
用户名：admin
登录密码：456666
'PORT': '3306'
'ENGINE': 'django.db.backends.mysql',             # 指定了要使用的数据库后端
```

**注意**：IP 不是 localhost



django + vue(引用Element ui) + mysql 前后端分离





## 项目结束

白盒测试、黑盒测试

当项目开发完后，建议使用 命令将项目的库依赖导出

> pip freeze > requirements.txt 


下面是基于之前用户故事，对整个“教师信息管理系统”所需的前端路由（Vue SPA）和后端 REST API 路由（Django DRF）的设计。路由均遵循 RESTful 规范，便于开发和扩展，同时兼顾用户体验。

---

## 一、前端路由（Vue + Vue-Router）

| 路由路径                     | 组件                | 说明                  |
| ------------------------ | ----------------- | ------------------- |
| `/`                      | HomeView          | 系统首页，展示推荐教师、最新通知等   |
| `/login`                 | LoginView         | 登录页面                |
| `/register`              | RegisterView      | 注册页面（学生/教师）         |
| `/teachers`              | TeacherListView   | 导师列表页面，可多维度检索       |
| `/teachers/:id`          | TeacherDetailView | 导师详情页，包含基本信息、日程、成果等 |
| `/teachers/:id/schedule` | ScheduleView      | 仅查看/同步该导师的日程        |
| `/teachers/:id/research` | ResearchView      | 仅查看该导师的基金与科研成果      |
| `/search`                | SearchView        | 全局搜索页（关键字/学院/研究方向）  |
| `/recommendations`       | RecommendView     | 根据用户偏好/历史行为的导师推荐    |
| `/appointments`          | MyAppointments    | 学生：我的预约列表           |
| `/appointments/new/:tid` | AppointmentForm   | 学生：对导师 `:tid` 发起新预约 |
| `/appointments/:id`      | AppointmentDetail | 预约详情（学生或教师查看、教师审批）  |
| `/profile`               | ProfileView       | 当前用户（学生/教师）个人中心     |
| `/admin`                 | AdminDashboard    | 管理员后台首页             |
| `/admin/users`           | UserManageView    | 管理学生/教师账号           |
| `/admin/sync`            | DataSyncView      | 配置外部数据源定时同步         |
| `/admin/stats`           | StatsView         | 系统统计与推荐算法参数配置       |

---

## 二、后端 REST API 路由（Django REST Framework）

### 1. 教师信息模块 `/api/teachers/`

| 方法        | 路径                    | 说明                    |
| --------- | --------------------- | --------------------- |
| GET       | `/api/teachers/`      | 获取导师列表，可通过 query 参数筛选 |
| POST      | `/api/teachers/`      | 管理员/教师 创建新导师档案        |
| GET       | `/api/teachers/{id}/` | 获取单个导师基本信息            |
| PUT/PATCH | `/api/teachers/{id}/` | 更新导师基本信息              |
| DELETE    | `/api/teachers/{id}/` | 删除导师档案（管理员权限）         |

**支持的查询参数**

* `?name=`
* `?department=`
* `?research=`
* `?title=`

---

### 2. 日程模块 `/api/teachers/{id}/schedule/`

| 方法        | 路径                                           | 说明         |
| --------- | -------------------------------------------- | ---------- |
| GET       | `/api/teachers/{id}/schedule/`               | 获取导师所有日程   |
| POST      | `/api/teachers/{id}/schedule/`               | 教师新建可预约时间段 |
| PUT/PATCH | `/api/teachers/{id}/schedule/{schedule_id}/` | 更新某条日程     |
| DELETE    | `/api/teachers/{id}/schedule/{schedule_id}/` | 删除某条日程     |

---

### 3. 科研成果模块 `/api/teachers/{id}/research/`

| 方法        | 路径                                           | 说明            |
| --------- | -------------------------------------------- | ------------- |
| GET       | `/api/teachers/{id}/research/`               | 获取导师基金和科研成果列表 |
| POST      | `/api/teachers/{id}/research/`               | 教师添加新成果/项目    |
| PUT/PATCH | `/api/teachers/{id}/research/{research_id}/` | 更新某条成果        |
| DELETE    | `/api/teachers/{id}/research/{research_id}/` | 删除某条成果        |

---

### 4. 教师检索 `/api/search/`

| 方法  | 路径                      | 说明                                           |
| --- | ----------------------- | -------------------------------------------- |
| GET | `/api/search/teachers/` | 全局多维度搜索，支持 `q=关键词`、`department=`、`research=` |

---

### 5. 教师推荐 `/api/recommendations/`

| 方法  | 路径                      | 说明                |
| --- | ----------------------- | ----------------- |
| GET | `/api/recommendations/` | 根据用户特征/历史行为返回推荐导师 |

---

### 6. 预约模块 `/api/appointments/`

| 方法        | 路径                        | 说明                     |
| --------- | ------------------------- | ---------------------- |
| GET       | `/api/appointments/`      | 我的预约列表（学生或教师角色区分）      |
| POST      | `/api/appointments/`      | 学生对导师发起新预约（请求体包括导师、时间） |
| GET       | `/api/appointments/{id}/` | 查看某条预约详情               |
| PUT/PATCH | `/api/appointments/{id}/` | 教师审核：接受/拒绝/改期          |
| DELETE    | `/api/appointments/{id}/` | 取消预约                   |

---

### 7. 管理与同步 `/api/admin/`

| 方法        | 路径                                        | 说明             |
| --------- | ----------------------------------------- | -------------- |
| POST      | `/api/admin/sync/externalsources/`        | 配置并触发外部平台数据同步  |
| GET       | `/api/admin/users/`                       | 列出所有用户         |
| PUT/PATCH | `/api/admin/users/{user_id}/permissions/` | 更新用户角色与权限      |
| GET/PUT   | `/api/admin/stats/`                       | 查看&配置推荐算法与系统统计 |

---

### 8. 其他公共/认证接口

| 方法   | 路径                    | 说明              |
| ---- | --------------------- | --------------- |
| POST | `/api/auth/login/`    | 登录，返回 JWT token |
| POST | `/api/auth/logout/`   | 注销              |
| POST | `/api/auth/register/` | 注册（学生/教师）       |
| GET  | `/api/auth/user/`     | 获取当前登录用户信息      |

---

# 接口API

下面以[ **RESTful** 风格](https://blog.csdn.net/zzvar/article/details/118164133)，结合前后端路由设计，给出详细的接口文档。所有接口均以 `http://<域名>/api/` 为前缀，并使用 **JSON** 格式请求与响应。

统一要求：

* 所有修改类 (POST/PUT/PATCH/DELETE) 接口都需在请求头中带 `Authorization: Bearer <token>`（除登录、注册外）。
* 时间字段一律采用 ISO 8601，如 `"2025-06-01T10:00:00Z"`。
* 错误返回统一 `{ "code": <int>, "message": <string>, "details": <object?> }`。

---

## 1. 认证与用户

| 方法 | 路径                    | 描述              | 请求体                                  | 响应体                                            |
| ---- | ----------------------- | ----------------- | --------------------------------------- | ------------------------------------------------- |
| POST | `/api/auth/register/` | 注册（学生/教师） | `{ username, password, email, role }` | `{ id, username, email, role, created_at }`     |
| POST | `/api/auth/login/`    | 登录              | `{ username, password }`              | `{ token, user: { id, username, email, role }}` |
| POST | `/api/auth/logout/`   | 注销              | —                                      | `{ message: "Logged out" }`                     |
| GET  | `/api/auth/user/`     | 当前用户信息      | —                                      | `{ id, username, email, role, created_at }`     |

---

## 2. 用户管理（仅管理员）

| 方法   | 路径                        | 描述              | 请求体                | 响应体                                          |
| ------ | --------------------------- | ----------------- | --------------------- | ----------------------------------------------- |
| GET    | `/api/admin/users/`       | 列出所有用户      | —                    | `[{ id, username, email, role, created_at }]` |
| PUT    | `/api/admin/users/{uid}/` | 更新用户角色/信息 | `{ email?, role? }` | 更新后的用户对象                                |
| DELETE | `/api/admin/users/{uid}/` | 删除用户          | —                    | `{ message: "Deleted" }`                      |

---

## 3. 教师档案

### 3.1 列表与检索

| 方法 | 路径               | 描述     | 参数                                          | 响应体                                                                                        |
| ---- | ------------------ | -------- | --------------------------------------------- | --------------------------------------------------------------------------------------------- |
| GET  | `/api/teachers/` | 教师列表 | `?name=&department=&research_areas=&title=` | `[{ id, user_id, name, department, title, research_areas, homepage_url, avatar_url, bio }]` |

### 3.2 详情、创建、更新、删除

| 方法      | 路径                     | 描述     | 请求体                                                                                       | 响应体                     |
| --------- | ------------------------ | -------- | -------------------------------------------------------------------------------------------- | -------------------------- |
| GET       | `/api/teachers/{tid}/` | 教师详情 | —                                                                                           | 单个教师对象               |
| POST      | `/api/teachers/`       | 新增教师 | `{ user_id, name, department, title?, research_areas?, homepage_url?, avatar_url?, bio? }` | 新建的教师对象             |
| PUT/PATCH | `/api/teachers/{tid}/` | 更新教师 | 可选字段同 POST                                                                              | 更新后的教师对象           |
| DELETE    | `/api/teachers/{tid}/` | 删除教师 | —                                                                                           | `{ message: "Deleted" }` |

---

## 4. 日程管理

| 方法      | 路径                                    | 描述         | 请求体                                                  | 响应体                                                                                                |
| --------- | --------------------------------------- | ------------ | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| GET       | `/api/teachers/{tid}/schedule/`       | 导师所有日程 | —                                                      | `[{ id, teacher_id, start_time, end_time, is_available, external_source, external_id, synced_at }]` |
| POST      | `/api/teachers/{tid}/schedule/`       | 新建时段     | `{ start_time, end_time, is_available? (默认 true) }` | 新建的时段对象                                                                                        |
| PUT/PATCH | `/api/teachers/{tid}/schedule/{sid}/` | 更新时段     | `{ start_time?, end_time?, is_available? }`           | 更新后的时段对象                                                                                      |
| DELETE    | `/api/teachers/{tid}/schedule/{sid}/` | 删除时段     | —                                                      | `{ message: "Deleted" }`                                                                            |

---

## 5. 科研成果管理

| 方法      | 路径                                    | 描述         | 请求体                                                          | 响应体                                                             |
| --------- | --------------------------------------- | ------------ | --------------------------------------------------------------- | ------------------------------------------------------------------ |
| GET       | `/api/teachers/{tid}/research/`       | 导师成果列表 | —                                                              | `[{ id, teacher_id, title, type, date, description, file_url }]` |
| POST      | `/api/teachers/{tid}/research/`       | 新增成果     | `{ title, type, date (YYYY-MM-DD), description?, file_url? }` | 新建的成果对象                                                     |
| PUT/PATCH | `/api/teachers/{tid}/research/{rid}/` | 更新成果     | 可选字段同 POST                                                 | 更新后的成果对象                                                   |
| DELETE    | `/api/teachers/{tid}/research/{rid}/` | 删除成果     | —                                                              | `{ message: "Deleted" }`                                         |

---

## 6. 全局搜索

| 方法 | 路径                      | 描述           | 参数                                | 响应体       |
| ---- | ------------------------- | -------------- | ----------------------------------- | ------------ |
| GET  | `/api/search/teachers/` | 多维度搜索导师 | `?q=&department=&research_areas=` | 教师对象数组 |

---

## 7. 推荐系统

| 方法 | 路径                      | 描述     | 参数                         | 响应体                          |
| ---- | ------------------------- | -------- | ---------------------------- | ------------------------------- |
| GET  | `/api/recommendations/` | 推荐导师 | 可选 `?student_id=&limit=` | `[{ teacher: {...}, score }]` |

---

## 8. 预约管理

| 方法      | 路径                         | 描述               | 请求体                                  | 响应体                                                           |
| --------- | ---------------------------- | ------------------ | --------------------------------------- | ---------------------------------------------------------------- |
| GET       | `/api/appointments/`       | 我的预约列表       | —                                      | `[{ id, student_id, teacher_id, time_slot, status, remarks }]` |
| POST      | `/api/appointments/`       | 新建预约           | `{ teacher_id, time_slot, remarks? }` | 新建的预约对象                                                   |
| GET       | `/api/appointments/{aid}/` | 预约详情           | —                                      | 单个预约对象                                                     |
| PUT/PATCH | `/api/appointments/{aid}/` | 教师审核（改状态） | `{ status: 'accepted'                   | 'rejected', remarks? }`                                          |
| DELETE    | `/api/appointments/{aid}/` | 取消预约           | —                                      | `{ message: "Deleted" }`                                       |

---

## 9. 推荐参数与统计（管理员）

| 方法 | 路径                                        | 描述             | 请求体         | 响应体                                                             |
| ---- | ------------------------------------------- | ---------------- | -------------- | ------------------------------------------------------------------ |
| GET  | `/api/admin/stats/`                       | 查看系统统计     | —             | `{ total_users, total_teachers, total_apps, search_count, ... }` |
| GET  | `/api/admin/recommendation/params/`       | 查看推荐算法参数 | —             | `[{ id, factor, weight }]`                                       |
| PUT  | `/api/admin/recommendation/params/{pid}/` | 更新参数         | `{ weight }` | 更新后的参数对象                                                   |

---

## 10. 外部数据同步（管理员）

| 方法 | 路径                                 | 描述         | 请求体                  | 响应体                                        |
| ---- | ------------------------------------ | ------------ | ----------------------- | --------------------------------------------- |
| POST | `/api/admin/sync/externalsources/` | 触发同步     | `{ source: 'gongda'     | 'baidu' }`                                    |
| GET  | `/api/admin/sync/logs/`            | 同步日志列表 | 可分页 `?page=&size=` | `[{ id, source, status, details, run_at }]` |

---

## 11. 通知

| 方法 | 路径                               | 描述         | 请求体 | 响应体                                           |
| ---- | ---------------------------------- | ------------ | ------ | ------------------------------------------------ |
| GET  | `/api/notifications/`            | 我的通知列表 | —     | `[{ id, type, content, is_read, created_at }]` |
| PUT  | `/api/notifications/{nid}/read/` | 标记为已读   | —     | `{ message: "Marked read" }`                   |

---

以上接口文档完整涵盖了用户故事中的所有功能模块，并兼顾了权限与可维护性。根据实际开发可再补充分页、筛选、排序等细节。

## 12. 举例

在前后端分离架构中，**API 接口（通常是 RESTful API）**充当前端与后端之间通信的桥梁。前端（如 Vue）通过 HTTP 请求向后端（如 Django）发送请求，后端处理业务逻辑并返回数据（通常是 JSON 格式）给前端展示。

---

## ✅ 一、前后端分离中 API 接口作用

* **前端** ：仅负责界面展示与交互逻辑，不直接处理数据库；
* **后端** ：通过 API 接口处理数据读取、写入、权限校验等，返回前端所需数据；
* **接口作用** ：让前端无须了解后端实现细节即可使用后端能力。

---

## ✅ 二、示例：教师信息管理系统中的接口调用

### 🎯 场景：学生在前端页面搜索导师

---

### 🌐 示例 API 接口设计（后端 Django DRF）：

```http
GET /api/teachers/?keyword=人工智能&department=计算机学院
```

* **方法** ：GET
* **路径** ：`/api/teachers/`
* **查询参数** ：
* `keyword`：关键词（如导师研究方向）
* `department`：学院

### ✅ 后端 Django 接口代码示例（简化）

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Teacher
from .serializers import TeacherSerializer

class TeacherListView(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword', '')
        department = request.GET.get('department', '')
    
        queryset = Teacher.objects.all()
        if keyword:
            queryset = queryset.filter(research_area__icontains=keyword)
        if department:
            queryset = queryset.filter(department=department)
    
        serializer = TeacherSerializer(queryset, many=True)
        return Response(serializer.data)
```

---

### 💻 前端 Vue 调用接口示例（使用 Axios）：

```javascript
// TeacherSearch.vue
import axios from 'axios'

export default {
  data() {
    return {
      teachers: [],
      keyword: '',
      department: ''
    }
  },
  methods: {
    searchTeachers() {
      axios.get('/api/teachers/', {
        params: {
          keyword: this.keyword,
          department: this.department
        }
      }).then(response => {
        this.teachers = response.data
      }).catch(error => {
        console.error('搜索失败：', error)
      })
    }
  }
}
```

---

### 🧾 接口返回数据示例（JSON）

```json
[
  {
    "id": 1,
    "name": "李明",
    "department": "计算机学院",
    "research_area": "人工智能、深度学习",
    "email": "liming@example.com"
  },
  {
    "id": 2,
    "name": "王晓红",
    "department": "计算机学院",
    "research_area": "机器学习、数据挖掘",
    "email": "wangxh@example.com"
  }
]
```

---










# 附录

## 1. 安装、使用 virtualenv 虚拟环境

> 虚拟环境：[PyCharm Django Python 开发环境配置 详细教程 - FreeK0x00 - 博客园 (cnblogs.com)](https://www.cnblogs.com/wuhongbin/p/14318656.html)

（1）安装 virtualenv 虚拟环境：

```
 pip install virtualenv

```

**使用虚拟环境**：

（2）创建虚拟环境目录 testvir

```
 ...> virtualenv [testvir]

```

（3）进入虚拟环境目录

```
 ...> cd testvir

```

（4）查看目录

```
 ...> dir

```

（5）进入 Scripts 工作目录

```
 ...>testvir> cd Scripts

```

（6）激活当前虚拟环境

```
 ...>Scripts> activate.bat  或者  cd Scripts

```

（7）查看当前环境

```
 (testvir) ... >Scripts> pip list

```

（8）退出虚拟环境

```
 (testvir) ... >Scripts> deactivate.bat

```



## 2. 在 Django 中使用 MySQL 作为数据库

需要以下步骤：

### 安装 MySQL 驱动

安装 PyMySQL，这是 Python 连接 MySQL 的驱动：

```bash
pip install pymysql

```

### 配置 Django 项目

修改 Django 项目的 `settings.py` 文件，配置数据库连接信息：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 指定了要使用的数据库后端
        'NAME': 'teacher_info_manage',
        'USER': 'admin',
        'PASSWORD': '456666',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

```

### 连接测试

确保 Django 能够连接到 MySQL 数据库。可以通过以下命令运行 Django 的检查工具：

```bash
python manage.py check

```

如果没有错误信息，说明连接配置正确。



### 示例

以下是一个完整的示例：

#### 安装 PyMySQL

```bash
pip install pymysql

```

#### 配置 `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

```

#### 在 Django 中使用

在 Django 项目中，可以使用 Django 的 ORM 来操作数据库。例如：

```python
from django.db import models

class MyModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()

```

运行 Django 的迁移命令来创建数据库表：

```bash
python manage.py makemigrations
python manage.py migrate

```

### 常见问题

- **连接失败**：检查 MySQL 服务是否运行，用户名、密码、数据库名是否正确。
- **权限不足**：确保 MySQL 用户有权限访问指定数据库。
- **驱动问题**：确保 pyMySQL 已正确安装。
- **防火墙限制**：如果 MySQL 服务器在远程主机上，确保防火墙允许连接到 MySQL 的端口（默认 3306）。



## Django项目框架

**创建项目**

### 使用命令行创建项目

```
django-admin startproject 项目名称
```

**项目目录介绍**

```
|---mysite # 项目的/目录 
  |---mysite # 项目目录 
      |---__init__.py 
      |---settings.py # 配置文件 
      |---urls.py # 路由系统 ===> url与视图的对应关系 
      |---wsgi.py # runserver命令就使用wsgiref模块做简单的web server 
|---manage.py # 管理文件
```















## 项目相关

### 项目选题

教师信息管理系统              16

**为了便于学生选择合适的导师，也为了宣传教师的信息，希望构造教师信息** 

**管理系统，将教师的信息统一管理，便于教师及时更新发布信息，便于学生** 

**浏览教师信息，并可以预约教师。** 

– 提供教师基本信息，可同工大主页、百度知道等结合 

– 提供教师日程 

– 提供教师基金和科研成果， 

– 教师检索 

– 教师推荐 

– 提供教师预约功能 

– 附注：可同教师的在线日历等关联



### 学生角色

**卡片ID**：S-01
**标题**：按关键词与条件搜索导师
**正面：用户故事**：作为学生，我希望在系统中通过姓名、学科关键词、学院或研究方向等多维度条件进行搜索与筛选，以便快速定位合适的导师。
**反面：成功与失败场景**：

- **成功**：输入关键词后，系统实时返回多条符合条件的教师列表，学生能点击进入详情页。
- **失败**：输入无效关键词或网络异常时，系统提示“未找到结果”或“网络错误，请重试”。
  **优先级**：高
  **备注**：需与后端检索 API 联调。

**卡片ID**：S-02
**标题**：浏览导师详情与科研成果
**正面：用户故事**：作为学生，我希望在导师详情页查看其个人简介、教学与科研背景、基金项目和论文成果，以便评估导师的学术水平和研究方向。
**反面：成功与失败场景**：

- **成功**：详情页模块加载完整，科研成果按年份排序，点击外链可正常跳转。
- **失败**：若成果数据缺失或接口超时，系统展示“暂无数据”提示，并允许刷新重试。
  **优先级**：中
  **备注**：与教师端数据展示保持一致风格。

**卡片ID**：S-03
**标题**：查看并同步导师日程
**正面：用户故事**：作为学生，我希望能在老师详情页查看其公开的日程和可预约时间，并同步到我的个人日历，以便合理安排面谈时间。
**反面：成功与失败场景**：

- **成功**：点击“一键同步”后，日程正确导入用户日历，并在提醒中心显示同步记录。
- **失败**：若第三方日历接口授权失败或导出文件损坏，系统提示“同步失败，请检查授权或重试”。
  **优先级**：高
  **备注**：需评估日历 API 限制与数据安全。

**卡片ID**：S-04
**标题**：在线预约与通知
**正面：用户故事**：作为学生，我希望提交预约申请后，能收到系统确认消息和日程变更通知，以便及时调整计划。
**反面：成功与失败场景**：

- **成功**：预约提交后，系统发送“预约成功”通知；若教师接受或拒绝，分别发送确认或改期通知。
- **失败**：若教师未响应或网络异常，系统定时提醒用户并允许重新提交。
  **优先级**：高
  **备注**：需与消息中心与邮件服务集成。

卡片ID**：S-05**

标题**：**学生获得教师推荐

- **用户角色** ：学生
- **功能需求** ：能够根据自己的专业、兴趣等因素，获得系统推荐的教师。
- **验收条件** ：学生登录系统后，在首页的 “推荐教师” 区域，系统根据学生所学专业和之前浏览的教师信息等，推荐 3 - 5 位合适的教师，推荐结果符合逻辑且有一定针对性。

------

### 教师角色

**卡片ID**：T-01
**标题**：维护个人主页与科研展示
**正面：用户故事**：作为教师，我希望自由编辑个人主页内容，包括头像、简介、研究方向、项目和成果展示，以便学生了解我的专业背景。
**反面：成功与失败场景**：

- **成功**：编辑后页面即时预览，发布后学生端可立即查看最新信息。
- **失败**：若富文本内容格式错误或保存失败，系统展示详细错误并保留编辑内容。
  **优先级**：高
  **备注**：需实现富文本编辑器与版本控制功能。

**卡片ID**：T-02
**标题**：设置日程与第三方日历同步
**正面：用户故事**：作为教师，我希望设置可预约的办公时间，并将日程与 Google Calendar、Outlook 等第三方日历同步，以减少重复维护。
**反面：成功与失败场景**：

- **成功**：OAuth 授权完成后，办公时间自动推送至第三方日历；后续调整也即时同步。
- **失败**：授权超时或 API 限制，系统提示“同步暂不可用”，并保留本地配置。
  **优先级**：高
  **备注**：需评估 OAuth 安全与频率限制。

**卡片ID**：T-03
**标题**：审批与管理预约请求
**正面：用户故事**：作为教师，我希望在系统内查看学生的预约请求详情，并能够接受、拒绝或提出改期建议，以便高效安排。
**反面：成功与失败场景**：

- **成功**：审批操作后，系统实时更新请求状态并发送通知；列表准确反映当前状态。
- **失败**：若操作超时或通知发送失败，系统提示“操作失败，请重试”并保留原有请求状态。
  **优先级**：中
  **备注**：与通知中心、日志管理关联。

------

### 管理员角色

**卡片ID**：A-01
**标题**：管理平台用户与权限
**正面：用户故事**：作为管理员，我希望能够创建、编辑与删除学生和教师账号，并分配相应角色和权限，以保证系统安全与数据准确。
**反面：成功与失败场景**：

- **成功**：用户操作后系统日志记录完整，账号变动即时生效；相应人员收到通知。
- **失败**：若批量导入文件格式错误或超出权限范围，系统提示具体错误并回滚操作。
  **优先级**：高
  **备注**：需与权限框架（RBAC）集成。

**卡片ID**：A-02
**标题**：定时同步外部数据源
**正面：用户故事**：作为管理员，我希望配置并执行与工大主页、百度知道等外部平台的教师信息定时同步，以保持数据最新。
**反面：成功与失败场景**：

- **成功**：同步任务定时执行，新增/更新数据准确导入；日志显示成功明细。
- **失败**：若接口限流或数据冲突，系统在日志中记录失败项，并生成报表供人工审核。
  **优先级**：中
  **备注**：需考虑 API 限流与数据清洗。

**卡片ID**：A-03
**标题**：推荐算法与统计报表
**正面：用户故事**：作为管理员，我希望能调整导师推荐算法参数，并查看系统使用统计（搜索热度、预约量、活跃用户），以优化系统效果。
**反面：成功与失败场景**：

- **成功**：参数调整后推荐结果及时更新，并能在测试环境对比效果；统计报表准确展示数据。
- **失败**：若算法执行异常或统计接口超时，系统提示“操作失败”，并可回滚至上一个稳定版本。
  **优先级**：低
  **备注**：初期可使用默认参数，后续迭代。

------

### 产品待办列表（Backlog）

以下为基于用户故事卡片整理的产品待办列表（Backlog），已按优先级从高到低排序，数字越大优先级越高。上游故事编号对应本表中的“用户故事编号”。

| 用户故事编号 | 用户故事简称             | 用户故事描述                                                 | 优先级估算 | 上游故事编号 |
| ------------ | ------------------------ | ------------------------------------------------------------ | ---------- | ------------ |
| 1            | 学生搜索导师             | 作为学生，我希望在系统中通过姓名、学科关键词、学院或研究方向等多维度条件进行搜索与筛选，以便快速定位合适的导师。 | 5          | –            |
| 2            | 查看并同步导师日程       | 作为学生，我希望能在导师详情页查看其公开的日程和可预约时间，并同步到我的个人日历，以便合理安排面谈时间。 | 5          | 1            |
| 3            | 在线预约与通知           | 作为学生，我希望提交预约申请后，能收到系统确认消息和日程变更通知，以便及时调整计划。 | 5          | 2            |
| 4            | 维护个人主页与科研展示   | 作为教师，我希望自由编辑个人主页内容，包括头像、简介、研究方向、项目和成果展示，以便学生了解我的专业背景。 | 5          | –            |
| 5            | 设置日程与第三方日历同步 | 作为教师，我希望设置可预约的办公时间，并将日程与 Google Calendar、Outlook 等第三方日历同步，以减少重复维护。 | 5          | 4            |
| 6            | 管理平台用户与权限       | 作为管理员，我希望能够创建、编辑与删除学生和教师账号，并分配相应角色和权限，以保证系统安全与数据准确。 | 5          | –            |
| 7            | 浏览导师详情与科研成果   | 作为学生，我希望在导师详情页查看其个人简介、教学与科研背景、基金项目和论文成果，以便评估导师的学术水平和研究方向。 | 3          | 1            |
| 8            | 学生查询推荐教师         | 作为学生，我希望能够根据自己的专业、兴趣等因素，获得系统推荐的教师。 | 3          | 1            |
| 9            | 审批与管理预约请求       | 作为教师，我希望在系统内查看学生的预约请求详情，并能够接受、拒绝或提出改期建议，以便高效安排。 | 3          | 5            |
| 10           | 外部数据源定时同步       | 作为管理员，我希望配置并执行与工大主页、百度知道等外部平台的教师信息定时同步，以保持数据最新。 | 3          | –            |
| 11           | 推荐算法与统计报表       | 作为管理员，我希望能调整导师推荐算法参数，并查看系统使用统计（搜索热度、预约量、活跃用户），以优化系统效果。 | 1          | –            |

