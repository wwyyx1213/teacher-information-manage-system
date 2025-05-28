<template>
  <div class="p-6 max-w-6xl mx-auto">
    <!-- 系统简介 -->
    <section class="mb-10">
      <h1 class="text-3xl font-bold mb-4">欢迎使用教师信息管理系统</h1>
      <p class="text-gray-700 text-lg">
        本系统用于管理教师的基本信息、课程安排、预约与评价等功能，提升教务管理效率。
      </p>
    </section>

    <!-- 推荐教师 -->
    <section>
      <h2 class="text-2xl font-semibold mb-4">推荐教师</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <div v-for="teacher in teachers" :key="teacher.id" class="p-4 bg-white rounded-2xl shadow hover:shadow-md transition">
          <h3 class="text-xl font-bold mb-2">{{ teacher.name }}</h3>
          <p class="text-gray-600">专业：{{ teacher.subject }}</p>
          <p class="text-gray-600">教学经验：{{ teacher.experience }} 年</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      teachers: [
        { id: 1, name: '张老师', subject: '数学', experience: 8 },
        { id: 2, name: '李老师', subject: '英语', experience: 5 },
        { id: 3, name: '王老师', subject: '计算机', experience: 10 },
      ],
    };
  },
};
</script>

<style scoped>
</style>
