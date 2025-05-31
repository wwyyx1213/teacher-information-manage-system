import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
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
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('token')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export function getCaptcha() {
    return api.get('/captcha/')
}

// 登录
export function login(data) {
    return api.post('/auth/login/', data)
}

// 注册
export function register(data) {
    return api.post('/auth/register/', data)
}

// 获取当前用户信息
export function getCurrentUser() {
    return api.get('/auth/user/')
}

export default api