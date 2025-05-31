import api from './index'

export const teacherApi = {
    // 获取教师列表（支持多条件检索）
    getTeachers(params) {
        return api.get('/teachers/', { params })
    },

    // 获取教师详情
    getTeacherDetail(id) {
        return api.get(`/teachers/${id}/`)
    },

    // 获取教师日程
    getTeacherSchedule(teacherId) {
        return api.get(`/teachers/${teacherId}/schedule/`)
    },

    // 新建/同步教师日程
    syncTeacherSchedule(teacherId, data) {
        return api.post(`/teachers/${teacherId}/schedule/`, data)
    },

    // 获取教师科研成果
    getTeacherResearch(teacherId) {
        return api.get(`/teachers/${teacherId}/research/`)
    },

    // 新增科研成果
    addTeacherResearch(teacherId, data) {
        return api.post(`/teachers/${teacherId}/research/`, data)
    }
}