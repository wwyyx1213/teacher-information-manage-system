<template>
  <div class="teacher-detail">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>{{ teacher.user?.first_name }} {{ teacher.user?.last_name }}</h2>
          <el-tag>{{ teacher.title }}</el-tag>
        </div>
      </template>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="院系">{{ teacher.department }}</el-descriptions-item>
        <el-descriptions-item label="研究方向">{{ teacher.research_direction }}</el-descriptions-item>
      </el-descriptions>
      
      <div class="introduction">
        <h3>个人简介</h3>
        <p>{{ teacher.introduction }}</p>
      </div>
    </el-card>

    <el-tabs v-model="activeTab" class="detail-tabs">
      <el-tab-pane label="研究项目" name="projects">
        <el-timeline>
          <el-timeline-item
            v-for="project in projects"
            :key="project.id"
            :timestamp="project.start_date"
            placement="top"
          >
            <el-card>
              <h4>{{ project.title }}</h4>
              <p>资金来源：{{ project.funding_source }}</p>
              <p>{{ project.description }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </el-tab-pane>

      <el-tab-pane label="发表论文" name="publications">
        <el-table :data="publications" style="width: 100%">
          <el-table-column prop="title" label="论文标题" />
          <el-table-column prop="journal" label="期刊名称" />
          <el-table-column prop="publication_date" label="发表日期" width="120" />
          <el-table-column prop="citation_count" label="引用次数" width="100" />
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="可预约时间" name="schedule">
        <el-calendar v-model="currentDate">
          <template #dateCell="{ data }">
            <div class="calendar-cell">
              <p>{{ data.day.split('-').slice(2).join('') }}</p>
              <el-button
                v-if="hasAvailableTime(data.day)"
                type="primary"
                size="small"
                @click="handleAppointment(data.day)"
              >
                预约
              </el-button>
            </div>
          </template>
        </el-calendar>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { teacherApi } from '@/api/teacher'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const teacher = ref({})
const projects = ref([])
const publications = ref([])
const schedules = ref([])
const activeTab = ref('projects')
const currentDate = ref(new Date())

const loadTeacherDetail = async () => {
  try {
    const response = await teacherApi.getTeacherDetail(route.params.id)
    teacher.value = response.data
  } catch (error) {
    ElMessage.error('获取教师详情失败')
  }
}

const loadProjects = async () => {
  try {
    const response = await teacherApi.getTeacherProjects(route.params.id)
    projects.value = response.data
  } catch (error) {
    ElMessage.error('获取研究项目失败')
  }
}

const loadPublications = async () => {
  try {
    const response = await teacherApi.getTeacherPublications(route.params.id)
    publications.value = response.data
  } catch (error) {
    ElMessage.error('获取发表论文失败')
  }
}

const loadSchedules = async () => {
  try {
    const response = await teacherApi.getTeacherSchedule(route.params.id)
    schedules.value = response.data
  } catch (error) {
    ElMessage.error('获取日程安排失败')
  }
}

const hasAvailableTime = (day) => {
  return schedules.value.some(schedule => 
    schedule.date === day && schedule.is_available
  )
}

const handleAppointment = (day) => {
  router.push({
    path: '/appointment',
    query: {
      teacherId: route.params.id,
      date: day
    }
  })
}

onMounted(() => {
  loadTeacherDetail()
  loadProjects()
  loadPublications()
  loadSchedules()
})
</script>

<style scoped>
.teacher-detail {
  padding: 20px;
}

.profile-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.introduction {
  margin-top: 20px;
}

.detail-tabs {
  margin-top: 20px;
}

.calendar-cell {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}
</style>