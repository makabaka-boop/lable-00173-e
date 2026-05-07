<template>
  <div class="watchlist-container">
    <div class="watchlist-header">
      <span>我的自选 ({{ watchlistStore.items.length }}/50)</span>
    </div>

    <div v-if="watchlistStore.loading" class="loading-wrapper">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else-if="watchlistStore.items.length === 0" class="empty-wrapper">
      <el-empty description="暂无自选股，可在行情或交易页面添加" />
    </div>

    <div v-else class="watchlist-list">
      <div
        v-for="(item, index) in watchlistStore.items"
        :key="item.id"
        class="watchlist-item"
        draggable="true"
        @dragstart="onDragStart(index, $event)"
        @dragover.prevent="onDragOver(index)"
        @drop="onDrop(index)"
      >
        <div class="item-drag">
          <el-icon><Rank /></el-icon>
        </div>
        <div class="item-main">
          <div class="item-info">
            <span class="item-name">{{ item.name }}</span>
            <span class="item-code">{{ item.code }}</span>
          </div>
          <div class="item-note">
            <el-input
              v-if="editingId === item.id"
              v-model="editNoteValue"
              size="small"
              placeholder="输入备注"
              @blur="saveNote(item)"
              @keyup.enter="saveNote(item)"
            />
            <span v-else class="note-text" @click="startEditNote(item)">
              {{ item.note || '点击添加备注' }}
            </span>
          </div>
        </div>
        <div class="item-actions">
          <el-button type="danger" size="small" link @click="handleDelete(item)">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useWatchlistStore } from '@/stores/watchlist'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Rank, Delete } from '@element-plus/icons-vue'
import type { WatchlistItem } from '@/types'

const watchlistStore = useWatchlistStore()

const editingId = ref<number | string | null>(null)
const editNoteValue = ref('')
const dragIndex = ref<number | null>(null)

const startEditNote = (item: WatchlistItem) => {
  editingId.value = item.id
  editNoteValue.value = item.note
}

const saveNote = async (item: WatchlistItem) => {
  if (editingId.value === null) return
  editingId.value = null
  if (editNoteValue.value === item.note) return
  const ok = await watchlistStore.updateNote(Number(item.id), editNoteValue.value)
  if (!ok) {
    ElMessage.error('更新备注失败')
  }
}

const handleDelete = async (item: WatchlistItem) => {
  try {
    await ElMessageBox.confirm(`确认从自选中移除 ${item.name}？`, '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    })
    const ok = await watchlistStore.deleteItem(Number(item.id))
    if (ok) {
      ElMessage.success('已移除')
    } else {
      ElMessage.error('移除失败')
    }
  } catch {
    // cancelled
  }
}

const onDragStart = (index: number, event: DragEvent) => {
  dragIndex.value = index
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
  }
}

const onDragOver = (index: number) => {
  // just allow drop
}

const onDrop = async (index: number) => {
  if (dragIndex.value === null || dragIndex.value === index) return
  const newItems = [...watchlistStore.items]
  const [moved] = newItems.splice(dragIndex.value, 1)
  newItems.splice(index, 0, moved)
  const itemIds = newItems.map(i => Number(i.id))
  await watchlistStore.reorder(itemIds)
  dragIndex.value = null
}

onMounted(() => {
  watchlistStore.fetchList()
})
</script>

<style scoped lang="scss">
.watchlist-container {
  padding: 24px;
}

.watchlist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--el-border-color-light);

  span {
    font-weight: 500;
    font-size: 16px;
    color: var(--el-text-color-primary);
  }
}

.loading-wrapper {
  padding: 24px;
  background: var(--el-bg-color);
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
}

.empty-wrapper {
  padding: 48px 24px;
  background: var(--el-bg-color);
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
}

.watchlist-list {
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.watchlist-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--el-border-color-light);
  transition: background 0.2s;
  cursor: default;

  &:last-child {
    border-bottom: none;
  }

  &:hover {
    background: var(--el-fill-color-lighter);
  }
}

.item-drag {
  cursor: grab;
  color: var(--el-text-color-placeholder);
  display: flex;
  align-items: center;
  font-size: 16px;

  &:active {
    cursor: grabbing;
  }
}

.item-main {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 16px;
}

.item-info {
  display: flex;
  align-items: baseline;
  gap: 8px;
  min-width: 160px;
}

.item-name {
  font-weight: 600;
  color: var(--el-text-color-primary);
  font-size: 14px;
}

.item-code {
  color: var(--el-text-color-regular);
  font-size: 12px;
}

.item-note {
  flex: 1;
  min-width: 0;

  .el-input {
    max-width: 300px;
  }
}

.note-text {
  color: var(--el-text-color-placeholder);
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: inline-block;
  max-width: 300px;

  &:hover {
    color: var(--el-color-primary);
  }
}

.item-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

@media (max-width: 768px) {
  .watchlist-container {
    padding: 16px;
  }

  .item-main {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
}
</style>
