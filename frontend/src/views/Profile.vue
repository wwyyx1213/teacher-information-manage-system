<template>
    <div class="profile-view">
        <!-- 非教师用户提示 -->
        <el-result
            v-if="!isTeacher"
            icon="warning"
            title="权限不足"
            sub-title="只有教师用户可以访问此页面"
        >
            <template #extra>
                <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
            </template>
        </el-result>
        
        <!-- 教师用户界面 -->
        <template v-else>
            <div class="page-header">
                <h1>教师个人中心</h1>
            </div>
            <el-card>
                <el-tabs v-model="activeTab" tab-position="left" class="profile-tabs">
                    <el-tab-pane label="基本信息" name="base">
                        <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" class="profile-form">
                            <el-form-item label="姓名" prop="name">
                                <el-input v-model="form.name" />
                            </el-form-item>
                            <el-form-item label="院系" prop="department">
                                <el-select v-model="form.department" filterable placeholder="请选择院系">
                                    <el-option v-for="dept in departments" :key="dept" :label="dept" :value="dept" />
                                </el-select>
                            </el-form-item>
                            <el-form-item label="职称" prop="title">
                                <el-select v-model="form.title" filterable placeholder="请选择职称">
                                    <el-option v-for="title in titles" :key="title" :label="title" :value="title" />
                                </el-select>
                            </el-form-item>
                            <el-form-item label="研究方向" prop="research_areas">
                                <el-input v-model="form.research_areas" placeholder="多个方向用逗号分隔" />
                            </el-form-item>
                            <el-form-item label="个人主页" prop="homepage_url">
                                <el-input v-model="form.homepage_url" />
                            </el-form-item>
                            <el-form-item label="头像URL" prop="avatar_url">
                                <el-input v-model="form.avatar_url" />
                            </el-form-item>
                            <el-form-item label="个人简介" prop="bio">
                                <el-input type="textarea" v-model="form.bio" :rows="3" />
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
                            </el-form-item>
                        </el-form>
                    </el-tab-pane>
                    <el-tab-pane label="日程管理" name="schedule">
                        <div class="schedule-management">
                            <div class="schedule-header">
                                <h3>日程管理</h3>
                                <el-button type="primary" @click="showAddScheduleDialog">添加日程</el-button>
                            </div>
                            
                            <!-- 日程列表 -->
                            <el-table :data="schedules" style="width: 100%" v-loading="scheduleLoading">
                                <el-table-column prop="start_time" label="开始时间" width="180">
                                    <template #default="scope">
                                        {{ formatDateTime(scope.row.start_time) }}
                                    </template>
                                </el-table-column>
                                <el-table-column prop="end_time" label="结束时间" width="180">
                                    <template #default="scope">
                                        {{ formatDateTime(scope.row.end_time) }}
                                    </template>
                                </el-table-column>
                                <el-table-column prop="is_available" label="状态" width="100">
                                    <template #default="scope">
                                        <el-tag :type="scope.row.is_available ? 'success' : 'info'">
                                            {{ scope.row.is_available ? '可预约' : '不可预约' }}
                                        </el-tag>
                                    </template>
                                </el-table-column>
                                <el-table-column label="操作" width="150">
                                    <template #default="scope">
                                        <el-button type="primary" link @click="editSchedule(scope.row)" class="action-button edit-button">编辑</el-button>
                                        <el-button type="danger" link @click="deleteSchedule(scope.row)" class="action-button delete-button">删除</el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </el-tab-pane>
                    <el-tab-pane label="成果管理" name="achievement">
                        <div class="achievement-management">
                            <div class="achievement-header">
                                <h3>成果管理</h3>
                                <el-button type="primary" @click="showAddAchievementDialog">添加成果</el-button>
                            </div>
                            
                            <!-- 成果列表 -->
                            <el-table :data="achievements" style="width: 100%" v-loading="achievementLoading">
                                <el-table-column prop="title" label="标题" min-width="200" />
                                <el-table-column prop="type" label="类型" width="120">
                                    <template #default="scope">
                                        <el-tag>{{ scope.row.type }}</el-tag>
                                    </template>
                                </el-table-column>
                                <el-table-column prop="date" label="日期" width="120">
                                    <template #default="scope">
                                        {{ formatDate(scope.row.date) }}
                                    </template>
                                </el-table-column>
                                <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
                                <el-table-column label="操作" width="150">
                                    <template #default="scope">
                                        <el-button type="primary" link @click="editAchievement(scope.row)" class="action-button edit-button">编辑</el-button>
                                        <el-button type="danger" link @click="deleteAchievement(scope.row)" class="action-button delete-button">删除</el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </el-tab-pane>
                </el-tabs>
            </el-card>
        </template>
    </div>

    <!-- 添加/编辑日程对话框 -->
    <el-dialog
        v-model="scheduleDialogVisible"
        :title="isEditingSchedule ? '编辑日程' : '添加日程'"
        width="500px"
    >
        <el-form :model="scheduleForm" :rules="scheduleRules" ref="scheduleFormRef" label-width="100px">
            <el-form-item label="日期" prop="date">
                <el-date-picker
                    v-model="scheduleForm.date"
                    type="date"
                    placeholder="选择日期"
                    style="width: 100%"
                />
            </el-form-item>
            <el-form-item label="开始时间" prop="start_time">
                <el-select v-model="scheduleForm.start_time" placeholder="选择时间段" style="width: 100%">
                    <el-option
                        v-for="time in availableHours"
                        :key="time.start"
                        :label="time.label"
                        :value="time.start"
                    />
                </el-select>
            </el-form-item>
            <el-form-item label="状态" prop="is_available">
                <el-switch
                    v-model="scheduleForm.is_available"
                    active-text="可预约"
                    inactive-text="不可预约"
                />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="scheduleDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitSchedule" :loading="submittingSchedule">
                    确定
                </el-button>
            </span>
        </template>
    </el-dialog>

    <!-- 添加/编辑成果对话框 -->
    <el-dialog
        v-model="achievementDialogVisible"
        :title="isEditingAchievement ? '编辑成果' : '添加成果'"
        width="500px"
    >
        <el-form :model="achievementForm" :rules="achievementRules" ref="achievementFormRef" label-width="100px">
            <el-form-item label="标题" prop="title">
                <el-input v-model="achievementForm.title" />
            </el-form-item>
            <el-form-item label="类型" prop="type">
                <el-select v-model="achievementForm.type" placeholder="选择类型" style="width: 100%">
                    <el-option label="论文" value="论文" />
                    <el-option label="项目" value="项目" />
                    <el-option label="基金" value="基金" />
                    <el-option label="著作" value="著作" />
                </el-select>
            </el-form-item>
            <el-form-item label="日期" prop="date">
                <el-date-picker
                    v-model="achievementForm.date"
                    type="date"
                    placeholder="选择日期"
                    style="width: 100%"
                />
            </el-form-item>
            <el-form-item label="描述" prop="description">
                <el-input
                    v-model="achievementForm.description"
                    type="textarea"
                    :rows="3"
                    placeholder="请输入成果描述"
                />
            </el-form-item>
            <el-form-item label="文件URL" prop="file_url">
                <el-input v-model="achievementForm.file_url" placeholder="可选：输入相关文件URL" />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="achievementDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitAchievement" :loading="submittingAchievement">
                    确定
                </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import api from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

