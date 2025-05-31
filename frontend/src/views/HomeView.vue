<script setup>
// 组件逻辑，后续实现具体功能
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Search, ArrowRight } from '@element-plus/icons-vue'; // 导入 Element Plus 图标
import { useUserStore } from '@/stores/user' // 假设你的 Pinia 用户 store 路径

const userStore = useUserStore()
const router = useRouter()

// 搜索相关的响应式数据和方法（占位符）
const searchQuery = ref('');
const searchCondition = ref('name'); // 默认按姓名搜索
const searchConditions = [
  { label: '姓名', value: 'name' },
  { label: '专业', value: 'major' },
  { label: '职称', value: 'title' },
  { label: '研究方向', value: 'research_areas' },
];

const handleSearch = () => {
  console.log('Searching for:', searchQuery.value, 'by', searchCondition.value);
  // TODO: Implement actual search logic and navigation
};

// 推荐教师数据（占位符）
const recommendedTeachers = ref([
  { id: 1, name: '推荐教师 A', major: '计算机科学', reason: '该教师在人工智能领域有丰富经验', avatar: 'https://via.placeholder.com/60' },
  { id: 2, name: '推荐教师 B', major: '软件工程', reason: '活跃于开源社区', avatar: 'https://via.placeholder.com/60' },
  { id: 3, name: '推荐教师 C', major: '网络安全', reason: '有多个国家级项目', avatar: 'https://via.placeholder.com/60' },
   { id: 4, name: '推荐教师 D', major: '数据科学', reason: '发表多篇顶会论文', avatar: 'https://via.placeholder.com/60' },
]);

// 教师列表数据（占位符）
const teacherList = ref([
  { id: 101, name: '教师 01', gender: '男', major: '计算机科学', title: '教授', contact: '...', avatar: 'https://via.placeholder.com/80' },
  { id: 102, name: '教师 02', gender: '女', major: '软件工程', title: '副教授', contact: '...', avatar: 'https://via.placeholder.com/80' },
  { id: 103, name: '教师 03', gender: '男', major: '网络安全', title: '讲师', contact: '...', avatar: 'https://via.placeholder.com/80' },
  { id: 104, name: '教师 04', gender: '女', major: '数据科学', title: '教授', contact: '...', avatar: 'https://via.placeholder.com/80' },
   { id: 105, name: '教师 05', gender: '男', major: '计算机科学', title: '副教授', contact: '...', avatar: 'https://via.placeholder.com/80' },
  { id: 106, name: '教师 06', gender: '女', major: '软件工程', title: '讲师', contact: '...', avatar: 'https://via.placeholder.com/80' },
  { id: 107, name: '教师 07', gender: '男', major: '网络安全', title: '教授', contact: '...', avatar: 'https://via.placeholder.com/80' },
  { id: 108, name: '教师 08', gender: '女', major: '数据科学', title: '副教授', contact: '...', avatar: 'https://via.placeholder.com/80' },
]);

// 教师列表筛选条件（占位符）
const filterMajor = ref('');
const filterTitle = ref('');
const majors = ref(['计算机科学', '软件工程', '网络安全', '数据科学']); // 示例专业列表
const titles = ref(['教授', '副教授', '讲师']); // 示例职称列表

const handleFilter = () => {
  console.log('Filtering by:', filterMajor.value, filterTitle.value);
  // TODO: Implement actual filtering logic
};

// 跳转到教师详情页（占位符）
const goToTeacherDetail = (teacherId) => {
  console.log('Navigate to teacher detail:', teacherId);
  // TODO: Implement actual navigation
};

// 退出登录方法（占位符）
const handleLogout = () => {
  localStorage.removeItem('token')
  userStore.logout && userStore.logout() // 如果有 logout 方法
  router.push('/login')
};
</script>

