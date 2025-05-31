import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue')
    },
    {
      path: '/teachers',
      name: 'teachers',
      component: () => import('../views/teacher/TeacherList.vue')
    },
    {
      path: '/teachers/:id',
      name: 'teacher-detail',
      component: () => import('../views/teacher/TeacherDetail.vue')
    },
    {
      path: '/my-appointments',
      name: 'my-appointments',
      component: () => import('../views/student/MyAppointments.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/appointments',
      name: 'appointments',
      component: () => import('../views/teacher/Appointments.vue'),
      meta: { requiresAuth: true, role: 'teacher' }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.meta.role && to.meta.role !== userStore.role) {
    next('/')
  } else {
    next()
  }
})

export default router
