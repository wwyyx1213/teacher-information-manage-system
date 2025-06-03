<template>
  <div class="teacher-appointments">
    <div class="page-header">
      <h1>预约管理</h1>
    </div>
    <el-card class="appointment-list" v-loading="loading">
      <el-table :data="appointments" style="width: 100%">
        <el-table-column prop="student.username" label="学生姓名" />
        <el-table-column prop="time_slot" label="预约时间">
          <template #default="{ row }">
            {{ formatDateTime(row.time_slot) }} {{ row.time_range }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remarks" label="咨询事项" show-overflow-tooltip />
        <el-table-column label="操作" width="220">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending'"
              type="success"
              link
              @click="handleAccept(row)"
            >
              接受
            </el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="danger"
              link
              @click="handleReject(row)"
            >
              拒绝
            </el-button>
            <el-button
              type="primary"
              link
              @click="viewStudentDetail(row.student.id)"
            >
              查看学生
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const appointments = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 获取预约列表
const fetchAppointments = async () => {
  try {
    loading.value = true
    const response = await api.get('/appointments/')
    console.log('预约列表响应:', response)  // 添加调试日志
    appointments.value = response.results
    total.value = response.count
  } catch (error) {
    console.error('获取预约列表错误:', error)  // 添加调试日志
    ElMessage.error('获取预约列表失败：' + (error.response?.data?.message || error.message))
  } finally {
    loading.value = false
  }
}

// 格式化日期时间
const formatDateTime = (datetime) => {
  const date = new Date(datetime)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }).replace(/\//g, '-')
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    accepted: 'success',
    rejected: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    pending: '待确认',
    accepted: '已接受',
    rejected: '已拒绝'
  }
  return texts[status] || status
}

// 接受预约
const handleAccept = async (appointment) => {
  try {
    await api.patch(`/appointments/${appointment.id}/`, { status: 'accepted' })
    ElMessage.success('已接受预约')
    fetchAppointments()
  } catch (error) {
    ElMessage.error('操作失败：' + (error.response?.data?.message || error.message))
  }
}

// 拒绝预约
const handleReject = async (appointment) => {
  try {
    await ElMessageBox.confirm(
      '确定要拒绝该预约吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await api.patch(`/appointments/${appointment.id}/`, { status: 'rejected' })
    ElMessage.success('已拒绝预约')
    fetchAppointments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败：' + (error.response?.data?.message || error.message))
    }
  }
}

// 查看学生详情
const viewStudentDetail = (studentId) => {
  // 可跳转到学生详情页，若有实现
  // router.push(`/students/${studentId}`)
}

// 分页
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchAppointments()
}
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchAppointments()
}

onMounted(() => {
  fetchAppointments()
})
</script>

<style scoped>
.teacher-appointments {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
.page-header {
  margin-bottom: 20px;
  text-align: center;
}
.page-header h1 {
  margin: 0;
  color: #303133;
}
.appointment-list {
  margin-bottom: 20px;
}
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style> 