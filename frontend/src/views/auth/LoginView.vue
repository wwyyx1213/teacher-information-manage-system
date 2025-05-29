<template>
  <div class="login-view">
    <el-card class="login-card">
      <h2>用户登录</h2>
      <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" autocomplete="username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" autocomplete="current-password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onLogin">登录</el-button>
        </el-form-item>
      </el-form>
      <div class="register-link">
        还没有账号？
        <el-link type="primary" @click="goRegister">去注册</el-link>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

const router = useRouter()
const loginFormRef = ref(null)
const loginForm = ref({ username: '', password: '' })
const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const onLogin = () => {
  loginFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const res = await api.post('/login/', loginForm.value)
        localStorage.setItem('token', res.data.token)
        ElMessage.success('登录成功')
        router.push('/')
      } catch (e) {
        ElMessage.error('用户名或密码错误')
      }
    }
  })
}

const goRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-view {
  min-height: calc(100vh - 60px); /* 60px为NavBar高度，如有不同请调整 */
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 60px;
}
.login-card {
  width: 400px;
  padding: 20px;
  position: relative;
}
.register-link {
  position: absolute;
  right: 20px;
  bottom: 16px;
  font-size: 14px;
}
h2 {
  text-align: center;
  margin-bottom: 20px;
}
</style>