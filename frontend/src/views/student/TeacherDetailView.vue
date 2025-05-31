<template>
  <div class="teacher-detail-container">
    <el-card>
      <template #header>
        <div class="header-flex">
          <span>教师详情</span>
          <el-button type="primary" @click="goToAppointment" style="float:right;">预约</el-button>
        </div>
      </template>
      <!-- 这里可以继续补充教师详情内容 -->
      <div class="teacher-info">
        <el-avatar :src="teacherInfo.avatar" size="large" />
        <div class="info-text">
          <h2>{{ teacherInfo.name }}</h2>
          <p>{{ teacherInfo.title }} | {{ teacherInfo.department }}</p>
          <p>{{ teacherInfo.bio }}</p>
        </div>
      </div>
      <!-- 你可以继续补充tabs等内容 -->
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import teacherApi from '../../api/teacher'

const route = useRoute()
const router = useRouter()
const teacherId = route.params.id

const teacherInfo = ref({
  name: '',
  department: '',
  title: '',
  avatar: '',
  bio: '',
  research_areas: '',
  contact: '',
  education: '',
  work_experience: ''
})

const fetchTeacherDetail = async () => {
  try {
    const response = await teacherApi.getTeacherDetail(teacherId)
    teacherInfo.value = response
  } catch (error) {
    ElMessage.error('获取教师信息失败')
  }
}

const goToAppointment = () => {
  router.push(`/teachers/${teacherId}/appointments`)
}

onMounted(() => {
  fetchTeacherDetail()
})
</script>

<style scoped>
.teacher-detail-container {
  padding: 40px;
}
.header-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.teacher-info {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-top: 20px;
}
.info-text h2 {
  margin: 0 0 8px 0;
}
.info-text p {
  margin: 0;
  color: #606266;
}
</style>