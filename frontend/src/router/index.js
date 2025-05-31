import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/student/dashboard',
    name: 'StudentDashboard',
    component: () => import('../views/student/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/teacher/dashboard',
    name: 'TeacherDashboard',
    component: () => import('../views/teacher/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teachers',
    name: 'teachers',
    component: () => import('../views/TeacherListView.vue')
  },
  {
    path: '/teachers/:id',
    name: 'teacher-detail',
    component: () => import('../views/TeacherDetailView.vue')
  },
  {
    path: '/teachers/:id/schedule',
    name: 'teacher-schedule',
    component: () => import('../views/ScheduleView.vue')
  },
  {
    path: '/teachers/:id/research',
    name: 'teacher-research',
    component: () => import('../views/ResearchView.vue')
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('../views/SearchView.vue')
  },
  {
    path: '/recommendations',
    name: 'recommendations',
    component: () => import('../views/RecommendView.vue')
  },
  {
    path: '/appointments',
    name: 'appointments',
    component: () => import('../views/MyAppointments.vue')
  },
  {
    path: '/appointments/new/:tid',
    name: 'new-appointment',
    component: () => import('../views/AppointmentForm.vue')
  },
  {
    path: '/appointments/:id',
    name: 'appointment-detail',
    component: () => import('../views/AppointmentDetail.vue')
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/ProfileView.vue')
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('../views/AdminDashboard.vue')
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: () => import('../views/UserManageView.vue')
  },
  {
    path: '/admin/sync',
    name: 'admin-sync',
    component: () => import('../views/DataSyncView.vue')
  },
  {
    path: '/admin/stats',
    name: 'admin-stats',
    component: () => import('../views/StatsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  if (to.meta.requiresAuth) {
    if (!user.id) {
      next('/login')
    } else if (to.meta.role && to.meta.role !== user.role) {
      next(user.role === 'student' ? '/student/dashboard' : '/teacher/dashboard')
    } else {
      next()
    }
  } else {
    if (user.id && (to.path === '/login' || to.path === '/register')) {
      next(user.role === 'student' ? '/student/dashboard' : '/teacher/dashboard')
    } else {
      next()
    }
  }
})

export default router
