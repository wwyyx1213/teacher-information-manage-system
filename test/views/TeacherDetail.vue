<template>
  <div>
    <el-card v-if="teacher">
      <h2>{{ teacher.user.username }}（{{ teacher.title }}）</h2>
      <p><b>院系：</b>{{ teacher.department }}</p>
      <p><b>研究方向：</b>{{ teacher.research_direction }}</p>
      <p><b>简介：</b>{{ teacher.introduction }}</p>
      <el-divider>科研项目</el-divider>
      <ul>
        <li v-for="p in teacher.projects" :key="p.id">{{ p.title }}（{{ p.funding_source }}）</li>
      </ul>
      <el-divider>发表论文</el-divider>
      <ul>
        <li v-for="pub in teacher.publications" :key="pub.id">{{ pub.title }}（{{ pub.journal }}，{{ pub.publication_date }}）</li>
      </ul>
      <el-button type="success" @click="goAppointment">预约导师</el-button>
    </el-card>
  </div>
</template>

<script>
import request from '../utils/request'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  setup() {
    const teacher = ref(null)
    const route = useRoute()
    const router = useRouter()

    const fetchTeacher = async () => {
      const res = await request.get(`teachers/${route.params.id}/`)
      teacher.value = res.data
    }

    const goAppointment = () => {
      router.push({ path: '/appointment', query: { teacher: route.params.id } })
    }

    onMounted(fetchTeacher)

    return { teacher, goAppointment }
  }
}
</script>
