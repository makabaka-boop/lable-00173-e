<template>
  <header class="header">
    <div class="header-container">
      <div class="header-left">
        <div class="breadcrumb-wrapper">
          <span class="breadcrumb-item breadcrumb-home" @click="goToMarket">
            证券交易系统
          </span>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-item breadcrumb-current">{{ currentPageLabel }}</span>
        </div>
      </div>

      <div class="header-right">
        <el-divider direction="vertical" />
        <el-dropdown @command="handleCommand">
          <span class="user-menu">
            <el-icon><user-filled /></el-icon>
            {{ userStore.user?.name || '用户' }}
            <el-icon class="el-icon--right">
              <arrow-down />
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人资料</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { formatCurrency } from '@/utils/format'
import { ElMessage } from 'element-plus'
import { ArrowDown, UserFilled, HomeFilled } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const pageMap: Record<string, string> = {
  '/market': '行情中心',
  '/trading': '交易管理',
  '/positions': '持仓管理',
  '/backtest': '策略回测',
  '/profile': '个人资料',
}

const currentPageLabel = computed(() => {
  return pageMap[route.path] || '页面'
})

const goToMarket = () => {
  router.push('/market')
}

const handleCommand = (command: string) => {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  }
}
</script>

<style scoped lang="scss">
.header {
  background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
  border-bottom: 1px solid var(--el-border-color-light);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 98;
}

.header-container {
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  flex: 1;
}

.breadcrumb-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--el-fill-color-lighter);
  border-radius: 4px;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-regular);
  transition: all 0.3s ease;
  cursor: pointer;

  &:hover {
    color: var(--el-color-primary);
  }
}

.breadcrumb-home {
  color: var(--el-color-primary);

  &:hover {
    color: var(--el-color-primary-dark-2);
  }
}

.breadcrumb-current {
  color: var(--el-text-color-primary);
  font-weight: 600;
  cursor: default;

  &:hover {
    color: var(--el-text-color-primary);
  }
}

.breadcrumb-separator {
  color: var(--el-text-color-regular);
  font-size: 14px;
  margin: 0 4px;
}

:deep(.el-breadcrumb) {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-breadcrumb__inner) {
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-regular);
  transition: all 0.3s ease;

  &:hover {
    color: var(--el-color-primary);
    text-decoration: underline;
  }
}

:deep(.el-breadcrumb__inner.is-link) {
  cursor: pointer;
  color: var(--el-color-primary);

  &:hover {
    color: var(--el-color-primary-dark-2);
  }
}

:deep(.el-breadcrumb__separator) {
  color: var(--el-text-color-regular);
  font-size: 14px;
  margin: 0 4px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.balance {
  color: var(--el-text-color-regular);
  font-weight: 500;
  font-size: 14px;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--el-text-color-primary);
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 4px 8px;
  border-radius: 4px;

  &:hover {
    color: var(--el-color-primary);
    background: var(--el-fill-color-lighter);
  }
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 16px;
  }

  .balance {
    display: none;
  }

  :deep(.el-breadcrumb__inner) {
    font-size: 12px;
  }
}
</style>
