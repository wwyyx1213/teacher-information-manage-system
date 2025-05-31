<template>
  <div class="dashboard-container">
    <el-container>
      <el-header>
        <div class="header-content">
          <h2>教师仪表板</h2>
          <el-button type="danger" @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-card class="appointments-card">
              <template #header>
                <div class="card-header">
                  <h3>预约管理</h3>
                </div>
              </template>
              
              <el-table :data="appointments" v-loading="loading">
                <el-table-column prop="student_name" label="学生姓名" />
                <el-table-column prop="appointment_time" label="预约时间" />
                <el-table-column prop="description" label="预约说明" show-overflow-tooltip />
                <el-table-column prop="status" label="状态">
                  <template #default="{ row }">
                    <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作">
                  <template #default="{ row }">
                    <el-button 
                      v-if="row.status === 'pending'"
                      type="success" 
                      size="small" 
                      @click="handleAppointment(row.id, 'accepted')"
                    >
                      接受
                    </el-button>
                    <el-button 
                      v-if="row.status === 'pending'"
                      type="danger" 
                      size="small" 
                      @click="handleAppointment(row.id, 'rejected')"
                    >
                      拒绝
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card class="profile-card">
              <template #header>
                <div class="card-header">
                  <h3>个人信息</h3>
                  <el-button type="primary" size="small" @click="showEditDialog">编辑</el-button>
                </div>
              </template>
              
              <div v-loading="profileLoading">
                <div class="profile-item">
                  <label>姓名：</label>
                  <span>{{ profile.name }}</span>
                </div>
                <div class="profile-item">
                  <label>部门：</label>
                  <span>{{ profile.department }}</span>
                </div>
                <div class="profile-item">
                  <label>职称：</label>
                  <span>{{ profile.title }}</span>
                </div>
                <div class="profile-item">
                  <label>研究方向：</label>
                  <span>{{ profile.research_areas }}</span>
                </div>
                <div class="profile-item">
                  <label>邮箱：</label>
                  <span>{{ profile.email }}</span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>

    <!-- 编辑个人信息对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑个人信息"
      width="500px"
    >
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="editForm.name" />
        </el-form-item>
        
        <el-form-item label="部门" prop="department">
          <el-input v-model="editForm.department" />
        </el-form-item>
        
        <el-form-item label="职称" prop="title">
          <el-input v-model="editForm.title" />
        </el-form-item>
        
        <el-form-item label="研究方向" prop="research_areas">
          <el-input
            v-model="editForm.research_areas"
            type="textarea"
            rows="3"
            placeholder="请输入研究方向，多个方向用逗号分隔"
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEdit" :loading="submitting">
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../../api'

export default {
  name: 'TeacherDashboard',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const profileLoading = ref(false)
    const submitting = ref(false)
    const editDialogVisible = ref(false)
    const editFormRef = ref(null)
    
    const appointments = ref([])
    const profile = ref({})
    
    const editForm = reactive({
      name: '',
      department: '',
      title: '',
      research_areas: '',
      email: ''
    })
    
    const editRules = {
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' }
      ],
      department: [
        { required: true, message: '请输入部门', trigger: 'blur' }
      ],
      title: [
        { required: true, message: '请输入职称', trigger: 'blur' }
      ],
      research_areas: [
        { required: true, message: '请输入研究方向', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ]
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
    
    const fetchProfile = async () => {
      profileLoading.value = true
      try {
        const response = await api.get('/user/')
        profile.value = response.data
      } catch (error) {
        ElMessage.error('获取个人信息失败')
      } finally {
        profileLoading.value = false
      }
    }
    
    const showEditDialog = () => {
      Object.assign(editForm, profile.value)
      editDialogVisible.value = true
    }
    
    const submitEdit = async () => {
      if (!editFormRef.value) return
      
      await editFormRef.value.validate(async (valid) => {
        if (valid) {
          submitting.value = true
          try {
            await api.put('/user/', editForm)
            ElMessage.success('保存成功')
            editDialogVisible.value = false
            fetchProfile()
          } catch (error) {
            ElMessage.error(error.response?.data?.message || '保存失败')
          } finally {
            submitting.value = false
          }
        }
      })
    }
    
    const handleAppointment = async (id, status) => {
      try {
        await ElMessageBox.confirm(
          `确定要${status === 'accepted' ? '接受' : '拒绝'}这个预约吗？`,
          '提示',
          {
            type: 'warning'
          }
        )
        
        await api.put(`/appointments/${id}/`, { status })
        ElMessage.success(`${status === 'accepted' ? '接受' : '拒绝'}预约成功`)
        fetchAppointments()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('操作失败')
        }
      }
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
    
    const handleLogout = async () => {
      try {
        await api.post('/logout/')
        localStorage.removeItem('user')
        ElMessage.success('已成功退出登录')
        router.push('/login')
      } catch (error) {
        ElMessage.error('退出登录失败')
      }
    }
    
    onMounted(() => {
      fetchAppointments()
      fetchProfile()
    })
    
    return {
      loading,
      profileLoading,
      submitting,
      appointments,
      profile,
      editDialogVisible,
      editForm,
      editFormRef,
      editRules,
      showEditDialog,
      submitEdit,
      handleAppointment,
      getStatusType,
      getStatusText,
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

.profile-item {
  margin-bottom: 15px;
}

.profile-item label {
  font-weight: bold;
  margin-right: 10px;
  color: #666;
}

.el-button {
  width: 100%;
  margin-bottom: 10px;
}
</style> 