<template>
  <div class="appointments-container">
    <el-card>
      <template #header>
        <span>我的预约（教师）</span>
      </template>
      <el-button type="primary" @click="goToProfile" style="margin-bottom: 20px;">
        返回个人信息
      </el-button>
      <el-table :data="appointments" style="width: 100%">
        <el-table-column prop="student_name" label="学生姓名" width="120" />
        <el-table-column prop="date" label="预约日期" width="160" />
        <el-table-column prop="time" label="时间段" width="120" />
        <el-table-column prop="status" label="状态" width="100" />
        <el-table-column prop="remarks" label="备注" />
      </el-table>
      <el-empty v-if="appointments.length === 0" description="暂无预约信息" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const appointments = ref([])

const fetchAppointments = async () => {
  try {
    // 假设后端接口为 /appointments/teacher/
    const res = await api.get('/appointments/teacher/')
    appointments.value = res.data || res
  } catch (e) {
    ElMessage.error('获取预约信息失败')
  }
}

const goToProfile = () => {
  // 跳转到当前教师的个人信息页
  const teacherId = userStore.user?.id
  if (teacherId) {
    router.push(`/teacher/${teacherId}`)
  } else {
    // 可选：提示未获取到教师ID
  }
}

onMounted(fetchAppointments)
</script>

<style scoped>
.appointments-container {
  padding: 40px;
}
</style>