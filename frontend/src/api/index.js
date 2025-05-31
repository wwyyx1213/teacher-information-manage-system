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
    response => {
        return response.data
    },
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // 未授权，清除token并跳转到登录页
                    localStorage.removeItem('token')
                    window.location.href = '/login'
                    break
                case 403:
                    // 权限不足
                    console.error('权限不足')
                    break
                case 404:
                    // 请求的资源不存在
                    console.error('请求的资源不存在')
                    break
                case 500:
                    // 服务器错误
                    console.error('服务器错误')
                    break
                default:
                    console.error('发生错误：', error.response.data)
            }
        }
        return Promise.reject(error)
    }
)

export default api 