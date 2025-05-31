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
    // 获取所有教师
    getAllTeachers() {
        return api.get('/teachers/')
    },

    // 随机获取8个教师
    getRandomTeachers() {
        return api.get('/teachers/random8/')
    },

    // 获取推荐教师
    getRecommendedTeachers() {
        return api.get('/teachers/recommendations/')
    },

    // 搜索教师
    searchTeachers(keyword) {
        return api.get(`/teachers/search/?q=${encodeURIComponent(keyword)}`)
    },

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
    },

    // 教师个人信息（教师端）
    getTeacherProfile() {
        return api.get('/teacher/profile/')
    },
    updateTeacherProfile(data) {
        return api.put('/teacher/profile/', data)
    }
}

export default teacherApi