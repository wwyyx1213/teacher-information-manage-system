<template>
  <div class="home-container">
    <!-- 顶部欢迎区域 -->
    <el-card class="welcome-card">
      <h1>欢迎使用教师信息管理系统</h1>
      <p>在这里，您可以：</p>
      <div class="feature-list">
         <el-button round>浏览教师信息</el-button>
         <el-button round>查看教师日程</el-button>
         <el-button round>预约教师</el-button>
         <el-button round>查看科研成果</el-button>
      </div>
    </el-card>

    <!-- 搜索区域 -->
    <el-card class="search-card">
       <div class="search-input-container">
          <el-input v-model="searchQuery" placeholder="搜索教师" class="search-input">
             <template #prepend>搜索教师</template>
             <template #append>
                <el-select v-model="searchCondition" placeholder="条件" style="width: 100px">
                   <el-option v-for="condition in searchConditions" :key="condition.value" :label="condition.label" :value="condition.value"></el-option>
                </el-select>
             </template>
          </el-input>
          <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
       </div>
    </el-card>

    <!-- 推荐教师区域 -->
    <el-card class="recommended-teachers-card">
      <template #header>
        <div class="card-header">
          <span>推荐教师</span>
          <el-button type="text" @click="$router.push('/recommendations')">查看更多<el-icon class="el-icon--right"><ArrowRight /></el-icon></el-button>
        </div>
      </template>
      <div class="recommended-teachers-list">
        <el-scrollbar>
          <div class="scrollbar-flex-content">
            <el-card v-for="teacher in recommendedTeachers" :key="teacher.id" class="teacher-card" shadow="hover" @click="goToTeacherDetail(teacher.id)">
              <template #header>
                 <div class="teacher-card-header">
                    <el-avatar :size="60" :src="teacher.avatar_url || teacher.avatar" />
                    <div class="teacher-info">
                       <h3>{{ teacher.name }}</h3>
                       <p>{{ teacher.department || teacher.major }}</p>
                    </div>
                 </div>
              </template>
              <p>{{ teacher.recommend_reason || teacher.reason }}</p>
            </el-card>
          </div>
        </el-scrollbar>
      </div>
       <el-empty v-if="!recommendedTeachers.length && !loadingRecommend" description="暂无推荐教师" />
    </el-card>

    <!-- 教师列表区域 -->
    <el-card class="teacher-list-card">
       <template #header>
          <div class="card-header">
             <span>教师列表</span>
             <div class="filter-options">
                <el-select v-model="filterMajor" placeholder="按专业筛选" clearable @change="handleFilter" style="width: 120px; margin-right: 10px;">
                   <el-option v-for="major in majors" :key="major" :label="major" :value="major"></el-option>
                </el-select>
                 <el-select v-model="filterTitle" placeholder="按职称筛选" clearable @change="handleFilter" style="width: 120px;">
                   <el-option v-for="title in titles" :key="title" :label="title" :value="title"></el-option>
                </el-select>
             </div>
          </div>
       </template>
       <el-row :gutter="20" class="teacher-grid">
          <el-col :span="6" v-for="teacher in teacherList" :key="teacher.id">
             <el-card class="teacher-card-grid" shadow="hover" @click="goToTeacherDetail(teacher.id)">
                <div class="teacher-card-content">
                   <el-avatar :size="50" :src="teacher.avatar_url || teacher.avatar" class="teacher-avatar-grid" />
                   <div class="teacher-details-grid">
                      <h3>{{ teacher.name }}</h3>
                      <p>院系: {{ teacher.department }}</p>
                      <p>职称: {{ teacher.title }}</p>
                   </div>
                </div>
             </el-card>
          </el-col>
       </el-row>
        <el-empty v-if="!teacherList.length && !loadingList" description="暂无教师数据" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import api from '../api'
