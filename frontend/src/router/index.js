import { createRouter, createWebHistory } from 'vue-router'
import TeacherDetailView from '../views/TeacherDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/teachers',
      name: 'teachers',
      component: () => import('../views/TeacherListView.vue')
    },
    {
      path: '/teachers/:id',
      name: 'teacher-detail',
      component: TeacherDetailView,
      props: true
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
})

export default router
