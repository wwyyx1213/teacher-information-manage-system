<template>
  <div class="home">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="logo">
        <img src="../assets/logo.png" alt="Logo" />
        <span>教师信息管理系统</span>
      </div>
      <div class="nav-links">
        <el-menu mode="horizontal" :router="true" :default-active="activeIndex">
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/teachers">教师列表</el-menu-item>
          <template v-if="userStore.isLoggedIn">
            <el-menu-item v-if="userStore.isStudent" index="/my-appointments">
              我的预约
            </el-menu-item>
            <el-menu-item v-if="userStore.isTeacher" index="/appointments">
              预约管理
            </el-menu-item>
            <el-menu-item index="/profile">个人中心</el-menu-item>
          </template>
        </el-menu>
      </div>
    </el-header>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 搜索区域 -->
      <div class="search-section">
        <teacher-search />
      </div>

      <!-- 推荐教师区域 -->
      <div class="recommended-section">
        <div class="section-header">
          <h2>推荐教师</h2>
          <el-button type="primary" link @click="$router.push('/teachers')">
            查看更多
          </el-button>
        </div>
        <el-row :gutter="20" v-loading="loading">
          <el-col :span="6" v-for="teacher in recommendedTeachers" :key="teacher.id">
            <el-card class="teacher-card" :body-style="{ padding: '0px' }">
              <div class="teacher-avatar">
                <el-avatar :size="100" :src="teacher.avatar_url || '/default-avatar.png'" />
              </div>
              <div class="teacher-info">
                <h3>{{ teacher.name }}</h3>
                <p class="department">{{ teacher.department }}</p>
                <p class="title">{{ teacher.title }}</p>
                <p class="research">{{ teacher.research_areas }}</p>
                <el-button type="primary" link @click="viewTeacherDetail(teacher.id)">
                  查看详情
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import TeacherSearch from '../components/TeacherSearch.vue'
import api from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const recommendedTeachers = ref([])
const activeIndex = ref('/')

const fetchRecommendedTeachers = async () => {
  try {
    loading.value = true
    const response = await api.get('/recommendations/')
    recommendedTeachers.value = response.results
  } catch (error) {
    ElMessage.error('获取推荐教师失败：' + (error.response?.data?.message || error.message))
  } finally {
    loading.value = false
  }
}

const viewTeacherDetail = (teacherId) => {
  router.push(`/teachers/${teacherId}`)
}

onMounted(() => {
  fetchRecommendedTeachers()
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo img {
  height: 40px;
}

.logo span {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.main-content {
  padding-top: 80px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-section {
  margin-bottom: 40px;
}

.recommended-section {
  padding: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  color: #303133;
}

.teacher-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.teacher-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.teacher-avatar {
  padding: 20px;
  text-align: center;
  background-color: #f5f7fa;
}

.teacher-info {
  padding: 20px;
  text-align: center;
}

.teacher-info h3 {
  margin: 0 0 10px;
  color: #303133;
}

.department, .title, .research {
  margin: 5px 0;
  color: #606266;
  font-size: 14px;
}

.research {
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
</style> 