<template>
  <aside class="sidebar" :class="{ collapsed }">
    <div class="sidebar-header">
      <div v-if="!collapsed" class="logo">
        <span class="logo-icon">📈</span>
        <span class="logo-text">证券交易系统</span>
      </div>
      <button class="collapse-btn" @click="collapsed = !collapsed">
        <el-icon>
          <component :is="collapsed ? 'expand-right' : 'fold'" />
        </el-icon>
      </button>
    </div>

    <nav class="sidebar-nav">
      <router-link 
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        :class="{ active: isActive(item.path) }"
        :title="item.label"
      >
        <el-icon class="nav-icon">
          <component :is="item.icon" />
        </el-icon>
        <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  DataAnalysis, 
  ShoppingCart, 
  Briefcase, 
  Histogram,
  Fold,
  ExpandRight
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const collapsed = ref(false)

const navItems = [
  { path: '/market', label: '行情中心', icon: 'DataAnalysis' },
  { path: '/trading', label: '交易管理', icon: 'ShoppingCart' },
  { path: '/positions', label: '持仓管理', icon: 'Briefcase' },
  { path: '/backtest', label: '策略回测', icon: 'Histogram' },
]

const isActive = (path: string) => route.path === path
</script>

<style scoped lang="scss">
.sidebar {
  width: 240px;
  height: 100vh;
  background: linear-gradient(180deg, #ffffff 0%, #f5f7fa 100%);
  border-right: 1px solid var(--el-border-color-light);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 99;
  box-shadow: var(--shadow-sm);

  &.collapsed {
    width: 80px;

    .logo-text {
      display: none;
    }

    .nav-label {
      display: none;
    }

    .sidebar-header {
      justify-content: center;
    }
  }
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid var(--el-border-color-light);
  height: 64px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  background: linear-gradient(135deg, var(--el-color-primary) 0%, #0052a3 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 14px;
}

.collapse-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--el-text-color-regular);
  font-size: 18px;
  transition: all 0.3s ease;
  padding: 4px;

  &:hover {
    color: var(--el-color-primary);
  }
}

.sidebar-nav {
  flex: 1;
  padding: 16px 8px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: var(--el-text-color-regular);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: 14px;

  &:hover {
    background: var(--el-fill-color-lighter);
    color: var(--el-color-primary);
  }

  &.active {
    background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 102, 204, 0.05) 100%);
    color: var(--el-color-primary);
    font-weight: 500;
  }
}

.nav-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.nav-label {
  flex: 1;
  white-space: nowrap;
}

::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #d0d0d0;
  border-radius: 3px;

  &:hover {
    background: #999999;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 80px;

    .logo-text {
      display: none;
    }

    .nav-label {
      display: none;
    }

    .sidebar-header {
      justify-content: center;
    }
  }
}
</style>
