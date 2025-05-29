<template>
  <div class="appointment">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>预约教师</h2>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
      >
        <el-form-item label="预约日期" prop="date">
          <el-date-picker
            v-model="form.date"
            type="date"
            placeholder="选择日期"
            :disabled-date="disabledDate"
          />
        </el-form-item>

        <el-form-item label="预约时间段" prop="timeSlot">
          <el-select v-model="form.timeSlot" placeholder="选择时间段">
            <el-option
              v-for="slot in availableTimeSlots"
              :key="slot.value"
              :label="slot.label"
              :value="slot.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="预约目的" prop="purpose">
          <el-input
            v-model="form.purpose"
            type="textarea"
            :rows="4"
            placeholder="请简要说明预约目的"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">提交预约</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { teacherApi } from '@/api/teacher'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)

const form = ref({
  date: '',
  timeSlot: '',
  purpose: ''
})

const rules = {
  date: [{ required: true, message: '请选择预约日期', trigger: 'change' }],
  timeSlot: [{ required: true, message: '请选择时间段', trigger: 'change' }],
  purpose: [{ required: true, message: '请填写预约目的', trigger: 'blur' }]
}

const availableTimeSlots = ref([])

const loadAvailableTimeSlots = async () => {
  try {
    const response = await teacherApi.getTeacherSchedule(route.query.teacherId)
    const schedules = response.data.filter(schedule => 
      schedule.date === form.value.date && schedule.is_available
    )
    availableTimeSlots.value = schedules.map(schedule => ({
      label: `${schedule.start_time} - ${schedule.end_time}`,
      value: schedule.id
    }))
  } catch (error) {
    ElMessage.error('获取可用时间段失败')
  }
}

const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7
}

const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await teacherApi.createAppointment({
          teacher: route.query.teacherId,
          schedule: form.value.timeSlot,
          purpose: form.value.purpose
        })
        ElMessage.success('预约申请已提交')
        router.push('/teachers')
      } catch (error) {
        ElMessage.error('预约提交失败')
      }
    }
  })
}

const resetForm = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
}

onMounted(() => {
  if (route.query.date) {
    form.value.date = route.query.date
    loadAvailableTimeSlots()
  }
})
</script>

<style scoped>
.appointment {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>