const router = useRouter()
const userStore = useUserStore()
const isTeacher = computed(() => userStore.isTeacher)

const activeTab = ref('base')
const form = reactive({
    name: '',
    department: '',
    title: '',
    research_areas: '',
    homepage_url: '',
    avatar_url: '',
    bio: ''
})
const rules = {
    name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
    department: [{ required: true, message: '请选择院系', trigger: 'change' }],
    title: [{ required: true, message: '请选择职称', trigger: 'change' }],
}
const formRef = ref()
const saving = ref(false)
const departments = ref(['计算机学院','数学学院','物理学院','化学学院','信息工程学院','自动化学院'])
const titles = ref(['教授','副教授','讲师','助教'])

const fetchProfile = async () => {
    if (!isTeacher.value) return
    
    try {
        const res = await api.get('/profile/')
        Object.assign(form, res)
    } catch (e) {
        ElMessage.error(e.response?.data?.message || '获取个人信息失败')
        if (e.response?.status === 403) {
            router.push('/')
        }
    }
}

const handleSave = () => {
    if (!isTeacher.value) {
        ElMessage.error('只有教师用户可以修改个人信息')
        return
    }
    
    formRef.value.validate(async (valid) => {
        if (!valid) return
        saving.value = true
        try {
            await api.put('/profile/', form)
            ElMessage.success('保存成功')
            fetchProfile()
        } catch (e) {
            if (e.response?.status === 403) {
                ElMessage.error('权限不足，无法修改')
            } else {
                ElMessage.error(e.response?.data?.message || '保存失败')
            }
        } finally {
            saving.value = false
        }
    })
}

// 日程管理相关
const schedules = ref([])
const scheduleLoading = ref(false)
const scheduleDialogVisible = ref(false)
const isEditingSchedule = ref(false)
const submittingSchedule = ref(false)
const scheduleFormRef = ref()
const scheduleForm = reactive({
    date: '',
    start_time: '',
    is_available: true
})
const scheduleRules = {
    date: [{ required: true, message: '请选择日期', trigger: 'change' }],
    start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }]
}
const availableHours = [
    { start: 8, end: 9, label: '8:00-9:00' },
    { start: 9, end: 10, label: '9:00-10:00' },
    { start: 10, end: 11, label: '10:00-11:00' },
    { start: 11, end: 12, label: '11:00-12:00' },
    { start: 14, end: 15, label: '14:00-15:00' },
    { start: 15, end: 16, label: '15:00-16:00' },
    { start: 16, end: 17, label: '16:00-17:00' },
    { start: 19, end: 20, label: '19:00-20:00' },
    { start: 20, end: 21, label: '20:00-21:00' }
]

