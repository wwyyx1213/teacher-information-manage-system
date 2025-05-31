import api from './index'

// 登录
export const login = (data) => api.post('/auth/login/', data).then(res => res.data)

// 注册
export const register = (data) => api.post('/auth/register/', data).then(res => res.data)

// 获取当前用户信息
export const getCurrentUser = () => api.get('/auth/user/').then(res => res.data)