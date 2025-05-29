import api from './index'

export const teacherApi = {
    // 获取教师列表
    getTeachers(params) {
        return api.get('/teachers/', { params })
    },

    // 获取教师详情
    getTeacherDetail(id) {
        return api.get(`/teachers/${id}/`)
    },

    // 获取教师日程
    getTeacherSchedule(teacherId) {
        return api.get(`/schedules/`, { params: { teacher: teacherId } })
    },

    // 获取教师项目
    getTeacherProjects(teacherId) {
        return api.get(`/projects/`, { params: { teacher: teacherId } })
    },

    // 获取教师论文
    getTeacherPublications(teacherId) {
        return api.get(`/publications/`, { params: { teacher: teacherId } })
    },

    // 创建预约
    createAppointment(data) {
        return api.post('/appointments/', data)
    }
}