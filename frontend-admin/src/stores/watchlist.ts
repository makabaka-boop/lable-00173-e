import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { WatchlistItem } from '@/types'

export const useWatchlistStore = defineStore('watchlist', () => {
  const items = ref<WatchlistItem[]>([])
  const loading = ref(false)

  const setItems = (data: WatchlistItem[]) => {
    items.value = data
  }

  const addItem = (item: WatchlistItem) => {
    items.value.push(item)
  }

  const removeItem = (itemId: number) => {
    const index = items.value.findIndex(i => i.id === itemId)
    if (index !== -1) {
      items.value.splice(index, 1)
    }
  }

  const updateItem = (itemId: number, updates: Partial<WatchlistItem>) => {
    const item = items.value.find(i => i.id === itemId)
    if (item) {
      Object.assign(item, updates)
    }
  }

  const reorder = (orders: { id: number; sortOrder: number }[]) => {
    const itemMap = new Map(items.value.map(i => [i.id, i]))
    for (const order of orders) {
      const item = itemMap.get(order.id)
      if (item) {
        item.sortOrder = order.sortOrder
      }
    }
    items.value.sort((a, b) => a.sortOrder - b.sortOrder)
  }

  const hasCode = (code: string) => {
    return items.value.some(i => i.code === code)
  }

  const getItemByCode = (code: string) => {
    return items.value.find(i => i.code === code)
  }

  return {
    items,
    loading,
    setItems,
    addItem,
    removeItem,
    updateItem,
    reorder,
    hasCode,
    getItemByCode,
  }
})
