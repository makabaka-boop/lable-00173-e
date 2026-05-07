import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Stock, KlineData } from '@/types'

export const useMarketStore = defineStore('market', () => {
  const stocks = ref<Stock[]>([])
  const selectedStock = ref<Stock | null>(null)
  const klineData = ref<KlineData[]>([])
  const loading = ref(false)

  return {
    stocks,
    selectedStock,
    klineData,
    loading,
    setStocks: (data: Stock[]) => { stocks.value = data },
    setSelectedStock: (stock: Stock | null) => { selectedStock.value = stock },
    setKlineData: (data: KlineData[]) => { klineData.value = data },
    updateStock: (code: string, updates: Partial<Stock>) => {
      const stock = stocks.value.find(s => s.code === code)
      if (stock) Object.assign(stock, updates)
    },
  }
})
