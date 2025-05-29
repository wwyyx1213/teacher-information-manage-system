import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(
        import.meta.env.BASE_URL),
    routes: [{
            path: '/',
            name: 'home',
            component: () =>
                import ('../views/HomeView.vue')
        },
        {
            path: '/teachers',
            name: 'teachers',
            component: () =>
                import ('../views/teacher/TeacherList.vue')
        },
        {
            path: '/teacher/:id',
            name: 'teacher-detail',
            component: () =>
                import ('../views/teacher/TeacherDetail.vue')
        },
        {
            path: '/appointment',
            name: 'appointment',
            component: () =>
                import ('../views/appointment/AppointmentView.vue')
        },
        {
            path: '/login',
            name: 'login',
            component: () =>
                import ('../views/auth/LoginView.vue')
        }
    ]
})

export default router