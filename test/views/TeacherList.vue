<template>
  <div>
    <el-card>
      <div style="margin-bottom: 20px;">
        <el-input
          v-model="search"
          placeholder="搜索教师姓名/方向/院系"
          style="width: 300px"
          @input="fetchTeachers"
        />
      </div>
      <el-table :data="teachers" style="width: 100%">
        <el-table-column prop="user.username" label="姓名" />
        <el-table-column prop="title" label="职称" />
        <el-table-column prop="department" label="院系" />
        <el-table-column prop="research_direction" label="研究方向" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" @click="goDetail(scope.row.id)" size="small">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import request from '../utils/request'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const teachers = ref([])
    const search = ref('')
    const router = useRouter()

    const fetchTeachers = async () => {
      const res = await request.get('teachers/', {
        params: search.value ? { search: search.value } : {}
      })
      teachers.value = res.data
    }

    const goDetail = (id) => {
      router.push(`/teacher/${id}`)
    }

    onMounted(fetchTeachers)

    return { teachers, search, fetchTeachers, goDetail }
  }
}
</script>
