<template>
  <div class="appointments-container">
    <el-card>
      <template #header>
        <span>我的预约</span>
      </template>
      <el-table :data="appointments" style="width: 100%">
        <el-table-column prop="teacher_name" label="教师姓名" width="120" />
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

const appointments = ref([])

const fetchAppointments = async () => {
  try {
    // 假设后端接口为 /appointments/my/
    const res = await api.get('/appointments/my/')
    appointments.value = res.data || res
  } catch (e) {
    ElMessage.error('获取预约信息失败')
  }
}

onMounted(fetchAppointments)
</script>

<style scoped>
.appointments-container {
  padding: 40px;
}
</style>