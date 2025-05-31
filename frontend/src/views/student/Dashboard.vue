<template>
  <div class="dashboard-container">
    <el-container>
      <el-header>
        <div class="header-content">
          <h2>学生仪表板</h2>
          <el-button type="danger" @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>个人信息</span>
                </div>
              </template>
              <div class="user-info">
                <p><strong>用户名：</strong>{{ user.username }}</p>
                <p><strong>邮箱：</strong>{{ user.email }}</p>
                <p><strong>角色：</strong>学生</p>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="16">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>快捷操作</span>
                </div>
              </template>
              <el-row :gutter="20">
                <el-col :span="8">
                  <el-button type="primary" @click="$router.push('/search')">搜索教师</el-button>
                </el-col>
                <el-col :span="8">
                  <el-button type="success" @click="$router.push('/recommendations')">查看推荐</el-button>
                </el-col>
                <el-col :span="8">
                  <el-button type="warning" @click="$router.push('/appointments')">我的预约</el-button>
                </el-col>
              </el-row>
            </el-card>
          </el-col>
        </el-row>

        <el-row :gutter="20" class="mt-20">
          <el-col :span="16">
            <el-card class="appointments-card">
              <template #header>
                <div class="card-header">
                  <h3>我的预约</h3>
                  <el-button type="primary" @click="showAppointmentDialog">新建预约</el-button>
                </div>
              </template>
              
              <el-table :data="appointments" v-loading="loading">
                <el-table-column prop="teacher_name" label="教师姓名" />
                <el-table-column prop="appointment_time" label="预约时间" />
                <el-table-column prop="status" label="状态">
                  <template #default="{ row }">
                    <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作">
                  <template #default="{ row }">
                    <el-button 
                      v-if="row.status === 'pending'"
                      type="danger" 
                      size="small" 
                      @click="cancelAppointment(row.id)"
                    >
                      取消预约
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card class="recommendations-card">
              <template #header>
                <div class="card-header">
                  <h3>推荐教师</h3>
                </div>
              </template>
              
              <div v-loading="recommendationsLoading">
                <div v-for="teacher in recommendedTeachers" :key="teacher.id" class="teacher-item">
                  <h4>{{ teacher.name }}</h4>
                  <p>{{ teacher.department }}</p>
                  <p>{{ teacher.research_areas }}</p>
                  <el-button type="primary" size="small" @click="showTeacherDetail(teacher.id)">
                    查看详情
                  </el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>

    <!-- 新建预约对话框 -->
    <el-dialog
      v-model="appointmentDialogVisible"
      title="新建预约"
      width="500px"
    >
      <el-form :model="appointmentForm" :rules="appointmentRules" ref="appointmentFormRef" label-width="100px">
        <el-form-item label="选择教师" prop="teacher_id">
          <el-select v-model="appointmentForm.teacher_id" placeholder="请选择教师">
            <el-option
              v-for="teacher in teachers"
              :key="teacher.id"
              :label="teacher.name"
              :value="teacher.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="预约时间" prop="appointment_time">
          <el-date-picker
            v-model="appointmentForm.appointment_time"
            type="datetime"
            placeholder="选择预约时间"
            :disabled-date="disabledDate"
            :disabled-hours="disabledHours"
          />
        </el-form-item>
        
        <el-form-item label="预约说明" prop="description">
          <el-input
            v-model="appointmentForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入预约说明"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="appointmentDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAppointment" :loading="submitting">
            确认预约
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import api from '../../api'

