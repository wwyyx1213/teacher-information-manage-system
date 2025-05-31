<template>
  <div class="teacher-search">
    <el-card class="search-card">
      <div class="search-header">
        <h2>搜索教师</h2>
      </div>
      <el-form :model="searchForm" class="search-form">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="姓名">
              <el-input v-model="searchForm.name" placeholder="请输入教师姓名" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="院系">
              <el-select v-model="searchForm.department" placeholder="请选择院系" clearable>
                <el-option v-for="dept in departments" :key="dept" :label="dept" :value="dept" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="职称">
              <el-select v-model="searchForm.title" placeholder="请选择职称" clearable>
                <el-option v-for="title in titles" :key="title" :label="title" :value="title" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="研究方向">
              <el-select v-model="searchForm.research_areas" placeholder="请选择研究方向" clearable filterable>
                <el-option v-for="area in researchAreas" :key="area" :label="area" :value="area" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item>
          <el-button type="primary" @click="handleSearch" :loading="loading">搜索</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <div class="search-results" v-if="teachers.length > 0">
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
    </div>

    <el-empty v-else-if="!loading" description="暂无搜索结果" />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const teachers = ref([])

const searchForm = reactive({
  name: '',
  department: '',
  title: '',
  research_areas: ''
})

const departments = ref(['计算机学院', '数学学院', '物理学院', '化学学院'])
const titles = ref(['教授', '副教授', '讲师', '助教'])
const researchAreas = ref(['人工智能', '大数据', '软件工程', '应用数学', '理论物理', '有机化学'])

const handleSearch = async () => {
  try {
    loading.value = true
    const params = {}
    Object.keys(searchForm).forEach(key => {
      if (searchForm[key]) {
        params[key] = searchForm[key]
      }
    })
    
    const response = await api.get('/search/teachers/', { params })
    teachers.value = response.results
  } catch (error) {
    ElMessage.error('搜索失败：' + (error.response?.data?.message || error.message))
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  teachers.value = []
}

const viewTeacherDetail = (teacherId) => {
  router.push(`/teachers/${teacherId}`)
}
</script>

<style scoped>
.teacher-search {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.search-header {
  margin-bottom: 20px;
  text-align: center;
}

.search-header h2 {
  margin: 0;
  color: #303133;
}

.search-form {
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
</style> 