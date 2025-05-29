<template>
  <div class="schedule-view">
    <el-card>
      <h2>导师日程</h2>
      <el-table :data="scheduleList" style="width: 100%">
        <el-table-column prop="date" label="日期" width="150" />
        <el-table-column prop="time" label="时间" width="120" />
        <el-table-column prop="event" label="事项" />
      </el-table>
      <el-button type="primary" @click="syncSchedule" style="margin-top: 20px;">
        同步日程
      </el-button>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

const route = useRoute()
const scheduleList = ref([])

const loadSchedule = async () => {
  try {
    const res = await api.get(`/teachers/${route.params.id}/schedule/`)
    scheduleList.value = res.data
  } catch (e) {
    ElMessage.error('获取日程失败')
  }
}

const syncSchedule = async () => {
  try {
    await api.post(`/teachers/${route.params.id}/schedule/sync/`)
    ElMessage.success('同步成功')
    loadSchedule()
  } catch (e) {
    ElMessage.error('同步失败')
  }
}

onMounted(() => {
  loadSchedule()
})
</script>

<style scoped>
.schedule-view {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.el-card {
  width: 600px;
}
</style>