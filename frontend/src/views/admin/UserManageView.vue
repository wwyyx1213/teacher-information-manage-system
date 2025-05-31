<template>
  <div class="user-manage-container">
    <el-card>
      <template #header>
        <div class="header-flex">
          <span>用户管理</span>
          <el-button type="primary" @click="showAddDialog = true">新增用户</el-button>
        </div>
      </template>
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索用户名/姓名/角色"
          clearable
          @input="filterUsers"
          style="width: 300px;"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      <el-table :data="filteredUsers" style="width: 100%; margin-top: 20px;">
        <el-table-column prop="username" label="用户名" width="140" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="role" label="角色" width="100" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column label="操作" width="160">
          <template #default="scope">
            <el-button size="small" type="danger" @click="deleteUser(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="filteredUsers.length === 0" description="暂无用户" />
    </el-card>

    <!-- 新增用户对话框 -->
    <el-dialog v-model="showAddDialog" title="新增用户" width="400px">
      <el-form :model="addForm" ref="addFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username" :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
          <el-input v-model="addForm.username" />
        </el-form-item>
        <el-form-item label="姓名" prop="name" :rules="[{ required: true, message: '请输入姓名', trigger: 'blur' }]">
          <el-input v-model="addForm.name" />
        </el-form-item>
        <el-form-item label="角色" prop="role" :rules="[{ required: true, message: '请选择角色', trigger: 'change' }]">
          <el-select v-model="addForm.role" placeholder="请选择角色">
            <el-option label="学生" value="student" />
            <el-option label="教师" value="teacher" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="addForm.email" />
        </el-form-item>
        <el-form-item label="密码" prop="password" :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
          <el-input v-model="addForm.password" type="password" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="addUser">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import api from '@/api'

const users = ref([])
const filteredUsers = ref([])
const searchKeyword = ref('')
const showAddDialog = ref(false)
const addForm = ref({
  username: '',
  name: '',
  role: '',
  email: '',
  password: ''
})
const addFormRef = ref(null)

// 获取所有用户
const fetchUsers = async () => {
  try {
    const res = await api.get('/admin/users/')
    users.value = res.data || res
    filteredUsers.value = users.value
  } catch (e) {
    ElMessage.error('获取用户列表失败')
  }
}

// 搜索过滤
const filterUsers = () => {
  const keyword = searchKeyword.value.trim().toLowerCase()
  if (!keyword) {
    filteredUsers.value = users.value
    return
  }
  filteredUsers.value = users.value.filter(user =>
    (user.username && user.username.toLowerCase().includes(keyword)) ||
    (user.name && user.name.toLowerCase().includes(keyword)) ||
    (user.role && user.role.toLowerCase().includes(keyword))
  )
}

// 删除用户
const deleteUser = (user) => {
  ElMessageBox.confirm(`确定要删除用户 ${user.username} 吗？`, '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await api.delete(`/admin/users/${user.id}/`)
      ElMessage.success('删除成功')
      fetchUsers()
    } catch (e) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 新增用户
const addUser = () => {
  addFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await api.post('/admin/users/', addForm.value)
        ElMessage.success('新增用户成功')
        showAddDialog.value = false
        Object.keys(addForm.value).forEach(k => addForm.value[k] = '')
        fetchUsers()
      } catch (e) {
        ElMessage.error('新增用户失败')
      }
    }
  })
}

onMounted(fetchUsers)
</script>

<style scoped>
.user-manage-container {
  padding: 40px;
}
.header-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.search-bar {
  margin: 20px 0 0 0;
  display: flex;
  justify-content: flex-start;
}
</style>