import api from './index'

// 获取所有用户
export const getAllUsers = () => api.get('/admin/users/').then(res => res.data)

// 新增用户
export const addUser = (data) => api.post('/admin/users/', data).then(res => res.data)

// 删除用户
export const deleteUser = (id) => api.delete(`/admin/users/${id}/`).then(res => res.data)