<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    router
  >
    <el-menu-item index="/">首页</el-menu-item>
    <el-menu-item index="/search">搜索</el-menu-item>
    <el-menu-item index="/recommendations">推荐</el-menu-item>
    <el-menu-item index="/appointments">预约</el-menu-item>
    <div class="flex-grow" />
    <template v-if="!userStore.isLoggedIn">
      <el-menu-item index="/login">登录</el-menu-item>
      <el-menu-item index="/register">注册</el-menu-item>
    </template>
    <template v-else>
      <div class="user-info">
        <el-dropdown trigger="click" @command="handleCommand">
          <div class="avatar-wrapper">
            <el-avatar :size="40" class="avatar" :style="{ backgroundColor: getAvatarColor() }">
              {{ userInitial }}
            </el-avatar>
            <span class="username">{{ userStore.user?.username }}</span>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="appointments">预约管理</el-dropdown-item>
              <el-dropdown-item v-if="userStore.isTeacher" command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </template>
  </el-menu>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const activeIndex = ref('/')

// 计算用户名的首字母作为头像显示
const userInitial = computed(() => {
  console.log('Current user:', userStore.user) // 添加调试日志
  if (userStore.user && userStore.user.username) {
    return userStore.user.username.charAt(0).toUpperCase()
  }
  return '?'
})

// 生成头像背景色
const getAvatarColor = () => {
  const colors = ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399']
  const index = Math.floor(Math.random() * colors.length)
  return colors[index]
}

// 处理下拉菜单命令
const handleCommand = async (command) => {
  switch (command) {
    case 'logout':
      try {
        await userStore.logout()
        ElMessage.success('已退出登录')
        router.push('/login')
      } catch (error) {
        ElMessage.error('退出登录失败')
      }
      break
    case 'profile':
      router.push('/profile')
      break
    case 'appointments':
      router.push('/appointments')
      break
  }
}

// 组件挂载时检查用户状态
onMounted(async () => {
  console.log('Navbar mounted, checking auth...') // 添加调试日志
  if (userStore.token) {
    await userStore.checkAuth()
  }
})
</script>

<style scoped>
.el-menu-demo {
  display: flex;
  padding: 0 20px;
  align-items: center;
}

.flex-grow {
  flex-grow: 1;
}

.user-info {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.avatar-wrapper {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 10px;
}

.avatar {
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
}

.username {
  color: #606266;
  font-size: 14px;
  margin-left: 8px;
}

.el-dropdown {
  display: flex;
  align-items: center;
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  padding: 8px 16px;
}

:deep(.el-dropdown-menu__item.is-divided) {
  border-top: 1px solid #ebeef5;
  margin-top: 4px;
}
</style> 