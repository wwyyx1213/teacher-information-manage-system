<script setup>
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <div class="home-view">
    <el-card>
      <h1>欢迎使用教师信息管理系统</h1>
      <p>您可以浏览教师信息、预约咨询、查看研究成果等。</p>
      <el-button type="primary" @click="$router.push('/teachers')">浏览教师</el-button>
    </el-card>
  </div>
</template>

<style scoped>
.home-view {
  padding: 40px;
  display: flex;
  justify-content: center;
}
</style>
