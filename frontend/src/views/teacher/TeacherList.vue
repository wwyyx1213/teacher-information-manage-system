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