<template>
  <div class="teacher-list">
    <div class="page-header">
      <h1>教师列表</h1>
    </div>

    <!-- 搜索区域 -->
    <teacher-search />

    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="院系">
          <el-select v-model="filterForm.department" placeholder="选择院系" clearable>
            <el-option
              v-for="dept in departments"
              :key="dept"
              :label="dept"
              :value="dept"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="职称">
          <el-select v-model="filterForm.title" placeholder="选择职称" clearable>
            <el-option
              v-for="title in titles"
              :key="title"
              :label="title"
              :value="title"
            />
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
import { useRouter } from 'vue-router'
import TeacherSearch from '../../components/TeacherSearch.vue'
import api from '../../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const teachers = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)

// 筛选表单
const filterForm = reactive({
  department: '',
  title: ''
})

// 模拟数据，实际应从后端获取
const departments = ref(['计算机学院', '数学学院', '物理学院', '化学学院'])
const titles = ref(['教授', '副教授', '讲师', '助教'])

// 获取教师列表
const fetchTeachers = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      ...filterForm
    }
    
    const response = await api.get('/teachers/', { params })
    teachers.value = response.results
    total.value = response.count
  } catch (error) {
    ElMessage.error('获取教师列表失败：' + (error.response?.data?.message || error.message))
  } finally {
    loading.value = false
  }
}

// 处理筛选
const handleFilter = () => {
  currentPage.value = 1
  fetchTeachers()
}

// 重置筛选
const resetFilter = () => {
  filterForm.department = ''
  filterForm.title = ''
  handleFilter()
}

// 处理分页
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchTeachers()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchTeachers()
}

// 查看教师详情
const viewTeacherDetail = (teacherId) => {
  router.push(`/teachers/${teacherId}`)
}

onMounted(() => {
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