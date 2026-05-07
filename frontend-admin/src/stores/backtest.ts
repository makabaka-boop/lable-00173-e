import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { BacktestResult } from '@/types'

export const useBacktestStore = defineStore('backtest', () => {
  const results = ref<BacktestResult[]>([])
  const currentResult = ref<BacktestResult | null>(null)
  const loading = ref(false)

  return {
    results,
    currentResult,
    loading,
    addResult: (result: BacktestResult) => { results.value.unshift(result) },
    setResults: (data: BacktestResult[]) => { results.value = data },
    setCurrentResult: (result: BacktestResult | null) => { currentResult.value = result },
    updateResult: (id: string | number, updates: Partial<BacktestResult>) => {
      const result = results.value.find(r => r.id === id)
      if (result) Object.assign(result, updates)
    },
    deleteResult: (id: string | number) => { results.value = results.value.filter(r => r.id !== id) },
  }
})
