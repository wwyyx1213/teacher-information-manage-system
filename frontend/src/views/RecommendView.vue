<template>
  <div class="recommend-view">
    <el-card class="recommend-header">
      <h2>为你推荐的教师</h2>
      <p>系统根据你的专业、兴趣或教师活跃度智能推荐</p>
    </el-card>
    <el-row :gutter="20" v-loading="loading">
      <el-col :span="6" v-for="teacher in recommendedTeachers" :key="teacher.id">
        <el-card class="teacher-card" shadow="hover" @click="goToTeacherDetail(teacher.id)">
          <div class="teacher-card-header">
            <el-avatar :size="80" :src="teacher.avatar_url || '/default-avatar.png'" />
            <div class="teacher-info">
              <h3>{{ teacher.name }}</h3>
              <p>{{ teacher.department }}</p>
              <p>{{ teacher.title }}</p>
            </div>
          </div>
          <div class="recommend-reason">{{ teacher.recommend_reason }}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-empty v-if="!recommendedTeachers.length && !loading" description="暂无推荐教师" />
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const recommendedTeachers = ref([])
const loading = ref(false)

const fetchRecommendedTeachers = async () => {
  try {
    loading.value = true
    const res = await api.get('/recommendations/')
    recommendedTeachers.value = res.results || res
  } catch (e) {
    ElMessage.error('获取推荐教师失败')
  } finally {
    loading.value = false
  }
}
const goToTeacherDetail = (id) => {
  router.push(`/teachers/${id}`)
}
onMounted(() => {
  fetchRecommendedTeachers()
})
</script>
<style scoped>
.recommend-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
.recommend-header {
  margin-bottom: 20px;
  text-align: center;
}
.teacher-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.3s;
}
.teacher-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}
.teacher-card-header {
  display: flex;
  align-items: center;
  gap: 15px;
}
.teacher-info h3 {
  margin: 0 0 5px 0;
  font-size: 1.2em;
  color: #303133;
}
.teacher-info p {
  margin: 0;
  font-size: 0.95em;
  color: #606266;
}
.recommend-reason {
  margin-top: 10px;
  color: #409eff;
  font-size: 0.98em;
}
</style> 