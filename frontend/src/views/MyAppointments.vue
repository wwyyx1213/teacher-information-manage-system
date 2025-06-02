<template>
  <div class="my-appointments">
    <h2>我的预约</h2>
    
    <el-tabs v-model="activeTab">
      <el-tab-pane label="待处理预约" name="pending">
        <el-table :data="pendingAppointments" style="width: 100%">
          <el-table-column prop="teacher" label="教师姓名" />
          <el-table-column prop="time_slot" label="预约时间" />
          <el-table-column prop="remarks" label="备注" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag type="warning">待处理</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      
      <el-tab-pane label="已接受预约" name="accepted">
        <el-table :data="acceptedAppointments" style="width: 100%">
          <el-table-column prop="teacher" label="教师姓名" />
          <el-table-column prop="time_slot" label="预约时间" />
          <el-table-column prop="remarks" label="备注" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag type="success">已接受</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import api from '../api'

const userStore = useUserStore()
const activeTab = ref('pending')
const pendingAppointments = ref([])
const acceptedAppointments = ref([])

const fetchAppointments = async () => {
  try {
    const response = await api.get('/appointments/')
    pendingAppointments.value = response.filter(app => app.status === 'pending')
    acceptedAppointments.value = response.filter(app => app.status === 'accepted')
  } catch (error) {
    ElMessage.error('获取预约信息失败')
  }
}

onMounted(() => {
  fetchAppointments()
})
</script>

<style scoped>
.my-appointments {
  max-width: 1000px;
  margin: 20px auto;
  padding: 0 20px;
}

h2 {
  margin-bottom: 20px;
}

.el-tabs {
  margin-top: 20px;
}
</style> 