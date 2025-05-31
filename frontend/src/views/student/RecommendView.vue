<template>
  <div class="recommend-container">
    <el-card class="recommended-teachers-card">
      <template #header>
        <div class="card-header">
          <span>推荐教师</span>
        </div>
      </template>
      <div class="recommended-teachers-list">
        <el-scrollbar>
          <div class="scrollbar-flex-content">
            <el-card
              v-for="teacher in recommendedTeachers"
              :key="teacher.id"
              class="teacher-card"
              shadow="hover"
              @click="goToTeacherDetail(teacher.id)"
            >
              <template #header>
                <div class="teacher-card-header">
                  <el-avatar :size="60" :src="teacher.avatar" />
                  <div class="teacher-info">
                    <h3>{{ teacher.name }}</h3>
                    <p>{{ teacher.major }}</p>
                  </div>
                </div>
              </template>
              <p>{{ teacher.reason }}</p>
            </el-card>
          </div>
        </el-scrollbar>
      </div>
      <el-empty v-if="recommendedTeachers.length === 0" description="暂无推荐教师" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

const router = useRouter()
const recommendedTeachers = ref([])

const fetchRecommendedTeachers = async () => {
  try {
    // 假设后端接口为 /teachers/recommendations/
    const res = await api.get('/teachers/recommendations/')
    recommendedTeachers.value = res.data || res // 视后端返回结构调整
  } catch (e) {
    ElMessage.error('获取推荐教师失败')
  }
}

const goToTeacherDetail = (teacherId) => {
  router.push(`/teachers/${teacherId}`)
}

onMounted(fetchRecommendedTeachers)
</script>

<style scoped>
.recommend-container {
  padding: 40px;
}
.recommended-teachers-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.card-header {
  display: flex;
  align-items: center;
  font-size: 1.2em;
  font-weight: bold;
  color: #303133;
}
.recommended-teachers-list {
  padding-bottom: 10px;
}
.scrollbar-flex-content {
  display: flex;
  gap: 20px;
}
.teacher-card {
  width: 300px;
  flex-shrink: 0;
  cursor: pointer;
  transition: transform 0.3s ease;
}
.teacher-card:hover {
  transform: translateY(-5px);
}
.teacher-card-header {
  display: flex;
  align-items: center;
}
.teacher-info {
  margin-left: 15px;
}
.teacher-info h3 {
  margin: 0 0 5px 0;
  font-size: 1.1em;
  color: #303133;
}
.teacher-info p {
  margin: 0;
  font-size: 0.9em;
  color: #606266;
}
.teacher-card .el-card__body {
  padding-top: 0;
  font-size: 0.9em;
  color: #606266;
}
</style>