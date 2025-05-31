<template>
    <div class="placeholder-view">
        <el-card>教师详情页面开发中...</el-card>
    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Calendar, User, Document, Clock } from '@element-plus/icons-vue'
import teacherApi from '../api/teacher'

const route = useRoute()
const teacherId = route.params.id
const activeTab = ref('basic')

// 教师基本信息
const teacherInfo = ref({
  name: '',
  department: '',
  title: '',
  avatar: '',
  bio: '',
  research_areas: '',
  contact: '',
  education: '',
  work_experience: ''
})

// 日程数据
const scheduleData = ref([])
const currentWeek = ref(new Date())

// 科研成果数据
const researchData = ref({
  projects: [],
  achievements: []
})

// 预约相关数据
const appointmentData = ref({
  availableDates: [],
  selectedDate: null,
  selectedTime: null,
  consultation: ''
})

// 获取教师详情
const fetchTeacherDetail = async () => {
  try {
    const response = await teacherApi.getTeacherDetail(teacherId)
    teacherInfo.value = response
  } catch (error) {
    ElMessage.error('获取教师信息失败')
  }
}

// 获取教师日程
const fetchTeacherSchedule = async () => {
  try {
    const response = await teacherApi.getTeacherSchedule(teacherId)
    scheduleData.value = response
  } catch (error) {
    ElMessage.error('获取教师日程失败')
  }
}

// 获取科研成果
const fetchResearchData = async () => {
  try {
    const response = await teacherApi.getTeacherResearch(teacherId)
    researchData.value = response
  } catch (error) {
    ElMessage.error('获取科研成果失败')
  }
}

// 获取可预约时间
const fetchAvailableDates = async () => {
  try {
    const response = await teacherApi.getAvailableDates(teacherId)
    appointmentData.value.availableDates = response
  } catch (error) {
    ElMessage.error('获取可预约时间失败')
  }
}

// 提交预约
const submitAppointment = async () => {
  try {
    await teacherApi.submitAppointment({
      teacherId,
      date: appointmentData.value.selectedDate,
      time: appointmentData.value.selectedTime,
      consultation: appointmentData.value.consultation
    })
    ElMessage.success('预约提交成功')
  } catch (error) {
    ElMessage.error('预约提交失败')
  }
}

onMounted(() => {
  fetchTeacherDetail()
  fetchTeacherSchedule()
  fetchResearchData()
  fetchAvailableDates()
})
</script>
<style scoped>
.placeholder-view {
    padding: 40px;
    text-align: center;
}
</style> 