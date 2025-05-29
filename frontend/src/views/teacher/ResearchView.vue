<template>
  <div class="research-view">
    <el-card>
      <h2>基金与科研成果</h2>
      <h3>基金项目</h3>
      <el-table :data="fundList" style="width: 100%; margin-bottom: 30px;">
        <el-table-column prop="name" label="项目名称" />
        <el-table-column prop="amount" label="经费（万元）" width="120" />
        <el-table-column prop="year" label="年份" width="100" />
      </el-table>
      <h3>科研成果</h3>
      <el-table :data="achievementList" style="width: 100%">
        <el-table-column prop="title" label="成果标题" />
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column prop="publish_date" label="发表/获奖日期" width="150" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

const route = useRoute()
const fundList = ref([])
const achievementList = ref([])

const loadResearch = async () => {
  try {
    const res = await api.get(`/teachers/${route.params.id}/research/`)
    fundList.value = res.data.funds || []
    achievementList.value = res.data.achievements || []
  } catch (e) {
    ElMessage.error('获取科研信息失败')
  }
}

onMounted(() => {
  loadResearch()
})
</script>

<style scoped>
.research-view {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.el-card {
  width: 700px;
}
</style>