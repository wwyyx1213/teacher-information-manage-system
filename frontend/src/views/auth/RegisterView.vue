<template>
  <div class="register-view">
    <el-card class="register-card">
      <h2>用户注册</h2>
      <el-form :model="registerForm" :rules="registerRules" ref="registerFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" />
        </el-form-item>
        <el-form-item label="账户类型" prop="role">
          <el-select v-model="registerForm.role" placeholder="请选择账户类型">
            <el-option label="学生" value="student" />
            <el-option label="老师" value="teacher" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onRegister">注册</el-button>
        </el-form-item>
      </el-form>
      <div class="login-link">
        已有账号？
        <el-link type="primary" @click="goLogin">去登录</el-link>
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
const registerFormRef = ref(null)
const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: '',
  role: ''
})

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {
    if (registerForm.value.confirmPassword !== '') {
      registerFormRef.value.validateField('confirmPassword')
    }
    callback()
  }
}

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.value.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ validator: validatePass, trigger: 'blur' }],
  confirmPassword: [{ validator: validatePass2, trigger: 'blur' }],
  role: [{ required: true, message: '请选择账户类型', trigger: 'change' }]
}

const onRegister = () => {
  registerFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await api.post('/register/', {
          username: registerForm.value.username,
          password: registerForm.value.password,
          role: registerForm.value.role
        })
        ElMessage.success('注册成功')
        router.push('/login')
        registerForm.value = { username: '', password: '', confirmPassword: '', role: '' }
      } catch (e) {
        ElMessage.error('注册失败：' + (e.response?.data?.message || '未知错误'))
      }
    }
  })
}

const goLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-view {
  min-height: calc(100vh - 60px);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 60px;
}
.register-card {
  width: 400px;
  padding: 20px;
  position: relative;
}
.login-link {
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