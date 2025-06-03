import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'

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
    },
    {
      path: '/recommendations',
      name: 'recommendations',
      component: () => import('../views/RecommendView.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/admin/UserManageView.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresRole = to.meta.role

  // 如果用户已登录，检查认证状态
  if (userStore.isLoggedIn) {
    try {
      await userStore.checkAuth()
    } catch (error) {
      console.error('检查认证状态失败:', error)
      userStore.logout()
      next('/login')
      return
    }
  }

  // 检查是否需要认证
  if (requiresAuth) {
    if (!userStore.isLoggedIn) {
      ElMessage.warning('请先登录')
      next('/login')
      return
    }

    // 检查角色权限
    if (requiresRole) {
      if (userStore.role !== requiresRole) {
        ElMessage.error('权限不足')
        if (userStore.role === 'admin') {
          next('/admin')
        } else if (userStore.role === 'teacher') {
          next('/appointments')
        } else {
          next('/')
        }
        return
      }
    }

    // 特殊处理管理员路由
    if (to.path.startsWith('/admin')) {
      if (userStore.role !== 'admin') {
        ElMessage.error('权限不足，仅管理员可访问')
        next('/login')
        return
      }
    }

    // 如果已登录用户访问登录页，重定向到对应角色首页
    if (to.path === '/login' || to.path === '/') {
      if (userStore.role === 'admin') {
        next('/admin')
      } else if (userStore.role === 'teacher') {
        next('/appointments')
      } else {
        next('/teachers')
      }
      return
    }
  }

  next()
})

export default router
