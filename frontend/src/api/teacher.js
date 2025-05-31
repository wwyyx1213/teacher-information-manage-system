import axios from 'axios'

const baseURL = 'http://localhost:8000/api'

// 创建axios实例
const api = axios.create({
    baseURL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 请求拦截器
api.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// 响应拦截器
api.interceptors.response.use(
    response => response.data,
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // 未授权，跳转到登录页
                    window.location.href = '/login'
                    break
                case 403:
                    // 权限不足
                    console.error('权限不足')
                    break
                default:
                    console.error('请求失败')
            }
        }
        return Promise.reject(error)
    }
)

// 教师相关API
export const teacherApi = {
    // 获取教师详情
    getTeacherDetail(id) {
        return api.get(`/teachers/${id}/`)
    },

    // 获取教师日程
    getTeacherSchedule(id) {
        return api.get(`/teachers/${id}/schedule/`)
    },

    // 获取教师科研成果
    getTeacherResearch(id) {
        return api.get(`/teachers/${id}/research/`)
    },

    // 获取可预约时间
    getAvailableDates(id) {
        return api.get(`/teachers/${id}/available-dates/`)
    },

    // 提交预约
    submitAppointment(data) {
        return api.post('/appointments/', data)
    }
}

export default teacherApi 