<template>
  <div class="home-container">
    <!-- 右上角用户信息和退出按钮 -->
    <div class="user-info-bar">
      <span class="username">当前用户：{{ userStore.currentUser?.username || '未登录' }}</span>
      <el-button type="danger" @click="handleLogout" size="small">退出登录</el-button>
    </div>
    <!-- 欢迎区域 -->
    <el-card class="welcome-card">
      <h1>欢迎使用教师信息管理系统</h1>
      <p>在这里，您可以：</p>
      <div class="feature-list">
         <el-button round>浏览教师信息</el-button>
         <el-button round>查看教师日程</el-button>
         <el-button round>预约教师</el-button>
         <el-button round>查看科研成果</el-button>
      </div>
    </el-card>

    <!-- 搜索区域 -->
    <el-card class="search-card">
       <div class="search-input-container">
          <el-input v-model="searchQuery" placeholder="搜索教师" class="search-input">
             <template #prepend>搜索教师</template>
             <template #append>
                <el-select v-model="searchCondition" placeholder="条件" style="width: 100px">
                   <el-option v-for="condition in searchConditions" :key="condition.value" :label="condition.label" :value="condition.value"></el-option>
                </el-select>
             </template>
          </el-input>
          <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
       </div>
    </el-card>

    <!-- 推荐教师区域 -->
    <el-card class="recommended-teachers-card">
      <template #header>
        <div class="card-header">
          <span>推荐教师</span>
          <el-button type="text" @click="$router.push('/recommendations')">查看更多<el-icon class="el-icon--right"><ArrowRight /></el-icon></el-button>
        </div>
      </template>
      <div class="recommended-teachers-list">
        <el-scrollbar>
          <div class="scrollbar-flex-content">
            <el-card v-for="teacher in recommendedTeachers" :key="teacher.id" class="teacher-card" shadow="hover" @click="goToTeacherDetail(teacher.id)">
              <template #header>
                 <div class="teacher-card-header">
                    <el-avatar :size="60" :src="teacher.avatar" />
                    <div class="teacher-info">
                       <h3>{{ teacher.name }}</h3>
                       <p>{{ teacher.major }}</p>
                    </div>
                 </div>
              </template>
              <p>{{ teacher.reason }}</p>
            </el-card>
             <!-- Add more placeholder cards if needed to test scrolling -->
          </div>
        </el-scrollbar>
      </div>
       <el-empty v-if="recommendedTeachers.length === 0" description="暂无推荐教师" />
    </el-card>

    <!-- 教师列表区域 -->
    <el-card class="teacher-list-card">
       <template #header>
          <div class="card-header">
             <span>教师列表</span>
             <div class="filter-options">
                <el-select v-model="filterMajor" placeholder="按专业筛选" clearable @change="handleFilter" style="width: 120px; margin-right: 10px;">
                   <el-option v-for="major in majors" :key="major" :label="major" :value="major"></el-option>
                </el-select>
                 <el-select v-model="filterTitle" placeholder="按职称筛选" clearable @change="handleFilter" style="width: 120px;">
                   <el-option v-for="title in titles" :key="title" :label="title" :value="title"></el-option>
                </el-select>
             </div>
          </div>
       </template>
       <el-row :gutter="20" class="teacher-grid">
          <el-col :span="6" v-for="teacher in teacherList" :key="teacher.id">
             <el-card class="teacher-card-grid" shadow="hover" @click="goToTeacherDetail(teacher.id)">
                <div class="teacher-card-content">
                   <el-avatar :size="50" :src="teacher.avatar" class="teacher-avatar-grid" />
                   <div class="teacher-details-grid">
                      <h3>{{ teacher.name }}</h3>
                      <p>专业: {{ teacher.major }}</p>
                      <p>职称: {{ teacher.title }}</p>
                   </div>
                </div>
             </el-card>
          </el-col>
       </el-row>
        <el-empty v-if="teacherList.length === 0" description="暂无教师数据" />
    </el-card>

  </div>
</template>

<style scoped>
.home-container {
  padding: 20px; /* 为主内容区域添加内边距 */
  width: 100%; /* 确保宽度为100% */
  max-width: 1200px; /* 设置最大宽度 */
  margin: 0 auto; /* 内容居中 */
  box-sizing: border-box;
}

