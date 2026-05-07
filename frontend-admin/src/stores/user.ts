import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, AccountStats, Position } from '@/types'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const accountStats = ref<AccountStats | null>(null)
  const positions = ref<Position[]>([])
  const loading = ref(false)

  // 初始化时从 localStorage 恢复用户信息
  const initializeUser = () => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      try {
        user.value = JSON.parse(savedUser)
      } catch (e) {
        console.error('Failed to parse saved user:', e)
      }
    }
  }

  const isLoggedIn = computed(() => !!user.value)

  return {
    user,
    accountStats,
    positions,
    loading,
    isLoggedIn,
    initializeUser,
    setUser: (userData: User) => { 
      user.value = userData
      localStorage.setItem('user', JSON.stringify(userData))
    },
    setAccountStats: (stats: AccountStats) => { accountStats.value = stats },
    setPositions: (pos: Position[]) => { positions.value = pos },
    updateBalance: (amount: number) => { if (user.value) user.value.balance = amount },
    logout: () => { 
      user.value = null
      accountStats.value = null
      positions.value = []
      localStorage.removeItem('user')
      localStorage.removeItem('userId')
      localStorage.removeItem('token')
    },
  }
})
