import { defineStore } from 'pinia'
import api from '../api'
import { ElMessage } from 'element-plus'
import router from '../router'

// 清除所有cookie的函数
const clearAllCookies = () => {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i]
        const eqPos = cookie.indexOf('=')
        const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim()
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=${window.location.hostname};`
    }
}

// 清除session的函数
const clearSession = async () => {
    try {
        await api.post('/clear-session/')
        clearAllCookies()
    } catch (error) {
        console.error('Clear session error:', error)
        clearAllCookies()
    }
}

export const useUserStore = defineStore('user', {
    state: () => ({
        user: JSON.parse(localStorage.getItem('user') || 'null'),
        token: localStorage.getItem('token') || null,
        isLoggedIn: !!localStorage.getItem('token'),
        role: localStorage.getItem('role') || null
    }),

    getters: {
        isStudent: (state) => state.role === 'student',
        isTeacher: (state) => state.role === 'teacher',
        isAdmin: (state) => state.role === 'admin'
    },

    actions: {
        async login(credentials) {
            try {
                // 在登录前先清除所有session
                await clearSession()

                const response = await api.post('/login/', credentials)
                console.log('Login response:', response) // 添加调试日志

                if (response && response.user) {
                    this.user = response.user
                    this.role = response.user.role
                    this.isLoggedIn = true
                    localStorage.setItem('user', JSON.stringify(this.user))
                    localStorage.setItem('role', this.role)
                    localStorage.setItem('token', 'session')
                    this.token = 'session'
                    ElMessage.success(response.message || '登录成功')
                    return response
                } else {
                    throw new Error('登录响应格式错误')
                }
            } catch (error) {
                console.error('Login error:', error) // 添加调试日志
                this.logout()
                throw error
            }
        },

        async register(userData) {
            try {
                const response = await api.post('/register/', userData)
                ElMessage.success(response.message || '注册成功')
                return response
            } catch (error) {
                throw error
            }
        },

        async logout() {
            try {
                await api.post('/logout/')
                // 清除所有本地存储
                localStorage.clear()
                sessionStorage.clear()

                // 清除所有cookie
                clearAllCookies()

                // 重置状态
                this.user = null
                this.role = null
                this.isLoggedIn = false
                this.token = null

                // 强制刷新页面以确保所有状态都被清除
                window.location.href = '/'
            } catch (error) {
                console.error('Logout error:', error)
                // 即使API调用失败，也清除本地状态
                localStorage.clear()
                sessionStorage.clear()
                clearAllCookies()
                this.user = null
                this.role = null
                this.isLoggedIn = false
                this.token = null
                window.location.href = '/'
            }
        },

        async checkAuth() {
            try {
                const response = await api.get('/user/')
                console.log('Check auth response:', response) // 添加调试日志
                if (response) {
                    this.user = response
                    this.role = response.role
                    this.isLoggedIn = true
                    localStorage.setItem('user', JSON.stringify(this.user))
                    localStorage.setItem('role', this.role)
                }
            } catch (error) {
                console.error('Check auth error:', error) // 添加调试日志
                this.logout()
            }
        },

        async updateProfile(profileData) {
            try {
                const response = await api.put('/user/profile/', profileData)
                this.user = { ...this.user, ...response }
                localStorage.setItem('user', JSON.stringify(this.user))
                ElMessage.success('个人信息更新成功')
                return response
            } catch (error) {
                throw error
            }
        }
    }
}) 