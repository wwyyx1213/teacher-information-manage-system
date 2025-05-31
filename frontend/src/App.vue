<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import { useUserStore } from './stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<template>
  <el-container class="layout-container">
    <el-header>
      <el-menu
        :router="true"
        mode="horizontal"
        class="nav-menu"
      >
        <el-menu-item index="/">教师信息管理系统</el-menu-item>
        <el-menu-item index="/teachers">教师列表</el-menu-item>
        <el-menu-item index="/search">搜索</el-menu-item>
        <el-menu-item index="/recommendations">推荐教师</el-menu-item>
        <div class="flex-grow" />
        <template v-if="!userStore.isLoggedIn">
          <el-menu-item index="/login">登录</el-menu-item>
          <el-menu-item index="/register">注册</el-menu-item>
        </template>
        <template v-else>
          <el-menu-item index="/appointments">我的预约</el-menu-item>
          <el-menu-item index="/profile">个人中心</el-menu-item>
          <el-menu-item @click="handleLogout">退出</el-menu-item>
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
  display: flex; /* 设置为flex容器 */
  flex-direction: column; /* 子元素垂直排列 */
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
  flex-shrink: 0; /* 头部不缩小 */
}

/* 导航菜单样式 */
.nav-menu {
  display: flex;
  align-items: center;
  height: 60px;
}

.flex-grow {
  flex-grow: 1;
}

/* 主内容区域样式 */
.el-main {
  padding: 80px 0 20px;
  min-height: calc(100vh - 60px);
  background-color: #f5f7fa;
  box-sizing: border-box;
  flex-grow: 1;
  overflow-y: auto;
  width: 1345px; /* 确保宽度100% */
  flex-basis: auto; /* 明确设置 flex-basis */
}

/* 响应式布局 */
@media (max-width: 768px) {
  .el-main {
    padding: 70px 0 10px;
  }
}
</style>
