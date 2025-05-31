import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(
        import.meta.env.BASE_URL),
    routes: [
        // 首页、登录、注册
        {
            path: '/',
            name: 'home',
            component: () =>
                import ('../views/HomeView.vue')
        },
        {
            path: '/login',
            name: 'login',
            component: () =>
                import ('../views/LoginView.vue')
        },
        {
            path: '/register',
            name: 'register',
            component: () =>
                import ('../views/RegisterView.vue')
        },

        // 学生相关
        {
            path: '/teachers',
            name: 'student-teachers',
            component: () =>
                import ('../views/student/TeacherListView.vue')
        },
        {
            path: '/teachers/:id',
            name: 'teacher-detail',
            component: () =>
                import ('../views/student/TeacherDetailView.vue'),
            props: true
        },
        {
            path: '/teachers/:id/:appointments',
            name: 'student-appointment',
            component: () =>
                import ('../views/student/AppointmentView.vue'),
            props: true
        },
        {
            path: '/recommendations',
            name: 'student-recommendations',
            component: () =>
                import ('../views/student/RecommendView.vue')
        },
        {
            path: '/myappointments',
            name: 'student-myappointments',
            component: () =>
                import ('../views/student/MyAppointments.vue')
        },

        // 教师功能
        {
            path: '/teacher/:person',
            name: 'teacher-profile',
            component: () =>
                import ('../views/teacher/PersonView.vue'),
            props: true
        },
        {
            path: '/teacher/:appointments',
            name: 'teacher-appointments',
            component: () =>
                import ('../views/teacher/PersonAppointmentView.vue'),
            props: true
        },

        // 管理员
        {
            path: '/admin',
            name: 'admin-users',
            component: () =>
                import ('../views/admin/UserManageView.vue')
        },
        {
            path: '/admin/sync',
            name: 'admin-sync',
            component: () =>
                import ('../views/admin/DataSyncView.vue')
        }
    ]
})

export default router