<template>
  <div class="teacher-detail">
    <div v-loading="loading">
      <!-- 顶部信息栏 -->
      <div class="header-info">
        <div class="avatar-section">
          <el-avatar :size="120" :src="teacher.avatar_url || '/default-avatar.png'" />
        </div>
        <div class="info-section">
          <h1>{{ teacher.name }}</h1>
          <p class="department">{{ teacher.department }}</p>
          <p class="title">{{ teacher.title }}</p>
          <div class="actions">
            <el-button v-if="userStore.isStudent" type="primary" @click="handleFollow">
              {{ isFollowing ? '取消关注' : '关注' }}
            </el-button>
            <el-button v-if="userStore.isTeacher && userStore.userId === teacher.user_id" type="primary" @click="handleEdit">
              编辑信息
            </el-button>
          </div>
        </div>
      </div>

      <!-- 标签导航 -->
      <el-tabs v-model="activeTab" class="detail-tabs">
        <!-- 基本信息 -->
        <el-tab-pane label="基本信息" name="basic">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>个人简介</span>
              </div>
            </template>
            <div class="bio-content">{{ teacher.bio || '暂无简介' }}</div>
          </el-card>
        </el-tab-pane>

        <!-- 日程安排 -->
        <el-tab-pane label="日程安排" name="schedule">
          <el-card class="schedule-card">
            <template #header>
              <div class="card-header">
                <span>可预约时间</span>
                <el-button v-if="userStore.isTeacher && userStore.userId === teacher.user_id" type="primary" link @click="handleAddSchedule">
                  添加时间段
                </el-button>
              </div>
            </template>
            <div class="schedule-content">
              <el-calendar v-model="currentDate">
                <template #dateCell="{ data }">
                  <div class="calendar-cell">
                    <p>{{ data.day.split('-').slice(2).join('') }}</p>
                    <div v-if="getScheduleForDate(data.day)" class="schedule-dot"></div>
                  </div>
                </template>
              </el-calendar>
            </div>
          </el-card>
        </el-tab-pane>

        <!-- 科研成果 -->
        <el-tab-pane label="科研成果" name="research">
          <el-card class="research-card">
            <template #header>
              <div class="card-header">
                <span>研究成果</span>
                <el-button v-if="userStore.isTeacher && userStore.userId === teacher.user_id" type="primary" link @click="handleAddResearch">
                  添加成果
                </el-button>
              </div>
            </template>
            <div class="research-content">
              <el-timeline>
                <el-timeline-item
                  v-for="achievement in achievements"
                  :key="achievement.id"
                  :timestamp="achievement.date"
                  placement="top"
                >
                  <el-card>
                    <h4>{{ achievement.title }}</h4>
                    <p>{{ achievement.description }}</p>
                    <p class="type">类型：{{ achievement.type }}</p>
                    <el-link v-if="achievement.file_url" :href="achievement.file_url" target="_blank">
                      查看详情
                    </el-link>
                  </el-card>
                </el-timeline-item>
              </el-timeline>
            </div>
          </el-card>
        </el-tab-pane>

        <!-- 预约 -->
        <el-tab-pane label="预约" name="appointment">
          <el-card class="appointment-card">
            <template #header>
              <div class="card-header">
                <span>预约咨询</span>
              </div>
            </template>
            <div class="appointment-content">
              <el-form :model="appointmentForm" label-width="100px">
                <el-form-item label="预约日期">
                  <el-date-picker
                    v-model="appointmentForm.date"
                    type="date"
                    placeholder="选择日期"
                    :disabled-date="disabledDate"
                  />
                </el-form-item>
                <el-form-item label="预约时间">
                  <el-select v-model="appointmentForm.time" placeholder="选择时间段">
                    <el-option
                      v-for="time in availableTimes"
                      :key="time"
                      :label="time"
                      :value="time"
                    />
                  </el-select>
                </el-form-item>
                <el-form-item label="咨询事项">
                  <el-input
                    v-model="appointmentForm.remarks"
                    type="textarea"
                    :rows="4"
                    placeholder="请简要描述您的咨询事项"
                  />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleAppointment" :loading="submitting">
                    提交预约
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import api from '../../api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const submitting = ref(false)
const activeTab = ref('basic')
const currentDate = ref(new Date())
const isFollowing = ref(false)

const teacher = ref({})
const achievements = ref([])
const schedules = ref([])

const appointmentForm = reactive({
  date: '',
  time: '',
  remarks: ''
})

// 获取教师详情
const fetchTeacherDetail = async () => {
  try {
    loading.value = true
    const response = await api.get(`/teachers/${route.params.id}/`)
    teacher.value = response
  } catch (error) {
    ElMessage.error('获取教师信息失败：' + (error.response?.data?.message || error.message))
  } finally {
    loading.value = false
  }
}

