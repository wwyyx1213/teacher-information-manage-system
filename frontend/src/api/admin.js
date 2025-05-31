import api from './index'

// 用户管理
export function getAllUsers() {
    return api.get('/admin/users/')
}
export function updateUser(uid, data) {
    return api.put(`/admin/users/${uid}/`, data)
}
export function deleteUser(uid) {
    return api.delete(`/admin/users/${uid}/`)
}

// 数据同步
export function syncExternalSources(data) {
    return api.post('/admin/sync/externalsources/', data)
}

// 统计与推荐参数
export function getStats() {
    return api.get('/admin/stats/')
}
export function getRecommendationParams() {
    return api.get('/admin/recommendation/params/')
}
export function updateRecommendationParam(pid, data) {
    return api.put(`/admin/recommendation/params/${pid}/`, data)
}