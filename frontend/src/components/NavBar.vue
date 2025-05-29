<template>
  <el-menu mode="horizontal" :router="true" class="nav-bar">
    <el-menu-item index="/">首页</el-menu-item>
    <el-menu-item index="/teachers">教师列表</el-menu-item>
    <el-menu-item v-if="!userStore.token" index="/login">登录</el-menu-item>
    <el-sub-menu v-else>
      <template #title>个人中心</template>
      <el-menu-item @click="logout">退出登录</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
const userStore = useUserStore()
const router = useRouter()
const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.nav-bar {
  margin-bottom: 20px;
}
</style>