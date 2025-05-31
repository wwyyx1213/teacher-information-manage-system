## 提示词

请根据项目文档README.md（其中数据库和url不能变）优化项目中首页设计，要求要满足文档内要求，界面要美观，符合人类审美，然后同时请连通前后端间（告诉含API的请求体和响应体），且给出测试步骤，前后端均在当前目录下，backend为后端django，frontend为前端vue（使用element ui）









注册接口：

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
     
     
     响应体：
         {
           "message": "注册成功",
           "user": {
             "id": 用户ID,
             "username": "用户名",
             "email": "邮箱",
             "role": "角色"
           }
         }
         
     {
        "message": "注册成功",
        "user": {
            "id": 15,
            "username": "ouu",
            "role": "student"
        }
    }


 

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






