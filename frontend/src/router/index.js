import { createRouter, createWebHistory } from 'vue-router'
import RegisterView from '@/views/auth/RegisterView.vue'
import LoginView from '@/views/auth/LoginView.vue'

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
            component: LoginView
        },
        {
            path: '/register',
            name: 'register',
            component: RegisterView
        }
    ]
})

export default router