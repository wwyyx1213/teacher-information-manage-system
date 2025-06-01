<template>
  <div class="teacher-list">
    <div class="page-header">
      <h1>教师列表</h1>
    </div>

    <!-- 多维度筛选条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="姓名">
          <el-input v-model="filterForm.name" placeholder="输入姓名" clearable />
        </el-form-item>
        <el-form-item label="院系">
          <el-select v-model="filterForm.department" placeholder="选择院系" clearable filterable>
            <el-option v-for="dept in departments" :key="dept" :label="dept" :value="dept" />
          </el-select>
        </el-form-item>
        <el-form-item label="职称">
          <el-select v-model="filterForm.title" placeholder="选择职称" clearable>
            <el-option v-for="title in titles" :key="title" :label="title" :value="title" />
          </el-select>
        </el-form-item>
        <el-form-item label="研究方向">
          <el-select v-model="filterForm.research_areas" placeholder="选择研究方向" clearable filterable>
            <el-option v-for="area in researchAreas" :key="area" :label="area" :value="area" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">筛选</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 教师列表 -->
    <div class="teacher-grid" v-loading="loading">
      <el-row :gutter="20">
        <el-col :span="6" v-for="teacher in teachers" :key="teacher.id">
          <el-card class="teacher-card" :body-style="{ padding: '0px' }">
            <div class="teacher-avatar">
              <el-avatar :size="100" :src="teacher.avatar_url || '/default-avatar.png'" />
            </div>
            <div class="teacher-info">
              <h3>{{ teacher.name }}</h3>
              <p class="department">{{ teacher.department }}</p>
              <p class="title">{{ teacher.title }}</p>
              <p class="research">{{ teacher.research_areas }}</p>
              <el-button type="primary" link @click="viewTeacherDetail(teacher.id)">
                查看详情
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[12, 24, 36, 48]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const teachers = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)

// 筛选表单
const filterForm = reactive({
  name: '',
  department: '',
  title: '',
  research_areas: ''
})

const departments = ref([])
const titles = ref([])
const researchAreas = ref([])

// 获取教师列表
const fetchTeachers = async () => {
  try {
    loading.value = true
    // 只传递有值的参数，研究方向用模糊匹配
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    Object.keys(filterForm).forEach(key => {
      if (filterForm[key]) {
        // 研究方向用 research_areas 参数，后端应支持 icontains
        params[key] = filterForm[key]
      }
    })
    const response = await api.get('/teachers/', { params })
    teachers.value = response.results || response
    total.value = response.count || teachers.value.length
    // 自动收集院系、职称、研究方向（去重、非空）
    departments.value = [...new Set((response.results || response).map(t => t.department).filter(Boolean))]
    // 职称自动收集所有实际存在的职称
    titles.value = [...new Set((response.results || response).map(t => t.title).filter(Boolean))]
    researchAreas.value = [...new Set((response.results || response).flatMap(t => (t.research_areas ? t.research_areas.split(/[，,;；\s]+/) : [])).filter(Boolean))]
  } catch (error) {
    ElMessage.error('获取教师列表失败：' + (error.response?.data?.message || error.message))
  } finally {
    loading.value = false
  }
}

const updateUrlQuery = () => {
  const query = {}
  Object.keys(filterForm).forEach(key => {
    if (filterForm[key]) query[key] = filterForm[key]
  })
  if (currentPage.value !== 1) query.page = currentPage.value
  if (pageSize.value !== 12) query.page_size = pageSize.value
  router.replace({ path: '/teachers', query })
}

const handleFilter = () => {
  currentPage.value = 1
  updateUrlQuery()
  fetchTeachers()
}

const resetFilter = () => {
  filterForm.name = ''
  filterForm.department = ''
  filterForm.title = ''
  filterForm.research_areas = ''
  currentPage.value = 1
  updateUrlQuery()
  fetchTeachers()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  updateUrlQuery()
  fetchTeachers()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  updateUrlQuery()
  fetchTeachers()
}

// 查看教师详情
const viewTeacherDetail = (teacherId) => {
  router.push(`/teachers/${teacherId}`)
}

// 监听路由参数（首页/其他页面跳转带参数时自动填充筛选）
onMounted(() => {
  // 如果有query参数，自动填充筛选
  const q = route.query
  if (q) {
    if (q.name) filterForm.name = q.name
    if (q.department) filterForm.department = q.department
    if (q.title) filterForm.title = q.title
    if (q.research_areas) filterForm.research_areas = q.research_areas
    if (q.page) currentPage.value = parseInt(q.page)
    if (q.page_size) pageSize.value = parseInt(q.page_size)
  }
  fetchTeachers()
})
</script>

<style scoped>
.teacher-list {
  padding: 20px;
  max-width: 1200px;
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

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-form .el-form-item {
  min-width: 180px;
  max-width: 220px;
}

.teacher-grid {
  margin-top: 20px;
}

.teacher-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.teacher-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.teacher-avatar {
  padding: 20px;
  text-align: center;
  background-color: #f5f7fa;
}

.teacher-info {
  padding: 20px;
  text-align: center;
}

.teacher-info h3 {
  margin: 0 0 10px;
  color: #303133;
}

.department, .title, .research {
  margin: 5px 0;
  color: #606266;
  font-size: 14px;
}

.research {
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style> 