export default {
  name: 'StudentDashboard',
  setup() {
    const router = useRouter()
    const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))
    const loading = ref(false)
    const recommendationsLoading = ref(false)
    const submitting = ref(false)
    const appointmentDialogVisible = ref(false)
    const appointmentFormRef = ref(null)
    
    const appointments = ref([])
    const recommendedTeachers = ref([])
    const teachers = ref([])
    
    const appointmentForm = ref({
      teacher_id: '',
      appointment_time: '',
      description: ''
    })
    
    const appointmentRules = {
      teacher_id: [
        { required: true, message: '请选择教师', trigger: 'change' }
      ],
      appointment_time: [
        { required: true, message: '请选择预约时间', trigger: 'change' }
      ],
      description: [
        { required: true, message: '请输入预约说明', trigger: 'blur' }
      ]
    }
    
    const handleLogout = async () => {
      try {
        await axios.post('http://localhost:8000/api/logout/')
        localStorage.removeItem('user')
        ElMessage.success('已成功退出登录')
        router.push('/login')
      } catch (error) {
        ElMessage.error('退出登录失败')
      }
    }
    
    const fetchAppointments = async () => {
      loading.value = true
      try {
        const response = await api.get('/appointments/')
        appointments.value = response.data
      } catch (error) {
        ElMessage.error('获取预约列表失败')
      } finally {
        loading.value = false
      }
    }
    
    const fetchRecommendedTeachers = async () => {
      recommendationsLoading.value = true
      try {
        const response = await api.get('/recommendations/')
        recommendedTeachers.value = response.data
      } catch (error) {
        ElMessage.error('获取推荐教师失败')
      } finally {
        recommendationsLoading.value = false
      }
    }
    
    const fetchTeachers = async () => {
      try {
        const response = await api.get('/teachers/')
        teachers.value = response.data
      } catch (error) {
        ElMessage.error('获取教师列表失败')
      }
    }
    
    const showAppointmentDialog = () => {
      appointmentDialogVisible.value = true
      fetchTeachers()
    }
    
    const submitAppointment = async () => {
      if (!appointmentFormRef.value) return
      
      await appointmentFormRef.value.validate(async (valid) => {
        if (valid) {
          submitting.value = true
          try {
            await api.post('/appointments/', appointmentForm.value)
            ElMessage.success('预约成功')
            appointmentDialogVisible.value = false
            fetchAppointments()
          } catch (error) {
            ElMessage.error(error.response?.data?.message || '预约失败')
          } finally {
            submitting.value = false
          }
        }
      })
    }
    
    const cancelAppointment = async (id) => {
      try {
        await ElMessageBox.confirm('确定要取消这个预约吗？', '提示', {
          type: 'warning'
        })
        
        await api.delete(`/appointments/${id}/`)
        ElMessage.success('取消预约成功')
        fetchAppointments()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('取消预约失败')
        }
      }
    }
    
    const showTeacherDetail = (teacherId) => {
      router.push(`/teacher/${teacherId}`)
    }
    
    const getStatusType = (status) => {
      const types = {
        pending: 'warning',
        accepted: 'success',
        rejected: 'danger',
        cancelled: 'info'
      }
      return types[status] || 'info'
    }
    
    const getStatusText = (status) => {
      const texts = {
        pending: '待确认',
        accepted: '已接受',
        rejected: '已拒绝',
        cancelled: '已取消'
      }
      return texts[status] || status
    }
    
    const disabledDate = (time) => {
      return time.getTime() < Date.now() - 8.64e7
    }
    
    const disabledHours = () => {
      const hours = []
      for (let i = 0; i < 24; i++) {
        if (i < 9 || i > 17) {
          hours.push(i)
        }
      }
      return hours
    }
    
    onMounted(() => {
      if (!user.value.id) {
        router.push('/login')
      }
      fetchAppointments()
      fetchRecommendedTeachers()
    })

    return {
      user,
      loading,
      recommendationsLoading,
      submitting,
      appointmentDialogVisible,
      appointmentForm,
      appointmentFormRef,
      appointmentRules,
      appointments,
      recommendedTeachers,
      teachers,
      showAppointmentDialog,
      submitAppointment,
      cancelAppointment,
      showTeacherDetail,
      getStatusType,
      getStatusText,
      disabledDate,
      disabledHours,
      handleLogout
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.el-header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.el-main {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  line-height: 2;
}

.el-button {
  width: 100%;
  margin-bottom: 10px;
}

.teacher-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.teacher-item:last-child {
  border-bottom: none;
}

.teacher-item h4 {
  margin: 0 0 5px 0;
}

.teacher-item p {
  margin: 5px 0;
  color: #666;
}
</style> 