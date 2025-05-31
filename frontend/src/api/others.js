import api from './index'

// 全局搜索教师
export function searchTeachers(params) {
    return api.get('/search/teachers/', { params })
}

// 推荐教师
export function getRecommendations(params) {
    return api.get('/recommendations/', { params })
}