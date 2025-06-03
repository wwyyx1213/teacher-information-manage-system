<template>
    <div class="user-manage-view">
        <div class="page-header">
            <h1>用户管理</h1>
            <p class="subtitle">管理系统用户，包括学生和教师账号</p>
        </div>
        
        <el-card class="manage-card">
            <div class="action-bar">
                <el-button-group>
                    <el-button
                        type="primary"
                        @click="handleUpdateDatabase"
                        :loading="updatingDatabase"
                        class="action-btn"
                    >
                        <el-icon><Refresh /></el-icon>
                        更新数据库
                    </el-button>
                    <el-button
                        type="success"
                        @click="handleRefresh"
                        :loading="loading"
                        class="action-btn"
                    >
                        <el-icon><RefreshRight /></el-icon>
                        刷新列表
                    </el-button>
                </el-button-group>
            </div>

            <el-table 
                :data="users" 
                style="width: 100%" 
                v-loading="loading" 
                border 
                stripe
                :default-sort="{ prop: 'date_joined', order: 'descending' }"
            >
                <el-table-column prop="username" label="用户名" min-width="120" sortable />
                <el-table-column prop="email" label="邮箱" min-width="180" sortable />
                <el-table-column prop="role" label="角色" width="100" sortable>
                    <template #default="{ row }">
                        <el-tag :type="getRoleTagType(row.role)">
                            {{ formatRole(row.role) }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="is_active" label="状态" width="100" sortable>
                    <template #default="{ row }">
                        <el-tag :type="row.is_active ? 'success' : 'danger'">
                            {{ row.is_active ? '正常' : '禁用' }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="date_joined" label="注册时间" width="180" sortable>
                    <template #default="{ row }">
                        {{ formatDate(row.date_joined) }}
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="250" fixed="right">
                    <template #default="{ row }">
                        <el-button-group>
                            <el-button
                                v-if="row.role !== 'admin'"
                                :type="row.is_active ? 'warning' : 'success'"
                                size="small"
                                @click="handleToggleStatus(row)"
                                :loading="row.updating"
                                :title="row.is_active ? '禁用用户' : '启用用户'"
                            >
                                <el-icon>
                                    <component :is="row.is_active ? 'Lock' : 'Unlock'" />
                                </el-icon>
                                {{ row.is_active ? '禁用' : '启用' }}
                            </el-button>
                            <el-button
                                v-if="row.role !== 'admin'"
                                type="danger"
                                size="small"
                                @click="handleDelete(row)"
                                :loading="row.deleting"
                                title="删除用户"
                            >
                                <el-icon><Delete /></el-icon>
                                删除
                            </el-button>
                        </el-button-group>
                    </template>
                </el-table-column>
            </el-table>

            <div class="table-footer" v-if="users.length > 0">
                <span class="total-count">共 {{ users.length }} 个用户</span>
            </div>
        </el-card>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, RefreshRight, Lock, Unlock, Delete } from '@element-plus/icons-vue'
import api from '@/api'
import { formatDate } from '@/utils/format'
import { useRouter } from 'vue-router'

const users = ref([])
const loading = ref(false)
const updatingDatabase = ref(false)
const router = useRouter()

// 获取用户列表
const fetchUsers = async () => {
    loading.value = true
    try {
        const response = await api.get('/admin/users/')
        users.value = response.map(user => ({
            ...user,
            updating: false,
            deleting: false
        }))
    } catch (error) {
        console.error('获取用户列表失败:', error)
        if (error.response?.status === 403) {
            ElMessage.error('权限不足，请确保您具有管理员权限')
            router.push('/login')
        } else if (error.response?.status === 401) {
            ElMessage.error('请先登录')
            router.push('/login')
        } else {
            ElMessage.error(error.response?.data?.message || '获取用户列表失败，请稍后重试')
        }
    } finally {
        loading.value = false
    }
}

// 更新数据库
const handleUpdateDatabase = async () => {
    try {
        await ElMessageBox.confirm('确定要更新数据库吗？这将清理过期的预约请求和日程。', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
        
        updatingDatabase.value = true
        const response = await api.post('/admin/update-database/')
        ElMessage.success(response.message || '数据库更新成功')
        if (response.details) {
            ElMessage.info(`清理了 ${response.deleted_count} 条过期数据，包括 ${response.details.expired_appointments} 条过期预约和 ${response.details.old_schedules} 条过期日程`)
        }
    } catch (error) {
        console.error('更新数据库失败:', error)
        if (error.response?.status === 403) {
            ElMessage.error('权限不足，请确保您具有管理员权限')
            router.push('/login')
        } else if (error.response?.status === 401) {
            ElMessage.error('请先登录')
            router.push('/login')
        } else if (error === 'cancel') {
            // 用户取消操作，不做处理
        } else {
            ElMessage.error(error.response?.data?.message || '更新数据库失败，请稍后重试')
        }
    } finally {
        updatingDatabase.value = false
    }
}

// 切换用户状态
const handleToggleStatus = async (user) => {
    try {
        await ElMessageBox.confirm(
            `确定要${user.is_active ? '禁用' : '启用'}该用户吗？`,
            '提示',
            {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }
        )
        
        user.updating = true
        const response = await api.put(`/admin/users/${user.id}/`, {
            is_active: !user.is_active
        })
        user.is_active = !user.is_active
        ElMessage.success(response.message || '用户状态更新成功')
    } catch (error) {
        console.error('更新用户状态失败:', error)
        if (error.response?.status === 403) {
            ElMessage.error('权限不足，请确保您具有管理员权限')
            router.push('/login')
        } else if (error.response?.status === 401) {
            ElMessage.error('请先登录')
            router.push('/login')
        } else if (error === 'cancel') {
            // 用户取消操作，不做处理
        } else {
            ElMessage.error(error.response?.data?.message || '更新用户状态失败，请稍后重试')
        }
    } finally {
        user.updating = false
    }
}

// 删除用户
const handleDelete = async (user) => {
    try {
        await ElMessageBox.confirm(
            '确定要删除该用户吗？此操作不可恢复。',
            '警告',
            {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'error'
            }
        )
        
        user.deleting = true
        const response = await api.delete(`/admin/users/${user.id}/`)
        ElMessage.success(response.message || '用户删除成功')
        await fetchUsers()  // 重新获取用户列表
    } catch (error) {
        console.error('删除用户失败:', error)
        if (error.response?.status === 403) {
            ElMessage.error('权限不足，请确保您具有管理员权限')
            router.push('/login')
        } else if (error.response?.status === 401) {
            ElMessage.error('请先登录')
            router.push('/login')
        } else if (error === 'cancel') {
            // 用户取消操作，不做处理
        } else {
            ElMessage.error(error.response?.data?.message || '删除用户失败，请稍后重试')
        }
    } finally {
        user.deleting = false
    }
}

// 格式化角色显示
const formatRole = (role) => {
    const roleMap = {
        'admin': '管理员',
        'teacher': '教师',
        'student': '学生'
    }
    return roleMap[role] || role
}

// 获取角色标签类型
const getRoleTagType = (role) => {
    const typeMap = {
        'admin': 'danger',
        'teacher': 'warning',
        'student': 'success'
    }
    return typeMap[role] || 'info'
}

// 刷新列表
const handleRefresh = async () => {
    await fetchUsers()
}

onMounted(() => {
    fetchUsers()
})
</script>

<style scoped>
.user-manage-view {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    background-color: #f5f7fa;
    min-height: calc(100vh - 40px);
}

.page-header {
    margin-bottom: 30px;
    text-align: center;
    padding: 20px 0;
    background: linear-gradient(135deg, #409EFF, #67C23A);
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.page-header h1 {
    margin: 0;
    color: #fff;
    font-size: 28px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.page-header .subtitle {
    margin: 10px 0 0;
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
}

.manage-card {
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.action-bar {
    margin-bottom: 20px;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.action-btn {
    display: flex;
    align-items: center;
    gap: 5px;
    font-weight: 600;
}

.action-btn .el-icon {
    margin-right: 4px;
}

.el-table {
    margin-top: 20px;
    border-radius: 8px;
    overflow: hidden;
}

.el-table :deep(th) {
    background-color: #f5f7fa !important;
    font-weight: 600;
    color: #606266;
}

.el-table :deep(td) {
    padding: 12px 0;
}

.el-tag {
    border-radius: 4px;
    font-weight: 500;
}

.el-button-group {
    display: flex;
    gap: 8px;
}

.el-button {
    border-radius: 4px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 4px;
}

.table-footer {
    margin-top: 20px;
    text-align: right;
    color: #909399;
    font-size: 14px;
}

@media screen and (max-width: 768px) {
    .user-manage-view {
        padding: 10px;
    }
    
    .el-table {
        font-size: 14px;
    }
    
    .el-button {
        padding: 8px 15px;
    }

    .action-bar {
        flex-direction: column;
    }

    .action-btn {
        width: 100%;
        justify-content: center;
    }
}
</style> 