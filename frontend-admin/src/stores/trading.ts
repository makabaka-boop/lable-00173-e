import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Order, TradeHistory } from '@/types'

export const useTradingStore = defineStore('trading', () => {
  const orders = ref<Order[]>([])
  const tradeHistory = ref<TradeHistory[]>([])
  const loading = ref(false)

  return {
    orders,
    tradeHistory,
    loading,
    addOrder: (order: Order) => { orders.value.unshift(order) },
    updateOrder: (id: string, updates: Partial<Order>) => {
      const order = orders.value.find(o => o.id === id)
      if (order) Object.assign(order, updates)
    },
    cancelOrder: (id: string) => {
      const order = orders.value.find(o => o.id === id)
      if (order) order.status = 'cancelled'
    },
    addTradeHistory: (trade: TradeHistory) => { tradeHistory.value.unshift(trade) },
    setOrders: (data: Order[]) => { orders.value = data },
    setTradeHistory: (data: TradeHistory[]) => { tradeHistory.value = data },
  }
})
