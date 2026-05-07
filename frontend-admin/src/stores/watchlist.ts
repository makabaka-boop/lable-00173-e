import { defineStore } from 'pinia'
import { ref } from 'vue'
import { watchlistAPI } from '@/utils/api'
import type { WatchlistItem } from '@/types'

export const useWatchlistStore = defineStore('watchlist', () => {
  const items = ref<WatchlistItem[]>([])
  const loading = ref(false)

  const fetchList = async () => {
    loading.value = true
    try {
      const response: any = await watchlistAPI.getList()
      if (response.code === 200) {
        items.value = response.data
      }
    } finally {
      loading.value = false
    }
  }

  const addItem = async (code: string, name: string, note?: string) => {
    try {
      const response: any = await watchlistAPI.addItem(code, name, note)
      if (response.code === 200 || response.code === 201) {
        await fetchList()
        return { success: true }
      }
      return { success: false, message: response.message || '加入自选失败' }
    } catch (error: any) {
      const msg = error?.response?.data?.message || '加入自选失败'
      return { success: false, message: msg }
    }
  }

  const deleteItem = async (itemId: number) => {
    const response: any = await watchlistAPI.deleteItem(itemId)
    if (response.code === 200) {
      items.value = items.value.filter(i => i.id !== itemId)
      return true
    }
    return false
  }

  const updateNote = async (itemId: number, note: string) => {
    const response: any = await watchlistAPI.updateNote(itemId, note)
    if (response.code === 200) {
      const idx = items.value.findIndex(i => i.id === itemId)
      if (idx !== -1) {
        items.value[idx] = response.data
      }
      return true
    }
    return false
  }

  const reorder = async (itemIds: number[]) => {
    const response: any = await watchlistAPI.reorder(itemIds)
    if (response.code === 200) {
      await fetchList()
      return true
    }
    return false
  }

  const isInWatchlist = (code: string) => {
    return items.value.some(i => i.code === code)
  }

  return {
    items,
    loading,
    fetchList,
    addItem,
    deleteItem,
    updateNote,
    reorder,
    isInWatchlist,
  }
})
