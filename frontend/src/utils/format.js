import dayjs from 'dayjs'

// 格式化日期时间
export const formatDateTime = (datetime) => {
    if (!datetime) return ''
    return dayjs(datetime).format('YYYY-MM-DD HH:mm')
}

// 格式化日期
export const formatDate = (date) => {
    if (!date) return ''
    return dayjs(date).format('YYYY-MM-DD')
}

// 格式化时间
export const formatTime = (time) => {
    if (!time) return ''
    return dayjs(time).format('HH:mm')
}

// 格式化角色显示
export const formatRole = (role) => {
    const roleMap = {
        'admin': '管理员',
        'teacher': '教师',
        'student': '学生'
    }
    return roleMap[role] || role
}

// 格式化状态显示
export const formatStatus = (status) => {
    const statusMap = {
        'pending': '待处理',
        'accepted': '已接受',
        'rejected': '已拒绝'
    }
    return statusMap[status] || status
} 