// 成果管理相关
const achievements = ref([])
const achievementLoading = ref(false)
const achievementDialogVisible = ref(false)
const isEditingAchievement = ref(false)
const submittingAchievement = ref(false)
const achievementFormRef = ref()
const achievementForm = reactive({
    title: '',
    type: '',
    date: '',
    description: '',
    file_url: ''
})
const achievementRules = {
    title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
    type: [{ required: true, message: '请选择类型', trigger: 'change' }],
    date: [{ required: true, message: '请选择日期', trigger: 'change' }],
    description: [{ required: true, message: '请输入描述', trigger: 'blur' }]
}

// 获取日程列表
const fetchSchedules = async () => {
    if (!isTeacher.value) return
    scheduleLoading.value = true
    try {
        const res = await api.get('/teacher/schedules/')
        schedules.value = res
    } catch (e) {
        ElMessage.error(e.response?.data?.message || '获取日程列表失败')
    } finally {
        scheduleLoading.value = false
    }
}

// 获取成果列表
const fetchAchievements = async () => {
    if (!isTeacher.value) return
    achievementLoading.value = true
    try {
        const res = await api.get('/teacher/achievements/')
        achievements.value = res
    } catch (e) {
        ElMessage.error(e.response?.data?.message || '获取成果列表失败')
    } finally {
        achievementLoading.value = false
    }
}

// 显示添加日程对话框
const showAddScheduleDialog = () => {
    isEditingSchedule.value = false
    scheduleForm.date = ''
    scheduleForm.start_time = ''
    scheduleForm.is_available = true
    scheduleDialogVisible.value = true
}

// 显示添加成果对话框
const showAddAchievementDialog = () => {
    isEditingAchievement.value = false
    achievementForm.title = ''
    achievementForm.type = ''
    achievementForm.date = ''
    achievementForm.description = ''
    achievementForm.file_url = ''
    achievementDialogVisible.value = true
}

// 编辑日程
const editSchedule = (schedule) => {
    isEditingSchedule.value = true
    scheduleForm.date = dayjs(schedule.start_time).format('YYYY-MM-DD')
    scheduleForm.start_time = dayjs(schedule.start_time).hour()
    scheduleForm.is_available = schedule.is_available
    scheduleForm.id = schedule.id
    scheduleDialogVisible.value = true
}

// 编辑成果
const editAchievement = (achievement) => {
    isEditingAchievement.value = true
    Object.assign(achievementForm, achievement)
    achievementDialogVisible.value = true
}

// 删除日程
const deleteSchedule = async (schedule) => {
    try {
        await ElMessageBox.confirm('确定要删除这个日程吗？', '提示', {
            type: 'warning'
        })
        await api.delete(`/teacher/schedules/${schedule.id}/`)
        ElMessage.success('删除成功')
        fetchSchedules()
    } catch (e) {
        if (e !== 'cancel') {
            ElMessage.error(e.response?.data?.message || '删除失败')
        }
    }
}

// 删除成果
const deleteAchievement = async (achievement) => {
    try {
        await ElMessageBox.confirm('确定要删除这个成果吗？', '提示', {
            type: 'warning'
        })
        await api.delete(`/teacher/achievements/${achievement.id}/`)
        ElMessage.success('删除成功')
        fetchAchievements()
    } catch (e) {
        if (e !== 'cancel') {
            ElMessage.error(e.response?.data?.message || '删除失败')
        }
    }
}

// 提交日程
const submitSchedule = async () => {
    if (!scheduleFormRef.value) return
    await scheduleFormRef.value.validate(async (valid) => {
        if (valid) {
            submittingSchedule.value = true
            try {
                const startTime = dayjs(scheduleForm.date)
                    .hour(scheduleForm.start_time)
                    .minute(0)
                    .second(0)
                const endTime = startTime.add(1, 'hour')
                
                const data = {
                    start_time: startTime.toISOString(),
                    end_time: endTime.toISOString(),
                    is_available: scheduleForm.is_available
                }
                
                if (isEditingSchedule.value) {
                    await api.put(`/teacher/schedules/${scheduleForm.id}/`, data)
                    ElMessage.success('更新成功')
                } else {
                    await api.post('/teacher/schedules/', data)
                    ElMessage.success('添加成功')
                }
                scheduleDialogVisible.value = false
                fetchSchedules()
            } catch (e) {
                ElMessage.error(e.response?.data?.message || '操作失败')
            } finally {
                submittingSchedule.value = false
            }
        }
    })
}

