import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true  // 允许跨域请求携带cookie
})

// 获取CSRF令牌
function getCsrfToken() {
    const name = 'csrftoken='
    const decodedCookie = decodeURIComponent(document.cookie)
    const cookieArray = decodedCookie.split(';')

    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i].trim()
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length)
        }
    }
    return ''
}

// 请求拦截器
api.interceptors.request.use(
    config => {
        // 如果是退出登录请求，确保不携带 cookie
        if (config.url === '/logout/') {
            config.withCredentials = false
            return config
        }

        // 添加CSRF令牌到请求头
        if (config.method !== 'get') {
            const csrfToken = getCsrfToken()
            if (csrfToken) {
                config.headers['X-CSRFToken'] = csrfToken
            }
        }

        return config
    },
    error => {
        ElMessage.error('请求发送失败')
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
                    // 未授权，清除所有状态
                    localStorage.clear()
                    document.cookie.split(';').forEach(cookie => {
                        const [name] = cookie.trim().split('=')
                        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;`
                    })
                    ElMessage.error('登录已过期，请重新登录')
                    router.push('/login')
                    break
                case 403:
                    ElMessage.error('权限不足')
                    break
                case 404:
                    ElMessage.error('请求的资源不存在')
                    break
                case 500:
                    ElMessage.error('服务器错误')
                    break
                default:
                    ElMessage.error(error.response.data?.message || '发生错误')
            }
        } else {
            ElMessage.error('网络错误，请检查网络连接')
        }
        return Promise.reject(error)
    }
)

export default api 