.welcome-card,
.search-card,
.recommended-teachers-card,
.teacher-list-card {
  margin-bottom: 20px; /* 卡片之间间隔 */
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/* 欢迎区域样式 */
.welcome-card {
  text-align: center;
  padding: 40px;
}

.welcome-card h1 {
  margin-bottom: 20px;
  color: #409eff;
  font-size: 2.5em;
}

.welcome-card p {
  font-size: 1.2em;
  color: #606266;
  margin-bottom: 20px;
}

.feature-list {
   display: flex;
   justify-content: center;
   gap: 20px; /* 按钮之间的间隔 */
   flex-wrap: wrap; /* 允许换行 */
}

/* 搜索区域样式 */
.search-card .el-card__body {
    padding: 20px;
}

.search-input-container {
   display: flex;
   align-items: center;
   max-width: 800px; /* 限制搜索框最大宽度 */
   margin: 0 auto;
   gap: 10px;
}

.search-input {
   flex-grow: 1;
}

/* 推荐教师区域样式 */
.recommended-teachers-card .el-card__header {
   padding: 10px 20px;
}

.recommended-teachers-list {
   /* overflow-x: auto; /* 允许横向滚动 */
   /* white-space: nowrap; /* 防止卡片换行 */
   padding-bottom: 10px; /* 避免滚动条遮挡 */
}

.scrollbar-flex-content {
   display: flex;
   gap: 20px;
}

.recommended-teachers-list .teacher-card {
   width: 300px; /* 设置卡片宽度 */
   flex-shrink: 0; /* 防止卡片缩小 */
   cursor: pointer;
   transition: transform 0.3s ease;
}

.recommended-teachers-list .teacher-card:hover {
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

.recommended-teachers-list .teacher-card .el-card__body {
   padding-top: 0;
   font-size: 0.9em;
   color: #606266;
}

/* 教师列表区域样式 */
.teacher-list-card .el-card__header {
   padding: 10px 20px;
}

.card-header {
   display: flex;
   justify-content: space-between;
   align-items: center;
}

.card-header span {
   font-size: 1.2em;
   font-weight: bold;
   color: #303133;
}

.filter-options .el-select {
   margin-left: 10px; /* 筛选条件之间的间隔 */
}

.teacher-grid {
   margin: 0 -10px; /* 抵消el-row的负外边距，确保左右对齐 */
}

.teacher-grid .el-col {
   padding-left: 10px !important; /* 调整el-col的内边距 */
   padding-right: 10px !important;
   margin-bottom: 20px; /* 行之间的间隔 */
}

.teacher-card-grid {
   cursor: pointer;
   height: 100%; /* 确保卡片等高 */
   transition: transform 0.3s ease;
}

.teacher-card-grid:hover {
    transform: translateY(-5px);
}

.teacher-card-grid .el-card__body {
   padding: 15px; /* 调整内边距 */
}

.teacher-card-content {
   display: flex;
   align-items: center;
}

.teacher-avatar-grid {
   flex-shrink: 0;
   margin-right: 15px;
}

.teacher-details-grid h3 {
   margin: 0 0 5px 0;
   font-size: 1em;
   color: #303133;
}

.teacher-details-grid p {
   margin: 0 0 3px 0;
   font-size: 0.8em;
   color: #606266;
}

/* 右上角用户信息栏样式 */
.user-info-bar {
  position: absolute;
  top: 20px;
  right: 40px;
  display: flex;
  align-items: center;
  gap: 16px;
  z-index: 10;
}

.username {
  font-size: 15px;
  color: #409eff;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .teacher-grid .el-col {
    flex: 0 0 33.3333%; /* 1200px 以下，每行3个 */
    max-width: 33.3333%;
  }
}

@media (max-width: 992px) {
  .teacher-grid .el-col {
    flex: 0 0 50%; /* 992px 以下，每行2个 */
    max-width: 50%;
  }
}

@media (max-width: 768px) {
  .home-container {
    padding: 10px; /* 减小移动端内边距 */
  }
  .welcome-card {
    padding: 20px;
  }
  .welcome-card h1 {
    font-size: 2em;
  }
   .feature-list {
      gap: 10px;
   }
  .search-input-container {
     flex-direction: column;
     align-items: stretch;
  }
  .search-input .el-input-group__append {
     width: auto !important; /* 确保下拉框宽度自适应 */
  }
   .recommended-teachers-list .teacher-card {
      width: 250px; /* 调整移动端卡片宽度 */
   }
  .teacher-grid .el-col {
    flex: 0 0 100%; /* 768px 以下，每行1个 */
    max-width: 100%;
  }
}
</style>