// 提交成果
const submitAchievement = async () => {
    if (!achievementFormRef.value) return
    await achievementFormRef.value.validate(async (valid) => {
        if (valid) {
            submittingAchievement.value = true
            try {
                const data = {
                    ...achievementForm,
                    date: dayjs(achievementForm.date).format('YYYY-MM-DD')
                }
                
                if (isEditingAchievement.value) {
                    await api.put(`/teacher/achievements/${achievementForm.id}/`, data)
                    ElMessage.success('更新成功')
                } else {
                    await api.post('/teacher/achievements/', data)
                    ElMessage.success('添加成功')
                }
                achievementDialogVisible.value = false
                fetchAchievements()
            } catch (e) {
                ElMessage.error(e.response?.data?.message || '操作失败')
            } finally {
                submittingAchievement.value = false
            }
        }
    })
}

// 格式化日期时间
const formatDateTime = (datetime) => {
    return dayjs(datetime).format('YYYY-MM-DD HH:mm')
}

// 格式化日期
const formatDate = (date) => {
    return dayjs(date).format('YYYY-MM-DD')
}

onMounted(() => {
    fetchProfile()
    fetchSchedules()
    fetchAchievements()
})
</script>

<style scoped>
.profile-view {
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
    background: linear-gradient(to right, #409EFF, #67C23A);
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.page-header h1 {
    margin: 0;
    color: #fff;
    font-size: 28px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.el-card {
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.profile-tabs {
    min-height: 600px;
    padding: 20px;
}

.profile-tabs :deep(.el-tabs__nav) {
    width: 160px;
}

.profile-tabs :deep(.el-tabs__item) {
    height: 50px;
    line-height: 50px;
    font-size: 16px;
    text-align: left;
    padding-left: 20px;
}

.profile-tabs :deep(.el-tabs__content) {
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 0 8px 8px 0;
    min-height: 500px;
}

.profile-form {
    margin-top: 20px;
    max-width: 800px;
    padding: 30px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
}

.schedule-management,
.achievement-management {
    padding: 30px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
}

.schedule-header,
.achievement-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 2px solid #ebeef5;
}

.schedule-header h3,
.achievement-header h3 {
    margin: 0;
    color: #303133;
    font-size: 20px;
    font-weight: 600;
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

.el-dialog {
    max-width: 600px;
    border-radius: 8px;
}

.el-dialog :deep(.el-dialog__header) {
    padding: 20px;
    margin: 0;
    border-bottom: 1px solid #ebeef5;
}

.el-dialog :deep(.el-dialog__body) {
    padding: 30px 20px;
}

.el-dialog :deep(.el-dialog__footer) {
    padding: 15px 20px;
    border-top: 1px solid #ebeef5;
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 20px;
}

.el-form-item {
    margin-bottom: 25px;
}

.el-form-item :deep(.el-form-item__label) {
    font-weight: 500;
    color: #606266;
}

.el-input,
.el-select,
.el-date-picker {
    width: 100%;
}

.el-input :deep(.el-input__inner),
.el-select :deep(.el-input__inner) {
    border-radius: 4px;
}

.el-tag {
    margin-right: 8px;
    border-radius: 4px;
}

.el-button {
    border-radius: 4px;
    font-weight: 500;
}

.el-button--primary {
    background: linear-gradient(to right, #409EFF, #67C23A);
    border: none;
}

.el-button--primary:hover {
    background: linear-gradient(to right, #67C23A, #409EFF);
    opacity: 0.9;
}

.el-button--danger {
    background: linear-gradient(to right, #F56C6C, #E6A23C);
    border: none;
}

.el-button--danger:hover {
    background: linear-gradient(to right, #E6A23C, #F56C6C);
    opacity: 0.9;
}

/* 修改操作按钮样式 */
.action-button {
    font-weight: 500;
    padding: 4px 8px;
    margin: 0 4px;
    border-radius: 4px;
    transition: all 0.3s;
}

.edit-button {
    color: #409EFF;
    background-color: rgba(64, 158, 255, 0.1);
}

.edit-button:hover {
    color: #fff;
    background-color: #409EFF;
}

.delete-button {
    color: #F56C6C;
    background-color: rgba(245, 108, 108, 0.1);
}

.delete-button:hover {
    color: #fff;
    background-color: #F56C6C;
}

/* 添加响应式布局 */
@media screen and (max-width: 768px) {
    .profile-view {
        padding: 10px;
    }
    
    .profile-tabs :deep(.el-tabs__nav) {
        width: 120px;
    }
    
    .profile-tabs :deep(.el-tabs__content) {
        padding: 15px;
    }
    
    .schedule-management,
    .achievement-management {
        padding: 15px;
    }
}
</style> 