import { ElMessage } from 'element-plus'
import { Search, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 搜索相关
const searchQuery = ref('')
const searchCondition = ref('name')
const searchConditions = [
  { label: '姓名', value: 'name' },
  { label: '院系', value: 'department' },
  { label: '职称', value: 'title' },
  { label: '研究方向', value: 'research_areas' },
]
const handleSearch = () => {
  router.push({
    path: '/teachers',
    query: {
      [searchCondition.value]: searchQuery.value
    }
  })
}

// 推荐教师
const recommendedTeachers = ref([])
const loadingRecommend = ref(false)
const fetchRecommendedTeachers = async () => {
  try {
    loadingRecommend.value = true
    const res = await api.get('/recommendations/')
    recommendedTeachers.value = (res.results || res) // 兼容不同返回结构
  } catch (e) {
    ElMessage.error('获取推荐教师失败')
  } finally {
    loadingRecommend.value = false
  }
}

// 教师列表
const teacherList = ref([])
const loadingList = ref(false)
const filterMajor = ref('')
const filterTitle = ref('')
const majors = ref([])
const titles = ref([])
const fetchTeacherList = async () => {
  try {
    loadingList.value = true
    const params = {}
    if (filterMajor.value) params.department = filterMajor.value
    if (filterTitle.value) params.title = filterTitle.value
    const res = await api.get('/teachers/', { params })
    teacherList.value = res.results || res
    // 自动收集专业和职称
    majors.value = [...new Set((res.results || res).map(t => t.department).filter(Boolean))]
    titles.value = [...new Set((res.results || res).map(t => t.title).filter(Boolean))]
  } catch (e) {
    ElMessage.error('获取教师列表失败')
  } finally {
    loadingList.value = false
  }
}
const handleFilter = () => {
  fetchTeacherList()
}
const goToTeacherDetail = (id) => {
  router.push(`/teachers/${id}`)
}
onMounted(() => {
  fetchRecommendedTeachers()
  fetchTeacherList()
})
</script>

<style scoped>
.home-container {
  padding: 20px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  box-sizing: border-box;
}
.welcome-card,
.search-card,
.recommended-teachers-card,
.teacher-list-card {
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.welcome-card {
  text-align: center;
  padding: 40px;
}
.welcome-card h1 {
  margin-bottom: 20px;
  color: #409eff;
  font-size: 2.5em;
}
.welcome-card p {
  font-size: 1.2em;
  color: #606266;
  margin-bottom: 20px;
}
.feature-list {
   display: flex;
   justify-content: center;
   gap: 20px;
   flex-wrap: wrap;
}
.search-card .el-card__body {
    padding: 20px;
}
.search-input-container {
   display: flex;
   align-items: center;
   max-width: 800px;
   margin: 0 auto;
   gap: 10px;
}
.search-input {
   flex-grow: 1;
}
.recommended-teachers-card .el-card__header {
   padding: 10px 20px;
}
.recommended-teachers-list {
   padding-bottom: 10px;
}
.scrollbar-flex-content {
   display: flex;
   gap: 20px;
}
.recommended-teachers-list .teacher-card {
   width: 300px;
   flex-shrink: 0;
   cursor: pointer;
   transition: transform 0.3s ease;
}
.recommended-teachers-list .teacher-card:hover {
   transform: translateY(-5px);
}
.teacher-card-header {
   display: flex;
   align-items: center;
}
.teacher-info {
   margin-left: 15px;
}
.teacher-info h3 {
   margin: 0 0 5px 0;
   font-size: 1.1em;
   color: #303133;
}
.teacher-info p {
   margin: 0;
   font-size: 0.9em;
   color: #606266;
}
.recommended-teachers-list .teacher-card .el-card__body {
   padding-top: 0;
   font-size: 0.9em;
   color: #606266;
}
.teacher-list-card .el-card__header {
   padding: 10px 20px;
}
.card-header {
   display: flex;
   justify-content: space-between;
   align-items: center;
}
.card-header span {
   font-size: 1.2em;
   font-weight: bold;
   color: #303133;
}
.filter-options .el-select {
   margin-left: 10px;
}
.teacher-grid {
   margin: 0 -10px;
}
.teacher-grid .el-col {
   padding-left: 10px !important;
   padding-right: 10px !important;
   margin-bottom: 20px;
}
.teacher-card-grid {
   cursor: pointer;
   height: 100%;
   transition: transform 0.3s ease;
}
.teacher-card-grid:hover {
    transform: translateY(-5px);
}
.teacher-card-grid .el-card__body {
   padding: 15px;
}
.teacher-card-content {
   display: flex;
   align-items: center;
}
.teacher-avatar-grid {
   flex-shrink: 0;
   margin-right: 15px;
}
.teacher-details-grid h3 {
   margin: 0 0 5px 0;
   font-size: 1em;
   color: #303133;
}
.teacher-details-grid p {
   margin: 0 0 3px 0;
   font-size: 0.8em;
   color: #606266;
}
@media (max-width: 1200px) {
  .teacher-grid .el-col {
    flex: 0 0 33.3333%;
    max-width: 33.3333%;
  }
}
@media (max-width: 992px) {
  .teacher-grid .el-col {
    flex: 0 0 50%;
    max-width: 50%;
  }
}
@media (max-width: 768px) {
  .home-container {
    padding: 10px;
  }
  .welcome-card {
    padding: 20px;
  }
  .welcome-card h1 {
    font-size: 2em;
  }
   .feature-list {
      gap: 10px;
   }
  .search-input-container {
     flex-direction: column;
     align-items: stretch;
  }
  .search-input .el-input-group__append {
     width: auto !important;
  }
   .recommended-teachers-list .teacher-card {
      width: 250px;
   }
  .teacher-grid .el-col {
    flex: 0 0 100%;
    max-width: 100%;
  }
}
</style> 