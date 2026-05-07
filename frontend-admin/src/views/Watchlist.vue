<template>
  <div class="watchlist-container">
    <div class="watchlist-section">
      <div class="list-header">
        <span>我的自选股 ({{ watchlistStore.items.length }}/50)</span>
        <div class="header-actions">
          <el-button 
            type="primary" 
            size="small" 
            :disabled="!hasPendingReorder"
            @click="saveReorder"
          >
            保存排序
          </el-button>
        </div>
      </div>

      <el-table 
        :data="watchlistStore.items" 
        stripe 
        style="width: 100%" 
        empty-text="暂无自选股"
        row-key="id"
      >
        <el-table-column label="排序" width="60" align="center">
          <template #default="{ $index }">
            <span class="sort-handle">
              <el-icon><Rank /></el-icon>
            </span>
            <span class="sort-num">{{ $index + 1 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="code" label="代码" min-width="100" />
        <el-table-column prop="name" label="名称" min-width="120" />
        <el-table-column label="现价" min-width="100" align="right">
          <template #default="{ row }">
            <span class="price">{{ getStockPrice(row.code) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="涨跌" min-width="100" align="right">
          <template #default="{ row }">
            <span :style="{ color: getPriceColor(row.code) }">
              {{ getStockChange(row.code) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="备注" min-width="200">
          <template #default="{ row }">
            <div v-if="editingId !== row.id" class="note-display" @click="startEdit(row)">
              <span v-if="row.note">{{ row.note }}</span>
              <span v-else class="note-placeholder">点击添加备注...</span>
            </div>
            <el-input 
              v-else
              v-model="editNoteValue"
              ref="noteInputRef"
              size="small"
              maxlength="255"
              show-word-limit
              @blur="saveNote(row)"
              @keyup.enter="saveNote(row)"
              @keyup.esc="cancelEdit"
            />
          </template>
        </el-table-column>
        <el-table-column label="添加时间" min-width="160">
          <template #default="{ row }">
            {{ formatDate(row.createdAt) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="150" align="center">
          <template #default="{ row }">
            <el-button 
              size="small" 
              :disabled="$index === 0"
              @click="moveUp($index)"
            >
              上移
            </el-button>
            <el-button 
              size="small" 
              :disabled="$index === watchlistStore.items.length - 1"
              @click="moveDown($index)"
            >
              下移
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="handleRemove(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from 'vue'
import { useWatchlistStore } from '@/stores/watchlist'
import { useMarketStore } from '@/stores/market'
import { watchlistAPI, marketAPI } from '@/utils/api'
import { formatNumber, formatPercent, getPriceColor, getPriceSymbol, formatDate } from '@/utils/format'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Rank } from '@element-plus/icons-vue'
import type { WatchlistItem, Stock } from '@/types'

const watchlistStore = useWatchlistStore()
const marketStore = useMarketStore()

const editingId = ref<number | null>(null)
const editNoteValue = ref('')
const originalSortOrders = ref<Map<number, number>>(new Map())
const noteInputRef = ref<InstanceType<any> | null>(null)

const hasPendingReorder = computed(() => {
  for (const item of watchlistStore.items) {
    const original = originalSortOrders.value.get(item.id)
    if (original !== undefined && original !== item.sortOrder) {
      return true
    }
  }
  return false
})

const getStockData = (code: string): Stock | undefined => {
  return marketStore.stocks.find(s => s.code === code)
}

const getStockPrice = (code: string) => {
  const stock = getStockData(code)
  return stock ? formatNumber(stock.price, 2) : '--'
}

const getStockChange = (code: string) => {
  const stock = getStockData(code)
  if (!stock) return '--'
  const symbol = getPriceSymbol(stock.change)
  return `${symbol} ${formatNumber(Math.abs(stock.change), 2)} (${formatPercent(stock.changePercent)})`
}

const getPriceColor = (code: string) => {
  const stock = getStockData(code)
  if (!stock) return 'var(--el-text-color-regular)'
  if (stock.change > 0) return 'var(--el-color-danger)'
  if (stock.change < 0) return 'var(--el-color-success)'
  return 'var(--el-text-color-regular)'
}

const startEdit = (row: WatchlistItem) => {
  editingId.value = row.id
  editNoteValue.value = row.note || ''
  nextTick(() => {
    noteInputRef.value?.focus()
    const inputEl = noteInputRef.value?.$el?.querySelector('input')
    if (inputEl) inputEl.select()
  })
}

const saveNote = async (row: WatchlistItem) => {
  if (editingId.value === null) return

  const newNote = editNoteValue.value.trim()
  const oldNote = row.note || ''

  if (newNote !== oldNote) {
    try {
      const response = await watchlistAPI.updateNote(row.id, newNote)
      if (response.code === 200) {
        watchlistStore.updateItem(row.id, { note: newNote })
        ElMessage.success('备注已更新')
      } else {
        ElMessage.error(response.message || '更新失败')
      }
    } catch (error) {
      ElMessage.error('更新失败，请重试')
    }
  }

  cancelEdit()
}

const cancelEdit = () => {
  editingId.value = null
  editNoteValue.value = ''
}

const moveUp = (index: number) => {
  if (index <= 0) return
  const items = watchlistStore.items.map(item => ({ ...item }))
  const temp = items[index]
  items[index] = items[index - 1]
  items[index - 1] = temp
  items.forEach((item, idx) => {
    item.sortOrder = idx
  })
  watchlistStore.setItems(items)
}

const moveDown = (index: number) => {
  const items = watchlistStore.items.map(item => ({ ...item }))
  if (index >= items.length - 1) return
  const temp = items[index]
  items[index] = items[index + 1]
  items[index + 1] = temp
  items.forEach((item, idx) => {
    item.sortOrder = idx
  })
  watchlistStore.setItems(items)
}

const saveReorder = async () => {
  const orders = watchlistStore.items.map(item => ({
    id: item.id,
    sortOrder: item.sortOrder
  }))

  try {
    const response = await watchlistAPI.reorder(orders)
    if (response.code === 200) {
      originalSortOrders.value = new Map(watchlistStore.items.map(i => [i.id, i.sortOrder]))
      ElMessage.success('排序已保存')
    } else {
      ElMessage.error(response.message || '保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败，请重试')
  }
}

const handleRemove = async (row: WatchlistItem) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除 "${row.name}" 吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    const response = await watchlistAPI.removeItem(row.id)
    if (response.code === 200) {
      watchlistStore.removeItem(row.id)
      originalSortOrders.value.delete(row.id)
      ElMessage.success('已删除')
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败，请重试')
    }
  }
}

const fetchWatchlist = async () => {
  try {
    watchlistStore.loading = true
    const response = await watchlistAPI.getList()
    if (response.code === 200) {
      watchlistStore.setItems(response.data)
      originalSortOrders.value = new Map(response.data.map((i: WatchlistItem) => [i.id, i.sortOrder]))
    }
  } catch (error) {
    console.error('Failed to fetch watchlist:', error)
    ElMessage.error('获取自选股列表失败')
  } finally {
    watchlistStore.loading = false
  }
}

const fetchStocks = async () => {
  if (marketStore.stocks.length === 0) {
    try {
      const response = await marketAPI.getStocks()
      if (response.code === 200) {
        marketStore.setStocks(response.data)
      }
    } catch (error) {
      console.error('Failed to fetch stocks:', error)
    }
  }
}

onMounted(async () => {
  await Promise.all([fetchWatchlist(), fetchStocks()])
})
</script>

<style scoped lang="scss">
.watchlist-container {
  padding: 24px;
}

.watchlist-section {
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--el-border-color-light);

  span {
    font-weight: 500;
    color: var(--el-text-color-primary);
  }
}

.header-actions {
  display: flex;
  gap: 8px;
}

.sort-handle {
  color: var(--el-text-color-placeholder);
  cursor: move;
  margin-right: 4px;
}

.sort-num {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.note-display {
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;

  &:hover {
    background: var(--el-fill-color-light);
  }
}

.note-placeholder {
  color: var(--el-text-color-placeholder);
  font-style: italic;
}

.price {
  font-weight: 600;
  color: var(--el-text-color-primary);
}

@media (max-width: 768px) {
  .watchlist-container {
    padding: 16px;
  }

  .watchlist-section {
    padding: 16px;
  }
}
</style>
