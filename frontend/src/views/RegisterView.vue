<template>
    <div class="register-container">
        <el-card class="register-card">
            <template #header>
                <h2>注册</h2>
            </template>
            <el-form :model="registerForm" :rules="rules" ref="registerFormRef">
                <el-form-item prop="username">
                    <el-input v-model="registerForm.username" placeholder="用户名">
                        <template #prefix>
                            <el-icon><User /></el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input v-model="registerForm.password" type="password" placeholder="密码">
                        <template #prefix>
                            <el-icon><Lock /></el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="email">
                    <el-input v-model="registerForm.email" placeholder="邮箱">
                        <template #prefix>
                            <el-icon><Message /></el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="role">
                    <el-select v-model="registerForm.role" placeholder="选择角色" style="width: 100%;">
                        <el-option label="学生" value="student"></el-option>
                        <el-option label="教师" value="teacher"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleRegister" style="width: 100%">
                        注册
                    </el-button>
                </el-form-item>
                <div class="login-link">
                    已有账号？<router-link to="/login">立即登录</router-link>
                </div>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue' // Import icons

const router = useRouter()
const userStore = useUserStore()
const registerFormRef = ref(null)

const registerForm = reactive({
    username: '',
    password: '',
    email: '',
    role: ''
})

const rules = {
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
    ],
    email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] }
    ],
    role: [
        { required: true, message: '请选择角色', trigger: 'change' }
    ]
}

const handleRegister = async () => {
    if (!registerFormRef.value) return

    await registerFormRef.value.validate(async (valid) => {
        if (valid) {
            try {
                await userStore.register(registerForm)
                ElMessage.success('注册成功，请登录') // Assuming registration doesn't auto-login
                router.push('/login') // Redirect to login page after successful registration
            } catch (error) {
                ElMessage.error(error.response?.data?.message || '注册失败')
            }
        }
    })
}
</script>

<style scoped>
.register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 60px);
    background-color: #f5f7fa;
}

.register-card {
    width: 100%;
    max-width: 400px;
}

.register-card :deep(.el-card__header) {
    text-align: center;
}

.login-link {
    text-align: center;
    margin-top: 20px;
}

.login-link a {
    color: #409eff;
    text-decoration: none;
}
</style> 