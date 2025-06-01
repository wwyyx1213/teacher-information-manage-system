import { defineStore } from 'pinia'
import api from '../api'
import { ElMessage } from 'element-plus'
import router from '../router'

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
                const response = await api.post('/login/', credentials)
                this.user = response.user
                this.role = response.user.role
                this.isLoggedIn = true
                localStorage.setItem('user', JSON.stringify(this.user))
                localStorage.setItem('role', this.role)
                localStorage.setItem('token', 'session')
                this.token = 'session'
                ElMessage.success(response.message || '登录成功')
                return response
            } catch (error) {
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
            } catch (error) {
                console.error('Logout error:', error)
            } finally {
                this.user = null
                this.token = null
                this.isLoggedIn = false
                this.role = null
                localStorage.removeItem('token')
                localStorage.removeItem('user')
                localStorage.removeItem('role')

                document.cookie.split(';').forEach(cookie => {
                    const [name] = cookie.trim().split('=')
                    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`
                })

                router.push('/')
                window.location.reload()
            }
        },

        async checkAuth() {
            try {
                const response = await api.get('/user/')
                this.user = response
                this.role = response.role
                this.isLoggedIn = true
                localStorage.setItem('user', JSON.stringify(this.user))
                localStorage.setItem('role', this.role)
            } catch (error) {
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