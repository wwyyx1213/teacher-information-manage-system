<template>
  <div class="teacher-list-container">
    <el-card class="teacher-list-card">
      <template #header>
        <div class="card-header">
          <span>全部教师</span>
        </div>
      </template>
      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="请输入姓名、专业、职称、研究方向等标签"
          clearable
          style="width: 320px; margin-bottom: 20px;"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="handleSearch" style="margin-left: 10px;">搜索</el-button>
        <el-button @click="resetSearch" style="margin-left: 10px;">重置</el-button>
      </div>
      <div class="teacher-list-content">
        <el-scrollbar>
          <div class="scrollbar-flex-content">
            <el-card
              v-for="teacher in teacherList"
              :key="teacher.id"
              class="teacher-card"
              shadow="hover"
              @click="goToTeacherDetail(teacher.id)"
            >
              <template #header>
                <div class="teacher-card-header">
                  <el-avatar :size="60" :src="teacher.avatar" />
                  <div class="teacher-info">
                    <h3>{{ teacher.name }}</h3>
                    <p>{{ teacher.major }}</p>
                  </div>
                </div>
              </template>
              <p>{{ teacher.bio }}</p>
            </el-card>
          </div>
        </el-scrollbar>
      </div>
      <el-empty v-if="teacherList.length === 0" description="暂无教师数据" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import teacherApi from '../../api/teacher'

const router = useRouter()
const teacherList = ref([])
const searchKeyword = ref('')

// 获取所有教师
const fetchAllTeachers = async () => {
  try {
    const res = await teacherApi.getAllTeachers()
    teacherList.value = res
  } catch (e) {
    ElMessage.error('获取教师列表失败')
  }
}

// 搜索教师
const handleSearch = async () => {
  if (!searchKeyword.value.trim()) {
    fetchAllTeachers()
    return
  }
  try {
    // 假设后端支持标签搜索接口 /teachers/search/?q=xxx
    const res = await teacherApi.searchTeachers(searchKeyword.value.trim())
    teacherList.value = res
  } catch (e) {
    ElMessage.error('搜索失败')
  }
}

// 重置搜索
const resetSearch = () => {
  searchKeyword.value = ''
  fetchAllTeachers()
}

const goToTeacherDetail = (teacherId) => {
  router.push(`/teachers/${teacherId}`)
}

onMounted(fetchAllTeachers)
</script>

<style scoped>
.teacher-list-container {
  padding: 40px;
}
.teacher-list-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.card-header {
  display: flex;
  align-items: center;
  font-size: 1.2em;
  font-weight: bold;
  color: #303133;
}
.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.teacher-list-content {
  padding-bottom: 10px;
}
.scrollbar-flex-content {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}
.teacher-card {
  width: 300px;
  flex-shrink: 0;
  cursor: pointer;
  transition: transform 0.3s ease;
}
.teacher-card:hover {
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
.teacher-card .el-card__body {
  padding-top: 0;
  font-size: 0.9em;
  color: #606266;
}
</style>