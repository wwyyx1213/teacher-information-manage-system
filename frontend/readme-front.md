好的，让我们开始创建并实现前端项目。我们将使用Vue 3和Element Plus来构建界面。

### 第一步：创建Vue 3项目

首先，在项目根目录下创建前端项目：

```bash
# 创建前端项目
npm create vue@latest frontend

# 在交互式提示中选择：
# ✔ Project name: frontend
# ✔ Add TypeScript? No
# ✔ Add JSX Support? No
# ✔ Add Vue Router? Yes
# ✔ Add Pinia? Yes
# ✔ Add Vitest? No
# ✔ Add End-to-End Testing? No
# ✔ Add ESLint? Yes
# ✔ Add Prettier? Yes

cd frontend
npm install
```

### 第二步：安装必要的依赖

```bash
# 安装Element Plus
npm install element-plus

# 安装axios用于API请求
npm install axios

# 安装其他工具库
npm install @element-plus/icons-vue
npm install dayjs
```

### 第三步：配置项目

1. 首先修改 `src/main.js`：

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
```

2. 创建API配置文件 `src/api/index.js`：

```javascript
import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 请求拦截器
api.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

export default api
```

3. 创建API服务文件 `src/api/teacher.js`：

```javascript
import api from './index'

export const teacherApi = {
    // 获取教师列表
    getTeachers(params) {
        return api.get('/teachers/', { params })
    },
    
    // 获取教师详情
    getTeacherDetail(id) {
        return api.get(`/teachers/${id}/`)
    },
    
    // 获取教师日程
    getTeacherSchedule(teacherId) {
        return api.get(`/schedules/`, { params: { teacher: teacherId } })
    },
    
    // 获取教师项目
    getTeacherProjects(teacherId) {
        return api.get(`/projects/`, { params: { teacher: teacherId } })
    },
    
    // 获取教师论文
    getTeacherPublications(teacherId) {
        return api.get(`/publications/`, { params: { teacher: teacherId } })
    },
    
    // 创建预约
    createAppointment(data) {
        return api.post('/appointments/', data)
    }
}
```

### 第四步：创建路由配置

修改 `src/router/index.js`：

```javascript
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/teachers',
      name: 'teachers',
      component: () => import('../views/teacher/TeacherList.vue')
    },
    {
      path: '/teacher/:id',
      name: 'teacher-detail',
      component: () => import('../views/teacher/TeacherDetail.vue')
    },
    {
      path: '/appointment',
      name: 'appointment',
      component: () => import('../views/appointment/AppointmentView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue')
    }
  ]
})

export default router
```

### 第五步：创建视图组件

1. 创建教师列表页面 `src/views/teacher/TeacherList.vue`：

```vue
<template>
  <div class="teacher-list">
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="关键词">
          <el-input v-model="searchForm.keyword" placeholder="姓名/研究方向/院系"></el-input>
        </el-form-item>
        <el-form-item label="院系">
          <el-select v-model="searchForm.department" placeholder="选择院系">
            <el-option
              v-for="dept in departments"
              :key="dept"
              :label="dept"
              :value="dept"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="list-card">
      <el-table :data="teachers" style="width: 100%">
        <el-table-column prop="user.first_name" label="姓名" width="120" />
        <el-table-column prop="title" label="职称" width="120" />
        <el-table-column prop="department" label="院系" width="180" />
        <el-table-column prop="research_direction" label="研究方向" />
        <el-table-column fixed="right" label="操作" width="120">
          <template #default="scope">
            <el-button
              link
              type="primary"
              @click="viewDetail(scope.row.id)"
            >
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { teacherApi } from '@/api/teacher'
import { ElMessage } from 'element-plus'

const router = useRouter()
const teachers = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const departments = ref(['计算机学院', '数学学院', '物理学院', '化学学院'])

const searchForm = ref({
  keyword: '',
  department: ''
})

const loadTeachers = async () => {
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchForm.value.keyword,
      department: searchForm.value.department
    }
    const response = await teacherApi.getTeachers(params)
    teachers.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    ElMessage.error('获取教师列表失败')
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadTeachers()
}

const resetSearch = () => {
  searchForm.value = {
    keyword: '',
    department: ''
  }
  handleSearch()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  loadTeachers()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  loadTeachers()
}

const viewDetail = (id) => {
  router.push(`/teacher/${id}`)
}

onMounted(() => {
  loadTeachers()
})
</script>

<style scoped>
.teacher-list {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
}

.list-card {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
```

2. 创建教师详情页面 `src/views/teacher/TeacherDetail.vue`：

```vue
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
```

3. 创建预约页面 `src/views/appointment/AppointmentView.vue`：

```vue
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
```

这些是主要的前端界面组件。接下来，我们还需要：

1. 创建登录页面
2. 实现状态管理
3. 添加导航栏
4. 实现首页
5. 添加错误处理
6. 实现响应式设计

