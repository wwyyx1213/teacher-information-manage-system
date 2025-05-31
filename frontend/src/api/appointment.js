import api from './index'

// 获取我的预约列表
export function getMyAppointments() {
    return api.get('/appointments/')
}

// 新建预约
export function createAppointment(data) {
    return api.post('/appointments/', data)
}

// 获取预约详情
export function getAppointmentDetail(id) {
    return api.get(`/appointments/${id}/`)
}

// 教师审批预约
export function updateAppointment(id, data) {
    return api.put(`/appointments/${id}/`, data)
}