// 获取科研成果
const fetchAchievements = async () => {
  try {
    const response = await api.get(`/teachers/${route.params.id}/research/`)
    achievements.value = response
  } catch (error) {
    ElMessage.error('获取科研成果失败：' + (error.response?.data?.message || error.message))
  }
}

// 获取日程安排
const fetchSchedules = async () => {
  try {
    const response = await api.get(`/teachers/${route.params.id}/schedule/`)
    schedules.value = response
  } catch (error) {
    ElMessage.error('获取日程安排失败：' + (error.response?.data?.message || error.message))
  }
}

// 处理关注
const handleFollow = async () => {
  try {
    if (isFollowing.value) {
      await api.delete(`/follows/${teacher.value.id}/`)
      isFollowing.value = false
      ElMessage.success('已取消关注')
    } else {
      await api.post('/follows/', { teacher_id: teacher.value.id })
      isFollowing.value = true
      ElMessage.success('关注成功')
    }
  } catch (error) {
    ElMessage.error('操作失败：' + (error.response?.data?.message || error.message))
  }
}

// 处理编辑
const handleEdit = () => {
  router.push(`/teacher/edit/${teacher.value.id}`)
}

// 处理添加日程
const handleAddSchedule = () => {
  // 实现添加日程的逻辑
}

// 处理添加科研成果
const handleAddResearch = () => {
  // 实现添加科研成果的逻辑
}

// 获取指定日期的日程
const getScheduleForDate = (date) => {
  return schedules.value.find(schedule => schedule.start_time.startsWith(date))
}

// 禁用不可预约的日期
const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7
}

// 获取可预约时间段
const availableTimes = computed(() => {
  const times = [
    '09:00-10:00',
    '10:00-11:00',
    '15:00-16:00',
    '16:00-17:00',
    '19:00-20:00',
    '20:00-21:00'
  ]
  
  // 过滤掉已预约的时间段
  const date = appointmentForm.date
  if (!date) return times
  
  // 将日期转换为本地日期字符串（YYYY-MM-DD）
  const localDate = new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).replace(/\//g, '-')
  
  const bookedTimes = schedules.value
    .filter(schedule => schedule.start_time.startsWith(localDate))
    .map(schedule => schedule.time_slot)
  
  return times.filter(time => !bookedTimes.includes(time))
})

// 处理预约
const handleAppointment = async () => {
  if (!appointmentForm.date || !appointmentForm.time || !appointmentForm.remarks) {
    ElMessage.warning('请填写完整的预约信息')
    return
  }

  try {
    submitting.value = true
    
    // 格式化日期和时间
    const date = new Date(appointmentForm.date)
    const [startTime] = appointmentForm.time.split('-')
    const [hours, minutes] = startTime.split(':')
    
    // 设置时间（使用本地时间）
    date.setHours(parseInt(hours))
    date.setMinutes(parseInt(minutes))
    date.setSeconds(0)
    
    // 转换为 UTC 时间
    const utcDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000)
    const timeSlot = utcDate.toISOString().split('.')[0]
    
    console.log('本地时间：', date.toLocaleString())
    console.log('发送的预约时间：', timeSlot)
    
    const response = await api.post('/appointments/', {
      teacher_id: teacher.value.id,
      time_slot: timeSlot,
      remarks: appointmentForm.remarks
    })
    
    if (response.message) {
      ElMessage.success(response.message)
      router.push('/my-appointments')
    } else {
      ElMessage.error('预约失败：服务器响应格式错误')
    }
  } catch (error) {
    console.error('预约错误：', error)
    ElMessage.error('预约失败：' + (error.response?.data?.message || error.message))
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchTeacherDetail()
  fetchAchievements()
  fetchSchedules()
})
</script>

<style scoped>
.teacher-detail {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header-info {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.avatar-section {
  flex-shrink: 0;
}

.info-section {
  flex-grow: 1;
}

.info-section h1 {
  margin: 0 0 10px;
  color: #303133;
}

.department, .title {
  margin: 5px 0;
  color: #606266;
}

.actions {
  margin-top: 20px;
}

.detail-tabs {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-card, .schedule-card, .research-card, .appointment-card {
  margin-bottom: 20px;
}

.bio-content {
  line-height: 1.6;
  color: #606266;
}

.calendar-cell {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.schedule-dot {
  width: 8px;
  height: 8px;
  background-color: #409EFF;
  border-radius: 50%;
  margin-top: 4px;
}

.research-content {
  padding: 20px 0;
}

.type {
  color: #909399;
  font-size: 14px;
  margin: 5px 0;
}

.appointment-content {
  max-width: 600px;
  margin: 0 auto;
}
</style> 