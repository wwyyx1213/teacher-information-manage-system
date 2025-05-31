<template>
  <div class="person-container">
    <el-card>
      <template #header>
        <span>个人信息</span>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px" style="max-width: 400px;">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="工号" prop="job_number">
          <el-input v-model="form.job_number" disabled />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="form.department" />
        </el-form-item>
        <el-form-item label="职称" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="联系方式" prop="contact">
          <el-input v-model="form.contact" />
        </el-form-item>
        <el-form-item label="简介" prop="bio">
          <el-input type="textarea" v-model="form.bio" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">保存修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

const form = ref({
  name: '',
  job_number: '',
  department: '',
  title: '',
  contact: '',
  bio: ''
})
const formRef = ref(null)
const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  department: [{ required: true, message: '请输入部门', trigger: 'blur' }],
  title: [{ required: true, message: '请输入职称', trigger: 'blur' }]
}

const fetchProfile = async () => {
  try {
    // 假设后端接口为 /teacher/profile/
    const res = await api.get('/teacher/profile/')
    Object.assign(form.value, res.data || res)
  } catch (e) {
    ElMessage.error('获取个人信息失败')
  }
}

const onSubmit = () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 假设后端接口为 /teacher/profile/
        await api.put('/teacher/profile/', form.value)
        ElMessage.success('信息已更新')
      } catch (e) {
        ElMessage.error('保存失败')
      }
    }
  })
}

onMounted(fetchProfile)
</script>

<style scoped>
.person-container {
  padding: 40px;
  display: flex;
  justify-content: center;
}
</style>