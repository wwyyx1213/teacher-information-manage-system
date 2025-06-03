<template>
  <div class="my-appointments">
    <div class="page-header">
      <h1>我的预约</h1>
    </div>

    <el-card class="appointment-list" v-loading="loading">
      <el-table :data="appointments" style="width: 100%">
        <el-table-column prop="teacher.name" label="教师姓名" />
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
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending'"
              type="danger"
              link
              @click="handleCancel(row)"
            >
              取消预约
            </el-button>
            <el-button
              type="primary"
              link
              @click="viewTeacherDetail(row.teacher.id)"
            >
              查看教师
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
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
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    const response = await api.get('/appointments/', { params })
    appointments.value = response.results
    total.value = response.count
  } catch (error) {
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

// 处理取消预约
const handleCancel = async (appointment) => {
  try {
    await ElMessageBox.confirm(
      '确定要取消这个预约吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.delete(`/appointments/${appointment.id}/`)
    ElMessage.success('预约已取消')
    fetchAppointments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消预约失败：' + (error.response?.data?.message || error.message))
    }
  }
}

// 查看教师详情
const viewTeacherDetail = (teacherId) => {
  router.push(`/teachers/${teacherId}`)
}

// 处理分页
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
.my-appointments {
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