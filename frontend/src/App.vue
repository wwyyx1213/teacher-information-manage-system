<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import { useUserStore } from './stores/user'
import { useRouter } from 'vue-router'
import { Avatar } from '@element-plus/icons-vue'
import { computed, onMounted } from 'vue'

const userStore = useUserStore()
const router = useRouter()

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

// 计算用户名的首字母作为头像显示
const userInitial = computed(() => {
  if (userStore.user && userStore.user.username) {
    return userStore.user.username.charAt(0).toUpperCase()
  }
  return '?'
})

// 检查并处理目标路由
onMounted(() => {
  const targetRoute = localStorage.getItem('targetRoute')
  if (targetRoute) {
    localStorage.removeItem('targetRoute')
    router.push(targetRoute)
  }
})

</script>

<template>
  <el-container class="layout-container">
    <el-header>
      <el-menu
        :router="true"
        mode="horizontal"
        class="nav-menu"
        :collapse="false"
      >
        <el-menu-item index="/">教师信息管理系统</el-menu-item>
        <el-menu-item index="/teachers">教师列表</el-menu-item>
        <el-menu-item index="/recommendations">推荐教师</el-menu-item>
        <div class="flex-grow" />
        
        <!-- 未登录用户显示 -->
        <template v-if="!userStore.isLoggedIn">
          <el-menu-item index="/login">登录</el-menu-item>
          <el-menu-item index="/register">注册</el-menu-item>
        </template>
        
        <!-- 已登录用户显示 -->
        <template v-else>
          <el-menu-item index="/my-appointments" v-if="userStore.isStudent">我的预约</el-menu-item>
          <el-menu-item index="/appointments" v-if="userStore.isTeacher">预约管理</el-menu-item>
          <el-menu-item index="/admin" v-if="userStore.isAdmin">用户管理</el-menu-item>
          <el-menu-item index="/profile">个人中心</el-menu-item>
          <el-menu-item @click="handleLogout">退出</el-menu-item>
          <el-menu-item class="avatar-wrapper">
            <el-avatar :size="40" class="avatar">
              {{ userInitial }}
            </el-avatar>
            <span class="username">{{ userStore.user?.username }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-header>

    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<style>
/* 全局样式 */
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

/* 布局容器样式 */
.layout-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* 头部样式 */
.el-header {
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: #fff;
  flex-shrink: 0;
  overflow-x: auto;
  overflow-y: hidden;
}

.el-header::-webkit-scrollbar {
  display: none;
}

/* 导航菜单样式 */
.nav-menu {
  display: flex;
  align-items: center;
  height: 60px;
  border-bottom: none;
  width: auto;
  min-width: 100%;
}

.nav-menu .el-menu-item {
  height: 60px;
  line-height: 60px;
  white-space: nowrap;
}

.flex-grow {
  flex-grow: 1;
  min-width: 20px;
}

.avatar-wrapper {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 10px;
  height: 60px;
  transition: background-color 0.3s;
}

.avatar-wrapper:hover {
  background-color: #f5f7fa;
}

.avatar {
  background-color: #a2b0be;
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
}

.username {
  font-size: 14px;
  color: #606266;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 主内容区域样式 */
.el-main {
  padding: 80px 0 20px;
  min-height: calc(100vh - 60px);
  background-color: #f5f7fa;
  box-sizing: border-box;
  flex-grow: 1;
  overflow-y: auto;
  width: 1345px;
  margin: 0 auto;
  flex-basis: auto;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .el-main {
    padding: 70px 0 10px;
    width: 100%;
  }
}
</style>