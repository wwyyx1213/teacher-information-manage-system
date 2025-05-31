<template>
  <div class="appointment-view">
    <el-card>
      <template #header>
        <span>预约教师：{{ teacherInfo.name }}</span>
      </template>
      <div>
        <el-calendar
          v-model="selectedDate"
          :disabled-date="isDateDisabled"
          @input="onDateSelect"
        />
      </div>
      <div v-if="showForm" class="appointment-form">
        <el-form :model="form" ref="formRef" label-width="80px">
          <el-form-item label="预约时间">
            <el-date-picker
              v-model="form.time"
              type="datetime"
              :disabled-date="isDateDisabled"
              :default-value="selectedDate"
              placeholder="请选择具体时间"
            />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="form.remarks" type="textarea" placeholder="请输入备注" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitAppointment">提交预约</el-button>
          </el-form-item>
        </el-form>
      </div>
      <el-empty v-if="!calendarLoaded" description="正在加载日程..." />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import teacherApi from '../../api/teacher'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const teacherId = route.params.id

const teacherInfo = ref({ name: '' })
const busyDates = ref([]) // 存储教师忙碌的日期
const selectedDate = ref(null)
const showForm = ref(false)
const calendarLoaded = ref(false)
const form = ref({
  time: '',
  remarks: ''
})
const formRef = ref(null)

// 获取教师信息
const fetchTeacherInfo = async () => {
  try {
    const res = await teacherApi.getTeacherDetail(teacherId)
    teacherInfo.value = res
  } catch (e) {
    ElMessage.error('获取教师信息失败')
  }
}

// 获取教师日程（假设 busyDates 为['2024-06-01','2024-06-03']）
const fetchTeacherSchedule = async () => {
  try {
    const res = await teacherApi.getTeacherSchedule(teacherId)
    busyDates.value = res.busy_dates || []
    calendarLoaded.value = true
  } catch (e) {
    ElMessage.error('获取教师日程失败')
    calendarLoaded.value = true
  }
}

// 判断日期是否可选
const isDateDisabled = (date) => {
  const d = date.toISOString().slice(0, 10)
  return busyDates.value.includes(d)
}

// 选择日期后显示表单
const onDateSelect = (date) => {
  if (!isDateDisabled(date)) {
    showForm.value = true
    form.value.time = date
  } else {
    showForm.value = false
  }
}

// 提交预约
const submitAppointment = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await api.post('/appointments/', {
          teacher_id: teacherId,
          time: form.value.time,
          remarks: form.value.remarks
        })
        ElMessage.success('预约成功')
        router.push('/myappointments')
      } catch (e) {
        ElMessage.error('预约失败')
      }
    }
  })
}

onMounted(() => {
  fetchTeacherInfo()
  fetchTeacherSchedule()
})
</script>

<style scoped>
.appointment-view {
  padding: 40px;
  max-width: 600px;
  margin: 0 auto;
}
.appointment-form {
  margin-top: 30px;
}
</style>