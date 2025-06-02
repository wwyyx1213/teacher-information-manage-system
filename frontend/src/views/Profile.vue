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
                        <div class="placeholder-tab">日程管理功能开发中...</div>
                    </el-tab-pane>
                    <el-tab-pane label="成果管理" name="achievement">
                        <div class="placeholder-tab">成果管理功能开发中...</div>
                    </el-tab-pane>
                    <el-tab-pane label="预约管理" name="appointment">
                        <div class="placeholder-tab">预约管理功能开发中...</div>
                    </el-tab-pane>
                </el-tabs>
            </el-card>
        </template>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import api from '../api'
import { ElMessage } from 'element-plus'

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

onMounted(() => {
    fetchProfile()
})
</script>

<style scoped>
.profile-view {
    padding: 20px;
    max-width: 700px;
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
.profile-tabs {
    min-height: 400px;
}
.profile-form {
    margin-top: 20px;
    max-width: 500px;
}
.placeholder-tab {
    color: #aaa;
    text-align: center;
    padding: 60px 0;
    font-size: 1.2em;
}
</style> 