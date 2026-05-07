import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Login from '@/views/Login.vue'
import Market from '@/views/Market.vue'
import Trading from '@/views/Trading.vue'
import Positions from '@/views/Positions.vue'
import Backtest from '@/views/Backtest.vue'
import Profile from '@/views/Profile.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    redirect: '/market',
  },
  {
    path: '/market',
    name: 'Market',
    component: Market,
    meta: { requiresAuth: true },
  },
  {
    path: '/trading',
    name: 'Trading',
    component: Trading,
    meta: { requiresAuth: true },
  },
  {
    path: '/positions',
    name: 'Positions',
    component: Positions,
    meta: { requiresAuth: true },
  },
  {
    path: '/backtest',
    name: 'Backtest',
    component: Backtest,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isAuthenticated = userStore.isLoggedIn

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    next('/market')
  } else {
    next()
  }
})

export default router
