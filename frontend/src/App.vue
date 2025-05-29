<script setup>
import NavBar from '@/components/NavBar.vue'
</script>

<template>
  <div class="app-container">
    <NavBar class="navbar-fixed" />
    <div class="main-content">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.navbar-fixed {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
}
.main-content {
  margin-top: 60px; /* 根据NavBar实际高度调整 */
  padding: 16px;
}
</style>
