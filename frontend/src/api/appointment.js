import api from './index'

// 学生：获取我的预约
export const getMyAppointments = () => api.get('/appointments/my/').then(res => res.data)

// 教师：获取我的预约
export const getTeacherAppointments = () => api.get('/appointments/teacher/').then(res => res.data)

// 提交预约
export const createAppointment = (data) => api.post('/appointments/', data).then(res => res.data)