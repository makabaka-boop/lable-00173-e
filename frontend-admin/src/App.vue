<template>
  <div class="app">
    <template v-if="isLoginPage">
      <router-view />
    </template>
    <template v-else>
      <Sidebar />
      <div class="main-wrapper">
        <Header />
        <main class="main-content">
          <router-view />
        </main>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'

const route = useRoute()
const userStore = useUserStore()

const isLoginPage = computed(() => {
  return route.path === '/login'
})

onMounted(() => {
  // 初始化用户信息
  userStore.initializeUser()
})
</script>

<style scoped lang="scss">
.app {
  width: 100%;
  height: 100vh;
  display: flex;
  background: var(--el-fill-color-light);
}

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 240px;
  transition: margin-left 0.3s ease;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

@media (max-width: 768px) {
  .main-wrapper {
    margin-left: 80px;
  }
}
</style>
