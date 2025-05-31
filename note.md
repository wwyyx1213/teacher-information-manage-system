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






